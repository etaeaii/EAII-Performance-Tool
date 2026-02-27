import streamlit as st
import subprocess
import streamlit.components.v1 as components
from datetime import datetime, timedelta
import requests
import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import socket
import os
import hashlib
import json
import re
import base64
import zipfile
import html
import threading
import shlex
import platform
from uuid import uuid4
import logging
import time
import psutil
import uuid
import io
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Patch
from matplotlib import patheffects

# --- Streamlit App Configuration ---
st.set_page_config(
    page_title="EAII🚀PTT - Performance Testing Tool",
    page_icon="🦗",
    layout="wide",
)

# Define CSS styles (no Streamlit commands)
HIDE_UI_CSS = """
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display: none;}
.st-emotion-cache-zq5wmm {visibility: hidden;}
</style>
"""

# --- COSMIC STYLE CSS ---
st.markdown("""
<style>
:root {
    --cosmic-primary: #6a00ff;
    --cosmic-secondary: #00e5ff;
    --cosmic-dark: #0d0221;
    --cosmic-darker: #04000a;
    --cosmic-accent: #ff2a6d;
    --cosmic-text: #d1f7ff;
    --cosmic-neon: #05d9e8;
}
* { font-family: 'Comic Sans MS' }
h1, h2, h3, h4, h5, h6 {
    font-family: 'Comic Sans MS', sans-serif !important;
    color: var(--cosmic-secondary) !important;
    text-shadow: 0 0 5px var(--cosmic-neon);
}
            
.stButton>button {
    background: linear-gradient(90deg, var(--cosmic-primary), var(--cosmic-accent)) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 700 !important;
    box-shadow: 0 0 10px var(--cosmic-primary) !important;
}
.stButton>button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 0 20px var(--cosmic-accent) !important;
}
.stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>select {
    background-color: var(--cosmic-darker) !important;
    color: var(--cosmic-text) !important;
    border: 1px solid var(--cosmic-primary) !important;
    border-radius: 8px !important;
}
.stSidebar {
    background: linear-gradient(180deg, var(--cosmic-dark), var(--cosmic-darker)) !important;
    border-right: 1px solid var(--cosmic-primary) !important;
}
.stMarkdown { color: var(--cosmic-text) !important; }
.stProgress>div>div>div>div {
    background: linear-gradient(90deg, var(--cosmic-primary), var(--cosmic-accent)) !important;
}
.stDataFrame {
    background-color: var(--cosmic-darker) !important;
    border: 1px solid var(--cosmic-primary) !important;
    border-radius: 8px !important;
}
.stTabs [aria-selected="true"] {
    color: var(--cosmic-secondary) !important;
    border-bottom: 2px solid var(--cosmic-accent) !important;
}
.stAlert { border-left: 4px solid var(--cosmic-accent) !important; }
.stSuccess { background-color: rgba(0, 229, 255, 0.1) !important; border-left: 4px solid var(--cosmic-secondary) !important; }
.stWarning { background-color: rgba(255, 42, 109, 0.1) !important; border-left: 4px solid var(--cosmic-accent) !important; }
.stError { background-color: rgba(255, 42, 109, 0.2) !important; border-left: 4px solid var(--cosmic-accent) !important; }
.card {
    background: var(--cosmic-darker);
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    border: 1px solid var(--cosmic-primary);
    box-shadow: 0 0 15px var(--cosmic-primary);
    transition: transform 0.3s ease;
}
.card:hover {
    transform: translateY(-5px);
}
.card-header {
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--cosmic-secondary);
    text-shadow: 0 0 5px var(--cosmic-neon);
    margin-bottom: 1rem;
}

/* Apply to Streamlit components */
.stButton>button.nav-button {
    padding-left: 35px !important;
}
.stButton>button.nav-button:before {
    content: "→";
    position: absolute;
    left: 15px;
    color: white;
    text-shadow: 0 0 5px var(--cosmic-neon);
}
.stMarkdown { color: var(--cosmic-text) !important; }
.stProgress>div>div>div>div {
    background: linear-gradient(90deg, var(--cosmic-primary), var(--cosmic-accent)) !important;
}
.stDataFrame {
    background-color: var(--cosmic-darker) !important;
    border: 1px solid var(--cosmic-primary) !important;
    border-radius: 8px !important;
}
.stTabs [aria-selected="true"] {
    color: var(--cosmic-secondary) !important;
    border-bottom: 2px solid var(--cosmic-accent) !important;
}
.stAlert { border-left: 4px solid var(--cosmic-accent) !important; }
.stSuccess { background-color: rgba(0, 229, 255, 0.1) !important; border-left: 4px solid var(--cosmic-secondary) !important; }
.stWarning { background-color: rgba(255, 42, 109, 0.1) !important; border-left: 4px solid var(--cosmic-accent) !important; }
.stError { background-color: rgba(255, 42, 109, 0.2) !important; border-left: 4px solid var(--cosmic-accent) !important; }
.glow-text { text-shadow: 0 0 8px var(--cosmic-neon); }
.glow-box { box-shadow: 0 0 15px var(--cosmic-primary); }
.glow-border { border: 1px solid var(--cosmic-primary); box-shadow: 0 0 10px var(--cosmic-primary); }
.card {
    background: var(--cosmic-darker);
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    border: 1px solid var(--cosmic-primary);
    box-shadow: 0 0 15px var(--cosmic-primary);
    transition: transform 0.3s ease;
}
.metric-card {
        background: linear-gradient(135deg, var(--card-bg) 0%, rgba(12, 18, 38, 0.8) 100%);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        border: 1px solid var(--primary);
        transition: transform 0.3s ease;
    }

.card:hover {
    transform: translateY(-5px);
}
.card-header {
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--cosmic-secondary);
    text-shadow: 0 0 5px var(--cosmic-neon);
    margin-bottom: 1rem;
}
.metric-container {
    padding: 15px;
    border-radius: 10px;
    background: rgba(4, 0, 10, 0.5);
    border: 1px solid var(--cosmic-primary);
    min-height: 100px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    box-shadow: 0 0 10px var(--cosmic-primary);
}
.progress-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 15px;
}
.stop-button-container {
    margin-top: 20px;
    text-align: center;
}
.dashboard-container {
    margin-top: 20px;
    text-align: center;
}
.summary-card {
    background: var(--cosmic-darker);
    border-radius: 10px;
    padding: 1rem;
    margin: 1rem 0;
    border-left: 4px solid var(--cosmic-accent);
    box-shadow: 0 0 10px var(--cosmic-primary);
}
.summary-header {
    font-weight: 700;
    color: var(--cosmic-secondary);
    text-shadow: 0 0 5px var(--cosmic-neon);
    margin-bottom: 0.5rem;
}
.summary-metric {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.3rem;
}
.summary-label {
    color: var(--cosmic-text);
}
.summary-value {
    font-weight: 700;
    color: var(--cosmic-secondary);
}

.status-indicator {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    margin-right: 0.5rem;
}
.status-active {
    background: var(--cosmic-secondary);
    box-shadow: 0 0 8px var(--cosmic-neon);
}
.status-healthy {
    background-color: #00C853;
}
.status-warning {
    background-color: #FFC107;
}
.status-critical {
    background-color: #FF5252;
    animation: pulse 1.5s infinite;
}
.locust-active {
    color: var(--cosmic-secondary);
}
.locust-inactive {
    color: #FF5252;
}
@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(5, 217, 232, 0.7); }
    70% { box-shadow: 0 0 0 10px rgba(5, 217, 232, 0); }
    100% { box-shadow: 0 0 0 0 rgba(5, 217, 232, 0); }
}

</style>
""", unsafe_allow_html=True)


# Configuration
LOCUST_PORT = int(os.getenv("LOCUST_PORT", "8089").strip(' \\'))
STREAMLIT_PORT = int(os.getenv("PORT", 8501))
PUBLIC_HOST = os.getenv("PUBLIC_HOST", "localhost")  # Public hostname/IP


# --- CONFIGURATION ---
USER_DB_FILE = "user_credentials.json"
MAX_USERS_LIMITS = {
    "Load Test": 100000,
    "Stress Test": 100000,
    "Spike Test": 100000,
    "Endurance Test": 100000,
    "Volume Test": 100000,
    "Concurrency Test": 100000
}
DEFAULT_DURATIONS = {
    "Load Test": 1800,
    "Stress Test": 1800,
    "Spike Test": 600,
    "Endurance Test": 3600,
    "Volume Test": 2700,
    "Concurrency Test": 900
}

TEST_TYPE_DESCRIPTIONS = {
    "Load Test": "Simulates normal user load to evaluate system performance under typical conditions.",
    "Stress Test": "Tests system limits by applying load beyond normal capacity to identify breaking points.",
    "Spike Test": "Evaluates system response to sudden, extreme increases in user load.",
    "Endurance Test": "Assesses system stability over extended periods under sustained load.",
    "Volume Test": "Tests system performance with large data volumes to evaluate data handling.",
    "Concurrency Test": "Measures system performance with multiple simultaneous users."
}

# === Rating label mapping derived from test results ===
RATING_LABELS = {
    1: "Critical",
    2: "Warning",
    3: "Healthy (Acceptable)",
    4: "Healthy (Good)",
    5: "Healthy (Excellent)"
}

def get_rating_label(rating: int) -> str:
    """Return human-friendly label for a numeric rating (1-5)."""
    try:
        return RATING_LABELS.get(int(rating), "Unknown")
    except Exception:
        return "Unknown"



def rating_float_to_label_and_class(rating_float: float, rating_counts=None, total_metrics=None) -> tuple:
    """Map a float rating to a (label, css_class, stars) tuple."""
    try:
        r = float(rating_float)
    except Exception:
        r = 0.0

    # FIXED: No gaps, consistent logic
    if r < 2.0:  # Really bad: 0.0 to 1.99
        return "Critical", "critical", "⭐"
    elif r < 3.0:  # Bad: 2.0 to 2.99
        return "Warning", "warning", "⭐⭐"
    elif r < 3.5:  # OK: 3.0 to 3.49
        return "Healthy (Acceptable)", "healthy", "⭐⭐⭐"
    elif r < 4.5:  # Good: 3.5 to 4.49
        return "Healthy (Good)", "healthy", "⭐⭐⭐⭐"
    else:  # Excellent: 4.5+
        return "Healthy (Excellent)", "healthy", "⭐⭐⭐⭐⭐"



# Update ate_viz variable
ate_viz = True
    
if 'config' not in st.session_state:
    st.session_state.config = {}  # Initialize config to avoid AttributeError
    
if 'test_results' not in st.session_state:
    st.session_state.test_results = None
    
if 'test_error' not in st.session_state:
    st.session_state.test_error = None
    
if 'locust_output' not in st.session_state:
    st.session_state.locust_output = ""# --- SESSION STATE INIT ---
    
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"
    
if 'test_running' not in st.session_state:
    st.session_state.test_running = False
    
if 'locust_process' not in st.session_state:
    st.session_state.locust_process = None
    
if 'generate_viz' not in st.session_state:
    st.session_state.generate_viz = False
    
if 'config' not in st.session_state:
    st.session_state.config = {}  # Initialize config to avoid AttributeError
    
if 'test_results' not in st.session_state:
    st.session_state.test_results = None
    
if 'test_error' not in st.session_state:
    st.session_state.test_error = None
    
if 'locust_output' not in st.session_state:
    st.session_state.locust_output = ""

if 'system_stats' not in st.session_state:
    st.session_state.system_stats = {
        'cpu': 0,
        'memory': 0,
        'network': {'sent': 0, 'recv': 0},
        'locust_active': False,
        'last_updated': 0
    }

# Add initialization for selected_test_type
if 'selected_test_type' not in st.session_state:
    st.session_state.selected_test_type = list(MAX_USERS_LIMITS.keys())[0]  # Default to the first test type

# Initialize session state
if 'show_record_management' not in st.session_state:
    st.session_state.show_record_management = False

# Initialize session state variables if not already set
if "test_saved" not in st.session_state:
    st.session_state.test_saved = False
if "generate_viz" not in st.session_state:
    st.session_state.generate_viz = False
if "locust_process" not in st.session_state:
    st.session_state.locust_process = None
if "test_running" not in st.session_state:
    st.session_state.test_running = False

# --- HELPER FUNCTIONS ---

