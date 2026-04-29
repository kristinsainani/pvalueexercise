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
if "answered" not in st.session_state:
    st.session_state.answered = False

# ---------------------------
# SIMULATION (Q1)
# ---------------------------
def run_simulation():
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
        st.write("No significant results—try increasing sample size or effect.")
        return

    # Bar chart
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

    st.write(f"Fraction where null is actually true: {n_null_true / n_total:.2f}")

    st.write(
        """
These are all statistically significant results.

But some are false positives—cases where the null hypothesis was actually true.

If the p-value were the probability that the null is true,  
the "Null TRUE" bar should be near zero.

But it isn’t.

So a p-value cannot be the probability that the null hypothesis is true.
"""
    )

# ---------------------------
# QUESTION
# ---------------------------

st.subheader("P-Values")
st.write("**Question 1**")

st.write(
    "The p-value tells you the probability that the null hypothesis is true."
)

answer = st.radio("True or False?", ["True", "False"])

# Submit
if st.button("Submit"):
    st.session_state.answered = True

# Show results only after answering
if st.session_state.answered:

    st.write("**Correct answer: False**")

    if answer == "False":
        st.write("✅ Correct")
    else:
        st.write("❌ Not quite")

    st.write(
        """
A p-value is not the probability that the null hypothesis is true.

A p-value tells you how surprising your data would be if the null hypothesis were true.

To get the probability that the null is true, you would also need:
- how often the null is true to begin with, and  
- how likely you are to detect real effects.

This is the same mistake as saying you know the probability that your conclusion is wrong or that the alternative hypothesis is true.
"""
    )

    st.write("---")

    run_simulation()

# Reset button (useful while building)
if st.button("Reset"):
    st.session_state.answered = False
