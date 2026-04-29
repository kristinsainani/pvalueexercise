import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

# ---------------------------
# PAGE SETUP
# ---------------------------
st.set_page_config(page_title="Stat Misconceptions Lab", layout="centered")

st.title("🧠 Stat Misconceptions Lab")
st.write("Answer first. Then test your intuition with simulation.")

# ---------------------------
# SESSION STATE
# ---------------------------
if "q" not in st.session_state:
    st.session_state.q = 0
if "show_answer" not in st.session_state:
    st.session_state.show_answer = False

# ---------------------------
# SIMULATION FUNCTION (Q1)
# ---------------------------

def simulate_posterior_null():
    st.write("### Simulation")

    st.write(
        """
If the p-value were the probability that the null hypothesis is true,  
then among significant results, almost none should come from true nulls.

Let’s test that.
"""
    )

    # Controls
    prior_null = st.slider("Probability null is true", 0.0, 1.0, 0.5)
    n = st.slider("Sample size per group", 10, 100, 30)
    effect = st.slider("Effect size if null is false", 0.0, 1.5, 0.5)

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
        st.write("No significant results in this simulation.")
        return

    # -------- BAR CHART --------
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

    # Key number
    st.write(f"Fraction of significant results where null is true: {n_null_true / n_total:.2f}")

    # Explanation
    st.write(
        """
These are all studies with statistically significant results.

But some of them are false positives—cases where the null hypothesis was actually true.

If the p-value were the probability that the null is true,  
the "Null TRUE" bar should be near zero.

But it isn’t.

So a p-value cannot be the probability that the null hypothesis is true.
"""
    )

# ---------------------------
# QUESTIONS
# ---------------------------

questions = [
    {
        "section": "P-Values",
        "prompt": "The p-value tells you the probability that the null hypothesis is true.",
        "correct": "False",
        "explanation": """
This is false.

A p-value is not the probability that the null hypothesis is true.

A p-value tells you how surprising your data would be if the null hypothesis were true.

To get the probability that the null is true, you would also need:
- how often the null is true to begin with, and  
- how likely you are to detect real effects.

This is the same kind of mistake as saying you know the probability that your conclusion is wrong or that the alternative hypothesis is true.
""",
        "simulation": simulate_posterior_null,
    }
]

# ---------------------------
# MAIN FLOW
# ---------------------------

# Safety fix
if st.session_state.q >= len(questions):
    st.session_state.q = 0

q = questions[st.session_state.q]

st.subheader(q["section"])
st.write(f"Question {st.session_state.q + 1}")
st.write(q["prompt"])

# Answer choice
answer = st.radio("True or False?", ["True", "False"], key="q1")

# Submit button
if st.button("Submit"):
    st.session_state.show_answer = True

# ONLY show after submit
if st.session_state.show_answer:

    st.write(f"**Correct answer: {q['correct']}**")

    # Optional: show whether student was right
    if answer == q["correct"]:
        st.write("✅ Correct")
    else:
        st.write("❌ Not quite")

    st.write(q["explanation"])

    st.write("---")

    q["simulation"]()
