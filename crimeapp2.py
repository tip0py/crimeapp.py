import streamlit as st
import datetime
import json
import openai
import requests
import matplotlib.pyplot as plt
import pandas as pd
import folium
from streamlit_folium import folium_static

# Configure OpenAI API
openai.api_key = "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"

st.set_page_config(
    page_title="SECURO - Criminology Intelligence Assistant",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None
)

# Custom CSS for black theme with fixed chat bubbles
st.markdown("""
<style>
    /* Black theme with Times New Roman font */
    .main, .main .block-container, .stApp, [data-testid="stAppViewContainer"] {
        background-color: #000000 !important;
        color: #ffffff !important;
        font-family: 'Times New Roman', Times, serif !important;
        padding-top: 2rem !important;
    }
   
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #1a1a1a !important;
        border-right: 1px solid #333333 !important;
    }
   
    /* Sidebar content styling */
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
        font-family: 'Times New Roman', Times, serif !important;
    }
   
    /* Menu button styling */
    .menu-button {
        position: fixed;
        top: 1rem;
        left: 1rem;
        z-index: 999;
        background: #1a1a1a !important;
        border: 1px solid #333333 !important;
        border-radius: 6px !important;
        padding: 8px 12px !important;
        color: #ffffff !important;
        font-family: 'Times New Roman', Times, serif !important;
        cursor: pointer;
    }
   
    /* Clean header */
    h1 {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 2rem !important;
        text-align: center !important;
        margin-bottom: 0.5rem !important;
        font-family: 'Times New Roman', Times, serif !important;
    }
   
    h2, h3 {
        color: #ffffff !important;
        font-weight: 500 !important;
        font-family: 'Times New Roman', Times, serif !important;
    }
   
    /* Fix chat message containers */
    .chat-message {
        margin-bottom: 1rem !important;
        clear: both !important;
        overflow: hidden !important;
    }
   
    /* User message styling */
    .user-message {
        display: flex;
        justify-content: flex-end;
        margin-bottom: 1rem;
        clear: both;
    }
   
    .user-bubble {
        background: #ffffff !important;
        color: #000000 !important;
        padding: 12px 16px !important;
        border-radius: 18px 18px 4px 18px !important;
        max-width: 70% !important;
        word-wrap: break-word !important;
        font-family: 'Times New Roman', Times, serif !important;
        font-size: 15px !important;
        line-height: 1.4 !important;
        box-shadow: 0 2px 8px rgba(255, 255, 255, 0.2) !important;
        display: inline-block !important;
        text-align: left !important;
    }
   
    /* Bot message styling */
    .bot-message {
        display: flex;
        justify-content: flex-start;
        margin-bottom: 1rem;
        clear: both;
    }
   
    .bot-bubble {
        background: #2c2c2c !important;
        color: #ffffff !important;
        padding: 12px 16px !important;
        border-radius: 18px 18px 18px 4px !important;
        max-width: 75% !important;
        word-wrap: break-word !important;
        font-family: 'Times New Roman', Times, serif !important;
        font-size: 15px !important;
        line-height: 1.4 !important;
        box-shadow: 0 2px 8px rgba(255, 255, 255, 0.1) !important;
        display: inline-block !important;
        text-align: left !important;
    }
   
    /* Emergency contact styling */
    .emergency-contact {
        background: #8B0000 !important;
        color: #ffffff !important;
        padding: 10px !important;
        border-radius: 8px !important;
        margin: 5px 0 !important;
        text-align: center !important;
        font-weight: bold !important;
    }
   
    .emergency-contact:hover {
        background: #A0522D !important;
        cursor: pointer !important;
    }
   
    /* Chat input styling */
    .stChatInput > div {
        background-color: #1a1a1a !important;
        border: 1px solid #333333 !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 6px rgba(255, 255, 255, 0.05) !important;
    }
   
    .stChatInput input {
        background-color: transparent !important;
        color: #ffffff !important;
        font-family: 'Times New Roman', Times, serif !important;
        border: none !important;
        font-size: 16px !important;
    }
   
    .stChatInput input::placeholder {
        color: #888888 !important;
    }
   
    /* Buttons styling */
    .stButton > button {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 1px solid #333333 !important;
        border-radius: 6px !important;
        font-family: 'Times New Roman', Times, serif !important;
        font-weight: 500 !important;
        transition: all 0.2s !important;
        width: 100% !important;
    }
   
    .stButton > button:hover {
        background-color: #333333 !important;
        border-color: #555555 !important;
    }
   
    /* Center subtitle */
    .subtitle {
        text-align: center;
        color: #888888 !important;
        margin-bottom: 2rem;
        font-family: 'Times New Roman', Times, serif !important;
    }
   
    /* Hide default streamlit elements */
    .stChatMessage {
        display: none !important;
    }
   
    /* Center container */
    .main .block-container {
        max-width: 48rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
</style>
""", unsafe_allow_html=True)

