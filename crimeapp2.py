import streamlit as st
import datetime
import json
import requests
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static
import hashlib
import time
import os

# Uncomment if you want PDF support later
# import PyPDF2

st.set_page_config(
    page_title="SECURO - Criminology Intelligence Assistant",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ======== CSS (keep your existing styles) ========
st.markdown("""
<style>
    /* (Your entire CSS from the original code here) */
    /* I’ll omit for brevity but include it exactly as you have it */
</style>
""", unsafe_allow_html=True)

# ======== User Authentication ========
class UserAuthentication:
    def __init__(self):
        if "users_db" not in st.session_state:
            st.session_state.users_db = {}
       
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
   
    def create_account(self, username, password, role):
        if username in st.session_state.users_db:
            return False, "Username already exists"
        if len(password) < 6:
            return False, "Password must be at least 6 characters"
        st.session_state.users_db[username] = {
            "password": self.hash_password(password),
            "role": role,
            "created": datetime.datetime.now().isoformat()
        }
        return True, "Account created successfully"
   
    def login(self, username, password):
        if username not in st.session_state.users_db:
            return False, "Username not found"
        if st.session_state.users_db[username]["password"] != self.hash_password(password):
            return False, "Invalid password"
        st.session_state.logged_in = True
        st.session_state.current_user = username
        st.session_state.user_role = st.session_state.users_db[username]["role"]
        return True, "Login successful"

# ======== GeminiAPI (placeholder for your AI provider) ========
class GeminiAPI:
    def __init__(self):
        # Replace with your real API key or service
        self.api_key = "YOUR_API_KEY_HERE"
       
    def get_gemini_response(self, prompt):
        # For now, just echo prompt or dummy response for demo
        # Replace this with your real API call
        return f"SECURO Response based on your query:\n\n{prompt[:500]}..."

# ======== Main Chatbot class ========
class CriminologyIntelligenceBot:
    def __init__(self):
        self.crime_data = self.load_real_crime_data()
        self.gemini_api = GeminiAPI()

        self.emergency_contacts = {
            "police": {
                "name": "Royal St. Christopher and Nevis Police Force",
                "number": "911",
                "alternative": "(869) 465-2241",
                "warning": "⚠️ **EMERGENCY POLICE CONTACT** ⚠️\n\nYou are about to contact the police emergency services.\n\nUse 911 for immediate emergencies."
            },
            "hospital": {
                "name": "Joseph N. France General Hospital",
                "number": "911",
                "alternative": "(869) 465-2551",
                "warning": "🏥 **EMERGENCY MEDICAL CONTACT** 🏥\n\nYou are about to contact emergency medical services.\n\nUse 911 for medical emergencies."
            },
            "fire": {
                "name": "Fire and Rescue Services",
                "number": "911",
                "alternative": "(869) 465-2366",
                "warning": "🚒 **EMERGENCY FIRE & RESCUE CONTACT** 🚒\n\nYou are about to contact fire and rescue services.\n\nUse 911 for fire emergencies."
            }
        }

    def load_real_crime_data(self):
        data_path = os.path.join("data", "crime_stats.json")
        if os.path.exists(data_path):
            with open(data_path, "r") as f:
                return json.load(f)
        else:
            return {}

    # Optional PDF loader for future use
    # def load_crime_report_pdf(self, filename="2023_Annual_Crime_Report.pdf"):
    #     data_path = os.path.join("data", filename)
    #     if os.path.exists(data_path):
    #         with open(data_path, "rb") as f:
    #             reader = PyPDF2.PdfReader(f)
    #             text = ""
    #             for page in reader.pages:
    #                 text += page.extract_text()
    #             return text
    #     return "No PDF report found."

    def create_criminology_prompt(self, user_input):
        stats_2024 = self.crime_data.get("2024", {})
        homicides = stats_2024.get("homicide", "N/A")
        assaults = stats_2024.get("assault", "N/A")
        clearance = stats_2024.get("clearance_rate", "N/A")

        prompt = f"""
You are SECURO, an AI Criminology Assistant specialized in St. Kitts & Nevis.

Key Stats (2024):
- Homicides: {homicides}
- Assaults: {assaults}
- Clearance Rate: {clearance}

User Query:
{user_input}

Please provide an expert criminology response contextualized for St. Kitts & Nevis.
"""
        return prompt

    def create_crime_chart(self, year="2024"):
        if year not in self.crime_data:
            return None
        data = self.crime_data[year]
        categories = ['homicide', 'assault', 'robbery', 'burglary', 'drug_possession',
                      'drug_trafficking', 'organized_crime', 'white_collar', 'cyber_crime']
        values = [data.get(cat, 0) for cat in categories]

        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor('black')

        bars = ax.bar(categories, values, color='orange', alpha=0.85)
        ax.set_facecolor('black')
        ax.tick_params(colors='white')
        ax.set_title(f"Crime Statistics Breakdown - {year}", color='white')
        ax.set_ylabel('Number of Cases', color='white')
        ax.set_xlabel('Crime Type', color='white')
        ax.set_xticklabels(categories, rotation=45, ha='right', fontsize=9, color='white')

        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval + 1, yval, ha='center', color='white')

        return fig

    def create_crime_map(self):
        st_kitts_center = [17.3578, -62.7822]
        m = folium.Map(location=st_kitts_center, zoom_start=11, tiles=None)
        folium.TileLayer(
            tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
            attr='Google Satellite',
            name='Google Satellite',
            overlay=False,
            control=True
        ).add_to(m)
        folium.TileLayer(
            tiles='https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}',
            attr='Google Terrain',
            name='Google Terrain',
            overlay=False,
            control=True
        ).add_to(m)
        folium.TileLayer('OpenStreetMap', name='OpenStreetMap', overlay=False, control=True).add_to(m)

        # Using real affected areas data
        hotspots = []
        for year_data in self.crime_data.values():
            for area in year_data.get("most_affected_areas", []):
                # Dummy location for demonstration (adjust with real coordinates)
                coords_map = {
                    "Basseterre": [17.2948, -62.7234],
                    "Frigate Bay": [17.2619, -62.6853],
                    "Sandy Point": [17.3547, -62.8119],
                    "Charlestown": [17.1372, -62.6219],
                    "Dieppe Bay": [17.4075, -62.8097]
                }
                coords = coords_map.get(area)
                if coords:
                    hotspots.append({
                        "name": area,
                        "coords": coords,
                        "crimes": year_data.get("total_crimes", 1000)//len(year_data.get("most_affected_areas", [1])),
                        "type": "High"
                    })

        # Add markers
        for spot in hotspots:
            folium.CircleMarker(
                location=spot["coords"],
                radius=8,
                popup=f"{spot['name']} - Crimes: {spot['crimes']}",
                color="red",
                fill=True,
                fill_color="red",
                fill_opacity=0.6,
            ).add_to(m)

        folium.LayerControl().add_to(m)
        return m

    def get_emergency_contact_warning(self, service_type):
        if service_type in self.emergency_contacts:
            return self.emergency_contacts[service_type]["warning"]
        return "Emergency contact not found."

    def process_criminologist_query(self, user_input):
        user_input_lower = user_input.lower()
        # Emergency contacts info
        if any(word in user_input_lower for word in ["emergency", "contact", "number", "help"]):
            return """**EMERGENCY CONTACTS FOR ST. KITTS & NEVIS**

Use the sidebar buttons for specific emergency services:
- Police (911)
- Hospital (911)
- Fire Department (911)

For all emergencies, dial 911 immediately."""
       
        elif any(word in user_input_lower for word in ["chart", "graph", "statistics", "visual", "plot"]):
            return "Crime Statistics Chart Generated - check sidebar."

        elif any(word in user_input_lower for word in ["map", "location", "hotspot", "area", "geographic"]):
            return "Crime Hotspot Map Generated - see sidebar."

        else:
            prompt = self.create_criminology_prompt(user_input)
            return self.gemini_api.get_gemini_response(prompt)

