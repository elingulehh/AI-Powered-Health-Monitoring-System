import streamlit as st
import streamlit_authenticator as stauth
import yaml
from data import load_user_data, add_user, add_health_record
from utils import preprocess_data

# Load config
with open('config.yaml') as file:
    config = yaml.safe_load(file)

# ---------------------------
# Authentication Setup
# ---------------------------
users = load_user_data()
if not users:
    # Default users for demo
    add_user('patient1', 'pass1', 'Patient', {'name': 'John Doe', 'age': 30})
    add_user('doctor1', 'pass1', 'Doctor', {'name': 'Dr. Smith', 'specialty': 'Cardiology'})
    users = load_user_data()

usernames = list(users.keys())
plaintext_passwords = [users[u]['password'] for u in usernames]
names = [users[u]['profile'].get('name', u) for u in usernames]

# Hash passwords with stauth.Hasher
hasher = stauth.Hasher()
hashed_passwords = hasher.hash_list(plaintext_passwords)

# Build credentials
credentials = {
    'usernames': {
        username: {
            'name': name,
            'password': hashed_pw
        } for username, name, hashed_pw in zip(usernames, names, hashed_passwords)
    }
}

authenticator = stauth.Authenticate(
    credentials,
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(
    page_title="AI Health Monitoring System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

authenticator.login(location='main')

# Get authentication status from session_state
name = st.session_state.get("name")
authentication_status = st.session_state.get("authentication_status")
username = st.session_state.get("username")

if authentication_status:
    st.sidebar.title(f"👋 {name}")
    authenticator.logout(button_name='Logout', location='sidebar')

    user_role = users[username]['role']
    user_profile = users[username]['profile']

    # Store in session_state for pages
    st.session_state.username = username
    st.session_state.user_role = user_role
    st.session_state.user_profile = user_profile

    # Sidebar controls
    st.sidebar.markdown("---")
    st.sidebar.header("⚙️ Simulation Settings")
    
    if user_role == 'Patient':
        with st.sidebar.expander("➕ Manual Data Entry"):
            heart_rate = st.number_input("Heart Rate (BPM)", 40, 180, 75)
            blood_oxygen = st.number_input("Blood Oxygen (%)", 80, 100, 98)
            temperature = st.number_input("Temperature (°C)", 35.0, 42.0, 36.5, step=0.1)
            respiration_rate = st.number_input("Respiration Rate", 8, 40, 16)
            activity_level = st.selectbox("Activity Level", ["low", "moderate", "high"])
            if st.button("Add Vitals", use_container_width=True):
                vitals = {
                    'heart_rate': heart_rate,
                    'blood_oxygen': blood_oxygen,
                    'temperature': temperature,
                    'respiration_rate': respiration_rate,
                    'activity_level': activity_level
                }
                add_health_record(username, vitals)
                st.success("✅ Vitals added!")

    st.sidebar.markdown("### Multi-User Simulation")
    num_users = st.sidebar.slider("Number of Users", 1, 10, 3, 
                                  help="Simulated users for anomaly detection")
    num_minutes = st.sidebar.slider("Minutes per User", 100, 1000, 300,
                                    help="Data points generated per user")
    contamination = st.sidebar.slider("Anomaly Rate", 0.01, 0.20, 0.05, 0.01,
                                     help="Expected percentage of anomalies")

    # Store simulation params in session_state
    st.session_state.num_users = num_users
    st.session_state.num_minutes = num_minutes
    st.session_state.contamination = contamination

    # Main welcome page
    st.title("🏥 AI-Powered Health Monitoring System")
    st.markdown("### Real-time Health Analytics with Machine Learning")
    
    # Feature cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        **🧪 Anomaly Detection**
        
        AI-powered anomaly detection using Isolation Forest algorithm with multi-user support and interactive visualizations.
        """)
    
    with col2:
        st.info("""
        **🔮 AI Predictions**
        
        LSTM neural networks for time-series forecasting of vital signs with confidence intervals.
        """)
    
    with col3:
        st.info("""
        **📊 Health Dashboard**
        
        Real-time monitoring with health scores, alerts, and personalized insights.
        """)
    
    # Instructions
    st.markdown("---")
    st.subheader("📖 Getting Started")
    
    if user_role == 'Patient':
        st.markdown("""
        **Welcome to your health monitoring dashboard!**
        
        1. **Dashboard** - View your current vitals and health trends
        2. **Anomaly Detection** - Simulate and analyze health data patterns
        3. **AI Predictions** - Get future health forecasts using LSTM
        4. **Reports** - Export your health data in multiple formats
        5. **Medications & Appointments** - Manage your healthcare schedule
        
        💡 **Tip:** Use the sidebar to manually add vitals or adjust simulation parameters.
        """)
    else:  # Doctor
        st.markdown("""
        **Welcome to the Doctor Dashboard!**
        
        1. **Dashboard** - Monitor patient vital signs and set alert thresholds
        2. **Anomaly Detection** - Analyze multi-patient health patterns
        3. **Patient Reports** - Review comprehensive patient health data
        
        💡 **Tip:** Select patients from the dashboard to view their health metrics.
        """)
    
    # System Status
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("User Role", user_role, delta="Active")
    with col2:
        st.metric("Simulation Users", num_users)
    with col3:
        st.metric("Data Points/User", num_minutes)
    with col4:
        st.metric("Anomaly Rate", f"{contamination*100}%")
    
    # Quick links
    st.markdown("---")
    st.markdown("### 🚀 Quick Navigation")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.page_link("pages/dashboard.py", label="📊 Dashboard", icon="📊")
    with col2:
        st.page_link("pages/anomaly_detection.py", label="🧪 Anomaly Detection", icon="🧪")
    with col3:
        st.page_link("pages/ai_predictions.py", label="🔮 AI Predictions", icon="🔮")
    with col4:
        st.page_link("pages/reports.py", label="📄 Reports", icon="📄")

elif authentication_status == False:
    st.error('❌ Username/password is incorrect')
    st.info("**Demo Credentials:**\n- Patient: `patient1` / `pass1`\n- Doctor: `doctor1` / `pass1`")
elif authentication_status == None:
    st.warning('Please enter your username and password')
    st.info("**Demo Credentials:**\n- Patient: `patient1` / `pass1`\n- Doctor: `doctor1` / `pass1`")
