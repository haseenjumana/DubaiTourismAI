import os
import streamlit as st
import tempfile
import time
import base64
import json
import sys
from dotenv import load_dotenv

# Load environment variables from .env file (if it exists)
load_dotenv()

from utils.language_utils import translate_text, detect_language, supported_languages
from utils.audio_utils import text_to_speech, speech_to_text
from utils.vector_store import initialize_vector_store, get_dubai_info
from utils.model_utils import get_ai_response

# Set page configuration
st.set_page_config(
    page_title="Dubai Tourism & Business AI Assistant",
    page_icon="🏙️",
    layout="wide",
    menu_items={}
)

# Hide hamburger menu and footer
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# Initialize session state variables
if 'language' not in st.session_state:
    st.session_state.language = "English"
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = initialize_vector_store()
if 'audio_recording' not in st.session_state:
    st.session_state.audio_recording = False
if 'speech_success' not in st.session_state:
    st.session_state.speech_success = False
if 'user_query' not in st.session_state:
    st.session_state.user_query = ""

# Display logo and title
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown(
        """
        <div style="text-align: center">
            <svg width="150" height="150" xmlns="http://www.w3.org/2000/svg">
                <rect width="150" height="150" fill="white"/>
                <text x="75" y="75" font-family="Arial" font-size="16" text-anchor="middle" alignment-baseline="middle" fill="#e60000">
                    Dubai Tourism
                </text>
                <text x="75" y="95" font-family="Arial" font-size="14" text-anchor="middle" alignment-baseline="middle" fill="#00274e">
                    AI Assistant
                </text>
            </svg>
            <h1 style="font-size: 2.5em; margin-top: 0;">Dubai Tourism & Business AI Assistant</h1>
        </div>
        """, 
        unsafe_allow_html=True
    )

# Navigation menu
st.markdown(
    """
    <div style="display: flex; justify-content: center; gap: 20px; margin-bottom: 20px;">
        <a href="/" target="_self" style="text-decoration: none; color: #e60000; font-weight: bold; padding: 5px 10px; border-bottom: 2px solid #e60000;">AI Chat</a>
        <a href="/Business" target="_self" style="text-decoration: none; color: #333; padding: 5px 10px;">Business</a>
        <a href="/Tourism" target="_self" style="text-decoration: none; color: #333; padding: 5px 10px;">Tourism</a>
        <a href="/About" target="_self" style="text-decoration: none; color: #333; padding: 5px 10px;">About</a>
    </div>
    """,
    unsafe_allow_html=True
)

# Language selector
st.sidebar.title("Settings")
selected_language = st.sidebar.selectbox(
    "Choose your language",
    list(supported_languages.keys()),
    index=list(supported_languages.keys()).index(st.session_state.language)
)

if selected_language != st.session_state.language:
    st.session_state.language = selected_language

# Display page content based on selected language
if st.session_state.language == "English":
    page_description = "Ask me anything about tourism, business, or government services in Dubai."
    voice_input_text = "Voice Input"
    text_input_placeholder = "Type your question here..."
    submit_button_text = "Ask"
    clear_chat_text = "Clear Chat"
    audio_response_text = "Get audio response"
elif st.session_state.language == "Arabic":
    page_description = "اسألني أي شيء عن السياحة أو الأعمال أو الخدمات الحكومية في دبي."
    voice_input_text = "إدخال صوتي"
    text_input_placeholder = "اكتب سؤالك هنا..."
    submit_button_text = "اسأل"
    clear_chat_text = "مسح المحادثة"
    audio_response_text = "الحصول على رد صوتي"
elif st.session_state.language == "Hindi":
    page_description = "दुबई में पर्यटन, व्यापार, या सरकारी सेवाओं के बारे में मुझसे कुछ भी पूछें।"
    voice_input_text = "आवाज़ इनपुट"
    text_input_placeholder = "अपना प्रश्न यहां टाइप करें..."
    submit_button_text = "पूछें"
    clear_chat_text = "चैट साफ़ करें"
    audio_response_text = "ऑडियो प्रतिक्रिया प्राप्त करें"

st.markdown(f"### {page_description}")

