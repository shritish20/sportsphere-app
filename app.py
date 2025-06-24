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

# --- Data Generation Logic (MOVED HERE - and kept for self-containment) ---
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
    end_date = datetime(2025, 6, 24) # Current date is Tuesday, June 24, 2025
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
data = generate_all_data()

# --- Streamlit App Layout ---

# Custom CSS for better styling (minimal example)
st.markdown("""
<style>
    .st-emotion-cache-nahz7x { /* Targeting the main content area */
        padding-top: 2rem;
        padding-right: 3rem;
        padding-left: 3rem;
        padding-bottom: 2rem;
    }
    h1, h2, h3 {
        color: #FF4B4B; /* A sporty red */
    }
    .stSelectbox label, .stTextInput label, .stDateInput label {
        font-weight: bold;
    }
    .stButton > button {
        background-color: #FF4B4B;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 0.5rem 1rem;
    }
    .stButton > button:hover {
        background-color: #FF7B7B;
    }
    div[data-testid="stSidebar"] {
        background-color: #f0f2f6; /* Light grey for sidebar */
    }
    .st-emotion-cache-1jmve30 { /* Card-like background for containers */
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.05);
        margin-bottom: 1rem;
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
                    st.write(f"*{row['message']}*")
                    st.caption(f"_{row['timestamp'].strftime('%Y-%m-%d %H:%M')}_")
        st.markdown("---")
        # Optional: Show more feed items in a collapsible expander
        with st.expander("View All Feed Items (Tabular)"):
            st.dataframe(data["Feed"], use_container_width=True)

elif selected_tab == "📊 Cricket Scores":
    st.markdown("### Live & Upcoming Cricket Matches")
    st.write("Get real-time updates and schedules for your favorite cricket games.")

    if not data["Cricket Scores"].empty:
        live_matches = data["Cricket Scores"][data["Cricket Scores"]['status'] == 'Live'].head(5)
        upcoming_matches = data["Cricket Scores"][data["Cricket Scores"]['status'] == 'Upcoming'].head(5)
        completed_matches = data["Cricket Scores"][data["Cricket Scores"]['status'] == 'Completed'].head(5)

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

    if not data["Multi-Sport Scores"].empty:
        col_sport_filter, col_status_filter = st.columns(2)
        all_sports = ['All'] + sorted(data["Multi-Sport Scores"]['sport_name'].unique().tolist())
        selected_sport = col_sport_filter.selectbox("Filter by Sport", all_sports)

        all_statuses = ['All'] + sorted(data["Multi-Sport Scores"]['status'].unique().tolist())
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
                    st.caption(f"Status: {match['status']} | Time: {match['time_elapsed']}")
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
        sport_type = st.selectbox("Sport Type", sports)
        team1 = st.selectbox("Team 1", team_names, key="team1_select")
        team2 = st.selectbox("Team 2", [t for t in team_names if t != team1], key="team2_select") # Ensure teams are different
        venue = st.selectbox("Venue", venues)
        match_format = st.selectbox("Match Format", match_formats)
        num_overs = st.number_input("Number of Overs (for Cricket)", min_value=1, max_value=50, value=20 if sport_type == 'Cricket' else 0, disabled=(sport_type != 'Cricket'))
        start_date_input = st.date_input("Match Date", datetime.now().date())
        start_time_input = st.time_input("Match Time", datetime.now().time())

        st.subheader("Officials")
        umpire1 = st.text_input("Umpire 1 Name", fake.name())
        umpire2 = st.text_input("Umpire 2 Name", fake.name())
        scorer = st.text_input("Scorer Name", fake.name())

        submitted = st.form_submit_button("Create Match")

        if submitted:
            if team1 == team2:
                st.error("Team 1 and Team 2 cannot be the same!")
            else:
                new_match_id = f"MID_{len(data['Start Scoring']) + 901:05d}"
                st.success(f"Match '{new_match_id}' between {team1} and {team2} created successfully!")
                st.info("Note: This is a demo. Data is not permanently stored or added to the underlying DataFrame.")
                # In a real app, you would append this to your data source/database.
                # Example:
                # new_match_row = pd.DataFrame([{
                #     'match_id': new_match_id,
                #     'sport_type': sport_type,
                #     'teams': [team1, team2],
                #     'start_time': datetime.combine(start_date_input, start_time_input),
                #     'venue': venue,
                #     'umpires': umpire1,
                #     'scorers': scorer,
                #     'match_format': match_format,
                #     'number_of_overs': num_overs if sport_type == 'Cricket' else None,
                #     'status': 'Scheduled'
                # }])
                # data["Start Scoring"] = pd.concat([data["Start Scoring"], new_match_row], ignore_index=True)


    st.markdown("---")
    with st.expander("View Existing Matches (Tabular)"):
        st.dataframe(data["Start Scoring"], use_container_width=True)

elif selected_tab == "🏆 Start a Tournament":
    st.markdown("### Organize a New Tournament!")
    st.write("Plan and manage your tournaments with ease.")

    with st.form("new_tournament_form"):
        st.subheader("Tournament Details")
        tournament_name = st.text_input("Tournament Name", f"{fake.word().capitalize()} Cup")
        organizer_name = st.text_input("Organizer Name", fake.name())
        start_date_t = st.date_input("Start Date", datetime.now().date())
        end_date_t = st.date_input("End Date", datetime.now().date() + timedelta(days=7))
        tournament_location = st.selectbox("Location", venues)
        tournament_format = st.selectbox("Tournament Format", tournament_formats)

        st.subheader("Participating Teams (Select at least 2)")
        selected_teams = st.multiselect("Select Teams", team_names, default=random.sample(team_names, k=min(4, len(team_names))))

        submitted_tournament = st.form_submit_button("Create Tournament")

        if submitted_tournament:
            if len(selected_teams) < 2:
                st.error("Please select at least two teams for the tournament.")
            elif start_date_t > end_date_t:
                st.error("End Date cannot be before Start Date.")
            else:
                new_tournament_id = f"TID_{len(data['Start a Tournament']) + 51:05d}"
                st.success(f"Tournament '{tournament_name}' ({new_tournament_id}) created successfully with {len(selected_teams)} teams!")
                st.info("Note: This is a demo. Data is not permanently stored or added to the underlying DataFrame.")
                # In a real app, you would append this to your data source/database.

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
                    st.write(f"**Dates:** {row['start_date'].strftime('%b %d')} - {row['end_date'].strftime('%b %d')}")
                    st.write(f"**Location:** {row['location']}")
                    st.write(f"**Format:** {row['format']}")
                    st.write(f"**Teams:** {', '.join(row['teams_list'][:3])}{'...' if len(row['teams_list']) > 3 else ''}")
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

        user_matches = data["My Matches"][data["My Matches"]['user_id'] == selected_user].sort_values(by='date', ascending=False)

        if not user_matches.empty:
            st.subheader(f"Matches for {selected_user}")
            for i, match in user_matches.iterrows():
                with st.container(border=True):
                    st.write(f"**Match ID:** {match['match_id']}")
                    st.write(f"**Role:** {match['role']}")
                    st.write(f"**Status:** {match['participation_status']}")
                    st.write(f"**Result:** {match['result']}")
                    if pd.notna(match['performance_summary']) and match['performance_summary'] != '':
                        st.write(f"**Performance:** {match['performance_summary']}")
                    st.caption(f"Date: {match['date'].strftime('%Y-%m-%d')}")
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
        selected_team = st.selectbox("Select a Team", team_options)

        team_info = data["My Teams"][data["My Teams"]['team_name'] == selected_team].iloc[0]

        if not team_info.empty:
            st.subheader(f"Details for {team_info['team_name']}")
            col_img, col_details = st.columns([0.2, 0.8])
            with col_img:
                st.image(team_info['logo_url'], width=100) # Placeholder image
            with col_details:
                st.write(f"**Sport Type:** {team_info['sport_type']}")
                st.write(f"**Created By:** {team_info['created_by']}")
                st.write(f"**Captain ID:** {team_info['captain_id']}")
                st.write(f"**Rating:** ⭐ {team_info['rating']}")
                st.write(f"**Wins/Losses:** {team_info['wins']} / {team_info['losses']}")

            st.markdown("#### Team Roster")
            players_list = team_info['players_list']
            if isinstance(players_list, str): # Handle case where list might be stringified from CSV
                import ast
                players_list = ast.literal_eval(players_list)

            player_columns = st.columns(4) # Display players in columns
            for idx, player in enumerate(players_list):
                with player_columns[idx % 4]:
                    st.markdown(f"- {player}")
        else:
            st.info("Team not found.")

    st.markdown("---")
    with st.expander("View All My Teams Data (Tabular)"):
        st.dataframe(data["My Teams"], use_container_width=True)

elif selected_tab == "📈 My Stats":
    st.markdown("### Your Player Statistics")
    st.write("Review your career performance and achievements.")

    if not data["My Stats"].empty and not data["Profile"].empty:
        # Combine stats and profile data for a richer view
        merged_stats_profile = pd.merge(data["My Stats"], data["Profile"], on='user_id', how='left')

        all_player_ids = sorted(merged_stats_profile['user_id'].unique().tolist())
        selected_player_id = st.selectbox("Select Your Player ID", all_player_ids, index=0)

        player_data = merged_stats_profile[merged_stats_profile['user_id'] == selected_player_id].iloc[0]

        if not player_data.empty:
            st.subheader(f"Stats for {player_data['name']}")
            col_photo, col_basic_info = st.columns([0.2, 0.8])
            with col_photo:
                st.image(player_data['photo_url'], width=150)
            with col_basic_info:
                st.write(f"**Level:** {player_data['level']}")
                st.write(f"**Bio:** {player_data['bio']}")
                st.write(f"**Location:** {player_data['location']}")
                st.write(f"**Teams Joined:** {', '.join(player_data['teams_joined'])}")

            st.markdown("#### Key Performance Indicators")
            kpi1, kpi2, kpi3, kpi4 = st.columns(4)
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
            if player_data['achievements']:
                for achievement in player_data['achievements']:
                    st.success(f"🏅 {achievement}")
            else:
                st.info("No notable achievements yet!")

            # Simple bar chart for a few key stats
            chart_data = pd.DataFrame({
                'Metric': ['Runs', 'Wickets', 'Catches'],
                'Value': [player_data['runs_scored'], player_data['wickets_taken'], player_data['catches']]
            })
            fig = px.bar(chart_data, x='Metric', y='Value', title=f"Performance Summary for {player_data['name']}")
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
            # Display highlights in a grid-like fashion
            cols = st.columns(3)
            for i, highlight in filtered_highlights.head(15).iterrows(): # Show top 15 highlights
                with cols[i % 3]:
                    with st.container(border=True):
                        st.subheader(highlight['event_description'])
                        st.write(f"**Player:** {highlight['player']}")
                        st.write(f"**Match ID:** {highlight['match_id']}")
                        st.caption(f"Recorded: {highlight['timestamp'].strftime('%Y-%m-%d %H:%M')}")
                        if highlight['media_type'] == 'Video':
                            # In a real app, you'd embed a video player here
                            st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") # Example YouTube link (Rickroll)
                            st.caption("*(Placeholder Video)*")
                        else: # Image
                            st.image("https://via.placeholder.com/150", caption="Highlight Image", width=150)
                            st.caption("*(Placeholder Image)*")
                        st.link_button("Watch/View Full", highlight['url'])
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
                st.error("Please fill in all required personal details.")
            elif not user_sports_interested:
                st.error("Please select at least one sport you're interested in.")
            else:
                new_user_id = f"UID_{len(data['Create Account']) + 10001:05d}"
                st.success(f"Welcome, {user_name}! Your account ({new_user_id}) has been created successfully.")
                st.info("Note: This is a demo. Data is not permanently stored or added to the underlying DataFrame.")
                # In a real app, you would save this new user data to a database.

    st.markdown("---")
    with st.expander("View Existing Accounts (Tabular)"):
        st.dataframe(data["Create Account"], use_container_width=True)


elif selected_tab == "🛒 Shop":
    st.markdown("### Sportsphere Shop")
    st.write("Browse and buy the latest sports gear!")

    if not data["Shop"].empty:
        product_categories = ['All'] + data["Shop"]['category'].unique().tolist()
        selected_category = st.selectbox("Filter by Category", product_categories)

        filtered_products = data["Shop"]
        if selected_category != 'All':
            filtered_products = filtered_products[filtered_products['category'] == selected_category]

        if not filtered_products.empty:
            # Display products in a grid (3 columns)
            cols = st.columns(3)
            for i, product in filtered_products.iterrows():
                with cols[i % 3]:
                    with st.container(border=True):
                        st.image(product['image_url'], caption=product['name'], use_column_width=True) # Use a placeholder image
                        st.subheader(product['name'])
                        st.markdown(f"**Price:** ₹{product['price']:.2f}")
                        st.caption(f"Category: {product['category']}")
                        st.write(f"Rating: ⭐ {product['ratings']} ({product['sold_count']} sold)")
                        if product['inventory_count'] > 0:
                            st.success(f"In Stock: {product['inventory_count']}")
                            st.button(f"Add to Cart", key=f"add_to_cart_{product['product_id']}")
                        else:
                            st.error("Out of Stock")
        else:
            st.info("No products found for the selected category.")

    st.markdown("---")
    with st.expander("View All Shop Products (Tabular)"):
        st.dataframe(data["Shop"], use_container_width=True)

elif selected_tab == "🧍‍♂️ Profile":
    st.markdown("### Your Sportsphere Profile")
    st.write("Manage your public profile and view your comprehensive stats.")

    if not data["Profile"].empty:
        all_profile_ids = sorted(data["Profile"]['user_id'].unique().tolist())
        selected_profile_id = st.selectbox("Select Your Profile", all_profile_ids, index=0)

        profile_info = data["Profile"][data["Profile"]['user_id'] == selected_profile_id].iloc[0]

        if not profile_info.empty:
            col_left, col_right = st.columns([0.3, 0.7])
            with col_left:
                st.image(profile_info['photo_url'], width=200, caption=profile_info['name'])
            with col_right:
                st.subheader(profile_info['name'])
                st.write(f"**Location:** {profile_info['location']}")
                st.write(f"**Level:** {profile_info['level']}")
                st.write(f"**Bio:** {profile_info['bio']}")
            
            st.markdown("---")
            st.subheader("Sports Journey")
            col_m, col_t = st.columns(2)
            col_m.metric("Matches Played", profile_info['matches_played'])
            col_t.metric("Tournaments Participated", profile_info['tournaments'])

            st.write(f"**Teams Joined:** {', '.join(profile_info['teams_joined'])}")

            st.markdown("#### Achievements")
            if profile_info['achievements']:
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
        current_lang = data["Change Language"][data["Change Language"]["is_default"] == True].iloc[0]['language_name']
        st.info(f"Current language: **{current_lang}**")

        lang_options = data["Change Language"]["language_name"].tolist()
        selected_lang = st.selectbox("Choose a new language", lang_options)

        if st.button("Apply Language"):
            st.success(f"Language changed to **{selected_lang}**! (This is a demo, actual language change not implemented)")
            # In a real app, you would update a user preference or session state
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
        recent_shares = data["Share App'].sort_values(by='timestamp', ascending=False).head(5)
        for i, share in recent_shares.iterrows():
            st.text(f"[{share['timestamp'].strftime('%Y-%m-%d %H:%M')}] {share['user_id']} shared on {share['platform']} to {share['shared_to']}.")
    else:
        st.info("No share activity recorded yet.")

    with st.expander("View All Share Data (Tabular)"):
        st.dataframe(data["Share App"], use_container_width=True)


elif selected_tab == "🆘 Help & Support":
    st.markdown("### Need Assistance?")
    st.write("Submit a support ticket and we'll get back to you.")

    with st.form("help_support_form"):
        st.subheader("Submit a New Ticket")
        ticket_user_id = st.text_input("Your User ID (e.g., UID_00001)")
        issue_type = st.selectbox("Type of Issue", issue_types)
        description = st.text_area("Describe your issue in detail", height=150)

        ticket_submitted = st.form_submit_button("Submit Ticket")

        if ticket_submitted:
            if not ticket_user_id or not description:
                st.error("Please provide your User ID and a description of the issue.")
            else:
                new_ticket_id = f"TICKET_{len(data['Help & Support']) + 201:05d}"
                st.success(f"Your ticket ({new_ticket_id}) has been submitted! We will review it shortly.")
                st.info("Note: This is a demo. Data is not permanently stored or added to the underlying DataFrame.")

    st.markdown("---")
    st.subheader("Your Open Tickets")
    if not data["Help & Support"].empty:
        # Filter for open or in-progress tickets
        open_tickets = data["Help & Support"][data["Help & Support"]['status'].isin(['Open', 'In Progress'])]
        if not open_tickets.empty:
            for i, ticket in open_tickets.iterrows():
                with st.container(border=True):
                    st.write(f"**Ticket ID:** {ticket['ticket_id']}")
                    st.write(f"**Issue Type:** {ticket['issue_type']}")
                    st.write(f"**Status:** {ticket['status']}")
                    st.caption(f"Created: {ticket['created_at'].strftime('%Y-%m-%d %H:%M')}")
                    with st.expander("View Details"):
                        st.write(ticket['description'])
        else:
            st.info("You have no open support tickets.")
    
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
                st.error("Please fill in all fields.")
            else:
                new_contact_id = f"CONT_{len(data['Contact Us']) + 201:05d}"
                st.success("Thank you for your message! We will get back to you soon.")
                st.info("Note: This is a demo. Data is not permanently stored or added to the underlying DataFrame.")
    
    st.markdown("---")
    st.subheader("Recent Contacts")
    if not data["Contact Us"].empty:
        # Display recent contacts
        recent_contacts = data["Contact Us"].sort_values(by='timestamp', ascending=False).head(5)
        for i, contact in recent_contacts.iterrows():
            st.text(f"[{contact['timestamp'].strftime('%Y-%m-%d %H:%M')}] From {contact['name']} ({contact['email']}) - Status: {contact['response_status']}")
    else:
        st.info("No recent contact messages.")

    with st.expander("View All Contact Us Data (Tabular)"):
        st.dataframe(data["Contact Us"], use_container_width=True)

# Footer
st.markdown("---")
st.write("© 2025 Sportsphere. All rights reserved. | Developed with Streamlit")

