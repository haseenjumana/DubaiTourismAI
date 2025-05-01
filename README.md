# 🌆 Dubai Tourism & Business AI Assistant

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url-here.streamlit.app) [![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/) [![OpenAI](https://img.shields.io/badge/AI-OpenAI-brightgreen.svg)](https://openai.com/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![FAISS](https://img.shields.io/badge/Vector%20Search-FAISS-orange.svg)](https://github.com/facebookresearch/faiss) [![ElevenLabs](https://img.shields.io/badge/TTS-ElevenLabs-purple.svg)](https://elevenlabs.io/)

## 🌟 Overview

The **Dubai Tourism & Business AI Assistant** is an enterprise-grade, multilingual virtual concierge providing authoritative information about Dubai's tourism attractions and business landscape. Leveraging OpenAI's GPT-4o technology with vector-based knowledge retrieval, this application delivers accurate, context-aware information for tourists and business professionals navigating Dubai's diverse offerings and regulatory requirements.

<p align="center">
  <img src="generated-icon.png" alt="Dubai AI Assistant" width="250"/>
</p>

## ✨ Key Features

### 🌐 Interactive Experience
- **Advanced Multilingual Support** - Seamlessly interact in 3 languages ( Arabic, English and hindi)
- **Voice Interaction System** - Engage with natural voice conversations using ElevenLabs' realistic text-to-speech technology
- **Context-Aware Responses** - Receive intelligent, contextually relevant information that builds upon previous exchanges

### 🏙️ Dubai Tourism Expertise
- **Comprehensive Attraction Database** - Access detailed information on Dubai's iconic landmarks, hidden gems, and seasonal events
- **Local Transportation Guide** - Navigate Dubai's metro, tram, bus, and taxi systems with ease
- **Cultural Insights** - Learn about local customs, etiquette, and cultural sensitivities
- **Visa & Travel Requirements** - Get up-to-date information on tourist visa processes and entry requirements

### 💼 Business Intelligence
- **Free Zone Analysis** - Compare Dubai's 30+ free zones with specialized recommendations by industry
- **Licensing & Regulatory Guidance** - Navigate Dubai's business setup process with step-by-step instructions
- **Market Opportunity Insights** - Access sector-specific market analysis and growth opportunities
- **Networking Recommendations** - Discover relevant business events, conferences, and networking opportunities

## 🛠️ Technology Stack

### Core Technologies
- **Streamlit** - Enterprise-grade web application framework for rapid deployment
- **OpenAI GPT-4o** - State-of-the-art language model with conversational capabilities
- **FAISS** - Facebook AI's vector similarity search for efficient information retrieval
- **ElevenLabs** - Premium text-to-speech API for natural voice interactions

### Architecture Components
- **Vector Knowledge Base** - Pre-indexed information about Dubai for instant retrieval
- **Multi-Stage Response Generation** - Context-aware AI reasoning with factual grounding
- **Enhanced Error Recovery** - Robust handling of API failures and network interruptions
- **Adaptive User Interface** - Responsive design optimized for mobile and desktop experience

## 📒 Project Structure

```
.
├── app.py                   # Main application entry point with UI components
├── pages/                   # Multi-page Streamlit app structure
│   ├── 1_Business.py        # Business information & setup guidance
│   ├── 2_Tourism.py         # Tourism attractions & travel advice
│   └── 3_About.py           # Project info & technology explanation
├── utils/                   # Core functionality modules
│   ├── audio_utils.py       # Voice processing with ElevenLabs integration
│   ├── language_utils.py    # Translation & language detection services
│   ├── model_utils.py       # OpenAI API integration & prompt engineering
│   └── vector_store.py      # FAISS vector search & knowledge retrieval
├── data/                    # Structured Dubai information
│   ├── attractions.json     # Tourism locations with metadata
│   ├── business_zones.json  # Free zone details and requirements
│   ├── regulations.json     # Business licensing information
│   └── transport.json       # Public transportation options
├── assets/                  # Static media resources
│   ├── images/              # UI images and attraction photos
│   └── audio/               # Pre-recorded audio snippets
├── .streamlit/              # Streamlit configuration
│   └── config.toml          # App settings for local & cloud deployment
├── requirements.txt         # Project dependencies
├── .env.example            # Template for environment variables
└── README.md               # Project documentation
```

The multi-page architecture separates business and tourism information for improved user experience, while utility modules handle specialized functions like language processing, voice synthesis, and vector-based information retrieval.

## 🔧 Setup Instructions

### Prerequisites

- Python 3.9+ with pip
- OpenAI API key ([Get one here](https://platform.openai.com/))
- ElevenLabs API key (optional, for voice features - [Get one here](https://elevenlabs.io/))
- Git (for cloning the repository)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/haseenjumana/dubai-tourism-ai.git
   cd dubai-tourism-ai
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up API keys**
   - Create a `.env` file in the project root with the following content:
     ```
     OPENAI_API_KEY=your_openai_api_key
     ELEVEN_LABS_API_KEY=your_elevenlabs_api_key
     ```
   - Alternatively, you can create a `.streamlit/secrets.toml` file:
     ```toml
     [openai]
     api_key = "your-openai-api-key"
     
     [elevenlabs]
     api_key = "your-elevenlabs-api-key"
     ```

5. **Initialize the vector store (first run only)**
   ```bash
   python -c "from utils.vector_store import initialize_vector_store; initialize_vector_store()"
   ```

6. **Launch the application**
   ```bash
   streamlit run app.py
   ```
   
7. **Access the web interface**
   Open your browser and navigate to http://localhost:8501

## 🛠 Deployment

### Streamlit Cloud Deployment

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Set up deployment on Streamlit Cloud**
   - Sign in to [Streamlit Cloud](https://streamlit.io/cloud)
   - Click "New app" and connect your GitHub repository
   - Select the main branch and the app.py file
   - Under Advanced Settings, ensure:
     - Python version is set to 3.9 or higher
     - No custom port parameters in the command

3. **Configure secrets in Streamlit Cloud**
   - In your app's settings, navigate to "Secrets"
   - Add your API keys in this exact format:
     ```toml
     [openai]
     api_key = "your-openai-api-key"
     
     [elevenlabs]
     api_key = "your-elevenlabs-api-key"
     ```

4. **Deploy the application**
   - Click "Deploy" and wait for the build process to complete
   - Streamlit Cloud will automatically generate a URL for your app

> **Important**: Always use `streamlit run app.py` without custom port parameters on Streamlit Cloud. Custom port settings can cause deployment failures.

Refer to [STREAMLIT_CLOUD_DEPLOYMENT.md](STREAMLIT_CLOUD_DEPLOYMENT.md) for detailed troubleshooting and advanced deployment options.

## 👮‍♂️ Security Considerations

- **API Key Protection**: Never commit API keys to your repository
- **Environment Variables**: Use `.env` files locally and Streamlit Secrets in production
- **Access Control**: Consider implementing user authentication for sensitive business information
- **Data Validation**: Always validate user inputs to prevent injection attacks

Security guidelines are detailed in [SECRETS_SECURITY.md](SECRETS_SECURITY.md).

## 💪 Contributing

We welcome contributions to the Dubai Tourism & Business AI Assistant! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-amazing-feature
   ```
3. **Make your changes** and add appropriate tests
4. **Run tests** to ensure your changes don't break existing functionality
5. **Commit your changes**:
   ```bash
   git commit -m "Add some amazing feature"
   ```
6. **Push to your branch**:
   ```bash
   git push origin feature/your-amazing-feature
   ```
7. **Create a Pull Request**

Please ensure your code follows the project's coding standards and includes appropriate documentation.

## 🔐 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🌟 Acknowledgements

- **Data Sources**:
  - [Visit Dubai](https://www.visitdubai.com/) - Official tourism portal
  - [Dubai Department of Economy and Tourism](https://www.dubaidet.ae/) - Business setup information
  - [Dubai Free Zones Council](https://www.dfzc.ae/) - Free zone regulatory details

- **Technology Partners**:
  - [OpenAI](https://openai.com/) - For the GPT-4o language model powering conversations
  - [ElevenLabs](https://elevenlabs.io/) - For realistic text-to-speech voice synthesis
  - [Streamlit](https://streamlit.io/) - For the web application framework
  - [Facebook AI Research](https://ai.facebook.com/) - For the FAISS vector similarity search library

- **Special Thanks**:
  - The global developer community for their contributions to open-source libraries
  - All beta testers who provided valuable feedback during development

---

<p align="center">
  <i>Bringing the best of Dubai to the world through intelligent AI assistance.</i>
</p>










































