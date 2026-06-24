# frontend/components/dashboard.py

import streamlit as st
import pandas as pd
import requests


API_BASE_URL = "http://127.0.0.1:8000"


def render_dashboard():

    st.title(
        "📊 RAG Analytics Dashboard"
    )

    try:

        dashboard = requests.get(
            f"{API_BASE_URL}/dashboard"
        ).json()

        # =================================================
        # TOP METRICS
        # =================================================

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Documents",
            dashboard["documents"]
        )

        col2.metric(
            "Chunks",
            dashboard["chunks"]
        )

        col3.metric(
            "Domains",
            dashboard["domains"]
        )

        col4.metric(
            "Categories",
            dashboard["categories"]
        )

        st.divider()

        # =================================================
        # QUERY STATISTICS
        # =================================================
        st.subheader("📈 Query Statistics")

        query_stats = dashboard["query_stats"]

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Queries",
            query_stats.get(
                "total_queries",
                0
            )
        )

        col2.metric(
            "API Queries",
            query_stats.get(
                "api_queries",
                0
            )
        )

        col3.metric(
            "Code Queries",
            query_stats.get(
                "code_queries",
                0
            )
        )

        col4, col5, col6 , col7= st.columns(4)

        col4.metric(
            "Runbook Queries",
            query_stats.get(
                "runbook_queries",
                0
            )
        )

        col5.metric(
            "Document Queries",
            query_stats.get(
                "document_queries",
                0
            )
        )

        col6.metric(
            "Web Queries",
            query_stats.get(
                "web_queries",
                0
            )
        )
        col7.metric(
        "Memory Turns",
        len(
            st.session_state.get(
                "messages",
                []
            )
        )
)
        st.divider()

        st.divider()

# =================================================
# CACHE STATISTICS
# =================================================

        st.subheader(
            "⚡ Cache Statistics"
        )

        cache_stats = dashboard.get(
            "cache_stats",
            {}
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(

            "Cache Size",

            cache_stats.get(
                "cache_size",
                0
            )
        )

        col2.metric(

            "Cache Hits",

            cache_stats.get(
                "cache_hits",
                0
            )
        )

        col3.metric(

            "Cache Misses",

            cache_stats.get(
                "cache_misses",
                0
            )
        )

        col4.metric(

            "Hit Ratio %",

            cache_stats.get(
                "hit_ratio",
                0
            )
        )  

        st.divider()   
                
        # =================================================
        # AVAILABLE AGENTS
        # =================================================

        st.subheader(
            "🤖 Available Agents"
        )

        left, right = st.columns(2)

        with left:

            st.info(
                """
                🤖 Supervisor Agent

                Routes user queries
                to the correct agent.
                """
            )

            st.info(
                """
                📄 Document Agent

                General documentation
                question answering.
                """
            )

            st.info(
                """
                🌐 API Agent

                API endpoint analysis,
                request and response details.
                """
            )

        with right:

            st.info(
                """
                🔧 Runbook Agent

                Troubleshooting and
                incident resolution.
                """
            )

            st.info(
                """
                💻 Code Agent

                Explains classes,
                methods and functions.
                """
            )

        st.divider()

        # =================================================
        # AGENT DISTRIBUTION
        # =================================================

        st.subheader(
            "📈 Agent Distribution"
        )

        agent_df = pd.DataFrame(
            dashboard[
                "agent_distribution"
            ]
        )

        st.dataframe(
            agent_df,
            width="stretch"
        )

        st.bar_chart(
            agent_df.set_index(
                "agent_role"
            )
        )

        st.divider()

        # =================================================
        # AGENT COVERAGE
        # =================================================

        st.subheader(
            "📊 Agent Coverage"
        )

        total_docs = dashboard[
            "documents"
        ]

        coverage_rows = []

        for row in dashboard[
            "agent_distribution"
        ]:

            coverage_rows.append({

                "Agent":
                    row["agent_role"],

                "Documents":
                    row["count"],

                "Coverage %":
                    round(
                        (
                            row["count"]
                            /
                            total_docs
                        ) * 100,
                        2
                    )
            })

        coverage_df = pd.DataFrame(
            coverage_rows
        )

        st.dataframe(
            coverage_df,
            width="stretch"
        )

        st.divider()

        # =================================================
# FEEDBACK STATISTICS
# =================================================

        st.subheader(
            "👍 User Feedback"
        )

        feedback_stats = dashboard.get(
            "feedback_stats",
            {}
        )

        col1, col2, col3 = st.columns(3)

        positive = feedback_stats.get(
            "positive_feedback",
            0
        )

        negative = feedback_stats.get(
            "negative_feedback",
            0
        )

        total = positive + negative

        col1.metric(
            "👍 Positive",
            positive
        )

        col2.metric(
            "👎 Negative",
            negative
        )

        col3.metric(
            "📊 Total Feedback",
            total
        )

        # =================================================
        # SYSTEM STATUS
        # =================================================

        st.subheader(
            "🟢 System Status"
        )

        col1, col2, col3 = st.columns(3)

        col1.success(
            "FastAPI Connected"
        )

        col2.success(
            "Retriever Active"
        )

        col3.success(
            "Dashboard Active"
        )

    except Exception as e:

        st.error(
            f"Dashboard Error: {str(e)}"
        )