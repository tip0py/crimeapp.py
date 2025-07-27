import streamlit as st
import datetime
import json
import requests
import matplotlib.pyplot as plt
import pandas as pd
import folium
from streamlit_folium import folium_static
import hashlib
import time
import os

st.set_page_config(
    page_title="SECURO - Crime Mitigation AI Chat Bot",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None
)

# Updated CSS with enhanced magnifying glass animation
st.markdown("""
<style>
    /* Black theme with Times New Roman font */
    .main, .main .block-container, .stApp, [data-testid="stAppViewContainer"] {
        background-color: #000000 !important;
        color: #ffffff !important;
        font-family: 'Times New Roman', Times, serif !important;
        padding-top: 2rem !important;
    }

    /* Login page with your crime scene background */
    .login-page {
        background-image: url('data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAAfACgDASIAAhEBAxEB/8QAGQAAAwEBAQAAAAAAAAAAAAAABAUGAwIB/8QALBAAAQMDAwMEAQQDAAAAAAAAAQIDEQAEBSExEkFhBhMicYGRoTKx0fAjQsH/xAAYAQADAQEAAAAAAAAAAAAAAAACAwQBBf/EAB4RAAIDAQACAwAAAAAAAAAAAAABAgMREiExE0FR/9oADAMBAAIRAxEAPwCmxeKt7VCG2kBKEiABsK1VQeyMslplCVd6/aVoBb0uoACkkEJSEA+4NdeKbm2s8qpt12kOJbSAr9JeKtT5gCmsagtCj9isqy6ky99bKU6lUhKdVEmJ8A7V1jfYlbSUiGgYgVhLPG4yMoTcpcbeXAPyEyKjEzf5+3YSnwtTwPyJVxo+lGzjIzF31PuIQlWqfaSr8EpOkgfGRnYuGTkmXJDrbTqVEKyOjF1K0goBIAGWXL1LCzQW+q4wvEcVhJ7q/EGdUq5Jqwx/t5SzQ8ggKOqTP9Kqf9k=') !important;
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
        min-height: 100vh !important;
        position: relative !important;
    }

    /* Dark overlay for login page */
    .login-page::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.7) !important;
        z-index: 1 !important;
    }

    /* Ensure login content appears above overlay */
    .login-content {
        position: relative !important;
        z-index: 2 !important;
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
        font-size: 2.5rem !important;
        text-align: center !important;
        margin-bottom: 0.5rem !important;
        font-family: 'Times New Roman', Times, serif !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8) !important;
    }
   
    h2, h3 {
        color: #ffffff !important;
        font-weight: 500 !important;
        font-family: 'Times New Roman', Times, serif !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8) !important;
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

    /* Emergency button styling */
    .emergency-btn {
        background-color: #8B0000 !important;
        color: #ffffff !important;
        border: 2px solid #FF0000 !important;
    }

    .emergency-btn:hover {
        background-color: #FF0000 !important;
        border-color: #FF4444 !important;
    }
   
    /* Center subtitle */
    .subtitle {
        text-align: center;
        color: #FFFF00 !important;
        margin-bottom: 2rem;
        font-family: 'Times New Roman', Times, serif !important;
        font-weight: bold !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8) !important;
        font-size: 1.2rem !important;
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

    /* Enhanced login form styling */
    .login-container {
        background-color: rgba(26, 26, 26, 0.95) !important;
        padding: 2.5rem !important;
        border-radius: 15px !important;
        border: 2px solid #FFFF00 !important;
        max-width: 450px !important;
        margin: 2rem auto !important;
        box-shadow: 0 8px 32px rgba(255, 255, 0, 0.3) !important;
        backdrop-filter: blur(10px) !important;
    }

    /* SECURO branding */
    .securo-title {
        color: #FFFF00 !important;
        font-size: 3rem !important;
        font-weight: bold !important;
        text-align: center !important;
        text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.9) !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: 3px !important;
    }

    /* Crime scene tape effect */
    .crime-tape {
        background: repeating-linear-gradient(
            45deg,
            #FFFF00,
            #FFFF00 10px,
            #000000 10px,
            #000000 20px
        ) !important;
        height: 8px !important;
        margin: 1rem 0 !important;
        border: 2px solid #000000 !important;
    }

    /* Crime map container */
    .crime-map-container {
        background-color: #1a1a1a !important;
        border: 2px solid #333333 !important;
        border-radius: 10px !important;
        padding: 20px !important;
        margin: 20px 0 !important;
    }

    /* Enhanced magnifying glass celebration animation */
    @keyframes magnifySearch {
        0% { 
            transform: translateY(100vh) scale(0.5) rotate(0deg);
            opacity: 0;
        }
        20% {
            opacity: 1;
        }
        50% { 
            transform: translateY(30vh) scale(1.2) rotate(180deg);
            opacity: 1;
        }
        80% {
            transform: translateY(-10vh) scale(0.8) rotate(360deg);
            opacity: 0.8;
        }
        100% { 
            transform: translateY(-20vh) scale(0.3) rotate(540deg);
            opacity: 0;
        }
    }

    .magnify-celebration {
        position: fixed;
        font-size: 2rem;
        z-index: 9999;
        pointer-events: none;
        animation: magnifySearch 4s ease-out forwards;
    }

    /* Vary the animation timing for different magnifying glasses */
    .magnify-1 { animation-delay: 0s; left: 10%; }
    .magnify-2 { animation-delay: 0.3s; left: 20%; }
    .magnify-3 { animation-delay: 0.6s; left: 30%; }
    .magnify-4 { animation-delay: 0.9s; left: 40%; }
    .magnify-5 { animation-delay: 1.2s; left: 50%; }
    .magnify-6 { animation-delay: 1.5s; left: 60%; }
    .magnify-7 { animation-delay: 1.8s; left: 70%; }
    .magnify-8 { animation-delay: 2.1s; left: 80%; }
    .magnify-9 { animation-delay: 2.4s; left: 90%; }
    .magnify-10 { animation-delay: 2.7s; left: 85%; }
    .magnify-11 { animation-delay: 3.0s; left: 75%; }
    .magnify-12 { animation-delay: 3.3s; left: 65%; }
    .magnify-13 { animation-delay: 3.6s; left: 55%; }
    .magnify-14 { animation-delay: 3.9s; left: 45%; }
    .magnify-15 { animation-delay: 4.2s; left: 35%; }
</style>
""", unsafe_allow_html=True)

