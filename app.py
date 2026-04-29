import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind, t

# ---------------------------
# PAGE SETUP
# ---------------------------
st.set_page_config(page_title="Stat Misconceptions Lab", layout="centered")

st.title("🧠 Stat Misconceptions Lab")
st.write("Answer first. Then we’ll test your intuition with simulation.")

# ---------------------------
# SESSION STATE
# ---------------------------
if "q" not in st.session_state:
    st.session_state.q = 0
if "show_answer" not in st.session_state:
    st.session_state.show_answer = False

# ---------------------------
# SIMULATIONS
# ---------------------------

def simulate_pvalue_replication():
    np.random.seed(1)
    n_sims = 1000
    n = 20
    alpha = 0.05

    pvals = []

    for _ in range(n_sims):
        group1 = np.random.normal(0, 1, n)
        group2 = np.random.normal(0, 1, n)  # no real difference
        _, p = ttest_ind(group1, group2)
        pvals.append(p)

    pvals = np.array(pvals)
    sig_rate = np.mean(pvals < alpha)

    fig, ax = plt.subplots()
    ax.hist(pvals, bins=20)
    ax.axvline(alpha)
    ax.set_title("Distribution of p-values (null is TRUE)")
    ax.set_xlabel("p-value")
    ax.set_ylabel("Count")
    st.pyplot(fig)

    st.write(f"**Percent significant (p < 0.05): {sig_rate:.3f}**")

    st.write(
        "Even when there is NO real effect, you still get significant results about 5% of the time."
    )


def simulate_ci_coverage():
    np.random.seed(1)
    n_sims = 100
    n = 20
    true_mean = 0

    contains = []

    fig, ax = plt.subplots()

    for i in range(n_sims):
        data = np.random.normal(true_mean, 1, n)
        m = np.mean(data)
        s = np.std(data, ddof=1)
        se = s / np.sqrt(n)
        t_crit = t.ppf(0.975, df=n-1)

        lower = m - t_crit * se
        upper = m + t_crit * se

        hit = (lower <= true_mean) and (upper >= true_mean)
        contains.append(hit)

        color = "green" if hit else "red"
        ax.plot([lower, upper], [i, i], color=color)

    ax.axvline(true_mean)
    ax.set_title("95% Confidence Intervals Across Repeated Samples")
    ax.set_xlabel("Value")
    ax.set_ylabel("Simulation #")

    st.pyplot(fig)

    coverage = np.mean(contains)
    st.write(f"**Coverage: {coverage:.2f}**")

    st.write(
        "The true mean is fixed. The intervals move. About 95% of intervals capture the truth."
    )

# ---------------------------
# QUESTIONS
# ---------------------------

questions = [
    {
        "prompt": "If p = 0.01, then 99% of repeated studies will also be significant.",
        "correct": "False",
        "explanation": "A p-value does NOT tell you how often results will replicate. It only describes how surprising your data are under the null.",
        "simulation": simulate_pvalue_replication,
    },
    {
        "prompt": "There is a 95% probability that the true mean lies inside a 95% confidence interval.",
        "correct": "False",
        "explanation": "The true value is fixed. The interval changes. 95% refers to long-run coverage, not probability for this specific interval.",
        "simulation": simulate_ci_coverage,
    },
]

# ---------------------------
# MAIN FLOW
# ---------------------------

q = questions[st.session_state.q]

st.subheader(f"Question {st.session_state.q + 1}")
st.write(q["prompt"])

answer = st.radio("True or False?", ["True", "False"], key=f"q{st.session_state.q}")

if st.button("Submit"):
    st.session_state.show_answer = True

if st.session_state.show_answer:
    st.write(f"**Correct answer: {q['correct']}**")
    st.write(q["explanation"])

    st.write("---")
    st.write("### Simulation")
    q["simulation"]()

    if st.session_state.q < len(questions) - 1:
        if st.button("Next"):
            st.session_state.q += 1
            st.session_state.show_answer = False
    else:
        st.write("🎉 Done!")