# ======== Session State Initialization ========
def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = CriminologyIntelligenceBot()
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "current_user" not in st.session_state:
        st.session_state.current_user = None
    if "user_role" not in st.session_state:
        st.session_state.user_role = None
    if "auth" not in st.session_state:
        st.session_state.auth = UserAuthentication()
    if "emergency_confirmation" not in st.session_state:
        st.session_state.emergency_confirmation = None

# ======== Login/Register UI ========
def show_login_page():
    st.title("SECURO")
    st.markdown("<p class='subtitle'>Criminology Intelligence Assistant for St. Kitts & Nevis</p>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Create Account"])

    with tab1:
        st.subheader("Login to SECURO")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login", use_container_width=True):
            if username and password:
                success, message = st.session_state.auth.login(username, password)
                if success:
                    st.success(message)
                    time.sleep(1)
                    st.experimental_rerun()
                else:
                    st.error(message)
            else:
                st.error("Please enter both username and password")

    with tab2:
        st.subheader("Create New Account")
        new_username = st.text_input("Choose Username", key="new_username")
        new_password = st.text_input("Choose Password", type="password", key="new_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
        role = st.selectbox("Role", ["Criminologist", "Law Enforcement", "Researcher", "Student"])

        if st.button("Create Account", use_container_width=True):
            if new_username and new_password and confirm_password:
                if new_password != confirm_password:
                    st.error("Passwords do not match")
                else:
                    success, message = st.session_state.auth.create_account(new_username, new_password, role)
                    if success:
                        st.success(message)
                        st.info("You can now login using your credentials")
                    else:
                        st.error(message)
            else:
                st.error("Please fill in all fields")

# ======== Display messages ========
def display_message(role, content):
    if role == "user":
        st.markdown(f'''
        <div class="user-message">
            <div class="user-bubble">{content}</div>
        </div>''', unsafe_allow_html=True)
    else:
        st.markdown(f'''
        <div class="bot-message">
            <div class="bot-bubble">{content}</div>
        </div>''', unsafe_allow_html=True)

# ======== Emergency contact confirmation ========
def handle_emergency_contact(service_type):
    chatbot = st.session_state.chatbot
    warning_message = chatbot.get_emergency_contact_warning(service_type)
    st.session_state.messages.append({"role": "assistant", "content": warning_message})
    st.session_state.emergency_confirmation = service_type
    st.experimental_rerun()

# ======== Main App ========
def main():
    init_session_state()

    if not st.session_state.logged_in:
        show_login_page()
        return

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.write(f"Welcome, **{st.session_state.current_user}**")
        st.write(f"Role: *{st.session_state.user_role}*")
    with col2:
        st.title("SECURO")
        st.markdown("<p class='subtitle'>Criminology Intelligence Assistant for St. Kitts & Nevis</p>", unsafe_allow_html=True)
    with col3:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.session_state.user_role = None
            st.session_state.messages = []
            st.experimental_rerun()

    chatbot = st.session_state.chatbot

    # Sidebar
    with st.sidebar:
        st.header("Criminology Tools")
        st.success("🤖 Gemini AI is active")
        st.divider()

        # Emergency contacts
        st.subheader("🚨 Emergency Contacts")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Police", use_container_width=True):
                handle_emergency_contact("police")
        with col2:
            if st.button("Hospital", use_container_width=True):
                handle_emergency_contact("hospital")
        if st.button("Fire Department", use_container_width=True):
            handle_emergency_contact("fire")
        st.divider()

        # Analysis tools
        st.subheader("📊 Analysis Tools")
        if st.button("Crime Statistics Chart", use_container_width=True):
            fig = chatbot.create_crime_chart()
            if fig:
                st.pyplot(fig)
                st.session_state.messages.append({"role": "assistant", "content": "Crime statistics chart generated."})
                st.experimental_rerun()

        if st.button("Crime Hotspot Map", use_container_width=True):
            crime_map = chatbot.create_crime_map()
            folium_static(crime_map, width=300, height=400)
            st.session_state.messages.append({"role": "assistant", "content": "Crime hotspot map generated."})
            st.experimental_rerun()

        if st.button("Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.experimental_rerun()

    # Chat window
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            display_message(message["role"], message["content"])

        # Emergency confirmation buttons
        if st.session_state.emergency_confirmation:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("YES - Proceed with Emergency Contact", type="primary", use_container_width=True):
                    service = st.session_state.emergency_confirmation
                    contact_info = chatbot.emergency_contacts[service]
                    response = f"""**EMERGENCY CONTACT CONFIRMED**

Contacting: {contact_info['name']}
Primary Number: {contact_info['number']}
Direct Line: {contact_info['alternative']}

**Note:** This is a simulation. In a real emergency, call immediately.

Stay safe."""
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.session_state.emergency_confirmation = None
                    st.experimental_rerun()
            with col2:
                if st.button("NO - Cancel", use_container_width=True):
                    st.session_state.messages.append({"role": "assistant", "content": "Emergency contact cancelled."})
                    st.session_state.emergency_confirmation = None
                    st.experimental_rerun()

        # User input form
        with st.form("user_input_form", clear_on_submit=True):
            user_input = st.text_input("Ask SECURO anything about crime, statistics, or emergency contacts:", key="input")
            submitted = st.form_submit_button("Send")

            if submitted and user_input:
                st.session_state.messages.append({"role": "user", "content": user_input})

                response = chatbot.process_criminologist_query(user_input)
                st.session_state.messages.append({"role": "assistant", "content": response})

                st.experimental_rerun()

if __name__ == "__main__":
    main()
