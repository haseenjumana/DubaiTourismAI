import os
import pandas as pd
import faiss
import numpy as np
from openai import OpenAI
import csv
import json

# Initialize OpenAI client - check both env vars and streamlit secrets
try:
    if hasattr(st, "secrets") and "openai" in st.secrets:
        OPENAI_API_KEY = st.secrets["openai"]["api_key"]
    else:
        OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
except Exception as e:
    # Fallback to environment variables if secrets access fails
    print(f"Error accessing Streamlit secrets: {e}")
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    
if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)
else:
    st.warning("OPENAI_API_KEY not found in environment variables or Streamlit secrets")
    client = None
def get_embedding(text):
    """
    Get embedding for text using OpenAI's embeddings API
    """
    try:
        response = client.embeddings.create(
            model="text-embedding-ada-002",
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error getting embedding: {e}")
        return None

def create_faiss_index(embeddings):
    """
    Create a FAISS index from a list of embeddings
    """
    dimension = len(embeddings[0])
    index = faiss.IndexFlatL2(dimension)
    embeddings_np = np.array(embeddings).astype('float32')
    index.add(embeddings_np)
    return index

def initialize_vector_store():
    """
    Initialize FAISS vector store with Dubai tourism and business information
    """
    # Create the data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)

    # Define paths for data files
    json_path = "data/dubai_info.json"
    csv_path = "data/dubai_faqs.csv"

    # Define default FAQs to use if no data files exist
    default_faqs = [
        {"question": "What are the top tourist attractions in Dubai?", 
         "answer": "Dubai's top attractions include the Burj Khalifa (world's tallest building), Palm Jumeirah, Dubai Mall, Dubai Frame, Dubai Miracle Garden, Global Village, Dubai Marina, and the historic Al Fahidi district."},

        {"question": "How can I get a tourist visa for Dubai?", 
         "answer": "Tourist visas for Dubai can be obtained through airlines (Emirates/Etihad), hotels, travel agencies, or online through the GDRFA website. Many countries get visa-on-arrival. The process typically takes 3-5 working days."},

        {"question": "What is the best time to visit Dubai?", 
         "answer": "The best time to visit Dubai is from November to March when the weather is pleasant (20-25°C). Summer (June-September) is extremely hot (45°C+) but offers lower hotel rates. Key events include Dubai Shopping Festival (December-January) and Dubai Food Festival (February)."},

        {"question": "How can I start a business in Dubai?", 
         "answer": "To start a business in Dubai: 1) Choose a business activity, 2) Select a legal form (LLC, Free Zone, etc.), 3) Apply for initial approval, 4) Choose a trade name, 5) Get a business license through DED (Department of Economic Development), 6) Open a corporate bank account. Free Zones offer 100% foreign ownership."},

        {"question": "What is the Golden Visa program?", 
         "answer": "Dubai's Golden Visa offers 5-10 year residency to investors, entrepreneurs, specialized talents, scientists, outstanding students, humanitarian pioneers, and frontline heroes. Investment requirements range from AED 2 million in property to AED 10 million in public investments."},

        {"question": "What are the business free zones in Dubai?", 
         "answer": "Dubai has over 30 Free Zones including Dubai Internet City (technology), DMCC (commodities), JAFZA (Jebel Ali - manufacturing/logistics), Dubai Media City, Dubai Healthcare City, and Dubai International Financial Centre (DIFC). Each specializes in specific sectors with benefits like 100% foreign ownership and tax exemptions."},

        {"question": "How is the public transportation in Dubai?", 
         "answer": "Dubai's public transport includes the Metro (Red and Green lines), Dubai Tram, buses, water taxis (abras), and monorail. The Nol card is used for payment across all transport modes. Taxis and ride-hailing services like Uber and Careem are widely available."},

        {"question": "What are the local customs and etiquette in Dubai?", 
         "answer": "In Dubai, modest dress is appreciated (shoulders and knees covered in public places). Public displays of affection should be limited. Alcohol is only permitted in licensed venues. During Ramadan, eating/drinking in public daytime is restricted. Always ask permission before photographing locals."},

        {"question": "What documents do I need for a freelance visa in Dubai?", 
         "answer": "For a Dubai freelance visa you need: passport copy, CV/portfolio, bank statements, educational certificates, NOC from sponsor (if applicable), and business plan. Apply through free zones like Dubai Media City, TECOM, or Dubai Design District. Cost ranges from AED 15,000-30,000 annually."},

        {"question": "How can I check the status of my visa application?", 
         "answer": "Check your Dubai visa status through the GDRFA website (gdrfad.gov.ae), the GDRFA Dubai app, or by calling 800-5111. You'll need your application number and passport details. The ICA website (ica.gov.ae) can also be used for federal visa services."}
    ]

    # Load FAQs data, prioritizing JSON if available, then CSV, then fallback to defaults
    faqs = []

    # Try to load from JSON file first
    if os.path.exists(json_path):
        try:
            print("Loading data from JSON file")
            with open(json_path, 'r', encoding='utf-8') as file:
                faqs = json.load(file)
        except Exception as e:
            print(f"Error loading JSON file: {e}")
            faqs = []

    # If JSON failed or doesn't exist, try CSV
    if not faqs and os.path.exists(csv_path):
        try:
            print("Loading data from CSV file")
            faqs_df = pd.read_csv(csv_path)
            faqs = faqs_df.to_dict('records')
        except Exception as e:
            print(f"Error loading CSV file: {e}")
            faqs = []

    # If no data could be loaded, create default files
    if not faqs:
        print("No data files found, creating default files")
        faqs = default_faqs

        # Create JSON file
        try:
            with open(json_path, 'w', encoding='utf-8') as file:
                json.dump(faqs, file, indent=2)
        except Exception as e:
            print(f"Error creating JSON file: {e}")

        # Create CSV file
        try:
            with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=["question", "answer"])
                writer.writeheader()
                writer.writerows(faqs)
        except Exception as e:
            print(f"Error creating CSV file: {e}")

    # Combine questions and answers for better context
    texts = [f"Q: {item['question']}\nA: {item['answer']}" for item in faqs]

    # Due to OpenAI API quota limits, we'll use the simple keyword search method instead
    print("Using simple keyword search because of potential OpenAI API quota limitations")
    return {"texts": texts, "fallback": True}

