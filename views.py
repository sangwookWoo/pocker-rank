import json
from datetime import datetime

import streamlit as st
from st_supabase_connection import SupabaseConnection, execute_query

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

st_supabase_client = st.connection(
    name="pocker",
    type=SupabaseConnection,
    ttl=None,
    url=SUPABASE_URL,
    key=SUPABASE_KEY,
)

SupabaseConnection


def get_players():
    return execute_query(
        st_supabase_client.table("players").select("id, name, is_active"), ttl="10m"
    )


def get_active_players():
    return execute_query(
        st_supabase_client.table("players").select("id, name").eq("is_active", True),
        ttl="10m",
    )


def insert_player(name):
    execute_query(
        st_supabase_client.table("players").insert([{"name": name}]),
    )


def insert_log(rankings):
    execute_query(
        st_supabase_client.table("rankings").insert(rankings),
    )


def get_rankings():
    return execute_query(
        st_supabase_client.table("rankings").select(
            "rank",
            "...players(name)",
            "played_at",
        ),
        ttl="10m",
    )


def get_player_rankings(player_id):
    return execute_query(
        st_supabase_client.table("rankings")
        .select(
            "rank",
            "player_id",
            "played_at",
        )
        .eq("player_id", player_id),
    )


def get_head_to_head_record(player_names):
    response = st_supabase_client.client.rpc(
        "get_head_to_head_record", {"player_names": player_names}
    ).execute()

    if response.data:
        return response.data
    else:
        return None
