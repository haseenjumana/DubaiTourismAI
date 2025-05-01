import os
import streamlit as st

# Define supported languages and their codes - defined before imports to avoid dependency issues
supported_languages = {
    "English": "en",
    "Arabic": "ar",
    "Hindi": "hi"
}

# Handle potential import errors gracefully
try:
    from openai import OpenAI
    # Initialize OpenAI client
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    if OPENAI_API_KEY:
        client = OpenAI(api_key=OPENAI_API_KEY)
    else:
        st.warning("OPENAI_API_KEY not found in environment variables. Language detection may not work properly.")
        client = None
except ImportError:
    st.error("openai package not installed. Run: pip install openai")
    client = None

# Note: supported_languages already defined above

def detect_language(text):
    """
    Detect the language of the provided text
    Returns one of the supported languages
    """
    try:
        # Simple rule-based language detection as fallback
        # Check for Arabic characters (Unicode range for Arabic)
        arabic_char_count = sum(1 for char in text if '\u0600' <= char <= '\u06FF')
        if arabic_char_count > len(text) * 0.4:  # If more than 40% is Arabic
            return "Arabic"
            
        # Check for Hindi/Devanagari characters
        hindi_char_count = sum(1 for char in text if '\u0900' <= char <= '\u097F')
        if hindi_char_count > len(text) * 0.4:  # If more than 40% is Hindi
            return "Hindi"
            
        # Try with OpenAI if basic detection doesn't work
        try:
            # The newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # Do not change this unless explicitly requested by the user
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a language detection tool. Identify which language this text is written in. Only respond with one of these options: English, Arabic, Hindi. Nothing else."},
                    {"role": "user", "content": text}
                ],
                max_tokens=10,
                temperature=0.1
            )
            
            detected = response.choices[0].message.content.strip()
            if detected in supported_languages:
                return detected
        except Exception as e:
            print(f"OpenAI language detection failed: {e}")
            # Continue with default below
        
        # Default to English if nothing else worked
        return "English"
    except Exception as e:
        print(f"Error detecting language: {e}")
        return "English"  # Default to English on error

def translate_text(text, source_language, target_language):
    """
    Translate text from source language to target language
    """
    try:
        # The newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # Do not change this unless explicitly requested by the user
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"You are a professional translator. Translate the following text from {source_language} to {target_language}. Preserve the meaning, tone, and style. Only respond with the translation, no explanations or additional text."},
                {"role": "user", "content": text}
            ],
            temperature=0.3
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error translating text: {e}")
        return text  # Return original text if translation fails

