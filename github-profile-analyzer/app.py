import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.set_page_config(
    page_title="GitHub Developer Intelligence Platform",
    layout="wide"
)

st.title("🚀 GitHub Developer Intelligence Platform")

st.markdown(
    "Analyze GitHub profiles, recruiter readiness, portfolio quality and career opportunities."
)

username = st.text_input(
    "Enter GitHub Username",
    placeholder="e.g. torvalds"
)

if st.button("Analyze Profile"):

    profile_url = f"https://api.github.com/users/{username}"

    response = requests.get(profile_url)

    if response.status_code != 200:
        st.error("GitHub User Not Found")
        st.stop()

    user = response.json()

    followers = user.get("followers", 0)
    following = user.get("following", 0)
    repos = user.get("public_repos", 0)
    bio = user.get("bio") or "No Bio Available"
    location = user.get("location") or "Not Available"
    created = user.get("created_at", "")[:10]

    repos_url = f"https://api.github.com/users/{username}/repos"
    repos_response = requests.get(repos_url)

    repos_data = repos_response.json()

    repo_names = []
    stars = []
    forks = []
    languages = {}

    for repo in repos_data:

        repo_names.append(repo["name"])

        stars.append(
            repo.get("stargazers_count", 0)
        )

        forks.append(
            repo.get("forks_count", 0)
        )

        lang = repo.get("language")

        if lang:
            languages[lang] = (
                languages.get(lang, 0) + 1
            )

    total_stars = sum(stars)
    total_forks = sum(forks)

    developer_score = min(
        (
            repos * 4
            + followers * 2
            + min(total_stars, 20)
            + 20
        ),
        100
    )

    recruiter_score = min(
        (
            repos * 5
            + followers * 2
            + min(total_stars, 20)
            + 20
        ),
        100
    )

    quality_score = min(
        (
            repos * 4
            + total_stars * 2
            + total_forks
        ),
        100
    )

    if developer_score >= 80:
        level = "Professional"
    elif developer_score >= 60:
        level = "Advanced"
    elif developer_score >= 40:
        level = "Intermediate"
    else:
        level = "Beginner"

    st.subheader("📊 Developer Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Developer Score",
        f"{developer_score}/100"
    )

    col2.metric(
        "Recruiter Readiness",
        f"{recruiter_score}%"
    )

    col3.metric(
        "Repository Quality",
        f"{quality_score}/100"
    )

    col4.metric(
        "Level",
        level
    )

    st.divider()

    st.subheader("👤 Profile Information")

    st.write(f"**Username:** {username}")
    st.write(f"**Bio:** {bio}")
    st.write(f"**Location:** {location}")
    st.write(f"**Followers:** {followers}")
    st.write(f"**Following:** {following}")
    st.write(f"**Public Repositories:** {repos}")
    st.write(f"**Account Created:** {created}")

    st.divider()

    st.subheader("💻 Language Intelligence")

    if languages:

        lang_df = pd.DataFrame({
            "Language": list(languages.keys()),
            "Projects": list(languages.values())
        })

        fig = px.pie(
            lang_df,
            names="Language",
            values="Projects",
            title="Language Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    st.subheader("📁 Repository Analysis")

    repo_df = pd.DataFrame({
        "Repository": repo_names,
        "Stars": stars,
        "Forks": forks
    })

    st.dataframe(repo_df)

    st.divider()

    st.subheader("🥇 Top Repositories")

    top_projects = repo_df.sort_values(
        by="Stars",
        ascending=False
    ).head(5)

    st.dataframe(top_projects)

    st.divider()

    st.subheader("🩺 Portfolio Health Check")

    checks = []

    if repos >= 5:
        checks.append("✅ Good number of projects")
    else:
        checks.append("❌ Add more projects")

    if bio != "No Bio Available":
        checks.append("✅ Professional bio present")
    else:
        checks.append("❌ Add GitHub bio")

    if total_stars > 0:
        checks.append("✅ Community engagement present")
    else:
        checks.append("❌ Increase project visibility")

    for item in checks:
        st.write(item)

    st.divider()

    st.subheader("🚀 Career Recommendation Engine")

    career_scores = {
        "Data Analyst": 0,
        "ML Engineer": 0,
        "Software Engineer": 0,
        "Data Engineer": 0
    }

    if "Python" in languages:
        career_scores["ML Engineer"] += 30
        career_scores["Data Analyst"] += 25
        career_scores["Data Engineer"] += 20

    if "JavaScript" in languages:
        career_scores["Software Engineer"] += 30

    if "Java" in languages:
        career_scores["Software Engineer"] += 25

    if repos > 5:
        for role in career_scores:
            career_scores[role] += 20

    career_df = pd.DataFrame({
        "Role": list(career_scores.keys()),
        "Score": list(career_scores.values())
    })

    career_chart = px.bar(
        career_df,
        x="Role",
        y="Score",
        title="Career Match Analysis"
    )

    st.plotly_chart(
        career_chart,
        use_container_width=True
    )

    st.divider()

    st.subheader("📈 Improvement Suggestions")

    suggestions = [
        "Add deployed projects",
        "Improve README documentation",
        "Increase GitHub activity",
        "Build more AI/Data projects",
        "Add project screenshots"
    ]

    for s in suggestions:
        st.write("•", s)

    report = pd.DataFrame({
        "Metric": [
            "Developer Score",
            "Recruiter Readiness",
            "Repository Quality",
            "Repositories",
            "Followers"
        ],
        "Value": [
            developer_score,
            recruiter_score,
            quality_score,
            repos,
            followers
        ]
    })

    csv = report.to_csv(index=False)

    st.download_button(
        label="📥 Download Analysis Report",
        data=csv,
        file_name="github_developer_report.csv",
        mime="text/csv"
    )

else:
    st.info(
        "Enter a GitHub username and click Analyze Profile"
    )
