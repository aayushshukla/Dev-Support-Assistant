import requests
import streamlit as st
import mimetypes
from components.sidebar import render_sidebar
from components.analytics_bar import render_analytics_bar
from components.dashboardcomponent import render_dashboard

API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Developer Support Assistant",
    page_icon="🤖",
    layout="wide"
)

# =====================================================
# SESSION STATE INIT — must be before any render
# =====================================================

if "show_dashboard"   not in st.session_state:
    st.session_state.show_dashboard   = False
if "messages"         not in st.session_state:
    st.session_state.messages         = []
if "agent_result"     not in st.session_state:
    st.session_state.agent_result     = None
if "model_name"       not in st.session_state:
    st.session_state.model_name       = "gpt-4o-mini"
if "query_running"    not in st.session_state:
    st.session_state.query_running    = False
if "pending_feedback" not in st.session_state:
    st.session_state.pending_feedback = None

# =====================================================
# SIDEBAR — rendered first so it always reflects
# the latest session_state values
# =====================================================

render_sidebar()

# =====================================================
# UPLOAD SECTION IN SIDEBAR
# =====================================================

with st.sidebar:

    st.header("📄 Upload Document")
    st.markdown("**Supported Formats:** CSV · PDF · Markdown")

    uploaded_file = st.file_uploader(
        "Choose Document", type=["csv", "pdf", "md"]
    )

    if uploaded_file:
        st.info(f"Selected: {uploaded_file.name}")

        if st.button("Upload & Index"):
            with st.spinner("Uploading and indexing..."):
                mime_type = (
                    mimetypes.guess_type(uploaded_file.name)[0]
                    or "application/octet-stream"
                )
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/upload",
                        files={"file": (uploaded_file.name, uploaded_file, mime_type)},
                        timeout=600,
                    )
                    result = response.json()

                    if response.status_code != 200:
                        st.error("Upload request failed.")
                    elif result.get("status") == "duplicate":
                        st.warning("Document already exists in the knowledge base.")
                    elif result.get("status") == "success":
                        st.success("Upload completed successfully.")
                        st.info(f"Type: {uploaded_file.name.split('.')[-1].upper()}")
                        c1, c2 = st.columns(2)
                        c1.metric("Documents", result.get("documents_processed", 0))
                        c2.metric("Chunks",    result.get("chunks_created", 0))
                    else:
                        st.error(result.get("error", "Upload failed."))

                except Exception as e:
                    st.error(f"Upload Error: {str(e)}")

    st.divider()
    st.markdown("""
**Stack**
- PostgreSQL + pgvector
- Hybrid Retrieval + Reranker
- GPT Generation
""")

# =====================================================
# PROCESS PENDING FEEDBACK
# Must run OUTSIDE chat_message/spinner contexts
# =====================================================

if st.session_state.pending_feedback:
    fb = st.session_state.pending_feedback
    try:
        resp = requests.post(
            f"{API_BASE_URL}/feedback",
            json={
                "query":    fb["query"],
                "answer":   fb["answer"],
                "agent":    fb["agent"],
                "feedback": fb["type"],
            },
            timeout=30,
        )
        if resp.status_code == 200:
            st.toast("Thank you for your feedback!", icon="✅")
        else:
            st.toast("Failed to save feedback.", icon="❌")
    except Exception as e:
        st.toast(f"Feedback error: {str(e)}", icon="❌")
    finally:
        st.session_state.pending_feedback = None

# =====================================================
# DASHBOARD / ASSISTANT TOGGLE
# =====================================================

st.title("🤖 Developer Support Assistant")

c1, c2 = st.columns(2)
with c1:
    if st.button("📊 Dashboard"):
        st.session_state.show_dashboard = True
with c2:
    if st.button("💬 Assistant"):
        st.session_state.show_dashboard = False

if st.session_state.show_dashboard:
    render_dashboard()
    st.stop()

st.markdown(
    "Upload CSV, PDF and Markdown documentation "
    "and ask questions using RAG + pgvector."
)