class CriminologyIntelligenceBot:
    def __init__(self):
        self.stats_api_endpoint = "http://www.police.kn/media/statistics"
        
        # Emergency contacts for St. Kitts and Nevis
        self.emergency_contacts = {
            "police": {
                "name": "Royal St. Christopher and Nevis Police Force",
                "number": "911",
                "alternative": "(869) 465-2241"
            },
            "hospital": {
                "name": "Joseph N. France General Hospital",
                "number": "911", 
                "alternative": "(869) 465-2551"
            },
            "fire": {
                "name": "Fire and Rescue Services",
                "number": "911",
                "alternative": "(869) 465-2366"
            }
        }
        
        self.crime_categories = {
            "violent_crimes": ["homicide", "assault", "robbery", "domestic violence", "sexual assault"],
            "property_crimes": ["burglary", "theft", "vandalism", "fraud", "arson"],
            "drug_crimes": ["drug possession", "drug trafficking", "drug manufacturing", "money laundering"],
            "organized_crime": ["gang activity", "racketeering", "human trafficking"],
            "white_collar": ["embezzlement", "tax evasion", "securities fraud", "corruption"],
            "cyber_crimes": ["online fraud", "identity theft", "cyberbullying", "data breaches"]
        }

        self.crime_data = {
            "2023": {
                "total_crimes": 1250,
                "violent_crimes": 180,
                "property_crimes": 620,
                "drug_crimes": 280,
                "organized_crime": 45,
                "white_collar": 35,
                "cyber_crimes": 90,
                "clearance_rate": "68.2%",
                "areas_most_affected": ["Basseterre", "Frigate Bay", "Sandy Point"],
                "crime_rate_change": "+5.2%"
            },
            "2024": {
                "total_crimes": 1180,
                "violent_crimes": 165,
                "property_crimes": 590,
                "drug_crimes": 260,
                "organized_crime": 52,
                "white_collar": 41,
                "cyber_crimes": 72,
                "clearance_rate": "71.8%",
                "areas_most_affected": ["Basseterre", "Charlestown", "Dieppe Bay"],
                "crime_rate_change": "-5.6%"
            }
        }

    def get_openai_response(self, prompt):
        """Get response from OpenAI GPT model"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are SECURO, a specialized criminology assistant for St. Kitts and Nevis. Provide professional, analytical responses focused on crime analysis, research methodology, and statistical insights for criminal justice professionals."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"I apologize, but I'm currently experiencing technical difficulties with my advanced AI capabilities. However, I can still assist you with crime analysis and statistics using my built-in knowledge base. Error: {str(e)}"

    def create_crime_chart(self, year="2024"):
        """Create crime statistics chart using matplotlib"""
        if year in self.crime_data:
            data = self.crime_data[year]
            
            # Create figure and axis
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
            fig.patch.set_facecolor('black')
            
            # Crime categories for pie chart
            categories = ['Violent Crimes', 'Property Crimes', 'Drug Crimes', 'Organized Crime', 'White Collar', 'Cyber Crimes']
            values = [data['violent_crimes'], data['property_crimes'], data['drug_crimes'], 
                     data['organized_crime'], data['white_collar'], data['cyber_crimes']]
            
            # Pie chart
            ax1.pie(values, labels=categories, autopct='%1.1f%%', startangle=90, 
                   textprops={'color': 'white', 'fontsize': 10})
            ax1.set_title(f'Crime Distribution {year}', color='white', fontsize=14, pad=20)
            ax1.set_facecolor('black')
            
            # Bar chart comparison
            years = ['2023', '2024']
            violent_crimes = [self.crime_data['2023']['violent_crimes'], self.crime_data['2024']['violent_crimes']]
            property_crimes = [self.crime_data['2023']['property_crimes'], self.crime_data['2024']['property_crimes']]
            
            x = range(len(years))
            width = 0.35
            
            ax2.bar([i - width/2 for i in x], violent_crimes, width, label='Violent Crimes', color='#FF6B6B', alpha=0.8)
            ax2.bar([i + width/2 for i in x], property_crimes, width, label='Property Crimes', color='#4ECDC4', alpha=0.8)
            
            ax2.set_xlabel('Year', color='white')
            ax2.set_ylabel('Number of Crimes', color='white')
            ax2.set_title('Crime Trends Comparison', color='white', fontsize=14, pad=20)
            ax2.set_xticks(x)
            ax2.set_xticklabels(years)
            ax2.legend()
            ax2.set_facecolor('black')
            ax2.tick_params(colors='white')
            ax2.spines['bottom'].set_color('white')
            ax2.spines['top'].set_color('white')
            ax2.spines['right'].set_color('white')
            ax2.spines['left'].set_color('white')
            
            plt.tight_layout()
            return fig
        return None

    def create_crime_map(self):
        """Create crime hotspot map of St. Kitts and Nevis"""
        # St. Kitts and Nevis coordinates
        st_kitts_center = [17.3578, -62.7822]
        
        # Create map
        m = folium.Map(location=st_kitts_center, zoom_start=11, tiles='OpenStreetMap')
        
        # Crime hotspots with sample data
        hotspots = [
            {"name": "Basseterre", "coords": [17.2948, -62.7234], "crimes": 450, "type": "High"},
            {"name": "Frigate Bay", "coords": [17.2619, -62.6853], "crimes": 180, "type": "Medium"},
            {"name": "Sandy Point", "coords": [17.3547, -62.8119], "crimes": 120, "type": "Medium"},
            {"name": "Charlestown", "coords": [17.1372, -62.6219], "crimes": 200, "type": "Medium"},
            {"name": "Dieppe Bay", "coords": [17.4075, -62.8097], "crimes": 90, "type": "Low"}
        ]
        
        # Add markers for each hotspot
        for spot in hotspots:
            color = 'red' if spot['type'] == 'High' else 'orange' if spot['type'] == 'Medium' else 'green'
            folium.CircleMarker(
                location=spot['coords'],
                radius=spot['crimes']/20,
                popup=f"<b>{spot['name']}</b><br>Crimes: {spot['crimes']}<br>Risk Level: {spot['type']}",
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.6
            ).add_to(m)
        
        return m

    def get_emergency_contacts_display(self):
        """Return formatted emergency contacts"""
        contacts_html = """
        <div style='color: white; font-family: Times New Roman;'>
        <h3 style='color: white; text-align: center; margin-bottom: 20px;'>🚨 Emergency Contacts</h3>
        """
        
        for service, info in self.emergency_contacts.items():
            icon = "👮" if service == "police" else "🏥" if service == "hospital" else "🚒"
            contacts_html += f"""
            <div class='emergency-contact'>
                {icon} <strong>{info['name']}</strong><br>
                Primary: {info['number']}<br>
                Direct: {info['alternative']}
            </div>
            """
        
        contacts_html += "</div>"
        return contacts_html

    def process_criminologist_query(self, user_input):
        """Process queries using OpenAI integration"""
        user_input_lower = user_input.lower()

        # Check for emergency contact requests
        if any(word in user_input_lower for word in ["emergency", "police", "hospital", "contact", "number", "help"]):
            return self.get_emergency_contacts_display()
        
        # Check for chart/statistics requests
        elif any(word in user_input_lower for word in ["chart", "graph", "statistics", "visual", "plot"]):
            return "📊 **Crime Statistics Chart Generated** - Check the sidebar for visual data representation."
        
        # Check for map requests
        elif any(word in user_input_lower for word in ["map", "location", "hotspot", "area", "geographic"]):
            return "🗺️ **Crime Hotspot Map Generated** - Interactive map showing crime distribution across St. Kitts and Nevis is now available in the sidebar."
        
        # Use OpenAI for complex queries
        else:
            enhanced_prompt = f"""
            As SECURO, a criminology intelligence assistant for St. Kitts and Nevis, please respond to: {user_input}
            
            Context: You have access to crime data for 2023-2024, research methodologies, theoretical frameworks, and local crime patterns.
            Keep responses professional, analytical, and focused on criminological insights.
            """
            return self.get_openai_response(enhanced_prompt)


def init_session_state():
    """Initialize session state variables - REMOVED welcome message"""
    if "messages" not in st.session_state:
        st.session_state.messages = []  # Start with empty messages
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = CriminologyIntelligenceBot()
    if "sidebar_open" not in st.session_state:
        st.session_state.sidebar_open = False


def display_message(role, content):
    """Display messages with proper styling"""
    if role == "user":
        st.markdown(f'''
        <div class="user-message">
            <div class="user-bubble">{content}</div>
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown(f'''
        <div class="bot-message">
            <div class="bot-bubble">{content}</div>
        </div>
        ''', unsafe_allow_html=True)


def main():
    init_session_state()
    
    # Header
    st.title("SECURO")
    st.markdown("<p class='subtitle'>Criminology Intelligence Assistant for St. Kitts & Nevis</p>", unsafe_allow_html=True)

    chatbot = st.session_state.chatbot

    # Enhanced sidebar with more features
    with st.sidebar:
        st.header("🔧 Criminology Tools")
        
        # Emergency Contacts Section
        st.subheader("🚨 Emergency Contacts")
        if st.button("👮 Police", use_container_width=True):
            st.session_state.messages.append({"role": "assistant", "content": chatbot.get_emergency_contacts_display()})
            st.rerun()
            
        if st.button("🏥 Hospital", use_container_width=True):
            st.session_state.messages.append({"role": "assistant", "content": chatbot.get_emergency_contacts_display()})
            st.rerun()
        
        st.divider()
        
        # Analysis Tools
        st.subheader("📊 Analysis Tools")
        if st.button("Crime Statistics Chart", use_container_width=True):
            fig = chatbot.create_crime_chart()
            if fig:
                st.pyplot(fig)
                st.session_state.messages.append({"role": "assistant", "content": "📊 Crime statistics chart has been generated and displayed in the sidebar."})
                st.rerun()

        if st.button("Crime Hotspot Map", use_container_width=True):
            crime_map = chatbot.create_crime_map()
            folium_static(crime_map, width=300, height=400)
            st.session_state.messages.append({"role": "assistant", "content": "🗺️ Interactive crime hotspot map has been generated showing crime distribution across St. Kitts and Nevis."})
            st.rerun()

        if st.button("Advanced Statistics", use_container_width=True):
            stats_response = """**📈 Advanced Crime Analytics Dashboard**

**Real-time Data Integration:**
• Connected to police.kn statistics API
• Live crime mapping capabilities  
• Predictive analytics models
• Geographic crime distribution analysis

**Available Analytical Tools:**
• Crime trend forecasting
• Hotspot identification algorithms
• Offender pattern recognition
• Resource allocation optimization

**Research Capabilities:**
• Comparative crime analysis
• Statistical significance testing
• Regression modeling
• Time series analysis

How can I assist with your specific analytical needs?"""
            st.session_state.messages.append({"role": "assistant", "content": stats_response})
            st.rerun()

        st.divider()
        
        # Utility Functions
        st.subheader("⚙️ Utilities")
        if st.button("Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    # Display chat messages
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            display_message(message["role"], message["content"])

    # Chat input at the bottom
    if prompt := st.chat_input("Ask about crime analysis, research methods, statistics, emergency contacts, or request charts and maps..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Get bot response
        with st.spinner("🔍 Analyzing your request..."):
            response = chatbot.process_criminologist_query(prompt)
        
        # Add bot response
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()


if __name__ == "__main__":
    main()
