import streamlit as st
import pandas as pd
import plotly.express as px
import os
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

# Set page config for a wider layout and custom title/icon
st.set_page_config(page_title="Sportsphere", layout="wide", page_icon="🏀")

# --- GLOBAL CONSTANTS (Moved here for wider accessibility) ---
sports = ['Cricket', 'Football', 'Basketball', 'Badminton', 'Tennis', 'Volleyball']
team_names = [
    'Mumbai Mavericks', 'Delhi Dynamos', 'Chennai Chargers', 'Bangalore Blasters',
    'Kolkata Knights', 'Hyderabad Hawks', 'Pune Panthers', 'Ahmedabad Avengers',
    'Royal Challengers', 'Super Giants', 'Knight Riders', 'Sunrisers'
]
venues = [
    'Wankhede Stadium', 'Eden Gardens', 'Chinnaswamy Stadium', 'Arun Jaitley Stadium',
    'MA Chidambaram Stadium', 'Ekana Cricket Stadium', 'Sardar Patel Stadium',
    'Lords Arena', 'MCG', 'Old Trafford', 'Madison Square Garden', 'Stade de France'
]
match_formats = ['T20', 'ODI', 'Test', 'Friendly', 'League', 'Cup Final']
tournament_formats = ['Knockout', 'Round-robin', 'Group Stage & Playoffs']
languages = [('en', 'English', True), ('hi', 'Hindi', False), ('es', 'Spanish', False), ('fr', 'French', False)]
roles = ['Player', 'Scorer', 'Organizer', 'Spectator', 'Coach', 'Umpire']
issue_types = ['Bug', 'Feature Request', 'Payment Issue', 'Account Issue', 'Other']
platforms = ['WhatsApp', 'Twitter', 'Facebook', 'Email', 'Instagram', 'LinkedIn']


# --- Define Navigation Tabs ---
tabs = [
    "🏠 Feed", "📊 Cricket Scores", "🏀 Multi-Sport Scores", "🧮 Start Scoring",
    "🏆 Start a Tournament", "📋 My Matches", "👥 My Teams", "📈 My Stats",
    "🎬 Highlights", "🧑‍💻 Create Account", "🛒 Shop", "🧍‍♂️ Profile",
    "🌐 Change Language", "🔗 Share App", "🆘 Help & Support", "📧 Contact Us"
]

