import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
from langdetect import detect

# Language detection helper

def detect_language(text):
"""
Detects the primary language of the input text.
Classifies as Hindi ('hi'), English ('en'), or Hinglish (default/error).
"""
try:
lang = detect(text)
if lang == 'hi':
return 'Hindi'
elif lang == 'en':
return 'English'
else:
return 'Hinglish'
except:
return 'Hinglish'

# --- API Key Configuration ---

# Load environment variables from .env file

load_dotenv()

# CRITICAL FIX: The API key is now correctly loaded using the environment variable name

# "GEMINI_API_KEY" as specified in the README.

api_key = os.getenv("GEMINI_API_KEY")

# Configure the Gemini API client

if api_key:
genai.configure(api_key=api_key)
else: # Use a placeholder message or exit gracefully if key is missing
st.error("🚨 Configuration Error: GEMINI_API_KEY not found. Please add it to your .env file or Streamlit secrets.")

# Streamlit page setup

st.set_page_config(
page_title="YojanaSaathi - Government Schemes Assistant",
page_icon="🇮🇳",
layout="wide",
initial_sidebar_state="expanded"
)

# Custom CSS for WhatsApp-like styling and Inter font

st.markdown("""

<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main app background */
    .stApp {
        background: #f0f2f5;
    }
    
    /* Main container styling */
    .main {
        padding: 0 1rem;
        background: #f0f2f5;
    }
    
    /* Header styling - WhatsApp inspired */
    .header-container {
        background: #128c7e;
        padding: 1.5rem 0;
        border-radius: 0;
        margin-bottom: 1rem;
        text-align: center;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .header-title {
        font-family: 'Inter', sans-serif;
        font-size: 2.5rem;
        font-weight: 600;
        color: white;
        margin: 0;
    }
    
    .header-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        color: rgba(255,255,255,0.9);
        margin-top: 0.5rem;
        font-weight: 400;
    }
    
    /* Status card styling */
    .status-card {
        background: #dcf8c6;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border: none;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .status-text {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        color: #054740;
        margin: 0;
        font-weight: 400;
    }
    
    /* Chat message styling - WhatsApp style */
    .user-message {
        background: #dcf8c6;
        color: #054740;
        padding: 0.8rem 1.2rem;
        border-radius: 18px 18px 4px 18px;
        margin: 0.5rem 0;
        max-width: 70%;
        margin-left: auto;
        font-family: 'Inter', sans-serif;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        position: relative;
    }
    
    .assistant-message {
        background: white;
        color: #303030;
        padding: 0.8rem 1.2rem;
        border-radius: 18px 18px 18px 4px;
        margin: 0.5rem 0;
        max-width: 70%;
        margin-right: auto;
        font-family: 'Inter', sans-serif;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        position: relative;
    }
    
    /* Sidebar styling - White and Green Theme */
    .css-1d391kg {
        background: white !important;
        border-right: 2px solid #128c7e !important;
    }
    
    .sidebar .sidebar-content {
        background: white !important;
        color: #303030 !important;
    }
    
    /* Sidebar header styling */
    .stSidebar > div:first-child {
        background: white !important;
    }
    
    .stSidebar .stMarkdown {
        background: white !important;
    }
    
    /* Input styling - White and Green Theme */
    .stChatInput {
        background: white !important;
        border: 2px solid #128c7e !important;
        border-radius: 25px !important;
        padding: 0.8rem 1.5rem !important;
        font-family: 'Inter', sans-serif !important;
        box-shadow: 0 2px 10px rgba(18, 140, 126, 0.1) !important;
    }
    
    .stChatInput:focus {
        border-color: #128c7e !important;
        box-shadow: 0 0 0 3px rgba(18, 140, 126, 0.2) !important;
    }
    
    /* Input container styling */
    .stChatInputContainer {
        background: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.5rem !important;
        margin: 1rem 0 !important;
        box-shadow: 0 2px 10px rgba(18, 140, 126, 0.1) !important;
    }
    
    /* Input text styling */
    .stChatInput input {
        background: white !important;
        color: #303030 !important;
        border: none !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
    }
    
    .stChatInput input::placeholder {
        color: #128c7e !important;
        opacity: 0.7 !important;
    }
    
    /* Send button styling */
    .stChatInput button {
        background: #128c7e !important;
        color: white !important;
        border: none !important;
        border-radius: 50% !important;
        width: 40px !important;
        height: 40px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.3s ease !important;
    }
    
    .stChatInput button:hover {
        background: #0f7a6e !important;
        transform: scale(1.05) !important;
    }
    
    /* Quick tips card - Enhanced styling */
    .tips-card {
        background: white;
        padding: 1.2rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(18, 140, 126, 0.1);
        border: 1px solid rgba(18, 140, 126, 0.1);
        border-left: 4px solid #128c7e;
    }
    
    .tip-item {
        color: #54656f;
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        margin: 0.5rem 0;
        line-height: 1.4;
        padding: 0.3rem 0;
        border-bottom: 1px solid rgba(18, 140, 126, 0.05);
    }
    
    .tip-item:last-child {
        border-bottom: none;
    }
    
    /* Sidebar title styling */
    .sidebar-title {
        background: linear-gradient(135deg, #128c7e 0%, #0f7a6e 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(18, 140, 126, 0.2);
    }
    
    .sidebar-title h3 {
        margin: 0;
        font-weight: 600;
        font-size: 1.2rem;
    }
    
    .sidebar-title p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
        font-size: 0.85rem;
    }
    
    /* Spinner styling */
    .stSpinner {
        text-align: center;
        color: #128c7e;
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    
    /* Welcome message styling */
    .welcome-message {
        text-align: center;
        padding: 2rem 1rem;
        color: #54656f;
        background: white;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(18, 140, 126, 0.1);
        border: 1px solid rgba(18, 140, 126, 0.1);
    }
    
    /* Enhanced input area */
    .input-area {
        background: white;
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(18, 140, 126, 0.1);
        border: 1px solid rgba(18, 140, 126, 0.1);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .header-title {
            font-size: 2rem;
        }
        
        .user-message, .assistant-message {
            max-width: 85%;
        }
        
        .tips-card {
            padding: 1rem;
        }
    }
</style>

""", unsafe_allow_html=True)

