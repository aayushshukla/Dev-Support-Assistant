# feedbackcomponent.py

import streamlit as st
import requests

API_BASE_URL = "http://127.0.0.1:8000"


def render_feedback_component(query, answer, agent):

    st.divider()
    st.markdown("### Was this answer helpful?")

    # ── use a stable index-based key, not the raw query string ──
    # query strings cause key conflicts when they contain
    # spaces, slashes or other special characters
    feedback_key = str(hash(query))

    col1, col2 = st.columns(2)

    def send_feedback(feedback_type):
        try:
            response = requests.post(
                f"{API_BASE_URL}/feedback",
                json={
                    "query":    query,
                    "answer":   answer,
                    "agent":    agent,
                    "feedback": feedback_type,
                },
                timeout=30,
            )
            if response.status_code == 200:
                st.success("Thank you for your feedback!")
            else:
                st.error(f"Failed to save feedback. Status: {response.status_code}")
        except Exception as e:
            st.error(f"Feedback Error: {str(e)}")

    with col1:
        if st.button("👍 Helpful", key=f"positive_{feedback_key}"):
            send_feedback("positive")

    with col2:
        if st.button("👎 Not Helpful", key=f"negative_{feedback_key}"):
            send_feedback("negative")