class UserAuthentication:
    def __init__(self):
        if "users_db" not in st.session_state:
            st.session_state.users_db = {}
       
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
   
    def create_account(self, username, password, role, badge_number="", department=""):
        """Create new professional user account"""
        if username in st.session_state.users_db:
            return False, "Username already exists"
       
        if len(password) < 8:
            return False, "Password must be at least 8 characters for security"
       
        st.session_state.users_db[username] = {
            "password": self.hash_password(password),
            "role": role,
            "badge_number": badge_number if badge_number else "",
            "department": department if department else "",
            "created": datetime.datetime.now().isoformat(),
            "access_level": self.get_access_level(role)
        }
        return True, "Professional account created successfully"
   
    def get_access_level(self, role):
        levels = {
            "Senior Criminologist": 5,
            "Detective": 4,
            "Police Officer": 3,
            "Forensic Specialist": 4,
            "Legal Advisor": 4,
            "Researcher": 2,
            "Student": 1
        }
        return levels.get(role, 1)
   
    def login(self, username, password):
        if username not in st.session_state.users_db:
            return False, "Professional credentials not found"
       
        if st.session_state.users_db[username]["password"] != self.hash_password(password):
            return False, "Invalid credentials"
       
        user_data = st.session_state.users_db[username]
        st.session_state.logged_in = True
        st.session_state.current_user = username
        st.session_state.user_role = user_data["role"]
        st.session_state.access_level = user_data["access_level"]
        st.session_state.badge_number = user_data.get("badge_number", "")
        st.session_state.department = user_data.get("department", "")
        return True, "Professional access granted"

class GeminiAPI:
    def __init__(self):
        # Using your existing API key
        self.api_key = "AIzaSyCsb-NiyZwU5J-AitQan9HaHzNse2kN5_c"
       
    def get_gemini_response(self, prompt):
        try:
            API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={self.api_key}"
           
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": 0.3,  # Lower temperature for more professional responses
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 2048,  # Increased for detailed responses
                }
            }
           
            headers = {"Content-Type": "application/json"}
           
            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
           
            if response.status_code == 200:
                response_data = response.json()
                if 'candidates' in response_data and len(response_data['candidates']) > 0:
                    content = response_data['candidates'][0]['content']['parts'][0]['text']
                    return content
                else:
                    return "I apologize, but I couldn't generate a response. Please rephrase your professional inquiry."
            else:
                return f"System Error - API response code {response.status_code}. Please contact system administrator."
               
        except Exception as e:
            return f"Connection Error - Unable to process request: {str(e)}"

