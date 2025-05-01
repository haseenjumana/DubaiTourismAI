import streamlit as st
import pandas as pd
import requests
from PIL import Image
import os
import sys
import random
from io import BytesIO

# Add the parent directory to sys.path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import utility functions
from utils.model_utils import get_ai_response
from utils.vector_store import get_dubai_info, initialize_vector_store

# Page config
st.set_page_config(
    page_title="Dubai Tourism Guide",
    page_icon="🏝️",
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

# Initialize vector store if needed
if "vector_store" not in st.session_state:
    st.session_state.vector_store = initialize_vector_store()

# Tourism header
st.title("🌴 Dubai Tourism Guide")
st.markdown("""
### Discover the wonders of Dubai
Explore top attractions, hotels, dining, and cultural experiences in this vibrant city.
""")

# Function to display attraction details with placeholder image
def display_attraction(name, description, location, ticket_price, image_url=None):
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Create the asset directory if it doesn't exist
        os.makedirs("assets/attractions", exist_ok=True)
        
        # Use a placeholder image when image_url is None
        try:
            if image_url:
                # Try to download the image
                response = requests.get(image_url)
                if response.status_code == 200:
                    img = Image.open(BytesIO(response.content))
                    st.image(img, use_container_width=True)
                else:
                    # If download fails, use a placeholder
                    st.image("assets/dubai_tourism_logo.svg", use_container_width=True)
            else:
                # No image URL provided
                st.image("assets/dubai_tourism_logo.svg", use_container_width=True)
        except Exception as e:
            # Handle any errors with image loading
            st.image("assets/dubai_tourism_logo.svg", use_container_width=True)
    
    with col2:
        st.subheader(name)
        st.markdown(description)
        st.markdown(f"**Location:** {location}")
        st.markdown(f"**Ticket Price:** {ticket_price}")
        
        # Create map button with location data
        if st.button(f"📍 View on Map", key=f"map_{name.replace(' ', '_')}"):
            # Create a dictionary of Dubai attractions with their coordinates
            attraction_coordinates = {
                "Burj Khalifa": {"lat": 25.197197, "lon": 55.274376},
                "Dubai Mall": {"lat": 25.198765, "lon": 55.279503},
                "Palm Jumeirah": {"lat": 25.111882, "lon": 55.138779},
                "Dubai Frame": {"lat": 25.234661, "lon": 55.300659},
                "Dubai Miracle Garden": {"lat": 25.061905, "lon": 55.247468},
                "Museum of the Future": {"lat": 25.218172, "lon": 55.280606},
            }
            
            # Get coordinates for this attraction
            coords = attraction_coordinates.get(name, {"lat": 25.197197, "lon": 55.274376})  # Default to Burj Khalifa
            
            # Create HTML for an embedded map
            map_html = f"""
            <div style="margin-top: 10px;">
                <iframe 
                    width="100%" 
                    height="300" 
                    frameborder="0" 
                    scrolling="no" 
                    marginheight="0" 
                    marginwidth="0" 
                    src="https://www.openstreetmap.org/export/embed.html?bbox={coords['lon']-0.01}%2C{coords['lat']-0.01}%2C{coords['lon']+0.01}%2C{coords['lat']+0.01}&amp;layer=mapnik&amp;marker={coords['lat']}%2C{coords['lon']}" 
                    style="border: 1px solid #ddd; border-radius: 4px;"
                ></iframe>
                <br/>
                <small>
                    <a href="https://www.openstreetmap.org/?mlat={coords['lat']}&amp;mlon={coords['lon']}&amp;zoom=15" target="_blank">
                        View larger map
                    </a>
                </small>
            </div>
            """
            st.markdown(map_html, unsafe_allow_html=True)

# Top attractions
st.header("🏙️ Top Attractions in Dubai")

# List of attractions with details
attractions = [
    {
        "name": "Burj Khalifa",
        "description": "The world's tallest building standing at 828m. Enjoy breathtaking views from At The Top observation deck on the 124th, 125th, and 148th floors.",
        "location": "1 Sheikh Mohammed bin Rashid Blvd, Downtown Dubai",
        "ticket_price": "From AED 149 (non-prime hours) to AED 379 (prime hours)",
        "image_url": None  # Placeholder
    },
    {
        "name": "Dubai Mall",
        "description": "One of the world's largest shopping malls with over 1,200 shops, an aquarium, ice rink, and indoor theme parks. Home to the famous Dubai Fountain.",
        "location": "Financial Centre Road, Downtown Dubai",
        "ticket_price": "Free entry (attractions inside have separate fees)",
        "image_url": None  # Placeholder
    },
    {
        "name": "Palm Jumeirah",
        "description": "Man-made island in the shape of a palm tree. Features luxury hotels, residences, and attractions including Atlantis The Palm resort.",
        "location": "Palm Jumeirah, Dubai",
        "ticket_price": "Free to visit (hotels and attractions have separate fees)",
        "image_url": None  # Placeholder
    },
    {
        "name": "Dubai Frame",
        "description": "Iconic landmark offering panoramic views of old and new Dubai. The 150m-tall structure features a glass bridge connecting the two towers.",
        "location": "Zabeel Park, Za'abeel, Dubai",
        "ticket_price": "AED 50 for adults, AED 20 for children",
        "image_url": None  # Placeholder
    },
    {
        "name": "Dubai Miracle Garden",
        "description": "The world's largest natural flower garden with over 50 million flowers arranged in stunning designs, arches, and patterns.",
        "location": "Al Barsha South 3, Dubailand",
        "ticket_price": "AED 55 for adults, AED 40 for children (seasonal opening)",
        "image_url": None  # Placeholder
    },
    {
        "name": "Museum of the Future",
        "description": "Innovative museum exploring how technology could evolve to enhance humanity. The distinctive ring-shaped building is covered in Arabic calligraphy.",
        "location": "Sheikh Zayed Road, Financial Centre area",
        "ticket_price": "AED 145 per person",
        "image_url": None  # Placeholder
    }
]

# Display attractions in tabs
attraction_tabs = st.tabs([attr["name"] for attr in attractions])

for i, tab in enumerate(attraction_tabs):
    with tab:
        display_attraction(
            attractions[i]["name"],
            attractions[i]["description"],
            attractions[i]["location"],
            attractions[i]["ticket_price"],
            attractions[i]["image_url"]
        )

# Cultural experiences
st.header("🏮 Cultural Experiences")
st.markdown("""
Immerse yourself in Dubai's rich cultural heritage and traditions through these authentic experiences.
""")

# Display cultural experiences in columns
cultural_col1, cultural_col2 = st.columns(2)

with cultural_col1:
    st.subheader("Old Dubai Walking Tour")
    st.markdown("""
    Explore the historic Al Fahidi district, Dubai Creek, and traditional souks. 
    Learn about Dubai's pearl diving history and transformation from fishing village to global city.
    
    **Duration:** 3-4 hours  
    **Price:** From AED 150 per person  
    **Meeting Point:** Al Fahidi Metro Station
    """)
    
    st.subheader("Desert Safari with Bedouin Camp")
    st.markdown("""
    Experience thrilling dune bashing, camel rides, and traditional entertainment at a Bedouin-style camp. 
    Includes henna painting, shisha, and a barbecue dinner under the stars.
    
    **Duration:** 6 hours (afternoon to evening)  
    **Price:** From AED 250 per person  
    **Includes:** Hotel pickup and drop-off
    """)

with cultural_col2:
    st.subheader("Sheikh Mohammed Centre for Cultural Understanding")
    st.markdown("""
    Participate in cultural meals, heritage tours, and conversations with local Emiratis. 
    Ask questions about Emirati culture, customs, and religion in an open, friendly environment.
    
    **Location:** Al Fahidi Historical Neighborhood  
    **Price:** From AED 95 (cultural breakfast) to AED 130 (cultural dinner)  
    **Languages:** English (other languages available on request)
    """)
    
    st.subheader("Traditional Abra Ride on Dubai Creek")
    st.markdown("""
    Cross Dubai Creek on a traditional wooden boat used by locals for generations. 
    See the contrast between old and new Dubai while learning about the creek's importance to the city's development.
    
    **Duration:** 20 minutes  
    **Price:** Only AED 1 per trip  
    **Operating Hours:** 24 hours daily
    """)

# Seasonal events and festivals
st.header("🎭 Seasonal Events & Festivals")

# Create an expandable section for each season
seasons = st.tabs(["Winter (Oct-Mar)", "Summer (Apr-Sep)"])

with seasons[0]:
    st.subheader("Dubai Shopping Festival (December-January)")
    st.markdown("""
    The city's biggest shopping event featuring massive discounts, raffles with luxury prizes, 
    fireworks, concerts, and family entertainment across the city.
    """)
    
    st.subheader("Dubai Food Festival (February)")
    st.markdown("""
    Celebration of Dubai's diverse culinary scene with restaurant deals, food trucks, 
    chef demonstrations, and unique dining experiences at venues across the city.
    """)
    
    st.subheader("Art Dubai (March)")
    st.markdown("""
    Leading international art fair showcasing contemporary and modern art from the Middle East, 
    North Africa, and South Asia. Held at Madinat Jumeirah.
    """)

with seasons[1]:
    st.subheader("Dubai Summer Surprises (July-August)")
    st.markdown("""
    Six-week summer festival with retail promotions, indoor entertainment, and special 
    hotel rates to encourage tourism during the hot summer months.
    """)
    
    st.subheader("Eid Celebrations (Varies based on Islamic calendar)")
    st.markdown("""
    Festivities marking Eid Al-Fitr and Eid Al-Adha with special events, 
    fireworks, concerts, and family activities throughout the city.
    """)
    
    st.subheader("Dubai Sports World (June-August)")
    st.markdown("""
    Indoor sporting event allowing visitors to play and watch various sports in 
    air-conditioned comfort during the summer heat.
    """)

# Practical travel information
st.header("✈️ Practical Travel Information")

# Create tabs for different practical information categories
info_tabs = st.tabs(["Best Time to Visit", "Transportation", "Accommodation", "Visa Information", "Local Customs"])

with info_tabs[0]:
    st.subheader("Best Time to Visit Dubai")
    st.markdown("""
    **November to March:** Ideal weather with temperatures between 20-30°C (68-86°F). Peak tourist season with higher prices.
    
    **April and October:** Transition months with warm but tolerable temperatures, fewer crowds, and better rates.
    
    **May to September:** Very hot (40-50°C/104-122°F) but lowest prices and fewer tourists. Indoor activities and water parks are popular during this period.
    
    **Ramadan:** Dates vary each year. Many restaurants close during daylight hours, but the evening atmosphere is festive and special Iftar meals are available.
    """)

with info_tabs[1]:
    st.subheader("Getting Around Dubai")
    st.markdown("""
    **Dubai Metro:** Clean, efficient, and air-conditioned. Red Line runs along Sheikh Zayed Road, and Green Line covers older parts of Dubai. Gold Class and Women & Children carriages available.
    
    **Dubai Tram:** Connects Dubai Marina, JBR, and Palm Jumeirah areas.
    
    **Buses:** Extensive network covering areas not reached by Metro. Use Nol card for payment.
    
    **Taxis:** Abundant and relatively affordable. All are metered with different rates for day and night.
    
    **Ride-hailing apps:** Uber and Careem operate throughout the city.
    
    **Water transport:** Traditional abras (AED 1) across Dubai Creek, water taxis, and Dubai Ferry for scenic routes.
    
    **Nol Card:** Unified payment card for Dubai's public transport system. Available in Silver, Gold, and Blue varieties.
    """)

with info_tabs[2]:
    st.subheader("Where to Stay in Dubai")
    st.markdown("""
    **Dubai Marina & JBR:** Beachfront area with restaurants, shops, and nightlife. Popular with Western expats and tourists.
    
    **Downtown Dubai:** Home to Burj Khalifa and Dubai Mall. Central location with luxury hotels and apartments.
    
    **Palm Jumeirah:** Luxury resorts on the iconic palm-shaped island. Best for beach lovers with a higher budget.
    
    **Deira & Bur Dubai:** Historical areas with traditional souks. More affordable accommodation with authentic character.
    
    **Al Barsha & Business Bay:** Mid-range options near Mall of the Emirates and Dubai Design District.
    
    **Desert Resorts:** Luxury desert experiences outside the city, offering tranquility and traditional activities.
    """)

with info_tabs[3]:
    st.subheader("Visa Requirements")
    st.markdown("""
    **Visa on arrival (free, 30-90 days):** Available for citizens of GCC countries, USA, UK, EU, Australia, and many others. Check the official GDRFA website for the full list.
    
    **Tourist Visa:** Required for many nationalities. Can be obtained through airlines like Emirates, hotels, or tour operators.
    
    **Transit Visa:** Available for layovers of 8+ hours through Dubai-based airlines.
    
    **Application process:** Submit passport copy, photograph, and flight details. Processing time is usually 3-5 working days.
    
    **Visit Visa extensions:** Possible for an additional 30 days through GDRFA or by doing a visa run to a neighboring country.
    
    **Official resource:** [General Directorate of Residency and Foreigners Affairs](https://gdrfad.gov.ae/en)
    """)

with info_tabs[4]:
    st.subheader("Local Customs & Etiquette")
    st.markdown("""
    **Dress code:** Modest dress is appreciated, especially in shopping malls, public places, and religious sites. Cover shoulders and knees. Swimwear is acceptable only at beaches and pool areas.
    
    **Ramadan observance:** During the holy month, eating, drinking, and smoking in public during daylight hours is prohibited. Many restaurants close or offer screened areas for daytime dining.
    
    **Public behavior:** Public displays of affection should be limited to holding hands. Public intoxication, swearing, and aggressive behavior can result in legal consequences.
    
    **Photography:** Ask permission before photographing locals, especially women. Avoid photographing government buildings, airports, or military installations.
    
    **Alcohol consumption:** Legal only in licensed venues such as hotels, restaurants, and bars. Being drunk in public is an offense.
    
    **Religious respect:** Respect for Islam and other religions is expected. The call to prayer is heard throughout the day.
    """)

# Tourism Planning Tool
st.header("🗓️ Plan Your Dubai Trip")
st.markdown("Use this tool to create your perfect Dubai itinerary based on your interests and trip duration.")

# Create a trip planning form
with st.form("trip_planner"):
    trip_duration = st.slider("Trip Duration (Days)", 1, 14, 5)
    
    interests = st.multiselect(
        "Select Your Interests",
        ["Sightseeing", "Shopping", "Adventure", "Culture & History", "Relaxation", "Food & Dining", "Nightlife", "Family Activities"],
        default=["Sightseeing", "Shopping"]
    )
    
    budget = st.select_slider(
        "Budget Level",
        options=["Budget", "Moderate", "Luxury"],
        value="Moderate"
    )
    
    travel_month = st.selectbox(
        "When are you planning to visit?",
        ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    )
    
    generate_button = st.form_submit_button("Generate Itinerary")

# Display generated itinerary if button is clicked
if generate_button:
    st.subheader("Your Personalized Dubai Itinerary")
    
    # In a real application, this would use an AI model to generate a personalized itinerary
    # For now, we'll display a sample itinerary based on the selected parameters
    
    # Sample itinerary days based on interests
    sightseeing_days = [
        "**Morning:** Burj Khalifa 'At The Top' observation deck\n**Afternoon:** Dubai Mall exploration and Dubai Aquarium\n**Evening:** Dubai Fountain show and dinner at Souk Al Bahar",
        "**Morning:** Dubai Frame visit\n**Afternoon:** Zabeel Park relaxation\n**Evening:** Dinner with a view at one of Sheikh Zayed Road's rooftop restaurants",
        "**Morning:** Museum of the Future\n**Afternoon:** Dubai Marina Yacht Tour\n**Evening:** The Walk at JBR for dinner and people-watching"
    ]
    
    shopping_days = [
        "**Morning:** Dubai Mall for luxury shopping\n**Afternoon:** Continue at Fashion Avenue\n**Evening:** Souk Al Bahar for artisanal items",
        "**Morning:** Mall of the Emirates and Ski Dubai\n**Afternoon:** City Walk for outdoor shopping\n**Evening:** Boxpark for unique retail and dining",
        "**Morning:** Traditional souks in Deira (Gold Souk, Spice Souk)\n**Afternoon:** Textile Souk in Bur Dubai\n**Evening:** Dubai Festival City Mall and light show"
    ]
    
    adventure_days = [
        "**Morning:** Desert safari with dune bashing\n**Afternoon:** Camel riding and sandboarding\n**Evening:** Bedouin camp dinner and entertainment",
        "**Morning:** Skydiving over Palm Jumeirah\n**Afternoon:** Aquaventure Waterpark at Atlantis\n**Evening:** Dinner at Lost Chambers Aquarium",
        "**Morning:** Hot air balloon desert flight\n**Afternoon:** Helicopter tour over Dubai\n**Evening:** Dhow cruise dinner"
    ]
    
    culture_days = [
        "**Morning:** Al Fahidi Historical District walking tour\n**Afternoon:** Dubai Museum and Coffee Museum\n**Evening:** Cultural dinner at Sheikh Mohammed Centre",
        "**Morning:** Jumeirah Mosque visit and cultural understanding program\n**Afternoon:** Heritage House and diving village\n**Evening:** Traditional Emirati dinner",
        "**Morning:** Alserkal Avenue art galleries\n**Afternoon:** Dubai Opera tour or performance\n**Evening:** Cultural show and dinner"
    ]
    
    relaxation_days = [
        "**Morning:** Private beach day at a beach club\n**Afternoon:** Luxury spa treatment\n**Evening:** Sunset yacht cruise",
        "**Morning:** Yoga on the beach\n**Afternoon:** Talise Ottoman Spa at Jumeirah Zabeel Saray\n**Evening:** Peaceful dinner by the water",
        "**Morning:** Desert resort day pass\n**Afternoon:** Pool relaxation and treatments\n**Evening:** Stargazing in the desert"
    ]
    
    food_days = [
        "**Morning:** Traditional Emirati breakfast at Arabian Tea House\n**Afternoon:** Food tour in Old Dubai\n**Evening:** Dinner at a Michelin-starred restaurant",
        "**Morning:** Cooking class for Middle Eastern cuisine\n**Afternoon:** Food market exploration\n**Evening:** Dinner safari with international cuisine",
        "**Morning:** Farmers market visit (seasonal)\n**Afternoon:** Dubai Food Festival events (if available)\n**Evening:** Dhow dinner cruise"
    ]
    
    # Map interests to day plans
    interest_map = {
        "Sightseeing": sightseeing_days,
        "Shopping": shopping_days,
        "Adventure": adventure_days,
        "Culture & History": culture_days,
        "Relaxation": relaxation_days,
        "Food & Dining": food_days
    }
    
    # Create itinerary based on selected interests and duration
    itinerary_days = []
    for i in range(trip_duration):
        # Select an interest for this day (cycling through selected interests)
        if interests:
            day_interest = interests[i % len(interests)]
            if day_interest in interest_map:
                # Pick a random day plan for this interest
                day_plan = random.choice(interest_map[day_interest])
                itinerary_days.append((f"Day {i+1} - {day_interest}", day_plan))
    
    # Display the itinerary
    for day_title, day_plan in itinerary_days:
        st.markdown(f"### {day_title}")
        st.markdown(day_plan)
        st.markdown("---")
    
    # Add travel tips based on selected month
    st.subheader("Travel Tips for " + travel_month)
    
    winter_months = ["November", "December", "January", "February", "March"]
    summer_months = ["May", "June", "July", "August", "September"]
    
    if travel_month in winter_months:
        st.markdown("""
        * Perfect weather for outdoor activities and desert excursions
        * Pack light layers as evenings can be cooler
        * Book attractions in advance as this is peak tourist season
        * Look for festival events like Dubai Shopping Festival (Dec-Jan) or Food Festival (Feb)
        """)
    elif travel_month in summer_months:
        st.markdown("""
        * Expect very high temperatures (40-50°C); plan indoor activities during peak daylight hours
        * Take advantage of summer deals on hotels and shopping
        * Stay hydrated and use sun protection when outdoors
        * Water parks and mall activities are ideal during this season
        * Check for Dubai Summer Surprises events and promotions
        """)
    else:  # Transition months
        st.markdown("""
        * Transitional weather with comfortable temperatures most days
        * Good balance of reasonable prices and manageable crowds
        * Ideal for a mix of indoor and outdoor activities
        * Check for seasonal events and concert schedules
        """)

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