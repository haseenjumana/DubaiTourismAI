import streamlit as st
import pandas as pd
import requests
from PIL import Image
import os
import sys

# Add the parent directory to sys.path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import utility functions
from utils.model_utils import get_ai_response
from utils.vector_store import get_dubai_info, initialize_vector_store

# Page config
st.set_page_config(
    page_title="Dubai Business Guide",
    page_icon="💼",
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

# Business header
st.title("🏢 Dubai Business Guide")
st.markdown("""
### Your gateway to business opportunities in Dubai
Explore business setup, free zones, investment opportunities, and more.
""")

# Business sectors in Dubai
business_sectors = [
    {
        "name": "Technology & Innovation",
        "description": "Dubai's tech sector is growing rapidly with initiatives like Dubai Internet City and Dubai Silicon Oasis. Focus areas include AI, blockchain, fintech, and smart city technologies.",
        "website": "https://www.dic.ae/",
        "growth": "High growth"
    },
    {
        "name": "Tourism & Hospitality",
        "description": "A cornerstone of Dubai's economy, with luxury hotels, theme parks, and shopping destinations. The sector continues to expand with new attractions and accommodations.",
        "website": "https://www.visitdubai.com/en/business-in-dubai/tourism",
        "growth": "Steady growth"
    },
    {
        "name": "Real Estate & Construction",
        "description": "Known for iconic developments like Burj Khalifa and Palm Jumeirah, Dubai's real estate sector offers various investment opportunities in residential, commercial, and mixed-use properties.",
        "website": "https://dubailand.gov.ae/",
        "growth": "Cyclical growth"
    },
    {
        "name": "Finance & Banking",
        "description": "Dubai International Financial Centre (DIFC) is a leading financial hub with hundreds of financial institutions. The sector benefits from a robust regulatory framework and strategic location.",
        "website": "https://www.difc.ae/",
        "growth": "High growth"
    },
    {
        "name": "Healthcare",
        "description": "Dubai Healthcare City leads the emirate's medical tourism initiative. The sector is expanding with new hospitals, clinics, and medical research facilities.",
        "website": "https://dhcc.ae/",
        "growth": "Rapid growth"
    },
    {
        "name": "Retail & E-commerce",
        "description": "Home to some of the world's largest malls, Dubai's retail sector is evolving with e-commerce platforms and innovative shopping experiences.",
        "website": "https://www.dubaicommercity.ae/",
        "growth": "High growth"
    },
    {
        "name": "Logistics & Transportation",
        "description": "With Jebel Ali Port and Dubai International Airport, the emirate is a global logistics hub connecting East and West trade routes.",
        "website": "https://www.dubailogisticsdistrict.ae/",
        "growth": "Steady growth"
    },
    {
        "name": "Education",
        "description": "Dubai has a growing education sector with international schools, universities, and specialized training centers in Dubai Knowledge Park and Academic City.",
        "website": "https://www.khda.gov.ae/",
        "growth": "Moderate growth"
    },
    {
        "name": "Media & Entertainment",
        "description": "Dubai Media City hosts global media companies, production studios, and entertainment businesses. The sector includes film production, broadcasting, and digital media.",
        "website": "https://www.dmc.ae/",
        "growth": "Moderate growth"
    },
    {
        "name": "Renewable Energy",
        "description": "Dubai is investing heavily in renewable energy, particularly solar power through the Mohammed bin Rashid Al Maktoum Solar Park and other green initiatives.",
        "website": "https://www.dewa.gov.ae/en/about-us/strategic-initiatives/mbr-solar-park",
        "growth": "Rapid growth"
    }
]

# Display business sectors
st.header("📈 Booming Business Sectors in Dubai")

# Create DataFrame and display as interactive table
business_df = pd.DataFrame(business_sectors)
st.dataframe(
    business_df,
    column_config={
        "name": "Sector",
        "description": "Overview",
        "website": st.column_config.LinkColumn("Official Website"),
        "growth": st.column_config.TextColumn("Growth Status", help="Current growth trend of the sector")
    },
    hide_index=True,
    use_container_width=True
)

# Free Zones in Dubai
st.header("🏙️ Dubai Free Zones")
st.markdown("""
Free Zones offer 100% foreign ownership, tax exemptions, and streamlined business setup processes.
Here are some of Dubai's prominent free zones:
""")

# Two columns for free zones
col1, col2 = st.columns(2)

with col1:
    st.subheader("Dubai Internet City (DIC)")
    st.markdown("""
    - **Focus**: Technology, IT, Software
    - **Benefits**: 100% foreign ownership, 0% import/export duties
    - **Companies**: Microsoft, IBM, Oracle, HP
    - **Website**: [Dubai Internet City](https://www.dic.ae/)
    """)
    
    st.subheader("Dubai Media City (DMC)")
    st.markdown("""
    - **Focus**: Media, Advertising, Publishing
    - **Benefits**: 100% foreign ownership, world-class infrastructure
    - **Companies**: CNN, BBC, MBC, Thomson Reuters
    - **Website**: [Dubai Media City](https://www.dmc.ae/)
    """)
    
    st.subheader("Dubai Healthcare City (DHCC)")
    st.markdown("""
    - **Focus**: Healthcare, Medical services, Research
    - **Benefits**: 100% foreign ownership, medical community
    - **Companies**: Harvard Medical School Dubai Center, Cleveland Clinic
    - **Website**: [Dubai Healthcare City](https://dhcc.ae/)
    """)
    
    st.subheader("Dubai Multi Commodities Centre (DMCC)")
    st.markdown("""
    - **Focus**: Commodities trade, Diamonds, Tea, Crypto
    - **Benefits**: 0% corporate tax for 50 years, custom-built facilities
    - **Companies**: Over 21,000 businesses from various sectors
    - **Website**: [DMCC](https://www.dmcc.ae/)
    """)

with col2:
    st.subheader("Dubai International Financial Centre (DIFC)")
    st.markdown("""
    - **Focus**: Banking, Finance, Insurance
    - **Benefits**: Independent legal system, Financial regulations
    - **Companies**: HSBC, Standard Chartered, Citibank
    - **Website**: [DIFC](https://www.difc.ae/)
    """)
    
    st.subheader("Jebel Ali Free Zone (JAFZA)")
    st.markdown("""
    - **Focus**: Trading, Manufacturing, Logistics
    - **Benefits**: Proximity to port and airport, warehouses
    - **Companies**: Over 9,000 companies from 100+ countries
    - **Website**: [JAFZA](https://jafza.ae/)
    """)
    
    st.subheader("Dubai Production City (DPC)")
    st.markdown("""
    - **Focus**: Publishing, Printing, Media production
    - **Benefits**: Modern infrastructure, business licenses
    - **Companies**: Global printing and production companies
    - **Website**: [Dubai Production City](https://www.dubaiproductioncity.ae/)
    """)
    
    st.subheader("Dubai Silicon Oasis (DSO)")
    st.markdown("""
    - **Focus**: Technology, Electronics, R&D
    - **Benefits**: High-tech infrastructure, tech support
    - **Companies**: Intel, AMD, Fujitsu
    - **Website**: [Dubai Silicon Oasis](https://www.dsoa.ae/)
    """)

# Business Setup Process
st.header("🔄 Business Setup Process in Dubai")

# Create tabs for different business structures
tabs = st.tabs(["Mainland Company", "Free Zone Company", "Offshore Company"])

with tabs[0]:
    st.subheader("Mainland Company Setup")
    st.markdown("""
    1. **Choose a legal structure** (LLC, Sole Establishment, etc.)
    2. **Select your business activities** from DED approved list
    3. **Choose a trade name** and get initial approval
    4. **Secure a location** and obtain tenancy contract
    5. **Submit documents** to Department of Economic Development (DED)
    6. **Receive business license** after approval
    7. **Open corporate bank account**
    
    **Advantages**: 100% market access in UAE, no trade restrictions, broader business scope
    
    **Official Resource**: [Department of Economic Development](https://ded.ae/)
    """)

with tabs[1]:
    st.subheader("Free Zone Company Setup")
    st.markdown("""
    1. **Select a suitable Free Zone** based on your business activity
    2. **Choose a legal structure** (FZ LLC, FZ Company, Branch)
    3. **Apply for a business license** specific to your activities
    4. **Lease office space** within the free zone
    5. **Submit all documentation** to the Free Zone Authority
    6. **Receive Free Zone license** after approval
    7. **Open corporate bank account**
    
    **Advantages**: 100% foreign ownership, 0% corporate and personal tax, 100% repatriation of capital
    
    **Processing Time**: 1-3 weeks on average
    """)

with tabs[2]:
    st.subheader("Offshore Company Setup")
    st.markdown("""
    1. **Select offshore jurisdiction** (JAFZA Offshore, RAKICC, etc.)
    2. **Choose a company name** and verify availability
    3. **Prepare required documents** including shareholder information
    4. **Appoint directors and shareholders**
    5. **Submit application** to relevant offshore authority
    6. **Receive incorporation certificate**
    7. **Open offshore bank account**
    
    **Advantages**: High level of privacy, asset protection, no minimum capital requirements
    
    **Limitations**: Cannot conduct business within UAE, no physical office required
    """)

# Business FAQ Section
st.header("❓ Business FAQs")

expander1 = st.expander("What permits and licenses do I need to start a business in Dubai?")
with expander1:
    query = "What permits and licenses do I need to start a business in Dubai?"
    context = get_dubai_info(query, st.session_state.vector_store)
    response = "To start a business in Dubai, you'll need several permits and licenses including: 1) Commercial/Professional/Industrial License from DED or Free Zone Authority, 2) Establishment Card, 3) Chamber of Commerce membership, 4) Activity-specific permits (depending on business type), 5) Residency visa for foreign entrepreneurs, and 6) Labor cards for employees. Additional approvals may be needed for specific sectors like food, education, or healthcare."
    st.write(response)

expander2 = st.expander("What are the costs involved in setting up a business in Dubai?")
with expander2:
    query = "What are the costs involved in setting up a business in Dubai?"
    context = get_dubai_info(query, st.session_state.vector_store)
    response = "Business setup costs in Dubai include: 1) License fees (AED 10,000-50,000), 2) Registration fees (AED 3,000-15,000), 3) Office/facility rent (varies by location), 4) Visa costs (AED 3,000-5,000 per visa), 5) Bank guarantee deposits, 6) Chamber of Commerce membership (AED 1,000-2,500), and 7) Miscellaneous fees for attestations, typing, etc. The total can range from AED 15,000 for a small Free Zone company to AED 100,000+ for a mainland business with multiple activities."
    st.write(response)

expander3 = st.expander("Can foreigners own 100% of a business in Dubai?")
with expander3:
    query = "Can foreigners own 100% of a business in Dubai?"
    context = get_dubai_info(query, st.session_state.vector_store)
    response = "Yes, foreigners can own 100% of a business in Dubai through several options: 1) Free Zone companies allow complete foreign ownership with the limitation of primarily operating within the free zone or internationally, 2) Since the 2020 Foreign Direct Investment Law reforms, mainland businesses in most sectors can have 100% foreign ownership without a local sponsor, with some strategic sectors excepted, 3) Offshore companies for holding assets and investments without UAE operations. The process typically involves choosing a jurisdiction, applying for the appropriate license, and meeting capitalization requirements."
    st.write(response)

expander4 = st.expander("What are the tax benefits of setting up a business in Dubai?")
with expander4:
    query = "What are the tax benefits of setting up a business in Dubai?"
    context = get_dubai_info(query, st.session_state.vector_store)
    response = "Dubai offers significant tax benefits for businesses: 1) 0% corporate tax until June 2023 (9% thereafter with exemptions for small businesses and free zones), 2) No personal income tax, 3) No capital gains tax, 4) Free zones offer 15-50 year tax holidays, 5) No withholding tax, 6) Extensive double taxation agreements with 100+ countries, 7) VAT is a relatively low 5%, with many exemptions. These incentives make Dubai highly attractive for businesses looking to optimize their tax position while maintaining a legitimate operational base."
    st.write(response)

# Business Inquiry Form
st.header("📋 Business Inquiry Form")
st.markdown("Have specific questions about starting or expanding your business in Dubai? Submit your inquiry below.")

# Create form for business inquiries
with st.form("business_inquiry_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    business_type = st.selectbox(
        "Business Type",
        ["Technology", "Finance", "Retail", "Manufacturing", "Services", "Healthcare", "Education", "Media", "Logistics", "Other"]
    )
    inquiry = st.text_area("Your Business Inquiry")
    submit_button = st.form_submit_button("Submit Inquiry")

# Display confirmation message if form is submitted
if submit_button:
    st.success("Thank you for your inquiry! Our business advisors will contact you within 48 hours.")
    # In a real application, this would send the inquiry to a database or email

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