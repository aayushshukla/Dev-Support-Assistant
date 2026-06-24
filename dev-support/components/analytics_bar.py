import streamlit as st



def load_analytics_css():

    with open(
        "./styles/analytics_bar.css",
        "r",
        encoding="utf-8"
    ) as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

def render_analytics_bar(stats):
    load_analytics_css()
    st.markdown(
        """
        <div class="analytics-header">
            <h3>📊 RAG Analytics Dashboard</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Knowledge Base Metrics
    st.markdown("### Knowledge Base")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Documents",
        stats.get("total_documents", 0)
    )

    col2.metric(
        "Chunks",
        stats.get("total_chunks", 0)
    )

    col3.metric(
        "Domains",
        stats.get("total_domains", 0)
    )

    col4.metric(
        "Categories",
        stats.get("total_categories", 0)
    )

    st.divider()

    # Retrieval Metrics
    st.markdown("### Retrieval")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Retrieved",
        stats.get("retrieved_chunks", 0)
    )

    col2.metric(
        "Reranked",
        stats.get("reranked_chunks", 0)
    )

    col3.metric(
        "Sources",
        stats.get("sources_used", 0)
    )

    col4.metric(
        "Confidence",
        f"{stats.get('confidence', 0)}%"
    )


  

    st.divider()

    # Performance Metrics
    st.markdown("### Performance")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Search",
        f"{stats.get('vector_time_ms', 0)} ms"
    )

    col2.metric(
        "LLM",
        f"{stats.get('llm_time_ms', 0)} ms"
    )

    col3.metric(
        "Total",
        f"{stats.get('total_time_ms', 0)} ms"
    )

    col4.metric(
        "Tokens",
        stats.get("response_tokens", 0)
    )