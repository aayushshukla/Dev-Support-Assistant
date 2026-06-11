import streamlit as st
import streamlit.components.v1 as components
from backend.api_client import generate_code
from components.sidebar import render_sidebar
from components.agent_panel import render_agent_panel

# ==========================================
# Load CSS
# ==========================================

with open("assets/styles.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# ==========================================
# Load JavaScript
# ==========================================

with open("assets/scripts.js") as f:
    js_code = f.read()

components.html(
    f"""
    <script>
    {js_code}
    </script>
    """,
    height=0
)

# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title="Developer Assistant",
    page_icon="🤖",
    layout="wide"
)

# ==========================================
# Header
# ==========================================
st.markdown("""
<div class="header-container">
    <h1>🤖 Developer Assistant</h1>
    <p>
        AI-Powered Multi-Agent Software Engineering Platform
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# Sidebar
# ==========================================

selected_agents, project_type = render_sidebar()

# ==========================================
# Main Layout
# ==========================================

col1, col2 = st.columns([3, 1])

with col1:

    st.subheader("Requirement Input")

    user_prompt = st.text_area(
        "Describe your requirement",
        height=200,
        placeholder="Create a FastAPI application with PostgreSQL support..."
    )

    if st.button("🚀 Run Agents", use_container_width=True):

         

        result = generate_code(
            user_prompt
        )

        st.code(
            result["generated_code"]
        )
        # TODO:
        # Replace this block with FastAPI backend call.
        #
        # Example:
        # workflow = start_workflow(
        #     prompt=user_prompt,
        #     agents=selected_agents,
        #     project_type=project_type
        # )

        st.success("Workflow Started Successfully")

        for agent in selected_agents:
            render_agent_panel(agent)

with col2:

    st.subheader("System Status")

    st.metric("Agents Active", len(selected_agents))

    st.metric(
        "Project Type",
        project_type
    )

    st.progress(75)

    st.info("""
Workflow Steps

1. Requirements Analysis
2. Design
3. Code Generation
4. Testing
5. Documentation
""")

st.divider()

st.subheader("Architecture")

