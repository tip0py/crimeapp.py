import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import hashlib
import json
import os
import random

# Page configuration
st.set_page_config(
    page_title="SECURO - Crime Analysis System",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark crime theme
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d1b1b 50%, #1a1a1a 100%);
        font-family: 'Times New Roman', serif;
    }
    
    .main-header {
        background: linear-gradient(90deg, #8B0000, #2F4F4F, #8B0000);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
        border: 2px solid #8B0000;
    }
    
    .main-title {
        font-size: 4rem;
        font-weight: bold;
        color: #FF6B6B;
        text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.8);
        margin-bottom: 0.5rem;
        font-family: 'Times New Roman', serif;
        letter-spacing: 3px;
    }
    
    .subtitle {
        font-size: 1.5rem;
        color: #CCCCCC;
        font-family: 'Times New Roman', serif;
        font-style: italic;
    }
    
    .auth-container {
        background: rgba(20, 20, 20, 0.9);
        padding: 2rem;
        border-radius: 15px;
        border: 2px solid #8B0000;
        box-shadow: 0 8px 32px rgba(139, 0, 0, 0.3);
        margin: 2rem 0;
    }
    
    .chat-container {
        background: rgba(20, 20, 20, 0.95);
        border-radius: 15px;
        border: 2px solid #8B0000;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.5);
    }
    
    .user-message {
        background: linear-gradient(135deg, #2F4F4F, #1C1C1C);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #FF6B6B;
        font-family: 'Times New Roman', serif;
    }
    
    .bot-message {
        background: linear-gradient(135deg, #8B0000, #2F1B1B);
        color: #CCCCCC;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #FFD700;
        font-family: 'Times New Roman', serif;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #8B0000, #A52A2A);
        color: white;
        border: 2px solid #FF6B6B;
        border-radius: 10px;
        font-family: 'Times New Roman', serif;
        font-size: 1.1rem;
        font-weight: bold;
        padding: 0.5rem 2rem;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #A52A2A, #DC143C);
        border-color: #FFD700;
    }
    
    .stTextInput > div > div > input {
        background: rgba(20, 20, 20, 0.8);
        color: white;
        border: 2px solid #8B0000;
        border-radius: 8px;
        font-family: 'Times New Roman', serif;
    }
    
    .stSelectbox > div > div > select {
        background: rgba(20, 20, 20, 0.8);
        color: white;
        border: 2px solid #8B0000;
        font-family: 'Times New Roman', serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #FF6B6B !important;
        font-family: 'Times New Roman', serif !important;
    }
    
    .stMarkdown {
        color: #CCCCCC;
        font-family: 'Times New Roman', serif;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #2F4F4F, #1a1a1a);
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #8B0000;
        margin: 0.5rem 0;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Load Q&A data from CSV structure
@st.cache_data
def load_qa_data():
    qa_data = {
        'Criminology': {
            'What are the main theories of criminal behavior?': 'The main theories include: Classical Theory (rational choice), Biological Theory (genetic/physiological factors), Psychological Theory (personality disorders, mental illness), Sociological Theory (social environment, strain theory), and Integrated Theories that combine multiple approaches.',
            'How does social disorganization theory explain crime rates?': 'Social disorganization theory suggests that crime rates are higher in communities lacking social cohesion, informal social controls, and collective efficacy. Factors include residential mobility, ethnic heterogeneity, poverty, and weak social institutions.'
        },
        'Forensics': {
            'What is the difference between class and individual evidence?': 'Class evidence can only narrow down the source to a group (e.g., blood type, fiber type), while individual evidence can theoretically be traced to a single source with high certainty (e.g., DNA, fingerprints, tool marks).',
            'How long can DNA evidence remain viable?': 'DNA can remain viable for decades or even centuries under proper conditions. Factors affecting degradation include temperature, humidity, UV exposure, and bacterial contamination.'
        },
        'Investigation': {
            'What are the key principles of crime scene management?': 'Key principles include: secure and protect the scene, establish a perimeter, document everything before collection, maintain chain of custody, systematic search patterns, minimize contamination, and coordinate with specialists.',
            'How do you conduct an effective witness interview?': 'Best practices: establish rapport, use open-ended questions initially, listen actively, avoid leading questions, document thoroughly, be aware of memory limitations, consider cultural factors, and follow up for clarification.'
        }
    }
    return qa_data

# Simple authentication functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password, user_type):
    users_file = 'securo_users.json'
    users = {}
    
    if os.path.exists(users_file):
        try:
            with open(users_file, 'r') as f:
                users = json.load(f)
        except:
            users = {}
    
    if username in users:
        return False
    
    users[username] = {
        'password': hash_password(password),
        'user_type': user_type,
        'created_at': datetime.now().isoformat()
    }
    
    try:
        with open(users_file, 'w') as f:
            json.dump(users, f)
        return True
    except:
        return False

def authenticate(username, password):
    users_file = 'securo_users.json'
    if not os.path.exists(users_file):
        return None
    
    try:
        with open(users_file, 'r') as f:
            users = json.load(f)
        
        if username in users:
            if users[username]['password'] == hash_password(password):
                return users[username]['user_type']
    except:
        pass
    
    return None

# Chat response function
def get_chat_response(user_input, user_type):
    qa_data = load_qa_data()
    user_input_lower = user_input.lower()
    
    # Search through Q&A data
    for category, questions in qa_data.items():
        for question, answer in questions.items():
            if any(word in user_input_lower for word in question.lower().split()[:3]):
                return f"**[{category}]** {answer}"
    
    # General responses
    if any(word in user_input_lower for word in ['hello', 'hi', 'hey', 'greetings']):
        return f"🕵🏿‍♂️ Greetings, Agent. I am SECURO, your crime analysis assistant for St. Kitts and Nevis. How may I assist with your investigation today?"
    
    elif 'crime statistics' in user_input_lower or 'statistics' in user_input_lower:
        return "📊 I can provide detailed crime statistics for St. Kitts and Nevis. Please check the Analytics section for comprehensive charts and trends."
    
    elif 'hotspot' in user_input_lower or 'map' in user_input_lower:
        return "🗺️ Crime hotspot mapping is available. I can show you high-risk areas across all parishes of St. Kitts and Nevis."
    
    elif 'forensic' in user_input_lower or 'evidence' in user_input_lower:
        return "🔬 Forensic analysis capabilities include DNA evidence evaluation, fingerprint analysis, digital forensics, and evidence chain management. What specific forensic assistance do you need?"
    
    else:
        return "🤔 I'm analyzing your query. Please be more specific about the type of criminal investigation assistance you need, or ask about forensics, crime statistics, hotspots, or investigative procedures."

# Generate sample crime data
@st.cache_data
def generate_crime_data():
    parishes = ['Saint George Basseterre', 'Saint John Capesterre', 'Saint Anne Sandy Point', 
                'Saint Paul Capesterre', 'Saint Peter Basseterre', 'Saint Thomas Middle Island']
    crime_types = ['Theft', 'Assault', 'Burglary', 'Drug Offenses', 'Vandalism', 'Fraud']
    
    data = []
    for i in range(200):
        data.append({
            'Date': pd.date_range('2023-01-01', '2024-12-31', freq='D')[i % 365],
            'Parish': random.choice(parishes),
            'Crime_Type': random.choice(crime_types),
            'Severity': random.choice(['Low', 'Medium', 'High']),
            'Status': random.choice(['Open', 'Closed', 'Under Investigation'])
        })
    
    return pd.DataFrame(data)

# Main function
def main():
    # Display header
    st.markdown("""
    <div class="main-header">
        <div class="main-title">🕵🏿‍♂️ SECURO 🕵🏿‍♀️</div>
        <div class="subtitle">Crime Analysis & Forensic Intelligence System</div>
        <div class="subtitle">🇰🇳 St. Kitts and Nevis Division 🇰🇳</div>
    </div>
    """, unsafe_allow_html=True)

    # Check for crime board image
    image_files = "crime_board_image.jpg"
    for img_file in image_files:
        if os.path.exists(img_file):
            st.image(img_file, use_column_width=True)
            break

    # Authentication section
    if not st.session_state.authenticated:
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown('<div class="auth-container">', unsafe_allow_html=True)
            
            tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])
            
            with tab1:
                st.markdown("### Agent Login")
                username = st.text_input("Username", key="login_username")
                password = st.text_input("Password", type="password", key="login_password")
                
                if st.button("Access System", key="login_btn"):
                    if username and password:
                        user_type = authenticate(username, password)
                        if user_type:
                            st.session_state.authenticated = True
                            st.session_state.user_type = user_type
                            st.session_state.username = username
                            st.success(f"🎯 Access Granted, Agent {username}")
                            st.rerun()
                        else:
                            st.error("❌ Access Denied - Invalid Credentials")
                    else:
                        st.error("Please enter both username and password")
            
            with tab2:
                st.markdown("### New Agent Registration")
                new_username = st.text_input("Choose Username", key="reg_username")
                new_password = st.text_input("Create Password", type="password", key="reg_password")
                user_type = st.selectbox(
                    "Access Level",
                    ["Public", "Police Officer", "Forensic Specialist", "Criminologist", "Administrator"]
                )
                
                if st.button("Register Agent", key="reg_btn"):
                    if new_username and new_password:
                        if create_user(new_username, new_password, user_type):
                            st.success("✅ Agent Registration Complete - You can now login")
                        else:
                            st.error("❌ Username already exists or registration failed")
                    else:
                        st.error("Please fill in all fields")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        # Main application interface
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"### 🎯 Welcome back, Agent {st.session_state.username}")
            st.markdown(f"**Access Level:** {st.session_state.user_type}")
            
            # Chat interface
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            st.markdown("### 💬 SECURO Intelligence Chat")
            
            # Display chat history
            for message in st.session_state.chat_history:
                if message['role'] == 'user':
                    st.markdown(f'<div class="user-message">👤 **You:** {message["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="bot-message">🤖 **SECURO:** {message["content"]}</div>', unsafe_allow_html=True)
            
            # Chat input
            user_input = st.text_input("Ask SECURO about forensics, crime analysis, or investigations:", key="chat_input")
            
            if st.button("Send Query", key="send_btn"):
                if user_input:
                    # Add user message
                    st.session_state.chat_history.append({"role": "user", "content": user_input})
                    
                    # Get bot response
                    response = get_chat_response(user_input, st.session_state.user_type)
                    st.session_state.chat_history.append({"role": "bot", "content": response})
                    
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            # User info
            st.markdown("### 👤 Agent Profile")
            st.write(f"**Agent:** {st.session_state.username}")
            st.write(f"**Clearance:** {st.session_state.user_type}")
            st.write(f"**Status:** 🟢 Active")
            
            # Quick stats
            st.markdown("### 📊 Quick Stats")
            crime_data = generate_crime_data()
            
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Cases", len(crime_data))
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            open_cases = len(crime_data[crime_data['Status'] == 'Open'])
            st.metric("Open Cases", open_cases)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Analytics section (restricted for some users)
            if st.session_state.user_type != 'Public':
                st.markdown("### 📈 Crime Analytics")
                
                if st.button("View Crime Trends"):
                    monthly_data = crime_data.groupby(crime_data['Date'].dt.month).size().reset_index(name='count')
                    monthly_data['Date'] = monthly_data['Date']
                    
                    fig = px.line(
                        monthly_data,
                        x='Date', y='count',
                        title="Monthly Crime Trends",
                        color_discrete_sequence=['#FF6B6B']
                    )
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_color='white'
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            # Logout
            st.markdown("---")
            if st.button("🚪 Logout", key="logout_btn"):
                st.session_state.authenticated = False
                st.session_state.user_type = None
                st.session_state.username = None
                st.session_state.chat_history = []
                st.rerun()

if __name__ == "__main__":
    main()
