import streamlit as st

st.title("🚀 GitHub Profile Analyzer")

username = st.text_input("Enter GitHub Username")

if username:
    st.success(f"Analyzing {username}")

    repo_count = 5
    score = min(repo_count * 20, 100)

    st.metric("GitHub Score", score)

    if score > 80:
        st.success("Excellent Profile")
    elif score > 50:
        st.warning("Good Profile")
    else:
        st.error("Needs Improvement")
