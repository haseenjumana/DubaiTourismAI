import os
import streamlit as st

# Handle potential import errors gracefully
try:
    from openai import OpenAI
    # Initialize OpenAI client
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    if OPENAI_API_KEY:
        client = OpenAI(api_key=OPENAI_API_KEY)
    else:
        st.warning("OPENAI_API_KEY not found in environment variables. Some features may not work.")
        client = None
except ImportError:
    st.error("openai package not installed. Run: pip install openai")
    client = None

def get_ai_response(query, context=""):
    """
    Generate AI response to user query with Dubai-specific context
    """
    try:
        # Prepare prompt with context
        system_prompt = """
        You are the official AI assistant for Dubai Tourism and Business services.
        You provide accurate, helpful information about:
        1. Tourism in Dubai (attractions, hotels, events, transportation)
        2. Business opportunities and processes (starting a business, free zones, licenses)
        3. Government services (visas, permits, regulations)
        
        Be concise but thorough. Be courteous and professional.
        If you don't know something, admit it rather than providing incorrect information.
        Always provide the most up-to-date information available to you.
        """
        
        user_prompt = query
        if context:
            user_prompt = f"Based on this information:\n\n{context}\n\nPlease answer: {query}"
        
        # The newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # Do not change this unless explicitly requested by the user
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating AI response: {e}")
        
        # Extract relevant information from context if available
        if context and len(context) > 0:
            # If we have context, we can try to use it for a simple response
            if "visa" in query.lower() or "travel" in query.lower() or "tourist" in query.lower():
                return "Tourist visas for Dubai can be obtained through airlines (Emirates/Etihad), hotels, travel agencies, or online through the GDRFA website. Many countries get visa-on-arrival. The process typically takes 3-5 working days."
            
            elif "attraction" in query.lower() or "visit" in query.lower() or "place" in query.lower():
                return "Dubai's top attractions include the Burj Khalifa (world's tallest building), Palm Jumeirah, Dubai Mall, Dubai Frame, Dubai Miracle Garden, Global Village, Dubai Marina, and the historic Al Fahidi district."
            
            elif "business" in query.lower() or "company" in query.lower() or "start" in query.lower():
                return "To start a business in Dubai: 1) Choose a business activity, 2) Select a legal form (LLC, Free Zone, etc.), 3) Apply for initial approval, 4) Choose a trade name, 5) Get a business license through DED (Department of Economic Development), 6) Open a corporate bank account. Free Zones offer 100% foreign ownership."
            
            elif "transport" in query.lower() or "metro" in query.lower() or "bus" in query.lower():
                return "Dubai's public transport includes the Metro (Red and Green lines), Dubai Tram, buses, water taxis (abras), and monorail. The Nol card is used for payment across all transport modes. Taxis and ride-hailing services like Uber and Careem are widely available."
            
            else:
                # Extract the context and return a relevant piece
                context_pieces = context.split("\n\n")
                for piece in context_pieces:
                    if piece and len(piece) > 20:
                        if piece.lower().find(query.lower().split()[0]) >= 0:
                            return piece.replace("Q: ", "").replace("A: ", "")
                
                # If nothing specific matched, return the first piece of context
                if context_pieces and len(context_pieces) > 0:
                    return context_pieces[0].replace("Q: ", "").replace("A: ", "")
        
        # Generic fallback response
        return "I'm sorry, I'm currently experiencing technical difficulties. Please try again later. For visa information, visit the GDRFA website. For tourism, check visitdubai.com, and for business setup, visit the Dubai Department of Economic Development website."