class CriminologyProfessionalBot:
    def __init__(self):
        self.gemini_api = GeminiAPI()
        
        # Professional contact directory for St. Kitts & Nevis
        self.professional_contacts = {
            "police_hq": {
                "name": "Royal St. Christopher and Nevis Police Force HQ",
                "phone": "(869) 465-2241",
                "email": "info@police.kn",
                "address": "Cayon Street, Basseterre",
                "departments": ["CID", "Traffic", "Community Policing", "Narcotics"]
            },
            "forensics": {
                "name": "Police Forensic Unit",
                "phone": "(869) 465-2241 ext. 234",
                "specialties": ["DNA Analysis", "Ballistics", "Digital Forensics", "Crime Scene Processing"]
            },
            "courts": {
                "high_court": {
                    "name": "Eastern Caribbean Supreme Court - St. Kitts Circuit",
                    "phone": "(869) 465-2366",
                    "address": "Government Road, Basseterre"
                },
                "magistrate": {
                    "name": "Magistrate's Court",
                    "phone": "(869) 465-2521",
                    "sessions": ["Criminal", "Civil", "Traffic"]
                }
            },
            "dpp": {
                "name": "Director of Public Prosecutions Office",
                "phone": "(869) 467-1000",
                "services": ["Case Review", "Legal Advice", "Prosecution Oversight"]
            }
        }

        # Legal framework for St. Kitts & Nevis
        self.legal_framework = {
            "primary_legislation": {
                "criminal_code": {
                    "title": "Criminal Code (St. Christopher and Nevis)",
                    "key_sections": {
                        "homicide": "Sections 87-102",
                        "assault": "Sections 56-74",
                        "theft": "Sections 201-250",
                        "fraud": "Sections 251-280",
                        "drug_offenses": "Drug Prevention of Misuse Act",
                        "domestic_violence": "Domestic Violence Act 2020"
                    }
                },
                "evidence_act": {
                    "title": "Evidence Act",
                    "key_provisions": ["Admissibility Rules", "Chain of Custody", "Expert Testimony"]
                }
            },
            "recent_amendments": [
                {
                    "date": "2023-03-15",
                    "act": "Cybercrime Act 2023",
                    "summary": "New provisions for digital evidence and online offenses"
                },
                {
                    "date": "2022-11-20",
                    "act": "Criminal Justice Reform Act 2022",
                    "summary": "Updated sentencing guidelines and plea bargaining procedures"
                }
            ]
        }

        # Crime investigation protocols
        self.investigation_protocols = {
            "crime_scene": {
                "initial_response": [
                    "Secure the perimeter",
                    "Document initial observations",
                    "Identify and separate witnesses",
                    "Call for appropriate specialists",
                    "Establish command post"
                ],
                "documentation": [
                    "Photography (wide, medium, close-up)",
                    "Sketch mapping",
                    "Evidence log",
                    "Witness statements",
                    "Environmental conditions"
                ]
            },
            "evidence_handling": {
                "collection": [
                    "Use appropriate collection tools",
                    "Maintain chain of custody",
                    "Proper packaging and labeling",
                    "Document location and condition",
                    "Witness the collection process"
                ],
                "storage": [
                    "Climate-controlled environment",
                    "Secure access controls",
                    "Regular inventory checks",
                    "Proper documentation",
                    "Contamination prevention"
                ]
            }
        }

        # Case management templates
        self.case_templates = {
            "incident_report": """
**INCIDENT REPORT TEMPLATE**

**Case Number:** [Auto-generated]
**Date/Time:** {datetime}
**Reporting Officer:** {officer}
**Location:** 

**INCIDENT DETAILS:**
- Type of Offense:
- Victim Information:
- Suspect Information:
- Witnesses:

**NARRATIVE:**
[Detailed description of incident]

**EVIDENCE COLLECTED:**
- Physical Evidence:
- Digital Evidence:
- Statements Taken:

**FOLLOW-UP REQUIRED:**
- Additional Investigation:
- Forensic Analysis:
- Court Preparation:

**Officer Signature:** ________________
**Supervisor Review:** ________________
            """,
            
            "case_analysis": """
**CASE ANALYSIS FRAMEWORK**

**Case ID:** {case_id}
**Primary Investigator:** {investigator}
**Case Type:** {case_type}

**FACTUAL ANALYSIS:**
1. Known Facts
2. Disputed Facts
3. Missing Information

**EVIDENCE EVALUATION:**
1. Physical Evidence Strength
2. Witness Reliability
3. Digital Evidence Integrity

**LEGAL CONSIDERATIONS:**
1. Applicable Statutes
2. Precedent Cases
3. Procedural Requirements

**INVESTIGATIVE STRATEGY:**
1. Priority Actions
2. Resource Requirements
3. Timeline Considerations

**RISK ASSESSMENT:**
1. Flight Risk
2. Public Safety
3. Evidence Preservation
            """
        }

        # Statistical data for different years
        self.crime_statistics = {
            "2024": {
                "total_reported": 1847,
                "by_category": {
                    "Violent Crimes": 267,
                    "Property Crimes": 891,
                    "Drug Offenses": 423,
                    "White Collar": 89,
                    "Cybercrimes": 177
                }
            },
            "2023": {
                "total_reported": 1956,
                "by_category": {
                    "Violent Crimes": 302,
                    "Property Crimes": 967,
                    "Drug Offenses": 368,
                    "White Collar": 72,
                    "Cybercrimes": 106,
                    "Traffic Violations": 141
                }
            },
            "2022": {
                "total_reported": 2134,
                "by_category": {
                    "Violent Crimes": 334,
                    "Property Crimes": 1045,
                    "Drug Offenses": 401,
                    "White Collar": 58,
                    "Cybercrimes": 63,
                    "Traffic Violations": 233
                }
            }
        }

    def create_professional_prompt(self, user_input, user_role, access_level):
        """Create specialized prompt based on user role and access level"""
        
        base_context = f"""
You are SECURO, a professional criminology assistant specifically designed for law enforcement and criminal justice professionals in St. Kitts and Nevis. 

**Current User Profile:**
- Role: {user_role}
- Access Level: {access_level}/5
- Jurisdiction: St. Kitts and Nevis

**Your Expertise Areas:**
- Criminal Law (St. Christopher and Nevis Criminal Code)
- Evidence Analysis and Chain of Custody
- Crime Scene Investigation Protocols
- Case Management and Documentation
- Statistical Analysis and Crime Trends
- Forensic Science Applications
- Legal Procedure and Court Preparation
- Community Policing Strategies
- Drug Enforcement (CARICOM protocols)
- Cybercrime Investigation
- Human Rights and Professional Ethics

**Local Legal Framework:**
- Criminal Code (St. Christopher and Nevis)
- Evidence Act
- Cybercrime Act 2023
- Domestic Violence Act 2020
- Drug Prevention of Misuse Act
- Police Act

**Communication Style:**
- Professional and precise
- Evidence-based recommendations
- Cite relevant legal sections when applicable
- Consider Caribbean legal context
- Maintain confidentiality and ethics
- Provide actionable guidance

**Query:** {user_input}

Please provide a comprehensive, professional response that considers the user's role and the specific legal and procedural context of St. Kitts and Nevis.
        """
        
        return base_context

    def get_case_template(self, template_type):
        """Return formatted case template"""
        if template_type in self.case_templates:
            template = self.case_templates[template_type]
            return template.format(
                datetime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                officer=st.session_state.current_user,
                case_id=f"SKN-{datetime.datetime.now().strftime('%Y%m%d')}-{hash(str(time.time())) % 1000:03d}",
                investigator=st.session_state.current_user,
                case_type="[To be specified]"
            )
        return "Template not found"

    def get_legal_reference(self, query):
        """Provide legal references based on query"""
        query_lower = query.lower()
        
        legal_response = "**LEGAL REFERENCE - ST. KITTS & NEVIS**\n\n"
        
        if any(word in query_lower for word in ["homicide", "murder", "killing"]):
            legal_response += """**HOMICIDE OFFENSES**
- **Criminal Code Sections 87-102**
- Murder: Life imprisonment (Section 87)
- Manslaughter: Up to 25 years (Section 92)
- Infanticide: Up to 3 years (Section 95)

**Key Procedural Notes:**
- Mandatory autopsy required
- Forensic pathologist must be engaged
- Scene preservation critical for 72+ hours
- Crown counsel consultation required pre-charge
            """
        
        elif any(word in query_lower for word in ["theft", "stealing", "larceny"]):
            legal_response += """**THEFT OFFENSES**
- **Criminal Code Sections 201-250**
- Simple theft: Up to 2 years (Section 201)
- Theft over $5,000: Up to 7 years
- Breaking and entering: Up to 14 years (Section 231)

**Evidence Requirements:**
- Proof of ownership
- Value assessment
- Intent to permanently deprive
- Identification evidence
            """
        
        elif any(word in query_lower for word in ["assault", "battery", "violence"]):
            legal_response += """**ASSAULT OFFENSES**
- **Criminal Code Sections 56-74**
- Common assault: Up to 1 year (Section 56)
- Assault causing bodily harm: Up to 2 years
- Aggravated assault: Up to 14 years (Section 58)

**Documentation Required:**
- Medical reports
- Photographs of injuries
- Witness statements
- Victim impact statement
            """
        
        else:
            legal_response += """**GENERAL LEGAL RESOURCES**

**Primary Legislation:**
- Criminal Code (St. Christopher and Nevis)
- Evidence Act
- Police Act
- Cybercrime Act 2023
- Domestic Violence Act 2020

**Key Contacts:**
- DPP Office: (869) 467-1000
- High Court Registry: (869) 465-2366
- Legal Aid: (869) 465-2521

For specific legal interpretations, consult with the Director of Public Prosecutions Office.
            """
        
        return legal_response

    def create_crime_statistics_chart(self, year):
        """Create crime statistics chart for a specific year"""
        if year not in self.crime_statistics:
            return None, f"Crime statistics for {year} are not available. Available years: {', '.join(self.crime_statistics.keys())}"
        
        data = self.crime_statistics[year]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        fig.patch.set_facecolor('black')
        
        # Pie chart
        categories = list(data["by_category"].keys())
        values = list(data["by_category"].values())
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#FF9FF3'][:len(categories)]
        
        ax1.pie(values, labels=categories, autopct='%1.1f%%', colors=colors, startangle=90,
               textprops={'color': 'white', 'fontsize': 11})
        ax1.set_title(f'Crime Distribution {year}', color='white', fontsize=16, pad=20)
        ax1.set_facecolor('black')
        
        # Bar chart
        bars = ax2.bar(categories, values, color=colors, alpha=0.8)
        ax2.set_title(f'Crime Statistics {year}', color='white', fontsize=16, pad=20)
        ax2.set_ylabel('Number of Cases', color='white')
        ax2.set_facecolor('black')
        ax2.tick_params(colors='white', rotation=45)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 5,
                    f'{int(height)}', ha='center', va='bottom', color='white', fontweight='bold')
        
        for spine in ax2.spines.values():
            spine.set_color('white')
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        return fig, f"**CRIME STATISTICS FOR {year}**\n\nTotal Reported Crimes: {data['total_reported']}\nChart generated showing distribution and breakdown by category."

    def process_professional_query(self, user_input):
        """Process queries with professional criminology focus"""
        user_input_lower = user_input.lower()
        user_role = st.session_state.get('user_role', 'Professional')
        access_level = st.session_state.get('access_level', 1)

        # Handle greetings first
        if any(greeting in user_input_lower for greeting in ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]):
            return f"""**Good day, Officer {st.session_state.current_user}!**

Welcome to SECURO - your professional crime mitigation assistant for St. Kitts and Nevis law enforcement.

**I'm here to assist you with:**
- Case documentation and analysis
- Legal references and criminal code queries
- Investigation protocols and procedures
- Crime statistics and intelligence analysis
- Professional contact directory
- Crime hotspot mapping
- Forensic guidance and evidence handling

**How may I assist with your professional duties today?**

*For crime mapping, just ask to "show crime map" or "display hotspots"*
*For statistics, specify a year (2022, 2023, or 2024)*
            """

        # Handle crime map requests
        elif any(word in user_input_lower for word in ["map", "hotspot", "crime map", "mapping", "location"]):
            return "crime_map_requested"

        # Handle statistics requests with year detection
        elif any(word in user_input_lower for word in ["statistics", "data", "trends", "numbers", "crimes"]):
            # Look for year in the query
            import re
            year_match = re.search(r'\b(20\d{2})\b', user_input)
            if year_match:
                year = year_match.group(1)
                fig, response = self.create_crime_statistics_chart(year)
                if fig:
                    st.pyplot(fig)
                return response
            else:
                return "Please specify a year for crime statistics (e.g., 'Show me crime statistics for 2024'). Available years: 2022, 2023, 2024"

        # Handle specific professional requests
        elif any(word in user_input_lower for word in ["template", "report", "form", "document"]):
            if "incident" in user_input_lower:
                return f"**INCIDENT REPORT TEMPLATE GENERATED**\n\n{self.get_case_template('incident_report')}"
            elif "analysis" in user_input_lower or "case" in user_input_lower:
                return f"**CASE ANALYSIS TEMPLATE GENERATED**\n\n{self.get_case_template('case_analysis')}"
        
        elif any(word in user_input_lower for word in ["legal", "law", "statute", "criminal code"]):
            return self.get_legal_reference(user_input)
        
        elif any(word in user_input_lower for word in ["contact", "phone", "directory", "reach"]):
            return self.get_professional_directory()
        
        elif any(word in user_input_lower for word in ["protocol", "procedure", "how to", "steps"]):
            return self.get_investigation_protocol(user_input)
        
        # Use Gemini AI for complex queries
        else:
            enhanced_prompt = self.create_professional_prompt(user_input, user_role, access_level)
            return self.gemini_api.get_gemini_response(enhanced_prompt)

    def get_professional_directory(self):
        """Return professional contact directory"""
        return """**PROFESSIONAL CONTACT DIRECTORY - ST. KITTS & NEVIS**

**POLICE HEADQUARTERS**
- **Phone:** (869) 465-2241
- **Address:** Cayon Street, Basseterre
- **Departments:** CID, Traffic, Community Policing, Narcotics

**FORENSIC SERVICES**
- **Phone:** (869) 465-2241 ext. 234
- **Services:** DNA, Ballistics, Digital Forensics, Crime Scene

**LEGAL SYSTEM**
- **High Court:** (869) 465-2366 (Government Road, Basseterre)
- **Magistrate Court:** (869) 465-2521
- **DPP Office:** (869) 467-1000

**MEDICAL EXAMINER**
- **Joseph N. France Hospital:** (869) 465-2551
- **Pathology Services:** Available on request

**ADMINISTRATIVE**
- **Court Registry:** (869) 465-2366
- **Legal Aid:** (869) 465-2521
- **Probation Services:** (869) 467-1234

**For inter-agency coordination, use official channels and maintain professional protocols.**
        """

    def get_investigation_protocol(self, query):
        """Return relevant investigation protocols"""
        query_lower = query.lower()
        
        if "crime scene" in query_lower:
            return """**CRIME SCENE INVESTIGATION PROTOCOL**

**INITIAL RESPONSE (First 30 minutes)**
1. Secure perimeter with barrier tape
2. Establish single entry/exit point
3. Document initial observations in notebook
4. Identify and separate witnesses
5. Call appropriate specialists (forensics, medical examiner)
6. Establish command post outside scene

**DOCUMENTATION PHASE**
1. **Photography:** Wide shots → Medium shots → Close-ups
2. **Sketching:** Rough sketch → Finished scale drawing
3. **Evidence Log:** Number, photograph, document each item
4. **Environmental:** Weather, lighting, temperature conditions

**EVIDENCE COLLECTION**
1. Use proper PPE (gloves, shoe covers, suits)
2. Work from outside → inside
3. Collect most fragile evidence first
4. Maintain chain of custody documentation
5. Package and label immediately

**CRITICAL REMINDERS**
- NEVER move evidence before documentation
- Maintain continuous security of scene
- Document ALL personnel who enter scene
- Consider contamination prevention throughout
            """
        
        elif "evidence" in query_lower:
            return """**EVIDENCE HANDLING PROTOCOL**

**COLLECTION STANDARDS**
- Use appropriate tools for each evidence type
- Avoid contamination through proper PPE
- Document exact location with coordinates/measurements
- Photograph evidence in situ before collection
- Use clean packaging for each item

**LABELING REQUIREMENTS**
- Case number
- Item number
- Date and time of collection
- Location found
- Collecting officer name and badge
- Brief description

**CHAIN OF CUSTODY**
- Document every person who handles evidence
- Note time, date, purpose of each transfer
- Use sealed evidence bags with tamper-evident tape
- Store in appropriate conditions (temperature, humidity)
- Maintain access log to evidence storage

**DOCUMENTATION**
- Evidence log with complete descriptions
- Photographs of evidence as collected
- Chain of custody forms
- Storage location records
            """
        
        else:
            return """**GENERAL INVESTIGATION PROTOCOLS**

**CASE INITIATION**
1. Complaint/report received
2. Initial assessment of allegations
3. Case file creation
4. Resource allocation
5. Investigation plan development

**INVESTIGATION PROCESS**
1. Evidence collection and preservation
2. Witness interviews
3. Suspect identification and questioning
4. Expert consultations
5. Case file compilation

**CASE COMPLETION**
1. Evidence review and analysis
2. Consultation with prosecutors
3. Charge recommendation
4. Court file preparation
5. Case closure documentation

**For specific protocols, consult the Police Operations Manual or contact your supervisor.**
            """

    def create_professional_crime_map(self):
        """Create detailed crime mapping for law enforcement"""
        # St. Kitts and Nevis coordinates
        st_kitts_center = [17.3578, -62.7822]
        
        # Create professional map
        m = folium.Map(
            location=st_kitts_center,
            zoom_start=11,
            tiles=None
        )
        
        # Add multiple tile layers for operational use
        folium.TileLayer(
            tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
            attr='Google Satellite',
            name='Satellite View',
            overlay=False,
            control=True
        ).add_to(m)
        
        folium.TileLayer(
            tiles='https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
            attr='Google Maps',
            name='Street Map',
            overlay=False,
            control=True
        ).add_to(m)
        
        folium.TileLayer(
            tiles='OpenStreetMap',
            name='OpenStreetMap',
            overlay=False,
            control=True
        ).add_to(m)
        
        # Police stations and key facilities
        police_stations = [
            {"name": "Police HQ", "coords": [17.2948, -62.7234], "type": "headquarters"},
            {"name": "Charlestown Station", "coords": [17.1372, -62.6219], "type": "station"},
            {"name": "Sandy Point Station", "coords": [17.3547, -62.8119], "type": "station"}
        ]
        
        for station in police_stations:
            icon_color = 'blue' if station['type'] == 'headquarters' else 'green'
            folium.Marker(
                location=station['coords'],
                popup=f"<b>{station['name']}</b><br>Type: {station['type'].title()}",
                icon=folium.Icon(color=icon_color, icon='shield', prefix='fa')
            ).add_to(m)
        
        # Crime hotspots with detailed data
        hotspots = [
            {"name": "Basseterre Central", "coords": [17.2948, -62.7234], "crimes": 450, 
             "types": "Property: 180, Violent: 89, Drug: 125, Other: 56", "risk": "High"},
            {"name": "Frigate Bay Area", "coords": [17.2619, -62.6853], "crimes": 180,
             "types": "Property: 95, Violent: 34, Drug: 28, Other: 23", "risk": "Medium"},
            {"name": "Sandy Point Town", "coords": [17.3547, -62.8119], "crimes": 120,
             "types": "Property: 67, Violent: 23, Drug: 19, Other: 11", "risk": "Medium"},
            {"name": "Charlestown", "coords": [17.1372, -62.6219], "crimes": 200,
             "types": "Property: 89, Violent: 45, Drug: 38, Other: 28", "risk": "Medium"},
            {"name": "Dieppe Bay", "coords": [17.4075, -62.8097], "crimes": 90,
             "types": "Property: 45, Violent: 18, Drug: 15, Other: 12", "risk": "Low"}
        ]
        
        for spot in hotspots:
            color = 'red' if spot['risk'] == 'High' else 'orange' if spot['risk'] == 'Medium' else 'green'
            folium.CircleMarker(
                location=spot['coords'],
                radius=spot['crimes']/25,
                popup=f"""<b>{spot['name']}</b><br>
                         <b>Total Incidents:</b> {spot['crimes']}<br>
                         <b>Breakdown:</b> {spot['types']}<br>
                         <b>Risk Level:</b> {spot['risk']}<br>
                         <b>Last Updated:</b> {datetime.datetime.now().strftime('%Y-%m-%d')}""",
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.7,
                weight=2
            ).add_to(m)
        
        # Add layer control
        folium.LayerControl().add_to(m)
        
        return m


