import base64
import os

import numpy as np
import pandas as pd
import streamlit as st
from streamlit_card import card

from views import get_active_players, get_head_to_head_record

# ui
styles = {
    "card": {
        "margin-top": "10px",
        "margin-bottom": "10px",
        "margin-left": "1px",
        "width": "300px",
        "height": "300px",
    },
}

# image
win_path = os.path.join(os.getcwd(), "win.jpeg")
with open(win_path, "rb") as f:
    data = f.read()
    encoded = base64.b64encode(data)
    winner_image = "data:image/jpeg;base64," + encoded.decode("utf-8")

lose_path = os.path.join(os.getcwd(), "lose.jpeg")
with open(lose_path, "rb") as f:
    data = f.read()
    encoded = base64.b64encode(data)
    loser_image = "data:image/jpeg;base64," + encoded.decode("utf-8")


players = get_active_players().data
player_names = [player["name"] for player in players]

st.title("Head to Head Match Score")
target_players = []
with st.form("Enter Rankings"):
    player_name1 = st.selectbox(f"player1", options=player_names, key="player1")
    player_name2 = st.selectbox(f"player2", options=player_names, key="player2")
    submitted = st.form_submit_button("SHOW")
    if submitted:
        if player_name1 == player_name2:
            st.write("please choose each other player")
        else:
            data = get_head_to_head_record([player_name1, player_name2])
            df = pd.DataFrame(data)
            # who is winner?
            resuilt_df = df.sort_values(by="wins", ascending=False).reset_index()
            winner = resuilt_df.loc[0, "name"]
            winner_wins = resuilt_df.loc[0, "wins"]

            loser = resuilt_df.loc[1, "name"]
            loser_wins = resuilt_df.loc[1, "wins"]

            if winner_wins == loser_wins:
                st.write("Draw..!")
            else:
                col1, col2 = st.columns(2)
                with col1:
                    card(
                        title=f"{winner}(WINNER)",
                        text=f"{winner_wins} WIN, {loser_wins} LOSE",
                        key="1",
                        styles={
                            "card": {
                                "margin-top": "10px",
                                "margin-bottom": "10px",
                                "margin-left": "1px",
                                "width": "300px",
                                "height": "300px",
                            },
                        },
                        image=winner_image,
                    )
                with col2:
                    card(
                        title=f"{loser}(LOSER)",
                        text=f"{loser_wins} WIN, {winner_wins} LOSE",
                        key="2",
                        styles={
                            "card": {
                                "margin-top": "10px",
                                "margin-bottom": "10px",
                                "margin-left": "1px",
                                "width": "220px",
                                "height": "150px",
                            },
                        },
                        image=loser_image,
                    )
