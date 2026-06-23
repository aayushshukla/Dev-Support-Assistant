import requests
import streamlit as st
import mimetypes
from components.sidebar import (
    render_sidebar
)
from components.analytics_bar import (
    render_analytics_bar
)
from components.dashboardcomponent import (
    render_dashboard
)


API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Developer Support Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Developer Support Assistant")
if "show_dashboard" not in st.session_state:
    st.session_state.show_dashboard = False
col1, col2 = st.columns([1, 1])

with col1:

    if st.button("📊 Dashboard"):

        st.session_state.show_dashboard = True

with col2:

    if st.button("💬 Assistant"):

        st.session_state.show_dashboard = False
if st.session_state.show_dashboard:

    render_dashboard()

    st.stop()
st.markdown(
    """
Upload CSV, PDF and Markdown documentation
and ask questions using RAG + pgvector.
"""
)

# =====================================================
# SESSION STATE
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent_result" not in st.session_state:
    st.session_state.agent_result = None

render_sidebar()

    
# =====================================================
# SIDEBAR
# =====================================================
# =====================================================
# DOCUMENT UPLOAD SECTION
# =====================================================
#
# Responsibilities:
# 1. Allow users to upload supported documents.
# 2. Send uploaded files to FastAPI backend.
# 3. Display ingestion statistics.
# 4. Handle duplicate document detection.
# 5. Provide upload feedback to the user.
#
# Supported Formats:
# - CSV
# - PDF
# - Markdown (.md)
#
# Upload Flow:
#
# Streamlit UI
#       │
#       ▼
# FastAPI /upload
#       │
#       ▼
# Upload Agent
#       │
#       ▼
# CSV / PDF / Markdown Loader
#       │
#       ▼
# Chunking
#       │
#       ▼
# Embedding Generation
#       │
#       ▼
# PGVector Storage
#
# =====================================================

with st.sidebar:

    st.header("📄 Upload Document")

    st.markdown(
        """
### Supported Formats

- CSV
- PDF
- Markdown (.md)
"""
    )

    # ----------------------------------------------
    # FILE UPLOADER
    # ----------------------------------------------
    #
    # Allows users to upload:
    # CSV documentation
    # PDF documents
    # Markdown files
    #
    uploaded_file = st.file_uploader(
        "Choose Document",
        type=[
            "csv",
            "pdf",
            "md"
        ]
    )

    if uploaded_file:

        st.info(
            f"Selected File: {uploaded_file.name}"
        )

        # ------------------------------------------
        # UPLOAD BUTTON
        # ------------------------------------------
        #
        # Triggers ingestion pipeline.
        #
        if st.button("Upload & Index"):

            with st.spinner(
                "Uploading and indexing..."
            ):

                # ----------------------------------
                # DETERMINE MIME TYPE
                # ----------------------------------
                #
                # Required when sending file
                # to FastAPI endpoint.
                #
                mime_type = (
                    mimetypes.guess_type(
                        uploaded_file.name
                    )[0]
                    or
                    "application/octet-stream"
                )

                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file,
                        mime_type
                    )
                }

                try:

                    # ------------------------------
                    # CALL FASTAPI UPLOAD ENDPOINT
                    # ------------------------------
                    response = requests.post(
                        f"{API_BASE_URL}/upload",
                        files=files,
                        timeout=600
                    )

                    result = response.json()
                    st.session_state.agent_result = result
                    print(result)

                    st.session_state["analytics"] = {

                                "retrieved_chunks":
                                    result.get(
                                        "retrieved_chunks",
                                        0
                                    ),

                                "reranked_chunks":
                                    len(
                                        result.get(
                                            "sources",
                                            []
                                        )
                                    ),

                                "sources_used":
                                    result.get(
                                        "stats",
                                        {}
                                    ).get(
                                        "sources_used",
                                        0
                                    ),

                                "confidence": 95,

                                "vector_time_ms":
                                    result.get(
                                        "stats",
                                        {}
                                    ).get(
                                        "retrieval_time_ms",
                                        0
                                    ),

                                "llm_time_ms":
                                    result.get(
                                        "stats",
                                        {}
                                    ).get(
                                        "llm_time_ms",
                                        0
                                    ),

                                "total_time_ms":
                                    result.get(
                                        "stats",
                                        {}
                                    ).get(
                                        "total_time_ms",
                                        0
                                    ),

                                "response_tokens":
                                    len(
                                        result.get(
                                            "answer",
                                            ""
                                        ).split()
                                    )
                            }

                    answer = result.get(
                        "answer",
                        "No answer returned."
                    )
                    # ------------------------------
                    # REQUEST FAILURE
                    # ------------------------------
                    if response.status_code != 200:

                        st.error(
                            "Upload request failed."
                        )

                    # ------------------------------
                    # DUPLICATE DOCUMENT
                    # ------------------------------
                    #
                    # Triggered when content hash
                    # already exists in database.
                    #
                    elif result.get(
                        "status"
                    ) == "duplicate":

                        st.warning(
                            "Document already exists in the knowledge base."
                        )

                        duplicate_files = result.get(
                            "duplicate_files",
                            []
                        )

                        if duplicate_files:

                            st.markdown(
                                "### Duplicate Files"
                            )

                            for file in duplicate_files:

                                st.write(
                                    f"• {file}"
                                )

                    # ------------------------------
                    # SUCCESSFUL INGESTION
                    # ------------------------------
                    elif result.get(
                        "status"
                    ) == "success":

                        st.success(
                            "Upload completed successfully."
                        )

                        # Display uploaded file type
                        st.info(
                            f"File Type: "
                            f"{uploaded_file.name.split('.')[-1].upper()}"
                        )

                        # --------------------------
                        # INGESTION METRICS
                        # --------------------------
                        #
                        # Shows:
                        # - Documents processed
                        # - Chunks generated
                        #
                        col1, col2 = st.columns(
                            2
                        )

                        with col1:

                            st.metric(
                                "Documents",
                                result.get(
                                    "documents_processed",
                                    0
                                )
                            )

                        with col2:

                            st.metric(
                                "Chunks",
                                result.get(
                                    "chunks_created",
                                    0
                                )
                            )

                        # --------------------------
                        # DUPLICATE SUMMARY
                        # --------------------------
                        duplicate_count = result.get(
                            "duplicate_documents",
                            0
                        )

                        if duplicate_count > 0:

                            st.warning(
                                f"{duplicate_count} duplicate document(s) skipped."
                            )

                    # ------------------------------
                    # GENERAL FAILURE
                    # ------------------------------
                    else:

                        st.error(
                            result.get(
                                "error",
                                "Upload failed."
                            )
                        )

                except Exception as e:

                    # --------------------------
                    # NETWORK / API ERROR
                    # --------------------------
                    st.error(
                        f"Upload Error: {str(e)}"
                    )

    st.divider()

    # =================================================
    # SYSTEM INFORMATION
    # =================================================
    #
    # Displays current technology stack.
    #
    st.markdown(
        """
### System

- PostgreSQL + pgvector
- BGE Embeddings
- Hybrid Retrieval
- Reranker
- GPT Generation

### Supported Uploads

- CSV
- PDF
- Markdown
"""
    )
