import numpy as np
import pandas as pd
import streamlit as st

from views import get_active_players_rankings, get_rankings

st.write("# Pocker Rank 👋")


def calculate_standardized_rank(row):
    return 2 * (row["total_players"] - row["rank"]) / (row["total_players"] - 1) - 1


def apply_weight(row):
    weight = np.exp(0.1 * row["total_players"])
    return row["standardized_rank"] * weight


def get_rank_result(df):
    df["total_players"] = df.groupby("played_at")["name"].transform("count")
    df["standardized_rank"] = df.apply(calculate_standardized_rank, axis=1)
    df["final_score"] = df.apply(apply_weight, axis=1)
    result = df.groupby("name")["final_score"].mean().reset_index()
    result = result.sort_values(by="final_score", ascending=False)
    return result


def get_last_rank_result(df):
    df = df.sort_values(by="played_at", ascending=False)
    recent_date = df["played_at"].head(1)
    df = df[~df["played_at"].isin(recent_date)]
    df = get_rank_result(df)
    return df


data = get_active_players_rankings().data
df = pd.DataFrame(data)
result = get_rank_result(df)
last_result = get_last_rank_result(df)
result = pd.merge(result, last_result, on="name", how="inner")
result["change"] = result["final_score_x"] - result["final_score_y"]

for rank, row in result.iterrows():
    score = round(row["final_score_x"], 3)
    change = round(row["change"], 5)

    st.metric(
        label=f"RANK: {rank + 1} , SCORE : {score}",
        value=row["name"],
        delta=change,
    )

raw_rankings_button = st.button("Click, If you wanna check raw rankings")
if raw_rankings_button:
    data = get_rankings().data
    df = pd.DataFrame(data)
    st.dataframe(df, hide_index=True, use_container_width=True)
