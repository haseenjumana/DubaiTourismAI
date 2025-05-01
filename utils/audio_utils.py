import os
import tempfile
import base64
import streamlit as st

# Handle potential import errors gracefully
try:
    import requests
except ImportError:
    st.error("requests package not installed. Run: pip install requests")
    requests = None

try:
    from openai import OpenAI
    # Initialize OpenAI client
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    if OPENAI_API_KEY:
        client = OpenAI(api_key=OPENAI_API_KEY)
    else:
        st.warning("OPENAI_API_KEY not found in environment variables. Audio features may not work properly.")
        client = None
except ImportError:
    st.error("openai package not installed. Run: pip install openai")
    client = None

# Get ElevenLabs API key
ELEVEN_LABS_API_KEY = os.environ.get("ELEVEN_LABS_API_KEY", "")
if not ELEVEN_LABS_API_KEY:
    st.warning("ELEVEN_LABS_API_KEY not found in environment variables. Voice synthesis will fall back to OpenAI TTS if available.")

# Voice IDs for different languages
VOICE_IDS = {
    "English": "21m00Tcm4TlvDq8ikWAM",  # Rachel voice
    "Arabic": "AZnzlk1XvdvUeBnXmlld",   # Adia voice
    "Hindi": "IKne3meq5aSn9XLyUdCD"     # Anand voice
}

def speech_to_text(audio_file_path, language="English"):
    """
    Convert speech to text using OpenAI's Whisper model
    """
    try:
        with open(audio_file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return transcript.text
    except Exception as e:
        print(f"Error in speech-to-text conversion: {e}")
        return None

def text_to_speech(text, language="English"):
    """
    Convert text to speech using ElevenLabs API
    Returns audio file path or None if conversion fails
    """
    try:
        # Limit text length to avoid API errors
        if len(text) > 1000:
            text = text[:997] + "..."
            
        # Try ElevenLabs first if API key is available
        if ELEVEN_LABS_API_KEY:
            try:
                voice_id = VOICE_IDS.get(language, VOICE_IDS["English"])
                
                url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
                
                headers = {
                    "Accept": "audio/mpeg",
                    "Content-Type": "application/json",
                    "xi-api-key": ELEVEN_LABS_API_KEY
                }
                
                data = {
                    "text": text,
                    "model_id": "eleven_multilingual_v2",
                    "voice_settings": {
                        "stability": 0.5,
                        "similarity_boost": 0.5
                    }
                }
                
                response = requests.post(url, json=data, headers=headers)
                
                if response.status_code == 200:
                    # Create a temp file to store the audio
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
                        temp_file.write(response.content)
                        temp_file_path = temp_file.name
                    
                    # Return the path to the temp file
                    return temp_file_path
                else:
                    print(f"ElevenLabs API error: {response.status_code} - {response.text}")
                    # Continue to OpenAI fallback
            except Exception as e:
                print(f"Error with ElevenLabs API: {e}")
                # Continue to OpenAI fallback
        
        # Fallback to OpenAI TTS
        try:
            # Shorter excerpt for OpenAI TTS due to potential quota issues
            short_text = text[:500] if len(text) > 500 else text
            
            tts_response = client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=short_text
            )
            
            # Create a temp file to store the audio
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
                temp_file.write(tts_response.content)
                temp_file_path = temp_file.name
            
            return temp_file_path
            
        except Exception as e:
            print(f"Error with OpenAI TTS API: {e}")
            # If we get here, both TTS services failed
            return None
    
    except Exception as e:
        print(f"Error in text-to-speech conversion: {e}")
        return None

