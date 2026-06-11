import streamlit as st


def render_sidebar():

    st.sidebar.header("Agent Selection")

    selected_agents = st.sidebar.multiselect(
        "Choose Agents",
        [
            "Requirements Analyst",
            "Code Generator",
            "Documentation Agent",
            "Testing Agent",
            "Code Reviewer"
        ],
        default=[
            "Requirements Analyst",
            "Code Generator"
        ]
    )

    project_type = st.sidebar.selectbox(
        "Project Type",
        [
            "Web Application",
            "REST API",
            "Microservice",
            "Data Pipeline",
            "GenAI Application"
        ]
    )

    return selected_agents, project_type