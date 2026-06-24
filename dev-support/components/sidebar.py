# frontend/components/sidebar.py

import streamlit as st


def load_sidebar_css():
    try:
        with open("./styles/sidebar.css", "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass


def render_sidebar():
    load_sidebar_css()

    result = st.session_state.get("agent_result")

    with st.sidebar:

        st.markdown(
            '<div class="agent-monitor-title">🤖 Agent Monitor</div>',
            unsafe_allow_html=True,
        )

        if st.session_state.get("query_running", False):
            st.info("⏳ Processing query...")

        elif result and isinstance(result, dict) and result.get("agent"):

            agent   = result.get("agent",      "N/A")
            route   = result.get("route",      "N/A")
            latency = result.get("latency",    "N/A")
            cache   = result.get("cache",      "miss")
            conf    = result.get("confidence", 0)
            chunks  = result.get("retrieved_chunks", 0)

            st.markdown(
                f"""
                <div class="agent-card">
                    <div class="agent-label">Agent</div>
                    <div class="agent-value">{agent}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(
                f"""
                <div class="agent-card">
                    <div class="agent-label">Route</div>
                    <div class="agent-value">{route}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(
                f"""
                <div class="agent-card">
                    <div class="agent-label">Latency</div>
                    <div class="agent-value">{latency} ms</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(
                f"""
                <div class="agent-card">
                    <div class="agent-label">Confidence</div>
                    <div class="agent-value">{conf}%</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(
                f"""
                <div class="agent-card">
                    <div class="agent-label">Chunks</div>
                    <div class="agent-value">{chunks}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(
                f"""
                <div class="agent-card">
                    <div class="agent-label">Cache</div>
                    <div class="agent-value">{"⚡ Hit" if cache == "hit" else "❌ Miss"}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        else:
            st.markdown(
                '<div class="status-info">No query processed yet</div>',
                unsafe_allow_html=True,
            )

        st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown(
            '<div class="section-title">System Status</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="status-success">FastAPI Connected</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="status-success">Retriever Active</div>',
            unsafe_allow_html=True,
        )

    # model selector in its own sidebar block
    with st.sidebar:
        selected_model = st.selectbox(
            "LLM Model",
            ["gpt-4o-mini", "gpt-4.1-mini"],
            index=0,
            key="llm_model_selector",
        )
        st.session_state["model_name"] = selected_model