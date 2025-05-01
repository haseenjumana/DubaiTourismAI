import streamlit as st
import os
import sys

# Page config
st.set_page_config(
    page_title="About Dubai AI Assistant",
    page_icon="ℹ️",
    layout="wide",
    menu_items={}
)

# Hide hamburger menu and footer
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden !important;}
        footer {visibility: hidden !important;}
        header {visibility: hidden !important;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# About header
st.title("ℹ️ About Dubai Tourism & Business AI Assistant")
st.markdown("""
### Your intelligent guide to Dubai tourism and business opportunities
Learn about the technologies and features behind this AI assistant.
""")

# Project overview
st.header("🚀 Project Overview")
st.markdown("""
The Dubai Tourism & Business AI Assistant is a comprehensive multilingual platform designed to provide visitors and entrepreneurs with accurate, up-to-date information about Dubai. 

Whether you're planning a vacation, considering business opportunities, or seeking information about local customs and regulations, our assistant offers personalized responses to help you navigate Dubai with confidence.
""")

# Technologies used
st.header("💻 Technologies Used")

# Create columns for different technology categories
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Frontend")
    st.markdown("""
    - **Streamlit**: Python framework for creating interactive web applications
    - **HTML/CSS**: For styling and layout customization
    - **JavaScript**: Limited integration for enhanced interactivity
    """)

with col2:
    st.subheader("Backend")
    st.markdown("""
    - **Python**: Core programming language
    - **OpenAI API**: For natural language processing and response generation
    - **FAISS**: Vector database for semantic search
    - **NumPy**: Mathematical operations for embeddings
    - **Pandas**: Data manipulation and analysis
    """)

with col3:
    st.subheader("AI & NLP")
    st.markdown("""
    - **GPT-4o**: Latest language model for generating responses
    - **Embeddings API**: For semantic search and understanding
    - **ElevenLabs**: Text-to-speech for multiple languages
    - **Whisper**: Speech-to-text for voice input
    """)

# Features section
st.header("✨ Key Features")

features_tab1, features_tab2, features_tab3 = st.tabs(["Tourism Features", "Business Features", "Technical Features"])

with features_tab1:
    st.markdown("""
    ### Tourism Information
    - Detailed information on attractions, hotels, and activities
    - Cultural insights and local customs guidance
    - Transportation and navigation assistance
    - Seasonal event recommendations
    - Visa and travel requirement explanations
    - Personalized itinerary suggestions
    """)

with features_tab2:
    st.markdown("""
    ### Business Intelligence
    - Free zone comparison and selection guidance
    - Business setup process walkthrough
    - Licensing and permit information
    - Market trends and sector opportunities
    - Legal and regulatory compliance guidance
    - Networking and resource recommendations
    """)

with features_tab3:
    st.markdown("""
    ### Technical Capabilities
    - **Multilingual Support**: Seamless language detection and translation
    - **Voice Interface**: Speech input and natural voice responses
    - **Context-Aware Responses**: Understanding complex queries with context
    - **Semantic Search**: Finding relevant information beyond keyword matching
    - **Fallback Mechanisms**: Reliable responses even with API limitations
    - **Adaptive Learning**: Improving responses based on user interactions
    """)

# How it works section
st.header("⚙️ How It Works")

st.markdown("""
The Dubai Tourism & Business AI Assistant uses a sophisticated architecture to deliver accurate, helpful responses:

1. **Query Processing**: Your question is analyzed for language, intent, and key topics

2. **Knowledge Retrieval**: The system searches its knowledge base for relevant Dubai information

3. **Context Building**: Relevant facts and details are assembled into a comprehensive context

4. **Response Generation**: AI models generate a clear, concise answer based on the retrieved context

5. **Translation**: If needed, the response is translated back to your preferred language

6. **Voice Synthesis**: For audio responses, natural-sounding speech is generated in your language
""")

# Architecture diagram (simple text-based version)
st.subheader("System Architecture")
st.code("""
┌───────────────┐      ┌───────────────┐      ┌───────────────┐
│  User Input   │──────►  NLP Pipeline  ├──────►  Knowledge Base │
└───────────────┘      └───────┬───────┘      └───────┬───────┘
                              │                      │
                              ▼                      ▼
                       ┌───────────────┐      ┌───────────────┐
                       │  AI Processing │◄─────┤ Vector Search  │
                       └───────┬───────┘      └───────────────┘
                              │
                              ▼
                       ┌───────────────┐      ┌───────────────┐
                       │    Response    │─────►│  Translation   │
                       │   Generation   │      │     Layer      │
                       └───────┬───────┘      └───────┬───────┘
                              │                       │
                              ▼                       ▼
                       ┌───────────────────────────────────────┐
                       │            User Interface              │
                       └───────────────────────────────────────┘
""", language="")

# Data sources and acknowledgments
st.header("📚 Data Sources & Acknowledgments")

st.markdown("""
### Official Sources
- Dubai Department of Tourism and Commerce Marketing (DTCM)
- Dubai Department of Economic Development (DED)
- General Directorate of Residency and Foreigners Affairs (GDRFA)
- Dubai Free Zone Council
- Dubai Municipality

### Technology Partners
- OpenAI for language processing technology
- ElevenLabs for multilingual voice synthesis
- Streamlit for the web application framework

### Acknowledgments
This project was developed as an educational demonstration of how AI can enhance tourism and business information services. The goal is to showcase the potential of AI assistants in providing valuable, accurate information while respecting user privacy and data security.
""")

# Future roadmap
st.header("🔮 Future Development Roadmap")

st.markdown("""
### Upcoming Features

- **Dubai Now API Integration**: Real-time visa status checking and government service information
- **Personalized Recommendations**: Tailored suggestions based on user preferences and history
- **Analytics Dashboard**: Insights into popular queries and user satisfaction metrics
- **Mobile App Version**: Native applications for iOS and Android platforms
- **Extended Language Support**: Additional languages including Chinese, Russian, and German
- **AR Integration**: Augmented reality features for landmark identification and navigation
""")

# Contact information (placeholder)
st.header("📮 Contact & Feedback")

st.markdown("""
### We'd love to hear from you!

This project is continually improving based on user feedback. If you have suggestions, questions, or comments about the Dubai Tourism & Business AI Assistant, please reach out to us:

- **Email**: contact@dubaiaiassistant.ae
- **Phone**: +971 4 XXX XXXX
- **Social Media**: @DubaiAIAssistant
""")

# Feedback form
with st.form("feedback_form"):
    st.subheader("Feedback Form")
    name = st.text_input("Name")
    email = st.text_input("Email")
    feedback_type = st.selectbox(
        "Type of Feedback",
        ["General Feedback", "Bug Report", "Feature Request", "Content Suggestion", "Other"]
    )
    feedback = st.text_area("Your Feedback")
    submit_button = st.form_submit_button("Submit Feedback")

# Display confirmation message if form is submitted
if submit_button:
    st.success("Thank you for your feedback! We appreciate your input and will use it to improve our service.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>© 2024 Dubai Tourism & Business AI Assistant</p>
    </div>
    """, 
    unsafe_allow_html=True
)