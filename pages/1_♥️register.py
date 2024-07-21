import datetime

import streamlit as st

from views import get_players, insert_log, insert_player

MANAGER_PASSWORD = st.secrets["MANAGER_PASSWORD"]

st.write("# Register Game record or players 👋")
(
    tab1,
    tab2,
) = st.tabs(["Game record", "Players"])

with tab1:
    date = st.date_input(
        "what date did you play the game?", value=datetime.datetime.now()
    )
    time = st.time_input("What time did you play the game?", value=datetime.time(12, 0))
    played_at = datetime.datetime.combine(date, time).strftime("%Y-%m-%d %H:%M:%S")

    num_participants = st.number_input(
        "How many people participated in the game today?", step=1
    )

    players = get_players().data
    player_names = [player["name"] for player in players]
    if num_participants:
        with st.form("Enter Rankings"):
            rankings = []
            for rank in range(1, int(num_participants) + 1):
                ranking = {}
                selected_name = st.selectbox(
                    f"rank {rank}", options=player_names, key=f"rank_{rank}"
                )
                selected_id = next(
                    player["id"]
                    for player in players
                    if player["name"] == selected_name
                )
                ranking["rank"] = rank
                ranking["player_id"] = selected_id
                ranking["played_at"] = played_at
                rankings.append(ranking)

            submitted = st.form_submit_button("Record Rank")
            if submitted:
                password = st.text_input("Enter Manager Password 👇", "")
                if password == MANAGER_PASSWORD:
                    insert_log(rankings)
                    st.write(f"ranking log is succesfully registered")
                else:
                    st.write("Password is wrong, Please Retry")


with tab2:
    name = st.text_input("Enter name of player 👇", "")
    if name != "":
        password = st.text_input("Enter Manager Password 👇", "")
        if password == MANAGER_PASSWORD:
            insert_player(name)
            st.write(f"player {name} is succesfully registered")
        else:
            st.write("Password is wrong, Please Retry")