def get_dubai_info(query, vector_store, top_k=3):
    """
    Retrieve relevant Dubai information based on the query
    """
    # Check if we're in fallback mode
    if vector_store.get("fallback", False):
        return simple_keyword_search(query, vector_store["texts"], top_k)

    try:
        query_embedding = get_embedding(query)

        # If embedding failed, fall back to simple search
        if query_embedding is None:
            print("Embedding generation failed, using simple search fallback")
            return simple_keyword_search(query, vector_store["texts"], top_k)

        query_embedding_np = np.array([query_embedding]).astype('float32')

        # Search the vector store
        distances, indices = vector_store["index"].search(query_embedding_np, top_k)

        # Get the relevant texts
        relevant_texts = [vector_store["texts"][idx] for idx in indices[0]]

        # Combine texts into a single context
        context = "\n\n".join(relevant_texts)

        return context
    except Exception as e:
        print(f"Error retrieving Dubai information: {e}")
        print("Falling back to simple keyword search")
        return simple_keyword_search(query, vector_store["texts"], top_k)

def simple_keyword_search(query, texts, top_k=3):
    """
    A simple keyword-based search fallback when vector search is unavailable
    """
    print("Using simple keyword search because of potential OpenAI API quota limitations")
    try:
        # First look for exact phrase match
        exact_matches = []
        query_lower = query.lower()
        for text in texts:
            if query_lower in text.lower():
                exact_matches.append((text, len(query)))  # Higher score for exact matches

        # If we have exact matches, prioritize those
        if exact_matches:
            exact_matches.sort(key=lambda x: x[1], reverse=True)
            return "\n\n".join([text for text, _ in exact_matches[:top_k]])

        # Define categories for better matching
        categories = {
            "visa": ["visa", "travel", "tourist", "visit", "immigration", "entry"],
            "business": ["business", "company", "start", "entrepreneur", "license", "free zone", "investment"],
            "attractions": ["attraction", "visit", "place", "see", "museum", "beach", "mall", "shopping"],
            "transportation": ["transport", "metro", "bus", "taxi", "tram", "travel", "airport"],
            "food": ["food", "restaurant", "cuisine", "eat", "dinner", "lunch"],
            "culture": ["culture", "tradition", "custom", "language", "religion", "ramadan"],
            "weather": ["weather", "climate", "temperature", "hot", "rain", "sunny"],
            "accommodation": ["hotel", "stay", "accommodation", "apartment", "airbnb", "booking"],
        }

        # Check if query falls into any category
        query_category = None
        for category, keywords in categories.items():
            if any(word in query_lower for word in keywords):
                query_category = category
                break

        # Split the query into keywords
        keywords = query_lower.split()

        # Score each text based on keyword matches
        scored_texts = []
        for text in texts:
            text_lower = text.lower()
            # Basic word match scoring
            score = sum(1 for keyword in keywords if keyword in text_lower)

            # Bonus for category matches if we identified a category
            if query_category:
                category_bonus = sum(1 for keyword in categories[query_category] if keyword in text_lower)
                score += category_bonus * 0.5  # Add half weight for category matches

            # Extra points for question keywords in FAQ questions
            if "Q:" in text and "A:" in text:
                question_part = text.split("A:")[0]  # Get just the question part
                question_match = sum(1 for keyword in keywords if keyword in question_part.lower())
                score += question_match * 2  # Double points for question matches

            scored_texts.append((text, score))

        # Sort texts by score (highest first)
        scored_texts.sort(key=lambda x: x[1], reverse=True)

        # Get the top_k texts with non-zero scores
        top_texts = [text for text, score in scored_texts[:top_k] if score > 0]

        # If no matches found, provide categorical fallbacks
        if not top_texts:
            # If we identified a category but found no specific matches, return category-specific fallback
            if query_category == "visa":
                return "Tourist visas for Dubai can be obtained through airlines (Emirates/Etihad), hotels, travel agencies, or online through the GDRFA website. Many countries get visa-on-arrival. The process typically takes 3-5 working days."
            elif query_category == "business":
                return "To start a business in Dubai: 1) Choose a business activity, 2) Select a legal form (LLC, Free Zone, etc.), 3) Apply for initial approval, 4) Choose a trade name, 5) Get a business license through DED (Department of Economic Development), 6) Open a corporate bank account. Free Zones offer 100% foreign ownership."
            elif query_category == "attractions":
                return "Dubai's top attractions include the Burj Khalifa (world's tallest building), Palm Jumeirah, Dubai Mall, Dubai Frame, Dubai Miracle Garden, Global Village, Dubai Marina, and the historic Al Fahidi district."
            elif query_category == "transportation":
                return "Dubai's public transport includes the Metro (Red and Green lines), Dubai Tram, buses, water taxis (abras), and monorail. The Nol card is used for payment across all transport modes. Taxis and ride-hailing services like Uber and Careem are widely available."
            elif query_category == "food":
                return "Dubai offers diverse cuisines including Emirati, Lebanese, Indian, Pakistani, Iranian, and international options. Popular dishes include Al Machboos (spiced rice with meat), Al Harees (wheat and meat dish), and shawarma. Visit areas like Deira, Bur Dubai, or JBR for authentic local experiences."
            elif query_category == "culture":
                return "Dubai has Islamic culture with modern influences. Modest dress is recommended especially in religious/government places. Ramadan observes fasting during daylight; public eating may be restricted. Arabic is official, but English is widely spoken. Alcohol is only served in licensed venues."
            elif query_category == "weather":
                return "Dubai has a desert climate with very hot summers (40°C+/104°F+) from May-September and mild winters (25°C/77°F) from December-March. The best time to visit is November to April. It rarely rains, mostly January-March. Always carry water and sun protection."
            elif query_category == "accommodation":
                return "Dubai offers accommodation ranging from 5-star luxury hotels (Burj Al Arab, Atlantis) to budget options. Areas include Downtown (near Burj Khalifa), Dubai Marina (beachfront), Deira (traditional), and Palm Jumeirah (luxury resorts). Book early during high season (November-April)."
            else:
                # If all else fails, return general information on Dubai
                return "Dubai is a city and emirate in the United Arab Emirates known for luxury shopping, ultramodern architecture, and a lively nightlife scene. For tourism information, visit visitdubai.com. For business setup, visit the Dubai Department of Economic Development website."

        # Combine texts into a single context
        context = "\n\n".join(top_texts)

        return context
    except Exception as e:
        print(f"Error in simple search: {e}")
        return "Dubai is a city and emirate in the United Arab Emirates known for luxury shopping, ultramodern architecture, and a lively nightlife scene. For tourism information, visit visitdubai.com. For business setup, visit the Dubai Department of Economic Development website."
