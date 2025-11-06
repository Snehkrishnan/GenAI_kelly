import streamlit as st
import google.generativeai as genai

# Page configuration
st.set_page_config(
    page_title="Kelly - AI Scientist Poet",
    page_icon="🎭",
    layout="centered"
)

# Title and description
st.title("🎭 Kelly - The AI Scientist Poet")
st.markdown("*Ask any question and receive skeptical, analytical poetry*")

# Configure Gemini API
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Define Kelly's personality
kelly_personality = """You are Kelly, an AI scientist and a great poet. You MUST respond to EVERY question 
exclusively in the form of a poem. Your poetic responses must embody these traits:

1. SKEPTICAL: Question broad claims, ask for evidence, highlight uncertainties
2. ANALYTICAL: Break down complex ideas, examine assumptions, use logical reasoning
3. PROFESSIONAL: Maintain academic rigor, cite limitations, avoid hype

Poetic Style Guidelines:
- Use varied poetic structures (rhyming couplets, free verse, haiku sequences)
- Incorporate scientific metaphors and technical terminology naturally
- Balance skepticism with constructive suggestions
- End with practical, evidence-based recommendations
- Keep poems between 8-20 lines for clarity

Remember: NEVER respond in prose. Every answer must be a complete poem."""

# Initialize chat session in session state
if "chat_session" not in st.session_state:
    model = genai.GenerativeModel(
        model_name='gemini-2.5-flash',  # Updated to Gemini 2.5!
        system_instruction=kelly_personality
    )
    st.session_state.chat_session = model.start_chat(history=[])

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask Kelly a question..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get Kelly's response
    with st.chat_message("assistant"):
        with st.spinner("Kelly is composing a poem..."):
            response = st.session_state.chat_session.send_message(prompt)
            st.markdown(response.text)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response.text})

# Sidebar with info
with st.sidebar:
    st.header("About Kelly")
    st.write("""
    Kelly is an AI scientist who communicates exclusively through poetry.
    
    Powered by **Gemini 2.5 Flash** ⚡
    
    Her responses are:
    - 🔍 **Skeptical**: Questions broad claims
    - 🧪 **Analytical**: Breaks down complex ideas
    - 📊 **Professional**: Evidence-based and rigorous
    """)
    
    st.markdown("---")
    
    st.subheader("Example Questions")
    st.write("""
    - Will AI replace all jobs?
    - Can we trust medical AI systems?
    - Is deep learning the solution to everything?
    - What are the limitations of large language models?
    """)
    
    st.markdown("---")
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        model = genai.GenerativeModel(
            model_name='gemini-2.5-flash',  # Updated here too!
            system_instruction=kelly_personality
        )
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()
