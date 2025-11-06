import streamlit as st
import time

# Page configuration
st.set_page_config(
    page_title="Flowscribe - Workflow Assistant",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("📋 Flowscribe")
st.markdown(
    """
    <div style='background-color: #000; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
        <h3 style='margin-top: 0;'>👋 Hello! I'm Flowscribe, your intelligent workflow assistant.</h3>
        <p style='margin-bottom: 0;'>
            I'm here to help you understand, optimize, and navigate your workflows with ease. 
            Ask me anything about your processes, documentation, or workflow structures, and I'll 
            provide insights. Let's streamline your work together!
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar
with st.sidebar:
    st.header("🎯 Workflow Capture")
    st.markdown(
        """
        Flowscribe automatically navigates apps and captures 
        UI states to document workflows in real-time.
        
        **Supported Apps:**
        - Linear
        - Notion
        - Asana
        - [More coming soon]
        """
    )

    st.divider()
    
    st.subheader("💭 Example Tasks")
    st.markdown(
        """
        - "How do I create a project in Linear?"
        - "How do I filter a database in Notion?"
        - "How do I assign a task in Asana?"
        - "How do I change settings in Linear?"
        """
    )
    
    st.divider()

    
    
    st.subheader("📊 Capture Stats")
    st.metric("Workflows Captured", st.session_state.get("query_count", 0))
    
    st.divider()
    
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.query_count = 0
        st.rerun()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "query_count" not in st.session_state:
    st.session_state.query_count = 0
if "screenshot_count" not in st.session_state:
    st.session_state.screenshot_count = 0

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Display workflow steps if available
        if "workflow_steps" in message and message["workflow_steps"]:
            st.markdown("---")
            st.markdown("### 📸 Captured Workflow Steps")
            for i, step in enumerate(message["workflow_steps"], 1):
                with st.expander(f"Step {i}: {step['title']}", expanded=(i==1)):
                    st.markdown(f"**Action:** {step['action']}")
                    st.markdown(f"**UI State:** {step['state']}")
                    # Placeholder for screenshot
                    st.info(f"🖼️ Screenshot: {step['screenshot']}")

# Chat input
if prompt := st.chat_input("What workflow would you like me to capture? (e.g., 'How do I create a project in Linear?')"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.query_count += 1
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response with workflow capture process
    with st.chat_message("assistant"):
        # Show simple status indicator
        with st.status("🤖 Generating workflow instructions...", expanded=False) as status:
            time.sleep(3)  # Placeholder for backend call
            status.update(label="✅ Complete!", state="complete", expanded=False)
        
        # Increment screenshot count
        num_screenshots = 5  # Placeholder
        st.session_state.screenshot_count += num_screenshots
        
        # Generate response
        response = f"""
I've successfully captured the workflow for: **"{prompt}"**

Here's what I documented:

**Application:** Linear (detected automatically)  
**Task Type:** Project Creation  
**Total Steps:** 5  
**Screenshots Captured:** {num_screenshots}

The workflow has been broken down into clear, sequential steps with screenshots of each UI state. 
You can review each step below to see exactly how to perform this task.

*Note: This is a placeholder response. The actual backend will integrate with browser automation 
to capture real workflows in real-time.*
        """
        st.markdown(response)
        
        # Placeholder workflow steps
        workflow_steps = [
            {
                "title": "Navigate to Projects",
                "action": "Click on 'Projects' in the sidebar",
                "state": "Projects list view",
                "screenshot": "screenshot_001_projects_list.png"
            },
            {
                "title": "Open Create Dialog",
                "action": "Click 'Create Project' button",
                "state": "Create project modal opened",
                "screenshot": "screenshot_002_create_modal.png"
            },
            {
                "title": "Enter Project Details",
                "action": "Fill in project name and description",
                "state": "Form fields populated",
                "screenshot": "screenshot_003_filled_form.png"
            },
            {
                "title": "Configure Settings",
                "action": "Select team and set project status",
                "state": "Project settings configured",
                "screenshot": "screenshot_004_settings.png"
            },
            {
                "title": "Create Project",
                "action": "Click 'Create' button",
                "state": "Project created successfully",
                "screenshot": "screenshot_005_success.png"
            }
        ]
        
        st.markdown("---")
        st.markdown("### 📸 Captured Workflow Steps")
        for i, step in enumerate(workflow_steps, 1):
            with st.expander(f"Step {i}: {step['title']}", expanded=(i==1)):
                st.markdown(f"**Action:** {step['action']}")
                st.markdown(f"**UI State:** {step['state']}")
                # Placeholder for screenshot
                st.info(f"🖼️ Screenshot: {step['screenshot']}")
    
    # Add assistant response to chat history
    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "workflow_steps": workflow_steps
    })
    
    # Force rerun to update sidebar stats
    st.rerun()

# Footer
st.divider()
st.markdown(
    """
    <div style='text-align: center; color: gray; padding: 10px;'>
        <small>Flowscribe v1.0 | AI-Powered Workflow Documentation</small>
    </div>
    """,
    unsafe_allow_html=True
)