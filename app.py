import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Set page config
st.set_page_config(page_title="Sportsphere", layout="wide", page_icon="🏀")

# Sidebar navigation
st.sidebar.title("Sportsphere Navigation")
tabs = [
    "🏠 Feed", "📊 Cricket Scores", "🏀 Multi-Sport Scores", "🧮 Start Scoring",
    "🏆 Start a Tournament", "📋 My Matches", "👥 My Teams", "📈 My Stats",
    "🎬 Highlights", "🧑‍💻 Create Account", "🛒 Shop", "🧍‍♂️ Profile",
    "🌐 Change Language", "🔗 Share App", "🆘 Help & Support", "📧 Contact Us"
]
selected_tab = st.sidebar.selectbox("Select Tab", tabs)

# Function to load CSV data with error handling
@st.cache_data
def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        st.error(f"Data file {file_path} not found. Please run generate_data.py first.")
        return pd.DataFrame()

# Load all datasets
data_files = {
    "Feed": "data/feed.csv",
    "Cricket Scores": "data/cricket_scores.csv",
    "Multi-Sport Scores": "data/multi_sport_scores.csv",
    "Start Scoring": "data/start_match.csv",
    "Start a Tournament": "data/tournament.csv",
    "My Matches": "data/my_matches.csv",
    "My Teams": "data/my_teams.csv",
    "My Stats": "data/my_stats.csv",
    "Highlights": "data/highlights.csv",
    "Create Account": "data/create_account.csv",
    "Shop": "data/shop.csv",
    "Profile": "data/profile.csv",
    "Change Language": "data/language.csv",
    "Share App": "data/share_app.csv",
    "Help & Support": "data/help_support.csv",
    "Contact Us": "data/contact_us.csv"
}
data = {key: load_data(path) for key, path in data_files.items()}

# Display content based on selected tab
st.title("Sportsphere")
st.markdown(f"### {selected_tab}")

if selected_tab == "🏠 Feed":
    st.write("Activity feed updates (match results, tournament announcements, MVPs)")
    if not data["Feed"].empty:
        st.dataframe(data["Feed"], use_container_width=True)
        # Visualization: Event type distribution
        fig = px.histogram(data["Feed"], x="event_type", title="Event Type Distribution")
        st.plotly_chart(fig)

elif selected_tab == "📊 Cricket Scores":
    st.write("Live and recent cricket match scores")
    if not data["Cricket Scores"].empty:
        st.dataframe(data["Cricket Scores"], use_container_width=True)
        # Visualization: Score distribution
        fig = px.histogram(data["Cricket Scores"], x="score_team1", title="Team 1 Score Distribution")
        st.plotly_chart(fig)

elif selected_tab == "🏀 Multi-Sport Scores":
    st.write("Live and recent scores for football, basketball, and badminton")
    if not data["Multi-Sport Scores"].empty:
        st.dataframe(data["Multi-Sport Scores"], use_container_width=True)
        # Visualization: Scores by sport
        fig = px.box(data["Multi-Sport Scores"], x="sport_name", y="score1", title="Score Distribution by Sport")
        st.plotly_chart(fig)

elif selected_tab == "🧮 Start Scoring":
    st.write("Create and manage new matches")
    if not data["Start Scoring"].empty:
        st.dataframe(data["Start Scoring"], use_container_width=True)

elif selected_tab == "🏆 Start a Tournament":
    st.write("Create and manage tournaments")
    if not data["Start a Tournament"].empty:
        st.dataframe(data["Start a Tournament"], use_container_width=True)

elif selected_tab == "📋 My Matches":
    st.write("Matches for a user (as player, scorer, or spectator)")
    if not data["My Matches"].empty:
        st.dataframe(data["My Matches"], use_container_width=True)
        # Visualization: Role distribution
        fig = px.pie(data["My Matches"], names="role", title="User Role Distribution")
        st.plotly_chart(fig)

elif selected_tab == "👥 My Teams":
    st.write("Teams with rosters")
    if not data["My Teams"].empty:
        st.dataframe(data["My Teams"], use_container_width=True)

elif selected_tab == "📈 My Stats":
    st.write("Player statistics (batting, bowling, fielding)")
    if not data["My Stats"].empty:
        st.dataframe(data["My Stats"], use_container_width=True)
        # Visualization: Runs scored vs. matches played
        fig = px.scatter(data["My Stats"], x="matches_played", y="runs_scored", title="Runs Scored vs. Matches Played")
        st.plotly_chart(fig)

elif selected_tab == "🎬 Highlights":
    st.write("Match highlight clips and images")
    if not data["Highlights"].empty:
        st.dataframe(data["Highlights"], use_container_width=True)

elif selected_tab == "🧑‍💻 Create Account":
    st.write("User registration data")
    if not data["Create Account"].empty:
        st.dataframe(data["Create Account"], use_container_width=True)
        # Visualization: Gender distribution
        fig = px.pie(data["Create Account"], names="gender", title="Gender Distribution")
        st.plotly_chart(fig)

elif selected_tab == "🛒 Shop":
    st.write("Store products")
    if not data["Shop"].empty:
        st.dataframe(data["Shop"], use_container_width=True)
        # Visualization: Price distribution
        fig = px.histogram(data["Shop"], x="price", title="Product Price Distribution")
        st.plotly_chart(fig)

elif selected_tab == "🧍‍♂️ Profile":
    st.write("User profiles with stats and history")
    if not data["Profile"].empty:
        st.dataframe(data["Profile"], use_container_width=True)

elif selected_tab == "🌐 Change Language":
    st.write("Available languages")
    if not data["Change Language"].empty:
        st.dataframe(data["Change Language"], use_container_width=True)

elif selected_tab == "🔗 Share App":
    st.write("App share events")
    if not data["Share App"].empty:
        st.dataframe(data["Share App"], use_container_width=True)
        # Visualization: Platform distribution
        fig = px.pie(data["Share App"], names="platform", title="Share Platform Distribution")
        st.plotly_chart(fig)

elif selected_tab == "🆘 Help & Support":
    st.write("Support tickets and help logs")
    if not data["Help & Support"].empty:
        st.dataframe(data["Help & Support"], use_container_width=True)
        # Visualization: Issue type distribution
        fig = px.histogram(data["Help & Support"], x="issue_type", title="Issue Type Distribution")
        st.plotly_chart(fig)

elif selected_tab == "📧 Contact Us":
    st.write("Contact form submissions")
    if not data["Contact Us"].empty:
        st.dataframe(data["Contact Us"], use_container_width=True)

# Footer
st.markdown("---")
st.write("Sportsphere - Sports Management App | Developed for Streamlit Cloud")