# Load scheme documents

def load_scheme_documents(folder_path="schemes"):
"""
Loads all .txt files from the specified folder into a single context string.
Note: Requires a 'schemes' directory with .txt files to run successfully.
"""
all_text = ""
try: # Check if the folder exists
if not os.path.isdir(folder_path):
st.warning(f"⚠️ Scheme documents folder '{folder_path}' not found. Using empty context.")
return ""

        for filename in os.listdir(folder_path):
            if filename.endswith(".txt"):
                # Use os.path.join for platform independence
                file_path = os.path.join(folder_path, filename)
                with open(file_path, "r", encoding="utf-8") as file:
                    all_text += file.read() + "\n"
        return all_text.strip()
    except Exception as e:
        # Catch exceptions during file reading
        st.error(f"❌ Error loading scheme document: {filename if 'filename' in locals() else 'Unknown File'}")
        st.exception(e)
        return ""

context = load_scheme_documents()

# Gemini response function

def get_gemini_response(user_query, context):
"""
Generates a response from the Gemini model based on user query and scheme context.
The response language is dynamically set based on the user's query language.
""" # Check if the API is configured before calling the model
if not api_key:
return "Sorry, the API key is not configured. Please check the setup."

    model = genai.GenerativeModel("gemini-1.5-flash")

    # Detect language of the query
    user_lang = detect_language(user_query)

    # Updated prompt with explicit language instruction for consistency
    prompt = f"""

You are YojanaSaathi, an assistant that helps Indian citizens understand government welfare schemes.

Use the following scheme information to answer clearly, simply, and in the same language as the user's question.

The user has asked their question in **{user_lang}**, so respond only in **{user_lang}**, using natural expressions in that language. Do not switch languages mid-answer.

Context:
{context}

Question:
{user_query}

Answer:"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        # Handle potential API errors (e.g., authentication, rate limiting)
        print(f"Gemini API Error: {e}")
        return "माफ़ करना, मैं अभी जवाब नहीं दे पा रहा हूँ। कृपया कुछ देर बाद फिर से कोशिश करें या अपनी API key की जांच करें। (Sorry, I cannot answer right now. Please try again later or check your API key.)"

# Initialize chat history

if "chat_history" not not st.session_state:
st.session_state.chat_history = []

# Sidebar with enhanced styling

with st.sidebar:
st.markdown("""