# Display chat history
chat_container = st.container()
with chat_container:
    for i, message in enumerate(st.session_state.chat_history):
        if message["role"] == "user":
            st.markdown(f"<div style='background-color: #e1f5fe; padding: 10px; border-radius: 5px; margin-bottom: 10px;'><strong>You:</strong> {message['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='background-color: #f0f0f0; padding: 10px; border-radius: 5px; margin-bottom: 10px;'><strong>AI:</strong> {message['content']}</div>", unsafe_allow_html=True)

# User input options
input_col1, input_col2 = st.columns([5, 1])

# Initialize the submitted flag if it doesn't exist
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# Function to reset the form
def reset_form():
    st.session_state.submitted = False

with input_col1:
    # Use a unique key for each session to avoid the widget value persistence issue
    if st.session_state.submitted:
        # If just submitted, create a fresh text input with empty value
        user_input = st.text_input(
            label="", 
            placeholder=text_input_placeholder, 
            key=f"text_input_{len(st.session_state.chat_history)}"
        )
        # Reset the submitted flag
        st.session_state.submitted = False
    else:
        # Normal case
        user_input = st.text_input(
            label="", 
            placeholder=text_input_placeholder, 
            key=f"text_input_{len(st.session_state.chat_history)}"
        )

with input_col2:
    voice_button = st.button(voice_input_text)

# Audio recording functionality
if 'audio_recording' not in st.session_state:
    st.session_state.audio_recording = False

if 'transcript' not in st.session_state:
    st.session_state.transcript = ""
    
# Function to handle microphone recording
def start_recording():
    st.session_state.audio_recording = True
    # Reset any previous transcript
    st.session_state.transcript = ""
    st.session_state.speech_success = False
    
def stop_recording():
    st.session_state.audio_recording = False
    
    # Check if we're in demo mode or using real API
    use_demo_mode = True
    
    if use_demo_mode:
        # DEMO MODE: Use predefined examples instead of actual voice recognition
        # Simulate API call delay
        with st.spinner("Processing your voice (DEMO MODE)..."):
            time.sleep(1)  # Simulate processing time
            
            # For demo purposes, provide sample queries based on selected language
            sample_queries = {
                "English": [
                    "What are the top attractions in Dubai?", 
                    "How do I start a business in Dubai?",
                    "Tell me about Dubai's Free Zones",
                    "What's the best time to visit Dubai?"
                ],
                "Arabic": [
                    "ما هي أفضل المعالم السياحية في دبي؟",
                    "كيف يمكنني بدء عمل تجاري في دبي؟",
                    "أخبرني عن المناطق الحرة في دبي",
                    "ما هو أفضل وقت لزيارة دبي؟"
                ],
                "Hindi": [
                    "दुबई में सबसे अच्छे पर्यटन स्थल कौन से हैं?",
                    "मैं दुबई में व्यापार कैसे शुरू करूं?",
                    "दुबई के फ्री ज़ोन के बारे में बताएं",
                    "दुबई घूमने का सबसे अच्छा समय कौन सा है?"
                ]
            }
            
            language = st.session_state.language
            import random
            query = random.choice(sample_queries.get(language, sample_queries["English"]))
    else:
        # REAL MODE: Use actual speech recognition API
        # This would be implemented in a production version with actual audio recording
        with st.spinner("Processing your voice..."):
            # Create a temp audio file (placeholder)
            temp_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            temp_audio_file.close()
            
            try:
                # Call the actual speech-to-text function
                query = speech_to_text(temp_audio_file.name, st.session_state.language)
                
                # Handle failed speech recognition
                if not query:
                    st.error("Sorry, I couldn't understand the audio. Please try again or type your question.")
                    st.session_state.speech_success = False
                    return
                    
            except Exception as e:
                st.error(f"Speech recognition error: {str(e)}")
                st.session_state.speech_success = False
                return
            
            finally:
                # Clean up the temporary file
                if os.path.exists(temp_audio_file.name):
                    os.unlink(temp_audio_file.name)
    
    # Store the transcript in session state
    st.session_state.transcript = query
    st.session_state.user_query = query
    
    # Set success flag
    st.session_state.speech_success = True

# Handle voice button
if voice_button and not st.session_state.audio_recording:
    # Start recording
    start_recording()
    st.session_state.transcript = ""
    st.rerun()