def format_timedelta(td):
    """Format timedelta into HH:MM:SS"""
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def calculate_dynamic_spawn_rate(users: int, duration_minutes: int) -> int:
    """Calculate dynamic spawn rate based on number of users."""
    return max(1, users // 100)

def check_locust_status():
    """Check if Locust server is running"""
    try:
        res = requests.get(f"http://localhost:{LOCUST_PORT}/", timeout=1)
        return res.status_code == 200
    except:
        return False

def update_system_stats():
    """Update system resource usage statistics."""
    now = time.time()
    # Only update if more than 1 second has passed since last update
    if now - st.session_state.system_stats['last_updated'] > 1:
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        network = psutil.net_io_counters()
        locust_active = check_locust_status()
        
        st.session_state.system_stats = {
            'cpu': cpu,
            'memory': memory,
            'network': {
                'sent': network.bytes_sent / (1024 * 1024),  # Convert to MB
                'recv': network.bytes_recv / (1024 * 1024)   # Convert to MB
            },
            'locust_active': locust_active,
            'last_updated': now
        }



def get_system_metrics():
    """
    Returns CPU usage %, Memory usage %, Network Sent (MB), Network Received (MB).
    """
    cpu_usage = psutil.cpu_percent(interval=0.5)
    mem_usage = psutil.virtual_memory().percent

    net_io = psutil.net_io_counters()
    net_sent = net_io.bytes_sent / (1024 * 1024)   # Convert to MB
    net_recv = net_io.bytes_recv / (1024 * 1024)   # Convert to MB

    return cpu_usage, mem_usage, net_sent, net_recv


def display_system_status():
    """Display system status cards in Streamlit sidebar with dynamic styling."""

    # Update CPU, Memory, Network metrics
    cpu_usage, mem_usage, net_sent, net_recv = get_system_metrics()
    st.session_state.system_stats.update({
        'cpu': cpu_usage,
        'memory': mem_usage,
        'network': {'sent': net_sent, 'recv': net_recv},
        'last_updated': time.time()
    })

    stats = st.session_state.system_stats

    # CPU status class
    cpu_class = "status-healthy" if stats['cpu'] <= 70 else \
                "status-warning" if stats['cpu'] <= 90 else "status-critical"

    # Memory status class
    mem_class = "status-healthy" if stats['memory'] <= 80 else \
                "status-warning" if stats['memory'] <= 90 else "status-critical"

    
    # CPU Card
    st.sidebar.markdown(f"""
    <div class="system-status">
        <div class="status-indicator {cpu_class}"></div>
        <div>CPU Usage: {stats["cpu"]:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

    # Memory Card
    st.sidebar.markdown(f"""
    <div class="system-status">
        <div class="status-indicator {mem_class}"></div>
        <div>Memory Usage: {stats["memory"]:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

    # Network Card
    st.sidebar.markdown(f"""
    <div class="system-status">
        <div class="status-indicator status-healthy"></div>
        <div>Network: ↑{stats["network"]["sent"]:.1f}MB ↓{stats["network"]["recv"]:.1f}MB</div>
    </div>
    """, unsafe_allow_html=True)


# --- UTILITY FUNCTIONS ---
def validate_target_url(url):
    """Validate the target URL format"""
    pattern = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(pattern, url) is not None


def format_duration_display(duration_field) -> str:
    """Return a human-friendly duration string in minutes.

    Accepts:
      - numeric seconds (int/float)
      - string with units (e.g., '3600 seconds')
      - plain numeric string (interpreted as minutes if it came from saved history)
    Outputs like: '60.0 minutes' or 'Unknown' on failure.
    """
    if duration_field is None:
        return "Unknown"

    # Numeric (assume seconds)
    if isinstance(duration_field, (int, float)):
        try:
            minutes = float(duration_field) / 60.0
            return f"{minutes:.1f} minutes"
        except Exception:
            return str(duration_field)

    # String handling
    s = str(duration_field).strip()
    if not s:
        return "Unknown"

    # Common patterns: '123 seconds', '123s', '123.0', '123.0 minutes'
    # If explicitly contains 'second' or ends with 's' with digits, parse as seconds
    sec_match = re.search(r'([+-]?\d+(?:\.\d+)?)\s*(seconds|second|secs|sec|s)\b', s, re.I)
    if sec_match:
        try:
            secs = float(sec_match.group(1))
            return f"{secs/60.0:.1f} minutes"
        except Exception:
            return s

    # If explicitly contains 'minute' or 'min', parse as minutes
    min_match = re.search(r'([+-]?\d+(?:\.\d+)?)\s*(minutes|minute|min)\b', s, re.I)
    if min_match:
        try:
            mins = float(min_match.group(1))
            return f"{mins:.1f} minutes"
        except Exception:
            return s

    # If plain numeric string, interpret as minutes (this matches existing history format)
    num_match = re.match(r'^([+-]?\d+(?:\.\d+)?)$', s)
    if num_match:
        try:
            mins = float(num_match.group(1))
            return f"{mins:.1f} minutes"
        except Exception:
            return s

    # Fallback
    return s

def get_test_config(test_type, users, spawn_rate, duration):
    """Return the test configuration with appropriate limits applied."""
    # Enforce max users from MAX_USERS_LIMITS
    max_users = MAX_USERS_LIMITS.get(test_type, 100000)
    users = min(users, max_users)

    # Duration enforcement based on test type
    default_duration = DEFAULT_DURATIONS.get(test_type, 600)
    if test_type in ["Load Test", "Stress Test"]:
        duration = min(duration, default_duration)
    elif test_type == "Spike Test":
        duration = min(duration, default_duration)
    elif test_type == "Endurance Test":
        duration = max(duration, default_duration)
    elif test_type == "Volume Test":
        duration = min(duration, default_duration)
    elif test_type == "Concurrency Test":
        duration = min(duration, default_duration)
    
    return {"users": users, "spawn": spawn_rate, "duration": duration}

def get_public_dashboard_url():
    """Get the public URL for the Locust dashboard"""
    return f"http://{PUBLIC_HOST}:{LOCUST_PORT}"

def start_locust_server(target_host):
    """Start Locust server process publicly accessible."""
    process = subprocess.Popen([
        "locust", 
        "-f", "locustfile.py", 
        "--host", target_host, 
        "--web-port", str(LOCUST_PORT),
        "--web-host", "0.0.0.0"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    st.session_state.locust_process = process

    # Force status active immediately
    if 'system_stats' not in st.session_state:
        st.session_state.system_stats = {}
    st.session_state.system_stats.update({
        'locust_active': True,
        'last_updated': time.time()
    })

    return process



def trigger_test(users, spawn_rate, host):
    """Trigger the Locust test with given parameters."""
    for _ in range(15):
        try:
            res = requests.post(
                f"http://localhost:{LOCUST_PORT}/swarm",  # Use configured port
                data={
                    "user_count": users,
                    "spawn_rate": spawn_rate,
                    "host": host
                }, 
                timeout=5
            )
            if res.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            time.sleep(1)
    return False

def stop_test():
    """Stop the running Locust test and clean up the process."""
    try:
        res = requests.get(f"http://localhost:{LOCUST_PORT}/stop", timeout=5)
        
        if 'locust_process' in st.session_state and st.session_state.locust_process:
            try:
                st.session_state.locust_process.terminate()
                st.session_state.locust_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                st.session_state.locust_process.kill()
            finally:
                st.session_state.locust_process = None
        
        # Immediately mark system status as inactive
        if 'system_stats' not in st.session_state:
            st.session_state.system_stats = {}
        st.session_state.system_stats.update({
            'locust_active': False,
            'last_updated': time.time(),
            'cpu': 0.0,   # optional: reset stats
            'memory': 0.0,
            'network': {'sent': 0.0, 'recv': 0.0}
        })

        return res.status_code == 200
    except requests.exceptions.RequestException:
        if 'locust_process' in st.session_state and st.session_state.locust_process:
            try:
                st.session_state.locust_process.kill()
            except:
                pass
            finally:
                st.session_state.locust_process = None
        
        # Ensure status is inactive even on error
        if 'system_stats' not in st.session_state:
            st.session_state.system_stats = {}
        st.session_state.system_stats.update({
            'locust_active': False,
            'last_updated': time.time(),
            'cpu': 0.0,
            'memory': 0.0,
            'network': {'sent': 0.0, 'recv': 0.0}
        })

        return False


def fetch_stats():
    """Fetch current statistics from Locust."""
    try:
        res = requests.get(f"http://localhost:{LOCUST_PORT}/stats/requests", timeout=5)
        if res.status_code == 200:
            return res.json()
    except requests.exceptions.RequestException:
        pass
    return None


def delete_test_record(test_id, test_history):
    try:
        # Find and remove test
        test_to_delete = next(t for t in test_history if t['test_id'] == test_id)
        
        # Delete graph file if exists
        if test_to_delete.get('graph_file') and os.path.exists(test_to_delete['graph_file']):
            os.remove(test_to_delete['graph_file'])
        
        # Update history
        updated_history = [t for t in test_history if t['test_id'] != test_id]
        with open('test_history/test_history.json', 'w') as f:
            json.dump(updated_history, f, indent=2)
            
        return True, f"Deleted test {test_id} and associated files"
        
    except Exception as e:
        return False, f"Deletion failed: {str(e)}"

def monitor_test(duration: int) -> pd.DataFrame:
    """Monitor the test progress with enhanced UI, phase tracking, and statistics collection."""
    # Initialize logging
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='app.log', level=logging.INFO)
    
    # Calculate test phases
    ramp_time = duration // 3
    steady_time = duration // 3
    ramp_down_time = duration // 3
    
    # Validate durations
    if ramp_time <= 0 or steady_time <= 0 or ramp_down_time <= 0:
        logger.error("Invalid phase durations")
        st.error("⚠️ Test duration too short - increase test duration")
        return pd.DataFrame()

    # Timeline calculation
    start_time = time.time()
    timeline = {
        'ramp_up_end': start_time + ramp_time,
        'steady_end': start_time + ramp_time + steady_time,
        'test_end': start_time + duration
    }
    
    # UI Setup with modern styling
    st.markdown("""
    <style>
        .metric-card {
            padding: 15px;
            background: rgba(25, 28, 36, 0.7);
            border-radius: 10px;
            margin-bottom: 15px;
            border: 1px solid #6a00ff;
        }
        .progress-card {
            padding: 15px;
            background: rgba(25, 28, 36, 0.7);
            border-radius: 10px;
            margin-bottom: 15px;
        }
        .phase-card {
            padding: 15px;
            background: rgba(25, 28, 36, 0.7);
            border-radius: 10px;
            margin-bottom: 15px;
        }
        .metric-container {
            padding: 15px;
            background: rgba(25, 28, 36, 0.5);
            border-radius: 10px;
            margin-bottom: 15px;
        }
        .notification {
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
        }
        .warning {
            background: rgba(255, 171, 0, 0.15);
            border-left: 4px solid #FFAB00;
        }
        .success {
            background: rgba(0, 200, 83, 0.15);
            border-left: 4px solid #00C853;
        }
        .dashboard-btn {
            display: block;
            text-align: center;
            padding: 15px;
            border-radius: 10px;
            text-decoration: none;
            background: linear-gradient(135deg, #6a00ff 0%, #ff2a6d 100%);
            color: white !important;
            font-weight: bold;
            margin: 20px 0;
        }
        .section-title {
            color: #ffffff; 
            border-bottom: 2px solid #6a00ff; 
            padding-bottom: 5px;
            margin-bottom: 15px;
        }
        .stop-btn {
            background-color: #ff4b4b !important;
            color: white !important;
            border: none !important;
        }
        .stop-btn:hover {
            background-color: #ff0000 !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # Create UI containers
    progress_placeholder = st.empty()
    phase_placeholder = st.empty()
    stats_placeholder = st.empty()
    dashboard_placeholder = st.empty()
    notification_placeholder = st.empty()
    control_placeholder = st.container()

    # Statistics collection
    stats = []
    
    # Control buttons
    with control_placeholder:
        stop_clicked = st.button(
            "🛑 Stop Test", 
            key="stop_test",
            help="Manually stop the running test",
            type="primary",
            use_container_width=True
        )
        if stop_clicked:
            st.session_state.manual_stop = True

    try:
        while time.time() < timeline['test_end'] and st.session_state.get("test_running", False):
            current_time = time.time()
            elapsed = current_time - start_time
            remaining = max(0, duration - elapsed)
            progress = min(max((elapsed / duration) * 100, 0), 100)

            # Check for manual stop
            if st.session_state.get('manual_stop', False):
                logger.info("Test stopped manually")
                notification_placeholder.markdown("""
                <div class="notification warning">
                    <h3>🛑 Test Stopped Manually</h3>
                    <p>The test was stopped before completion</p>
                </div>
                """, unsafe_allow_html=True)
                st.session_state.test_running = False
                break

            # Determine current phase and remaining time
            if current_time < timeline['ramp_up_end']:
                phase = "Ramp-Up"
                phase_color = "#6a00ff"
                phase_progress = min(max((elapsed / ramp_time) * 100, 0), 100)
                phase_remaining = timeline['ramp_up_end'] - current_time
            elif current_time < timeline['steady_end']:
                phase = "Steady-State"
                phase_color = "#00e5ff"
                phase_progress = min(max(((elapsed - ramp_time) / steady_time) * 100, 0), 100)
                phase_remaining = timeline['steady_end'] - current_time
            else:
                phase = "Ramp-Down"
                phase_color = "#ff2a6d"
                phase_progress = min(max(((elapsed - ramp_time - steady_time) / ramp_down_time) * 100, 0), 100)
                phase_remaining = timeline['test_end'] - current_time

            # Update progress display
            with progress_placeholder.container():
                st.markdown('<h3 class="section-title">📊 Test Progress</h3>', unsafe_allow_html=True)
                
                cols = st.columns(3)
                with cols[0]:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div style="font-size: 1rem; margin-bottom: 10px;">⏱️ Elapsed Time</div>
                        <div style="font-size: 1.5rem; font-weight: bold;">{format_timedelta(timedelta(seconds=elapsed))}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with cols[1]:
                    st.markdown(f"""
                    <div class="progress-card">
                        <div style="font-size: 1rem; margin-bottom: 5px;">Overall Progress ({progress:.1f}%)</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.progress(progress/100)
                    
                    st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 15px;">
                        <span style='color:{phase_color}; font-weight:bold;'>
                            {phase} ({phase_progress:.1f}%)
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
                    st.progress(phase_progress/100)
                
                with cols[2]:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div style="font-size: 1rem; margin-bottom: 10px;">⏳ Remaining Time</div>
                        <div style="font-size: 1.5rem; font-weight: bold;">{format_timedelta(timedelta(seconds=remaining))}</div>
                    </div>
                    """, unsafe_allow_html=True)

            # Phase information display
            with phase_placeholder.container():
                st.markdown("### Phase Information")
                col1, col2, col3 = st.columns([1, 1, 1], gap="medium")
                with col1:
                    st.markdown(f"""
                    <div class="metric-container">
                        <div style="font-size: 1.1rem; color: #00e5ff;">
                            <strong>📈 Current Phase:</strong><br>{phase}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                with col2:
                    st.markdown(f"""
                    <div class="metric-container">
                        <div style="font-size: 1.1rem; color: #d1f7ff;">
                            <strong>⏳ Phase Remaining:</strong><br>
                            {format_timedelta(timedelta(seconds=max(0, phase_remaining)))}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                with col3:
                    st.markdown(f"""
                    <div class="metric-container">
                        <div style="font-size: 1rem; color: #d1f7ff;">
                            <strong>🕒 Phase Durations:</strong><br>
                            • Ramp-Up: {format_timedelta(timedelta(seconds=ramp_time))}<br>
                            • Steady-State: {format_timedelta(timedelta(seconds=steady_time))}<br>
                            • Ramp-Down: {format_timedelta(timedelta(seconds=ramp_down_time))}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            # Collect and display statistics
            data = fetch_stats()
            if data and "stats" in data:
                total = next((item for item in data["stats"] if item["name"] == "Total"), None)
                if total:
                    stats.append({
                        "Timestamp": datetime.now().strftime("%H:%M:%S"),
                        "Phase": phase,
                        "Users": total.get("user_count", 0),
                        "Requests/s": round(total.get("total_rps", 0), 2),
                        "Avg Response (ms)": round(total.get("avg_response_time", 0), 2),
                        "Fail %": round(total.get("fail_ratio", 0) * 100, 2),
                        "95%ile (ms)": round(total.get("response_time_percentile_95", 0), 2),
                    })
                    
                    with stats_placeholder.container():
                        st.markdown('<h3 class="section-title">📈 Performance Metrics</h3>', unsafe_allow_html=True)
                        st.dataframe(pd.DataFrame(stats).tail(5), height=200)

            # Show dashboard link
            dashboard_placeholder.markdown(
                f'<a href="{get_public_dashboard_url()}" target="_blank" class="dashboard-btn">📊 Open Live Performance Dashboard</a>',
                unsafe_allow_html=True
            )

            time.sleep(1)  # Update every second

        # Test completed normally
        if time.time() >= timeline['test_end'] and st.session_state.get("test_running", False):
            notification_placeholder.markdown(f"""
            <div class="notification success">
                <h3>✅ Test Completed Successfully</h3>
                <p>Ran for {format_timedelta(timedelta(seconds=duration))}</p>
            </div>
            """, unsafe_allow_html=True)
            st.session_state.test_running = False

    except Exception as e:
        logger.error(f"Monitoring error: {str(e)}", exc_info=True)
        notification_placeholder.markdown(f"""
        <div class="notification warning">
            <h3>❌ Monitoring Error</h3>
            <p>{str(e)}</p>
        </div>
        """, unsafe_allow_html=True)
    finally:
        # Cleanup
        st.session_state.test_running = False
        stop_test()
        
        if st.session_state.get('manual_stop', False):
            notification_placeholder.markdown(f"""
            <div class="notification warning">
                <h3>🛑 Test Stopped</h3>
                <p>Stopped after {format_timedelta(timedelta(seconds=elapsed))}</p>
            </div>
            """, unsafe_allow_html=True)
        
        return pd.DataFrame(stats)



# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def save_test_history(test_data, graph_filename=None):
    """Save test data to the test history JSON file with duplicate prevention and robust validation."""
    history_file = "test_history/test_history.json"
    os.makedirs("test_history", exist_ok=True)

    # Ensure test_data has a test_id
    if "test_id" not in test_data:
        test_data["test_id"] = f"TEST_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

    # Validate and resolve users
    users = test_data.get("users")
    if users is None or users == "Unknown" or not str(users).strip():
        # Check config for users
        users = test_data.get("config", {}).get("users", None)
        if users is None or users == "Unknown" or not str(users).strip():
            logger.warning(f"No valid 'users' provided for test_id {test_data['test_id']}. Defaulting to 'Not Provided'.")
            users = "Not Provided"
        else:
            logger.info(f"Retrieved 'users' ({users}) from config for test_id {test_data['test_id']}.")
    else:
        try:
            users = int(users)  # Ensure users is a number if possible
        except (ValueError, TypeError):
            logger.warning(f"Invalid 'users' value {users} for test_id {test_data['test_id']}. Keeping as is.")

    # Validate and resolve duration, converting to minutes
    duration = test_data.get("duration")
    if duration is None or duration == "Unknown" or not str(duration).strip():
        # Calculate duration from stats if possible
        stats = test_data.get("stats", {})
        total_requests = stats.get("total_requests", 0)
        rps = stats.get("rps", 0)
        if rps > 0 and total_requests > 0:
            duration_seconds = total_requests / rps  # Duration in seconds
            duration = f"{round(duration_seconds / 60, 2)}"  # Convert to minutes
            logger.info(f"Calculated duration {duration} from stats for test_id {test_data['test_id']}.")
        else:
            logger.warning(f"Cannot calculate 'duration' for test_id {test_data['test_id']}. Defaulting to 'Not Provided'.")
            duration = "Not Provided"
    else:
        # Validate duration and convert to minutes
        try:
            # Handle duration as a number or string with 's' (seconds)
            if str(duration).endswith("s"):
                duration_seconds = float(str(duration).rstrip("s"))
            else:
                duration_seconds = float(duration)
            duration = f"{round(duration_seconds / 60, 2)}"  # Convert to minutes
        except (ValueError, TypeError):
            logger.warning(f"Invalid 'duration' format {duration} for test_id {test_data['test_id']}. Defaulting to 'Not Provided'.")
            duration = "Not Provided"

    # Prepare the test record
    test_record = {
        "test_id": test_data.get("test_id"),
        "project_name": test_data.get("project_name", "Unnamed"),
        "test_type": test_data.get("test_type", "Load"),
        "timestamp": test_data.get("timestamp", datetime.now().isoformat()),
        "users": users,
        "duration": duration,
        "overall_status": test_data.get("overall_status", "Unknown"),
        "stats": test_data.get("stats", {
            "total_requests": 0,
            "failures": 0,
            "rps": 0.0,
            "avg_response_time": 0.0,
            "p95_response_time": 0.0,
            "max_response_time": 0.0,
            "failures_rate": 0.0
        }),
        "graph_file": graph_filename if graph_filename and os.path.exists(graph_filename) else None
    }

    # Load existing history
    test_history = []
    try:
        if os.path.exists(history_file):
            with open(history_file, "r") as f:
                test_history = json.load(f)
                if not isinstance(test_history, list):
                    test_history = []
    except (json.JSONDecodeError, FileNotFoundError):
        test_history = []

    # Check for existing test with same ID
    existing_index = next((i for i, t in enumerate(test_history) 
                          if t["test_id"] == test_record["test_id"]), -1)

    if existing_index >= 0:
        # Update existing record
        test_history[existing_index] = test_record
        action = "updated"
    else:
        # Add new record
        test_history.append(test_record)
        action = "saved"

    # Load existing history
    test_history = []
    try:
        if os.path.exists(history_file):
            with open(history_file, "r") as f:
                test_history = json.load(f)
                if not isinstance(test_history, list):
                    test_history = []
    except (json.JSONDecodeError, FileNotFoundError):
        test_history = []

    # Append new test record
    test_history.append(test_record)

    # Save updated history
    try:
        with open(history_file, "w") as f:
            json.dump(test_history, f, indent=2)
        st.success(f"Test '{test_record['test_id']}' saved successfully! ✅")
    except Exception as e:
        st.error(f"Failed to save test history: {e}")
    


def display_test_history():
    """Display test history with proper formatting and filtering."""
    try:
        with open('test_history/test_history.json', 'r') as f:
            test_history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        test_history = []
        st.warning("No test history found. Run some tests first!")

    if not test_history:
        return

    # Get unique projects and test types
    projects = sorted({t['project_name'] for t in test_history})
    test_types = sorted({t['test_type'] for t in test_history})

    # Filters
    col1, col2 = st.columns(2)
    with col1:
        selected_project = st.selectbox(
            "Filter by Project",
            ["All Projects"] + projects,
            key="project_filter"
        )
        # Quick download when a specific project is selected
        if selected_project != "All Projects":
            colp1, colp2 = st.columns([3, 1])
            with colp1:
                inc_reports_now = st.checkbox("Include project reports", value=True, key=f"inc_reports_now_{selected_project}")
                inc_graphs_now = st.checkbox("Include project graphs", value=True, key=f"inc_graphs_now_{selected_project}")
            with colp2:
                if st.button("Download project ZIP", key=f"download_proj_zip_now_{selected_project}"):
                    project_tests = [t for t in test_history if t.get('project_name') == selected_project]
                    if not project_tests:
                        st.warning("No tests found for this project.")
                    else:
                        try:
                            zip_bytes = create_zip_for_project(selected_project, project_tests, inc_reports_now, inc_graphs_now)
                            safe_name = re.sub(r'[^A-Za-z0-9_-]', '_', selected_project.strip()).lower()
                            zip_name = f"{safe_name}_tests_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
                            st.download_button("Click to download ZIP", data=zip_bytes, file_name=zip_name, mime="application/zip", key=f"dl_proj_zip_now_{selected_project}")
                        except Exception as e:
                            st.error(f"Failed to create project archive: {e}")
    with col2:
        selected_type = st.selectbox(
            "Filter by Test Type",
            ["All Test Types"] + test_types,
            key="type_filter"
        )

    # Apply filters
    filtered = test_history
    if selected_project != "All Projects":
        filtered = [t for t in filtered if t['project_name'] == selected_project]
    if selected_type != "All Test Types":
        filtered = [t for t in filtered if t['test_type'] == selected_type]

    # Sort by timestamp (newest first)
    filtered.sort(key=lambda x: x.get('timestamp', ''), reverse=True)

    # Display summary stats
    healthy = sum(1 for t in filtered if t.get('overall_status', '').startswith('✅'))
    warning = sum(1 for t in filtered if t.get('overall_status', '').startswith('⚠️'))
    critical = sum(1 for t in filtered if t.get('overall_status', '').startswith('❌'))

    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; margin: 1rem 0;">
        <div style="flex: 1; text-align: center; background: #d4edda; padding: 1rem; border-radius: 8px;">
            <h3>✅ Healthy</h3>
            <p style="font-size: 1.5rem; font-weight: bold;">{healthy}</p>
        </div>
        <div style="flex: 1; text-align: center; background: #fff3cd; padding: 1rem; border-radius: 8px; margin: 0 1rem;">
            <h3>⚠️ Warning</h3>
            <p style="font-size: 1.5rem; font-weight: bold;">{warning}</p>
        </div>
        <div style="flex: 1; text-align: center; background: #f8d7da; padding: 1rem; border-radius: 8px;">
            <h3>❌ Critical</h3>
            <p style="font-size: 1.5rem; font-weight: bold;">{critical}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Display each test
    for test in filtered:
        with st.expander(f"{test['test_type']} - {test['project_name']} - {test['test_id']}", expanded=False):
            cols = st.columns([1, 1, 1, 1])
            
            with cols[0]:
                st.metric("Status", test.get('overall_status', 'Unknown'))
                st.metric("Users", test.get('users', 'Unknown'))
                
            with cols[1]:
                # Use format helper to display duration correctly regardless of stored format
                st.metric("Duration", format_duration_display(test.get('duration')))
                st.metric("Requests", test['stats'].get('total_requests', 0))
                
            with cols[2]:
                st.metric("RPS", f"{test['stats'].get('rps', 0):.1f}")
                st.metric("Avg Response", f"{test['stats'].get('avg_response_time', 0):.1f} ms")
                
            with cols[3]:
                st.metric("Fail Rate", f"{test['stats'].get('failures_rate', 0):.1f}%")
                st.metric("95th %ile", f"{test['stats'].get('p95_response_time', 0):.1f} ms")

            # Generate and display report
            if st.button(f"📄 Generate Report for {test['test_id']}"):
                html_report = generate_html_report(test)
                st.download_button(
                    label="⬇️ Download HTML Report",
                    data=html_report,
                    file_name=f"report_{test['test_id']}.html",
                    mime="text/html"
                )
                # Save and render inline for quick preview
                

            # Delete button
            if st.button(f"🗑️ Delete {test['test_id']}"):
                success, message = delete_test_record(test['test_id'], test_history)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)


def generate_performance_graph(actual_performance, test_type, total_requests, failures_rate):
    """Generate a performance dashboard with fallback on error."""
    try:
        # ========== CONFIGURATION ========== #
        STATUS_CONFIG = {
            "Excellent": {"threshold": 0.9, "color": "#00C853", "description": "Performance exceeding expectations"},
            "Good": {"threshold": 0.75, "color": "#64DD17", "description": "Solid performance within targets"},
            "Acceptable": {"threshold": 0.5, "color": "#FFD600", "description": "Performance meeting minimum requirements"},
            "Warning": {"threshold": 0.25, "color": "#FF9100", "description": "Performance requires attention"},
            "Critical": {"threshold": 0.0, "color": "#FF5252", "description": "Immediate action required"}
        }

        STANDARDS = {
            "load": {
                "display_name": "Load Test",
                "metrics": {
                    "Requests Per Second (RPS)": {"target": 500, "warning": 400, "critical": 300},
                    "95th Percentile Response Time (ms)": {"target": 800, "warning": 1000, "critical": 1500},
                    "Average Response Time (ms)": {"target": 300, "warning": 500, "critical": 800},
                    "Max Response Time (ms)": {"target": 4000, "warning": 6000, "critical": 10000},
                    "Failure Rate (%)": {"target": 0, "warning": 3, "critical": 5}
                }
            },
            "concurrency": {
                "display_name": "Concurrency Test",
                "metrics": {
                    "Requests Per Second (RPS)": {"target": 280, "warning": 200, "critical": 150},
                    "95th Percentile Response Time (ms)": {"target": 900, "warning": 1200, "critical": 1800},
                    "Average Response Time (ms)": {"target": 400, "warning": 600, "critical": 800},
                    "Max Response Time (ms)": {"target": 5000, "warning": 7000, "critical": 10000},
                    "Failure Rate (%)": {"target": 0, "warning": 5, "critical": 8}
                }
            },
            "spike": {
                "display_name": "Spike Test",
                "metrics": {
                    "Requests Per Second (RPS)": {"target": 350, "warning": 250, "critical": 150},
                    "95th Percentile Response Time (ms)": {"target": 1200, "warning": 1800, "critical": 2500},
                    "Average Response Time (ms)": {"target": 500, "warning": 800, "critical": 1200},
                    "Max Response Time (ms)": {"target": 6000, "warning": 9000, "critical": 15000},
                    "Failure Rate (%)": {"target": 0, "warning": 10, "critical": 15}
                }
            },
            "volume": {
                "display_name": "Volume Test",
                "metrics": {
                    "Requests Per Second (RPS)": {"target": 400, "warning": 300, "critical": 200},
                    "95th Percentile Response Time (ms)": {"target": 500, "warning": 800, "critical": 1200},
                    "Average Response Time (ms)": {"target": 200, "warning": 300, "critical": 500},
                    "Max Response Time (ms)": {"target": 3000, "warning": 5000, "critical": 8000},
                    "Failure Rate (%)": {"target": 0, "warning": 1, "critical": 3}
                }
            },
            "stress": {
                "display_name": "Stress Test",
                "metrics": {
                    "Requests Per Second (RPS)": {"target": 200, "warning": 150, "critical": 100},
                    "95th Percentile Response Time (ms)": {"target": 2000, "warning": 3000, "critical": 5000},
                    "Average Response Time (ms)": {"target": 800, "warning": 1200, "critical": 2000},
                    "Max Response Time (ms)": {"target": 10000, "warning": 15000, "critical": 30000},
                    "Failure Rate (%)": {"target": 0, "warning": 15, "critical": 20}
                }
            },
            "endurance": {
                "display_name": "Endurance Test",
                "metrics": {
                    "Requests Per Second (RPS)": {"target": 150, "warning": 100, "critical": 50},
                    "95th Percentile Response Time (ms)": {"target": 1000, "warning": 1500, "critical": 2500},
                    "Average Response Time (ms)": {"target": 400, "warning": 600, "critical": 1000},
                    "Max Response Time (ms)": {"target": 5000, "warning": 8000, "critical": 15000},
                    "Failure Rate (%)": {"target": 0, "warning": 5, "critical": 10}
                }
            }
        }

        UI_CONFIG = {
            "figure_size": (14, 8), "bar_width": 0.6, "title_fontsize": 18,
            "metric_fontsize": 12, "value_fontsize": 11, "legend_fontsize": 10,
            "grid_alpha": 0.15, "bar_edge_width": 1.2, "background_color": "#F5F5F5",
            "text_color": "#212121", "secondary_text": "#616161", "border_color": "#BDBDBD"
        }

        # Normalize test type
        normalized_test_type = test_type.lower().strip()
        matched_test = None
        for test_key in STANDARDS:
            if normalized_test_type in [test_key, STANDARDS[test_key]["display_name"].lower()]:
                matched_test = test_key
                break
        if not matched_test:
            matched_test = "load"   # fallback

        test_config = STANDARDS[matched_test]
        metrics_config = test_config["metrics"]

        # Process performance data
        if isinstance(actual_performance, list):
            metric_names = list(metrics_config.keys())
            actual_performance = dict(zip(metric_names, actual_performance))

        standardized_data = {}
        for metric, value in actual_performance.items():
            try:
                standardized_data[metric] = float(value)
            except (ValueError, TypeError):
                standardized_data[metric] = 0

        # Prepare visualization data
        metrics = []
        actual_values = []
        targets = []
        warnings = []
        criticals = []
        statuses = []
        status_colors = []

        for metric, config in metrics_config.items():
            if metric in standardized_data:
                actual_value = standardized_data[metric]
                target = config["target"]
                warning = config["warning"]
                critical = config["critical"]

                # Calculate performance ratio
                if metric == 'Failure Rate (%)':
                    ratio = 1 - (actual_value / max(1, critical))
                else:
                    if 'Response Time' in metric:
                        ratio = target / max(1, actual_value)
                    else:
                        ratio = actual_value / max(1, target)

                # Determine status
                status = "Critical"
                for level_name, level_config in STATUS_CONFIG.items():
                    if ratio >= level_config["threshold"]:
                        status = level_name
                        break

                metrics.append(metric)
                actual_values.append(actual_value)
                targets.append(target)
                warnings.append(warning)
                criticals.append(critical)
                statuses.append(status)
                status_colors.append(STATUS_CONFIG[status]["color"])

        # ========== VISUALIZATION ========== #
        plt.style.use('default')
        fig, ax = plt.subplots(figsize=UI_CONFIG["figure_size"])
        fig.patch.set_facecolor(UI_CONFIG["background_color"])
        ax.set_facecolor(UI_CONFIG["background_color"])

        y_pos = np.arange(len(metrics))
        bars = ax.barh(y_pos, actual_values, UI_CONFIG["bar_width"],
                       color=status_colors, edgecolor='white',
                       linewidth=UI_CONFIG["bar_edge_width"], zorder=3)

        for bar in bars:
            bar.set_path_effects([patheffects.SimpleLineShadow(offset=(0.5, -0.5)),
                                  patheffects.Normal()])

        for i, (value, status) in enumerate(zip(actual_values, statuses)):
            ax.text(value + max(targets)*0.02, i,
                    f'{value:.0f}{"%" if metrics[i] == "Failure Rate (%)" else ""}\n({status})',
                    va='center', ha='left',
                    fontsize=UI_CONFIG["value_fontsize"], fontweight='bold',
                    color=UI_CONFIG["text_color"], linespacing=1.2,
                    bbox=dict(facecolor='white', alpha=0.8,
                              edgecolor=UI_CONFIG["border_color"],
                              boxstyle='round,pad=0.3'))

        for i, (target, warning, critical) in enumerate(zip(targets, warnings, criticals)):
            ax.fill_betweenx([i-0.3, i+0.3], target, warning,
                             color=STATUS_CONFIG["Warning"]["color"], alpha=0.1, zorder=1)
            ax.fill_betweenx([i-0.3, i+0.3], warning, critical,
                             color=STATUS_CONFIG["Critical"]["color"], alpha=0.1, zorder=1)

            if metrics[i] == 'Failure Rate (%)':
                for val, label, color in [
                    (target, 'TARGET', UI_CONFIG["text_color"]),
                    (warning, 'WARNING', STATUS_CONFIG["Warning"]["color"]),
                    (critical, 'CRITICAL', STATUS_CONFIG["Critical"]["color"])
                ]:
                    ax.text(val, i+0.4, label, ha='center', va='bottom',
                            color=color, fontsize=UI_CONFIG["value_fontsize"]-1,
                            fontweight='bold',
                            path_effects=[patheffects.withStroke(linewidth=3, foreground='white')])

        ax.set_yticks(y_pos)
        ax.set_yticklabels(metrics, fontsize=UI_CONFIG["metric_fontsize"],
                           fontweight='bold', color=UI_CONFIG["text_color"])
        ax.tick_params(axis='x', which='both', bottom=False, labelbottom=False)
        ax.grid(True, axis='x', color='white', linestyle='-', linewidth=1, alpha=0.8)
        ax.grid(True, axis='y', color=UI_CONFIG["border_color"],
                linestyle='--', linewidth=0.7, alpha=0.5)

        for spine in ax.spines.values():
            spine.set_color(UI_CONFIG["border_color"])
            spine.set_linewidth(1.2)

        ax.set_title(f"{test_config['display_name']} PERFORMANCE DASHBOARD\n",
                     fontsize=UI_CONFIG["title_fontsize"], fontweight='bold', pad=20,
                     color=UI_CONFIG["text_color"])
        ax.text(0.5, 1.03,
                f"Total Requests: {int(total_requests):,} | Failure Rate: {float(failures_rate):.2f}%",
                transform=ax.transAxes, ha='center', va='bottom',
                fontsize=UI_CONFIG["metric_fontsize"], color=UI_CONFIG["secondary_text"])

        legend_elements = []
        for level_name, level_config in STATUS_CONFIG.items():
            legend_elements.append(
                Patch(facecolor=level_config["color"], edgecolor='white',
                      label=f"{level_name}: {level_config['description']}")
            )
        legend_elements.extend([
            Patch(facecolor=STATUS_CONFIG["Warning"]["color"], alpha=0.1, label='Warning Zone'),
            Patch(facecolor=STATUS_CONFIG["Critical"]["color"], alpha=0.1, label='Critical Zone')
        ])

        ax.legend(handles=legend_elements, loc='lower center',
                  bbox_to_anchor=(0.5, -0.2), ncol=2,
                  frameon=True, framealpha=1,
                  facecolor='white', edgecolor=UI_CONFIG["border_color"],
                  fontsize=UI_CONFIG["legend_fontsize"])

        plt.tight_layout(rect=[0, 0.1, 1, 0.95])
        return fig

    except Exception as e:
        # Log the error (optional)
        print(f"Error generating performance graph: {e}")
        # Create a fallback figure with error message
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.text(0.5, 0.5, f"Graph generation failed.\nError: {e}",
                ha='center', va='center', fontsize=14, color='red',
                transform=ax.transAxes)
        ax.set_title("Performance Graph Error", fontsize=16)
        ax.axis('off')
        return fig


def generate_html_report(test_data):
    """Generate HTML report with concise next steps for critical issues."""
    # Normalize test_type
    test_type_mapping = {
        "load": "Load",
        "concurrency": "Concurrency",
        "stress": "Stress",
        "spike": "Spike",
        "volume": "Volume",
        "endurance": "Endurance"
    }

    # Data Extraction and Validation
    def extract_test_metadata():
        """Extract and validate basic test information."""
        raw_test_type = test_data.get("test_type", "Load").lower()
        test_type = test_type_mapping.get(raw_test_type, "Load")
        
        users = test_data.get("users", None)
        duration = test_data.get("duration", None)
        
        # Normalize duration to a human-friendly minutes string
        duration_display = format_duration_display(duration)

        return {
            "test_type": test_type,
            "project_name": test_data.get("project_name", "Unnamed Project"),
            "test_id": test_data.get("test_id", str(uuid.uuid4())[:8]),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M %p"),
            "users": "Unknown" if users is None or users <= 0 else str(users),
            "duration": duration_display,
            "warnings": get_data_warnings(users, duration)
        }

    def get_data_warnings(users, duration):
        """Generate warnings for missing/invalid data."""
        warnings = []
        if users is None or users <= 0:
            warnings.append("Warning: Number of users is missing or invalid")
        if duration is None or duration <= 0:
            warnings.append("Warning: Test duration is missing or invalid")
        return warnings

    def extract_performance_metrics():
        """Extract and normalize performance metrics."""
        stats = test_data.get("stats", {})
        return {
            "total_requests": stats.get("total_requests", 0),
            "failures_rate": stats.get("failures_rate", 0),
            "rps": stats.get("rps", 0),
            "avg_response": stats.get("avg_response_time", 0),
            "p95_response": stats.get("p95_response_time", 0),
            "max_response": stats.get("max_response_time", 0)
        }


    # Extract metadata and metrics
    metadata = extract_test_metadata()
    test_type = metadata["test_type"]
    project_name = metadata["project_name"]
    test_id = metadata["test_id"]
    timestamp = metadata["timestamp"]
    users_display = metadata["users"]
    duration_display = metadata["duration"]
    warnings = metadata["warnings"]

    metrics = extract_performance_metrics()
    total_requests = metrics["total_requests"]
    failures_rate = metrics["failures_rate"]
    rps = metrics["rps"]
    avg_response = metrics["avg_response"]
    p95_response = metrics["p95_response"]
    max_response = metrics["max_response"]

    # Test type descriptions
    test_type_descriptions = {
        "Load": """
            <p>Load testing evaluates system behavior under expected and peak load conditions.
            Measures throughput, response times, and resource utilization to identify performance
            bottlenecks at various load levels.</p>
            <p><strong>Key Focus:</strong> Maximum operating capacity, breaking point identification,
            and performance under sustained load.</p>
        """,
        "Concurrency": """
            <p>Concurrency testing examines how the system handles multiple users performing
            the same or different actions simultaneously. Identifies race conditions,
            deadlocks, and thread synchronization issues.</p>
            <p><strong>Key Focus:</strong> Multi-user scenarios, session management,
            and shared resource contention.</p>
        """,
        "Stress": """
            <p>Stress testing pushes the system beyond normal operational capacity to evaluate
            robustness and error handling under extreme conditions. Determines failure points
            and recovery mechanisms.</p>
            <p><strong>Key Focus:</strong> System stability at beyond-peak loads, graceful
            degradation, and recovery procedures.</p>
        """,
        "Spike": """
            <p>Spike testing evaluates system behavior when subjected to sudden and extreme
            increases in load. Measures how quickly the system can scale and whether it can
            handle rapid fluctuations.</p>
            <p><strong>Key Focus:</strong> Elasticity, auto-scaling capabilities, and
            response to sudden traffic bursts.</p>
        """,
        "Volume": """
            <p>Volume testing subjects the system to large amounts of data to verify stability
            and performance. Checks for memory leaks, storage limitations, and data processing
            efficiency.</p>
            <p><strong>Key Focus:</strong> Database performance, memory management, and
            large dataset handling.</p>
        """,
        "Endurance": """
            <p>Endurance testing evaluates system reliability over extended periods. Identifies
            performance degradation, memory leaks, or resource exhaustion.</p>
            <p><strong>Key Focus:</strong> Long-term stability, memory management, and
            sustained performance metrics.</p>
        """
    }

    test_description = test_type_descriptions.get(test_type, test_type_descriptions["Load"])

    # Define standards dictionary
    standards = {
        "load": {
            "display_name": "Load Test",
            "metrics": {
                "Requests Per Second (RPS)": {"target": 500, "warning": 400, "critical": 300},
                "95th Percentile Response Time (ms)": {"target": 800, "warning": 1000, "critical": 1500},
                "Average Response Time (ms)": {"target": 300, "warning": 500, "critical": 800},
                "Max Response Time (ms)": {"target": 4000, "warning": 6000, "critical": 10000},
                "Failure Rate (%)": {"target": 0, "warning": 3, "critical": 5}
            }
        },
        "concurrency": {
            "display_name": "Concurrency Test",
            "metrics": {
                "Requests Per Second (RPS)": {"target": 280, "warning": 200, "critical": 150},
                "95th Percentile Response Time (ms)": {"target": 900, "warning": 1200, "critical": 1800},
                "Average Response Time (ms)": {"target": 400, "warning": 600, "critical": 800},
                "Max Response Time (ms)": {"target": 5000, "warning": 7000, "critical": 10000},
                "Failure Rate (%)": {"target": 0, "warning": 5, "critical": 8}
            }
        },
        "spike": {
            "display_name": "Spike Test",
            "metrics": {
                "Requests Per Second (RPS)": {"target": 350, "warning": 250, "critical": 150},
                "95th Percentile Response Time (ms)": {"target": 1200, "warning": 1800, "critical": 2500},
                "Average Response Time (ms)": {"target": 500, "warning": 800, "critical": 1200},
                "Max Response Time (ms)": {"target": 6000, "warning": 9000, "critical": 15000},
                "Failure Rate (%)": {"target": 0, "warning": 10, "critical": 15}
            }
        },
        "volume": {
            "display_name": "Volume Test",
            "metrics": {
                "Requests Per Second (RPS)": {"target": 400, "warning": 300, "critical": 200},
                "95th Percentile Response Time (ms)": {"target": 500, "warning": 800, "critical": 1200},
                "Average Response Time (ms)": {"target": 200, "warning": 300, "critical": 500},
                "Max Response Time (ms)": {"target": 3000, "warning": 5000, "critical": 8000},
                "Failure Rate (%)": {"target": 0, "warning": 1, "critical": 3}
            }
        },
        "stress": {
            "display_name": "Stress Test",
            "metrics": {
                "Requests Per Second (RPS)": {"target": 200, "warning": 150, "critical": 100},
                "95th Percentile Response Time (ms)": {"target": 2000, "warning": 3000, "critical": 5000},
                "Average Response Time (ms)": {"target": 800, "warning": 1200, "critical": 2000},
                "Max Response Time (ms)": {"target": 10000, "warning": 15000, "critical": 30000},
                "Failure Rate (%)": {"target": 0, "warning": 15, "critical": 20}
            }
        },
        "endurance": {
            "display_name": "Endurance Test",
            "metrics": {
                "Requests Per Second (RPS)": {"target": 150, "warning": 100, "critical": 50},
                "95th Percentile Response Time (ms)": {"target": 1000, "warning": 1500, "critical": 2500},
                "Average Response Time (ms)": {"target": 400, "warning": 600, "critical": 1000},
                "Max Response Time (ms)": {"target": 5000, "warning": 8000, "critical": 15000},
                "Failure Rate (%)": {"target": 0, "warning": 5, "critical": 10}
            }
        }
    }

    # Status and rating logic
    def get_status_and_rating(metric, value, total_requests):
        """Determine status and rating for a metric based on standards."""
        current_standards = standards.get(test_type.lower(), standards["load"])['metrics']
        if metric not in current_standards:
            return ("✅", "Healthy", 5)

        good = current_standards[metric]["target"]
        warning = current_standards[metric]["warning"]

        if metric == "Requests Per Second (RPS)":
            if value >= good * 1.5:
                return ("✅", "Healthy (Excellent)", 5)
            elif value >= good:
                return ("✅", "Healthy (Good)", 4)
            elif value >= warning:
                return ("⚠️", "Warning", 2)
            else:
                return ("❌", "Critical", 1)
        else:
            if value <= good * 0.5:
                return ("✅", "Healthy (Excellent)", 5)
            elif value <= good:
                return ("✅", "Healthy (Good)", 4)
            elif value <= warning:
                return ("⚠️", "Warning", 2)
            else:
                return ("❌", "Critical", 1)

    # Get individual metric statuses and ratings
    rps_status, rps_status_text, rps_rating = get_status_and_rating("Requests Per Second (RPS)", rps, total_requests)
    avg_status, avg_status_text, avg_response_rating = get_status_and_rating("Average Response Time (ms)", avg_response, total_requests)
    p95_status, p95_status_text, p95_rating = get_status_and_rating("95th Percentile Response Time (ms)", p95_response, total_requests)
    max_status, max_status_text, max_response_rating = get_status_and_rating("Max Response Time (ms)", max_response, total_requests)
    fail_status, fail_status_text, fail_rating = get_status_and_rating("Failure Rate (%)", failures_rate, total_requests)

    # Calculate overall rating and status
    ratings = [rps_rating, avg_response_rating, p95_rating, max_response_rating, fail_rating]
    overall_rating = sum(ratings) / len(ratings)
    overall_label, overall_class, overall_stars = rating_float_to_label_and_class(overall_rating)
    overall_status = overall_label

    test_data["overall_status"] = overall_status
    test_data["overall_rating"] = round(overall_rating, 1)

    # Generate percentile distribution table
    rating_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for rating in ratings:
        rating_counts[rating] += 1
    total_metrics = len(ratings)
    rating_distribution = {r: (rating_counts[r] / total_metrics * 100) for r in range(1, 6)}
    distribution_rows = ""
    # Labels are derived from current test results mapping
    for rating in range(1, 6):
        label = get_rating_label(rating)
        distribution_rows += f"""
            <tr>
                <td>{rating}</td>
                <td>{label}</td>
                <td>{rating_distribution[rating]:.1f}%</td>
                <td>{rating_counts[rating]}</td>
                <td>{sum(v for k, v in rating_counts.items() if k <= rating) / total_metrics * 100:.1f}%</td>
            </tr>
        """
    chart_data_array = "[" + ", ".join(str(round(rating_distribution[r], 1)) for r in range(1, 6)) + "]"
    distribution_table = f"""
        <div class="summary">
            <h2>Rating Distribution</h2>
            <div class="rating-graph">
                <canvas id="ratingChart"></canvas>
                <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
                <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2.0.0/dist/chartjs-plugin-datalabels.min.js"></script>
                <script>
                    var ratingCtx = document.getElementById('ratingChart').getContext('2d');
                    new Chart(ratingCtx, {{
                        type: 'bar',
                        data: {{
                            labels: [
                                'Critical (1)', 
                                'Warning (2)', 
                                'Healthy (Acceptable) (3)', 
                                'Healthy (Good) (4)', 
                                'Healthy (Excellent) (5)'
                            ],
                            datasets: [{{
                                label: 'Current Distribution (%)',
                                data: {chart_data_array},
                                backgroundColor: [
                                    'rgba(220, 53, 69, 0.3)', 
                                    'rgba(255, 193, 7, 0.3)', 
                                    'rgba(183, 235, 143, 0.3)', 
                                    'rgba(149, 222, 100, 0.3)', 
                                    'rgba(40, 167, 69, 0.3)'
                                ],
                                borderColor: [
                                    '#dc3545', 
                                    '#ffc107', 
                                    '#b7eb8f', 
                                    '#95de64', 
                                    '#28a745'
                                ],
                                borderWidth: 1
                            }}]
                        }},
                        options: {{
                            responsive: true,
                            maintainAspectRatio: false,
                            scales: {{ 
                                y: {{ 
                                    beginAtZero: true, 
                                    max: 100, 
                                    title: {{ display: true, text: 'Percentage (%)' }} 
                                }} 
                            }},
                            plugins: {{ 
                                legend: {{ 
                                    display: true,
                                    position: 'top',
                                    labels: {{ usePointStyle: true }}
                                }},
                                tooltip: {{ mode: 'index', intersect: false }},
                                datalabels: {{
                                    anchor: 'end',
                                    align: 'top',
                                    formatter: function(value) {{ return value + '%'; }},
                                    font: {{
                                        weight: 'bold'
                                    }},
                                    color: '#000'
                                }}
                            }}
                        }},
                        plugins: [ChartDataLabels]
                    }});
                </script>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Rating</th>
                        <th>Status</th>
                        <th>Percentage (%)</th>
                        <th>Count</th>
                        <th>Cumulative %</th>
                    </tr>
                </thead>
                <tbody>
                    {distribution_rows}
                </tbody>
            </table>
        </div>
    """

    # Generate recommendations and next steps
    recommendations = []
    next_steps = []

    if rps_status == "⚠️":
        recommendations.append(f"Warning: Throughput ({rps:.1f} RPS, Rating: {rps_rating}) is below optimal levels (≥{standards[test_type.lower()]['metrics']['Requests Per Second (RPS)']['target']}). Increase server resources or optimize code.")
        next_steps.extend([
            "<li><strong>Monitor CPU/memory:</strong> Use Prometheus to track resource usage and identify bottlenecks.</li>",
            "<li><strong>Optimize code:</strong> Refine application code to reduce request processing time.</li>",
            "<li><strong>Use load balancing:</strong> Implement load balancing to distribute requests evenly.</li>",
            "<li><strong>Scale infrastructure:</strong> Ensure servers can handle expected load.</li>"
        ])
    elif rps_status == "❌":
        recommendations.append(f"Critical: Throughput ({rps:.1f} RPS, Rating: {rps_rating}) is significantly below target (≥{standards[test_type.lower()]['metrics']['Requests Per Second (RPS)']['target']}). Check server capacity and network.")
        next_steps.extend([
            "<li><strong>Analyze logs:</strong> Use ELK Stack to pinpoint errors or performance issues.</li>",
            "<li><strong>Check network:</strong> Use Wireshark to monitor network bottlenecks.</li>",
            "<li><strong>Cache with Redis:</strong> Implement caching to reduce server load.</li>",
            "<li><strong>Scale servers:</strong> Add capacity to handle higher request volumes.</li>"
        ])
    else:
        recommendations.append(f"Throughput ({rps:.1f} RPS, Rating: {rps_rating}) meets or exceeds {test_type} standards.")

    if avg_status == "⚠️":
        recommendations.append(f"Warning: Average response time ({avg_response:.1f} ms, Rating: {avg_response_rating}) is high (≤{standards[test_type.lower()]['metrics']['Average Response Time (ms)']['target']}). Optimize app performance.")
        next_steps.extend([
            "<li><strong>Profile code:</strong> Use New Relic to identify slow code paths.</li>",
            "<li><strong>Optimize queries:</strong> Add database indexes to speed up queries.</li>",
            "<li><strong>Monitor response times:</strong> Track performance with APM tools.</li>",
            "<li><strong>Optimize backend:</strong> Improve backend processes for load handling.</li>"
        ])
    elif avg_status == "❌":
        recommendations.append(f"Critical: Average response time ({avg_response:.1f} ms, Rating: {avg_response_rating}) exceeds limits (≤{standards[test_type.lower()]['metrics']['Average Response Time (ms)']['target']}). Optimize queries and processing.")
        next_steps.extend([
            "<li><strong>Profile code:</strong> Analyze code paths with profiling tools.</li>",
            "<li><strong>Cache with Redis:</strong> Use caching to reduce database load.</li>",
            "<li><strong>Check CPU:</strong> Investigate CPU usage for bottlenecks.</li>",
            "<li><strong>Use async processing:</strong> Implement asynchronous task handling.</li>"
        ])
    else:
        recommendations.append(f"Average response time ({avg_response:.1f} ms, Rating: {avg_response_rating}) is excellent.")

    if p95_status == "⚠️":
        recommendations.append(f"Warning: 95th percentile response time ({p95_response:.1f} ms, Rating: {p95_rating}) shows delays (≤{standards[test_type.lower()]['metrics']['95th Percentile Response Time (ms)']['target']}). Optimize slow requests.")
        next_steps.extend([
            "<li><strong>Analyze with Datadog:</strong> Visualize response time distributions.</li>",
            "<li><strong>Optimize APIs:</strong> Improve high-latency API performance.</li>",
            "<li><strong>Cache data:</strong> Store frequent data in cache.</li>",
            "<li><strong>Handle peak load:</strong> Ensure system manages traffic spikes.</li>"
        ])
    elif p95_status == "❌":
        recommendations.append(f"Critical: 95th percentile response time ({p95_response:.1f} ms, Rating: {p95_rating}) indicates slow performance (≤{standards[test_type.lower()]['metrics']['95th Percentile Response Time (ms)']['target']}). Optimize endpoints.")
        next_steps.extend([
            "<li><strong>Trace endpoints:</strong> Use New Relic to identify slow APIs.</li>",
            "<li><strong>Optimize queries:</strong> Review MySQL slow query log.</li>",
            "<li><strong>Cache with Redis:</strong> Reduce database load with caching.</li>",
            "<li><strong>Map slow features:</strong> Use Hotjar to identify slow interactions.</li>"
        ])
    else:
        recommendations.append(f"95th percentile response time ({p95_response:.1f} ms, Rating: {p95_rating}) is excellent.")

    if max_status == "⚠️":
        recommendations.append(f"Warning: Max response time ({max_response:.1f} ms, Rating: {max_response_rating}) is high (≤{standards[test_type.lower()]['metrics']['Max Response Time (ms)']['target']}). Optimize endpoints.")
        next_steps.extend([
            "<li><strong>Set alerts:</strong> Use Prometheus for >{standards[test_type.lower()]['metrics']['Max Response Time (ms)']['target']} ms alerts.</li>",
            "<li><strong>Profile requests:</strong> Analyze slow requests for issues.</li>",
            "<li><strong>Optimize calls:</strong> Improve database/API call performance.</li>",
            "<li><strong>Ensure stability:</strong> Test system under heavy load.</li>"
        ])
    elif max_status == "❌":
        recommendations.append(f"Critical: Max response time ({max_response:.1f} ms, Rating: {max_response_rating}) indicates severe issues (≤{standards[test_type.lower()]['metrics']['Max Response Time (ms)']['target']}). Fix slow endpoints.")
        next_steps.extend([
            "<li><strong>Trace outliers:</strong> Use Dynatrace to pinpoint delays.</li>",
            "<li><strong>Set timeouts:</strong> Configure Nginx for 5s timeouts.</li>",
            "<li><strong>Scale with ELB:</strong> Use AWS ELB to distribute traffic.</li>",
            "<li><strong>Check features:</strong> Use Google Analytics for slow funnels.</li>"
        ])
    else:
        recommendations.append(f"Max response time ({max_response:.1f} ms, Rating: {max_response_rating}) is excellent.")

    if fail_status == "⚠️":
        recommendations.append(f"Warning: Failure rate ({failures_rate:.2f}%, Rating: {fail_rating}) is high (≤{standards[test_type.lower()]['metrics']['Failure Rate (%)']['target']}%). Investigate error sources.")
        next_steps.extend([
            "<li><strong>Review logs:</strong> Use ELK Stack to identify failure causes.</li>",
            "<li><strong>Fix errors:</strong> Address timeouts or resource issues.</li>",
            "<li><strong>Add retries:</strong> Implement retry mechanisms for failures.</li>",
            "<li><strong>Ensure stability:</strong> Test reliability under load.</li>"
        ])
    elif fail_status == "❌":
        recommendations.append(f"Critical: Failure rate ({failures_rate:.2f}%, Rating: {fail_rating}) indicates instability (≤{standards[test_type.lower()]['metrics']['Failure Rate (%)']['target']}%). Fix errors immediately.")
        next_steps.extend([
            "<li><strong>Review logs:</strong> Analyze logs with ELK Stack for errors.</li>",
            "<li><strong>Fix issues:</strong> Address timeouts or exhaustion.</li>",
            "<li><strong>Add retries:</strong> Implement retry logic for reliability.</li>",
            "<li><strong>Monitor failures:</strong> Set up alerts for failure rates.</li>"
        ])
    else:
        recommendations.append(f"Failure rate ({failures_rate:.2f}%, Rating: {fail_rating}) is excellent.")

    # Generate and save performance graph
    os.makedirs("test_history", exist_ok=True)
    graph_filename = f"test_history/{test_id}_performance_graph.png"
    try:
        actual_performance = [
            rps,
            p95_response,
            avg_response,
            max_response,
            failures_rate
        ]
        graph = generate_performance_graph(actual_performance, test_type.lower(), total_requests, failures_rate)
        graph.savefig(graph_filename, bbox_inches="tight", dpi=100)
        plt.close(graph)
    except Exception as e:
        print(f"Failed to generate graph for test {test_id}: {e}")
        graph_filename = ""

    # Save test history
    try:
        save_test_history(test_data, graph_filename)
    except Exception as e:
        print(f"Failed to save test history for test {test_id}: {e}")

# Helper: save report HTML to disk
def save_report_html(html_content: str, filename: str) -> str:
    os.makedirs("reports", exist_ok=True)
    path = os.path.join("reports", filename)
    try:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(html_content)
        return path
    except Exception as e:
        print(f"Failed to save report file {path}: {e}")
        return ""

# --- NEW HELPER FUNCTIONS FOR IMPORTED JSON ---
def generate_performance_graph_from_test(test_data):
    """Generate a performance graph from test data without saving to disk."""
    test_type = test_data.get("test_type", "Load").lower()
    stats = test_data.get("stats", {})
    actual_performance = [
        stats.get("rps", 0),
        stats.get("p95_response_time", 0),
        stats.get("avg_response_time", 0),
        stats.get("max_response_time", 0),
        stats.get("failures_rate", 0)
    ]
    total_requests = stats.get("total_requests", 0)
    failures_rate = stats.get("failures_rate", 0)
    return generate_performance_graph(actual_performance, test_type, total_requests, failures_rate)


def generate_html_report_from_test(test_data):
    """Generate an HTML report from test data with embedded base64 graph."""
    # Generate graph in memory
    fig = generate_performance_graph_from_test(test_data)
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches="tight", dpi=100)
    buf.seek(0)
    graph_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)

    # Extract data
    test_type = test_data.get("test_type", "Load")
    project_name = test_data.get("project_name", "Unnamed")
    test_id = test_data.get("test_id", "unknown")
    timestamp = test_data.get("timestamp", datetime.now().isoformat())
    users = test_data.get("users", "Unknown")
    duration = test_data.get("duration", "Unknown")
    stats = test_data.get("stats", {})
    total_requests = stats.get("total_requests", 0)
    failures_rate = stats.get("failures_rate", 0)
    rps = stats.get("rps", 0)
    avg_response = stats.get("avg_response_time", 0)
    p95_response = stats.get("p95_response_time", 0)
    max_response = stats.get("max_response_time", 0)

    # Build a minimal HTML report (you can expand with full styling if needed)
    html = f"""
    <!DOCTYPE html>
    <html>
    <head><title>Performance Report {test_id}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        .metrics {{ display: grid; grid-template-columns: repeat(3,1fr); gap: 10px; }}
        .metric {{ background: #f5f5f5; padding: 10px; border-radius: 5px; }}
        .metric-label {{ font-weight: bold; }}
        .graph {{ margin-top: 20px; }}
    </style>
    </head>
    <body>
        <h1>{test_type} Test Report</h1>
        <p><strong>Project:</strong> {project_name}</p>
        <p><strong>Test ID:</strong> {test_id}</p>
        <p><strong>Date:</strong> {timestamp}</p>
        <p><strong>Users:</strong> {users}</p>
        <p><strong>Duration:</strong> {duration} seconds</p>
        <h2>Metrics</h2>
        <div class="metrics">
            <div class="metric"><span class="metric-label">Total Requests:</span> {total_requests}</div>
            <div class="metric"><span class="metric-label">RPS:</span> {rps:.1f}</div>
            <div class="metric"><span class="metric-label">Avg Response:</span> {avg_response:.1f} ms</div>
            <div class="metric"><span class="metric-label">P95 Response:</span> {p95_response:.1f} ms</div>
            <div class="metric"><span class="metric-label">Max Response:</span> {max_response:.1f} ms</div>
            <div class="metric"><span class="metric-label">Failure Rate:</span> {failures_rate:.2f}%</div>
        </div>
        <h2>Performance Graph</h2>
        <div class="graph">
            <img src="data:image/png;base64,{graph_base64}" style="max-width:100%; height:auto;" />
        </div>
    </body>
    </html>
    """
    return html


def create_zip_for_imported_tests(tests):
    """Create a ZIP archive (bytes) containing HTML reports and graphs for all imported tests."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for idx, test in enumerate(tests):
            # Generate HTML report
            html_content = generate_html_report_from_test(test)
            report_filename = f"report_{test.get('test_id', f'test_{idx}')}.html"
            zf.writestr(report_filename, html_content)
            
            # Generate graph
            fig = generate_performance_graph_from_test(test)
            img_buf = io.BytesIO()
            fig.savefig(img_buf, format='png', bbox_inches="tight", dpi=100)
            img_buf.seek(0)
            graph_filename = f"graph_{test.get('test_id', f'test_{idx}')}.png"
            zf.writestr(graph_filename, img_buf.getvalue())
            plt.close(fig)
    buf.seek(0)
    return buf.getvalue()


# --- STREAMLIT APP ---

# Ensure the test_history directory exists
os.makedirs('test_history', exist_ok=True)

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown(
        '''
        <h1 class="sidebar-title">EAII <span style="font-size:2.5rem;">🚀</span>PTT</h1>
        <blockquote>"Quality isn't just a goal — it's our guarantee."</blockquote>
        ''',
        unsafe_allow_html=True
    )
    
    # Navigation buttons
    if st.button("🏠 Home", use_container_width=True, key="home_btn"):
        st.session_state.current_page = "Home"
    
    if st.button("📊 Test History", use_container_width=True, key="history_btn"):
        st.session_state.current_page = "Test History"
    
    if st.button("❓ Help", use_container_width=True, key="help_btn"):
        st.session_state.current_page = "Help"
    
    if st.button("ℹ️ About System", use_container_width=True, key="about_btn"):
        st.session_state.current_page = "About System"
    
    st.markdown("---")
    st.markdown("### 🖥️ System Status")
    
    # Display real-time system status
    display_system_status()
    
    st.markdown("---")
    st.markdown(
        """
        <div style="background-color: #6A0DAD; color: white; padding: 8px; border-radius: 5px; text-align: center; font-size: 0.8rem;">
            Developed by Ethiopian AI Institute | QA Department © 2025
        </div>
        """,
        unsafe_allow_html=True
    )

# --- MAIN PAGE CONTENT ---
if st.session_state.current_page == "Home":
    st.markdown(f"""
    <div class="header-container" style="display: flex; align-items: center; justify-content: flex-start; gap: 20px; padding: 10px;">
        <div class="logo-column" style="flex: 0 0 auto;">
            <a href="https://aii.et/" target="_blank" class="logo-link">
                {"<img src='data:image/png;base64,{}' class='logo-img' style='width: 90px; height: 90px; margin: 0; box-shadow: 0 0 10px var(--cosmic-neon);'>".format(
                    base64.b64encode(open('image/logo.png', 'rb').read()).decode()
                ) if os.path.exists('image/logo.png') else '<span style="font-size: 2rem; color: var(--cosmic-secondary);">EAII</span>'}
            </a>
        </div>
        <div class="content-column" style="flex: 1; display: flex; flex-direction: column; justify-content: center;">
            <div class="title-group">
                <h2 class="main-title" style="margin: 0; display: flex; align-items: center; gap: 10px;">
                    <span class="title-text">EAII Performance Testing Tool</span>
                    <span class="locust-icon">🦗</span>
                </h2>
                <p class="subtitle" style="margin: 5px 0 0 0; color: var(--cosmic-text);">Comprehensive performance testing powered by Locust</p>
                <blockquote style="margin: 5px 0 0 0; font-style: italic; color: var(--cosmic-text);">
                    <span class="quote-mark">"</span>
                    Quality isn't just a goal — it's our guarantee
                    <span class="quote-mark">"</span>
                </blockquote>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🧪 Test Configuration", "📊 Performance Analysis"])
    
    with tab1:
        st.markdown("### ⚙️ TEST PARAMETERS")
        col1, col2 = st.columns(2)
        with col1:
            project_name = st.text_input("📋 Project Name", " ", help="Name of the project being tested")
            target_host = st.text_input("🌐 Target URL", " ", help="The endpoint to test")
            test_type = st.selectbox(
                "🔧 Test Type", 
                list(MAX_USERS_LIMITS.keys()), 
                index=list(MAX_USERS_LIMITS.keys()).index(st.session_state.selected_test_type),
                help="Select the type of performance test",
                key="test_type_select"
            )
            if test_type != st.session_state.selected_test_type:
                st.session_state.selected_test_type = test_type
                st.session_state.duration_minutes = DEFAULT_DURATIONS[test_type] // 60
            st.markdown(f"""
            <div style="margin-top: 10px; padding: 10px; background: rgba(26, 95, 180, 0.1); border-radius: 8px;">
                <h4 style="color: var(--cosmic-primary);">Test Description</h4>
                <p style="color: var(--cosmic-text);">{TEST_TYPE_DESCRIPTIONS.get(test_type, 'Select a test type')}</p>
            </div>
            """, unsafe_allow_html=True)


        with col2:
            max_users = MAX_USERS_LIMITS[test_type]

            col21, col22, col23 = st.columns(3)
            with col21:
                users = st.number_input(
                    f"👥 Total Users (Max {max_users:,})", min_value=1, max_value=max_users,
                    value=500 if test_type == "Spike Test" else 100,
                    help="Final user count for the test"
                )
            with col22:
                spawn_default = 100 if test_type == "Spike Test" else 10
                spawn_rate = st.slider(
                    "📈 Spawn Rate (users/sec)", 1, 100,
                    value=spawn_default,
                    help="How quickly to add users during the test"
                )
            with col23:
                default_duration = DEFAULT_DURATIONS[test_type]
                duration = st.number_input(
                    "⏱️ Duration (seconds)",
                    min_value=10,
                    max_value=86400,
                    value=default_duration
                )
                st.markdown(f'<div class="duration-info">≈ {duration//60} minutes, {duration%60} seconds</div>', 
                          unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

        if not st.session_state.test_running:
            if st.button("🚀 Start Performance Test", type="primary", use_container_width=True, key="start_test"):
                st.session_state.test_running = True
                st.session_state.config = get_test_config(test_type, users, spawn_rate, duration)
                st.session_state.project_name = project_name

                # Display test summary with improved margins and inline styles
                st.markdown(f"""
                <div class="summary-card" style="margin: 20px; padding: 20px; display: inline-block; width: 100%; box-sizing: border-box;">
                    <div class="summary-header" style="margin-bottom: 15px; font-size: 1.2rem;">🚀 Starting {test_type}</div>
                    <div class="summary-metric" style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <span class="summary-label" style="margin-right: 10px;">Project:</span>
                        <span class="summary-value">{project_name}</span>
                    </div>
                    <div class="summary-metric" style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <span class="summary-label" style="margin-right: 10px;">Users:</span>
                        <span class="summary-value">{st.session_state.config['users']}</span>
                    </div>
                    <div class="summary-metric" style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <span class="summary-label" style="margin-right: 10px;">Spawn Rate:</span>
                        <span class="summary-value">{st.session_state.config['spawn']} users/sec</span>
                    </div>
                    <div class="summary-metric" style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <span class="summary-label" style="margin-right: 10px;">Duration:</span>
                        <span class="summary-value">{st.session_state.config['duration']} seconds ≈ {st.session_state.config['duration'] // 60} mins</span>
                    </div>
                    <div class="summary-metric" style="display: flex; justify-content: space-between;">
                        <span class="summary-label" style="margin-right: 10px;">Target:</span>
                        <span class="summary-value">{target_host}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                try:
                    with st.spinner("Starting performance engine..."):
                        st.session_state.locust_process = start_locust_server(target_host)
                        time.sleep(5)

                    triggered = trigger_test(
                        st.session_state.config['users'],
                        st.session_state.config['spawn'],
                        target_host
                    )
                    if not triggered:
                        st.error("🚨 Failed to start the test on performance server")
                        st.session_state.test_running = False
                        if st.session_state.locust_process:
                            st.session_state.locust_process.terminate()
                            st.session_state.locust_process = None
                    else:
                        # Monitor test and collect data
                        df_stats = monitor_test(st.session_state.config['duration'])
                        if not df_stats.empty:
                            st.markdown("### 📊 Test Results")
                            st.dataframe(df_stats.style.format({
                                "Requests/s": "{:.2f}",
                                "Avg Response (ms)": "{:.2f}",
                                "Fail %": "{:.2f}",
                                "95%ile (ms)": "{:.2f}"
                            }).background_gradient(cmap='Blues'), use_container_width=True)

                            # Calculate summary stats
                            total_requests = df_stats["Requests/s"].sum() * (duration / len(df_stats))
                            failures = df_stats["Fail %"].mean() * total_requests / 100
                            failures_rate = (failures / total_requests) * 100 if total_requests > 0 else 0
                            avg_rps = df_stats["Requests/s"].mean()
                            avg_response = df_stats["Avg Response (ms)"].mean()
                            p95_response = df_stats["95%ile (ms)"].mean()
                            max_response = df_stats["Avg Response (ms)"].max()

                           

                            # Ensure unique test ID
                            test_data = {
                                "test_id": str(uuid.uuid4()),  # Generate unique ID
                                "test_type": test_type,
                                "project_name": project_name,
                                "config": st.session_state.config,
                                "users": st.session_state.current_user,  # Save actual user count
                                "duration": f"{duration} seconds",  # Save formatted duration
                                "start_time": datetime.now().isoformat(),
                                "end_time": datetime.now().isoformat(),
                                "stats": {
                                    "total_requests": total_requests,
                                    "failures_rate": failures_rate,
                                    "rps": avg_rps,
                                    "avg_response_time": avg_response,
                                    "p95_response_time": p95_response,
                                    "max_response_time": max_response
                                }
                            }

                            # Calculate duration (in seconds) between start_time and end_time
                            start_time = datetime.fromisoformat(test_data["start_time"])
                            end_time = datetime.fromisoformat(test_data["end_time"])
                            duration_seconds = (end_time - start_time).total_seconds()
                            test_data["duration_seconds"] = duration_seconds  # Add duration to test_data

                            # Initialize session state variables
                            if "test_saved" not in st.session_state:
                                st.session_state.test_saved = False
                            if "generate_viz" not in st.session_state:
                                st.session_state.generate_viz = False
                            if "locust_process" not in st.session_state:
                                st.session_state.locust_process = None
                            if "test_running" not in st.session_state:
                                st.session_state.test_running = False

                            # Generate performance data and graph (regardless of saving)
                            actual_performance = {
                                "Requests Per Second (RPS)": avg_rps,
                                "Average Response Time (ms)": avg_response,
                                "95th Percentile Response Time (ms)": p95_response,
                                "Max Response Time (ms)": max_response,
                                "Failure Rate (%)": failures_rate
                            }

                            # Generate graph and filename
                            graph_filename = f"test_history/{test_data['test_id']}_performance_graph.png"
                            graph = generate_performance_graph(actual_performance, test_type, total_requests, failures_rate)
                            graph.savefig(graph_filename, bbox_inches="tight", dpi=100)
                            plt.close(graph)

                            # Always show download button if graph exists
                            if os.path.exists(graph_filename):
                                with open(graph_filename, "rb") as file:
                                    img_bytes = file.read()
                                if st.download_button(
                                    label="Download Performance Graph",
                                    data=img_bytes,
                                    file_name=f"performance_graph_{test_data['test_id']}.png",
                                    mime="image/png",
                                    key=f"download_{test_data['test_id']}"
                                ):
                                    # Also save a copy to the reports directory for quick access
                                    os.makedirs(os.path.join("reports","graphs"), exist_ok=True)
                                    dest = os.path.join("reports","graphs", f"performance_graph_{test_data['test_id']}.png")
                                    try:
                                        with open(dest, "wb") as out_f:
                                            out_f.write(img_bytes)
                                        st.success(f"Graph saved to: {dest}")
                                    except Exception as e:
                                        st.error(f"Failed to save graph to reports: {e}")
                except Exception as e:
                    st.error(f"🚨 Error during test execution: {e}")
                    st.session_state.test_running = False
                    if st.session_state.locust_process:
                        st.session_state.locust_process.terminate()
                        st.session_state.locust_process = None

                finally:
                    stop_test()
                    st.session_state.test_running = False
                    st.rerun()

        else:
            st.warning("🛑 A test is currently stopped!")

    with tab2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header">📊 PERFORMANCE VISUALIZATION</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown('<div class="test-config">', unsafe_allow_html=True)
            st.markdown('<div class="config-header">📝 INPUT METRICS</div>', unsafe_allow_html=True)
            
            # Input fields
            graph_title = st.selectbox("📊 Test Type", 
                                    ["Load", "Stress", "Spike", "Endurance", "Volume", "Concurrency"],
                                    index=0)
            
            st.markdown("---")
            st.markdown("### 📈 Performance Metrics")
            total_requests = st.number_input("📤 Total Requests", value=26793, min_value=0, format="%d")
            failures_rate = st.number_input("❌ Failure Rate (%)", value=0.0, min_value=0.0, max_value=100.0, step=0.1, format="%.1f")
            
            actual_performance = {
                "Requests Per Second (RPS)": st.number_input("⚡ RPS (Requests/sec)", value=89, min_value=0),
                "Average Response Time (ms)": st.number_input("📏 Average Response (ms)", value=74, min_value=0),
                "95th Percentile Response Time (ms)": st.number_input("📊 95th Percentile (ms)", value=320, min_value=0),
                "Max Response Time (ms)": st.number_input("🔥 Max Response (ms)", value=1194, min_value=0),
            }
            
            if st.button('🎨 Generate Visualization', use_container_width=True, key="gen_viz"):
                # Create TEMPORARY test data (not stored in session state)
                test_data = {
                    "test_id": str(uuid.uuid4()),
                    "test_type": graph_title,
                    "project_name": project_name,
                    "duration": duration,
                    "users": users,
                    "stats": {
                        "total_requests": total_requests,
                        "failures_rate": failures_rate,
                        "rps": actual_performance["Requests Per Second (RPS)"],
                        "avg_response_time": actual_performance["Average Response Time (ms)"],
                        "p95_response_time": actual_performance["95th Percentile Response Time (ms)"],
                        "max_response_time": actual_performance["Max Response Time (ms)"]
                    },
                    "timestamp": datetime.now().isoformat()
                }
                
                # Generate visualization
                fig = generate_performance_graph(
                    actual_performance, 
                    graph_title, 
                    total_requests, 
                    failures_rate
                )
                
                # Generate HTML report
                html_report = generate_html_report(test_data)
                
                # Store ONLY what's needed for display in session state
                st.session_state.current_viz = {
                    "figure": fig,
                    "report": html_report,
                    "test_type": graph_title
                }
                
                st.rerun()

        with col2:
            if "current_viz" in st.session_state:
                # Display the visualization
                st.pyplot(st.session_state.current_viz["figure"])
                
                # Pure download button - NO SAVING LOGIC WHATSOEVER
                report_file_name = f"performance_report_{st.session_state.current_viz['test_type'].lower().replace(' ', '_')}.html"
                with open(report_file_name, "w", encoding="utf-8") as f:
                    # Save a copy automatically to reports/ when the user clicks download
                    rp = save_report_html(st.session_state.current_viz["report"], report_file_name)
                    if rp:
                        st.success(f"Saved report to {rp}")

                # Performance summary cards
                st.markdown("## 📊 Performance Summary")
                cols = st.columns(5)
                metric_keys = list(actual_performance.keys())
                for i, key in enumerate(metric_keys):
                    with cols[i]:
                        st.markdown(f"""
                        <div class="metric-card hover-grow" style="background: darkblue;">
                            <div class="metric-label">{key.split('(')[0]}</div>
                            <div class="metric-value">{actual_performance[key]}</div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="height:500px; display:flex; flex-direction:column; 
                            justify-content:center; align-items:center; 
                            background: rgba(25, 55, 109, 0.3); border-radius:15px;
                            border: 2px dashed #4fc3f7; margin-top:20px;">
                    <h3 style="color:#bbdefb; text-align:center;">🚀 Ready to Visualize</h3>
                    <p style="color:#90a4ae; text-align:center; max-width:80%;">
                        Configure your performance metrics on the left and click 
                        "Generate Visualization" to create your performance report
                    </p>
                    <div style="font-size:5rem; color:#4fc3f7; margin-top:20px;">📊</div>
                </div>
                """, unsafe_allow_html=True)
                
        st.markdown('</div>', unsafe_allow_html=True)

# --- TEST HISTORY PAGE ---
elif st.session_state.current_page == "Test History":
    st.title("📊 Test History")

    # --- Radio to choose source ---
    source = st.radio(
        "Select data source:",
        ["📁 Saved History", "📂 Upload JSON"],
        horizontal=True,
        key="history_source"
    )

    # --- Performance standards definitions (copied from original) ---
    PERFORMANCE_STANDARDS = {
        "load": {
            "display_name": "Load Test",
            "metrics": {
                "Requests Per Second (RPS)": {"target": 500, "warning": 400, "critical": 300},
                "Median Response Time (ms)": {"target": 300, "warning": 500, "critical": 800},
                "95th Percentile Response Time (ms)": {"target": 800, "warning": 1000, "critical": 1500},
                "Average Response Time (ms)": {"target": 300, "warning": 500, "critical": 800},
                "Max Response Time (ms)": {"target": 4000, "warning": 6000, "critical": 10000},
                "Failure Rate (%)": {"target": 0, "warning": 3, "critical": 5}
            },
            "health_weights": {
                "base_score": 0.5,
                "failure_rate_score": 0.3,
                "trend_score": 0.2
            },
            "failures_rate": [0.5, 2.0]  # [warning_threshold, critical_threshold]
        },
        "concurrency": {
            "display_name": "Concurrency Test",
            "metrics": {
                "Requests Per Second (RPS)": {"target": 280, "warning": 200, "critical": 150},
                "Median Response Time (ms)": {"target": 400, "warning": 600, "critical": 800},
                "95th Percentile Response Time (ms)": {"target": 900, "warning": 1200, "critical": 1800},
                "Average Response Time (ms)": {"target": 400, "warning": 600, "critical": 800},
                "Max Response Time (ms)": {"target": 5000, "warning": 7000, "critical": 10000},
                "Failure Rate (%)": {"target": 0, "warning": 5, "critical": 8}
            },
            "health_weights": {
                "base_score": 0.5,
                "failure_rate_score": 0.3,
                "trend_score": 0.2
            },
            "failures_rate": [0.5, 2.0]
        },
        "spike": {
            "display_name": "Spike Test",
            "metrics": {
                "Requests Per Second (RPS)": {"target": 350, "warning": 250, "critical": 150},
                "Median Response Time (ms)": {"target": 500, "warning": 800, "critical": 1200},
                "95th Percentile Response Time (ms)": {"target": 1200, "warning": 1800, "critical": 2500},
                "Average Response Time (ms)": {"target": 500, "warning": 800, "critical": 1200},
                "Max Response Time (ms)": {"target": 6000, "warning": 9000, "critical": 15000},
                "Failure Rate (%)": {"target": 0, "warning": 10, "critical": 15}
            },
            "health_weights": {
                "base_score": 0.5,
                "failure_rate_score": 0.3,
                "trend_score": 0.2
            },
            "failures_rate": [0.5, 2.0]
        },
        "volume": {
            "display_name": "Volume Test",
            "metrics": {
                "Requests Per Second (RPS)": {"target": 400, "warning": 300, "critical": 250},
                "Median Response Time (ms)": {"target": 200, "warning": 300, "critical": 500},
                "95th Percentile Response Time (ms)": {"target": 500, "warning": 800, "critical": 1200},
                "Average Response Time (ms)": {"target": 200, "warning": 300, "critical": 500},
                "Max Response Time (ms)": {"target": 3000, "warning": 5000, "critical": 8000},
                "Failure Rate (%)": {"target": 0, "warning": 1, "critical": 3}
            },
            "health_weights": {
                "base_score": 0.5,
                "failure_rate_score": 0.3,
                "trend_score": 0.2
            },
            "failures_rate": [0.5, 2.0]
        },
        "stress": {
            "display_name": "Stress Test",
            "metrics": {
                "Requests Per Second (RPS)": {"target": 200, "warning": 150, "critical": 100},
                "Median Response Time (ms)": {"target": 800, "warning": 1200, "critical": 2000},
                "95th Percentile Response Time (ms)": {"target": 2000, "warning": 3000, "critical": 5000},
                "Average Response Time (ms)": {"target": 800, "warning": 1200, "critical": 2000},
                "Max Response Time (ms)": {"target": 10000, "warning": 15000, "critical": 30000},
                "Failure Rate (%)": {"target": 0, "warning": 15, "critical": 20}
            },
            "health_weights": {
                "base_score": 0.5,
                "failure_rate_score": 0.3,
                "trend_score": 0.2
            },
            "failures_rate": [0.5, 2.0]
        },
        "endurance": {
            "display_name": "Endurance Test",
            "metrics": {
                "Requests Per Second (RPS)": {"target": 150, "warning": 100, "critical": 50},
                "Median Response Time (ms)": {"target": 400, "warning": 600, "critical": 1000},
                "95th Percentile Response Time (ms)": {"target": 1000, "warning": 1500, "critical": 2500},
                "Average Response Time (ms)": {"target": 400, "warning": 600, "critical": 1000},
                "Max Response Time (ms)": {"target": 5000, "warning": 8000, "critical": 15000},
                "Failure Rate (%)": {"target": 0, "warning": 5, "critical": 10}
            },
            "health_weights": {
                "base_score": 0.5,
                "failure_rate_score": 0.3,
                "trend_score": 0.2
            },
            "failures_rate": [0.5, 2.0]
        }
    }

    CSS_STYLES = """
    /* Base Styles */
    :root {
        --primary-color: #0a1a3b;
        --primary-light: #1a3a6a;
        --secondary-color: #2b5876;
        --accent-color: #f9a825;
        --success-color: #28a745;
        --warning-color: #ffc107;
        --danger-color: #dc3545;
        --light-bg: #f8f9fa;
        --card-bg: #ffffff;
        --text-dark: #333333;
        --text-light: #666666;
        --border-radius: 12px;
        --box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
        --transition: all 0.3s ease;
    }

    * {
        box-sizing: border-box;
    }

    body {
        font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
        margin: 0 auto;
        max-width: 1200px;
        background: linear-gradient(135deg, #f5f7fa 0%, #e4edf5 100%);
        color: var(--text-dark);
        line-height: 1.6;
        padding: 20px;
        min-height: 100vh;
    }

    /* Header - Modern Design */
    .header {
            position: relative;
            min-height: 200px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #0a1a3b 0%, #1a3a6a 100%);
            border: none;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
            margin: 20px 0;
            padding: 20px;
            color: white;
            text-align: center;
            isolation: isolate;
        }
        
        .header::before, .header::after { 
            content: ""; 
            position: absolute; 
            top: 0; 
            width: 20%; 
            height: 100%; 
            background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cpolygon points='30,0 51.96,15 51.96,45 30,60 8.04,45 8.04,15' fill='%23f9a825' opacity='1.0'/%3E%3C/svg%3E") repeat; 
            background-size: 60px 52px; 
            z-index: -1;
        }
        
        .header::before { 
            left: 0; 
        }
        
        .header::after { 
            right: 0; 
        }
         .logo {
            height: 100px;
            width: auto;
            margin-bottom: 20px;
            filter: drop-shadow(0 4px 12px rgba(0, 0, 0, 0.25));
            transition: transform var(--transition-normal);
        }
        
        .logo:hover {
            transform: scale(1.05);
        }
        .institute-text { 
            text-align: center;
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 5px;
        }
        
        .institute-text .amh { 
            font-family: "Segoe UI", sans-serif; 
            font-size: 1.4rem; 
            font-weight: 600; 
            color: white;
            margin: 0;
            padding: 0;
        }
        
        .institute-text .eng { 
            font-size: 1.1rem; 
            color: #f9a825; 
            font-weight: 500; 
            margin: 0;
            padding: 0;
        }
        

    /* Main Container */
    .project-section {
        background: var(--card-bg);
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow);
        margin: 30px 0;
        padding: 30px;
        page-break-after: always;
    }

    .project-summary h2 {
        color: var(--primary-color);
        font-size: 1.8rem;
        border-bottom: 2px solid var(--light-bg);
        padding-bottom: 1rem;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .project-summary h2::before {
        content: "📊";
        font-size: 1.5rem;
    }

    /* Test Description */
    .test-description {
        background: linear-gradient(135deg, var(--secondary-color) 0%, #4e4376 100%);
        color: white;
        padding: 25px 30px;
        border-radius: var(--border-radius);
        margin: 30px 0;
        box-shadow: var(--box-shadow);
        border-left: 5px solid var(--accent-color);
    }

    .test-description h2 {
        color: white;
        font-size: 1.8rem;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .test-description h2::before {
        content: "🧪";
        font-size: 1.5rem;
    }

    .test-description p {
        font-size: 1.1rem;
        opacity: 0.95;
        line-height: 1.7;
    }

    /* Report Info Cards */
    .report-info {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 25px;
        margin: 40px 0;
    }

    .info-box {
        background: var(--card-bg);
        padding: 25px;
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow);
        transition: var(--transition);
        border: 1px solid rgba(0, 0, 0, 0.05);
        position: relative;
        overflow: hidden;
    }

    .info-box::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(to bottom, var(--primary-color), var(--accent-color));
    }

    .info-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
    }

    .info-box h3 {
        color: var(--primary-color);
        font-size: 1.3rem;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 2px solid var(--light-bg);
    }

    .info-box p {
        margin: 12px 0;
        color: var(--text-light);
        font-size: 1rem;
        line-height: 1.6;
    }

    .info-box strong {
        color: var(--text-dark);
        min-width: 140px;
        display: inline-block;
        font-weight: 600;
    }

    /* Load Test Status */
    .load-test-status {
        padding: 20px 25px;
        border-radius: var(--border-radius);
        font-weight: 700;
        text-align: center;
        margin: 30px 0;
        font-size: 1.2rem;
        box-shadow: var(--box-shadow);
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
        border-left: 5px solid;
    }

    .load-test-status.healthy {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        color: #155724;
        border-left-color: var(--success-color);
    }

    .load-test-status.warning {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        color: #856404;
        border-left-color: var(--warning-color);
    }

    .load-test-status.critical {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        color: #721c24;
        border-left-color: var(--danger-color);
    }

    /* Metrics Grid */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin: 30px 0;
    }

    .metric-card {
        background: var(--card-bg);
        padding: 20px;
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow);
        text-align: center;
        border-top: 4px solid var(--primary-color);
        transition: var(--transition);
    }

    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    }

    .metric-card h3 {
        margin: 0 0 15px 0;
        font-size: 1.1rem;
        color: var(--text-light);
        font-weight: 600;
    }

    .metric-value {
        font-size: 2rem;
        color: var(--primary-color);
        margin: 10px 0;
        font-weight: 800;
        font-family: 'SF Mono', Monaco, 'Cascadia Code', monospace;
    }

    /* Status Overview */
    .status-overview {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 20px;
        margin: 30px 0;
    }

    .status-item {
        background: var(--card-bg);
        padding: 20px;
        border-radius: var(--border-radius);
        text-align: center;
        transition: var(--transition);
        box-shadow: var(--box-shadow);
        border-left: 5px solid;
    }

    .status-item:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
    }

    .status-item.healthy {
        background: #dcfce7;
        border-left-color: var(--success-color);
    }

    .status-item.warning {
        background: #fef3c7;
        border-left-color: var(--warning-color);
    }

    .status-item.critical {
        background: #fee2e2;
        border-left-color: var(--danger-color);
    }

    .status-item div:first-child {
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 10px;
        color: var(--primary-color);
    }

    /* Tables */
    table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        margin: 30px 0;
        background: var(--card-bg);
        border-radius: var(--border-radius);
        overflow: hidden;
        box-shadow: var(--box-shadow);
    }

    th, td {
        padding: 16px 20px;
        text-align: left;
        border-bottom: 1px solid rgba(0, 0, 0, 0.05);
    }

    th {
        background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
        color: white;
        font-weight: 600;
        font-size: 1rem;
        position: sticky;
        top: 0;
    }

    tr {
        transition: var(--transition);
    }

    tr:hover {
        background-color: rgba(10, 26, 59, 0.03);
    }

    /* Status Badges */
    .status {
        padding: 8px 20px;
        border-radius: 25px;
        font-weight: 700;
        font-size: 0.9rem;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    .status.healthy {
        background: linear-gradient(135deg, var(--success-color), #20c997);
        color: white;
    }

    .status.warning {
        background: linear-gradient(135deg, var(--warning-color), #fd7e14);
        color: black;
    }

    .status.critical {
        background: linear-gradient(135deg, var(--danger-color), #c82333);
        color: white;
    }

    /* Graph Container */
    .graph-container {
        margin: 30px 0;
        padding: 25px;
        background: var(--card-bg);
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow);
        border: 1px solid rgba(0, 0, 0, 0.05);
    }

    .graph-container h4 {
        margin: 0 0 20px 0;
        color: var(--secondary-color);
        font-size: 1.4rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .graph-container h4::before {
        content: "📈";
    }

    .graph-container img {
        max-width: 100%;
        height: auto;
        border-radius: 8px;
        border: 1px solid rgba(0, 0, 0, 0.1);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }

    /* Recommendations */
    .recommendations {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 30px;
        border-radius: var(--border-radius);
        margin: 30px 0;
        border-left: 5px solid var(--accent-color);
        box-shadow: var(--box-shadow);
    }

    .recommendations h3 {
        color: var(--primary-color);
        font-size: 1.5rem;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .recommendations h3::before {
        content: "💡";
    }

    .recommendations ul {
        padding-left: 20px;
        margin: 0;
    }

    .recommendations li {
        margin-bottom: 12px;
        line-height: 1.6;
        color: var(--text-dark);
    }

    /* Next Steps - Fixed Numbering */
    .next-steps {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 30px;
        border-radius: var(--border-radius);
        margin: 30px 0;
        border-left: 5px solid var(--accent-color);
        box-shadow: var(--box-shadow);
    }

    .next-steps h3 {
        color: var(--primary-color);
        font-size: 1.5rem;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .next-steps h3::before {
        content: "🚀";
    }

    .next-steps > ul {
        list-style: none;
        padding: 0;
        margin: 0;
        counter-reset: step-counter;
    }

    .next-steps > ul > li {
        background: white;
        padding: 20px 20px 20px 60px; /* More left padding for numbering */
        margin-bottom: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border-left: 4px solid var(--primary-color);
        transition: var(--transition);
        position: relative;
        counter-increment: step-counter;
        min-height: 70px;
        display: flex;
        align-items: center;
    }

    .next-steps > ul > li::before {
        content: counter(step-counter) ".";
        position: absolute;
        left: 20px;
        font-weight: bold;
        color: var(--primary-color);
        font-size: 1.2rem;
        min-width: 30px;
        text-align: center;
        background: rgba(10, 26, 59, 0.1);
        border-radius: 50%;
        height: 30px;
        line-height: 30px;
        top: 50%;
        transform: translateY(-50%);
    }

    .next-steps > ul > li:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    .next-steps > ul > li strong {
        color: var(--primary-color);
        font-weight: 600;
        margin-right: 5px;
    }

    /* Footer */
    .footer {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-light) 100%);
        color: white;
        text-align: center;
        margin-top: 60px;
        font-size: 0.95rem;
        padding: 40px 30px;
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow);
        position: relative;
        overflow: hidden;
    }

    .footer::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--accent-color), #ffcc00, var(--accent-color));
    }

    .footer-content {
        max-width: 900px;
        margin: 0 auto;
        position: relative;
        z-index: 1;
    }

    .footer p {
        margin: 10px 0;
        line-height: 1.6;
        opacity: 0.9;
    }

    .footer strong {
        color: var(--accent-color);
    }

    .footer a {
        color: var(--accent-color);
        text-decoration: none;
        font-weight: 600;
        transition: var(--transition);
    }

    .footer a:hover {
        color: #ffcc00;
        text-decoration: underline;
    }

    /* Utility Classes */
    .insight-positive {
        color: var(--success-color);
        font-weight: 600;
    }

    .insight-warning {
        color: var(--warning-color);
        font-weight: 600;
    }

    .insight-critical {
        color: var(--danger-color);
        font-weight: 600;
    }

    .emoji {
        font-size: 1.2rem;
        margin-right: 0.5rem;
    }

    /* Responsive Design */
    @media (max-width: 1200px) {
        body {
            padding: 15px;
        }
    }

    @media (max-width: 992px) {
        .report-info {
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        }
        
        .metrics-grid, .status-overview {
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        }
    }

    @media (max-width: 768px) {
        .header {
            min-height: 160px;
            padding: 20px 15px;
            margin: 10px 0 30px;
        }
        
        .institute-text h1 {
            font-size: 1.4rem;
        }
        
        .institute-text h2 {
            font-size: 1.1rem;
        }
        
        .project-section {
            padding: 20px;
        }
        
        .test-description,
        .info-box,
        .graph-container,
        .recommendations,
        .next-steps {
            padding: 20px;
        }
        
        .next-steps > ul > li {
            padding: 15px 15px 15px 50px;
        }
        
        .next-steps > ul > li::before {
            left: 15px;
        }
    }

    @media (max-width: 576px) {
        .header {
            min-height: 140px;
            padding: 15px 10px;
        }
        
        .header img {
            width: 80px;
        }
        
        .institute-text .amh {
            font-size: 14px;
        }
        
        .institute-text .eng {
            font-size: 12px;
        }
        
        .report-info,
        .metrics-grid,
        .status-overview {
            grid-template-columns: 1fr;
            gap: 15px;
        }
        
        th, td {
            padding: 12px 15px;
            font-size: 0.9rem;
        }
        
        .next-steps > ul > li {
            padding: 15px 15px 15px 45px;
            min-height: auto;
            align-items: flex-start;
        }
        
        .next-steps > ul > li::before {
            top: 15px;
            transform: none;
        }
        
        .footer {
            padding: 30px 20px;
            font-size: 0.85rem;
        }
    }

    /* Print Styles */
    @media print {
        body {
            background: white !important;
            padding: 0 !important;
            margin: 0 !important;
            max-width: none !important;
        }
        
        .header, .footer {
            page-break-inside: avoid;
            box-shadow: none !important;
            border: 1px solid #ddd !important;
        }
        
        .project-section {
            page-break-after: always;
            box-shadow: none !important;
            border: 1px solid #ddd !important;
            margin: 10px 0 !important;
        }
        
        .graph-container {
            max-width: 100% !important;
            break-inside: avoid;
        }
        
        .info-box, .metric-card, .status-item {
            box-shadow: none !important;
            border: 1px solid #ddd !important;
        }
        
        .next-steps > ul > li::before {
            background: none !important;
        }
    }
    """

    def normalize_test_type(test_type):
        """Convert various test type names to standard keys."""
        if not test_type:
            return "load"
        
        test_type = test_type.lower().strip()
        if "load" in test_type:
            return "load"
        elif "concurrency" in test_type:
            return "concurrency"
        elif "spike" in test_type:
            return "spike"
        elif "volume" in test_type:
            return "volume"
        elif "stress" in test_type:
            return "stress"
        elif "endurance" in test_type:
            return "endurance"
        return "load"  # default

    def normalize_test_type(test_type):
        """Convert test type names to standard keys."""
        if not test_type:
            return "load"
        test_type = test_type.lower().strip()
        for key in PERFORMANCE_STANDARDS:
            if key in test_type:
                return key
        return "load"
    def remove_asterisks(string_list):
        """Remove all asterisks from each string in the list."""
        return [s.replace('*', '') for s in string_list]

    def get_status_and_rating(metric, value, test_type):
        """Determine status and rating for a metric based on standards."""
        normalized_type = normalize_test_type(test_type)
        standards = PERFORMANCE_STANDARDS.get(normalized_type, PERFORMANCE_STANDARDS["load"])["metrics"]
        
        if metric not in standards:
            return ("✅", "Healthy", 5)

        target = standards[metric]["target"]
        warning = standards[metric]["warning"]
        critical = standards[metric]["critical"]

        if metric == "Requests Per Second (RPS)":
            if value >= target:
                return ("✅", "Healthy", 5)
            elif value >= warning:
                return ("⚠️", "Warning", 3)
            elif value >= critical:
                return ("⚠️", "Warning", 2)
            else:
                return ("❌", "Critical", 1)
        else:
            if value <= target:
                return ("✅", "Healthy", 5)
            elif value <= warning:
                return ("⚠️", "Warning", 3)
            elif value <= critical:
                return ("⚠️", "Warning", 2)
            else:
                return ("❌", "Critical", 1)

    def create_trend_plot(performance_trend: list, project_name: str) -> str:
        """Generate a performance trend plot as an embedded Chart.js canvas + script (HTML snippet)."""
        # Build valid trend points with date parsing
        valid_trends = []
        for t in performance_trend:
            try:
                if t.get("date") and t["date"] != "Invalid":
                    datetime.strptime(t["date"], "%Y-%m-%d %H:%M:%S")
                    valid_trends.append(t)
            except (ValueError, TypeError):
                continue

        if not valid_trends:
            return '<div class="graph-container"><p style="color:#856404;">No valid trend data available.</p></div>'

        # Prepare labels and series
        dates = [datetime.strptime(t["date"], "%Y-%m-%d %H:%M:%S") for t in valid_trends]
        date_labels = [d.strftime("%b %d %H:%M") for d in dates]

        rps_series = [t["rps"] for t in valid_trends]
        avg_series = [t["avg_response"] for t in valid_trends]
        p95_series = [t["p95_response"] for t in valid_trends]
        max_series = [t["max_response"] for t in valid_trends]
        fail_series = [t.get("failure_rate", 0.0) for t in valid_trends]

        # Compute short trend text for display
        trend_data = calculate_trends(valid_trends)
        metrics_info = [
            ("RPS", f"{valid_trends[-1]['rps']:.1f}", trend_data.get('rps_short', trend_data.get('rps_trend', 'N/A'))),
            ("Avg", f"{valid_trends[-1]['avg_response']:.1f}ms", trend_data.get('response_short', trend_data.get('response_trend', 'N/A'))),
            ("P95", f"{valid_trends[-1]['p95_response']:.1f}ms", trend_data.get('p95_short', trend_data.get('p95_response_trend', 'N/A'))),
            ("Max", f"{valid_trends[-1]['max_response']:.1f}ms", trend_data.get('max_short', trend_data.get('max_response_trend', 'N/A'))),
            ("Fail", f"{valid_trends[-1].get('failure_rate', 0.0):.1f}%", trend_data.get('failure_short', trend_data.get('failure_rate_trend', 'N/A')))
        ]

        # Unique canvas id to allow multiple charts on the same page
        canvas_id = f"trendChart_{uuid.uuid4().hex[:8]}"

        # Build HTML + JS using Chart.js (delivered via CDN)
        chart_html = f"""
        <div class="rating-graph" style="height:420px; position: relative;">
            <canvas id="{canvas_id}"></canvas>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2.0.0/dist/chartjs-plugin-datalabels.min.js"></script>
        <script>
        (function() {{
            const labels = {json.dumps(date_labels)};
            const data = {{
                rps: {json.dumps(rps_series)},
                avg: {json.dumps(avg_series)},
                p95: {json.dumps(p95_series)},
                max: {json.dumps(max_series)},
                fail: {json.dumps(fail_series)}
            }};
            const ctx = document.getElementById('{canvas_id}').getContext('2d');
            const chart = new Chart(ctx, {{
                type: 'line',
                data: {{
                    labels: labels,
                    datasets: [
                        {{ label: 'RPS', data: data.rps, borderColor: '#1f77b4', backgroundColor: 'rgba(31,119,180,0.08)', tension: 0.3, yAxisID: 'y' }},
                        {{ label: 'Avg Response (ms)', data: data.avg, borderColor: '#2ca02c', backgroundColor: 'rgba(44,160,44,0.08)', tension: 0.3, yAxisID: 'y' }},
                        {{ label: 'P95 Response (ms)', data: data.p95, borderColor: '#ff7f0e', backgroundColor: 'rgba(255,127,14,0.08)', tension: 0.3, yAxisID: 'y' }},
                        {{ label: 'Max Response (ms)', data: data.max, borderColor: '#d62728', backgroundColor: 'rgba(214,39,40,0.08)', tension: 0.3, yAxisID: 'y' }},
                        {{ label: 'Failure Rate (%)', data: data.fail, borderColor: '#9467bd', backgroundColor: 'rgba(148,103,189,0.08)', tension: 0.3, yAxisID: 'y2', borderDash: [6,4] }}
                    ]
                }},
                options: {{
                    plugins: {{
                        legend: {{ position: 'top' }},
                        tooltip: {{ mode: 'index', intersect: false }},
                        datalabels: {{ display: false }}
                    }},
                    scales: {{
                        y: {{ type: 'linear', position: 'left', title: {{ display: true, text: 'Metric value' }} }},
                        y2: {{ type: 'linear', position: 'right', grid: {{ drawOnChartArea: false }}, title: {{ display: true, text: 'Failure Rate (%)' }}, ticks: {{ callback: function(value) {{ return value + '%'; }} }} }}
                    }},
                    responsive: true,
                    maintainAspectRatio: false
                }}
            }});
        }})();
        </script>
        <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:10px;">
            {''.join([f"<div style='background:#fff;padding:8px;border-radius:6px;box-shadow:0 1px 3px rgba(0,0,0,0.06);min-width:160px;'><strong>{html.escape(name)}</strong><div style='font-weight:bold'>{html.escape(value)}</div><div style='font-size:0.85rem;color:#555'>{html.escape(str(trend))}</div></div>" for (name, value, trend) in metrics_info])}
        </div>
        """

        return chart_html

    def calculate_trends(performance_trend):
        """Calculate trend data for performance metrics with robust handling of edge cases."""
        # Build list of valid dated trends and compute robust statistics
        valid = []
        timestamps = []
        for t in performance_trend:
            try:
                if t.get('date') and t['date'] != 'Invalid':
                    dt = datetime.strptime(t['date'], "%Y-%m-%d %H:%M:%S")
                    valid.append(t)
                    timestamps.append(dt.timestamp())
            except Exception:
                continue

        if len(valid) <= 1:
            return {
                'rps_trend': "⚪ No trend data",
                'rps_description': "At least two data points are needed to determine how the system's throughput is evolving.",
                'response_trend': "⚪ No trend data",
                'response_description': "At least two data points are required to evaluate the change in average response time.",
                'p95_response_trend': "⚪ No trend data",
                'p95_response_description': "At least two data points are needed to analyze how the 95th percentile response time is changing.",
                'max_response_trend': "⚪ No trend data",
                'max_response_description': "At least two data points are needed to understand how the system's slowest responses are trending.",
                'failure_rate_trend': "⚪ No trend data",
                'failure_rate_description': "At least two data points are required to assess how request reliability is changing over time."
            }

        # Sort valid by timestamp
        pairs = sorted(zip(timestamps, valid), key=lambda x: x[0])
        t_stamps = [p[0] for p in pairs]
        points = [p[1] for p in pairs]

        first = points[0]
        last = points[-1]

        def _pct_and_delta(first_val, last_val):
            """Return (pct_change, delta, note) where pct_change is None when undefined (first_val == 0 and last_val != 0)."""
            try:
                f = float(first_val)
                l = float(last_val)
            except Exception:
                return None, 0.0, 'invalid'

            delta = l - f
            if f == 0:
                if l == 0:
                    return 0.0, 0.0, 'no_change'
                return None, delta, 'from_zero'

            pct = (delta / f) * 100
            return pct, delta, 'ok'

        def _regression_info(values):
            """Compute linear slope and volatility (std/mean) for a series of values across timestamps."""
            try:
                y = np.array(values, dtype=float)
                x = np.array(t_stamps, dtype=float)
                if len(x) < 2:
                    return 0.0, 0.0
                # slope per second
                slope = np.polyfit(x, y, 1)[0]
                mean = y.mean() if y.size else 0.0
                std = y.std() if y.size else 0.0
                vol = std / mean if mean != 0 else 0.0
                # convert slope to percent per day for easier messaging
                slope_pct_per_day = (slope / mean * 86400 * 100) if mean != 0 else 0.0
                return slope_pct_per_day, vol
            except Exception:
                return 0.0, 0.0

        # Requests Per Second (RPS)
        rps_pct, rps_delta, rps_note = _pct_and_delta(first.get("rps", 0), last.get("rps", 0))
        rps_slope_pct_day, rps_vol = _regression_info([p.get('rps', 0) for p in points])
        if rps_note == 'from_zero':
            rps_trend = f"🟢 New activity: {int(last.get('rps',0))} RPS (was 0)"
            rps_description = f"Throughput started from 0 and is now {last.get('rps',0):.1f} RPS. This indicates new measurable traffic."
        else:
            rps_pct = rps_pct or 0.0
            icon = '🟢' if rps_pct >= 5 or rps_slope_pct_day >= 1 else '🔴' if rps_pct <= -5 or rps_slope_pct_day <= -1 else '🟡'
            icon_rps = icon
            strength = ''
            if abs(rps_slope_pct_day) >= 1 and len(points) >= 3:
                strength = f" (~{rps_slope_pct_day:+.1f}%/day)"
            volatility_note = ' volatile' if rps_vol >= 0.25 else ''
            rps_trend = f"{icon_rps} {rps_delta:+.0f} ({rps_pct:+.1f}%) {strength}{volatility_note}"
            rps_description = (
                f"Throughput changed by {rps_pct:.1f}% (+{rps_delta:.0f} RPS){strength}." if abs(rps_pct) >= 5 else
                f"Throughput shows small changes ({rps_pct:+.1f}%){strength}."
            )

        # Average Response Time
        resp_pct, resp_delta, resp_note = _pct_and_delta(first.get("avg_response", 0), last.get("avg_response", 0))
        resp_slope_pct_day, resp_vol = _regression_info([p.get('avg_response', 0) for p in points])
        if resp_note == 'from_zero':
            response_trend = f"🟢 New measured response time: {last.get('avg_response',0):.1f} ms (was 0)"
            response_description = f"Average response time moved from 0 to {last.get('avg_response',0):.1f} ms; assess whether this is expected."
        else:
            resp_pct = resp_pct or 0.0
            icon = '🟢' if resp_pct <= -5 or resp_slope_pct_day <= -1 else '🔴' if resp_pct >= 5 or resp_slope_pct_day >= 1 else '🟡'
            icon_resp = icon
            strength = ''
            if abs(resp_slope_pct_day) >= 1 and len(points) >= 3:
                strength = f" (~{resp_slope_pct_day:+.1f}%/day)"
            volatility_note = ' volatile' if resp_vol >= 0.25 else ''
            # For response times, lower is better so sign is inverted in message
            response_trend = f"{icon_resp} {resp_delta:+.0f} ({resp_pct:+.1f}%) {strength}{volatility_note}"
            response_description = (
                f"Average response time changed by {resp_pct:.1f}% ({resp_delta:+.0f} ms){strength}." if abs(resp_pct) >= 5 else
                f"Average response time shows small changes ({resp_pct:+.1f}%){strength}."
            )

        # P95 Response Time
        p95_pct, p95_delta, p95_note = _pct_and_delta(first.get("p95_response", 0), last.get("p95_response", 0))
        p95_slope_pct_day, p95_vol = _regression_info([p.get('p95_response', 0) for p in points])
        if p95_note == 'from_zero':
            p95_response_trend = f"🟢 New P95 value: {last.get('p95_response',0):.1f} ms (was 0)"
            p95_response_description = f"P95 increased from 0 to {last.get('p95_response',0):.1f} ms; investigate if this is expected under test conditions."
        else:
            p95_pct = p95_pct or 0.0
            icon_p95 = '🟢' if p95_pct <= -5 or p95_slope_pct_day <= -1 else '🔴' if p95_pct >= 5 or p95_slope_pct_day >= 1 else '🟡'
            strength_p95 = ''
            if abs(p95_slope_pct_day) >= 1 and len(points) >= 3:
                strength_p95 = f" (~{p95_slope_pct_day:+.1f}%/day)"
            volatility_note_p95 = ' volatile' if p95_vol >= 0.25 else ''
            p95_response_trend = f"{icon_p95} {p95_delta:+.1f}ms ({p95_pct:+.1f}%) {strength_p95}{volatility_note_p95}"
            p95_response_description = (
                f"The 95th percentile response time decreased by {abs(p95_pct):.1f}% ({abs(p95_delta):.1f} ms){strength_p95}, showing improved response times for nearly all users." if p95_pct <= -5 else
                f"The 95th percentile response time increased by {p95_pct:.1f}% ({p95_delta:+.1f} ms){strength_p95}, indicating delays are affecting a larger portion of users." if p95_pct >= 5 else
                f"The 95th percentile response time stayed stable, showing only a {p95_pct:.1f}% change ({p95_delta:+.1f} ms)."
            )

        # Max Response Time
        max_pct, max_delta, max_note = _pct_and_delta(first.get("max_response", 0), last.get("max_response", 0))
        max_slope_pct_day, max_vol = _regression_info([p.get('max_response', 0) for p in points])
        if max_note == 'from_zero':
            max_response_trend = f"🟢 New Max value: {last.get('max_response',0):.1f} ms (was 0)"
            max_response_description = f"Max response time moved from 0 to {last.get('max_response',0):.1f} ms; examine outliers causing this." 
        else:
            max_pct = max_pct or 0.0
            icon_max = '🟢' if max_pct <= -5 or max_slope_pct_day <= -1 else '🔴' if max_pct >= 5 or max_slope_pct_day >= 1 else '🟡'
            strength_max = ''
            if abs(max_slope_pct_day) >= 1 and len(points) >= 3:
                strength_max = f" (~{max_slope_pct_day:+.1f}%/day)"
            volatility_note_max = ' volatile' if max_vol >= 0.25 else ''
            max_response_trend = f"{icon_max} {max_delta:+.1f}ms ({max_pct:+.1f}%) {strength_max}{volatility_note_max}"
            max_response_description = (
                f"The maximum response time improved significantly by {abs(max_pct):.1f}% ({abs(max_delta):.1f} ms){strength_max}, reducing the longest delays users may experience." if max_pct <= -5 else
                f"The maximum response time worsened by {max_pct:.1f}% ({max_delta:+.1f} ms){strength_max}, meaning some requests are now taking much longer to complete." if max_pct >= 5 else
                f"The maximum response time remained steady with a small change of {max_pct:.1f}% ({max_delta:+.1f} ms)."
            )

        # Failure Rate (percentage points)
        fr_first = float(first.get("failure_rate", 0.0))
        fr_last = float(last.get("failure_rate", 0.0))
        fr_delta = fr_last - fr_first
        fr_slope_pct_day, fr_vol = _regression_info([p.get('failure_rate', 0.0) for p in points])
        if fr_first == 0:
            if fr_last == 0:
                failure_rate_trend = f"🟡 {fr_delta:+.1f}% (no change)"
                failure_rate_description = f"The failure rate remained consistent at 0.0%."
            else:
                failure_rate_trend = f"🔴 Increased from 0.0% to {fr_last:.2f}% (Δ {fr_delta:+.2f} percentage points)"
                failure_rate_description = f"Failure rate rose from 0.0% to {fr_last:.2f}%, indicating new failures that require investigation."
        else:
            fr_pct = (fr_delta / fr_first) * 100
            icon_fr = '🟢' if fr_pct <= -5 or fr_slope_pct_day <= -1 else '🔴' if fr_pct >= 5 or fr_slope_pct_day >= 1 else '🟡'
            strength_fr = ''
            if abs(fr_slope_pct_day) >= 1 and len(points) >= 3:
                strength_fr = f" (~{fr_slope_pct_day:+.1f}%/day)"
            volatility_note_fr = ' volatile' if fr_vol >= 0.25 else ''
            failure_rate_trend = f"{icon_fr} {fr_delta:+.2f}% ({fr_pct:+.1f}%){strength_fr}{volatility_note_fr}"
            if fr_pct <= -5:
                failure_rate_description = f"The failure rate improved, decreasing by {abs(fr_pct):.1f}% ({abs(fr_delta):.2f} percentage points){strength_fr}."
            else:
                if fr_pct >= 5:
                    failure_rate_description = f"The failure rate increased by {fr_pct:.1f}% ({fr_delta:+.2f} percentage points){strength_fr}, suggesting a decline in reliability."
                else:
                    failure_rate_description = f"The failure rate remained consistent with minimal change ({fr_pct:.1f}% / {fr_delta:+.2f} percentage points)."

        # Build short, human-friendly summaries for compact displays
        if isinstance(rps_pct, (int, float)):
            rps_short = f"{icon_rps} {rps_pct:+.1f}% — {'up' if rps_delta>0 else 'down' if rps_delta<0 else 'no change'} ({int(last.get('rps',0))} RPS)"
        else:
            rps_short = rps_trend

        if isinstance(resp_pct, (int, float)):
            response_short = f"{icon_resp if not np.isnan(resp_pct) else '🟡'} {resp_pct:+.1f}% — {'faster' if resp_delta<0 else 'slower' if resp_delta>0 else 'unchanged'} ({last.get('avg_response',0):.1f} ms)"
        else:
            response_short = response_trend

        if isinstance(p95_pct, (int, float)):
            p95_short = f"{icon_p95 if p95_pct==p95_pct else '🟡'} {p95_pct:+.1f}% — {'improved' if p95_delta<0 else 'worsened' if p95_delta>0 else 'unchanged'} ({last.get('p95_response',0):.1f} ms)"
        else:
            p95_short = p95_response_trend

        if isinstance(max_pct, (int, float)):
            max_short = f"{icon_max if max_pct==max_pct else '🟡'} {max_pct:+.1f}% — {'better' if max_delta<0 else 'worse' if max_delta>0 else 'unchanged'} ({last.get('max_response',0):.1f} ms)"
        else:
            max_short = max_response_trend

        if fr_first == 0 and fr_last == 0:
            failure_short = "🟡 0.00% — no change"
        elif fr_first == 0 and fr_last != 0:
            failure_short = f"🔴 Increased to {fr_last:.2f}%"
        else:
            failure_short = f"{icon_fr if 'icon_fr' in locals() else '🟡'} {fr_delta:+.2f}% ({fr_pct:+.1f}%)"

        return {
            'rps_trend': rps_trend,
            'rps_description': rps_description,
            'rps_short': rps_short,
            'response_trend': response_trend,
            'response_description': response_description,
            'response_short': response_short,
            'p95_response_trend': p95_response_trend,
            'p95_response_description': p95_response_description,
            'p95_short': p95_short,
            'max_response_trend': max_response_trend,
            'max_response_description': max_response_description,
            'max_short': max_short,
            'failure_rate_trend': failure_rate_trend,
            'failure_rate_description': failure_rate_description,
            'failure_short': failure_short
        }

    def generate_key_insights(ratings, trends, latest_test, test_type):
        """Generate a dynamic Key Insights section."""
        normalized_type = normalize_test_type(test_type)
        standards = PERFORMANCE_STANDARDS.get(normalized_type, PERFORMANCE_STANDARDS["load"])["metrics"]
        
        good_points = []
        bad_points = []
        analogy = "a dependable but busy service desk"

        # Helpers for parsing
        def _parse_percent(trend_str):
            """Try to extract the percent value from trend strings like '🟢 +200 (+46.4%)' or handle 'New' cases."""
            if not trend_str or not isinstance(trend_str, str):
                return None, 'unknown'
            if 'New' in trend_str or 'New activity' in trend_str or 'Increased from 0' in trend_str:
                return None, 'from_zero'
            m = re.findall(r'([+-]?\d+(?:\.\d+)?)%+', trend_str)
            if m:
                try:
                    return float(m[-1]), 'ok'
                except Exception:
                    return None, 'invalid'
            return None, 'none'

        def _get_rating(ratings, *keys):
            for k in keys:
                if k in ratings:
                    val = ratings[k]
                    return val[2] if isinstance(val, (list, tuple)) and len(val) > 2 else val
            return 5

        # RPS
        rps_rating = _get_rating(ratings, 'Requests Per Second (RPS)', 'rps', 'RPS')
        rps_pct, rps_note = _parse_percent(trends.get('rps_trend', ''))
        if rps_note == 'from_zero':
            good_points.append(f"Throughput is now measurable (started from 0). Current RPS: {latest_test.get('rps', 0):.1f}.")
        else:
            rps_pct = rps_pct or 0
            if rps_rating <= 2 or rps_pct <= -10:
                bad_points.append(f"Throughput is low (RPS down {abs(rps_pct):.1f}%), limiting the system's capacity to handle requests.")
                analogy += " with fewer open counters"
            elif rps_rating >= 4 or rps_pct >= 5:
                good_points.append(f"Throughput is strong (RPS change {rps_pct:+.1f}%), showing improved request handling capacity.")
            else:
                good_points.append(f"Throughput is stable, maintaining consistent request processing.")

        # Avg Response Time
        avg_rating = _get_rating(ratings, 'Average Response Time (ms)', 'avg_response', 'avg')
        avg_response = latest_test.get('avg_response', 0.0)
        avg_pct, avg_note = _parse_percent(trends.get('response_trend', ''))
        if avg_note == 'from_zero':
            bad_points.append(f"Average response time recorded as {avg_response:.1f} ms (no previous value to compare).")
        else:
            avg_pct = avg_pct or 0
            if avg_rating <= 2 or avg_pct >= 10:
                bad_points.append(f"Average response time worsened by {avg_pct:.1f}%, users may experience slower interactions.")
                if avg_response >= 1000:
                    bad_points.append(f"Average response time is high ({avg_response/1000:.1f} seconds), slowing down user experience.")
                    analogy += " with long lines at the counter"
            elif avg_rating >= 4 or avg_pct <= -5:
                good_points.append(f"Average response time improved ({avg_pct:+.1f}%).")
            else:
                good_points.append("Average response time is stable.")

        # P95 Response Time
        p95_rating = _get_rating(ratings, '95th Percentile Response Time (ms)', 'p95_response', 'p95')
        p95_response = latest_test.get('p95_response', 0.0)
        p95_pct, p95_note = _parse_percent(trends.get('p95_response_trend', ''))
        if p95_note == 'from_zero':
            bad_points.append(f"P95 recorded as {p95_response:.1f} ms with no prior data to compare.")
        else:
            p95_pct = p95_pct or 0
            if p95_rating <= 2 or p95_pct >= 10:
                bad_points.append(f"P95 response time is problematic ({p95_response/1000:.1f} seconds, Δ {p95_pct:+.1f}%), causing delays for some users.")
                analogy += " and some customers waiting longer"
            elif p95_rating >= 4 or p95_pct <= -5:
                good_points.append(f"P95 response time is outstanding ({p95_response/1000:.1f} seconds), showing consistent performance.")
            else:
                good_points.append(f"P95 response time is stable ({p95_response/1000:.1f} seconds), maintaining reliability.")

        # Max Response Time
        max_rating = _get_rating(ratings, 'Max Response Time (ms)', 'max_response', 'max')
        max_response = latest_test.get('max_response', 0.0)
        max_pct, max_note = _parse_percent(trends.get('max_response_trend', ''))
        if max_note == 'from_zero':
            bad_points.append(f"Max response recorded as {max_response:.1f} ms with no prior data to compare.")
        else:
            max_pct = max_pct or 0
            if max_rating <= 2 or max_pct >= 10:
                bad_points.append(f"Maximum response time is critical ({max_response/1000:.1f} seconds, Δ {max_pct:+.1f}%), risking timeouts.")
                analogy += " and some customers waiting hours"
            elif max_rating >= 4 or max_pct <= -5:
                good_points.append(f"Maximum response time is excellent ({max_response/1000:.1f} seconds), preventing extreme delays.")
            else:
                good_points.append(f"Maximum response time is acceptable ({max_response/1000:.1f} seconds), within expected limits.")

        # Failure Rate
        failure_rating = _get_rating(ratings, 'Failure Rate (%)', 'failure_rate')
        failure_rate = latest_test.get('failure_rate', 0.0)
        fr_pct, fr_note = _parse_percent(trends.get('failure_rate_trend', ''))
        if fr_note == 'from_zero':
            bad_points.append(f"Failure rate increased from 0.0% to {failure_rate:.2f}%, which requires investigation.")
            analogy += " with some requests not being processed"
        else:
            fr_pct = fr_pct or 0
            if failure_rating <= 2 or fr_pct >= 5:
                bad_points.append(f"Failure rate is high ({failure_rate:.2f}%), impacting system reliability.")
                analogy += " with some requests not being processed"
            elif failure_rate == 0.0:
                good_points.append(f"Perfect reliability (0.0% failures), ensuring all requests succeed.")
                analogy += " that never fails to serve"
            else:
                good_points.append(f"Failure rate is acceptable ({failure_rate:.2f}%), maintaining stable operation.")

        # Determine overall scenario
        def _count_criticals(ratings):
            c = 0
            for v in ratings.values():
                try:
                    rv = v[2]
                except Exception:
                    try:
                        rv = int(v)
                    except Exception:
                        rv = 5
                if rv <= 2:
                    c += 1
            return c

        critical_count = _count_criticals(ratings)
        scenario = "high_latency" if critical_count >= 2 and failure_rate <= standards["Failure Rate (%)"]["warning"] else \
                "high_failure" if failure_rate > standards["Failure Rate (%)"]["critical"] else \
                "mixed"

        if scenario == "high_latency":
            overall = f"The system is reliable but slow, with response times exceeding targets. It's like {analogy} that needs optimization."
        elif scenario == "high_failure":
            overall = f"The system is unreliable with frequent failures. It's like {analogy} that drops customer requests."
        else:
            overall = f"The system shows mixed performance. It's like {analogy} needing targeted improvements."

        # Create a concise one-line summary for quick reading
        top_good = good_points[0] if good_points else ''
        top_bad = bad_points[0] if bad_points else ''
        short_summary_parts = [p for p in (top_good, top_bad) if p]
        short_summary = ' • '.join(short_summary_parts) if short_summary_parts else overall

        return {
            "good_points": good_points,
            "bad_points": bad_points,
            "overall": overall,
            "scenario": scenario,
            "short_summary": short_summary
        }

    def generate_recommendations(ratings, latest_test, test_type, trends, insights):
        """Generate performance recommendations with enhanced positive feedback."""
        normalized_type = normalize_test_type(test_type)
        standards = PERFORMANCE_STANDARDS.get(normalized_type, PERFORMANCE_STANDARDS["load"])["metrics"]
        
        recommendations = []
        next_steps = []
        priority_map = {1: "🔴 Critical (Act Immediately)", 2: "🚨 High (Address Soon)", 3: "⚠️ Medium (Plan to Fix)", 5: "🧩 Low (Monitor)"}

        # Scenario-based overall recommendation
        scenario = insights["scenario"]
        if scenario == "high_latency":
            recommendations.append("The system meets reliability standards but suffers from slow response times. Focus on reducing latency to improve user experience.")
        elif scenario == "high_failure":
            recommendations.append("The system fails too often, compromising reliability. Immediate fixes are needed to reduce errors.")
        else:
            recommendations.append("The system shows mixed performance. Address critical issues first, then optimize other areas.")

        # RPS
        rps = latest_test.get('rps', 0.0)
        rps_target = standards['Requests Per Second (RPS)']['target']
        rps_rating = ratings.get('rps', (None, None, 5))[2]
        rps_change = float(trends['rps_trend'].split(' ')[-1][:-1]) if '<span' in trends['rps_trend'] else 0
        
        if rps_rating <= 2 or rps_change <= -10:
            recommendations.append(f"Throughput needs improvement ({rps:.1f} RPS vs. Target: {rps_target}). The system cannot handle the desired request volume.")
            next_steps.append(
                f"{priority_map[rps_rating]} Increase Throughput:\n\n"
                "• Upgrade server resources (CPU/memory) for higher capacity (Effort: 1-2 weeks, Impact: High)\n"
                "• Optimize database with strategic indexing (Effort: 1 week, Impact: Medium)\n"
                "• Implement horizontal scaling with load balancing (Effort: 2-3 weeks, Impact: High)\n"
                "• Profile application code for bottlenecks (Effort: 1 week, Impact: Medium)"
            )
        elif rps >= rps_target:
            recommendations.append(f"Throughput is excellent ({rps:.1f} RPS vs. Target: {rps_target}). The system reliably handles expected load.")
        else:
            recommendations.append(f"Throughput is adequate ({rps:.1f} RPS vs. Target: {rps_target}). Consider optimizations for future growth.")

        # Avg Response Time
        avg_response = latest_test.get('avg_response', 0.0)
        avg_target = standards['Average Response Time (ms)']['target']
        avg_rating = ratings.get('avg_response', (None, None, 5))[2]
        
        if avg_rating <= 2:
            recommendations.append(f"Average response time requires optimization ({avg_response:.1f}ms vs. Target: {avg_target}). Most requests are slower than desired.")
            next_steps.append(
                f"{priority_map[avg_rating]} Reduce Latency:\n\n"
                "• Analyze slow endpoints with distributed tracing (Effort: 3-5 days, Impact: High)\n"
                "• Optimize critical code paths (Effort: 1-2 weeks, Impact: Medium)\n"
                "• Implement caching for frequent data (Effort: 2 weeks, Impact: High)\n"
                "• Review network configuration (Effort: 1 week, Impact: Medium)"
            )
        elif avg_response <= avg_target * 0.5:  # 50% better than target
            recommendations.append(f"Average response time is outstanding ({avg_response:.1f}ms vs. Target: {avg_target}). The system delivers exceptional speed.")
        else:
            recommendations.append(f"Average response time is excellent ({avg_response:.1f}ms vs. Target: {avg_target}). The system performs reliably.")

        # P95 Response Time
        p95_response = latest_test.get('p95_response', 0.0)
        p95_target = standards['95th Percentile Response Time (ms)']['target']
        p95_rating = ratings.get('p95_response', (None, None, 5))[2]
        
        if p95_rating <= 2:
            recommendations.append(f"P95 response time needs attention ({p95_response:.1f}ms vs. Target: {p95_target}). Some users experience delays.")
            next_steps.append(
                f"{priority_map[p95_rating]} Improve Consistency:\n\n"
                "• Identify slowest 5% of transactions (Effort: 3-5 days, Impact: High)\n"
                "• Optimize complex database queries (Effort: 1-2 weeks, Impact: Medium)\n"
                "• Cache results for slow endpoints (Effort: 2 weeks, Impact: Medium)\n"
                "• Conduct targeted load testing (Effort: 1 week, Impact: Medium)"
            )
        elif p95_response <= p95_target * 0.5:
            recommendations.append(f"P95 response time is exceptional ({p95_response:.1f}ms vs. Target: {p95_target}). The system delivers consistent performance.")
        else:
            recommendations.append(f"P95 response time is excellent ({p95_response:.1f}ms vs. Target: {p95_target}). User experience remains reliable.")

        # Max Response Time
        max_response = latest_test.get('max_response', 0.0)
        max_target = standards['Max Response Time (ms)']['target']
        max_rating = ratings.get('max_response', (None, None, 5))[2]
        
        if max_rating <= 2:
            recommendations.append(f"Maximum response time is critical ({max_response:.1f}ms vs. Target: {max_target}). Some requests risk timing out.")
            next_steps.append(
                f"{priority_map[max_rating]} Fix Extreme Cases:\n\n"
                "• Investigate multi-second requests (Effort: 3-5 days, Impact: Critical)\n"
                "• Implement request timeouts (Effort: 1 week, Impact: High)\n"
                "• Resolve database locking issues (Effort: 1-2 weeks, Impact: High)\n"
                "• Add circuit breaking for dependencies (Effort: 2 weeks, Impact: High)"
            )
        elif max_response <= max_target * 0.3:
            recommendations.append(f"Maximum response time is outstanding ({max_response:.1f}ms vs. Target: {max_target}). The system handles edge cases reliably.")
        else:
            recommendations.append(f"Maximum response time is excellent ({max_response:.1f}ms vs. Target: {max_target}). No extreme delays detected.")

        # Failure Rate
        failure_rate = latest_test.get('failure_rate', 0.0)
        failure_target = standards['Failure Rate (%)']['target']
        failure_rating = ratings.get('failure_rate', (None, None, 5))[2]
        
        if failure_rating <= 2:
            recommendations.append(f"Failure rate is problematic ({failure_rate:.2f}% vs. Target: {failure_target}). System reliability needs improvement.")
            next_steps.append(
                f"{priority_map[failure_rating]} Enhance Stability:\n\n"
                "• Analyze error patterns in logs (Effort: 2-3 days, Impact: High)\n"
                "• Fix root cause bugs (Effort: 1-2 weeks, Impact: High)\n"
                "• Implement smart retry logic (Effort: 1 week, Impact: Medium)\n"
                "• Configure failure rate alerts (Effort: 1 week, Impact: Medium)"
            )
        elif failure_rate == 0.0:
            recommendations.append(f"Perfect reliability achieved (0.0% failures). The system operates flawlessly under load.")
        elif failure_rate <= failure_target * 0.5:
            recommendations.append(f"Failure rate is excellent ({failure_rate:.2f}% vs. Target: {failure_target}). The system demonstrates strong reliability.")
        else:
            recommendations.append(f"Failure rate is acceptable ({failure_rate:.2f}% vs. Target: {failure_target}). Continue current maintenance practices.")

        return recommendations, next_steps

    def generate_project_html(project_name, project_data, timestamp):
        """Generate HTML content for a project with Key Insights."""
        tests = project_data['tests']
        status_counts = project_data['status_counts']
        total_tests = status_counts['healthy'] + status_counts['warning'] + status_counts['critical']
        performance_trend = project_data['performance_trend']
        
        # Build a list of valid trend points sorted by date
        valid_trends = []
        for t in performance_trend:
            try:
                if t.get('date') and t['date'] != 'Invalid':
                    parsed = datetime.strptime(t['date'], "%Y-%m-%d %H:%M:%S")
                    valid_trends.append((parsed, t))
            except Exception:
                # ignore invalid dates
                continue
        valid_trends.sort(key=lambda x: x[0])
        sorted_trends = [t for _, t in valid_trends]

        # Derive earliest and latest tests from sorted trends
        if sorted_trends:
            earliest_test = sorted_trends[0]
            latest_test = sorted_trends[-1]
        else:
            earliest_test = latest_test = {
                'rps': 883.0, 'avg_response': 1535.0, 'p95_response': 2700.0, 
                'max_response': 140322.0, 'failure_rate': 0.0, 'test_type': 'Load Test', 
                'date': timestamp
            }

        # ==== CALCULATE OVERALL RATING BASED ONLY ON TEST COUNTS ====
        # Healthy = 5 points, Warning = 3 points, Critical = 1 point
        
        # Get counts
        healthy_count = status_counts.get('healthy', 0)
        warning_count = status_counts.get('warning', 0)
        critical_count = status_counts.get('critical', 0)
        
        # Calculate total weighted score
        total_weighted_score = (healthy_count * 5) + (warning_count * 3) + (critical_count * 1)
        
        # Calculate average rating
        if total_tests > 0:
            average_rating = total_weighted_score / total_tests
        else:
            average_rating = 0
        
        # Determine overall status using the rating scheme (1-5 labels)
        average_label, overall_class, stars = rating_float_to_label_and_class(average_rating)
        project_status = average_label

        def get_rating_icon(rating):
            """Return an emoji icon for a given rating (1-5)."""
            if rating >= 5:
                return "🌟"
            elif rating == 4:
                return "✅"
            elif rating == 3:
                return "🟡"
            elif rating == 2:
                return "⚠️"
            else:
                return "❌"

        status_icon = get_rating_icon(round(average_rating))
        
        # Format average rating for display
        avg_rating_formatted = f"{average_rating:.1f}"
        
        test_type = latest_test.get('test_type', 'Load Test')
        
        # Use sorted trends for calculations (more robust than relying on list order)
        trend_data = calculate_trends(sorted_trends if sorted_trends else performance_trend)
        ratings = {
            metric: get_status_and_rating(metric, latest_test.get(metric, 0), test_type)
            for metric in ["Requests Per Second (RPS)", "Average Response Time (ms)", "95th Percentile Response Time (ms)", "Max Response Time (ms)", "Failure Rate (%)"]
        }
        insights = generate_key_insights(ratings, trend_data, latest_test, test_type)
        recommendations, next_steps = generate_recommendations(ratings, latest_test, test_type, trend_data, insights)
        # build HTML for next steps outside the f-string to avoid backslashes inside f-string expressions
        next_steps_html = "".join(
            f"<li><ul>{''.join(f'<li>{sub_step}</li>' for sub_step in step.splitlines() if sub_step)}</ul></li>"
            for step in next_steps
        )
        test_types = list({test.get('test_type', 'Load Test') for test in tests})
        trend_plot_html = create_trend_plot(sorted_trends if sorted_trends else performance_trend, project_name)
        
        html_content = f"""
            <div class="project-section">
                <div class="report-info">
                    <div class="info-box">
                        <h3>Test Information</h3>
                        <p><strong>Project Title:</strong> {project_name}</p>
                        <p><strong>Test Types:</strong> {', '.join(test_types)}</p>
                        <p><strong>Test ID:</strong> Multiple</p>
                    </div>
                    <div class="info-box">
                        <h3>Test Summary</h3>
                        <p><strong>Date:</strong> {timestamp}</p>
                        <p><strong>Tested By:</strong> Quality Assurance Department</p>
                    </div>
                    <div class="info-box">
                        <h3>System Information</h3>
                        <p><strong>Tool Version:</strong> Locust 3.35</p>
                        <p><strong>Generated By:</strong> EAII🚀PTT</p>
                    </div>
                </div>
                <div class="project-summary">
                    <h2>{project_name} Performance Summary</h2>
                    <div class="status-overview">
                        <div class="status-item healthy">
                            <div>Healthy Tests</div>
                            <div class="metric-value">{status_counts['healthy']}</div>
                        </div>
                        <div class="status-item warning">
                            <div>Warning Tests</div>
                            <div class="metric-value">{status_counts['warning']}</div>
                        </div>
                        <div class="status-item critical">
                            <div>Critical Tests</div>
                            <div class="metric-value">{status_counts['critical']}</div>
                        </div>
                    </div>
                    <h3>Overall Performance Results: <span class="{overall_class}">{status_icon} {project_status} {stars} Average Rating: {average_rating:.1f}/5</span></h3>
                    <div class="metrics-grid">
                        <div class="metric-card">
                            <div>Requests/Sec</div>
                            <div class="metric-value">{latest_test.get('rps', 89.0):.1f}</div>
                        </div>
                        <div class="metric-card">
                            <div>Avg Response (ms)</div>
                            <div class="metric-value">{latest_test.get('avg_response', 74.0):.1f}</div>
                        </div>
                        <div class="metric-card">
                            <div>P95 Response (ms)</div>
                            <div class="metric-value">{latest_test.get('p95_response', 320.0):.1f}</div>
                        </div>
                        <div class="metric-card">
                            <div>Max Response (ms)</div>
                            <div class="metric-value">{latest_test.get('max_response', 1194.0):.1f}</div>
                        </div>
                        <div class="metric-card">
                            <div>Failure Rate (%)</div>
                            <div class="metric-value">{latest_test.get('failure_rate', 0.0):.2f}</div>
                        </div>
                    </div>
                    <h3>Performance Trends</h3>
                    <div class="graph-container">
                        {trend_plot_html}
                    </div>
                    <table>
                        <thead>
                            <tr>
                                <th>Metric</th>
                                <th>Initial Value</th>
                                <th>Latest Value</th>
                                <th>Trend</th>
                                <th>Description</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Requests/Sec</td>
                                <td>{earliest_test.get('rps', 89.0):.1f}</td>
                                <td>{latest_test.get('rps', 89.0):.1f}</td>
                                <td>{trend_data['rps_trend']}</td>
                                <td>{trend_data['rps_description']}</td>
                            </tr>
                            <tr>
                                <td>Avg Response (ms)</td>
                                <td>{earliest_test.get('avg_response', 74.0):.1f}</td>
                                <td>{latest_test.get('avg_response', 74.0):.1f}</td>
                                <td>{trend_data['response_trend']}</td>
                                <td>{trend_data['response_description']}</td>
                            </tr>
                            <tr>
                                <td>P95 Response (ms)</td>
                                <td>{earliest_test.get('p95_response', 320.0):.1f}</td>
                                <td>{latest_test.get('p95_response', 320.0):.1f}</td>
                                <td>{trend_data['p95_response_trend']}</td>
                                <td>{trend_data['p95_response_description']}</td>
                            </tr>
                            <tr>
                                <td>Max Response (ms)</td>
                                <td>{earliest_test.get('max_response', 1194.0):.1f}</td>
                                <td>{latest_test.get('max_response', 1194.0):.1f}</td>
                                <td>{trend_data['max_response_trend']}</td>
                                <td>{trend_data['max_response_description']}</td>
                            </tr>
                            <tr>
                                <td>Failure Rate (%)</td>
                                <td>{earliest_test.get('failure_rate', 0.0):.2f}</td>
                                <td>{latest_test.get('failure_rate', 0.0):.2f}</td>
                                <td>{trend_data['failure_rate_trend']}</td>
                                <td>{trend_data['failure_rate_description']}</td>
                            </tr>
                        </tbody>
                    </table>
                    <div class="recommendations">
                        <h3>Overall Performance Results: <span class="{overall_class}">{status_icon} {project_status} {stars} Average Rating: {average_rating:.1f}/5</span></h3>
                        <h4>Recommendations</h4>
                        <ul>{"".join([f"<li>{rec}</li>" for rec in recommendations])}</ul>
                        <h4>Next Steps</h4>
                        <div class="next-steps">
                            <ul>{next_steps_html}</ul>
                        </div>
                    </div>
                </div>
        """
        
        for test in sorted(tests, key=lambda x: x.get("timestamp", ""), reverse=True):
            status_class = "status-critical" if "Critical" in test.get("overall_status", "") else \
                        "status-warning" if "Warning" in test.get("overall_status", "") else "status-healthy"
            
            try:
                test_date = datetime.fromisoformat(test["timestamp"]).strftime("%Y-%m-%d %H:%M:%S") if test.get("timestamp") else "Unknown"
            except (ValueError, TypeError) as e:
                print(f"Invalid timestamp format in test {test.get('test_id', 'N/A')}: {e}")
                test_date = "Invalid"

            graph_base64 = ""
            graph_file = test.get('graph_file', '')
            
            # Try to load existing graph file first
            if graph_file and os.path.exists(graph_file):
                try:
                    with open(graph_file, 'rb') as f:
                        graph_base64 = base64.b64encode(f.read()).decode()
                except Exception as e:
                    print(f"Failed to read graph file {graph_file} for test {test.get('test_id', 'N/A')}: {e}")
                    graph_base64 = ""
            
            # If graph file is missing or couldn't be loaded, generate it on the fly
            if not graph_base64:
                try:
                    stats = test.get('stats', {})
                    actual_performance = [
                        stats.get('rps', 0),
                        stats.get('p95_response_time', 0),
                        stats.get('avg_response_time', 0),
                        stats.get('max_response_time', 0),
                        stats.get('failures_rate', 0)
                    ]
                    fig = generate_performance_graph(
                        actual_performance,
                        test.get('test_type', 'Load').lower(),
                        stats.get('total_requests', 0),
                        stats.get('failures_rate', 0)
                    )
                    buf = io.BytesIO()
                    fig.savefig(buf, format='png', bbox_inches="tight", dpi=100)
                    buf.seek(0)
                    graph_base64 = base64.b64encode(buf.read()).decode()
                    plt.close(fig)
                except Exception as e:
                    print(f"Failed to generate graph for test {test.get('test_id', 'N/A')}: {e}")
                    graph_base64 = ""

            # Prepare display for users and duration
            users_display = test.get('users', 'N/A')
            duration_raw = test.get('duration', None)
            duration_display = format_duration_display(duration_raw)

            html_content += f"""
                <div class="test-card">
                    <h3>Test Type: {test.get('test_type', 'N/A')} 
                        <span class="{status_class}">{test.get('overall_status', 'Unknown')}</span>
                    </h3>
                    <p><strong>Test ID:</strong> {test.get('test_id', 'N/A')} • <strong>Date:</strong> {test_date} • <strong>Users:</strong> {users_display} • <strong>Duration:</strong> {duration_display}</p>
                    <div class="metrics-grid">
                        <div class="metric-card">
                            <div>Requests/Sec</div>
                            <div class="metric-value">{test['stats'].get('rps', 'N/A')}</div>
                        </div>
                        <div class="metric-card">
                            <div>Avg Response (ms)</div>
                            <div class="metric-value">{test['stats'].get('avg_response_time', 'N/A')}</div>
                        </div>
                        <div class="metric-card">
                            <div>P95 Response (ms)</div>
                            <div class="metric-value">{test['stats'].get('p95_response_time', 'N/A')}</div>
                        </div>
                        <div class="metric-card">
                            <div>Max Response (ms)</div>
                            <div class="metric-value">{test['stats'].get('max_response_time', 'N/A')}</div>
                        </div>
                        <div class="metric-card">
                            <div>Failure Rate (%)</div>
                            <div class="metric-value">{(test['stats'].get('failures', 0) / test['stats'].get('total_requests', 1) * 100):.2f}</div>
                        </div>
                    </div>
            """
            if graph_base64:
                html_content += f"""
                    <div class="graph-container">
                        <h4>Performance Graph</h4>
                        <img src="data:image/png;base64,{graph_base64}" alt="Performance Graph for Test {test.get('test_id', 'N/A')}">
                    </div>
                """
            else:
                html_content += """
                    <div class="graph-container">
                        <p>No graph file available</p>
                    </div>
                """
            
            html_content += "</div>"
        
        html_content += "</div>"
        return html_content

    def generate_history_report(test_history, project_name=None):
        """Generate comprehensive HTML report with health scoring, per-test graphs, and trend plot."""
        if project_name:
            test_history = [t for t in test_history if t.get('project_name') == project_name]
        
        print(f"Filtered test_history count: {len(test_history)}")
        for idx, test in enumerate(test_history):
            print(f"Test {idx + 1} test_type: {test.get('test_type', 'Missing')}")
            print(f"Test {idx + 1} stats: {json.dumps(test.get('stats', {}), indent=2)}")
        
        projects = {}
        for test in test_history:
            try:
                project_name = test['project_name']
                test_type = test.get('test_type', 'Load Test')
                test_type = test_type if test_type in PERFORMANCE_STANDARDS else 'Load Test'
                
                if project_name not in projects:
                    projects[project_name] = {
                        'tests': [],
                        'total_tests': 0,
                        'total_requests': 0,
                        'total_failures': 0,
                        'status_counts': {'healthy': 0, 'warning': 0, 'critical': 0},
                        'performance_trend': []
                    }
                
                projects[project_name]['tests'].append(test)
                projects[project_name]['total_tests'] += 1
                
                total_requests = test['stats'].get('total_requests', 0)
                total_failures = test['stats'].get('failures', 0)
                if isinstance(total_requests, list):
                    print(f"Warning: total_requests is a list: {total_requests}. Using first element or 0.")
                    total_requests = total_requests[0] if total_requests else 0
                if isinstance(total_failures, list):
                    print(f"Warning: total_failures is a list: {total_failures}. Using first element or 0.")
                    total_failures = total_failures[0] if total_failures else 0
                
                projects[project_name]['total_requests'] += total_requests
                projects[project_name]['total_failures'] += total_failures
                
                status = test.get('overall_status', '').lower()
                if 'healthy' in status:
                    projects[project_name]['status_counts']['healthy'] += 1
                elif 'warning' in status:
                    projects[project_name]['status_counts']['warning'] += 1
                else:
                    projects[project_name]['status_counts']['critical'] += 1
                
                failure_rate = (total_failures / total_requests) * 100 if total_requests > 0 else 0
                
                try:
                    test_date = datetime.fromisoformat(test['timestamp']).strftime("%Y-%m-%d %H:%M:%S") if test.get("timestamp") else "Unknown"
                except (ValueError, TypeError) as e:
                    print(f"Invalid timestamp format in test {test.get('test_id', 'N/A')}: {e}")
                    test_date = "Invalid"
                
                projects[project_name]['performance_trend'].append({
                    'date': test_date,
                    'rps': float(test['stats'].get('rps', 89.0)),
                    'avg_response': float(test['stats'].get('avg_response_time', 74.0)),
                    'p95_response': float(test['stats'].get('p95_response_time', 320.0)),
                    'max_response': float(test['stats'].get('max_response_time', 1194.0)),
                    'failure_rate': float(failure_rate),
                    'test_type': test_type
                })
                
            except KeyError as e:
                print(f"Missing key in test data: {e}")
                continue

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Performance Test Report</title>
            <style>{CSS_STYLES}</style>
            <link href="https://fonts.googleapis.com/earlyaccess/notosansethiopic.css" rel="stylesheet">
        </head>
        <body>
            <div class="header">
            {(
                f"<img src='data:image/png;base64,{base64.b64encode(open('image/logo.png', 'rb').read()).decode()}' class='logo-img' style='width: 100px; height: 100px; margin-bottom: 15px; object-fit: contain;'>"
                if os.path.exists('image/logo.png')
                else "<img src='data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgdmlld0JveD0iMCAwIDEwMCAxMDAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0iTTUwIDVhNDAgNDAgMCAwIDAgMCA4MC40YzIuNi0xLjIgNS4xLTIuOCA3LjUtNC43IDYuMS00LjkgMTEuNS0xMS40IDE1LjQtMTguOCA0LjUtOC45IDcuMi0xOS4xIDcuMi0yOS45IDAtMjIuMTAtMTcuOS00MC00MC00MFoiIGZpbGw9IiNmOWE4MjUiLz48L3N2Zz4=' class='logo-img' style='width: 100px; height: 100px; margin-bottom: 15px; object-fit: contain;'>"
            )}
            <div class="institute-text">
                <h1 class="amh">የኢትዮጵያ አርቲፊሻል ኢንተለጀንስ ኢንስቲትዩት</h1>
                <h1 class="eng">ETHIOPIAN ARTIFICIAL INTELLIGENCE INSTITUTE</h1>
                <h2>EAII Performance Testing Tool</h2>
            </div>
        </div>

        """
        
        for project_name, project_data in projects.items():
            html_content += generate_project_html(project_name, project_data, timestamp)
        
        html_content += f"""
            <footer class="footer">
            <div class="footer-content">
                <p><strong>Ethiopian Artificial Intelligence Institute</strong></p>
                <p>Quality Assurance & Performance Testing Department</p>
                <hr style="border: 0; border-top: 1px solid rgba(255,255,255,0.2); margin: 10px 0;">
                <p>Report generated by <strong>EAII🚀PTT</strong> • {timestamp}</p>
                <p>Tool Version: <strong>1.0.0</strong></p>
                <p style="font-size: 0.85rem; opacity: 0.9;">For inquiries: qa@eaii.gov.et</p>
                <p style="margin-top: 10px; font-size: 0.85rem;">
                    Convert PDF using this URL: 
                    <a href="https://www.freeconvert.com/html-to-pdf" target="_blank">
                        https://www.freeconvert.com/html-to-pdf
                    </a>
                </p>
            </div>
        </footer>

        </body>
        </html>
        """

        return html_content

    


   # Custom CSS (modified to limit table body to five rows)
    st.markdown("""
    <style>
    .table-container {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        overflow-x: auto;
        background-color: #ffffff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .table-header {
        display: flex;
        padding: 12px;
        background-color: #f1f3f5;
        font-weight: 600;
        color: #333;
        border-bottom: 2px solid #e0e0e0;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        position: sticky;
        top: 0;
        z-index: 1;
    }
    .table-body {
        max-height: calc(5 * 48px); /* Approximately 5 rows (adjust 48px to match your row height) */
        overflow-y: auto;
        -webkit-overflow-scrolling: touch;
    }
    .table-row {
        display: flex;
        padding: 12px;
        border-bottom: 1px solid #f0f0f0;
        align-items: center;
        transition: background-color 0.2s;
        height: 48px; /* Fixed row height */
        box-sizing: border-box;
    }
    .table-row:hover {
        background-color: #05d9e8;
    }
    .table-cell {
        flex: 1;
        padding: 0 8px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        font-size: 14px;
    }
    .table-cell-id { flex: 1.5; }
    .table-cell-project { flex: 2; }
    .table-cell-type { flex: 1.5; }
    .table-cell-date { flex: 2; }
    .table-cell-status { flex: 1; }
    .table-cell-requests { flex: 1; }
    .table-cell-failure { flex: 1; }
    .table-cell-rps { flex: 1; }
    .table-cell-response { flex: 1; }
    .table-cell-actions { flex: 0.5; text-align: right; }
    .delete-btn {
        background-color: #ff4d4f;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 6px 12px;
        cursor: pointer;
        font-size: 14px;
        transition: background-color 0.2s;
    }
    .delete-btn:hover {
        background-color: #e63946;
    }
    .table-body::-webkit-scrollbar {
        width: 8px;
    }
    .table-body::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    .table-body::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 4px;
    }
    .table-body::-webkit-scrollbar-thumb:hover {
        background: #555;
    }
    </style>
""", unsafe_allow_html=True)

    def save_test_history(test_data, graph_filename=None):
        """Save test data to the test history JSON file with duplicate prevention."""
        history_file = "test_history/test_history.json"
        os.makedirs("test_history", exist_ok=True)

        # Ensure test_data has a test_id
        if "test_id" not in test_data:
            test_data["test_id"] = f"TEST_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

        # Prepare the test record
        test_record = {
            "test_id": test_data.get("test_id"),
            "project_name": test_data.get("project_name", "Unnamed"),
            "test_type": test_data.get("test_type", "Load"),
            "timestamp": test_data.get("timestamp", datetime.now().isoformat()),
            "users": test_data.get("users", "Unknown"),
            "duration": test_data.get("duration", "Unknown"),
            "overall_status": test_data.get("overall_status", "Unknown"),
            "stats": test_data.get("stats", {
                "total_requests": 0,
                "failures": 0,
                "rps": 0.0,
                "avg_response_time": 0.0,
                "p95_response_time": 0.0,
                "max_response_time": 0.0,
                "failures_rate": 0.0
            }),
            "graph_file": graph_filename if graph_filename and os.path.exists(graph_filename) else None
        }

        # Load existing history
        test_history = []
        try:
            if os.path.exists(history_file):
                with open(history_file, "r") as f:
                    test_history = json.load(f)
                    if not isinstance(test_history, list):
                        test_history = []
        except (json.JSONDecodeError, FileNotFoundError):
            test_history = []

        # Check for existing test with same ID
        existing_index = next((i for i, t in enumerate(test_history) 
                            if t["test_id"] == test_record["test_id"]), -1)

        if existing_index >= 0:
            # Update existing record
            test_history[existing_index] = test_record
            action = "updated"
        else:
            # Add new record
            test_history.append(test_record)
            action = "saved"

        # Save updated history
        try:
            with open(history_file, "w") as f:
                json.dump(test_history, f, indent=2)
            return True, f"Test '{test_record['test_id']}' {action} successfully! ✅"
        except Exception as e:
            return False, f"Failed to save test history: {e}"

    def create_zip_from_paths(paths):
        """Create a ZIP archive (bytes) from a list of files or directories.

        - paths: list of file paths or directory paths to include in the archive.
        Returns bytes of the ZIP file.
        """
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for p in paths:
                try:
                    if os.path.isdir(p):
                        for root, _, files in os.walk(p):
                            for fname in files:
                                fp = os.path.join(root, fname)
                                arcname = os.path.relpath(fp, start=p)
                                zf.write(fp, arcname)
                    elif os.path.exists(p):
                        zf.write(p, os.path.basename(p))
                except Exception:
                    # Skip problematic files but continue
                    continue
        buf.seek(0)
        return buf.getvalue()

    def create_zip_for_project(project_name, tests, include_reports=True, include_graphs=True):
        """Create a ZIP bytes containing selected tests, graph files and matching reports for a project.

        - Includes per-test HTML reports generated by `generate_html_report(test)` for each test in `tests`.
        """
        buf = io.BytesIO()
        safe_project = re.sub(r"[^A-Za-z0-9_-]", "_", project_name.strip())
        with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            # Add a summary JSON of tests
            try:
                zf.writestr(f"{safe_project}_test_summary.json", json.dumps(tests, indent=2))
            except Exception:
                pass

            # Add per-test HTML reports (always include these)
            for t in tests:
                try:
                    html_report = generate_html_report(t)
                    test_type_safe = (t.get('test_type') or 'test').lower().replace(' ', '_')
                    test_id = t.get('test_id', uuid.uuid4().hex[:8])
                    report_name = f"performance_report_{test_type_safe}_{test_id}.html"
                    zf.writestr(os.path.join('reports', report_name), html_report)
                except Exception:
                    # If report generation fails, skip but continue
                    continue

            # Add referenced graph files
            if include_graphs:
                for t in tests:
                    gf = t.get("graph_file")
                    if gf and os.path.exists(gf):
                        try:
                            zf.write(gf, os.path.join("graphs", os.path.basename(gf)))
                        except Exception:
                            continue

            # Add matching existing reports (simple filename contains project name match)
            if include_reports and os.path.exists("reports"):
                for fname in os.listdir("reports"):
                    try:
                        if project_name.lower() in fname.lower():
                            zf.write(os.path.join("reports", fname), os.path.join("reports", fname))
                    except Exception:
                        continue

        buf.seek(0)
        return buf.getvalue()

    def display_test_history():
        """Display test history with proper formatting and filtering."""
        try:
            with open('test_history/test_history.json', 'r') as f:
                test_history = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            test_history = []
            st.warning("No test history found. Run some tests first!")

        if not test_history:
            return

        # Get unique projects and test types
        projects = sorted({t['project_name'] for t in test_history})
        test_types = sorted({t['test_type'] for t in test_history})

        # Filters
        col1, col2 = st.columns(2)
        with col1:
            selected_project = st.selectbox(
                "Filter by Project",
                ["All Projects"] + projects,
                key="project_filter"
            )
            # Quick download when a specific project is selected
            if selected_project != "All Projects":
                colp1, colp2 = st.columns([3, 1])
                with colp1:
                    inc_reports_now = st.checkbox("Include project reports", value=True, key=f"inc_reports_now_{selected_project}")
                    inc_graphs_now = st.checkbox("Include project graphs", value=True, key=f"inc_graphs_now_{selected_project}")
                with colp2:
                    if st.button("Download project ZIP", key=f"download_proj_zip_now_{selected_project}"):
                        project_tests = [t for t in test_history if t.get('project_name') == selected_project]
                        if not project_tests:
                            st.warning("No tests found for this project.")
                        else:
                            try:
                                zip_bytes = create_zip_for_project(selected_project, project_tests, inc_reports_now, inc_graphs_now)
                                safe_name = re.sub(r'[^A-Za-z0-9_-]', '_', selected_project.strip()).lower()
                                zip_name = f"{safe_name}_tests_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
                                st.download_button("Click to download ZIP", data=zip_bytes, file_name=zip_name, mime="application/zip", key=f"dl_proj_zip_now_{selected_project}")
                            except Exception as e:
                                st.error(f"Failed to create project archive: {e}")
        with col2:
            selected_type = st.selectbox(
                "Filter by Test Type",
                ["All Test Types"] + test_types,
                key="type_filter"
            )

        # Apply filters
        filtered = test_history
        if selected_project != "All Projects":
            filtered = [t for t in filtered if t['project_name'] == selected_project]
        if selected_type != "All Test Types":
            filtered = [t for t in filtered if t['test_type'] == selected_type]

        # Sort by timestamp (newest first)
        filtered.sort(key=lambda x: x.get('timestamp', ''), reverse=True)

        # If a single project is selected, provide a quick project ZIP download
        if selected_project != "All Projects":
            with st.expander(f"Download ZIP for project: {selected_project}"):
                colA, colB = st.columns([3, 1])
                with colA:
                    include_reports_proj = st.checkbox("Include project reports", value=True, key=f"proj_inc_reports_{selected_project}")
                    include_graphs_proj = st.checkbox("Include project graphs", value=True, key=f"proj_inc_graphs_{selected_project}")
                with colB:
                    if st.button("Prepare project ZIP", key=f"proj_zip_btn_{selected_project}"):
                        project_tests = [t for t in test_history if t.get('project_name') == selected_project]
                        if not project_tests:
                            st.warning("No tests found for this project.")
                        else:
                            try:
                                zip_bytes = create_zip_for_project(selected_project, project_tests, include_reports_proj, include_graphs_proj)
                                safe_name = re.sub(r'[^A-Za-z0-9_-]', '_', selected_project.strip()).lower()
                                zip_name = f"{safe_name}_tests_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
                                st.success(f"Archive ready: {zip_name} ({len(zip_bytes) // 1024} KB)")
                                st.download_button("Download project ZIP", data=zip_bytes, file_name=zip_name, mime="application/zip", key=f"proj_zip_download_{selected_project}")
                            except Exception as e:
                                st.error(f"Failed to create project archive: {e}")

        # Display summary stats
        healthy = sum(1 for t in filtered if t.get('overall_status', '').startswith('✅'))
        warning = sum(1 for t in filtered if t.get('overall_status', '').startswith('⚠️'))
        critical = sum(1 for t in filtered if t.get('overall_status', '').startswith('❌'))

        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; margin: 1rem 0;">
            <div style="flex: 1; text-align: center; background: #d4edda; padding: 1rem; border-radius: 8px;">
                <h3>✅ Healthy</h3>
                <p style="font-size: 1.5rem; font-weight: bold;">{healthy}</p>
            </div>
            <div style="flex: 1; text-align: center; background: #fff3cd; padding: 1rem; border-radius: 8px; margin: 0 1rem;">
                <h3>⚠️ Warning</h3>
                <p style="font-size: 1.5rem; font-weight: bold;">{warning}</p>
            </div>
            <div style="flex: 1; text-align: center; background: #f8d7da; padding: 1rem; border-radius: 8px;">
                <h3>❌ Critical</h3>
                <p style="font-size: 1.5rem; font-weight: bold;">{critical}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Download / Archive options
        with st.expander("Download tests & reports"):
            col1, col2 = st.columns([3, 1])
            with col1:
                include_reports = st.checkbox("Include saved reports (reports/)", value=True)
                include_graphs = st.checkbox("Include graphs referenced in history", value=True)
            with col2:
                if st.button("Prepare ZIP of selected items"):
                    paths = ["test_history"]
                    if include_reports and os.path.exists("reports"):
                        paths.append("reports")
                    # Include graph files referenced by filtered tests
                    extras = []
                    for t in filtered:
                        gf = t.get("graph_file")
                        if gf and os.path.exists(gf):
                            extras.append(gf)
                    try:
                        zip_bytes = create_zip_from_paths(paths + extras)
                        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                        zip_name = f"eaii_test_archive_{ts}.zip"
                        st.success(f"Archive ready: {zip_name} ({len(zip_bytes) // 1024} KB)")
                        st.download_button("Download ZIP", data=zip_bytes, file_name=zip_name, mime="application/zip")
                    except Exception as e:
                        st.error(f"Failed to create archive: {e}")

        # Display each test
        for test in filtered:
            with st.expander(f"{test['test_id']} - {test['project_name']} - {test['test_type']}", expanded=False):
                cols = st.columns([1, 1, 1, 1])
                
                with cols[0]:
                    st.metric("Status", test.get('overall_status', 'Unknown'))
                    st.metric("Users", test.get('users', 'Unknown'))
                    
                with cols[1]:
                    st.metric("Duration", f"{test.get('duration', 0)/60:.1f} min" if isinstance(test.get('duration'), (int, float)) else 'Unknown')
                    st.metric("Requests", test['stats'].get('total_requests', 0))
                    
                with cols[2]:
                    st.metric("RPS", f"{test['stats'].get('rps', 0):.1f}")
                    st.metric("Avg Response", f"{test['stats'].get('avg_response_time', 0):.1f} ms")
                    
                with cols[3]:
                    st.metric("Fail Rate", f"{test['stats'].get('failures_rate', 0):.1f}%")
                    st.metric("95th %ile", f"{test['stats'].get('p95_response_time', 0):.1f} ms")

                # Generate and display report
                if st.button(f"📄 Generate Report for {test['test_id']}"):
                    html_report = generate_html_report(test)
                    st.download_button(
                        label="⬇️ Download HTML Report",
                        data=html_report,
                        file_name=f"report_{test['test_id']}.html",
                        mime="text/html"
                    )
                    # Save and render inline for quick preview
                    report_path = save_report_html(html_report, f"report_{test['test_id']}.html")
                    if report_path:
                        st.success(f"Report saved to: {report_path}")
                    try:
                        components.html(html_report, height=800, scrolling=True)
                    except Exception as e:
                        st.warning("Could not render report inline; file has been saved.")
                        st.write(report_path)

                # Delete button
                if st.button(f"🗑️ Delete {test['test_id']}"):
                    success, message = delete_test_record(test['test_id'], test_history)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)


    def generate_html_report(test_data):
        """Generate HTML report with concise next steps for critical issues."""
        # Normalize test_type
        test_type_mapping = {
            "load": "Load",
            "concurrency": "Concurrency",
            "stress": "Stress",
            "spike": "Spike",
            "volume": "Volume",
            "endurance": "Endurance"
        }

        def extract_test_metadata():
            """Extract and validate basic test information."""
            raw_test_type = test_data.get("test_type", "Load").lower()
            test_type = test_type_mapping.get(raw_test_type, "Load")
            
            # Safely get and convert users to integer
            users = test_data.get("users", None)
            try:
                users = int(users) if users is not None else None
            except (ValueError, TypeError):
                users = None
            
            # Safely get, convert duration to integer, then to minutes
            duration = test_data.get("duration", None)
            
            
            return {
                "test_type": test_type,
                "project_name": test_data.get("project_name", "Unnamed Project"),
                "test_id": test_data.get("test_id", str(uuid.uuid4())[:8]),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M %p"),
                "users": users,  # Use the converted value
                "duration": duration,
            }

        def extract_performance_metrics():
            """Extract and normalize performance metrics."""
            stats = test_data.get("stats", {})
            return {
                "total_requests": stats.get("total_requests", 0),
                "failures_rate": stats.get("failures_rate", 0),
                "rps": stats.get("rps", 0),
                "avg_response": stats.get("avg_response_time", 0),
                "p95_response": stats.get("p95_response_time", 0),
                "max_response": stats.get("max_response_time", 0)
            }


        # Extract metadata and metrics
        metadata = extract_test_metadata()
        test_type = metadata["test_type"]
        project_name = metadata["project_name"]
        test_id = metadata["test_id"]
        timestamp = metadata["timestamp"]
        users = metadata["users"]
        duration = metadata["duration"]

        metrics = extract_performance_metrics()
        total_requests = metrics["total_requests"]
        failures_rate = metrics["failures_rate"]
        rps = metrics["rps"]
        avg_response = metrics["avg_response"]
        p95_response = metrics["p95_response"]
        max_response = metrics["max_response"]

        # Test type descriptions
        test_type_descriptions = {
            "Load": """
                <p>Load testing evaluates system behavior under expected and peak load conditions.
                Measures throughput, response times, and resource utilization to identify performance
                bottlenecks at various load levels.</p>
                <p><strong>Key Focus:</strong> Maximum operating capacity, breaking point identification,
                and performance under sustained load.</p>
            """,
            "Concurrency": """
                <p>Concurrency testing examines how the system handles multiple users performing
                the same or different actions simultaneously. Identifies race conditions,
                deadlocks, and thread synchronization issues.</p>
                <p><strong>Key Focus:</strong> Multi-user scenarios, session management,
                and shared resource contention.</p>
            """,
            "Stress": """
                <p>Stress testing pushes the system beyond normal operational capacity to evaluate
                robustness and error handling under extreme conditions. Determines failure points
                and recovery mechanisms.</p>
                <p><strong>Key Focus:</strong> System stability at beyond-peak loads, graceful
                degradation, and recovery procedures.</p>
            """,
            "Spike": """
                <p>Spike testing evaluates system behavior when subjected to sudden and extreme
                increases in load. Measures how quickly the system can scale and whether it can
                handle rapid fluctuations.</p>
                <p><strong>Key Focus:</strong> Elasticity, auto-scaling capabilities, and
                response to sudden traffic bursts.</p>
            """,
            "Volume": """
                <p>Volume testing subjects the system to large amounts of data to verify stability
                and performance. Checks for memory leaks, storage limitations, and data processing
                efficiency.</p>
                <p><strong>Key Focus:</strong> Database performance, memory management, and
                large dataset handling.</p>
            """,
            "Endurance": """
                <p>Endurance testing evaluates system reliability over extended periods. Identifies
                performance degradation, memory leaks, or resource exhaustion.</p>
                <p><strong>Key Focus:</strong> Long-term stability, memory management, and
                sustained performance metrics.</p>
            """
        }

        test_description = test_type_descriptions.get(test_type, test_type_descriptions["Load"])

        # Define standards dictionary
        standards = {
            "load": {
                "display_name": "Load Test",
                "metrics": {
                    "Requests Per Second (RPS)": {"target": 500, "warning": 400, "critical": 300},
                    "95th Percentile Response Time (ms)": {"target": 800, "warning": 1000, "critical": 1500},
                    "Average Response Time (ms)": {"target": 300, "warning": 500, "critical": 800},
                    "Max Response Time (ms)": {"target": 4000, "warning": 6000, "critical": 10000},
                    "Failure Rate (%)": {"target": 0, "warning": 3, "critical": 5}
                }
            },
            "concurrency": {
                "display_name": "Concurrency Test",
                "metrics": {
                    "Requests Per Second (RPS)": {"target": 280, "warning": 200, "critical": 150},
                    "95th Percentile Response Time (ms)": {"target": 900, "warning": 1200, "critical": 1800},
                    "Average Response Time (ms)": {"target": 400, "warning": 600, "critical": 800},
                    "Max Response Time (ms)": {"target": 5000, "warning": 7000, "critical": 10000},
                    "Failure Rate (%)": {"target": 0, "warning": 5, "critical": 8}
                }
            },
            "spike": {
                "display_name": "Spike Test",
                "metrics": {
                    "Requests Per Second (RPS)": {"target": 350, "warning": 250, "critical": 150},
                    "95th Percentile Response Time (ms)": {"target": 1200, "warning": 1800, "critical": 2500},
                    "Average Response Time (ms)": {"target": 500, "warning": 800, "critical": 1200},
                    "Max Response Time (ms)": {"target": 6000, "warning": 9000, "critical": 15000},
                    "Failure Rate (%)": {"target": 0, "warning": 10, "critical": 15}
                }
            },
            "volume": {
                "display_name": "Volume Test",
                "metrics": {
                    "Requests Per Second (RPS)": {"target": 450, "warning": 400, "critical": 300},
                    "95th Percentile Response Time (ms)": {"target": 500, "warning": 800, "critical": 1200},
                    "Average Response Time (ms)": {"target": 200, "warning": 300, "critical": 500},
                    "Max Response Time (ms)": {"target": 3000, "warning": 5000, "critical": 8000},
                    "Failure Rate (%)": {"target": 0, "warning": 1, "critical": 3}
                }
            },
            "stress": {
                "display_name": "Stress Test",
                "metrics": {
                    "Requests Per Second (RPS)": {"target": 200, "warning": 150, "critical": 100},
                    "95th Percentile Response Time (ms)": {"target": 2000, "warning": 3000, "critical": 5000},
                    "Average Response Time (ms)": {"target": 800, "warning": 1200, "critical": 2000},
                    "Max Response Time (ms)": {"target": 10000, "warning": 15000, "critical": 30000},
                    "Failure Rate (%)": {"target": 0, "warning": 15, "critical": 20}
                }
            },
            "endurance": {
                "display_name": "Endurance Test",
                "metrics": {
                    "Requests Per Second (RPS)": {"target": 150, "warning": 100, "critical": 50},
                    "95th Percentile Response Time (ms)": {"target": 1000, "warning": 1500, "critical": 2500},
                    "Average Response Time (ms)": {"target": 400, "warning": 600, "critical": 1000},
                    "Max Response Time (ms)": {"target": 5000, "warning": 8000, "critical": 15000},
                    "Failure Rate (%)": {"target": 0, "warning": 5, "critical": 10}
                }
            }
        }

        # Status and rating logic
        def get_status_and_rating(metric, value, total_requests):
            """Determine status and rating for a metric based on standards."""
            current_standards = standards.get(test_type.lower(), standards["load"])["metrics"]
            if metric not in current_standards:
                return ("✅", "Healthy", 5, "⭐⭐⭐⭐⭐")

            good = current_standards[metric]["target"]
            warning = current_standards[metric]["warning"]

            if metric == "Requests Per Second (RPS)":
                if value >= good * 1.5:
                    return ("✅", "Healthy (Excellent)", 5, "⭐⭐⭐⭐⭐")
                elif value >= good:
                    return ("✅", "Healthy (Good)", 4, "⭐⭐⭐⭐")
                elif value >= warning:
                    return ("⚠️", "Warning", 2, "⭐⭐")
                else:
                    return ("❌", "Critical", 1, "⭐")
            else:
                if value <= good * 0.5:
                    return ("✅", "Healthy (Excellent)", 5, "⭐⭐⭐⭐⭐")
                elif value <= good:
                    return ("✅", "Healthy (Good)", 4, "⭐⭐⭐⭐")
                elif value <= warning:
                    return ("⚠️", "Warning", 2, "⭐⭐")
                else:
                    return ("❌", "Critical", 1, "⭐")

        # Get individual metric statuses and ratings - NOW UNPACKING 4 VALUES
        rps_status, rps_status_text, rps_rating, rps_stars = get_status_and_rating("Requests Per Second (RPS)", rps, total_requests)
        avg_status, avg_status_text, avg_response_rating, avg_stars = get_status_and_rating("Average Response Time (ms)", avg_response, total_requests)
        p95_status, p95_status_text, p95_rating, p95_stars = get_status_and_rating("95th Percentile Response Time (ms)", p95_response, total_requests)
        max_status, max_status_text, max_response_rating, max_stars = get_status_and_rating("Max Response Time (ms)", max_response, total_requests)
        fail_status, fail_status_text, fail_rating, fail_stars = get_status_and_rating("Failure Rate (%)", failures_rate, total_requests)

        # Calculate overall rating and status
        ratings = [rps_rating, avg_response_rating, p95_rating, max_response_rating, fail_rating]
        overall_rating = sum(ratings) / len(ratings)
        overall_label, overall_class, overall_stars = rating_float_to_label_and_class(overall_rating)
        overall_status = overall_label

        test_data["overall_status"] = overall_status
        test_data["overall_rating"] = round(overall_rating, 1)

        # Generate percentile distribution table
        rating_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for rating in ratings:
            rating_counts[rating] += 1
        total_metrics = len(ratings)
        rating_distribution = {r: (rating_counts[r] / total_metrics * 100) for r in range(1, 6)}
        distribution_rows = ""
        # Labels are derived from current test results mapping
        for rating in range(1, 6):
            label = get_rating_label(rating)
            distribution_rows += f"""
                <tr>
                    <td>{rating}</td>
                    <td>{label}</td>
                    <td>{rating_distribution[rating]:.1f}%</td>
                    <td>{rating_counts[rating]}</td>
                    <td>{sum(v for k, v in rating_counts.items() if k <= rating) / total_metrics * 100:.1f}%</td>
                </tr>
            """
        chart_data_array = "[" + ", ".join(str(round(rating_distribution[r], 1)) for r in range(1, 6)) + "]"
        distribution_table = f"""
            <div class="summary">
                <h2>Rating Distribution</h2>
                <div class="rating-graph">
                    <canvas id="ratingChart"></canvas>
                    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
                    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2.0.0/dist/chartjs-plugin-datalabels.min.js"></script>
                    <script>
                        var ratingCtx = document.getElementById('ratingChart').getContext('2d');
                        new Chart(ratingCtx, {{
                            type: 'bar',
                            data: {{
                                labels: [
                                    'Critical (1)', 
                                    'Warning (2)', 
                                    'Healthy (Acceptable) (3)', 
                                    'Healthy (Good) (4)', 
                                    'Healthy (Excellent) (5)'
                                ],
                                datasets: [{{
                                    label: 'Current Distribution (%)',
                                    data: {chart_data_array},
                                    backgroundColor: [
                                        'rgba(220, 53, 69, 0.3)', 
                                        'rgba(255, 193, 7, 0.3)', 
                                        'rgba(183, 235, 143, 0.3)', 
                                        'rgba(149, 222, 100, 0.3)', 
                                        'rgba(40, 167, 69, 0.3)'
                                    ],
                                    borderColor: [
                                        '#dc3545', 
                                        '#ffc107', 
                                        '#b7eb8f', 
                                        '#95de64', 
                                        '#28a745'
                                    ],
                                    borderWidth: 1
                                }}]
                            }},
                            options: {{
                                responsive: true,
                                maintainAspectRatio: false,
                                scales: {{ 
                                    y: {{ 
                                        beginAtZero: true, 
                                        max: 100, 
                                        title: {{ display: true, text: 'Percentage (%)' }} 
                                    }} 
                                }},
                                plugins: {{ 
                                    legend: {{ 
                                        display: true,
                                        position: 'top',
                                        labels: {{ usePointStyle: true }}
                                    }},
                                    tooltip: {{ mode: 'index', intersect: false }},
                                    datalabels: {{
                                        anchor: 'end',
                                        align: 'top',
                                        formatter: function(value) {{ return value + '%'; }},
                                        font: {{
                                            weight: 'bold'
                                        }},
                                        color: '#000'
                                    }}
                                }}
                            }},
                            plugins: [ChartDataLabels]
                        }});
                    </script>
                </div>
                <table>
                    <thead>
                        <tr>
                            <th>Rating</th>
                            <th>Status</th>
                            <th>Percentage (%)</th>
                            <th>Count</th>
                            <th>Cumulative %</th>
                        </tr>
                    </thead>
                    <tbody>
                        {distribution_rows}
                    </tbody>
                </table>
            </div>
        """

        # Generate recommendations and next steps
        recommendations = []
        next_steps = []

        if rps_status == "⚠️":
            recommendations.append(f"Warning: Throughput ({rps:.1f} RPS, Rating: {rps_rating}) is below optimal levels (≥{standards[test_type.lower()]['metrics']['Requests Per Second (RPS)']['target']}). Increase server resources or optimize code.")
            next_steps.extend([
                "<li><strong>Monitor CPU/memory:</strong> Use Prometheus to track resource usage and identify bottlenecks.</li>",
                "<li><strong>Optimize code:</strong> Refine application code to reduce request processing time.</li>",
                "<li><strong>Use load balancing:</strong> Implement load balancing to distribute requests evenly.</li>",
                "<li><strong>Scale infrastructure:</strong> Ensure servers can handle expected load.</li>"
            ])
        elif rps_status == "❌":
            recommendations.append(f"Critical: Throughput ({rps:.1f} RPS, Rating: {rps_rating}) is significantly below target (≥{standards[test_type.lower()]['metrics']['Requests Per Second (RPS)']['target']}). Check server capacity and network.")
            next_steps.extend([
                "<li><strong>Analyze logs:</strong> Use ELK Stack to pinpoint errors or performance issues.</li>",
                "<li><strong>Check network:</strong> Use Wireshark to monitor network bottlenecks.</li>",
                "<li><strong>Cache with Redis:</strong> Implement caching to reduce server load.</li>",
                "<li><strong>Scale servers:</strong> Add capacity to handle higher request volumes.</li>"
            ])
        else:
            recommendations.append(f"Throughput ({rps:.1f} RPS, Rating: {rps_rating}) meets or exceeds {test_type} standards.")

        if avg_status == "⚠️":
            recommendations.append(f"Warning: Average response time ({avg_response:.1f} ms, Rating: {avg_response_rating}) is high (≤{standards[test_type.lower()]['metrics']['Average Response Time (ms)']['target']}). Optimize app performance.")
            next_steps.extend([
                "<li><strong>Profile code:</strong> Use New Relic to identify slow code paths.</li>",
                "<li><strong>Optimize queries:</strong> Add database indexes to speed up queries.</li>",
                "<li><strong>Monitor response times:</strong> Track performance with APM tools.</li>",
                "<li><strong>Optimize backend:</strong> Improve backend processes for load handling.</li>"
            ])
        elif avg_status == "❌":
            recommendations.append(f"Critical: Average response time ({avg_response:.1f} ms, Rating: {avg_response_rating}) exceeds limits (≤{standards[test_type.lower()]['metrics']['Average Response Time (ms)']['target']}). Optimize queries and processing.")
            next_steps.extend([
                "<li><strong>Profile code:</strong> Analyze code paths with profiling tools.</li>",
                "<li><strong>Cache with Redis:</strong> Use caching to reduce database load.</li>",
                "<li><strong>Check CPU:</strong> Investigate CPU usage for bottlenecks.</li>",
                "<li><strong>Use async processing:</strong> Implement asynchronous task handling.</li>"
            ])
        else:
            recommendations.append(f"Average response time ({avg_response:.1f} ms, Rating: {avg_response_rating}) is excellent.")

        if p95_status == "⚠️":
            recommendations.append(f"Warning: 95th percentile response time ({p95_response:.1f} ms, Rating: {p95_rating}) shows delays (≤{standards[test_type.lower()]['metrics']['95th Percentile Response Time (ms)']['target']}). Optimize slow requests.")
            next_steps.extend([
                "<li><strong>Analyze with Datadog:</strong> Visualize response time distributions.</li>",
                "<li><strong>Optimize APIs:</strong> Improve high-latency API performance.</li>",
                "<li><strong>Cache data:</strong> Store frequent data in cache.</li>",
                "<li><strong>Handle peak load:</strong> Ensure system manages traffic spikes.</li>"
            ])
        elif p95_status == "❌":
            recommendations.append(f"Critical: 95th percentile response time ({p95_response:.1f} ms, Rating: {p95_rating}) indicates slow performance (≤{standards[test_type.lower()]['metrics']['95th Percentile Response Time (ms)']['target']}). Optimize endpoints.")
            next_steps.extend([
                "<li><strong>Trace endpoints:</strong> Use New Relic to identify slow APIs.</li>",
                "<li><strong>Optimize queries:</strong> Review MySQL slow query log.</li>",
                "<li><strong>Cache with Redis:</strong> Reduce database load with caching.</li>",
                "<li><strong>Map slow features:</strong> Use Hotjar to identify slow interactions.</li>"
            ])
        else:
            recommendations.append(f"95th percentile response time ({p95_response:.1f} ms, Rating: {p95_rating}) is excellent.")

        if max_status == "⚠️":
            recommendations.append(f"Warning: Max response time ({max_response:.1f} ms, Rating: {max_response_rating}) is high (≤{standards[test_type.lower()]['metrics']['Max Response Time (ms)']['target']}). Optimize endpoints.")
            next_steps.extend([
                "<li><strong>Set alerts:</strong> Use Prometheus for >{standards[test_type.lower()]['metrics']['Max Response Time (ms)']['target']} ms alerts.</li>",
                "<li><strong>Profile requests:</strong> Analyze slow requests for issues.</li>",
                "<li><strong>Optimize calls:</strong> Improve database/API call performance.</li>",
                "<li><strong>Ensure stability:</strong> Test system under heavy load.</li>"
            ])
        elif max_status == "❌":
            recommendations.append(f"Critical: Max response time ({max_response:.1f} ms, Rating: {max_response_rating}) indicates severe issues (≤{standards[test_type.lower()]['metrics']['Max Response Time (ms)']['target']}). Fix slow endpoints.")
            next_steps.extend([
                "<li><strong>Trace outliers:</strong> Use Dynatrace to pinpoint delays.</li>",
                "<li><strong>Set timeouts:</strong> Configure Nginx for 5s timeouts.</li>",
                "<li><strong>Scale with ELB:</strong> Use AWS ELB to distribute traffic.</li>",
                "<li><strong>Check features:</strong> Use Google Analytics for slow funnels.</li>"
            ])
        else:
            recommendations.append(f"Max response time ({max_response:.1f} ms, Rating: {max_response_rating}) is excellent.")

        if fail_status == "⚠️":
            recommendations.append(f"Warning: Failure rate ({failures_rate:.2f}%, Rating: {fail_rating}) is high (≤{standards[test_type.lower()]['metrics']['Failure Rate (%)']['target']}%). Investigate error sources.")
            next_steps.extend([
                "<li><strong>Review logs:</strong> Use ELK Stack to identify failure causes.</li>",
                "<li><strong>Fix errors:</strong> Address timeouts or resource issues.</li>",
                "<li><strong>Add retries:</strong> Implement retry mechanisms for failures.</li>",
                "<li><strong>Ensure stability:</strong> Test reliability under load.</li>"
            ])
        elif fail_status == "❌":
            recommendations.append(f"Critical: Failure rate ({failures_rate:.2f}%, Rating: {fail_rating}) indicates instability (≤{standards[test_type.lower()]['metrics']['Failure Rate (%)']['target']}%). Fix errors immediately.")
            next_steps.extend([
                "<li><strong>Review logs:</strong> Analyze logs with ELK Stack for errors.</li>",
                "<li><strong>Fix issues:</strong> Address timeouts or exhaustion.</li>",
                "<li><strong>Add retries:</strong> Implement retry logic for reliability.</li>",
                "<li><strong>Monitor failures:</strong> Set up alerts for failure rates.</li>"
            ])
        else:
            recommendations.append(f"Failure rate ({failures_rate:.2f}%, Rating: {fail_rating}) is excellent.")

        # Generate and save performance graph
        os.makedirs("test_history", exist_ok=True)
        graph_filename = f"test_history/{test_id}_performance_graph.png"
        try:
            actual_performance = [
                rps,
                p95_response,
                avg_response,
                max_response,
                failures_rate
            ]
            graph = generate_performance_graph(actual_performance, test_type.lower(), total_requests, failures_rate)
            graph.savefig(graph_filename, bbox_inches="tight", dpi=100)
            plt.close(graph)
        except Exception as e:
            print(f"Failed to generate graph for test {test_id}: {e}")
            graph_filename = ""

        # Save test history
        try:
            save_test_history(test_data, graph_filename)
        except Exception as e:
            print(f"Failed to save test history for test {test_id}: {e}")

        # Encode graph as base64
        graph_base64 = ""
        if graph_filename and os.path.exists(graph_filename):
            try:
                with open(graph_filename, "rb") as image_file:
                    graph_base64 = base64.b64encode(image_file.read()).decode("utf-8")
            except Exception as e:
                print(f"Failed to read graph file {graph_filename} for test {test_id}: {e}")

        graph_section = f"""
            <div class="graph-container">
                <h4>Performance Metrics Graph</h4>
                <img src="data:image/png;base64,{graph_base64}" alt="Performance Metrics Graph for Test {test_id}" style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 4px;">
            </div>
        """ if graph_base64 else """
            <div class="graph-container">
                <p>Failed to generate performance graph.</p>
            </div>
        """

        load_status = f"""
            <div class="load-test-status {overall_class.lower()}">
                {test_type} Test Status: {test_data["overall_status"]} (Average Rating: {test_data["overall_rating"]}/5)
            </div>
        """

        # CSS styles (unchanged for brevity; can be provided if needed)
        # CSS styles
        CSS_STYLES = """
        /* Base Styles */
        :root {
            --primary-color: #0a1a3b;
            --secondary-color: #2b5876;
            --accent-color: #f9a825;
            --success-color: #28a745;
            --warning-color: #ffc107;
            --danger-color: #dc3545;
            --light-bg: #f8f9fa;
            --card-bg: #ffffff;
            --text-dark: #333333;
            --text-light: #666666;
            --border-radius: 12px;
            --box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
            --transition: all 0.3s ease;
        }

        * {
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            margin: 0 auto;
            max-width: 1200px;
            background: linear-gradient(135deg, #f5f7fa 0%, #e4edf5 100%);
            color: var(--text-dark);
            line-height: 1.6;
            padding: 20px;
            min-height: 100vh;
        }

        /* Header - Enhanced Design */
        .header {
            position: relative;
            min-height: 200px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #0a1a3b 0%, #1a3a6a 100%);
            border: none;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
            margin: 20px 0;
            padding: 20px;
            color: white;
            text-align: center;
            isolation: isolate;
        }
        
        .header::before, .header::after { 
            content: ""; 
            position: absolute; 
            top: 0; 
            width: 20%; 
            height: 100%; 
            background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cpolygon points='30,0 51.96,15 51.96,45 30,60 8.04,45 8.04,15' fill='%23f9a825' opacity='1.0'/%3E%3C/svg%3E") repeat; 
            background-size: 60px 52px; 
            z-index: -1;
        }
        
        .header::before { 
            left: 0; 
        }
        
        .header::after { 
            right: 0; 
        }

        /* Logo Container */
        .logo-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 15px;
            margin-bottom: 20px;
            z-index: 1;
        }
        .logo:hover {
            transform: scale(1.05);
        }
        .header img {
            width: clamp(90px, 12vw, 120px);
            height: auto;
            filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.2));
            transition: var(--transition);
        }

        .header img:hover {
            transform: scale(1.05);
        }

        /* Institute Text - Enhanced */
        .institute-text {
            text-align: center;
            padding: 0 20px;
            max-width: 900px;
            z-index: 1;
        }

        .institute-text h1, 
        .institute-text h2 {
            color: white;
            margin: 8px 0;
            text-align: center;
            line-height: 1.4;
            font-weight: 600;
        }

        .institute-text h1 {
            font-size: clamp(1.6rem, 4.5vw, 2.5rem);
            background: linear-gradient(90deg, #ffffff, #f0f0f0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: -0.5px;
        }

        .institute-text h2 {
            font-size: clamp(1.2rem, 3vw, 1.8rem);
            color: rgba(255, 255, 255, 0.9);
            margin-top: 10px;
        }

        .institute-text .amh {
            font-family: "Noto Sans Ethiopic", "Segoe UI", sans-serif;
            font-size: clamp(16px, 2.2vw, 20px);
            font-weight: 500;
            line-height: 1.5;
            color: #ffffff;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }

        .institute-text .eng {
            font-size: clamp(14px, 2vw, 18px);
            color: var(--accent-color);
            font-weight: 700;
            margin-top: 5px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        /* Test Description Banner */
        .test-description {
            background: linear-gradient(135deg, #2b5876 0%, #4e4376 100%);
            color: white;
            padding: 25px 30px;
            border-radius: var(--border-radius);
            margin: 30px 0;
            box-shadow: var(--box-shadow);
            border-left: 5px solid var(--accent-color);
        }

        .test-description h2 {
            color: white;
            font-size: 1.8rem;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .test-description h2::before {
            content: "📊";
            font-size: 1.5rem;
        }

        .test-description p {
            font-size: 1.1rem;
            opacity: 0.95;
            line-height: 1.7;
        }

        /* Report Info Cards - Enhanced */
        .report-info {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
            margin: 40px 0;
        }

        .info-box {
            background: var(--card-bg);
            padding: 25px;
            border-radius: var(--border-radius);
            box-shadow: var(--box-shadow);
            transition: var(--transition);
            border: 1px solid rgba(0, 0, 0, 0.05);
            position: relative;
            overflow: hidden;
        }

        .info-box::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: linear-gradient(to bottom, var(--primary-color), var(--accent-color));
        }

        .info-box:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
        }

        .info-box h3 {
            color: var(--primary-color);
            font-size: 1.3rem;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid var(--light-bg);
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .info-box h3::before {
            content: "📋";
            font-size: 1.2rem;
        }

        .info-box p {
            margin: 12px 0;
            color: var(--text-light);
            font-size: 1rem;
        }

        .info-box strong {
            color: var(--text-dark);
            min-width: 150px;
            display: inline-block;
        }

        /* Load Status Banner */
        .load-test-status {
            padding: 20px;
            border-radius: var(--border-radius);
            font-weight: 700;
            text-align: center;
            margin: 30px 0;
            font-size: 1.2rem;
            box-shadow: var(--box-shadow);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
            border: none;
        }

        .load-test-status::before {
            font-size: 1.5rem;
        }

        .load-test-status.healthy {
            background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
            color: #155724;
            border-left: 5px solid var(--success-color);
        }

        .load-test-status.warning {
            background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
            color: #856404;
            border-left: 5px solid var(--warning-color);
        }

        .load-test-status.critical {
            background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
            color: #721c24;
            border-left: 5px solid var(--danger-color);
        }

        /* Metrics Grid - Enhanced */
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 25px;
            margin: 30px 0;
        }

        .metric-card {
            background: var(--card-bg);
            padding: 25px;
            border-radius: var(--border-radius);
            box-shadow: var(--box-shadow);
            text-align: center;
            border-top: 4px solid var(--primary-color);
            transition: var(--transition);
            position: relative;
            overflow: hidden;
        }

        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        }

        .metric-card h3 {
            margin: 0 0 15px 0;
            font-size: 1.1rem;
            color: var(--text-light);
            font-weight: 600;
        }

        .metric-value {
            font-size: 2.2rem;
            color: var(--primary-color);
            margin: 15px 0;
            font-weight: 800;
            font-family: 'SF Mono', Monaco, 'Cascadia Code', monospace;
        }

        /* Status Badges - Enhanced */
        .status {
            padding: 8px 20px;
            border-radius: 25px;
            font-weight: 700;
            font-size: 0.9rem;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }

        .status::before {
            font-size: 1rem;
        }

        .status.healthy {
            background: linear-gradient(135deg, #28a745, #20c997);
            color: white;
        }

        .status.warning {
            background: linear-gradient(135deg, #ffc107, #fd7e14);
            color: black;
        }

        .status.critical {
            background: linear-gradient(135deg, #dc3545, #c82333);
            color: white;
        }

        /* Tables - Enhanced */
        table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            margin: 30px 0;
            background: var(--card-bg);
            box-shadow: var(--box-shadow);
            border-radius: var(--border-radius);
            overflow: hidden;
        }

        th, td {
            padding: 18px 20px;
            text-align: left;
            border-bottom: 1px solid rgba(0, 0, 0, 0.05);
        }

        th {
            background: linear-gradient(135deg, var(--primary-color), #1a3a6a);
            color: white;
            font-weight: 600;
            font-size: 1rem;
            position: sticky;
            top: 0;
        }

        tr {
            transition: var(--transition);
        }

        tr:hover {
            background-color: rgba(10, 26, 59, 0.03);
            transform: translateX(5px);
        }

        /* Graph Container - Enhanced */
        .graph-container {
            margin: 30px 0;
            padding: 25px;
            background: var(--card-bg);
            border-radius: var(--border-radius);
            box-shadow: var(--box-shadow);
            border: 1px solid rgba(0, 0, 0, 0.05);
        }

        .graph-container h4 {
            margin: 0 0 20px 0;
            color: var(--secondary-color);
            font-size: 1.4rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .graph-container h4::before {
            content: "📈";
        }

        .graph-container img {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            border: 1px solid rgba(0, 0, 0, 0.1);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }

        /* Recommendations & Next Steps - Enhanced */
        .recommendations, .next-steps {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 30px;
            border-radius: var(--border-radius);
            margin: 30px 0;
            border-left: 5px solid var(--accent-color);
            box-shadow: var(--box-shadow);
        }

        .recommendations h3, .next-steps h3 {
            color: var(--primary-color);
            font-size: 1.5rem;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .recommendations h3::before {
            content: "💡";
        }

        .next-steps li {
            margin-bottom: 15px;
            padding: 15px 15px 15px 40px; /* Increased left padding */
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            border-left: 4px solid var(--primary-color);
            transition: var(--transition);
            position: relative;
        }

        /* Remove counter and use list-style instead */
        .next-steps ol {
            list-style: decimal;
            padding-left: 20px;
            margin: 0;
        }

        .next-steps li {
            list-style-position: outside;
            padding-left: 10px;
            margin-left: 0;
        }

        .next-steps li:hover {
            transform: translateX(5px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }

        /* Footer - Enhanced */
        .footer {
            background: linear-gradient(135deg, var(--primary-color) 0%, #1a3a6a 100%);
            color: white;
            text-align: center;
            margin-top: 60px;
            font-size: 0.95rem;
            padding: 40px 30px;
            border-radius: var(--border-radius);
            box-shadow: var(--box-shadow);
            position: relative;
            overflow: hidden;
        }

        .footer::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--accent-color), #ffcc00, var(--accent-color));
        }

        .footer-content {
            max-width: 900px;
            margin: 0 auto;
            position: relative;
            z-index: 1;
        }

        .footer p {
            margin: 10px 0;
            line-height: 1.6;
            opacity: 0.9;
        }

        .footer strong {
            color: var(--accent-color);
        }

        .footer a {
            color: var(--accent-color);
            text-decoration: none;
            font-weight: 600;
            transition: var(--transition);
        }

        .footer a:hover {
            color: #ffcc00;
            text-decoration: underline;
        }

        /* Responsive Design */
        @media (max-width: 1200px) {
            body {
                padding: 15px;
            }
        }

        @media (max-width: 992px) {
            .report-info {
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            }
            
            .metrics-grid {
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            }
        }

        @media (max-width: 768px) {
            .header {
                min-height: 160px;
                padding: 20px 15px;
                margin: 10px auto 30px;
            }
            
            .institute-text h1 {
                font-size: 1.4rem;
            }
            
            .institute-text h2 {
                font-size: 1.1rem;
            }
            
            .test-description {
                padding: 20px;
            }
            
            .info-box {
                padding: 20px;
            }
            
            .metric-value {
                font-size: 1.8rem;
            }
            
            th, td {
                padding: 12px 15px;
                font-size: 0.9rem;
            }
            
            .graph-container,
            .recommendations,
            .next-steps {
                padding: 20px;
            }
        }

        @media (max-width: 576px) {
            .header {
                min-height: 140px;
                padding: 15px 10px;
                border-radius: 10px;
            }
            
            .header img {
                width: 80px;
            }
            
            .institute-text .amh {
                font-size: 14px;
            }
            
            .institute-text .eng {
                font-size: 12px;
            }
            
            .test-description h2 {
                font-size: 1.3rem;
            }
            
            .report-info {
                grid-template-columns: 1fr;
                gap: 15px;
            }
            
            .metrics-grid {
                grid-template-columns: 1fr;
                gap: 15px;
            }
            
            .footer {
                padding: 30px 20px;
                font-size: 0.85rem;
            }
        }

        /* Print Styles */
        @media print {
            body {
                background: white !important;
                padding: 0 !important;
            }
            
            .header, .footer {
                page-break-inside: avoid;
                box-shadow: none !important;
            }
            
            .project-section {
                page-break-after: always;
                box-shadow: none !important;
                border: 1px solid #ddd;
            }
            
            .graph-container {
                max-width: 100%;
                break-inside: avoid;
            }
            
            .info-box, .metric-card {
                box-shadow: none !important;
                border: 1px solid #ddd !important;
            }
        }
        """
        # HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Performance Test Report</title>
            <style>{CSS_STYLES}</style>
            <link href="https://fonts.googleapis.com/earlyaccess/notosansethiopic.css" rel="stylesheet">
        </head>
        <body>
            <div class="header">
                {(
                    f"<img src='data:image/png;base64,{base64.b64encode(open('image/logo.png', 'rb').read()).decode()}' class='logo-img' style='width: 100px; height: 100px; margin-bottom: 15px; object-fit: contain;'>"
                    if os.path.exists('image/logo.png')
                    else "<img src='data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgdmlld0JveD0iMCAwIDEwMCAxMDAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0iTTUwIDVhNDAgNDAgMCAwIDAgMCA4MC40YzIuNi0xLjIgNS4xLTIuOCA3LjUtNC43IDYuMS00LjkgMTEuNS0xMS40IDE1LjQtMTguOCA0LjUtOC45IDcuMi0xOS4xIDcuMi0yOS45IDAtMjIuMTAtMTcuOS00MC00MC00MFoiIGZpbGw9IiNmOWE4MjUiLz48L3N2Zz4=' class='logo-img' style='width: 100px; height: 100px; margin-bottom: 15px; object-fit: contain;'>"
                )}
                <div class="institute-text">
                    <h1 class="amh">የኢትዮጵያ አርቲፊሻል ኢንተለጀንስ ኢንስቲትዩት</h1>
                    <h1 class="eng">ETHIOPIAN ARTIFICIAL INTELLIGENCE INSTITUTE</h1>
                    <h2>EAII Performance Testing Tool</h2>
                </div>
            </div>
            <div class="project-section">
                <div class="test-description">
                    <h2>Test Type: {test_type} Test</h2>
                    {test_description}
                </div>
            <div class="report-info">
                <div class="info-box">
                    <h3>Test Information</h3>
                    <p><strong>Project Title:</strong> {project_name}</p>
                    <p><strong>Test Type:</strong> {test_type} Test</p>
                    <p><strong>Test ID:</strong> {test_id}</p>
                </div>
                <div class="info-box">
                    <h3>Test Summary</h3>
                    <p><strong>Date:</strong> {timestamp}</p>
                    <p><strong>Number of Users:</strong> {users}</p>
                    <p><strong>Test Duration:</strong> {duration} minutes</p>
                </div>
                <div class="info-box">
                    <h3>System Information</h3>
                    <p><strong>Tool Version:</strong> Locust 3.35</p>
                    <p><strong>Generated By:</strong> EAII🚀PTT</p>
                    <p><strong>Average Rating:</strong> {test_data['overall_rating']}/5</p>
                </div>
            </div>
                {load_status}
                {graph_section}
                {distribution_table}
                <div class="summary">
                    <h2>Detailed Metrics Analysis</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Metric</th>
                                <th>Description</th>
                                <th>Actual Performance</th>
                                <th>Expected Standard</th>
                                <th>Insight</th>
                                <th>Status</th>
                                <th>Rating</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Requests Per Second</td>
                                <td>Number of requests the system handles per second</td>
                                <td>{rps:.1f} RPS</td>
                                <td>≥{standards[test_type.lower()]['metrics']['Requests Per Second (RPS)']['target']} RPS</td>
                                <td class="insight-{rps_status_text.lower()}">
                                    {f"Excellent throughput, well above standards" if rps_status == '✅' and rps >= standards[test_type.lower()]['metrics']['Requests Per Second (RPS)']['target'] * 1.5 else
                                    f"Good throughput, meets standards" if rps_status == '✅' and rps >= standards[test_type.lower()]['metrics']['Requests Per Second (RPS)']['target'] else
                                    f"Moderate throughput, approaching warning levels" if rps_status == '⚠️' else
                                    f"Low throughput, does not meet standards" if rps_status == '❌' else "Unknown performance"}
                                </td>
                                <td><span class="status {rps_status_text.lower()}">{rps_status} {rps_status_text}</span></td>
                                <td>{rps_rating}</td>
                            </tr>
                            <tr>
                                <td>Average Response Time</td>
                                <td>Average time taken to respond to all requests</td>
                                <td>{avg_response:.1f} ms</td>
                                <td>≤{standards[test_type.lower()]['metrics']['Average Response Time (ms)']['target']} ms</td>
                                <td class="insight-{avg_status_text.lower()}">
                                    {f"Excellent response time, well below threshold" if avg_status == '✅' and avg_response <= standards[test_type.lower()]['metrics']['Average Response Time (ms)']['target'] * 0.5 else
                                    f"Good response time, within acceptable range" if avg_status == '✅' and avg_response <= standards[test_type.lower()]['metrics']['Average Response Time (ms)']['target'] else
                                    f"Moderate response time, nearing warning levels" if avg_status == '⚠️' else
                                    f"Poor response time, exceeds acceptable range" if avg_status == '❌' else "Unknown performance"}
                                </td>
                                <td><span class="status {avg_status_text.lower()}">{avg_status} {avg_status_text}</span></td>
                                <td>{avg_response_rating}</td>
                            </tr>
                            <tr>
                                <td>95th Percentile</td>
                                <td>Time taken to complete 95% of requests</td>
                                <td>{p95_response:.1f} ms</td>
                                <td>≤{standards[test_type.lower()]['metrics']['95th Percentile Response Time (ms)']['target']} ms</td>
                                <td class="insight-{p95_status_text.lower()}">
                                    {f"Excellent performance, minimal delays for users" if p95_status == '✅' and p95_response <= standards[test_type.lower()]['metrics']['95th Percentile Response Time (ms)']['target'] * 0.5 else
                                    f"Good performance, few users experience delays" if p95_status == '✅' and p95_response <= standards[test_type.lower()]['metrics']['95th Percentile Response Time (ms)']['target'] else
                                    f"Moderate performance, some users may notice delays" if p95_status == '⚠️' else
                                    f"Poor performance, many users experience delays" if p95_status == '❌' else "Unknown performance"}
                                </td>
                                <td><span class="status {p95_status_text.lower()}">{p95_status} {p95_status_text}</span></td>
                                <td>{p95_rating}</td>
                            </tr>
                            <tr>
                                <td>Max Response Time</td>
                                <td>Longest time taken to process a single request</td>
                                <td>{max_response:.1f} ms</td>
                                <td>≤{standards[test_type.lower()]['metrics']['Max Response Time (ms)']['target']} ms</td>
                                <td class="insight-{max_status_text.lower()}">
                                    {f"Excellent stability, minimal peak delays" if max_status == '✅' and max_response <= standards[test_type.lower()]['metrics']['Max Response Time (ms)']['target'] * 0.5 else
                                    f"Good stability, minor peak delays" if max_status == '✅' and max_response <= standards[test_type.lower()]['metrics']['Max Response Time (ms)']['target'] else
                                    f"Moderate stability, noticeable peak delays" if max_status == '⚠️' else
                                    f"Poor stability, severe peak delays detected" if max_status == '❌' else "Unknown performance"}
                                </td>
                                <td><span class="status {max_status_text.lower()}">{max_status} {max_status_text}</span></td>
                                <td>{max_response_rating}</td>
                            </tr>
                            <tr>
                                <td>Failure Rate</td>
                                <td>Percentage of failed requests</td>
                                <td>{failures_rate:.2f}%</td>
                                <td>≤{standards[test_type.lower()]['metrics']['Failure Rate (%)']['target']}%</td>
                                <td class="{'insight-positive' if fail_status_text == 'Healthy' else 'insight-warning' if fail_status_text == 'Warning' else 'insight-critical'}">
                                    {f"Excellent reliability, no significant failures" if fail_status_text == 'Healthy' and failures_rate <= standards[test_type.lower()]['metrics']['Failure Rate (%)']['target'] * 0.5 else
                                    f"Good reliability, acceptable failure rate" if fail_status_text == 'Healthy' and failures_rate <= standards[test_type.lower()]['metrics']['Failure Rate (%)']['target'] else
                                    f"Moderate reliability, some concerns detected" if fail_status_text == 'Warning' else
                                    f"Poor reliability, critical failure issues" if fail_status_text == 'Critical' else "Unknown performance"}
                                </td>
                                <td><span class="status {fail_status_text.lower()}">{fail_status} {fail_status_text}</span></td>
                                <td>{fail_rating}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div class="summary">
                    <h2>Analysis Result</h2>
                    <p class="{overall_class.lower()}"><strong>{test_type} Test Status: {test_data['overall_status']} (Average Rating: {test_data['overall_rating']}/5)</strong></p>
                    <h3>Recommendations</h3>
                    <ul>{''.join(f'<li>{rec}</li>' for rec in recommendations)}</ul>
                    <h3>Next Steps</h3>
                    <div class="next-steps">
                        <ul>{''.join(next_steps)}</ul>
                    </div>
                </div>
            </div>
            <footer class="footer">
            <div class="footer-content">
                <p><strong>Ethiopian Artificial Intelligence Institute</strong></p>
                <p>Quality Assurance & Performance Testing Department</p>
                <hr style="border: 0; border-top: 1px solid rgba(255,255,255,0.2); margin: 10px 0;">
                <p>Report generated by <strong>EAII🚀PTT</strong> • {timestamp}</p>
                <p>Tool Version: <strong>1.0.0</strong></p>
                <p style="font-size: 0.85rem; opacity: 0.9;">For inquiries: qa@eaii.gov.et</p>
                <p style="margin-top: 10px; font-size: 0.85rem;">
                    Convert PDF using this URL: 
                    <a href="https://www.freeconvert.com/html-to-pdf" target="_blank">
                        https://www.freeconvert.com/html-to-pdf
                    </a>
                </p>
            </div>
        </footer>
        </body>
        </html>
        """

        return html_content

    def delete_test_record(test_id, test_history):
        """Delete a test record and its associated graph file."""
        test_to_delete = next((test for test in test_history if test['test_id'] == test_id), None)
        if not test_to_delete:
            return False, "Test not found."
        
        graph_deleted = False
        if 'graph_file' in test_to_delete and test_to_delete['graph_file']:
            try:
                if os.path.exists(test_to_delete['graph_file']):
                    os.remove(test_to_delete['graph_file'])
                    graph_deleted = True
            except Exception as e:
                return False, f"Error deleting graph file: {str(e)}"
        
        updated_history = [test for test in test_history if test['test_id'] != test_id]
        try:
            with open('test_history/test_history.json', 'w') as f:
                json.dump(updated_history, f, indent=2)
            success_msg = f"Deleted test {test_id}!"
            if graph_deleted:
                success_msg += " (Graph file also deleted)"
            return True, success_msg
        except Exception as e:
            return False, f"Failed to save updated history: {str(e)}"

    def delete_project_records(project_name, test_history):
        """Delete all test records for a project and their associated graph files."""
        project_tests = [test for test in test_history if test['project_name'] == project_name]
        deleted_graphs = 0
        
        for test in project_tests:
            if 'graph_file' in test and test['graph_file']:
                try:
                    if os.path.exists(test['graph_file']):
                        os.remove(test['graph_file'])
                        deleted_graphs += 1
                except Exception as e:
                    st.error(f"Error deleting graph file for test {test['test_id']}: {str(e)}")
        
        updated_history = [test for test in test_history if test['project_name'] != project_name]
        try:
            with open('test_history/test_history.json', 'w') as f:
                json.dump(updated_history, f, indent=2)
            success_msg = f"Deleted project '{project_name}' and all {len(project_tests)} tests!"
            if deleted_graphs > 0:
                success_msg += f" (Deleted {deleted_graphs} associated graph files)"
            return True, success_msg
        except Exception as e:
            return False, f"Failed to save updated history: {str(e)}"

    # ========== SAVED HISTORY BRANCH ==========
    if source == "📁 Saved History":
        # Call the existing main function to display saved history
        # But we need to define main first (it's defined above)
        def main():
            """Main function to display test history and manage records."""
            # Initialize session state
            if 'show_record_management' not in st.session_state:
                st.session_state.show_record_management = False

            # Load test history
            try:
                with open('test_history/test_history.json', 'r') as f:
                    test_history = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                test_history = []
                st.warning("No test history found. Run some tests first!")

            # Initialize project_names and test_types
            project_names = sorted(list(set(test['project_name'] for test in test_history))) if test_history else []
            test_types = sorted(list(set(test['test_type'] for test in test_history))) if test_history else []

            if test_history:
                # Filters
                col1, col2, col3 = st.columns([2, 2, 1])
                with col1:
                    selected_project = st.selectbox(
                        "Filter by Project",
                        ["All Projects"] + project_names,
                        key="project_filter"
                    )
                with col2:
                    selected_type = st.selectbox(
                        "Filter by Test Type",
                        ["All Test Types"] + test_types,
                        key="type_filter"
                    )
                with col3:
                    st.write("")  # Spacer
                    st.write("")  # Spacer
                    if st.button("⚙️ Manage Records", help="Record management options", key="manage_toggle"):
                        st.session_state.show_record_management = not st.session_state.show_record_management
                        st.rerun()

                # Filter test history
                filtered_history = test_history
                if selected_project != "All Projects":
                    filtered_history = [test for test in filtered_history if test['project_name'] == selected_project]
                if selected_type != "All Test Types":
                    filtered_history = [test for test in filtered_history if test['test_type'] == selected_type]
                filtered_history.sort(key=lambda x: x['timestamp'], reverse=True)

                # Record Management
                if st.session_state.show_record_management:
                    with st.expander("🔧 Record Management", expanded=True):
                        st.subheader("Delete Options")
                        tab1, tab2 = st.tabs(["Delete Single Record", "Delete Entire Project"])
                        
                        with tab1:
                            if not filtered_history:
                                st.warning("No tests match current filters")
                            else:
                                test_ids = [test['test_id'] for test in filtered_history]
                                selected_test_id = st.selectbox(
                                    "Select test to delete",
                                    test_ids,
                                    key="delete_single_select"
                                )
                                
                                if selected_test_id:
                                    test_to_delete = next(test for test in filtered_history if test['test_id'] == selected_test_id)
                                    
                                    # Display test details for confirmation
                                    cols = st.columns([3,1])
                                    with cols[0]:
                                        st.warning(f"""
                                        **You are about to permanently delete:**
                                        - Test ID: `{selected_test_id}`
                                        - Project: `{test_to_delete['project_name']}`
                                        - Type: `{test_to_delete['test_type']}`
                                        - Date: `{test_to_delete['timestamp']}`
                                        """)
                                    
                                    with cols[1]:
                                        if test_to_delete.get('graph_file'):
                                            st.error("⚠️ Associated graph file will also be deleted")
                                    
                                    # Double confirmation for deletion
                                    confirm = st.checkbox(f"I confirm deletion of test {selected_test_id}", key=f"confirm_del_{selected_test_id}")
                                    
                                    if st.button("🗑️ Delete Selected Test", 
                                            key="delete_single_btn",
                                            disabled=not confirm,
                                            help="Requires confirmation checkbox"):
                                        
                                        with st.spinner(f"Deleting {selected_test_id}..."):
                                            success, message = delete_test_record(selected_test_id, test_history)
                                            
                                        if success:
                                            st.success(message)
                                            st.balloons()
                                            time.sleep(1)  # Let user see success message
                                            st.rerun()
                                        else:
                                            st.error(message)

                        with tab2:
                            if not project_names:
                                st.warning("No projects available to delete")
                            else:
                                selected_delete_project = st.selectbox(
                                    "Select project to delete",
                                    project_names,
                                    key="delete_project_select"
                                )
                                
                                # Calculate project statistics
                                project_tests = [t for t in test_history if t['project_name'] == selected_delete_project]
                                project_stats = {
                                    'total_tests': len(project_tests),
                                    'graphs': sum(1 for t in project_tests if t.get('graph_file'))
                                }
                                
                                st.error(f"""
                                ### 🚨 Critical Action
                                This will permanently delete:
                                - All {project_stats['total_tests']} tests for **{selected_delete_project}**
                                - {project_stats['graphs']} associated graph files
                                """)
                                
                                # Multi-step confirmation
                                col1, col2 = st.columns(2)
                                with col1:
                                    confirm_name = st.text_input(
                                        "Type the project name to confirm",
                                        key=f"confirm_project_{selected_delete_project}"
                                    )
                                with col2:
                                    st.write("")  # Spacer
                                    confirm_check = st.checkbox(
                                        "I understand this cannot be undone",
                                        key=f"confirm_check_{selected_delete_project}"
                                    )
                                
                                if st.button("🔥 Delete Entire Project", 
                                            key="delete_project_btn",
                                            type="primary",
                                            disabled=(confirm_name != selected_delete_project or not confirm_check),
                                            help="Requires exact project name and confirmation"):
                                    
                                    with st.spinner(f"Deleting {selected_delete_project} project..."):
                                        success, message = delete_project_records(selected_delete_project, test_history)
                                    
                                    if success:
                                        st.success(message)
                                        time.sleep(1.5)  # Let user see success message
                                        st.rerun()
                                    else:
                                        st.error(message)

                # Summary Statistics
                st.subheader("📈 Summary Statistics")
                def get_status_category(status):
                    """Normalize status values for counting"""
                    status = str(status).lower()
                    if 'healthy' in status:
                        return 'healthy'
                    elif 'warning' in status:
                        return 'warning'
                    elif 'critical' in status:
                        return 'critical'
                    return 'unknown'

                # Calculate summary statistics
                total_tests = len(filtered_history)
                if total_tests > 0:
                    status_counts = {
                        'healthy': 0,
                        'warning': 0,
                        'critical': 0
                    }
                    
                    for test in filtered_history:
                        status = get_status_category(test.get('overall_status', ''))
                        if status in status_counts:
                            status_counts[status] += 1
                    
                    success_rate = (status_counts['healthy'] / total_tests) * 100
                    warning_rate = (status_counts['warning'] / total_tests) * 100
                    critical_rate = (status_counts['critical'] / total_tests) * 100
                else:
                    success_rate = warning_rate = critical_rate = 0.0
                
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Total Tests", total_tests)
                col2.metric("Success Rate", f"{success_rate:.1f}%", delta="Healthy")
                col3.metric("Warning Rate", f"{warning_rate:.1f}%", delta="Warning", delta_color="off")
                col4.metric("Critical Rate", f"{critical_rate:.1f}%", delta="Critical", delta_color="inverse")

                # Test Records Table
                st.subheader("🧾 Test Records")
                st.markdown("""
                    <div class="table-container">
                        <div class="table-header">
                            <div class="table-cell table-cell-id">Test ID</div>
                            <div class="table-cell table-cell-project">Project</div>
                            <div class="table-cell table-cell-type">Test Type</div>
                            <div class="table-cell table-cell-date">Date</div>
                            <div class="table-cell table-cell-status">Status</div>
                            <div class="table-cell table-cell-requests">Requests</div>
                            <div class="table-cell table-cell-failure">Failure Rate</div>
                            <div class="table-cell table-cell-rps">RPS</div>
                            <div class="table-cell table-cell-response">Avg Response</div>
                            <div class="table-cell table-cell-actions">Actions</div>
                        </div>
                        <div class="table-body">
                """, unsafe_allow_html=True)

                for index, test in enumerate(filtered_history):
                    st.markdown(f"""
                        <div class="table-row">
                            <div class="table-cell table-cell-id">{test['test_id']}</div>
                            <div class="table-cell table-cell-project">{test['project_name']}</div>
                            <div class="table-cell table-cell-type">{test['test_type']}</div>
                            <div class="table-cell table-cell-date">
                                {datetime.fromisoformat(test['timestamp']).strftime("%Y-%m-%d %H:%M") if test.get('timestamp') else "Invalid"}
                            </div>
                            <div class="table-cell table-cell-status">{test['overall_status']}</div>
                            <div class="table-cell table-cell-requests">{test['stats'].get('total_requests', 0)}</div>
                            <div class="table-cell table-cell-failure">{test['stats'].get('failures_rate', 0):.1f}%</div>
                            <div class="table-cell table-cell-rps">{test['stats'].get('rps', 0):.1f}</div>
                            <div class="table-cell table-cell-response">{test['stats'].get('avg_response_time', 0):.1f} ms</div>
                            <div class="table-cell table-cell-actions">
                    """, unsafe_allow_html=True)

                    # Generate the HTML report using the current test data
                    html_report = generate_html_report(test)

                    # Create a specific filename for the download
                    test_type_safe = test['test_type'].lower().replace(' ', '_')
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    file_name = f"performance_report_{test_type_safe}_{test['test_id']}_{timestamp}.html"

                    # Download button for the HTML report
                    st.download_button(
                        label="📥",
                        data=html_report,
                        file_name=file_name,
                        mime="text/html",
                        key=f"download_{test['test_id']}_{index}",
                        help=f"Download report for test {test['test_id']}"
                    )

                    

                    if st.button("🗑️", key=f"delete_{test['test_id']}_{index}", help=f"Delete test {test['test_id']}"):
                        success, message = delete_test_record(test['test_id'], test_history)
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                    
                    st.markdown("</div>", unsafe_allow_html=True)

                # Direct project download for currently filtered project (appears below the table)
                if selected_project != "All Projects":
                    st.markdown("<hr/>", unsafe_allow_html=True)
                    with st.container():
                        st.markdown(f"**Download ZIP for filtered project:** **{selected_project}**")
                        colz1, colz2 = st.columns([3, 1])
                        with colz1:
                            inc_reports_below = st.checkbox("Include project reports", value=True, key=f"inc_reports_below_{selected_project}")
                            inc_graphs_below = st.checkbox("Include project graphs", value=True, key=f"inc_graphs_below_{selected_project}")
                        with colz2:
                            safe_key = re.sub(r"[^A-Za-z0-9_]", "_", selected_project.strip()).lower()
                            if st.button("📦 Download filtered project ZIP", key=f"download_filtered_zip_{safe_key}"):
                                project_tests = [t for t in filtered_history if t['project_name'] == selected_project]
                                if not project_tests:
                                    st.warning("No tests found for this project / filter.")
                                else:
                                    try:
                                        zip_bytes = create_zip_for_project(selected_project, project_tests, inc_reports_below, inc_graphs_below)
                                        safe_name = re.sub(r'[^A-Za-z0-9_-]', '_', selected_project.strip()).lower()
                                        zip_name = f"{safe_name}_filtered_tests_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
                                        st.download_button("Click to download ZIP", data=zip_bytes, file_name=zip_name, mime="application/zip", key=f"dl_filtered_zip_{safe_key}")
                                    except Exception as e:
                                        st.error(f"Failed to create archive: {e}")

                            # CSV / JSON export for the currently filtered records (visible table)
                            if st.button("⬇️ Prepare filtered records CSV", key=f"prep_csv_{safe_key}"):
                                if not filtered_history:
                                    st.warning("No records match current filters to export.")
                                else:
                                    try:
                                        df = pd.DataFrame([{
                                            "Test ID": t.get('test_id'),
                                            "Project": t.get('project_name'),
                                            "Test Type": t.get('test_type'),
                                            "Date": (datetime.fromisoformat(t.get('timestamp')).strftime("%Y-%m-%d %H:%M") if t.get('timestamp') else "Invalid"),
                                            "Status": t.get('overall_status'),
                                            "Requests": t.get('stats', {}).get('total_requests', 0),
                                            "Failure Rate": f"{t.get('stats', {}).get('failures_rate', 0):.2f}",
                                            "RPS": f"{t.get('stats', {}).get('rps', 0):.1f}",
                                            "Avg Response": f"{t.get('stats', {}).get('avg_response_time', 0):.1f}"
                                        } for t in filtered_history])
                                        csv_bytes = df.to_csv(index=False).encode('utf-8')
                                        csv_name = f"filtered_tests_{safe_key}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                                        st.success(f"CSV ready: {csv_name} ({len(csv_bytes)//1024} KB)")
                                        st.download_button("⬇️ Download filtered CSV", data=csv_bytes, file_name=csv_name, mime="text/csv", key=f"dl_csv_{safe_key}")

                                        # Optionally save to reports folder
                                        if st.checkbox("Also save CSV to reports/", key=f"save_csv_reports_{safe_key}"):
                                            os.makedirs("reports", exist_ok=True)
                                            csv_path = os.path.join("reports", csv_name)
                                            try:
                                                with open(csv_path, "wb") as fh:
                                                    fh.write(csv_bytes)
                                                st.success(f"CSV saved to: {csv_path}")
                                            except Exception as e:
                                                st.error(f"Failed to save CSV: {e}")
                                    except Exception as e:
                                        st.error(f"Failed to export CSV: {e}")

                            if st.button("⬇️ Download filtered records (JSON)", key=f"dl_json_{safe_key}"):
                                try:
                                    json_bytes = json.dumps(filtered_history, indent=2).encode('utf-8')
                                    json_name = f"filtered_tests_{safe_key}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                                    st.download_button("⬇️ Download JSON", data=json_bytes, file_name=json_name, mime="application/json", key=f"dl_jsonbtn_{safe_key}")
                                except Exception as e:
                                    st.error(f"Failed to prepare JSON: {e}")

                # Project-Specific Downloads
                with st.expander("📁 Project-Specific Downloads", expanded=False):
                    if not project_names:
                        st.warning("No projects available to download")
                    else:
                        selected_download_project = st.selectbox(
                            "Select Project to Download",
                            ["All Projects"] + project_names,
                            key="project_download_select"
                        )
                        
                        if selected_download_project != "All Projects":
                            project_history = [test for test in test_history if test['project_name'] == selected_download_project]
                            
                            if st.button(f"📦 Generate {selected_download_project} Project Report"):
                                report_html = generate_history_report(project_history, project_name=selected_download_project)
                                if report_html:
                                    project_file_name = f"performance_report_{selected_download_project.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.html"
                                    st.download_button(
                                        label=f"⬇️ Download {selected_download_project} Report",
                                        data=report_html,
                                        file_name=project_file_name,
                                        mime="text/html"  
                                    )

                            if st.button(f"📊 Export {selected_download_project} to CSV"):
                                project_df = pd.DataFrame([{
                                    "Test ID": test['test_id'],
                                    "Project": test['project_name'],
                                    "Number of Users":test['users'],
                                    "Test Duration": f"{float(test['duration']) / 60:.1f}" if test.get('duration') and test['duration'].replace('.', '', 1).isdigit() else "Invalid",
                                    "Test Type": test['test_type'],
                                    "Date": datetime.fromisoformat(test['timestamp']).strftime("%Y-%m-%d %H:%M") if test.get('timestamp') else "Invalid",
                                    "Status": test['overall_status'],
                                    "Requests": test['stats'].get('total_requests', 0),
                                    "Failures": test['stats'].get('failures_rate', 0),
                                    "RPS": f"{test['stats'].get('rps', 0):.1f}",
                                    "Avg Response": f"{test['stats'].get('avg_response_time', 0):.1f} ms"
                                } for test in project_history])
                                
                                csv = project_df.to_csv(index=False)
                                csv_filename = f"performance_history_{selected_download_project.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv"
                                st.download_button(
                                    label=f"⬇️ Download {selected_download_project} CSV",
                                    data=csv,
                                    file_name=csv_filename,
                                    mime="text/csv"
                                )
                                # Also save CSV to reports folder for easy access
                                os.makedirs("reports", exist_ok=True)
                                csv_path = os.path.join("reports", csv_filename)
                                try:
                                    with open(csv_path, "w", encoding="utf-8") as fh:
                                        fh.write(csv)
                                    st.success(f"CSV saved to: {csv_path}")
                                except Exception as e:
                                    st.error(f"Failed to save CSV: {e}")
            else:
                st.warning("No test records to display.")

        # Call main to display saved history
        main()

    
   
    # ========== UPLOAD JSON BRANCH ==========
    else:
        st.subheader("📂 Upload Test JSON")
        uploaded_file = st.file_uploader(
            "Choose a JSON file containing test records",
            type=["json"],
            key="uploaded_json"
        )

        if uploaded_file is not None:
            try:
                file_content = uploaded_file.read().decode("utf-8").strip()
                if not file_content:
                    st.error("❌ The uploaded file is empty. Please provide a valid JSON file.")
                else:
                    imported_tests = json.loads(file_content)
                    if not isinstance(imported_tests, list):
                        st.error("❌ JSON must be a list of test objects. Please check the file format.")
                    else:
                        st.success(f"✅ Loaded {len(imported_tests)} test(s) from JSON.")

                        # Filter out non-dict items
                        valid_tests = [t for t in imported_tests if isinstance(t, dict)]
                        if len(valid_tests) != len(imported_tests):
                            st.warning(f"Ignored {len(imported_tests)-len(valid_tests)} invalid entries.")

                        # If no valid tests, stop
                        if not valid_tests:
                            st.warning("No valid test objects found.")
                        else:
                            # --- Summary stats ---
                            def get_status_category(status):
                                status = str(status).lower()
                                if 'healthy' in status:
                                    return 'healthy'
                                elif 'warning' in status:
                                    return 'warning'
                                elif 'critical' in status:
                                    return 'critical'
                                return 'unknown'

                            status_counts = {'healthy': 0, 'warning': 0, 'critical': 0}
                            for t in valid_tests:
                                cat = get_status_category(t.get('overall_status', ''))
                                if cat in status_counts:
                                    status_counts[cat] += 1

                            healthy = status_counts['healthy']
                            warning = status_counts['warning']
                            critical = status_counts['critical']

                            st.markdown(f"""
                            <div style="display: flex; justify-content: space-between; margin: 1rem 0;">
                                <div style="flex:1; text-align:center; background:#d4edda; padding:1rem; border-radius:8px;">
                                    <h3 style="color:black;">✅ Healthy</h3>
                                    <p style="font-size:1.5rem; font-weight:bold; color:black;">{healthy}</p>
                                </div>
                                <div style="flex:1; text-align:center; background:#fff3cd; padding:1rem; border-radius:8px; margin:0 1rem;">
                                    <h3 style="color:black;">⚠️ Warning</h3>
                                    <p style="font-size:1.5rem; font-weight:bold; color:black;">{warning}</p>
                                </div>
                                <div style="flex:1; text-align:center; background:#f8d7da; padding:1rem; border-radius:8px;">
                                    <h3 style="color:black;">❌ Critical</h3>
                                    <p style="font-size:1.5rem; font-weight:bold; color:black;">{critical}</p>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                            # --- Extract filter options ---
                            project_names = sorted(set(t.get('project_name', 'Unknown') for t in valid_tests))
                            test_types = sorted(set(t.get('test_type', 'Unknown') for t in valid_tests))

                            col1, col2 = st.columns(2)
                            with col1:
                                selected_project = st.selectbox(
                                    "Filter by Project",
                                    ["All Projects"] + project_names,
                                    key="upload_project_filter"
                                )
                            with col2:
                                selected_type = st.selectbox(
                                    "Filter by Test Type",
                                    ["All Test Types"] + test_types,
                                    key="upload_type_filter"
                                )

                            # Apply filters
                            filtered_tests = valid_tests
                            if selected_project != "All Projects":
                                filtered_tests = [t for t in filtered_tests if t.get('project_name') == selected_project]
                            if selected_type != "All Test Types":
                                filtered_tests = [t for t in filtered_tests if t.get('test_type') == selected_type]

                            # Sort by timestamp (newest first)
                            filtered_tests.sort(key=lambda x: x.get('timestamp', ''), reverse=True)

                            st.write(f"**Showing {len(filtered_tests)} test(s)**")

                            # --- Display each test in an expander ---
                            for idx, test in enumerate(filtered_tests):
                                test_id = test.get('test_id', f"test_{idx}")
                                project = test.get('project_name', 'N/A')
                                test_type = test.get('test_type', 'N/A')
                                timestamp = test.get('timestamp', 'N/A')

                                with st.expander(f"{test_id} - {project} - {test_type} - {timestamp}"):
                                    cols = st.columns([1, 1, 1, 1])

                                    stats = test.get('stats', {})
                                    total_requests = stats.get('total_requests', 0)
                                    failures_rate = stats.get('failures_rate', 0)
                                    rps = stats.get('rps', 0)
                                    avg_response = stats.get('avg_response_time', 0)
                                    p95_response = stats.get('p95_response_time', 0)
                                    max_response = stats.get('max_response_time', 0)

                                    with cols[0]:
                                        st.metric("Status", test.get('overall_status', 'Unknown'))
                                        st.metric("Users", test.get('users', 'Unknown'))

                                    with cols[1]:
                                        st.metric("Duration", f"{test.get('duration', 0)} s")
                                        st.metric("Requests", total_requests)

                                    with cols[2]:
                                        st.metric("RPS", f"{rps:.1f}")
                                        st.metric("Avg Response", f"{avg_response:.1f} ms")

                                    with cols[3]:
                                        st.metric("Fail Rate", f"{failures_rate:.1f}%")
                                        st.metric("95th %ile", f"{p95_response:.1f} ms")

                                    # --- Buttons for individual test ---
                                    col_btn1, col_btn2 = st.columns(2)
                                    with col_btn1:
                                        if st.button(f"📄 Generate Report", key=f"gen_{test_id}_{idx}"):
                                            html_report = generate_html_report(test)
                                            st.download_button(
                                                label="⬇️ Download HTML Report",
                                                data=html_report,
                                                file_name=f"report_{test_id}.html",
                                                mime="text/html",
                                                key=f"dl_{test_id}_{idx}"
                                            )

                                    with col_btn2:
                                        if st.button(f"📊 Generate Graph", key=f"graph_{test_id}_{idx}"):
                                            actual_performance = [
                                                rps,
                                                p95_response,
                                                avg_response,
                                                max_response,
                                                failures_rate
                                            ]
                                            fig = generate_performance_graph(
                                                actual_performance,
                                                test_type.lower(),
                                                total_requests,
                                                failures_rate
                                            )
                                            buf = io.BytesIO()
                                            fig.savefig(buf, format='png', bbox_inches="tight", dpi=100)
                                            buf.seek(0)
                                            st.download_button(
                                                label="⬇️ Download Graph",
                                                data=buf,
                                                file_name=f"graph_{test_id}.png",
                                                mime="image/png",
                                                key=f"dl_graph_{test_id}_{idx}"
                                            )
                                            plt.close(fig)

                            # --- Direct project download for currently filtered project ---
                            if selected_project != "All Projects":
                                st.markdown("<hr/>", unsafe_allow_html=True)
                                with st.container():
                                    st.markdown(f"**Download ZIP for filtered project:** **{selected_project}**")
                                    colz1, colz2 = st.columns([3, 1])
                                    with colz1:
                                        inc_reports_below = st.checkbox("Include project reports", value=True, key=f"inc_reports_below_{selected_project}")
                                        inc_graphs_below = st.checkbox("Include project graphs", value=True, key=f"inc_graphs_below_{selected_project}")
                                    with colz2:
                                        safe_key = re.sub(r"[^A-Za-z0-9_]", "_", selected_project.strip()).lower()
                                        if st.button("📦 Download filtered project ZIP", key=f"download_filtered_zip_{safe_key}"):
                                            project_tests = [t for t in filtered_tests if t.get('project_name') == selected_project]
                                            if not project_tests:
                                                st.warning("No tests found for this project / filter.")
                                            else:
                                                try:
                                                    zip_bytes = create_zip_for_project(selected_project, project_tests, inc_reports_below, inc_graphs_below)
                                                    safe_name = re.sub(r'[^A-Za-z0-9_-]', '_', selected_project.strip()).lower()
                                                    zip_name = f"{safe_name}_filtered_tests_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
                                                    st.download_button("Click to download ZIP", data=zip_bytes, file_name=zip_name, mime="application/zip", key=f"dl_filtered_zip_{safe_key}")
                                                except Exception as e:
                                                    st.error(f"Failed to create archive: {e}")

                                        # CSV / JSON export for the currently filtered records
                                        if st.button("⬇️ Prepare filtered records CSV", key=f"prep_csv_{safe_key}"):
                                            if not filtered_tests:
                                                st.warning("No records match current filters to export.")
                                            else:
                                                try:
                                                    df = pd.DataFrame([{
                                                        "Test ID": t.get('test_id'),
                                                        "Project": t.get('project_name'),
                                                        "Test Type": t.get('test_type'),
                                                        "Date": (datetime.fromisoformat(t.get('timestamp')).strftime("%Y-%m-%d %H:%M") if t.get('timestamp') else "Invalid"),
                                                        "Status": t.get('overall_status'),
                                                        "Requests": t.get('stats', {}).get('total_requests', 0),
                                                        "Failure Rate": f"{t.get('stats', {}).get('failures_rate', 0):.2f}",
                                                        "RPS": f"{t.get('stats', {}).get('rps', 0):.1f}",
                                                        "Avg Response": f"{t.get('stats', {}).get('avg_response_time', 0):.1f}"
                                                    } for t in filtered_tests])
                                                    csv_bytes = df.to_csv(index=False).encode('utf-8')
                                                    csv_name = f"filtered_tests_{safe_key}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                                                    st.success(f"CSV ready: {csv_name} ({len(csv_bytes)//1024} KB)")
                                                    st.download_button("⬇️ Download filtered CSV", data=csv_bytes, file_name=csv_name, mime="text/csv", key=f"dl_csv_{safe_key}")

                                                    # Optionally save to reports folder
                                                    if st.checkbox("Also save CSV to reports/", key=f"save_csv_reports_{safe_key}"):
                                                        os.makedirs("reports", exist_ok=True)
                                                        csv_path = os.path.join("reports", csv_name)
                                                        try:
                                                            with open(csv_path, "wb") as fh:
                                                                fh.write(csv_bytes)
                                                            st.success(f"CSV saved to: {csv_path}")
                                                        except Exception as e:
                                                            st.error(f"Failed to save CSV: {e}")
                                                except Exception as e:
                                                    st.error(f"Failed to export CSV: {e}")

                                        if st.button("⬇️ Download filtered records (JSON)", key=f"dl_json_{safe_key}"):
                                            try:
                                                json_bytes = json.dumps(filtered_tests, indent=2).encode('utf-8')
                                                json_name = f"filtered_tests_{safe_key}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                                                st.download_button("⬇️ Download JSON", data=json_bytes, file_name=json_name, mime="application/json", key=f"dl_jsonbtn_{safe_key}")
                                            except Exception as e:
                                                st.error(f"Failed to prepare JSON: {e}")

                            # --- Project-Specific Downloads (all tests for a selected project) ---
                            with st.expander("📁 Project-Specific Downloads", expanded=False):
                                if not project_names:
                                    st.warning("No projects available to download")
                                else:
                                    selected_download_project = st.selectbox(
                                        "Select Project to Download",
                                        ["All Projects"] + project_names,
                                        key="project_download_select"
                                    )

                                    if selected_download_project != "All Projects":
                                        project_history = [test for test in valid_tests if test.get('project_name') == selected_download_project]

                                        if st.button(f"📦 Generate {selected_download_project} Project Report"):
                                            report_html = generate_history_report(project_history, project_name=selected_download_project)
                                            if report_html:
                                                project_file_name = f"performance_report_{selected_download_project.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.html"
                                                st.download_button(
                                                    label=f"⬇️ Download {selected_download_project} Report",
                                                    data=report_html,
                                                    file_name=project_file_name,
                                                    mime="text/html"
                                                )

                                        if st.button(f"📊 Export {selected_download_project} to CSV"):
                                            project_df = pd.DataFrame([{
                                                "Test ID": test.get('test_id'),
                                                "Project": test.get('project_name'),
                                                "Number of Users": test.get('users'),
                                                "Test Duration": f"{float(test.get('duration', 0)) / 60:.1f}" if test.get('duration') and str(test.get('duration')).replace('.', '', 1).isdigit() else "Invalid",
                                                "Test Type": test.get('test_type'),
                                                "Date": datetime.fromisoformat(test.get('timestamp')).strftime("%Y-%m-%d %H:%M") if test.get('timestamp') else "Invalid",
                                                "Status": test.get('overall_status'),
                                                "Requests": test.get('stats', {}).get('total_requests', 0),
                                                "Failures": test.get('stats', {}).get('failures_rate', 0),
                                                "RPS": f"{test.get('stats', {}).get('rps', 0):.1f}",
                                                "Avg Response": f"{test.get('stats', {}).get('avg_response_time', 0):.1f} ms"
                                            } for test in project_history])

                                            csv = project_df.to_csv(index=False)
                                            csv_filename = f"performance_history_{selected_download_project.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv"
                                            st.download_button(
                                                label=f"⬇️ Download {selected_download_project} CSV",
                                                data=csv,
                                                file_name=csv_filename,
                                                mime="text/csv"
                                            )
                                            # Also save CSV to reports folder
                                            os.makedirs("reports", exist_ok=True)
                                            csv_path = os.path.join("reports", csv_filename)
                                            try:
                                                with open(csv_path, "w", encoding="utf-8") as fh:
                                                    fh.write(csv)
                                                st.success(f"CSV saved to: {csv_path}")
                                            except Exception as e:
                                                st.error(f"Failed to save CSV: {e}")

            except json.JSONDecodeError as e:
                st.error(f"❌ Invalid JSON format: {e}")
            except Exception as e:
                st.error(f"❌ Unexpected error: {e}")
                st.exception(e)   # show full traceback for debugging
        else:
            st.info("👆 Upload a JSON file to view imported tests.")


    # --- Sample report generation (if __name__ == "__main__") ---
    if __name__ == "__main__":
        # Sample test history for report generation
        test_history = [
            {
                "project_name": "Immigration and Citizen Service (ICS)",
                "test_type": "Endurance Test",
                "test_id": "TEST_20250715_122107_54352e63",
                "timestamp": "2025-07-15T12:21:07",
                "overall_status": "Critical",
                "stats": {
                    "rps": 1251.0,
                    "avg_response_time": 859.0,
                    "p95_response_time": 4000.0,
                    "max_response_time": 24182.0,
                    "total_requests": 100000,
                    "failures_rate": 0
                },
                "users": 100,
                "duration": 600,
                "start_time": "2025-07-15T12:21:07",
                "end_time": "2025-07-15T12:31:07"
            },
            {
                "project_name": "Immigration and Citizen Service (ICS)",
                "test_type": "Concurrency Test",
                "test_id": "TEST_20250714_172429_dd53d2d1",
                "timestamp": "2025-07-14T17:24:29",
                "overall_status": "Critical",
                "stats": {
                    "rps": 1233.0,
                    "avg_response_time": 676.0,
                    "p95_response_time": 4100.0,
                    "max_response_time": 25163.0,
                    "total_requests": 100000,
                    "failures_rate": 0
                },
                "users": 150,
                "duration": 900,
                "start_time": "2025-07-14T17:24:29",
                "end_time": "2025-07-14T17:39:29"
            },
            {
                "project_name": "Immigration and Citizen Service (ICS)",
                "test_type": "Volume Test",
                "test_id": "TEST_20250714_165746_6b171344",
                "timestamp": "2025-07-14T16:57:46",
                "overall_status": "Healthy",
                "stats": {
                    "rps": 1121.0,
                    "avg_response_time": 123.0,
                    "p95_response_time": 190.0,
                    "max_response_time": 1569.0,
                    "total_requests": 100000,
                    "failures_rate": 0
                },
                "users": 50,
                "duration": 300,
                "start_time": "2025-07-14T16:57:46",
                "end_time": "2025-07-14T17:02:46"
            },
            {
                "project_name": "Immigration and Citizen Service (ICS)",
                "test_type": "Spike Test",
                "test_id": "TEST_20250714_165657_34e7b9ba",
                "timestamp": "2025-07-14T16:56:57",
                "overall_status": "Critical",
                "stats": {
                    "rps": 1283.0,
                    "avg_response_time": 913.0,
                    "p95_response_time": 4200.0,
                    "max_response_time": 21817.0,
                    "total_requests": 100000,
                    "failures_rate": 0
                },
                "users": 200,
                "duration": 1200,
                "start_time": "2025-07-14T16:56:57",
                "end_time": "2025-07-14T17:16:57"
            },
            {
                "project_name": "Immigration and Citizen Service (ICS)",
                "test_type": "Stress Test",
                "test_id": "TEST_20250714_155025_e7dda1e7",
                "timestamp": "2025-07-14T15:50:25",
                "overall_status": "Critical",
                "stats": {
                    "rps": 1245.0,
                    "avg_response_time": 1535.0,
                    "p95_response_time": 8200.0,
                    "max_response_time": 27464.0,
                    "total_requests": 100000,
                    "failures_rate": 0
                },
                "users": 250,
                "duration": 1800,
                "start_time": "2025-07-14T15:50:25",
                "end_time": "2025-07-14T16:20:25"
            },
            {
                "project_name": "Immigration and Citizen Service (ICS)",
                "test_type": "Load Test",
                "test_id": "TEST_20250714_145700_982b5d64",
                "timestamp": "2025-07-14T14:57:00",
                "overall_status": "Critical",
                "stats": {
                    "rps": 883.0,
                    "avg_response_time": 1535.0,
                    "p95_response_time": 2700.0,
                    "max_response_time": 140322.0,
                    "total_requests": 100000,
                    "failures_rate": 0
                },
                "users": 75,
                "duration": 600,
                "start_time": "2025-07-14T14:57:00",
                "end_time": "2025-07-14T15:07:00"
            }
        ]
        
        # Define project_names for the download section
        project_names = sorted(list(set(test['project_name'] for test in test_history))) if test_history else []
        
        # Generate history report
        report_html = generate_history_report(test_history, project_name="Immigration and Citizen Service (ICS)")
        with open("performance_report_ICS_corrected.html", "w", encoding="utf-8") as f:
            f.write(report_html)
        print("Corrected report generated: performance_report_ICS_corrected.html")

# --- HELP PAGE ---
elif st.session_state.current_page == "Help":
    with st.expander("❓ Help & Documentation", expanded=False):
        st.title("Help & Documentation")
        
        tabs = st.tabs(["Getting Started", "Test Configuration", "Understanding Results", "Installation Guide"])
        
        with tabs[0]:
            st.markdown("""
            ### Welcome to EAII Performance Testing Toolkit
            This guide will help you get started with performance testing your applications.
            
            **Key Features:**
            - 🚀 Multiple test types (Load, Stress, Spike, Endurance, Volume, Concurrency)
            - 📊 Real-time metrics visualization
            - 📈 Historical test result tracking
            
            **Basic Workflow:**
            1. Configure your test parameters on the Home page
            2. Start the performance test
            3. Monitor real-time results
            4. Analyze detailed reports and visualizations
            5. Save or export test results
            """)
            st.image("https://via.placeholder.com/800x400?text=Workflow+Diagram", use_container_width=True)
        
        with tabs[1]:
            st.markdown("""
            ### Test Configuration Parameters
            
            **Project Name**
            - Name to identify your test project
            - Used for organizing test history
            
            **Target URL**
            - The full URL of your application to test (e.g., https://yourapp.com)
            - Must include the protocol (http:// or https://)
            
            **Test Types**
            - **Load Test**: Simulates expected user load
            - **Stress Test**: Pushes beyond normal operational capacity
            - **Spike Test**: Sudden bursts of user activity
            - **Endurance Test**: Long-running test to identify memory leaks
            - **Volume Test**: Tests with large amounts of data
            - **Concurrency Test**: High number of simultaneous users
            
            **User Configuration**
            - **Total Users**: Maximum number of virtual users
            - **Spawn Rate**: How quickly users are added per second
            - **Duration**: Total test duration in seconds
            """)
            st.image("https://via.placeholder.com/800x400?text=Configuration+Options", use_container_width=True)
        
        with tabs[2]:
            st.markdown("""
            ### Understanding Test Results
            
            **Test History**
            - All tests are automatically saved with a unique ID
            - Filter by project, test type, or date range
            - View detailed metrics for each test
            - Generate professional HTML reports
            
            **Key Performance Metrics**
            - Total number of requests made during the test
            - Requests per second (throughput)
            - Average response time (milliseconds)
            - Failure rate (percentage of failed requests)
            - 95th percentile response time
            - Maximum response time
            
            **HTML Reports**
            - Professional formatted reports
            - Color-coded status indicators
            - Detailed recommendations
            - Exportable for sharing
            """)
            st.image("https://via.placeholder.com/800x400?text=Metrics+Explanation", use_container_width=True)

        
        with tabs[3]:
            st.markdown("""
            ## Installation Guide

            ### Prerequisites
            - Windows 10/11
            - Administrator privileges
            - 4GB+ RAM recommended

            ### Step 1: Install Python
            ```bash
            # Check current Python version
            python --version
            
            # If not Python 3.13.3, download and install from:
            ```
            [Download Python for Windows](https://www.python.org/downloads/windows)  

            During installation, ensure you check:  
            ☑ Add Python to PATH  
            ☑ Install pip  

            ### Step 2: Install VS Code (Recommended IDE)
            [Download VS Code](https://code.visualstudio.com/Download)  

            ### Step 3: Set Up Virtual Environment
            ```bash
            # Navigate to your project directory
            cd path\\to\\eaii_ptt
            
            # Remove old virtual environment (if exists)
            rmdir /s /q venv
            
            # Create new virtual environment
            python -m venv venv
            ```

            ### Step 4: Activate and Install Dependencies
            ```bash
            # Activate virtual environment
            .\\venv\\Scripts\\activate
            
            # Install required packages
            pip install -r requirements.txt
            
            # Verify installation
            pip list
            ```

            ### Step 5: Run the Application
            ```bash
            # Start the EAII_PTT tool
            streamlit run app.py
            ```
            Access the tool in your browser:  
            [http://localhost:8501](http://localhost:8501)  

            ### Troubleshooting Tips
            - If you get permission errors, run Command Prompt as Administrator
            - For Python path issues, check system environment variables
            - If packages fail to install, try: `pip install --upgrade pip`
            - For virtual environment issues: `python -m ensurepip --upgrade`
            """)



# --- ABOUT SYSTEM PAGE ---
elif st.session_state.current_page == "About System":
    st.title("ℹ️ About the System")

    with st.expander("📖 System Overview & Version Info", expanded=False):
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("""
            ### EAII Performance Testing Tool
            **Version:** 1.1.0  
            **Release Date:** June 2025  
            **Developed By:** Quality Assurance Department  
            **Institution:** Ethiopia Artificial Intelligence Institute  

            A comprehensive performance testing solution designed to:
            - Validate system reliability under various load conditions
            - Identify performance bottlenecks
            - Ensure optimal user experience
            - Support CI/CD pipelines with automated testing
            """)
        with col2:
            st.image("https://via.placeholder.com/500x300?text=System+Architecture", use_container_width=True)

    with st.expander("🛠️ Core Technologies & Features", expanded=False):
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("""
            ### Core Technologies
            - Python 3.10+
            - Streamlit 1.28+
            - Locust 2.15+
            - Pandas 2.0+
            - Matplotlib 3.7+
            """)
        with col2:
            st.markdown("""
            ### Key Features
            - 🧪 Multi-type testing framework
            - 📊 Real-time visualization
            - 📁 Historical test repository
            - 📈 Advanced analytics
            - 📤 Exportable reports
            """)

    with st.expander("💻 System Requirements & License", expanded=False):
        st.markdown("""
        ### System Requirements
        | Component | Minimum | Recommended |
        |----------|---------|-------------|
        | CPU | 4 cores | 8 cores |
        | RAM | 4 GB | 8 GB |
        | Storage | 10 GB | 50 GB |
        | OS | Linux/Windows 10+ | Ubuntu 22.04 LTS |
        | Python | 3.10+ | 3.11+ |

        ### License
        This software is proprietary technology of the Ethiopia Artificial Intelligence Institute.
        Unauthorized use, duplication, or distribution is strictly prohibited.

        **For technical support contact:** qa-support@eaii.gov.et
        """)
