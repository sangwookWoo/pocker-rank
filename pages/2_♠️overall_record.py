import numpy as np
import pandas as pd
import streamlit as st

from views import get_player_rankings, get_players

st.write("# Overall record")


players = get_players().data
player_names = [player["name"] for player in players]
selected_name = st.selectbox(f"players", options=player_names)
selected_id = next(
    player["id"] for player in players if player["name"] == selected_name
)

data = get_player_rankings(selected_id).data
st.write(f"### Total Play : {len(data)} Games")
df = pd.DataFrame(data)
grouped_df = (
    df.groupby("rank")["player_id"]
    .count()
    .reset_index()
    .rename(columns={"player_id": "count"})
)
st.bar_chart(grouped_df.set_index("rank"), x_label="rank", y_label="count")
