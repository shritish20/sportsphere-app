import streamlit as st
import pandas as pd
import plotly.express as px
import os
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

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

# --- Data Generation Logic (MOVED HERE) ---
@st.cache_data
def generate_all_data():
    # Initialize Faker
    fake = Faker()

    # Set random seed
    np.random.seed(42)
    random.seed(42)

    # Helper functions
    def random_date(start_date, end_date):
        time_delta = end_date - start_date
        random_days = random.randint(0, time_delta.days)
        return start_date + timedelta(days=random_days)

    def random_timestamp(start_date, end_date):
        time_delta = end_date - start_date
        random_seconds = random.randint(0, int(time_delta.total_seconds()))
        return start_date + timedelta(seconds=random_seconds)

    # Constants
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 6, 24) # Note: Current date is June 24, 2025, so end_date is relevant
    sports = ['Cricket', 'Football', 'Basketball', 'Badminton']
    team_names = [
        'Mumbai Mavericks', 'Delhi Dynamos', 'Chennai Chargers', 'Bangalore Blasters',
        'Kolkata Knights', 'Hyderabad Hawks', 'Pune Panthers', 'Ahmedabad Avengers'
    ]
    venues = ['Wankhede Stadium', 'Eden Gardens', 'Chinnaswamy Stadium', 'Lords Arena', 'MCG', 'Oval']
    match_formats = ['T20', 'ODI', 'Test']
    tournament_formats = ['Knockout', 'Round-robin']
    languages = [('en', 'English', True), ('hi', 'Hindi', False), ('es', 'Spanish', False)]
    roles = ['Player', 'Scorer', 'Organizer', 'Spectator']
    issue_types = ['Bug', 'Feature Request', 'Payment Issue', 'Other']
    platforms = ['WhatsApp', 'Twitter', 'Facebook', 'Email']

    # Create all DataFrames
    feed_data = {
        'timestamp': [random_timestamp(start_date, end_date) for _ in range(500)],
        'event_type': [random.choice(['Match Result', 'Tournament Announcement', 'MVP Award']) for _ in range(500)],
        'user_name': [fake.name() for _ in range(500)],
        'team_name': [random.choice(team_names) for _ in range(500)],
        'match_id': [f'MID_{i:05d}' for i in range(1, 501)],
        'message': [f"{random.choice(['Won by', 'Lost by', 'Declared MVP'])} {random.randint(1, 100)} {random.choice(['runs', 'wickets', 'points'])}" for _ in range(500)]
    }
    feed_df = pd.DataFrame(feed_data)

    cricket_scores_data = {
        'match_id': [f'MID_{i:05d}' for i in range(1, 301)],
        'team1_name': [random.choice(team_names) for _ in range(300)],
        'team2_name': [random.choice(team_names) for _ in range(300)],
        'score_team1': [random.randint(50, 350) for _ in range(300)],
        'score_team2': [random.randint(50, 350) for _ in range(300)],
        'overs': [f"{random.randint(1, 50)}.{random.randint(0, 5)}" for _ in range(300)],
        'wickets': [random.randint(0, 10) for _ in range(300)],
        'status': [random.choice(['Live', 'Completed', 'Upcoming']) for _ in range(300)],
        'current_inning': [random.choice([1, 2]) for _ in range(300)],
        'location': [random.choice(venues) for _ in range(300)],
        'match_date': [random_date(start_date, end_date) for _ in range(300)]
    }
    cricket_scores_df = pd.DataFrame(cricket_scores_data)

    multi_sport_scores_data = {
        'sport_name': [random.choice(sports[1:]) for _ in range(300)],
        'match_id': [f'MID_{i:05d}' for i in range(501, 801)],
        'team1': [random.choice(team_names) for _ in range(300)],
        'team2': [random.choice(team_names) for _ in range(300)],
        'score1': [random.randint(0, 100) for _ in range(300)],
        'score2': [random.randint(0, 100) for _ in range(300)],
        'time_elapsed': [f"{random.randint(0, 90)}:{random.randint(0, 59):02d}" for _ in range(300)],
        'status': [random.choice(['Live', 'Completed', 'Upcoming']) for _ in range(300)]
    }
    multi_sport_scores_df = pd.DataFrame(multi_sport_scores_data)

    start_match_data = {
        'match_id': [f'MID_{i:05d}' for i in range(801, 901)],
        'sport_type': [random.choice(sports) for _ in range(100)],
        'teams': [[random.choice(team_names), random.choice(team_names)] for _ in range(100)],
        'start_time': [random_timestamp(start_date, end_date) for _ in range(100)],
        'venue': [random.choice(venues) for _ in range(100)],
        'umpires': [fake.name() for _ in range(100)],
        'scorers': [fake.name() for _ in range(100)],
        'match_format': [random.choice(match_formats) for _ in range(100)],
        'number_of_overs': [random.choice([20, 50, None]) for _ in range(100)],
        'status': [random.choice(['Scheduled', 'In Progress', 'Completed']) for _ in range(100)]
    }
    start_match_df = pd.DataFrame(start_match_data)

    tournament_data = {
        'tournament_id': [f'TID_{i:05d}' for i in range(1, 51)],
        'name': [f"{fake.word().capitalize()} Cup {random.randint(2024, 2025)}" for _ in range(50)],
        'organizer': [fake.name() for _ in range(50)],
        'start_date': [random_date(start_date, end_date) for _ in range(50)],
        'end_date': [random_date(start_date, end_date) + timedelta(days=random.randint(5, 30)) for _ in range(50)],
        'teams_list': [random.sample(team_names, k=random.randint(4, 8)) for _ in range(50)],
        'location': [random.choice(venues) for _ in range(50)],
        'match_ids': [[f'MID_{i:05d}' for i in range(j, j+random.randint(5, 15))] for j in range(1, 1000, 20)][:50],
        'format': [random.choice(tournament_formats) for _ in range(50)]
    }
    tournament_df = pd.DataFrame(tournament_data)

    my_matches_data = {
        'user_id': [f'UID_{i:05d}' for i in range(1, 1001)],
        'match_id': [random.choice([f'MID_{i:05d}' for i in range(1, 901)]) for _ in range(1000)],
        'role': [random.choice(roles) for _ in range(1000)],
        'participation_status': [random.choice(['Confirmed', 'Pending', 'Declined']) for _ in range(1000)],
        'result': [random.choice(['Won', 'Lost', 'Draw', 'Ongoing']) for _ in range(1000)],
        'date': [random_date(start_date, end_date) for _ in range(1000)],
        'performance_summary': [f"{random.randint(0, 100)} runs, {random.randint(0, 5)} wickets" for _ in range(1000)]
    }
    my_matches_df = pd.DataFrame(my_matches_data)

    my_teams_data = {
        'team_id': [f'TEAM_{i:05d}' for i in range(1, 201)],
        'team_name': [random.choice(team_names) for _ in range(200)],
        'created_by': [fake.name() for _ in range(200)],
        'sport_type': [random.choice(sports) for _ in range(200)],
        'players_list': [[fake.name() for _ in range(random.randint(5, 15))] for _ in range(200)],
        'rating': [round(random.uniform(1, 5), 1) for _ in range(200)],
        'wins': [random.randint(0, 50) for _ in range(200)],
        'losses': [random.randint(0, 50) for _ in range(200)],
        'logo_url': [f"https://sportsphere.com/logos/team_{i}.png" for i in range(1, 201)],
        'captain_id': [f'UID_{random.randint(1, 10000):05d}' for _ in range(200)]
    }
    my_teams_df = pd.DataFrame(my_teams_data)

    my_stats_data = {
        'player_id': [f'UID_{i:05d}' for i in range(1, 1001)],
        'matches_played': [random.randint(0, 50) for _ in range(1000)],
        'runs_scored': [random.randint(0, 2000) for _ in range(1000)],
        'wickets_taken': [random.randint(0, 100) for _ in range(1000)],
        'catches': [random.randint(0, 50) for _ in range(1000)],
        'strike_rate': [round(random.uniform(50, 200), 1) for _ in range(1000)],
        'economy': [round(random.uniform(3, 10), 1) for _ in range(1000)],
        'average': [round(random.uniform(10, 50), 1) for _ in range(1000)],
        'MVP_count': [random.randint(0, 10) for _ in range(1000)]
    }
    my_stats_df = pd.DataFrame(my_stats_data)

    highlights_data = {
        'match_id': [random.choice([f'MID_{i:05d}' for i in range(1, 901)]) for _ in range(200)],
        'media_type': [random.choice(['Video', 'Image']) for _ in range(200)],
        'timestamp': [random_timestamp(start_date, end_date) for _ in range(200)],
        'player': [fake.name() for _ in range(200)],
        'event_description': [f"{random.choice(['Six', 'Wicket', 'Catch'])} by {fake.name()}" for _ in range(200)],
        'url': [f"https://sportsphere.com/highlights/{i}.mp4" for i in range(1, 201)]
    }
    highlights_df = pd.DataFrame(highlights_data)

    create_account_data = {
        'user_id': [f'UID_{i:05d}' for i in range(1, 10001)],
        'name': [fake.name() for _ in range(10000)],
        'email': [fake.email() for _ in range(10000)],
        'phone': [fake.phone_number() for _ in range(10000)],
        'gender': [random.choice(['Male', 'Female', 'Other']) for _ in range(10000)],
        'birthdate': [random_date(datetime(1980, 1, 1), datetime(2005, 1, 1)) for _ in range(10000)],
        'location': [random.choice(venues) for _ in range(10000)],
        'joined_date': [random_date(start_date, end_date) for _ in range(10000)],
        'sports_interested_in': [random.sample(sports, k=random.randint(1, 4)) for _ in range(10000)],
        'role': [random.choice(roles) for _ in range(10000)]
    }
    create_account_df = pd.DataFrame(create_account_data)

    shop_data = {
        'product_id': [f'PROD_{i:05d}' for i in range(1, 101)],
        'name': [f"{random.choice(['Bat', 'Ball', 'Jersey', 'Shoes'])} {fake.word().capitalize()}" for _ in range(100)],
        'price': [round(random.uniform(10, 200), 2) for _ in range(100)],
        'category': [random.choice(['Equipment', 'Apparel', 'Accessories']) for _ in range(100)],
        'description': [fake.sentence() for _ in range(100)],
        'image_url': [f"https://sportsphere.com/products/{i}.png" for i in range(1, 101)],
        'inventory_count': [random.randint(0, 1000) for _ in range(100)],
        'ratings': [round(random.uniform(1, 5), 1) for _ in range(100)],
        'sold_count': [random.randint(0, 500) for _ in range(100)]
    }
    shop_df = pd.DataFrame(shop_data)

    profile_data = {
        'user_id': [f'UID_{i:05d}' for i in range(1, 10001)],
        'name': [fake.name() for _ in range(10000)],
        'photo_url': [f"https://sportsphere.com/profiles/{i}.png" for i in range(1, 10001)],
        'teams_joined': [random.sample(team_names, k=random.randint(1, 3)) for _ in range(10000)],
        'matches_played': [random.randint(0, 50) for _ in range(10000)],
        'tournaments': [random.randint(0, 10) for _ in range(10000)],
        'bio': [fake.sentence() for _ in range(10000)],
        'location': [random.choice(venues) for _ in range(10000)],
        'achievements': [[random.choice(['MVP', 'Top Scorer', 'Best Bowler']) for _ in range(random.randint(0, 5))] for _ in range(10000)],
        'level': [random.randint(1, 100) for _ in range(10000)]
    }
    profile_df = pd.DataFrame(profile_data)

    language_data = {
        'lang_code': [lang[0] for lang in languages],
        'language_name': [lang[1] for lang in languages],
        'is_default': [lang[2] for lang in languages]
    }
    language_df = pd.DataFrame(language_data)

    share_app_data = {
        'user_id': [random.choice([f'UID_{i:05d}' for i in range(1, 10001)]) for _ in range(200)],
        'platform': [random.choice(platforms) for _ in range(200)],
        'timestamp': [random_timestamp(start_date, end_date) for _ in range(200)],
        'shared_to': [random.choice(['Friends', 'Group', 'Public']) for _ in range(200)]
    }
    share_app_df = pd.DataFrame(share_app_data)

    help_support_data = {
        'ticket_id': [f'TICKET_{i:05d}' for i in range(1, 201)],
        'user_id': [random.choice([f'UID_{i:05d}' for i in range(1, 10001)]) for _ in range(200)],
        'issue_type': [random.choice(issue_types) for _ in range(200)],
        'description': [fake.paragraph() for _ in range(200)],
        'status': [random.choice(['Open', 'In Progress', 'Resolved']) for _ in range(200)],
        'created_at': [random_timestamp(start_date, end_date) for _ in range(200)],
        'resolved_at': [random_timestamp(start_date, end_date) if random.choice([True, False]) else None for _ in range(200)],
        'agent_id': [f'AGENT_{random.randint(1, 50):05d}' for _ in range(200)]
    }
    help_support_df = pd.DataFrame(help_support_data)

    contact_us_data = {
        'contact_id': [f'CONT_{i:05d}' for i in range(1, 201)],
        'user_id': [random.choice([f'UID_{i:05d}' for i in range(1, 10001)]) for _ in range(200)],
        'name': [fake.name() for _ in range(200)],
        'email': [fake.email() for _ in range(200)],
        'message': [fake.paragraph() for _ in range(200)],
        'timestamp': [random_timestamp(start_date, end_date) for _ in range(200)],
        'response_status': [random.choice(['Pending', 'Responded']) for _ in range(200)]
    }
    contact_us_df = pd.DataFrame(contact_us_data)

    return {
        "Feed": feed_df,
        "Cricket Scores": cricket_scores_df,
        "Multi-Sport Scores": multi_sport_scores_df,
        "Start Scoring": start_match_df,
        "Start a Tournament": tournament_df,
        "My Matches": my_matches_df,
        "My Teams": my_teams_df,
        "My Stats": my_stats_df,
        "Highlights": highlights_df,
        "Create Account": create_account_df,
        "Shop": shop_df,
        "Profile": profile_df,
        "Change Language": language_df,
        "Share App": share_app_df,
        "Help & Support": help_support_df,
        "Contact Us": contact_us_df
    }

# Load all datasets using the generation function
# This will call generate_all_data once and cache the result.
data = generate_all_data()

# The rest of your Streamlit app code remains largely the same,
# as it now accesses the DataFrames directly from the 'data' dictionary.
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