# =====================================================
# CHAT HISTORY DISPLAY
# =====================================================

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =====================================================
# CHAT INPUT
# =====================================================

query = st.chat_input("Ask a technical question...")

if query:

    # clear stale result so sidebar shows nothing while waiting
    st.session_state.agent_result = None
    st.session_state.query_running = True

    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Searching documentation..."):
            try:
                # exclude current user message from history
                # messages[-1] is the user turn we just appended
                history_to_send = [
                    m for m in st.session_state.messages[:-1]
                    if m["role"] in ("user", "assistant")
                ][-6:]   # last 6 turns = 3 exchanges

                response = requests.post(
                    f"{API_BASE_URL}/ask",
                    json={
                        "query":        query,
                        "chat_history": history_to_send,
                        "model_name":   st.session_state.model_name,
                    },
                    timeout=300,
                )

                result = response.json()

                # ── update sidebar ──────────────────
                st.session_state.agent_result  = result
                st.session_state.query_running = False

                # ── analytics ──────────────────────
                try:
                    kb = requests.get(f"{API_BASE_URL}/stats", timeout=10).json()
                except Exception:
                    kb = {}

                st.session_state["analytics"] = {
                    "total_documents":  kb.get("total_documents", 0),
                    "total_chunks":     kb.get("total_chunks", 0),
                    "total_domains":    kb.get("total_domains", 0),
                    "total_categories": kb.get("total_categories", 0),
                    "retrieved_chunks": result.get("retrieved_chunks", 0),
                    "reranked_chunks":  len(result.get("sources", [])),
                    "sources_used":     result.get("stats", {}).get("sources_used", 0),
                    "confidence":       result.get("confidence", 0),
                    "vector_time_ms":   result.get("stats", {}).get("retrieval_time_ms", 0),
                    "llm_time_ms":      result.get("stats", {}).get("llm_time_ms", 0),
                    "total_time_ms":    result.get("stats", {}).get("total_time_ms", 0),
                    "response_tokens":  len(result.get("answer", "").split()),
                }

                answer  = result.get("answer", "No answer returned.")
                sources = result.get("sources", [])

                if "analytics" in st.session_state:
                    render_analytics_bar(st.session_state["analytics"])

                if result.get("source_type") == "external":
                    st.warning("🌐 Answer from external documentation")

                st.markdown(answer)

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )

                if sources:
                    with st.expander("📚 Sources"):
                        for idx, src in enumerate(sources, 1):
                            st.markdown(f"**Source {idx}:** {src.get('title','N/A')}")
                            st.caption(f"Domain: {src.get('domain','N/A')} · {src.get('source_url','N/A')}")
                            score = src.get("rerank_score")
                            if score:
                                st.caption(f"Score: {round(score, 4)}")
                            st.divider()

            except Exception as e:
                st.session_state.query_running = False
                error_msg = f"Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append(
                    {"role": "assistant", "content": error_msg}
                )

# =====================================================
# FEEDBACK BUTTONS
# Outside spinner/chat_message — survives rerun
# =====================================================

if (
    st.session_state.agent_result
    and st.session_state.messages
    and st.session_state.messages[-1]["role"] == "assistant"
):
    last_answer = st.session_state.messages[-1]["content"]
    last_query  = next(
        (m["content"] for m in reversed(st.session_state.messages)
         if m["role"] == "user"),
        "",
    )
    agent = st.session_state.agent_result.get("agent", "Unknown")

    st.divider()
    st.markdown("### Was this answer helpful?")
    fkey = str(abs(hash(last_query)))

    c1, c2 = st.columns(2)
    with c1:
        if st.button("👍 Helpful", key=f"pos_{fkey}"):
            st.session_state.pending_feedback = {
                "query": last_query, "answer": last_answer,
                "agent": agent,      "type":   "positive",
            }
            st.rerun()
    with c2:
        if st.button("👎 Not Helpful", key=f"neg_{fkey}"):
            st.session_state.pending_feedback = {
                "query": last_query, "answer": last_answer,
                "agent": agent,      "type":   "negative",
            }
            st.rerun()