def magnifying_glass_celebration():
    """Create professional magnifying glass celebration effect"""
    st.markdown("""
    <div id="magnify-container">
        <div class="magnify-celebration magnify-1"> </div>
        <div class="magnify-celebration magnify-2"> </div>
        <div class="magnify-celebration magnify-3"> </div>
        <div class="magnify-celebration magnify-4"> </div>
        <div class="magnify-celebration magnify-5"> </div>
        <div class="magnify-celebration magnify-6"> </div>
        <div class="magnify-celebration magnify-7"> </div>
        <div class="magnify-celebration magnify-8"> </div>
        <div class="magnify-celebration magnify-9"> </div>
        <div class="magnify-celebration magnify-10"> </div>
        <div class="magnify-celebration magnify-11"> </div>
        <div class="magnify-celebration magnify-12"> </div>
        <div class="magnify-celebration magnify-13"> </div>
        <div class="magnify-celebration magnify-14"> </div>
        <div class="magnify-celebration magnify-15"> </div>
    </div>
    <script>
        setTimeout(function() {
            document.getElementById('magnify-container').remove();
        }, 6000);
    </script>
    """, unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "professional_bot" not in st.session_state:
        st.session_state.professional_bot = CriminologyProfessionalBot()
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "current_user" not in st.session_state:
        st.session_state.current_user = None
    if "user_role" not in st.session_state:
        st.session_state.user_role = None
    if "access_level" not in st.session_state:
        st.session_state.access_level = 1
    if "auth" not in st.session_state:
        st.session_state.auth = UserAuthentication()

def show_professional_login():
    """Display professional login/registration page with crime scene background"""
    
    # Add login page class to body
    st.markdown('<div class="login-page">', unsafe_allow_html=True)
    st.markdown('<div class="login-content">', unsafe_allow_html=True)
    
    # SECURO Title with crime tape
    st.markdown('<h1 class="securo-title">SECURO</h1>', unsafe_allow_html=True)
    st.markdown('<div class="crime-tape"></div>', unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>CRIME MITIGATION AI CHAT BOT<br>Professional Access for St. Kitts & Nevis Law Enforcement</p>", unsafe_allow_html=True)
    
    # Security notice with enhanced styling
    st.markdown("""
    <div style="background: rgba(139, 0, 0, 0.8); padding: 15px; border-radius: 10px; border: 2px solid #FF0000; margin: 20px 0; text-align: center;">
        <h3 style="color: #FFFF00; margin: 0;">RESTRICTED ACCESS SYSTEM</h3>
        <p style="color: #ffffff; margin: 5px 0;">Authorized Personnel Only - Law Enforcement & Criminal Justice Professionals</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Login container
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Professional Login", "Register Professional Account"])
    
    with tab1:
        st.subheader("Access SECURO System")
        username = st.text_input("Professional Username", key="login_username", placeholder="Enter your professional username")
        password = st.text_input("Secure Password", type="password", key="login_password", placeholder="Enter your secure password")
        
        if st.button("ACCESS SECURO SYSTEM", use_container_width=True, type="primary"):
            if username and password:
                success, message = st.session_state.auth.login(username, password)
                if success:
                    st.success(f"Access Granted: {message}")
                    magnifying_glass_celebration()
                    time.sleep(3)
                    st.rerun()
                else:
                    st.error(f"Access Denied: {message}")
            else:
                st.error("Please enter your professional credentials")
    
    with tab2:
        st.subheader("Register Professional Account")
        st.warning("Professional verification required for account activation")
        
        new_username = st.text_input("Professional Username", key="new_username", placeholder="Choose a professional username")
        new_password = st.text_input("Secure Password (8+ characters)", type="password", key="new_password", placeholder="Create a strong password")
        confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password", placeholder="Confirm your password")
        
        role = st.selectbox("Professional Role", [
            "Senior Criminologist",
            "Detective", 
            "Police Officer",
            "Forensic Specialist",
            "Legal Advisor",
            "Researcher",
            "Student"
        ])
        
        badge_number = st.text_input("Badge/ID Number (if applicable)", placeholder="Enter badge or ID number")
        department = st.text_input("Department/Agency", placeholder="Enter your department or agency")
        
        if st.button("SUBMIT PROFESSIONAL REGISTRATION", use_container_width=True):
            if new_username and new_password and confirm_password:
                if new_password != confirm_password:
                    st.error("Passwords do not match")
                else:
                    success, message = st.session_state.auth.create_account(
                        new_username, new_password, role, badge_number, department
                    )
                    if success:
                        st.success(f"Registration Successful: {message}")
                        st.info("Your professional account has been created. You may now login to SECURO.")
                        magnifying_glass_celebration()
                    else:
                        st.error(f"Registration Failed: {message}")
            else:
                st.error("Please complete all required fields")
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close login-container
    st.markdown('</div>', unsafe_allow_html=True)  # Close login-content
    st.markdown('</div>', unsafe_allow_html=True)  # Close login-page

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
    
    # Check if user is logged in
    if not st.session_state.logged_in:
        show_professional_login()
        return
    
    # Professional header with credentials
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.write(f"**Officer:** {st.session_state.current_user}")
        st.write(f"**Role:** {st.session_state.user_role}")
        if st.session_state.get('badge_number'):
            st.write(f"**Badge:** {st.session_state.badge_number}")
        st.write(f"**Access Level:** {st.session_state.access_level}/5")
    
    with col2:
        st.markdown('<h1 class="securo-title">SECURO</h1>', unsafe_allow_html=True)
        st.markdown("<p class='subtitle'>CRIME MITIGATION AI CHAT BOT<br>Professional Intelligence System</p>", unsafe_allow_html=True)
    
    with col3:
        if st.button("Secure Logout", type="secondary"):
            # Clear all session data for security
            for key in ['logged_in', 'current_user', 'user_role', 'access_level', 'badge_number', 'department']:
                if key in st.session_state:
                    del st.session_state[key]
            st.session_state.messages = []
            st.rerun()

    bot = st.session_state.professional_bot

    # Sidebar toggle functionality
    if "sidebar_open" not in st.session_state:
        st.session_state.sidebar_open = True
    
    # Sidebar toggle button in header
    with col1:
        if st.button("☰ Menu", key="sidebar_toggle"):
            st.session_state.sidebar_open = not st.session_state.sidebar_open
            st.rerun()
    
    # Show sidebar only if open
    if st.session_state.sidebar_open:
        with st.sidebar:
            st.header(" Professional Tools")
            
            # System status - clean design
            st.markdown("""
            <div style="background: #1a4d1a; padding: 10px; border-radius: 8px; margin: 10px 0; text-align: center;">
                <strong> SYSTEM ONLINE</strong><br>
                <small>Officer: """ + st.session_state.user_role + """</small>
            </div>
            """, unsafe_allow_html=True)
            
            st.divider()
            
            # Emergency protocols - cleaner design
            st.subheader(" Emergency Response")
            
            # Emergency buttons with clean design
            col_a, col_b = st.columns(2)
            
            with col_a:
                if st.button(" \nPolice\nDispatch", use_container_width=True, help="Emergency: 911 | HQ: (869) 465-2241"):
                    st.markdown("""
                    <div style="background: #8B0000; padding: 15px; border-radius: 8px; color: white; text-align: center; margin: 10px 0;">
                        <h4> POLICE DISPATCH</h4>
                        <p><strong>Emergency:</strong> <a href="tel:911" style="color: #FFFF00;">911</a></p>
                        <p><strong>HQ Direct:</strong> <a href="tel:+18694652241" style="color: #FFFF00;">(869) 465-2241</a></p>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col_b:
                if st.button(" \nMedical\nEmergency", use_container_width=True, help="Emergency: 911 | Hospital: (869) 465-2551"):
                    st.markdown("""
                    <div style="background: #8B0000; padding: 15px; border-radius: 8px; color: white; text-align: center; margin: 10px 0;">
                        <h4> MEDICAL EMERGENCY</h4>
                        <p><strong>Emergency:</strong> <a href="tel:911" style="color: #FFFF00;">911</a></p>
                        <p><strong>Hospital:</strong> <a href="tel:+18694652551" style="color: #FFFF00;">(869) 465-2551</a></p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Legal emergency
            if st.button(" Legal/Court Emergency", use_container_width=True):
                st.markdown("""
                <div style="background: #8B0000; padding: 15px; border-radius: 8px; color: white; text-align: center; margin: 10px 0;">
                    <h4> LEGAL EMERGENCY</h4>
                    <p><strong>DPP Office:</strong> <a href="tel:+18694671000" style="color: #FFFF00;">(869) 467-1000</a></p>
                    <p><strong>Court Registry:</strong> <a href="tel:+18694652366" style="color: #FFFF00;">(869) 465-2366</a></p>
                </div>
                """, unsafe_allow_html=True)
            
            st.divider()
            
            # Professional resources
            st.subheader(" Case Management")
            
            if st.button(" Incident Report", use_container_width=True):
                template = bot.get_case_template('incident_report')
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"**INCIDENT REPORT TEMPLATE GENERATED**\n\n{template}"
                })
                st.rerun()
            
            if st.button(" Case Analysis", use_container_width=True):
                template = bot.get_case_template('case_analysis')
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"**CASE ANALYSIS FRAMEWORK GENERATED**\n\n{template}"
                })
                st.rerun()
            
            if st.button(" Legal Reference", use_container_width=True):
                legal_ref = bot.get_legal_reference("general")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": legal_ref
                })
                st.rerun()
            
            st.divider()
            
            # Professional directory
            st.subheader(" Contacts")
            
            if st.button(" Directory", use_container_width=True):
                directory = bot.get_professional_directory()
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": directory
                })
                st.rerun()
            
            st.divider()
            
            # System utilities
            st.subheader(" System")
            
            if st.button(" Clear Chat", use_container_width=True):
                st.session_state.messages = []
                st.success("Chat cleared.")
                st.rerun()
            
            # Clean system information
            st.divider()
            st.markdown("""
            <div style="background: #333; padding: 8px; border-radius: 5px; font-size: 12px; text-align: center;">
                <strong>SECURO v2.1</strong><br>
                St. Kitts & Nevis<br>
                """ + datetime.datetime.now().strftime('%Y-%m-%d %H:%M') + """
            </div>
            """, unsafe_allow_html=True)

    # Display chat messages
    chat_container = st.container()
    with chat_container:
        # Display all messages without automatic welcome
        for message in st.session_state.messages:
            display_message(message["role"], message["content"])

    # Professional chat input
    if prompt := st.chat_input("Enter case details, legal query, or request professional assistance..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Get professional response
        with st.spinner("Processing professional inquiry..."):
            response = bot.process_professional_query(prompt)
        
        # Handle special responses
        if response == "crime_map_requested":
            # Display crime map in main area
            with st.container():
                st.markdown("---")
                st.markdown('<div class="crime-map-container">', unsafe_allow_html=True)
                st.subheader(" St. Kitts & Nevis Crime Hotspot Map")
                st.markdown("*Interactive crime intelligence map showing current hotspots and police stations*")
                
                try:
                    crime_map = bot.create_professional_crime_map()
                    folium_static(crime_map, width=800, height=400)
                    
                    response = "**CRIME HOTSPOT MAP DISPLAYED ABOVE**\n\nThe interactive crime intelligence map shows:\n- Current crime hotspots with risk levels\n- Police station locations\n- Crime incident data by area\n- Multiple view layers (satellite, street, terrain)\n\nUse the map controls to zoom and switch between different views for tactical planning."
                    
                except Exception as e:
                    response = f"**MAP ERROR**: Unable to display crime map. Error: {str(e)}\n\nPlease try again or contact system administrator."
                
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown("---")
        
        # Add bot response
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

if __name__ == "__main__":
    main()
