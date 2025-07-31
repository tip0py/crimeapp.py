import streamlit as st
import time
import datetime
import random
import pandas as pd
import google.generativeai as genai

# Initialize the AI model (API key should be set via environment variable or Streamlit secrets)
# genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])  # Uncomment when you have API key configured
# model = genai.GenerativeModel('gemini-1.5-flash')

# Page configuration
st.set_page_config(
    page_title="SECURO - St. Kitts & Nevis Crime AI Assistant",
    page_icon="https://i.postimg.cc/V69LH7F4/Logo.jpg",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling - keeping the exact same design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&display=swap');
    /* ...existing CSS code... */
</style>
""", unsafe_allow_html=True)

# CSV data handling
@st.cache_data
def load_csv_data():
    """Load and cache CSV data"""
    csv_filename = "SecuroCrimeApp.csv"  # Your CSV filename
    try:
        df = pd.read_csv(csv_filename)
        return df
    except FileNotFoundError:
        st.error(f"❌ CSV file '{csv_filename}' not found. Please make sure it's in the same folder as this app.")
        return None
    except Exception as e:
        st.error(f"❌ Error loading CSV: {str(e)}")
        return None

# Load CSV into session state if not already loaded
if 'csv_data' not in st.session_state or st.session_state.csv_data is None:
    st.session_state.csv_data = load_csv_data()
if st.session_state.csv_data is not None:
    st.dataframe(st.session_state.csv_data.head())

def search_csv_data(df, query):
    """Search through CSV data for relevant information"""
    if df is None or df.empty:
        return "No CSV data loaded. Please upload a CSV file to search through crime data."
   
    search_term = query.lower()
    results = []
   
    # Search through all text columns
    for column in df.columns:
        if df[column].dtype == 'object':  # Text columns
            mask = df[column].astype(str).str.lower().str.contains(search_term, na=False)
            matching_rows = df[mask]
            if not matching_rows.empty:
                for _, row in matching_rows.iterrows():
                    results.append(f"Found in {column}: {row.to_dict()}")
   
    if results:
        return "\n\n".join(results[:3])  # Return top 3 results
    else:
        return f"No matches found for '{query}' in the uploaded crime data. Try different search terms."

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
    # Add initial bot message
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Welcome to SECURO, your AI crime investigation assistant for St. Kitts & Nevis law enforcement.\n\nI'm here to assist criminologists, police officers, forensic experts, and autopsy professionals with case analysis, evidence correlation, and investigative insights.\n\nPlease upload a CSV file with crime data to get started, then ask me questions about the data.\n\nHow can I assist with your investigation today?",
        "timestamp": datetime.datetime.now().strftime("%H:%M:%S")
    })

if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = "expanded"

# Header with sidebar toggle
col1, col2 = st.columns([1, 10])

with col1:
    if st.button("🔧", help="Toggle Sidebar", key="sidebar_toggle"):
        if st.session_state.sidebar_state == "expanded":
            st.session_state.sidebar_state = "collapsed"
        else:
            st.session_state.sidebar_state = "expanded"
        st.rerun()

with col2:
    st.markdown("""
    <div class="main-header">
        <div class="particles" id="particles"></div>
        <h1>SECURO</h1>
        <div class="tagline">AI Crime Investigation Assistant</div>
        <div class="location">🇰🇳 St. Kitts & Nevis Law Enforcement</div>
    </div>
    """, unsafe_allow_html=True)

# Particles animation script
st.markdown("""
<script>
function createParticles() {
    const particlesContainer = document.getElementById('particles');
    if (particlesContainer) {
        const particleCount = 40;
        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.animationDelay = Math.random() * 10 + 's';
            particle.style.animationDuration = (Math.random() * 10 + 15) + 's';
            particlesContainer.appendChild(particle);
        }
    }
}
createParticles();
</script>
""", unsafe_allow_html=True)

# Load CSV data status
st.markdown('<div class="section-header">📊 Crime Data Status</div>', unsafe_allow_html=True)

# Sidebar (only show if expanded)
if st.session_state.sidebar_state == "expanded":
    with st.sidebar:
        st.markdown('<div class="section-header">🚨 Emergency Contacts</div>', unsafe_allow_html=True)
        emergency_contacts = [
            {"name": "Emergency Hotline", "number": "911", "type": "police"},
            {"name": "Police Department", "number": "465-2241", "type": "police"},
            {"name": "Hospital", "number": "465-2551", "type": "hospital"},
            {"name": "Fire Department", "number": "465-2515 / 465-7167", "type": "fire"},
            {"name": "Coast Guard", "number": "465-8384 / 466-9280", "type": "legal"},
            {"name": "Red Cross", "number": "465-2584", "type": "forensic"},
            {"name": "NEMA (Emergency Mgmt)", "number": "466-5100", "type": "legal"}
        ]
        for contact in emergency_contacts:
            if st.button(f"📞 {contact['name']}\n{contact['number']}", key=contact['name']):
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"🚨 Emergency contact information accessed: {contact['name']} - {contact['number']}. Contact has been logged for case documentation.",
                    "timestamp": datetime.datetime.now().strftime("%H:%M:%S")
                })
                st.rerun()
        st.markdown('<div class="section-header">📍 Crime Hotspots Map</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="map-container crime-map">
            <iframe
                src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d243.44896!2d-62.7261!3d17.3026!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x8c1a602b153c94b5%3A0x8e3f7a7c7b1b9f5e!2sBasseterre%2C%20St%20Kitts%20%26%20Nevis!5e1!3m2!1sen!2sus!4v1634567890123!5m2!1sen!2sus&maptype=satellite"
                allowfullscreen=""
                loading="lazy"
                referrerpolicy="no-referrer-when-downgrade">
            </iframe>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="section-header">🎯 Active Crime Zones</div>', unsafe_allow_html=True)
        hotspots = [
            {"name": "Basseterre Downtown", "level": "🔴 High Risk", "coords": "17.3026, -62.7261"},
            {"name": "Sandy Point", "level": "🟡 Medium Risk", "coords": "17.3580, -62.8419"},
            {"name": "Charlestown (Nevis)", "level": "🟠 Active Cases", "coords": "17.1373, -62.6131"},
            {"name": "Frigate Bay", "level": "🟡 Tourist Area", "coords": "17.2742, -62.6897"}
        ]
        for hotspot in hotspots:
            if st.button(f"{hotspot['level']} {hotspot['name']}", key=f"hotspot_{hotspot['name']}"):
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"📍 Crime hotspot analysis: {hotspot['name']} ({hotspot['coords']})\n\n{hotspot['level']} - Recommend increased patrol presence and witness canvassing in this area. Coordinating with local units for enhanced surveillance.",
                    "timestamp": datetime.datetime.now().strftime("%H:%M:%S")
                })
                st.rerun()

# Main chat area
st.markdown('<div class="section-header">💬 Crime Investigation Chat</div>', unsafe_allow_html=True)

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <div class="message-content">{message["content"]}</div>
            <div class="message-time">{message["timestamp"]}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message bot-message">
            <div class="message-content">{message["content"]}</div>
            <div class="message-time">{message["timestamp"]}</div>
        </div>
        """, unsafe_allow_html=True)

# Chat input
col1, col2 = st.columns([5, 1])

with col1:
    user_input = st.text_input(
        "Message",
        placeholder="Ask questions about the uploaded crime data...",
        label_visibility="collapsed",
        key="user_input"
    )

with col2:
    if st.button("Send", type="primary"):
        if user_input:
            # Add user message
            st.session_state.messages.append({
                "role": "user",
                "content": user_input,
                "timestamp": datetime.datetime.now().strftime("%H:%M:%S")
            })
            # Generate response based on CSV data
            response = search_csv_data(st.session_state.csv_data, user_input)
            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
                "timestamp": datetime.datetime.now().strftime("%H:%M:%S")
            })
            st.rerun()

# Status bar
st.markdown("""
<div class="status-bar">
    <div class="status-item">
        <div class="status-dot status-online"></div>
        <span>SECURO AI Online</span>
    </div>
    <div class="status-item">
        <div class="status-dot status-processing"></div>
        <span>CSV Data Ready</span>
    </div>
    <div class="status-item">
        <div class="status-dot status-evidence"></div>
        <span>Emergency Services Linked</span>
    </div>
</div>
""", unsafe_allow_html=True)
