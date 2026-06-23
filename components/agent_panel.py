
import streamlit as st


def render_agent_panel(agent_name):
    """
    Render output for a selected agent.

    TODO:
    Replace all mock data with backend API responses.
    Example:
        agent_response = workflow_results[agent_name]
    """

    with st.expander(f"⚙️ {agent_name}", expanded=True):

        # =====================================================
        # REQUIREMENTS ANALYST
        # =====================================================

        if agent_name == "Requirements Analyst":

            st.markdown("""
            <div class="agent-card">
                <h4>📋 Requirements Agent</h4>
                <p>Generated functional requirements successfully.</p>
                <p>Generated non-functional requirements successfully.</p>
                <p>Created user stories.</p>
            </div>
            """,
            unsafe_allow_html=True)

            st.markdown("### Functional Requirements")

            st.markdown("""
            - User Authentication
            - Employee CRUD Operations
            - Role Based Access Control
            - Search and Filtering
            """)

            st.markdown("### Non-Functional Requirements")

            st.markdown("""
            - Secure APIs
            - High Availability
            - Scalability
            - Audit Logging
            """)

        # =====================================================
        # CODE GENERATOR
        # =====================================================

        elif agent_name == "Code Generator":

            st.markdown("""
            <div class="agent-card">
                <h4>💻 Code Generator</h4>
                <p>Generated FastAPI boilerplate successfully.</p>
            </div>
            """,
            unsafe_allow_html=True)

            st.code(
                """
from fastapi import FastAPI

app = FastAPI()

@app.get("/employees")
def get_employees():
    return {
        "message": "Employee List"
    }
                """,
                language="python"
            )

            # TODO:
            # Replace with generated code from backend

        # =====================================================
        # DOCUMENTATION AGENT
        # =====================================================

        elif agent_name == "Documentation Agent":

            st.markdown("""
            <div class="agent-card">
                <h4>📚 Documentation Agent</h4>
                <p>Generated API documentation.</p>
            </div>
            """,
            unsafe_allow_html=True)

            st.markdown("""
            ### API Endpoints

            | Method | Endpoint |
            |----------|----------|
            | GET | /employees |
            | POST | /employees |
            | PUT | /employees/{id} |
            | DELETE | /employees/{id} |
            """)

            # TODO:
            # Render markdown documentation returned by backend

        # =====================================================
        # TESTING AGENT
        # =====================================================

        elif agent_name == "Testing Agent":

            st.markdown("""
            <div class="agent-card">
                <h4>🧪 Testing Agent</h4>
                <p>Generated unit test cases.</p>
            </div>
            """,
            unsafe_allow_html=True)

            st.code(
                """
def test_get_employees():

    response = client.get(
        "/employees"
    )

    assert response.status_code == 200
                """,
                language="python"
            )

            # TODO:
            # Render generated tests from backend

        # =====================================================
        # CODE REVIEWER
        # =====================================================

        elif agent_name == "Code Reviewer":

            st.markdown("""
            <div class="agent-card">
                <h4>🔍 Code Reviewer</h4>
                <p>Code review completed successfully.</p>
            </div>
            """,
            unsafe_allow_html=True)

            st.success("REST standards followed")

            st.warning(
                "Add exception handling "
                "for database operations"
            )

            st.warning(
                "Add logging for API requests"
            )

            st.warning(
                "Implement retry mechanism"
            )

            # TODO:
            # Display actual review comments

        # =====================================================
        # DEFAULT AGENT
        # =====================================================

        else:

            st.markdown("""
            <div class="agent-card">
                <h4>🤖 Agent</h4>
                <p>No output available.</p>
            </div>
            """,
            unsafe_allow_html=True)

        # =====================================================
        # FOOTER
        # =====================================================

        st.divider()

        st.caption(
            f"Status: Completed | Agent: {agent_name}"
        )

        # TODO:
        # Replace with actual status:
        # Running / Completed / Failed