# --- Data Generation Logic (Cached for Performance) ---
@st.cache_data
def generate_all_data():
    """Generates all synthetic data for the Sportsphere application."""
    fake = Faker()

    # Set random seed for reproducibility
    np.random.seed(42)
    random.seed(42)

    # Helper functions for random dates/timestamps
    def random_date(start_date, end_date):
        time_delta = end_date - start_date
        random_days = random.randint(0, time_delta.days)
        return start_date + timedelta(days=random_days)

    def random_timestamp(start_date, end_date):
        time_delta = end_date - start_date
        random_seconds = random.randint(0, int(time_delta.total_seconds()))
        return start_date + timedelta(seconds=random_seconds)

    # Constants for data generation
    # Current date is June 24, 2025. Data should be around this period.
    start_date_data = datetime(2024, 1, 1)
    end_date_data = datetime(2025, 12, 31) # Extend to end of current year

    # --- Generate DataFrames ---

    # Feed Data
    feed_data = {
        'timestamp': [random_timestamp(start_date_data, end_date_data) for _ in range(500)],
        'event_type': [random.choice(['Match Result', 'Tournament Announcement', 'MVP Award', 'New Record']) for _ in range(500)],
        'user_name': [fake.name() for _ in range(500)],
        'team_name': [random.choice(team_names + ['N/A']) for _ in range(500)], # Allow N/A for non-team events
        'match_id': [f'MID_{random.randint(1, 900):05d}' for _ in range(500)],
        'message': [
            f"{random.choice(['Won by', 'Lost by', 'Declared MVP', 'Set new record'])} {random.randint(1, 100)} {random.choice(['runs', 'wickets', 'points', 'goals', 'medals'])}"
            for _ in range(500)
        ]
    }
    feed_df = pd.DataFrame(feed_data).sort_values(by='timestamp', ascending=False) # Sort for recency

    # Cricket Scores Data
    cricket_scores_data = {
        'match_id': [f'MID_C{i:04d}' for i in range(1, 301)],
        'team1_name': [random.choice(team_names) for _ in range(300)],
        'team2_name': [random.choice(team_names) for _ in range(300)],
        'score_team1': [random.randint(50, 350) for _ in range(300)],
        'score_team2': [random.randint(50, 350) for _ in range(300)],
        'overs': [f"{random.randint(1, 50)}.{random.randint(0, 5)}" for _ in range(300)],
        'wickets': [random.randint(0, 10) for _ in range(300)],
        'status': [random.choice(['Live', 'Completed', 'Upcoming']) for _ in range(300)],
        'current_inning': [random.choice([1, 2]) for _ in range(300)],
        'location': [random.choice(venues) for _ in range(300)],
        'match_date': [random_date(start_date_data, end_date_data + timedelta(days=90)) for _ in range(300)] # Extend date range for upcoming
    }
    cricket_scores_df = pd.DataFrame(cricket_scores_data)

    # Multi-Sport Scores Data
    multi_sport_scores_data = {
        'sport_name': [random.choice([s for s in sports if s != 'Cricket']) for _ in range(300)],
        'match_id': [f'MID_M{i:04d}' for i in range(1, 301)],
        'team1': [random.choice(team_names) for _ in range(300)],
        'team2': [random.choice(team_names) for _ in range(300)],
        'score1': [random.randint(0, 100) for _ in range(300)],
        'score2': [random.randint(0, 100) for _ in range(300)],
        'time_elapsed': [f"{random.randint(0, 90)}:{random.randint(0, 59):02d}" for _ in range(300)],
        'status': [random.choice(['Live', 'Completed', 'Upcoming']) for _ in range(300)]
    }
    multi_sport_scores_df = pd.DataFrame(multi_sport_scores_data)

    # Start Match Data (for scoring)
    start_match_data = {
        'match_id': [f'MID_S{i:04d}' for i in range(1, 101)],
        'sport_type': [random.choice(sports) for _ in range(100)],
        'teams': [[random.choice(team_names), random.choice(team_names)] for _ in range(100)],
        'start_time': [random_timestamp(start_date_data, end_date_data) for _ in range(100)],
        'venue': [random.choice(venues) for _ in range(100)],
        'umpires': [fake.name() for _ in range(100)],
        'scorers': [fake.name() for _ in range(100)],
        'match_format': [random.choice(match_formats) for _ in range(100)],
        'number_of_overs': [random.choice([20, 50, None]) for _ in range(100)],
        'status': [random.choice(['Scheduled', 'In Progress', 'Completed']) for _ in range(100)]
    }
    start_match_df = pd.DataFrame(start_match_data)

    # Tournament Data
    tournament_data = {
        'tournament_id': [f'TID_{i:04d}' for i in range(1, 51)],
        'name': [f"{fake.word().capitalize()} Cup {random.randint(2024, 2026)}" for _ in range(50)],
        'organizer': [fake.name() for _ in range(50)],
        'start_date': [random_date(start_date_data, end_date_data) for _ in range(50)],
        'end_date': [random_date(start_date_data, end_date_data) + timedelta(days=random.randint(5, 30)) for _ in range(50)],
        'teams_list': [random.sample(team_names, k=random.randint(4, 8)) for _ in range(50)],
        'location': [random.choice(venues) for _ in range(50)],
        'match_ids': [[f'MID_{random.randint(1,900):05d}' for _ in range(random.randint(5, 15))] for _ in range(50)],
        'format': [random.choice(tournament_formats) for _ in range(50)]
    }
    tournament_df = pd.DataFrame(tournament_data)

    # My Matches Data
    my_matches_data = {
        'user_id': [f'UID_{random.randint(1, 1000):04d}' for _ in range(1000)], # Limited user IDs for easier selection
        'match_id': [random.choice([f'MID_C{i:04d}' for i in range(1, 301)] + [f'MID_M{i:04d}' for i in range(1, 301)]) for _ in range(1000)],
        'role': [random.choice(roles) for _ in range(1000)],
        'participation_status': [random.choice(['Confirmed', 'Pending', 'Declined']) for _ in range(1000)],
        'result': [random.choice(['Won', 'Lost', 'Draw', 'Ongoing']) for _ in range(1000)],
        'date': [random_date(start_date_data, end_date_data) for _ in range(1000)],
        'performance_summary': [f"{random.randint(0, 100)} runs, {random.randint(0, 5)} wickets" if random.random() < 0.7 else None for _ in range(1000)]
    }
    my_matches_df = pd.DataFrame(my_matches_data)

    # My Teams Data
    my_teams_data = {
        'team_id': [f'TEAM_{i:04d}' for i in range(1, 201)],
        'team_name': [f"{random.choice(team_names)} {chr(65+i % 26)}" for i in range(200)], # Make team names unique
        'created_by': [fake.name() for _ in range(200)],
        'sport_type': [random.choice(sports) for _ in range(200)],
        'players_list': [[fake.name() for _ in range(random.randint(5, 15))] for _ in range(200)],
        'rating': [round(random.uniform(1, 5), 1) for _ in range(200)],
        'wins': [random.randint(0, 50) for _ in range(200)],
        'losses': [random.randint(0, 50) for _ in range(200)],
        'logo_url': [f"https://picsum.photos/id/{100 + i}/100/100" for i in range(200)], # Placeholder images
        'captain_id': [f'UID_{random.randint(1, 1000):04d}' for _ in range(200)]
    }
    my_teams_df = pd.DataFrame(my_teams_data)

    # My Stats Data
    my_stats_data = {
        'user_id': [f'UID_{i:04d}' for i in range(1, 1001)], # Match with user IDs from My Matches/Profile
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

    # Highlights Data
    highlights_data = {
        'match_id': [random.choice([f'MID_C{i:04d}' for i in range(1, 301)] + [f'MID_M{i:04d}' for i in range(1, 301)]) for _ in range(200)],
        'media_type': [random.choice(['Video', 'Image']) for _ in range(200)],
        'timestamp': [random_timestamp(start_date_data, end_date_data) for _ in range(200)],
        'player': [fake.name() for _ in range(200)],
        'event_description': [f"{random.choice(['Six', 'Wicket', 'Catch', 'Goal', 'Dunk'])} by {fake.name()}" for _ in range(200)],
        'url': [f"https://www.youtube.com/watch?v=dQw4w9WgXcQ" if random.random() > 0.5 else f"https://picsum.photos/id/{200+i}/600/400" for i in range(200)]
    }
    highlights_df = pd.DataFrame(highlights_data)

    # Create Account Data (User Registry)
    create_account_data = {
        'user_id': [f'UID_{i:04d}' for i in range(1, 10001)],
        'name': [fake.name() for _ in range(10000)],
        'email': [fake.email() for _ in range(10000)],
        'phone': [fake.phone_number() for _ in range(10000)],
        'gender': [random.choice(['Male', 'Female', 'Other']) for _ in range(10000)],
        'birthdate': [random_date(datetime(1980, 1, 1), datetime(2005, 1, 1)) for _ in range(10000)],
        'location': [random.choice(venues) for _ in range(10000)],
        'joined_date': [random_date(start_date_data, end_date_data) for _ in range(10000)],
        'sports_interested_in': [random.sample(sports, k=random.randint(1, 4)) for _ in range(10000)],
        'role': [random.choice(roles) for _ in range(10000)]
    }
    create_account_df = pd.DataFrame(create_account_data)

    # Shop Data
    shop_data = {
        'product_id': [f'PROD_{i:04d}' for i in range(1, 101)],
        'name': [f"{random.choice(['Pro', 'Elite', 'Youth', 'Classic'])} {random.choice(['Bat', 'Ball', 'Jersey', 'Shoes', 'Gloves', 'Racket'])} {fake.word().capitalize()}" for _ in range(100)],
        'price': [round(random.uniform(10, 200), 2) for _ in range(100)],
        'category': [random.choice(['Equipment', 'Apparel', 'Accessories', 'Footwear']) for _ in range(100)],
        'description': [fake.sentence() for _ in range(100)],
        'image_url': [f"https://picsum.photos/id/{300+i}/300/200" for i in range(100)], # Placeholder images
        'inventory_count': [random.randint(0, 100) for _ in range(100)],
        'ratings': [round(random.uniform(3, 5), 1) for _ in range(100)],
        'sold_count': [random.randint(0, 500) for _ in range(100)]
    }
    shop_df = pd.DataFrame(shop_data)

    # Profile Data (tied to Create Account Data)
    # Ensure all user_ids from Create Account have a profile entry
    profile_data = {
        'user_id': create_account_df['user_id'].tolist(),
        'name': create_account_df['name'].tolist(),
        'photo_url': [f"https://picsum.photos/id/{400+i}/200/200" for i in range(len(create_account_df))], # Placeholder images
        'teams_joined': [random.sample(team_names, k=random.randint(0, 3)) for _ in range(len(create_account_df))],
        'matches_played_profile': [random.randint(0, 100) for _ in range(len(create_account_df))], # Separate column for profile
        'tournaments': [random.randint(0, 15) for _ in range(len(create_account_df))],
        'bio': [fake.sentence() for _ in range(len(create_account_df))],
        'location': [random.choice(venues) for _ in range(len(create_account_df))],
        'achievements': [[random.choice(['MVP', 'Top Scorer', 'Best Bowler', 'Tournament Winner', 'Fair Play Award']) for _ in range(random.randint(0, 5))] for _ in range(len(create_account_df))],
        'level': [random.randint(1, 100) for _ in range(len(create_account_df))]
    }
    profile_df = pd.DataFrame(profile_data)

    # Language Data
    language_df = pd.DataFrame(languages, columns=['lang_code', 'language_name', 'is_default'])

    # Share App Data
    share_app_data = {
        'user_id': [random.choice(create_account_df['user_id'].tolist()) for _ in range(200)],
        'platform': [random.choice(platforms) for _ in range(200)],
        'timestamp': [random_timestamp(start_date_data, end_date_data) for _ in range(200)],
        'shared_to': [random.choice(['Friends', 'Group', 'Public']) for _ in range(200)]
    }
    share_app_df = pd.DataFrame(share_app_data)

    # Help & Support Data
    help_support_data = {
        'ticket_id': [f'TICKET_{i:04d}' for i in range(1, 201)],
        'user_id': [random.choice(create_account_df['user_id'].tolist()) for _ in range(200)],
        'issue_type': [random.choice(issue_types) for _ in range(200)],
        'description': [fake.paragraph(nb_sentences=3) for _ in range(200)],
        'status': [random.choice(['Open', 'In Progress', 'Resolved', 'Closed']) for _ in range(200)],
        'created_at': [random_timestamp(start_date_data, end_date_data) for _ in range(200)],
        'resolved_at': [random_timestamp(start_date_data, end_date_data) if random.random() < 0.7 else None for _ in range(200)],
        'agent_id': [f'AGENT_{random.randint(1, 50):04d}' for _ in range(200)]
    }
    help_support_df = pd.DataFrame(help_support_data)

    # Contact Us Data
    contact_us_data = {
        'contact_id': [f'CONT_{i:04d}' for i in range(1, 201)],
        'user_id': [random.choice(create_account_df['user_id'].tolist() + ['None']) for _ in range(200)], # Allow non-registered users
        'name': [fake.name() for _ in range(200)],
        'email': [fake.email() for _ in range(200)],
        'message': [fake.paragraph(nb_sentences=4) for _ in range(200)],
        'timestamp': [random_timestamp(start_date_data, end_date_data) for _ in range(200)],
        'response_status': [random.choice(['Pending', 'Responded']) for _ in range(200)]
    }
    contact_us_df = pd.DataFrame(contact_us_data)

    return {
        "Feed": feed_df,
        "Cricket Scores": cricket_scores_df,
        "Multi-Sport Scores": multi_sport_scores_df, # Correct key
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

# Load all datasets using the cached generation function
data = generate_all_data()

# --- Streamlit App Layout and Custom CSS ---

# Custom CSS for better styling (minimal example for a web app feel)
st.markdown("""
<style>
    /* Main content area padding */
    .st-emotion-cache-nahz7x {
        padding-top: 2rem;
        padding-right: 3rem;
        padding-left: 3rem;
        padding-bottom: 2rem;
    }
    /* Headings */
    h1, h2, h3, h4 {
        color: #FF4B4B; /* A sporty red */
        font-family: 'Segoe UI', sans-serif;
    }
    /* Labels for input widgets */
    .stSelectbox label, .stTextInput label, .stDateInput label, .stTimeInput label, .stNumberInput label, .stRadio label, .stMultiSelect label {
        font-weight: bold;
        color: #333333;
    }
    /* Buttons styling */
    .stButton > button {
        background-color: #FF4B4B;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.6rem 1.2rem;
        font-weight: bold;
        transition: all 0.2s ease-in-out;
    }
    .stButton > button:hover {
        background-color: #FF7B7B;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: none;
    }
    /* Sidebar styling */
    div[data-testid="stSidebar"] {
        background-color: #f0f2f6; /* Light grey for sidebar */
        border-right: 1px solid #e0e0e0;
    }
    .st-emotion-cache-1jmve30 { /* Card-like background for containers with border=True */
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.75rem; /* More rounded corners */
        box-shadow: 0 6px 12px 0 rgba(0,0,0,0.08); /* Stronger shadow */
        margin-bottom: 1.5rem; /* More space between cards */
        border: 1px solid #e0e0e0; /* Subtle border */
    }
    .stExpander {
        border: 1px solid #e0e0e0;
        border-radius: 0.75rem;
        padding: 0.5rem 1rem;
        margin-bottom: 1rem;
        background-color: #f9f9f9;
    }
    .stExpander > div > div > p {
        font-weight: bold;
        color: #FF4B4B;
    }
    /* Metric cards styling */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.75rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        border: 1px solid #eee;
    }
</style>
""", unsafe_allow_html=True)


# Main app title
st.title("Sportsphere ⚽🏀🏏")
st.markdown("Your ultimate platform for sports management and engagement!")

# Sidebar navigation
st.sidebar.title("Navigate Sportsphere")
selected_tab = st.sidebar.radio("Go to:", tabs)

# Display content based on selected tab
st.markdown(f"## {selected_tab}")

# --- Dynamic Content for Each Tab ---

if selected_tab == "🏠 Feed":
    st.markdown("### Recent Activity & News")
    st.write("Stay updated with the latest from your sports world!")

    if not data["Feed"].empty:
        # Sort feed by timestamp for recent events
        recent_feed = data["Feed"].sort_values(by="timestamp", ascending=False).head(20)

        # Use columns for a more engaging layout
        cols = st.columns(3)
        for i, row in recent_feed.iterrows():
            with cols[i % 3]: # Distribute cards across 3 columns
                with st.container(border=True): # Use a container to create a card-like effect
                    st.subheader(f"{row['event_type']}")
                    st.markdown(f"**Match ID:** {row['match_id']}")
                    st.write(f"**Team:** {row['team_name']}")
                    st.write(f"**User:** {row['user_name']}")
                    st.markdown(f"*{row['message']}*")
                    st.caption(f"_{row['timestamp'].strftime('%Y-%m-%d %H:%M')}_")
        st.markdown("---")
        # Optional: Show more feed items in a collapsible expander
        with st.expander("View All Feed Items (Tabular)"):
            st.dataframe(data["Feed"], use_container_width=True)

elif selected_tab == "📊 Cricket Scores":
    st.markdown("### Live & Upcoming Cricket Matches")
    st.write("Get real-time updates and schedules for your favorite cricket games.")

    if not data["Cricket Scores"].empty:
        live_matches = data["Cricket Scores"][data["Cricket Scores"]['status'] == 'Live'].head(5).reset_index(drop=True)
        upcoming_matches = data["Cricket Scores"][data["Cricket Scores"]['status'] == 'Upcoming'].sort_values(by='match_date').head(5).reset_index(drop=True)
        completed_matches = data["Cricket Scores"][data["Cricket Scores"]['status'] == 'Completed'].sort_values(by='match_date', ascending=False).head(5).reset_index(drop=True)

        st.subheader("🏏 Live Matches")
        if not live_matches.empty:
            for i, match in live_matches.iterrows():
                with st.container(border=True):
                    col1, col2, col3 = st.columns([0.3, 0.4, 0.3])
                    with col1:
                        st.metric(label=match['team1_name'], value=match['score_team1'])
                    with col2:
                        st.markdown(f"<h4 style='text-align: center;'>vs</h4>", unsafe_allow_html=True)
                        st.markdown(f"<p style='text-align: center; font-size: small;'>Overs: {match['overs']}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='text-align: center; font-size: small;'>Wickets: {match['wickets']}</p>", unsafe_allow_html=True)
                    with col3:
                        st.metric(label=match['team2_name'], value=match['score_team2'])
                    st.caption(f"Live from {match['location']} | Match ID: {match['match_id']}")
        else:
            st.info("No live matches currently.")

        st.subheader("📅 Upcoming Matches")
        if not upcoming_matches.empty:
            for i, match in upcoming_matches.iterrows():
                with st.container(border=True):
                    st.write(f"**{match['team1_name']}** vs **{match['team2_name']}**")
                    st.write(f"Date: {match['match_date'].strftime('%Y-%m-%d')} at {match['location']}")
                    st.caption(f"Match ID: {match['match_id']}")
        else:
            st.info("No upcoming matches scheduled.")

        st.subheader("✅ Recently Completed Matches")
        if not completed_matches.empty:
            for i, match in completed_matches.iterrows():
                with st.container(border=True):
                    winner = match['team1_name'] if match['score_team1'] > match['score_team2'] else match['team2_name']
                    st.write(f"**{match['team1_name']} ({match['score_team1']})** vs **{match['team2_name']} ({match['score_team2']})**")
                    st.success(f"Winner: **{winner}**")
                    st.caption(f"Played on {match['match_date'].strftime('%Y-%m-%d')} at {match['location']}")
        else:
            st.info("No recently completed matches.")

        st.markdown("---")
        with st.expander("Detailed Cricket Scores (Tabular)"):
            st.dataframe(data["Cricket Scores"], use_container_width=True)


elif selected_tab == "🏀 Multi-Sport Scores":
    st.markdown("### Scores Across All Sports")
    st.write("Stay on top of Football, Basketball, Badminton and more!")

    if not data["Multi-Sport Scores"].empty: # Fixed Key: Multi-Sport Scores
        col_sport_filter, col_status_filter = st.columns(2)
        all_sports = ['All'] + sorted(data["Multi-Sport Scores"]['sport_name'].unique().tolist())
        selected_sport = col_sport_filter.selectbox("Filter by Sport", all_sports)

        all_statuses = ['All'] + sorted(data["Multi-Sport Scores"]['status'].unique().tolist()) # Fixed Key: Multi-Sport Scores
        selected_status = col_status_filter.selectbox("Filter by Status", all_statuses)

        filtered_df = data["Multi-Sport Scores"].copy()
        if selected_sport != 'All':
            filtered_df = filtered_df[filtered_df['sport_name'] == selected_sport]
        if selected_status != 'All':
            filtered_df = filtered_df[filtered_df['status'] == selected_status]

        if not filtered_df.empty:
            # Display filtered results in a more compact way
            for i, match in filtered_df.iterrows():
                with st.container(border=True):
                    st.write(f"**{match['sport_name']}**: {match['team1']} {match['score1']} - {match['score2']} {match['team2']}")
                    st.caption(f"Status: {match['status']} | Time: {match['time_elapsed']} | Match ID: {match['match_id']}")
        else:
            st.info("No matches found for the selected filters.")

    st.markdown("---")
    with st.expander("View All Multi-Sport Scores (Tabular)"):
        st.dataframe(data["Multi-Sport Scores"], use_container_width=True)

elif selected_tab == "🧮 Start Scoring":
    st.markdown("### Start a New Match!")
    st.write("Organize and score your games easily.")

    with st.form("new_match_form"):
        st.subheader("Match Details")
        sport_type = st.selectbox("Sport Type", sports) # 'sports' is now global
        team1 = st.selectbox("Team 1", team_names, key="team1_select")

        # Filter team2 options to ensure it's different from team1
        team2_options = [t for t in team_names if t != team1]
        team2 = st.selectbox("Team 2", team2_options, key="team2_select")

        venue = st.selectbox("Venue", venues)
        match_format = st.selectbox("Match Format", match_formats)

        num_overs = 0
        if sport_type == 'Cricket':
             num_overs = st.number_input("Number of Overs (for Cricket)", min_value=1, max_value=50, value=20)
        else:
             st.info("Number of Overs is applicable only for Cricket matches.")

        start_date_input = st.date_input("Match Date", datetime.now().date())
        start_time_input = st.time_input("Match Time", datetime.now().time())

        st.subheader("Officials")
        umpire1 = st.text_input("Umpire 1 Name", "") # Empty by default
        umpire2 = st.text_input("Umpire 2 Name", "")
        scorer = st.text_input("Scorer Name", "")

        submitted = st.form_submit_button("Create Match")

        if submitted:
            if team1 == team2:
                st.error("Team 1 and Team 2 cannot be the same! Please select different teams.")
            elif not umpire1 or not scorer:
                st.error("Umpire 1 and Scorer names are required.")
            else:
                # In a real app, you'd get the next match ID from a database or a persistent counter
                new_match_id = f"MID_S{len(data['Start Scoring']) + 1:04d}" # Simple increment for demo

                # Create a dictionary for the new match data (for demonstration)
                new_match_row_dict = {
                    'match_id': new_match_id,
                    'sport_type': sport_type,
                    'teams': [team1, team2],
                    'start_time': datetime.combine(start_date_input, start_time_input),
                    'venue': venue,
                    'umpires': umpire1,
                    'scorers': scorer,
                    'match_format': match_format,
                    'number_of_overs': num_overs if sport_type == 'Cricket' else None,
                    'status': 'Scheduled'
                }

                # Display success and new match info
                st.success(f"Match '{new_match_id}' between {team1} and {team2} created successfully!")
                st.json(new_match_row_dict) # Show the data that would be saved
                st.info("Note: This is a demo. Data is not permanently stored or added to the underlying DataFrame.")
                # To actually add to the DataFrame in this demo, you'd do:
                # new_match_df = pd.DataFrame([new_match_row_dict])
                # data["Start Scoring"] = pd.concat([data["Start Scoring"], new_match_df], ignore_index=True)


    st.markdown("---")
    with st.expander("View Existing Matches (Tabular)"):
        st.dataframe(data["Start Scoring"], use_container_width=True)

elif selected_tab == "🏆 Start a Tournament":
    st.markdown("### Organize a New Tournament!")
    st.write("Plan and manage your tournaments with ease.")

    with st.form("new_tournament_form"):
        st.subheader("Tournament Details")
        tournament_name = st.text_input("Tournament Name", "")
        organizer_name = st.text_input("Organizer Name", "")
        start_date_t = st.date_input("Start Date", datetime.now().date())
        end_date_t = st.date_input("End Date", datetime.now().date() + timedelta(days=7))
        tournament_location = st.selectbox("Location", venues)
        tournament_format = st.selectbox("Tournament Format", tournament_formats)

        st.subheader("Participating Teams (Select at least 2)")
        selected_teams = st.multiselect("Select Teams", team_names, default=[])

        submitted_tournament = st.form_submit_button("Create Tournament")

        if submitted_tournament:
            if not tournament_name or not organizer_name:
                st.error("Tournament Name and Organizer Name are required.")
            elif len(selected_teams) < 2:
                st.error("Please select at least two teams for the tournament.")
            elif start_date_t > end_date_t:
                st.error("End Date cannot be before Start Date.")
            else:
                new_tournament_id = f"TID_{len(data['Start a Tournament']) + 1:04d}"
                st.success(f"Tournament '{tournament_name}' ({new_tournament_id}) created successfully with {len(selected_teams)} teams!")
                st.info("Note: This is a demo. Data is not permanently stored or added to the underlying DataFrame.")
                # new_tournament_row = pd.DataFrame([{
                #     'tournament_id': new_tournament_id, 'name': tournament_name, 'organizer': organizer_name,
                #     'start_date': start_date_t, 'end_date': end_date_t, 'teams_list': selected_teams,
                #     'location': tournament_location, 'match_ids': [], 'format': tournament_format
                # }])
                # data["Start a Tournament"] = pd.concat([data["Start a Tournament"], new_tournament_row], ignore_index=True)

    st.markdown("---")
    st.subheader("Current Tournaments")
    if not data["Start a Tournament"].empty:
        # Display current tournaments as cards
        cols = st.columns(3)
        for i, row in data["Start a Tournament"].iterrows():
            with cols[i % 3]:
                with st.container(border=True):
                    st.subheader(row['name'])
                    st.write(f"**Organizer:** {row['organizer']}")
                    st.write(f"**Dates:** {row['start_date'].strftime('%b %d, %Y')} - {row['end_date'].strftime('%b %d, %Y')}")
                    st.write(f"**Location:** {row['location']}")
                    st.write(f"**Format:** {row['format']}")
                    # Limit display of teams for brevity on card
                    teams_display = ', '.join(row['teams_list'][:3])
                    if len(row['teams_list']) > 3:
                        teams_display += f", and {len(row['teams_list']) - 3} more."
                    st.write(f"**Teams:** {teams_display if teams_display else 'N/A'}")
                    st.caption(f"Tournament ID: {row['tournament_id']}")
    else:
        st.info("No tournaments available.")

    with st.expander("View All Tournament Data (Tabular)"):
        st.dataframe(data["Start a Tournament"], use_container_width=True)

elif selected_tab == "📋 My Matches":
    st.markdown("### Your Match History")
    st.write("Track your participation and performance in various matches.")

    if not data["My Matches"].empty:
        # Allow user to select their ID to see their matches
        all_user_ids = sorted(data["My Matches"]['user_id'].unique().tolist())
        selected_user = st.selectbox("Select Your User ID", all_user_ids, index=0)

        user_matches = data["My Matches"][data["My Matches"]['user_id'] == selected_user].sort_values(by='date', ascending=False).reset_index(drop=True)

        if not user_matches.empty:
            st.subheader(f"Matches for {selected_user}")
            # Display matches in a more compact list/card format
            for i, match in user_matches.iterrows():
                with st.container(border=True):
                    st.markdown(f"**Match ID:** {match['match_id']} | **Date:** {match['date'].strftime('%Y-%m-%d')}")
                    st.write(f"**Role:** {match['role']} | **Status:** {match['participation_status']}")
                    st.markdown(f"**Result:** <span style='color:{'green' if match['result']=='Won' else 'red' if match['result']=='Lost' else 'orange'}; font-weight:bold;'>{match['result']}</span>", unsafe_allow_html=True)
                    if pd.notna(match['performance_summary']) and match['performance_summary'] != '':
                        st.markdown(f"**Performance:** *{match['performance_summary']}*")
        else:
            st.info("No matches found for this user ID.")

    st.markdown("---")
    with st.expander("View All My Matches Data (Tabular)"):
        st.dataframe(data["My Matches"], use_container_width=True)

elif selected_tab == "👥 My Teams":
    st.markdown("### Your Teams")
    st.write("Manage your teams and view rosters.")

    if not data["My Teams"].empty:
        # Allow user to select a team
        team_options = sorted(data["My Teams"]['team_name'].unique().tolist())
        selected_team_name = st.selectbox("Select a Team", team_options)

        team_info = data["My Teams"][data["My Teams"]['team_name'] == selected_team_name]

        if not team_info.empty:
            team_info = team_info.iloc[0] # Get the first (and likely only) row for the selected team
            st.subheader(f"Details for {team_info['team_name']}")
            col_img, col_details = st.columns([0.2, 0.8])
            with col_img:
                st.image(team_info['logo_url'], width=150) # Placeholder image
            with col_details:
                st.write(f"**Sport Type:** {team_info['sport_type']}")
                st.write(f"**Created By:** {team_info['created_by']}")
                st.write(f"**Captain ID:** {team_info['captain_id']}")
                st.write(f"**Rating:** ⭐ {team_info['rating']}")
                st.write(f"**Wins/Losses:** {team_info['wins']} / {team_info['losses']}")

            st.markdown("#### Team Roster")
            players_list = team_info['players_list']
            # Ensure players_list is actually a list (can be string if read from CSV)
            if isinstance(players_list, str):
                import ast
                try:
                    players_list = ast.literal_eval(players_list)
                except ValueError:
                    players_list = [players_list] # Fallback if not a list string

            if players_list:
                # Display players in a clean, multi-column format
                num_player_cols = 3
                player_columns = st.columns(num_player_cols)
                for idx, player in enumerate(players_list):
                    with player_columns[idx % num_player_cols]:
                        st.markdown(f"- {player}")
            else:
                st.info("No players listed for this team.")
        else:
            st.info("Team not found.") # Should not happen if selectbox uses unique team names

    st.markdown("---")
    with st.expander("View All My Teams Data (Tabular)"):
        st.dataframe(data["My Teams"], use_container_width=True)

elif selected_tab == "📈 My Stats":
    st.markdown("### Your Player Statistics")
    st.write("Review your career performance and achievements.")

    if not data["My Stats"].empty and not data["Profile"].empty:
        # Combine stats and profile data for a richer view
        # Ensure 'user_id' is the common key for merging
        merged_stats_profile = pd.merge(data["My Stats"], data["Profile"], on='user_id', how='left')

        all_player_ids = sorted(merged_stats_profile['user_id'].unique().tolist())
        selected_player_id = st.selectbox("Select Your Player ID", all_player_ids, index=0)

        player_data = merged_stats_profile[merged_stats_profile['user_id'] == selected_player_id]

        if not player_data.empty:
            player_data = player_data.iloc[0] # Get the single row for the selected player
            col_photo, col_basic_info = st.columns([0.2, 0.8])
            with col_photo:
                st.image(player_data['photo_url'], width=150)
            with col_basic_info:
                st.write(f"**Location:** {player_data['location']} | **Level:** {player_data['level']}")
                st.markdown(f"<p><i>{player_data['bio']}</i></p>", unsafe_allow_html=True)
                # Ensure teams_joined is handled as a list
                teams_joined_display = ', '.join(player_data['teams_joined']) if isinstance(player_data['teams_joined'], list) and player_data['teams_joined'] else 'N/A'
                st.write(f"**Teams Joined:** {teams_joined_display}")

            st.markdown("#### Key Performance Indicators")
            kpi1, kpi2, kpi3, kpi4 = st.columns(4)
            # Accessing columns that are guaranteed to be in merged_stats_profile
            kpi1.metric("Matches Played", player_data['matches_played'])
            kpi2.metric("Runs Scored", player_data['runs_scored'])
            kpi3.metric("Wickets Taken", player_data['wickets_taken'])
            kpi4.metric("MVP Count", player_data['MVP_count'])

            kpi5, kpi6, kpi7, kpi8 = st.columns(4)
            kpi5.metric("Strike Rate", player_data['strike_rate'])
            kpi6.metric("Economy", player_data['economy'])
            kpi7.metric("Average", player_data['average'])
            kpi8.metric("Catches", player_data['catches'])

            st.markdown("#### Achievements")
            if player_data['achievements'] and len(player_data['achievements']) > 0:
                for achievement in player_data['achievements']:
                    st.success(f"🏅 {achievement}")
            else:
                st.info("No notable achievements yet!")

            # Simple bar chart for a few key stats
            chart_data = pd.DataFrame({
                'Metric': ['Matches Played', 'Runs Scored', 'Wickets Taken', 'Catches'],
                'Value': [player_data['matches_played'], player_data['runs_scored'], player_data['wickets_taken'], player_data['catches']]
            })
            fig = px.bar(chart_data, x='Metric', y='Value', title=f"Performance Summary for {player_data['name']}",
                         color='Metric', color_discrete_map={'Matches Played': 'blue', 'Runs Scored': 'green', 'Wickets Taken': 'red', 'Catches': 'purple'})
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.info("Player data not found for the selected ID.")

    st.markdown("---")
    with st.expander("View All Player Stats (Tabular)"):
        st.dataframe(data["My Stats"], use_container_width=True)


elif selected_tab == "🎬 Highlights":
    st.markdown("### Match Highlights")
    st.write("Relive the best moments from recent games!")

    if not data["Highlights"].empty:
        # Filter and display highlights
        highlight_types = ['All'] + data["Highlights"]['media_type'].unique().tolist()
        selected_highlight_type = st.selectbox("Filter by Media Type", highlight_types)

        filtered_highlights = data["Highlights"]
        if selected_highlight_type != 'All':
            filtered_highlights = filtered_highlights[filtered_highlights['media_type'] == selected_highlight_type]

        if not filtered_highlights.empty:
            # Display highlights in a grid (3 columns)
            cols = st.columns(3)
            # Limit to a reasonable number for display, e.g., top 15
            for i, highlight in filtered_highlights.head(15).iterrows():
                with cols[i % 3]:
                    with st.container(border=True):
                        st.subheader(highlight['event_description'])
                        st.write(f"**Player:** {highlight['player']}")
                        st.write(f"**Match ID:** {highlight['match_id']}")
                        st.caption(f"Recorded: {highlight['timestamp'].strftime('%Y-%m-%d %H:%M')}")
                        if highlight['media_type'] == 'Video':
                            # Use a real YouTube video for demo or a placeholder
                            # Note: Streamlit's st.video usually expects a direct video URL, not a YouTube watch page.
                            # For YouTube, a generic embed works but actual playback might require an API key or a specific embed URL.
                            # Here, I'll use a public domain video or a known placeholder if available.
                            st.video("https://www.learningcontainer.com/wp-content/uploads/2020/05/sample-mp4-file.mp4") # Example public domain video
                            st.caption("*(Sample Video)*")
                        else: # Image
                            st.image(highlight['url'], caption="Highlight Image", use_column_width=True)
                        st.link_button("View Full", highlight['url'])
        else:
            st.info("No highlights found for the selected filter.")

    st.markdown("---")
    with st.expander("View All Highlights Data (Tabular)"):
        st.dataframe(data["Highlights"], use_container_width=True)


elif selected_tab == "🧑‍💻 Create Account":
    st.markdown("### Join Sportsphere!")
    st.write("Create your free account and start your sports journey.")

    with st.form("create_account_form"):
        st.subheader("Personal Details")
        user_name = st.text_input("Full Name", max_chars=100)
        user_email = st.text_input("Email", max_chars=100)
        user_phone = st.text_input("Phone Number", max_chars=20)
        user_gender = st.selectbox("Gender", ['Male', 'Female', 'Other', 'Prefer not to say'])
        user_birthdate = st.date_input("Date of Birth", min_value=datetime(1950, 1, 1).date(), max_value=datetime(2007, 1, 1).date())
        user_location = st.selectbox("Nearest City/Venue", venues)

        st.subheader("Sports Preferences")
        user_sports_interested = st.multiselect("Sports You're Interested In", sports)
        user_role = st.selectbox("Your Primary Role", roles)

        account_submitted = st.form_submit_button("Create My Account")

        if account_submitted:
            if not user_name or not user_email or not user_phone:
                st.error("Please fill in all required personal details (Full Name, Email, Phone Number).")
            elif not user_sports_interested:
                st.error("Please select at least one sport you're interested in.")
            elif "@" not in user_email or "." not in user_email:
                st.error("Please enter a valid email address.")
            else:
                # In a real app, you would get a unique ID from a database
                new_user_id = f"UID_{len(data['Create Account']) + 1:04d}"
                st.success(f"Welcome, {user_name}! Your account ({new_user_id}) has been created successfully.")
                st.info("Note: This is a demo. Data is not permanently stored or added to the underlying DataFrame.")
                # You would typically add new_user_data to a database here
                # new_user_data = {
                #     'user_id': new_user_id, 'name': user_name, 'email': user_email, 'phone': user_phone,
                #     'gender': user_gender, 'birthdate': user_birthdate, 'location': user_location,
                #     'joined_date': datetime.now().date(), 'sports_interested_in': user_sports_interested, 'role': user_role
                # }
                # new_user_df = pd.DataFrame([new_user_data])
                # data["Create Account"] = pd.concat([data["Create Account"], new_user_df], ignore_index=True)


    st.markdown("---")
    with st.expander("View Existing Accounts (Tabular)"):
        st.dataframe(data["Create Account"], use_container_width=True)


elif selected_tab == "🛒 Shop":
    st.markdown("### Sportsphere Shop")
    st.write("Browse and buy the latest sports gear!")

    if not data["Shop"].empty:
        col_cat_filter, col_search = st.columns([0.3, 0.7])

        product_categories = ['All'] + sorted(data["Shop"]['category'].unique().tolist())
        selected_category = col_cat_filter.selectbox("Filter by Category", product_categories)

        search_query = col_search.text_input("Search Products (e.g., 'Bat', 'Jersey')", "")

        filtered_products = data["Shop"]
        if selected_category != 'All':
            filtered_products = filtered_products[filtered_products['category'] == selected_category]

        if search_query:
            filtered_products = filtered_products[
                filtered_products['name'].str.contains(search_query, case=False, na=False) |
                filtered_products['description'].str.contains(search_query, case=False, na=False)
            ]

        if not filtered_products.empty:
            # Display products in a grid (3 columns)
            cols = st.columns(3)
            for i, product in filtered_products.iterrows():
                with cols[i % 3]:
                    with st.container(border=True):
                        st.image(product['image_url'], caption=product['name'], use_column_width=True) # Use a placeholder image
                        st.subheader(product['name'])
                        st.markdown(f"**Price:** <span style='font-size:1.2em; color:#4CAF50;'>₹{product['price']:.2f}</span>", unsafe_allow_html=True)
                        st.caption(f"Category: {product['category']}")
                        st.write(f"Rating: ⭐ {product['ratings']} ({product['sold_count']} sold)")
                        if product['inventory_count'] > 0:
                            st.success(f"In Stock: {product['inventory_count']}")
                            if st.button(f"Add to Cart", key=f"add_to_cart_{product['product_id']}"):
                                st.toast(f"'{product['name']}' added to cart! (Demo)")
                        else:
                            st.error("Out of Stock")
        else:
            st.info("No products found matching your filters.")

    st.markdown("---")
    with st.expander("View All Shop Products (Tabular)"):
        st.dataframe(data["Shop"], use_container_width=True)

elif selected_tab == "🧍‍♂️ Profile":
    st.markdown("### Your Sportsphere Profile")
    st.write("Manage your public profile and view your comprehensive stats.")

    if not data["Profile"].empty and not data["My Stats"].empty:
        # Merge Profile and My Stats to get a comprehensive player_data
        # Ensure the merge column 'user_id' exists in both.
        # Use a left merge to keep all profiles, filling missing stats with NaN
        merged_profile_stats = pd.merge(data["Profile"], data["My Stats"], on='user_id', how='left')

        all_profile_ids = sorted(merged_profile_stats['user_id'].unique().tolist())
        selected_profile_id = st.selectbox("Select Your Profile", all_profile_ids, index=0)

        profile_info = merged_profile_stats[merged_profile_stats['user_id'] == selected_profile_id]

        if not profile_info.empty:
            profile_info = profile_info.iloc[0] # Get the single row for the selected profile
            col_left, col_right = st.columns([0.3, 0.7])
            with col_left:
                st.image(profile_info['photo_url'], width=200, caption=profile_info['name'])
            with col_right:
                st.subheader(profile_info['name'])
                st.markdown(f"<p style='font-size:1.1em;'>📍 {profile_info['location']} | Level: <b>{profile_info['level']}</b></p>", unsafe_allow_html=True)
                st.markdown(f"<p><i>{profile_info['bio']}</i></p>", unsafe_allow_html=True)

                # Ensure teams_joined is handled as a list, and default if empty
                teams_joined_display = ', '.join(profile_info['teams_joined']) if isinstance(profile_info['teams_joined'], list) and profile_info['teams_joined'] else 'N/A'
                st.write(f"**Teams Joined:** {teams_joined_display}")

            st.markdown("---")
            st.subheader("Sports Journey")
            col_m, col_t = st.columns(2)
            # Use data from the merged DataFrame, providing defaults for NaN values
            col_m.metric("Matches Played", int(profile_info.get('matches_played', 0))) # .get() or fillna
            col_t.metric("Tournaments Participated", int(profile_info.get('tournaments', 0)))

            st.markdown("#### Achievements")
            if profile_info['achievements'] and len(profile_info['achievements']) > 0:
                for ach in profile_info['achievements']:
                    st.success(f"🏆 {ach}")
            else:
                st.info("No achievements yet. Keep playing!")

        else:
            st.info("Profile not found for the selected ID.")

    st.markdown("---")
    with st.expander("View All Profiles Data (Tabular)"):
        st.dataframe(data["Profile"], use_container_width=True)


elif selected_tab == "🌐 Change Language":
    st.markdown("### Select Your Preferred Language")
    st.write("Customize your Sportsphere experience.")

    if not data["Change Language"].empty:
        current_lang_row = data["Change Language"][data["Change Language"]["is_default"] == True]
        current_lang = current_lang_row.iloc[0]['language_name'] if not current_lang_row.empty else "English"
        st.info(f"Current language: **{current_lang}**")

        lang_options = data["Change Language"]["language_name"].tolist()
        selected_lang = st.selectbox("Choose a new language", lang_options, index=lang_options.index(current_lang))

        if st.button("Apply Language"):
            if selected_lang != current_lang:
                st.success(f"Language changed to **{selected_lang}**! (This is a demo, actual language change not implemented)")
                # In a real app, you would update a user preference or session state and potentially re-render content
            else:
                st.info("Language is already set to your selection.")
    else:
        st.warning("No language options available.")

    st.markdown("---")
    with st.expander("View Language Data (Tabular)"):
        st.dataframe(data["Change Language"], use_container_width=True)

elif selected_tab == "🔗 Share App":
    st.markdown("### Spread the Word!")
    st.write("Help your friends discover Sportsphere.")

    with st.form("share_app_form"):
        st.subheader("Share Options")
        platform_options = data["Share App"]['platform'].unique().tolist()
        share_platform = st.selectbox("Share Platform", platform_options)
        shared_to_option = st.radio("Share To", ['Friends', 'Group', 'Public'])

        message = st.text_area("Custom Message (Optional)", "Hey, check out Sportsphere! It's an amazing sports app.")

        share_button = st.form_submit_button("Share App")

        if share_button:
            st.success(f"App shared successfully via {share_platform} to {shared_to_option}! (Demo action)")
            st.write(f"Message: *'{message}'*")
            # In a real app, you might log this event or provide actual sharing links.

    st.markdown("---")
    st.subheader("Recent Share Activity")
    if not data["Share App"].empty:
        # Display recent shares
        recent_shares = data["Share App"].sort_values(by='timestamp', ascending=False).head(5).reset_index(drop=True)
        for i, share in recent_shares.iterrows():
            st.markdown(f"**[{share['timestamp'].strftime('%Y-%m-%d %H:%M')}]** `{share['user_id']}` shared on **{share['platform']}** to **{share['shared_to']}**.")
    else:
        st.info("No share activity recorded yet.")

    with st.expander("View All Share Data (Tabular)"):
        st.dataframe(data["Share App"], use_container_width=True)


elif selected_tab == "🆘 Help & Support":
    st.markdown("### Need Assistance?")
    st.write("Submit a support ticket and we'll get back to you.")

    with st.form("help_support_form"):
        st.subheader("Submit a New Ticket")
        ticket_user_id = st.text_input("Your User ID (e.g., UID_0001)")
        issue_type = st.selectbox("Type of Issue", issue_types)
        description = st.text_area("Describe your issue in detail", height=150)

        ticket_submitted = st.form_submit_button("Submit Ticket")

        if ticket_submitted:
            if not ticket_user_id or not description:
                st.error("Please provide your User ID and a description of the issue.")
            else:
                new_ticket_id = f"TICKET_{len(data['Help & Support']) + 1:04d}"
                st.success(f"Your ticket ({new_ticket_id}) has been submitted! We will review it shortly.")
                st.info("Note: This is a demo. Data is not permanently stored or added to the underlying DataFrame.")
                # You would add ticket data to a database here.

    st.markdown("---")
    st.subheader("Your Open Tickets")
    if not data["Help & Support"].empty:
        # Filter for open or in-progress tickets
        # For demo, let's just pick a random user to display their tickets
        demo_user_tickets = data["Help & Support"][data["Help & Support"]['user_id'] == random.choice(data["Help & Support"]['user_id'].unique())].head(5).reset_index(drop=True)

        if not demo_user_tickets.empty:
            st.write(f"Showing sample tickets for user: **{demo_user_tickets.iloc[0]['user_id']}**")
            for i, ticket in demo_user_tickets.iterrows():
                with st.container(border=True):
                    status_color = 'orange' if ticket['status'] == 'In Progress' else 'green' if ticket['status'] == 'Resolved' or ticket['status'] == 'Closed' else 'red'
                    st.markdown(f"**Ticket ID:** {ticket['ticket_id']} | **Issue Type:** {ticket['issue_type']}")
                    st.markdown(f"**Status:** <span style='color:{status_color}; font-weight:bold;'>{ticket['status']}</span>", unsafe_allow_html=True)
                    st.caption(f"Created: {ticket['created_at'].strftime('%Y-%m-%d %H:%M')}")
                    with st.expander("View Details"):
                        st.write(ticket['description'])
                        if pd.notna(ticket['resolved_at']):
                            st.info(f"Resolved on: {ticket['resolved_at'].strftime('%Y-%m-%d %H:%M')} by Agent {ticket['agent_id']}")
        else:
            st.info("No open support tickets found for this sample.")

    with st.expander("View All Help & Support Tickets (Tabular)"):
        st.dataframe(data["Help & Support"], use_container_width=True)

elif selected_tab == "📧 Contact Us":
    st.markdown("### Get in Touch!")
    st.write("Have a general inquiry? Send us a message.")

    with st.form("contact_us_form"):
        st.subheader("Your Information")
        contact_name = st.text_input("Your Name")
        contact_email = st.text_input("Your Email")
        contact_message = st.text_area("Your Message", height=150)

        contact_submitted = st.form_submit_button("Send Message")

        if contact_submitted:
            if not contact_name or not contact_email or not contact_message:
                st.error("Please fill in all fields (Name, Email, Message).")
            elif "@" not in contact_email or "." not in contact_email:
                st.error("Please enter a valid email address.")
            else:
                new_contact_id = f"CONT_{len(data['Contact Us']) + 1:04d}"
                st.success("Thank you for your message! We will get back to you soon.")
                st.info("Note: This is a demo. Data is not permanently stored or added to the underlying DataFrame.")
                # You would add contact data to a database here.

    st.markdown("---")
    st.subheader("Recent Contacts")
    if not data["Contact Us"].empty:
        # Display recent contacts
        recent_contacts = data["Contact Us"].sort_values(by='timestamp', ascending=False).head(5).reset_index(drop=True)
        for i, contact in recent_contacts.iterrows():
            response_status_color = 'orange' if contact['response_status'] == 'Pending' else 'green'
            st.markdown(f"**[{contact['timestamp'].strftime('%Y-%m-%d %H:%M')}]** From **{contact['name']}** ({contact['email']}) - Status: <span style='color:{response_status_color}; font-weight:bold;'>{contact['response_status']}</span>", unsafe_allow_html=True)
    else:
        st.info("No recent contact messages.")

    with st.expander("View All Contact Us Data (Tabular)"):
        st.dataframe(data["Contact Us"], use_container_width=True)

# Footer
st.markdown("---")
st.write("© 2025 Sportsphere. All rights reserved. | Developed with Streamlit")