# Display recording interface if currently recording
if st.session_state.audio_recording:
    # Show recording interface
    with st.container():
        st.warning(f"🎤 DEMO MODE: Voice recording simulation (Press Stop to get a sample question)")
        # Display animated microphone icon (simulated)
        cols = st.columns([3, 1, 3])
        with cols[1]:
            st.markdown("""
            <div style='text-align: center; animation: pulse 1.5s infinite;'>🎤</div>
            <style>
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.2); }
                100% { transform: scale(1); }
            }
            </style>
            """, unsafe_allow_html=True)
        
        # Add a note about the demo functionality    
        st.caption("Note: This is a simulation. When you press 'Stop', you'll receive a random predefined question in your selected language.")
        
        stop_col1, stop_col2, stop_col3 = st.columns([3, 1, 3])
        with stop_col2:
            if st.button("Stop Recording"):
                stop_recording()
                st.rerun()

# Display success message if speech was recognized
if st.session_state.speech_success:
    st.success(f"Recognized input: {st.session_state.transcript}")
    st.session_state.speech_success = False

# Update the input field with the transcript if we have one
if st.session_state.transcript and not user_input:
    user_input = st.session_state.transcript

# Submit button
submit_col1, submit_col2 = st.columns([4, 1])
with submit_col2:
    submit_button = st.button(submit_button_text)

# Process user input
if submit_button and user_input:
    # Add user message to chat history in the selected language
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # Detect language and translate to English if needed
    try:
        detected_lang = detect_language(user_input)
        english_query = user_input
        if detected_lang != "English":
            english_query = translate_text(user_input, detected_lang, "English")
    except Exception as e:
        error_message = str(e)
        print(f"Language detection error: {error_message}")
        
        # Display a user-friendly warning about API limitations
        if "quota" in error_message.lower() or "exceeded" in error_message.lower():
            st.warning("Language detection is currently unavailable due to API quota limitations. Using selected language setting instead.")
        
        # If language detection fails, use the language selected in the UI
        english_query = user_input
        if st.session_state.language != "English":
            # If user has selected a non-English language but we can't detect/translate,
            # let them know we're processing in the selected language
            st.info(f"Processing your query in {st.session_state.language}. Translation capabilities are limited in demo mode.")
    
    # Get Dubai-specific context from vector store
    context = get_dubai_info(english_query, st.session_state.vector_store)
    
    # Get AI response
    with st.spinner("Thinking..."):
        try:
            ai_response_english = get_ai_response(english_query, context)
        except Exception as e:
            error_message = str(e)
            print(f"Error getting AI response: {error_message}")
            
            # Check if this is a quota exceeded error
            if "quota" in error_message.lower() or "exceeded" in error_message.lower():
                ai_response_english = ("I'm sorry, but it appears the API quota has been exceeded. " 
                                     "This is a demonstration version with limited API calls. " 
                                     "Please try typing simpler queries or try again later when the quota refreshes.")
            else:
                # Generic fallback response for other errors
                ai_response_english = "I'm sorry, I'm having trouble processing your request right now. Please try again later."
    
    # Translate response back to user's language if needed
    ai_response = ai_response_english
    if st.session_state.language != "English":
        try:
            ai_response = translate_text(ai_response_english, "English", st.session_state.language)
        except Exception as e:
            # If translation fails, use English response
            print(f"Translation error: {e}")
            ai_response = ai_response_english
    
    # Add AI response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
    
    # We'll use a flag to clear the input instead of modifying session_state directly
    # Create a key in session state to rerun app
    st.session_state.submitted = True
    
    # Rerun the app to update the UI
    st.rerun()

# Audio response toggle
audio_response = st.sidebar.checkbox(audio_response_text)

# If audio response is enabled and there's chat history
if audio_response and st.session_state.chat_history:
    last_response = st.session_state.chat_history[-1]
    if last_response["role"] == "assistant":
        try:
            with st.sidebar:
                audio_data = text_to_speech(last_response["content"], st.session_state.language)
                if audio_data:
                    st.audio(audio_data, format="audio/mp3")
                else:
                    st.warning("Audio generation temporarily unavailable.")
        except Exception as e:
            print(f"Error in text-to-speech conversion: {e}")
            with st.sidebar:
                st.warning("Audio generation temporarily unavailable due to API limitations.")

# Clear chat button
if st.sidebar.button(clear_chat_text):
    st.session_state.chat_history = []
    st.rerun()

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

