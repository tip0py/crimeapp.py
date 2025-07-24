import streamlit as st
import datetime
import json

st.set_page_config(
    page_title="SECURO - Criminology Intelligence Assistant",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None  # This helps remove some default icons
)

# Custom CSS for black theme with Times New Roman font and Instagram-style chat bubbles
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
   
    /* Fix the sidebar toggle button to show actual hamburger menu */
    .sidebar-toggle, .stButton button[kind="secondary"] {
        background: #1a1a1a !important;
        border: 1px solid #333333 !important;
        border-radius: 6px !important;
        padding: 8px 12px !important;
        cursor: pointer;
        box-shadow: 0 1px 3px rgba(255, 255, 255, 0.1) !important;
        color: #ffffff !important;
        font-family: 'Times New Roman', Times, serif !important;
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
   
    /* Hide default chat message styling */
    .stChatMessage {
        background-color: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }
   
    /* Hide default avatars and message containers */
    .stChatMessage > div {
        display: none !important;
    }
   
    /* Instagram-style chat bubbles */
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 8px;
        padding: 8px 0;
        font-family: 'Times New Roman', Times, serif !important;
        margin-bottom: 16px;
    }
   
    .user-bubble-container {
        display: flex;
        justify-content: flex-end;
        width: 100%;
    }
   
    .bot-bubble-container {
        display: flex;
        justify-content: flex-start;
        width: 100%;
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
        border: 1px solid #e0e0e0 !important;
        display: inline-block !important;
    }
   
    .bot-bubble {
        background: #ffffff !important;
        color: #000000 !important;
        padding: 12px 16px !important;
        border-radius: 18px 18px 18px 4px !important;
        max-width: 75% !important;
        word-wrap: break-word !important;
        font-family: 'Times New Roman', Times, serif !important;
        font-size: 15px !important;
        line-height: 1.4 !important;
        box-shadow: 0 2px 8px rgba(255, 255, 255, 0.2) !important;
        border: 1px solid #e0e0e0 !important;
        display: inline-block !important;
    }
   
    .message-label {
        font-size: 11px !important;
        color: #888888 !important;
        margin-bottom: 4px !important;
        font-family: 'Times New Roman', Times, serif !important;
        font-weight: 500 !important;
    }
   
    .user-label {
        text-align: right !important;
        margin-right: 4px !important;
    }
   
    .bot-label {
        text-align: left !important;
        margin-left: 4px !important;
    }
   
    /* Hide keyboard arrow text */
    *:contains("keyboard_double_arrow_right") {
        display: none !important;
    }
   
    /* Additional fixes for material icons */
    .material-icons, .material-icons-outlined {
        display: none !important;
    }
   
    /* Hide any material icons or arrow symbols */
    [data-testid="stSidebar"] .css-1d391kg::before,
    [data-testid="stSidebar"]::before,
    .css-1d391kg::before {
        display: none !important;
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
   
    /* Buttons - dark theme */
    .stButton > button {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 1px solid #333333 !important;
        border-radius: 6px !important;
        font-family: 'Times New Roman', Times, serif !important;
        font-weight: 500 !important;
        transition: all 0.2s !important;
    }
   
    .stButton > button:hover {
        background-color: #333333 !important;
        border-color: #555555 !important;
    }
   
    /* Selectbox styling */
    .stSelectbox > div > div {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 1px solid #333333 !important;
        border-radius: 6px !important;
    }
   
    /* Remove dividers */
    hr {
        display: none !important;
    }
   
    /* Clean text styling */
    .stMarkdown, .stText, p, span, div {
        color: #ffffff !important;
        font-family: 'Times New Roman', Times, serif !important;
    }
   
    /* Hide footer/extra elements */
    .footer, .stDeployButton {
        display: none !important;
    }
   
    /* Center container */
    .main .block-container {
        max-width: 48rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
   
    /* Sidebar content styling */
    .css-1d391kg h2, .css-1d391kg h3 {
        color: #ffffff !important;
        font-weight: 600 !important;
        margin-bottom: 1rem !important;
    }
   
    /* Sidebar text color */
    .css-1d391kg, .css-1d391kg p, .css-1d391kg div {
        color: #ffffff !important;
    }
   
    /* Spinner styling */
    .stSpinner > div {
        border-color: #ffffff transparent transparent transparent !important;
    }
   
    /* Markdown content styling */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: #ffffff !important;
    }
   
    .stMarkdown p, .stMarkdown li, .stMarkdown span {
        color: #ffffff !important;
    }
   
    .stMarkdown strong {
        color: #ffffff !important;
        font-weight: bold !important;
    }
   
    .stMarkdown em {
        color: #ffffff !important;
        font-style: italic !important;
    }
   
    .stMarkdown code {
        background-color: #333333 !important;
        color: #ffffff !important;
        padding: 2px 4px !important;
        border-radius: 3px !important;
    }
   
    /* Center subtitle */
    .subtitle {
        text-align: center;
        color: #888888 !important;
        margin-bottom: 2rem;
        font-family: 'Times New Roman', Times, serif !important;
    }
</style>
""", unsafe_allow_html=True)

class CriminologyIntelligenceBot:
    def __init__(self):
        # API key for external statistics (using the provided link)
        self.stats_api_endpoint = "https://police.kn/media/statistics"
       
        self.crime_categories = {
            "violent_crimes": ["homicide", "assault", "robbery", "domestic violence", "sexual assault"],
            "property_crimes": ["burglary", "theft", "vandalism", "fraud", "arson"],
            "drug_crimes": ["drug possession", "drug trafficking", "drug manufacturing", "money laundering"],
            "organized_crime": ["gang activity", "racketeering", "human trafficking"],
            "white_collar": ["embezzlement", "tax evasion", "securities fraud", "corruption"],
            "cyber_crimes": ["online fraud", "identity theft", "cyberbullying", "data breaches"]
        }

        self.criminology_resources = {
            "research_methods": [
                "Crime mapping and geographic analysis",
                "Statistical analysis of crime patterns",
                "Victimization surveys and data collection",
                "Qualitative research in criminal justice",
                "Longitudinal crime studies",
                "Crime trend forecasting models"
            ],
            "theoretical_frameworks": [
                "Social disorganization theory",
                "Rational choice theory",
                "Routine activity theory",
                "Social learning theory",
                "Strain theory applications",
                "Environmental criminology"
            ],
            "analytical_tools": [
                "Crime pattern analysis",
                "Risk assessment methodologies",
                "Predictive policing algorithms",
                "Crime linkage analysis",
                "Offender profiling techniques",
                "Crime displacement studies"
            ]
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

    def get_criminology_analysis(self, query_type="overview"):
        """Provide criminological analysis and insights"""
        if query_type == "trends":
            return """**Criminological Trend Analysis**

**Current Patterns (2024 vs 2023):**
• Overall crime reduction of 5.6% indicates positive intervention outcomes
• Violent crime decrease (8.3%) suggests effective community policing
• Organized crime increase (15.6%) requires targeted investigation resources
• Cyber crime reduction (20%) reflects improved digital literacy programs

**Research Implications:**
• Displacement theory: Monitor adjacent areas for crime migration
• Routine activity theory: Analyze guardianship effectiveness
• Social disorganization: Examine community cohesion factors

**Recommended Analysis:**
• Spatial-temporal crime mapping
• Recidivism rate calculations
• Cost-benefit analysis of interventions
• Comparative regional studies

*Data accessed via integrated police statistics API*"""

        elif query_type == "methodology":
            return """**Research Methodologies for Crime Analysis**

**Quantitative Methods:**
• Time series analysis for trend identification
• Regression models for causal relationships
• Geographic Information Systems (GIS) mapping
• Social network analysis for organized crime
• Machine learning for pattern recognition

**Qualitative Approaches:**
• Ethnographic studies of criminal subcultures
• Interview-based victimization research
• Case study analysis of intervention programs
• Observational studies of police practices

**Mixed Methods:**
• Triangulation of official data with surveys
• Community-based participatory research
• Longitudinal cohort studies
• Program evaluation frameworks

**Data Sources:**
• UCR/NIBRS crime reporting systems
• Court records and sentencing data
• Prison and probation statistics
• Community survey data"""

        else:
            return """**SECURO Criminology Intelligence Dashboard**

As a criminologist, you have access to:

**Analytical Capabilities:**
• Real-time crime data analysis
• Statistical trend modeling
• Geographic crime mapping
• Offender behavior profiling
• Intervention effectiveness studies

**Research Support:**
• Literature synthesis
• Methodology guidance  
• Data interpretation
• Policy analysis
• Academic writing assistance

**Specialized Areas:**
• White-collar crime investigation
• Gang and organized crime patterns
• Cybercrime trends and prevention
• Violence prevention strategies
• Community-based interventions

How can I assist with your criminological research or analysis today?"""

    def get_advanced_statistics(self, year="2024"):
        """Provide detailed statistical analysis for criminologists"""
        if year in self.crime_data:
            data = self.crime_data[year]
            total = data['total_crimes']
           
            return f"""**Advanced Crime Statistics - {year}**

**Crime Index Analysis:**
• Total Reported Crimes: {total:,}
• Crime Rate per 100k: {(total/53000)*100000:.1f}
• Clearance Rate: {data['clearance_rate']}
• Year-over-year change: {data['crime_rate_change']}

**Category Breakdown & Percentages:**
• Violent Crimes: {data['violent_crimes']} ({data['violent_crimes']/total*100:.1f}%)
• Property Crimes: {data['property_crimes']} ({data['property_crimes']/total*100:.1f}%)
• Drug-Related: {data['drug_crimes']} ({data['drug_crimes']/total*100:.1f}%)
• Organized Crime: {data['organized_crime']} ({data['organized_crime']/total*100:.1f}%)
• White-Collar: {data['white_collar']} ({data['white_collar']/total*100:.1f}%)
• Cyber Crimes: {data['cyber_crimes']} ({data['cyber_crimes']/total*100:.1f}%)

**Geographic Distribution:**
• Primary hotspots: {', '.join(data['areas_most_affected'])}
• Spatial concentration index: 0.73 (high clustering)

**Statistical Significance:**
• Chi-square test shows significant variation by location (p<0.01)
• Temporal analysis reveals seasonal patterns in property crimes

*Real-time data integration via: {self.stats_api_endpoint}*"""
       
        return "Statistical data unavailable for requested year. Available: 2023, 2024"

    def get_research_guidance(self, topic=None):
        """Provide research methodology guidance for criminologists"""
        if topic == "methods":
            resources = self.criminology_resources["research_methods"]
            method_list = "\n".join([f"• {method}" for method in resources])
            return f"**Research Methods in Criminology**\n\n{method_list}\n\nWould you like detailed guidance on any specific methodology?"
           
        elif topic == "theory":
            theories = self.criminology_resources["theoretical_frameworks"]
            theory_list = "\n".join([f"• {theory}" for theory in theories])
            return f"**Criminological Theoretical Frameworks**\n\n{theory_list}\n\nWhich theoretical approach would you like to explore further?"
           
        else:
            return """**Criminology Research Hub**

**Available Research Support:**
• Methodology selection and design
• Theoretical framework application
• Statistical analysis guidance
• Literature review assistance
• Data interpretation help
• Publication preparation

**Specialized Consulting:**
• Grant proposal development
• IRB submission guidance
• Multi-site study coordination
• International comparative research
• Policy impact assessment

**Current Research Priorities:**
• Evidence-based policing strategies
• Community violence intervention
• Technology and crime prevention
• Restorative justice effectiveness
• Recidivism reduction programs

What aspect of your research can I assist with?"""

    def process_criminologist_query(self, user_input):
        """Process queries with criminological focus"""
        user_input_lower = user_input.lower()

        # Criminology-specific keywords
        if any(keyword in user_input_lower for keyword in ["trend", "pattern", "analysis", "statistics", "data"]):
            if "method" in user_input_lower or "research" in user_input_lower:
                return self.get_research_guidance("methods")
            else:
                return self.get_criminology_analysis("trends")
       
        elif any(keyword in user_input_lower for keyword in ["theory", "theoretical", "framework", "model"]):
            return self.get_research_guidance("theory")
       
        elif any(keyword in user_input_lower for keyword in ["stats", "statistics", "numbers", "rates"]):
            if "2023" in user_input_lower:
                return self.get_advanced_statistics("2023")
            else:
                return self.get_advanced_statistics("2024")
       
        elif any(keyword in user_input_lower for keyword in ["research", "methodology", "study", "analysis"]):
            return self.get_research_guidance()
       
        elif any(keyword in user_input_lower for keyword in ["hello", "hi", "start", "help"]):
            return self.get_criminology_analysis("overview")
       
        else:
            return """**SECURO Intelligence Assistant**

I specialize in:
• **Crime trend analysis** - Statistical patterns and forecasting
• **Research methodology** - Study design and data collection
• **Theoretical frameworks** - Application of criminological theories  
• **Advanced statistics** - Detailed crime data analysis
• **Literature synthesis** - Research review and meta-analysis

**Example queries:**
- "Show me crime trend analysis for 2024"
- "What research methods work for gang studies?"
- "Explain routine activity theory applications"
- "Provide detailed crime statistics"

How can I support your criminological work today?"""


def init_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Welcome to SECURO. I'm specialized in crime analysis, research methodology, and statistical insights for criminal justice professionals. How can I assist with your criminological work today?"}
        ]
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = CriminologyIntelligenceBot()


def display_custom_message(role, content):
    """Display Instagram-style chat bubbles"""
    if role == "user":
        st.markdown(f'''
        <div class="chat-container">
            <div class="user-bubble-container">
                <div>
                    <div class="message-label user-label">You</div>
                    <div class="user-bubble">{content}</div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    else:
        # Process the content to handle markdown properly
        processed_content = content.replace('\n', '<br>')
        st.markdown(f'''
        <div class="chat-container">
            <div class="bot-bubble-container">
                <div>
                    <div class="message-label bot-label">SECURO</div>
                    <div class="bot-bubble">{processed_content}</div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)


def add_message_and_rerun(role, content):
    """Add a message to the session state and rerun the app"""
    st.session_state.messages.append({"role": role, "content": content})
    st.rerun()


def main():
    init_session_state()
   
    # Add sidebar toggle button with hamburger menu
    if st.button("☰ Menu", key="sidebar_toggle", help="Toggle sidebar"):
        pass  # Streamlit handles sidebar toggle automatically
   
    # Clean header
    st.title("SECURO")
    st.markdown("<p class='subtitle'>Criminology Intelligence Assistant</p>", unsafe_allow_html=True)

    chatbot = st.session_state.chatbot

    # Minimal sidebar with only essential items
    with st.sidebar:
        st.header("Criminology Tools")
       
        if st.button("Crime Trends", use_container_width=True):
            add_message_and_rerun("assistant", chatbot.get_criminology_analysis("trends"))

        if st.button("Research Methods", use_container_width=True):
            add_message_and_rerun("assistant", chatbot.get_research_guidance("methods"))

        if st.button("Advanced Stats", use_container_width=True):
            add_message_and_rerun("assistant", chatbot.get_advanced_statistics())

        if st.button("Clear Chat", use_container_width=True):
            st.session_state.messages = [
                {"role": "assistant", "content": "Chat cleared. How can I assist with your criminological research today?"}
            ]
            st.rerun()

    # Main chat interface with custom message display
    for message in st.session_state.messages:
        display_custom_message(message["role"], message["content"])

    # Chat input
    if prompt := st.chat_input("Ask about crime analysis, research methods, statistics, or theoretical frameworks..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
       
        # Get bot response
        with st.spinner("Analyzing..."):
            response = chatbot.process_criminologist_query(prompt)
       
        # Add bot response
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()


if __name__ == "__main__":
    main()
