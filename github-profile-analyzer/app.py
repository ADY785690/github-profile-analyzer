import streamlit as st
import pandas as pd
import requests

st.set_page_config(
    page_title="AI GitHub Developer Intelligence Platform",
    layout="wide"
)

st.title("🚀 AI GitHub Developer Intelligence Platform")

st.markdown(
    "Analyze GitHub profiles, developer strength, recruiter readiness and portfolio quality."
)

username = st.text_input(
    "Enter GitHub Username",
    placeholder="e.g. torvalds"
)

if st.button("Analyze Profile"):

    profile_url = f"https://api.github.com/users/{username}"
    profile = requests.get(profile_url)

    if profile.status_code != 200:
        st.error("GitHub User Not Found")
    else:

        user = profile.json()

        followers = user["followers"]
        following = user["following"]
        repos = user["public_repos"]
        bio = user.get("bio", "No Bio")
        location = user.get("location", "Not Available")
        created = user["created_at"][:10]

        score = min(
            repos * 3 +
            followers * 2 +
            20,
            100
        )

        if score >= 80:
            level = "Professional"
        elif score >= 60:
            level = "Advanced"
        elif score >= 40:
            level = "Intermediate"
        else:
            level = "Beginner"

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Followers", followers)
        col2.metric("Repositories", repos)
        col3.metric("Developer Score", score)
        col4.metric("Profile Level", level)

        st.divider()

        st.subheader("👤 Profile Details")

        st.write("**Username:**", username)
        st.write("**Bio:**", bio)
        st.write("**Location:**", location)
        st.write("**Following:**", following)
        st.write("**Account Created:**", created)

        st.divider()

        repos_url = f"https://api.github.com/users/{username}/repos"
        repos_data = requests.get(repos_url).json()

        repo_names = []
        stars = []
        forks = []
        languages = {}

        for repo in repos_data:

            repo_names.append(repo["name"])
            stars.append(repo["stargazers_count"])
            forks.append(repo["forks_count"])

            lang = repo["language"]

            if lang:
                languages[lang] = languages.get(lang, 0) + 1

        st.subheader("📁 Repository Analysis")

        repo_df = pd.DataFrame({
            "Repository": repo_names,
            "Stars": stars,
            "Forks": forks
        })

        st.dataframe(repo_df)

        st.divider()

        st.subheader("⭐ Project Quality Metrics")

        total_stars = sum(stars)
        total_forks = sum(forks)

        c1, c2, c3 = st.columns(3)

        c1.metric("Total Stars", total_stars)
        c2.metric("Total Forks", total_forks)
        c3.metric("Public Projects", repos)

        st.divider()

        st.subheader("💻 Language Distribution")

        if languages:

            lang_df = pd.DataFrame({
                "Language": languages.keys(),
                "Projects": languages.values()
            })

            st.bar_chart(
                lang_df.set_index("Language")
            )

        st.divider()

        st.subheader("🎯 Recruiter Readiness")

        readiness = min(
            repos * 5 +
            followers +
            20,
            100
        )

        st.progress(readiness / 100)

        st.success(
            f"Recruiter Readiness Score: {readiness}%"
        )

        st.divider()

        st.subheader("📋 Portfolio Health Check")

        checks = []

        if repos >= 5:
            checks.append("✅ Good Number of Projects")
        else:
            checks.append("❌ Add More Projects")

        if followers >= 10:
            checks.append("✅ Community Presence")
        else:
            checks.append("❌ Increase GitHub Activity")

        if bio != "No Bio":
            checks.append("✅ Bio Available")
        else:
            checks.append("❌ Add Professional Bio")

        for item in checks:
            st.write(item)

        st.divider()

        st.subheader("🚀 Career Recommendations")

        careers = []

        if "Python" in languages:
            careers.append("ML Engineer")
            careers.append("Data Analyst")

        if "JavaScript" in languages:
            careers.append("Frontend Developer")

        if "Java" in languages:
            careers.append("Software Engineer")

        if not careers:
            careers.append("Software Engineer")

        for career in careers:
            st.success(career)

        st.divider()

        st.subheader("📈 Improvement Suggestions")

        suggestions = [
            "Add detailed README files",
            "Deploy more projects",
            "Increase GitHub activity",
            "Build AI/Data Science projects",
            "Add project documentation"
        ]

        for s in suggestions:
            st.write("•", s)

        report = pd.DataFrame({
            "Metric": [
                "Developer Score",
                "Recruiter Readiness",
                "Repositories",
                "Followers"
            ],
            "Value": [
                score,
                readiness,
                repos,
                followers
            ]
        })

        csv = report.to_csv(index=False)

        st.download_button(
            label="📥 Download Report",
            data=csv,
            file_name="github_analysis_report.csv",
            mime="text/csv"
        )

else:
    st.info("Enter GitHub username and click Analyze Profile")