# =====================================================
# CHAT HISTORY
# =====================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

# =====================================================
# CHAT INPUT
# =====================================================

query = st.chat_input(
    "Ask a technical question..."
)

if query:

    # ----------------------------------
    # USER MESSAGE
    # ----------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )

    with st.chat_message("user"):

        st.markdown(query)

    # ----------------------------------
    # ASSISTANT
    # ----------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "Searching documentation..."
        ):

            try:

                response = requests.post(
                    f"{API_BASE_URL}/ask",
                    json={
                        "query": query
                    },
                    timeout=300
                )

                result = response.json()
                st.session_state.agent_result=result
                stats_response = requests.get(
                f"{API_BASE_URL}/stats"
                      )
                
                kb_stats = stats_response.json()
                st.session_state["analytics"] = {

                                # Knowledge Base

                                "total_documents":
                                    kb_stats.get(
                                        "total_documents",
                                        0
                                    ),

                                "total_chunks":
                                    kb_stats.get(
                                        "total_chunks",
                                        0
                                    ),

                                "total_domains":
                                    kb_stats.get(
                                        "total_domains",
                                        0
                                    ),

                                "total_categories":
                                    kb_stats.get(
                                        "total_categories",
                                        0
                                    ),

                                # Retrieval

                                "retrieved_chunks":
                                    result.get(
                                        "retrieved_chunks",
                                        0
                                    ),

                                "reranked_chunks":
                                    len(
                                        result.get(
                                            "sources",
                                            []
                                        )
                                    ),

                                "sources_used":
                                    result.get(
                                        "stats",
                                        {}
                                    ).get(
                                        "sources_used",
                                        0
                                    ),

                                "confidence": 95,

                                # Performance

                                "vector_time_ms":
                                    result.get(
                                        "stats",
                                        {}
                                    ).get(
                                        "retrieval_time_ms",
                                        0
                                    ),

                                "llm_time_ms":
                                    result.get(
                                        "stats",
                                        {}
                                    ).get(
                                        "llm_time_ms",
                                        0
                                    ),

                                "total_time_ms":
                                    result.get(
                                        "stats",
                                        {}
                                    ).get(
                                        "total_time_ms",
                                        0
                                    ),

                                "response_tokens":
                                    len(
                                        result.get(
                                            "answer",
                                            ""
                                        ).split()
                                    )
                            }
                answer = result.get(
                    "answer",
                    "No answer returned."
                )

                sources = result.get(
                    "sources",
                    []
                )
                if "analytics" in st.session_state:

                    render_analytics_bar(
                        st.session_state[
                            "analytics"
                        ]
                    )
                if result.get("source_type") == "external":

                    st.warning(
                        "🌐 Answer generated from external documentation"
                    )
                st.markdown(answer)

                # Save chat history

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

                # ----------------------------------
                # SOURCE ATTRIBUTION
                # ----------------------------------

                if sources:

                    with st.expander(
                        "📚 Sources"
                    ):

                        for idx, source in enumerate(
                            sources,
                            start=1
                        ):

                            st.markdown(
                                f"### Source {idx}"
                            )

                            st.write(
                                f"**Title:** "
                                f"{source.get('title','N/A')}"
                            )

                            st.write(
                                f"**Domain:** "
                                f"{source.get('domain','N/A')}"
                            )

                            st.write(
                                f"**URL:** "
                                f"{source.get('source_url','N/A')}"
                            )

                            rerank_score = source.get(
                                "rerank_score"
                            )

                            if rerank_score:

                                st.write(
                                    f"**Score:** "
                                    f"{round(rerank_score,4)}"
                                )

                            st.divider()

            except Exception as e:

                error_message = (
                    f"Error: {str(e)}"
                )

                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message
                    }
                )