<div class="sidebar-title">
<h3>🇮🇳 YojanaSaathi</h3>
<p>Government Schemes Assistant</p>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
    <div class="tips-card">
        <h4 style="color: #128c7e; font-family: 'Inter', sans-serif; margin-bottom: 1rem; font-size: 1rem;">💡 Quick Tips</h4>
        <div class="tip-item">• You can ask in Hindi, English, or Hinglish</div>
        <div class="tip-item">• Be specific about your situation (age, income, location)</div>
        <div class="tip-item">• Ask about eligibility, benefits, or application process</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="tips-card">
        <h4 style="color: #128c7e; font-family: 'Inter', sans-serif; margin-bottom: 1rem; font-size: 1rem;">❓ Example Questions</h4>
        <div class="tip-item">Papa 65 ke ho gaye hain, pension milegi kya?</div>
        <div class="tip-item">What are the benefits of PM-KISAN?</div>
        <div class="tip-item">Ayushman Bharat ke liye kaise apply karu?</div>
    </div>
    """, unsafe_allow_html=True)

# Main content area

col1, col2, col3 = st.columns([1, 8, 1])

with col2: # Header
st.markdown("""

<div class="header-container">
<h1 class="header-title">🇮🇳 YojanaSaathi</h1>
<p class="header-subtitle">आपका AI साथी Government Schemes के लिए</p>
</div>
""", unsafe_allow_html=True)

    # Status card
    if api_key:
        status_message = "✅ Assistant तैयार है! अब पूछिए कुछ भी about government schemes"
    else:
        status_message = "🔴 Assistant अभी निष्क्रिय है (API Key missing/incorrect)."

    st.markdown(f"""
    <div class="status-card">
        <p class="status-text">{status_message}</p>
    </div>
    """, unsafe_allow_html=True)

    # Show chat history
    if st.session_state.chat_history:
        for q, a in st.session_state.chat_history:
            # Use columns to align chat bubbles (optional but common practice in Streamlit chat apps)
            user_col, _ = st.columns([7, 3])
            with user_col:
                st.markdown(f"""
                <div class="user-message">
                    <strong>🧑 आपका सवाल:</strong><br>{q}
                </div>
                """, unsafe_allow_html=True)

            _, assistant_col = st.columns([3, 7])
            with assistant_col:
                st.markdown(f"""
                <div class="assistant-message">
                    <strong>🤖 YojanaSaathi का जवाब:</strong><br>{a}
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="welcome-message">
            <h3 style="color: #128c7e; margin-bottom: 1rem;">👋 नमस्ते! मैं YojanaSaathi हूं</h3>
            <p style="margin: 0;">Government schemes के बारे में कुछ भी पूछिए। मैं Hindi, English, और Hinglish में जवाब दे सकता हूं।</p>
        </div>
        """, unsafe_allow_html=True)

# Enhanced Chat input area

st.markdown('<div class="input-area">', unsafe_allow_html=True)
query = st.chat_input("🗣️ पूछिए कुछ भी (जैसे: 'Papa 65 के हो गये हैं, pension मिलेगी क्या?')")
st.markdown('</div>', unsafe_allow_html=True)

if query and api_key: # Add user message to chat history immediately
st.session_state.chat_history.append((query, ""))

    # Show user message
    st.markdown(f"""
    <div class="user-message">
        <strong>🧑 आपका सवाल:</strong><br>{query}
    </div>
    """, unsafe_allow_html=True)

    # Show thinking spinner
    with st.spinner("🔍 सोच रहे हैं... कृपया प्रतीक्षा करें"):
        response = get_gemini_response(query, context)

    # Show assistant response
    st.markdown(f"""
    <div class="assistant-message">
        <strong>🤖 YojanaSaathi का जवाब:</strong><br>{response}
    </div>
    """, unsafe_allow_html=True)

    # Update the last entry in chat history with the response
    st.session_state.chat_history[-1] = (query, response)

    # Rerun to update the display
    st.rerun()

elif query and not api_key: # Handle chat input if API key is missing
st.error("Cannot process query: API Key is missing. Please configure GEMINI_API_KEY.")

# Footer

st.markdown("""

<div style="text-align: center; padding: 1.5rem 0; color: #54656f; font-family: 'Inter', sans-serif; font-size: 0.9rem;">
    <p>Made with ❤️ for भारत | Empowering citizens through AI</p>
</div>
""", unsafe_allow_html=True)
