import os
import streamlit as st
import vertexai
from vertexai import agent_engines
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Agent Chat UI",
    page_icon="💬",
    layout="wide",
)

# Initialize Vertex AI
def init_vertex_ai():
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION")
    bucket = os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET")

    if not project_id or not location or not bucket:
        st.error("Missing required environment variables. Please set GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION, and GOOGLE_CLOUD_STORAGE_BUCKET.")
        st.stop()

    vertexai.init(
        project=project_id,
        location=location,
        staging_bucket=f"gs://{bucket}",
    )
    return project_id, location, bucket

# Initialize session state
def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "session_id" not in st.session_state:
        st.session_state.session_id = None
    if "agent" not in st.session_state:
        st.session_state.agent = None
    if "user_id" not in st.session_state:
        st.session_state.user_id = "streamlit_user"

# Create a new session with the agent
def create_session(agent_name):
    try:
        # Get the remote agent
        remote_agent = agent_engines.get(agent_name)

        # Create a session with initial state
        initial_state = {"user_preference_temperature_unit": "Celsius"}
        session = remote_agent.create_session(
            user_id=st.session_state.user_id,
            state=initial_state
        )

        st.session_state.session_id = session["id"]
        st.session_state.agent = remote_agent
        return True
    except Exception as e:
        st.error(f"Error creating session: {e}")
        return False

# Send a message to the agent and get the response
def send_message(message):
    if not st.session_state.agent or not st.session_state.session_id:
        st.error("No active session. Please enter an agent name and create a session first.")
        return

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": message})

    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(message)

    # Display a placeholder for the agent's response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")

        full_response = ""

        # Stream the response
        try:
            for event in st.session_state.agent.stream_query(
                user_id=st.session_state.user_id,
                session_id=st.session_state.session_id,
                message=message,
            ):
                # Process the event to extract text content
                if isinstance(event, dict):
                    content = event.get("content")
                    if isinstance(content, dict):
                        parts = content.get("parts")
                        if isinstance(parts, list):
                            for part_item in parts:
                                if isinstance(part_item, dict):
                                    text_content = part_item.get("text")
                                    if isinstance(text_content, str) and text_content:
                                        full_response += text_content
                                        message_placeholder.markdown(full_response + "▌")
                elif hasattr(event, "text") and event.text:
                    full_response += event.text
                    message_placeholder.markdown(full_response + "▌")
                elif hasattr(event, "content") and event.content and hasattr(event.content, "parts") and event.content.parts:
                    for part_item_obj in event.content.parts:
                        if hasattr(part_item_obj, "text") and part_item_obj.text:
                            full_response += part_item_obj.text
                            message_placeholder.markdown(full_response + "▌")

            # Update the placeholder with the full response
            message_placeholder.markdown(full_response)

            # Add the assistant's response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            message_placeholder.markdown(f"Error: {e}")
            st.session_state.messages.append({"role": "assistant", "content": f"Error: {e}"})

# Main app
def main():
    # Initialize Vertex AI
    project_id, location, bucket = init_vertex_ai()

    # Initialize session state
    init_session_state()

    # App title
    st.title("Agent Chat UI")

    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")

        # Agent name input
        agent_name = st.text_input("Agent Resource Name", 
                                  help="Enter the full resource name of your deployed agent")

        # Create session button
        if st.button("Create New Session"):
            if agent_name:
                with st.spinner("Creating session..."):
                    if create_session(agent_name):
                        st.success("Session created successfully!")
                        st.session_state.messages = []
            else:
                st.error("Please enter an agent name")

        # Environment info
        st.subheader("Environment")
        st.write(f"Project ID: {project_id}")
        st.write(f"Location: {location}")
        st.write(f"Bucket: {bucket}")

        if st.session_state.session_id:
            st.write(f"Session ID: {st.session_state.session_id}")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        if not st.session_state.session_id:
            st.error("Please create a session first")
        else:
            send_message(prompt)

if __name__ == "__main__":
    main()
