import streamlit as st


def load_sidebar_css():

    with open(
        "./styles/sidebar.css",
        "r",
        encoding="utf-8"
    ) as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

def render_sidebar():

    load_sidebar_css()

    result = st.session_state.get(
        "agent_result"
    )

    with st.sidebar:

        st.markdown(
            """
            <div class="agent-monitor-title">
                🤖 Agent Monitor
            </div>
            """,
            unsafe_allow_html=True
        )

        if result:

            st.markdown(
                f"""
                <div class="agent-card">
                    
                        Agent
                   

                   
                        {result.get('agent','N/A')}
                    
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
               <div class="agent-card">
                    <div class="agent-label">
                        Route
                    </div>
                    <div class="agent-value">
                       {result.get('route','N/A')}
                    </div>
                </div>
                    
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="agent-card">
                    <div class="agent-label">
                        Latency
                    </div>
                    <div class="agent-value">
                        {result.get("latency", "N/A")} sec
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                """
                <div class="status-info">
                    No query processed yet
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class="section-title">
                System Status
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="status-success">
                FastAPI Connected
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="status-success">
                Retriever Active
            </div>
            """,
            unsafe_allow_html=True
        )
    with st.sidebar:

        selected_model = st.selectbox(
            "LLM Model",
            [
                "gpt-4o-mini",
                "gpt-4.1-nano"
            ],
            index=0,
            key="llm_model_selector"
        )

        st.session_state["model_name"] = (
            selected_model
        )