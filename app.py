import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

# ---------------------------
# PAGE SETUP
# ---------------------------
st.set_page_config(page_title="Stat Misconceptions Lab", layout="centered")

st.title("🧠 Stat Misconceptions Lab")
st.write("Answer the question first, then explore the simulation.")

# ---------------------------
# SESSION STATE
# ---------------------------
if "q" not in st.session_state:
    st.session_state.q = 0
if "answered" not in st.session_state:
    st.session_state.answered = False

# ---------------------------
# SIMULATION 1 (Q1 & Q2)
# ---------------------------
def simulation_false_positive():

    st.write("### Simulation")

    st.write(
        """
If the p-value told you the probability that the null is true or that you're wrong,  
then false positives should be very rare among significant results.

Let’s test that.
"""
    )

    prior_null = st.slider("Probability null is true", 0.0, 1.0, 0.9)
    n = st.slider("Sample size per group", 10, 100, 20)
    effect = st.slider("Effect size if null is false", 0.0, 1.5, 0.3)

    n_sims = 1000
    alpha = 0.05

    results = []

    for _ in range(n_sims):
        null_true = np.random.rand() < prior_null

        if null_true:
            g1 = np.random.normal(0, 1, n)
            g2 = np.random.normal(0, 1, n)
        else:
            g1 = np.random.normal(effect, 1, n)
            g2 = np.random.normal(0, 1, n)

        _, p = ttest_ind(g1, g2)

        if p < alpha:
            results.append(null_true)

    results = np.array(results)

    if len(results) == 0:
        st.write("No significant results—try adjusting settings.")
        return

    n_total = len(results)
    n_null_true = np.sum(results)
    n_null_false = n_total - n_null_true

    fig, ax = plt.subplots()

    labels = ["Null TRUE\n(False Positives)", "Null FALSE\n(True Effects)"]
    values = [n_null_true, n_null_false]

    ax.bar(labels, values)
    ax.set_title("Among Significant Results (p < 0.05)")
    ax.set_ylabel("Number of studies")

    st.pyplot(fig)

    st.write(f"Fraction of significant results where null is true: {n_null_true / n_total:.2f}")

    st.write(
        """
These are all statistically significant results.

But some are false positives—cases where the null hypothesis was actually true.

So even after getting a significant result,  
there can still be a substantial chance that you're wrong.
"""
    )

# ---------------------------
# SIMULATION 2 (Q3)
# ---------------------------
def simulation_replication():

    st.write("### Simulation")

    st.write(
        """
If a significant result guaranteed replication,  
then repeated studies should almost always be significant.

Let’s test that.
"""
    )

    n = st.slider("Sample size per group", 10, 100, 30)
    effect = st.slider("True effect size", 0.0, 1.5, 0.5)

    n_sims = 500
    alpha = 0.05

    significant = []

    for _ in range(n_sims):
        g1 = np.random.normal(effect, 1, n)
        g2 = np.random.normal(0, 1, n)

        _, p = ttest_ind(g1, g2)
        significant.append(p < alpha)

    significant = np.array(significant)

    prop_sig = np.mean(significant)

    fig, ax = plt.subplots()

    labels = ["Significant", "Not Significant"]
    values = [np.sum(significant), np.sum(~significant)]

    ax.bar(labels, values)
    ax.set_title("Results Across Repeated Studies")
    ax.set_ylabel("Number of studies")

    st.pyplot(fig)

    st.write(f"Proportion significant: {prop_sig:.2f}")

    st.write(
        """
Even with a real effect, not all studies are significant.

So a single significant result does not mean future studies will almost always replicate.
"""
    )

# ---------------------------
# QUESTIONS
# ---------------------------
questions = [

    # Q1
    {
        "section": "P-Values",
        "prompt": "The p-value tells you the probability that the null hypothesis is true.",
        "correct": "False",
        "explanation": """
A p-value is not the probability that the null hypothesis is true.

It tells you how surprising your data would be if the null hypothesis were true.

This is the same mistake as saying you know the probability you're wrong or that the alternative hypothesis is true.
""",
        "simulation": simulation_false_positive
    },

    # Q2
    {
        "section": "P-Values",
        "prompt": "If you reject the null hypothesis, you know the probability that you are making the wrong decision.",
        "correct": "False",
        "explanation": """
A p-value does not tell you the probability that your conclusion is wrong.

The simulation shows that among significant results,  
some are still false positives.

This is the same mistake as saying you know:
- the probability the null is true, or  
- the probability the alternative is true.
""",
        "simulation": simulation_false_positive
    },

    # Q3
    {
        "section": "P-Values",
        "prompt": "If a result is significant at p = 0.01, then repeated studies will be significant about 99% of the time.",
        "correct": "False",
        "explanation": """
A p-value does not tell you how often results will replicate.

Even when a real effect exists, results vary from study to study.

So a single significant result does not guarantee consistent replication.
""",
        "simulation": simulation_replication
    }

]

# ---------------------------
# MAIN FLOW
# ---------------------------

if st.session_state.q >= len(questions):
    st.session_state.q = 0

q = questions[st.session_state.q]

st.subheader(q["section"])
st.write(f"**Question {st.session_state.q + 1}**")
st.write(q["prompt"])

answer = st.radio("True or False?", ["True", "False"], key=f"q{st.session_state.q}")

if st.button("Submit"):
    st.session_state.answered = True

if st.session_state.answered:

    st.write(f"**Correct answer: {q['correct']}**")

    if answer == q["correct"]:
        st.write("✅ Correct")
    else:
        st.write("❌ Not quite")

    st.write(q["explanation"])

    st.write("---")

    q["simulation"]()

    if st.session_state.q < len(questions) - 1:
        if st.button("Next Question"):
            st.session_state.q += 1
            st.session_state.answered = False

if st.button("Reset"):
    st.session_state.q = 0
    st.session_state.answered = False
