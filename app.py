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
import sys
import signal

# ============================================================================
# RENDER DEPLOYMENT CONFIGURATION (FIXED)
# ============================================================================

# Detect Render environment
IS_RENDER = os.getenv('RENDER', 'false').lower() == 'true'
RENDER_EXTERNAL_URL = os.getenv('RENDER_EXTERNAL_URL', '')

# Configuration with Render support
LOCUST_PORT = int(os.getenv("LOCUST_PORT", "8089").strip(' \\'))
STREAMLIT_PORT = int(os.getenv("PORT", 8501))

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Render-specific configuration
if IS_RENDER:
    PUBLIC_HOST = RENDER_EXTERNAL_URL.replace('https://', '').replace('http://', '') if RENDER_EXTERNAL_URL else os.getenv("PUBLIC_HOST", "localhost")
    SHOW_LOCUST_DASHBOARD = False
    LOCUST_BIND_HOST = "0.0.0.0"  # Bind to all interfaces
    LOCUST_INTERNAL_URL = f"http://localhost:{LOCUST_PORT}"
    # Create persistent directories
    os.makedirs('/tmp/test_history', exist_ok=True)
    os.makedirs('/tmp/reports', exist_ok=True)
    os.makedirs('/tmp/reports/graphs', exist_ok=True)
else:
    PUBLIC_HOST = os.getenv("PUBLIC_HOST", "localhost")
    SHOW_LOCUST_DASHBOARD = True
    LOCUST_BIND_HOST = "0.0.0.0"
    LOCUST_INTERNAL_URL = f"http://localhost:{LOCUST_PORT}"
    os.makedirs('test_history', exist_ok=True)
    os.makedirs('reports', exist_ok=True)
    os.makedirs('reports/graphs', exist_ok=True)

logger.info(f"🚀 Starting EAII PTT in {'Render' if IS_RENDER else 'Local'} mode")
logger.info(f"📊 Streamlit port: {STREAMLIT_PORT}")
logger.info(f"🦗 Locust port: {LOCUST_PORT}")
logger.info(f"🌐 Public host: {PUBLIC_HOST}")

# --- Streamlit App Configuration ---
st.set_page_config(
    page_title="EAII🚀PTT - Performance Testing Tool",
    page_icon="🦗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS STYLES
# ============================================================================

HIDE_UI_CSS = """
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display: none;}
.st-emotion-cache-zq5wmm {visibility: hidden;}
</style>
"""

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

.stApp {
    background: linear-gradient(135deg, var(--cosmic-dark), var(--cosmic-darker));
}

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
    font-weight: 700 !important;
    box-shadow: 0 0 10px var(--cosmic-primary) !important;
    transition: all 0.3s ease !important;
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

.status-indicator {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    margin-right: 0.5rem;
    display: inline-block;
}

.status-healthy { background-color: #00C853; box-shadow: 0 0 8px #00C853; }
.status-warning { background-color: #FFC107; box-shadow: 0 0 8px #FFC107; }
.status-critical { background-color: #FF5252; box-shadow: 0 0 8px #FF5252; animation: pulse 1.5s infinite; }

@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(255, 82, 82, 0.7); }
    70% { box-shadow: 0 0 0 10px rgba(255, 82, 82, 0); }
    100% { box-shadow: 0 0 0 0 rgba(255, 82, 82, 0); }
}

.system-status {
    display: flex;
    align-items: center;
    padding: 8px;
    margin: 5px 0;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 5px;
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
    transition: all 0.3s ease;
}

.dashboard-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 20px rgba(106, 0, 255, 0.4);
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

/* Custom scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: var(--cosmic-darker);
}

::-webkit-scrollbar-thumb {
    background: var(--cosmic-primary);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--cosmic-accent);
}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# CONFIGURATION CONSTANTS
# ============================================================================

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

RATING_LABELS = {
    1: "Critical",
    2: "Warning",
    3: "Healthy (Acceptable)",
    4: "Healthy (Good)",
    5: "Healthy (Excellent)"
}

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'config' not in st.session_state:
    st.session_state.config = {}
if 'test_results' not in st.session_state:
    st.session_state.test_results = None
if 'test_error' not in st.session_state:
    st.session_state.test_error = None
if 'locust_output' not in st.session_state:
    st.session_state.locust_output = ""
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"
if 'test_running' not in st.session_state:
    st.session_state.test_running = False
if 'locust_process' not in st.session_state:
    st.session_state.locust_process = None
if 'generate_viz' not in st.session_state:
    st.session_state.generate_viz = False
if 'system_stats' not in st.session_state:
    st.session_state.system_stats = {
        'cpu': 0,
        'memory': 0,
        'network': {'sent': 0, 'recv': 0},
        'locust_active': False,
        'last_updated': 0
    }
if 'selected_test_type' not in st.session_state:
    st.session_state.selected_test_type = list(MAX_USERS_LIMITS.keys())[0]
if 'show_record_management' not in st.session_state:
    st.session_state.show_record_management = False
if 'test_saved' not in st.session_state:
    st.session_state.test_saved = False
if 'manual_stop' not in st.session_state:
    st.session_state.manual_stop = False

# ============================================================================
# HELPER FUNCTIONS (FIXED FOR RENDER)
# ============================================================================

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

    if r < 2.0:
        return "Critical", "critical", "⭐"
    elif r < 3.0:
        return "Warning", "warning", "⭐⭐"
    elif r < 3.5:
        return "Healthy (Acceptable)", "healthy", "⭐⭐⭐"
    elif r < 4.5:
        return "Healthy (Good)", "healthy", "⭐⭐⭐⭐"
    else:
        return "Healthy (Excellent)", "healthy", "⭐⭐⭐⭐⭐"

def format_timedelta(td):
    """Format timedelta into HH:MM:SS"""
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def get_system_metrics():
    """Returns CPU usage %, Memory usage %, Network Sent (MB), Network Received (MB)."""
    try:
        cpu_usage = psutil.cpu_percent(interval=0.5)
        mem_usage = psutil.virtual_memory().percent
        net_io = psutil.net_io_counters()
        net_sent = net_io.bytes_sent / (1024 * 1024)
        net_recv = net_io.bytes_recv / (1024 * 1024)
        return cpu_usage, mem_usage, net_sent, net_recv
    except Exception as e:
        logger.error(f"Error getting system metrics: {e}")
        return 0, 0, 0, 0

def verify_locust_installation():
    """Verify that Locust is properly installed and accessible"""
    try:
        # Try multiple methods to check locust
        methods = [
            ["locust", "--version"],
            ["python", "-m", "locust", "--version"],
            ["pip", "show", "locust"]
        ]
        
        for cmd in methods:
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    output = result.stdout.strip()
                    logger.info(f"✅ Locust check passed with: {' '.join(cmd)}")
                    logger.info(f"Output: {output[:100]}")
                    return True, output
            except FileNotFoundError:
                continue
            except Exception as e:
                logger.debug(f"Method {' '.join(cmd)} failed: {e}")
                continue
        
        # If we get here, try to install locust
        logger.warning("Locust not found, attempting to install...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "locust"], 
                         check=True, capture_output=True, text=True)
            logger.info("✅ Locust installed successfully")
            return True, "Installed on demand"
        except Exception as e:
            logger.error(f"Failed to install locust: {e}")
            return False, None
            
    except Exception as e:
        logger.error(f"❌ Error checking Locust: {e}")
        return False, None
        


def validate_target_url(url):
    """Validate the target URL format"""
    pattern = re.compile(
        r'^(?:http|ftp)s?://' 
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(pattern, url) is not None

def format_duration_display(duration_field) -> str:
    """Return a human-friendly duration string in minutes."""
    if duration_field is None:
        return "Unknown"

    if isinstance(duration_field, (int, float)):
        try:
            minutes = float(duration_field) / 60.0
            return f"{minutes:.1f} minutes"
        except Exception:
            return str(duration_field)

    s = str(duration_field).strip()
    if not s:
        return "Unknown"

    sec_match = re.search(r'([+-]?\d+(?:\.\d+)?)\s*(seconds|second|secs|sec|s)\b', s, re.I)
    if sec_match:
        try:
            secs = float(sec_match.group(1))
            return f"{secs/60.0:.1f} minutes"
        except Exception:
            return s

    min_match = re.search(r'([+-]?\d+(?:\.\d+)?)\s*(minutes|minute|min)\b', s, re.I)
    if min_match:
        try:
            mins = float(min_match.group(1))
            return f"{mins:.1f} minutes"
        except Exception:
            return s

    num_match = re.match(r'^([+-]?\d+(?:\.\d+)?)$', s)
    if num_match:
        try:
            mins = float(num_match.group(1))
            return f"{mins:.1f} minutes"
        except Exception:
            return s

    return s

def get_test_config(test_type, users, spawn_rate, duration):
    """Return the test configuration with appropriate limits applied."""
    max_users = MAX_USERS_LIMITS.get(test_type, 100000)
    users = min(users, max_users)
    default_duration = DEFAULT_DURATIONS.get(test_type, 600)
    
    if test_type in ["Load Test", "Stress Test", "Spike Test", "Volume Test", "Concurrency Test"]:
        duration = min(duration, default_duration)
    elif test_type == "Endurance Test":
        duration = max(duration, default_duration)
    
    return {"users": users, "spawn": spawn_rate, "duration": duration}

# ============================================================================
# LOCUST MANAGEMENT FUNCTIONS (FIXED FOR RENDER)
# ============================================================================

def verify_locust_installation():
    """Verify that Locust is properly installed and accessible"""
    try:
        result = subprocess.run(["locust", "--version"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version = result.stdout.strip()
            logger.info(f"✅ Locust installed: {version}")
            return True, version
        else:
            logger.error("❌ Locust command failed")
            return False, None
    except FileNotFoundError:
        logger.error("❌ Locust not found in PATH")
        return False, None
    except Exception as e:
        logger.error(f"❌ Error checking Locust: {e}")
        return False, None

def check_locust_status():
    """Check if Locust server is running with better error handling"""
    urls_to_try = [
        f"http://localhost:{LOCUST_PORT}/",
        f"http://127.0.0.1:{LOCUST_PORT}/",
    ]
    
    for url in urls_to_try:
        try:
            res = requests.get(url, timeout=2)
            if res.status_code == 200:
                return True
        except requests.exceptions.ConnectionError:
            continue
        except requests.exceptions.Timeout:
            continue
        except Exception as e:
            logger.debug(f"Error checking {url}: {e}")
            continue
    
    return False

def wait_for_locust(max_retries=30, delay=2):
    """Wait for Locust to become responsive"""
    for i in range(max_retries):
        if check_locust_status():
            logger.info(f"✅ Locust is responsive after {i+1} attempts")
            return True
        logger.info(f"Waiting for Locust to respond... ({i+1}/{max_retries})")
        time.sleep(delay)
    
    logger.error("❌ Locust failed to become responsive")
    return False

def start_locust_server(target_host):
    """Start Locust server process with comprehensive error handling"""
    try:
        # Kill any existing Locust processes
        if st.session_state.locust_process:
            try:
                st.session_state.locust_process.kill()
                st.session_state.locust_process.wait(timeout=5)
            except:
                pass
            st.session_state.locust_process = None
        
        # Verify Locust installation
        locust_installed, version = verify_locust_installation()
        if not locust_installed:
            st.error("❌ Locust is not installed. Please check your deployment.")
            return None
        
        # Prepare Locust command
        locust_cmd = [
            "locust",
            "-f", "locustfile.py",
            "--host", target_host,
            "--web-port", str(LOCUST_PORT),
            "--web-host", LOCUST_BIND_HOST,
            "--headless",
            "--only-summary"  # Reduce output
        ]
        
        logger.info(f"Starting Locust with command: {' '.join(locust_cmd)}")
        
        # Start Locust process
        if IS_RENDER:
            # On Render, capture output for debugging
            process = subprocess.Popen(
                locust_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                preexec_fn=os.setsid if os.name != 'nt' else None
            )
        else:
            process = subprocess.Popen(
                locust_cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        
        st.session_state.locust_process = process
        
        # Wait for process to start
        time.sleep(3)
        
        if process.poll() is None:
            logger.info(f"✅ Locust process started with PID: {process.pid}")
            
            # Wait for Locust to become responsive
            if wait_for_locust():
                st.session_state.system_stats['locust_active'] = True
                return process
            else:
                logger.error("❌ Locust process started but not responding")
                # Try to get error output
                if IS_RENDER:
                    try:
                        stdout, stderr = process.communicate(timeout=2)
                        logger.error(f"Locust stdout: {stdout}")
                        logger.error(f"Locust stderr: {stderr}")
                    except:
                        pass
                return None
        else:
            # Process died immediately
            if IS_RENDER:
                stdout, stderr = process.communicate()
                logger.error(f"❌ Locust failed to start:")
                logger.error(f"STDOUT: {stdout}")
                logger.error(f"STDERR: {stderr}")
            return None
            
    except Exception as e:
        logger.error(f"❌ Error starting Locust: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return None

def trigger_test(users, spawn_rate, host):
    """Trigger the Locust test with given parameters and better error handling."""
    max_retries = 30
    retry_delay = 2
    
    logger.info(f"Attempting to trigger test with {users} users at {spawn_rate}/sec")
    
    for attempt in range(max_retries):
        try:
            if not check_locust_status():
                logger.info(f"Locust not ready yet (attempt {attempt+1}/{max_retries})")
                time.sleep(retry_delay)
                continue
            
            # Try to trigger the test
            response = requests.post(
                f"http://localhost:{LOCUST_PORT}/swarm",
                data={
                    "user_count": users,
                    "spawn_rate": spawn_rate,
                    "host": host
                },
                timeout=10,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            if response.status_code == 200:
                logger.info(f"✅ Test triggered successfully on attempt {attempt+1}")
                return True
            else:
                logger.error(f"❌ Trigger failed with status {response.status_code}: {response.text}")
                
        except requests.exceptions.ConnectionError as e:
            logger.info(f"Connection refused (attempt {attempt+1}/{max_retries}): {e}")
        except requests.exceptions.Timeout as e:
            logger.info(f"Timeout (attempt {attempt+1}/{max_retries}): {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
        
        time.sleep(retry_delay)
    
    logger.error("❌ Failed to trigger test after all retries")
    return False

def stop_test():
    """Stop the running Locust test and clean up the process."""
    try:
        # Try to stop via API
        try:
            res = requests.get(f"http://localhost:{LOCUST_PORT}/stop", timeout=5)
            logger.info(f"Stop API response: {res.status_code}")
        except:
            pass
        
        # Kill the process
        if st.session_state.locust_process:
            try:
                if os.name == 'nt':  # Windows
                    st.session_state.locust_process.terminate()
                else:  # Unix/Linux
                    os.killpg(os.getpgid(st.session_state.locust_process.pid), signal.SIGTERM)
                
                st.session_state.locust_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                st.session_state.locust_process.kill()
            except Exception as e:
                logger.error(f"Error killing process: {e}")
            finally:
                st.session_state.locust_process = None
        
        # Update status
        st.session_state.system_stats.update({
            'locust_active': False,
            'last_updated': time.time()
        })
        
        return True
        
    except Exception as e:
        logger.error(f"Error in stop_test: {e}")
        return False

def fetch_stats():
    """Fetch current statistics from Locust."""
    try:
        response = requests.get(
            f"http://localhost:{LOCUST_PORT}/stats/requests",
            timeout=5
        )
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException as e:
        logger.debug(f"Error fetching stats: {e}")
    except Exception as e:
        logger.error(f"Unexpected error fetching stats: {e}")
    
    return None

def display_system_status():
    """Display system status cards in Streamlit sidebar."""
    try:
        cpu_usage, mem_usage, net_sent, net_recv = get_system_metrics()
        locust_active = check_locust_status()
        
        st.session_state.system_stats.update({
            'cpu': cpu_usage,
            'memory': mem_usage,
            'network': {'sent': net_sent, 'recv': net_recv},
            'locust_active': locust_active,
            'last_updated': time.time()
        })
        
        stats = st.session_state.system_stats
        
        # CPU status
        cpu_class = "status-healthy" if stats['cpu'] <= 70 else \
                    "status-warning" if stats['cpu'] <= 90 else "status-critical"
        
        st.sidebar.markdown(f"""
        <div class="system-status">
            <span class="status-indicator {cpu_class}"></span>
            <span>CPU: {stats['cpu']:.1f}%</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Memory status
        mem_class = "status-healthy" if stats['memory'] <= 80 else \
                    "status-warning" if stats['memory'] <= 90 else "status-critical"
        
        st.sidebar.markdown(f"""
        <div class="system-status">
            <span class="status-indicator {mem_class}"></span>
            <span>Memory: {stats['memory']:.1f}%</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Network
        st.sidebar.markdown(f"""
        <div class="system-status">
            <span class="status-indicator status-healthy"></span>
            <span>↑{stats['network']['sent']:.1f}MB ↓{stats['network']['recv']:.1f}MB</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Locust status
        locust_class = "status-healthy" if stats['locust_active'] else "status-critical"
        locust_text = "Active" if stats['locust_active'] else "Inactive"
        
        st.sidebar.markdown(f"""
        <div class="system-status">
            <span class="status-indicator {locust_class}"></span>
            <span>Locust: {locust_text}</span>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        logger.error(f"Error displaying system status: {e}")
        st.sidebar.error("⚠️ Status unavailable")

# ============================================================================
# MONITOR TEST FUNCTION (FIXED FOR RENDER)
# ============================================================================

def monitor_test(duration: int) -> pd.DataFrame:
    """Monitor the test progress with enhanced UI and statistics collection."""
    
    # Calculate test phases
    ramp_time = duration // 3
    steady_time = duration // 3
    ramp_down_time = duration // 3
    
    if ramp_time <= 0 or steady_time <= 0 or ramp_down_time <= 0:
        st.error("⚠️ Test duration too short - increase test duration")
        return pd.DataFrame()
    
    # Timeline calculation
    start_time = time.time()
    timeline = {
        'ramp_up_end': start_time + ramp_time,
        'steady_end': start_time + ramp_time + steady_time,
        'test_end': start_time + duration
    }
    
    # UI Containers
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
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🛑 Stop Test", key="stop_test", type="primary", use_container_width=True):
                st.session_state.manual_stop = True
        with col2:
            if st.button("🔄 Refresh", key="refresh", use_container_width=True):
                st.rerun()
    
    try:
        while time.time() < timeline['test_end'] and st.session_state.get("test_running", False):
            current_time = time.time()
            elapsed = current_time - start_time
            remaining = max(0, duration - elapsed)
            progress = min(max((elapsed / duration) * 100, 0), 100)
            
            # Check for manual stop
            if st.session_state.get('manual_stop', False):
                notification_placeholder.markdown("""
                <div style="background: rgba(255, 171, 0, 0.15); padding: 15px; border-radius: 8px; border-left: 4px solid #FFAB00;">
                    <h3>🛑 Test Stopped Manually</h3>
                </div>
                """, unsafe_allow_html=True)
                st.session_state.test_running = False
                break
            
            # Determine current phase
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
                cols = st.columns(3)
                with cols[0]:
                    st.markdown(f"""
                    <div class="metric-container">
                        <div style="font-size: 1rem;">⏱️ Elapsed</div>
                        <div style="font-size: 1.5rem; font-weight: bold;">{format_timedelta(timedelta(seconds=elapsed))}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with cols[1]:
                    st.progress(progress/100)
                    st.markdown(f"<p style='text-align:center; color:{phase_color};'>Overall: {progress:.1f}%</p>", unsafe_allow_html=True)
                    st.progress(phase_progress/100)
                    st.markdown(f"<p style='text-align:center; color:{phase_color};'>{phase}: {phase_progress:.1f}%</p>", unsafe_allow_html=True)
                
                with cols[2]:
                    st.markdown(f"""
                    <div class="metric-container">
                        <div style="font-size: 1rem;">⏳ Remaining</div>
                        <div style="font-size: 1.5rem; font-weight: bold;">{format_timedelta(timedelta(seconds=remaining))}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Phase info
            with phase_placeholder.container():
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; background: rgba(106, 0, 255, 0.1); padding: 10px; border-radius: 8px;">
                    <div><strong>Current Phase:</strong> <span style="color:{phase_color};">{phase}</span></div>
                    <div><strong>Phase Remaining:</strong> {format_timedelta(timedelta(seconds=max(0, phase_remaining)))}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Collect stats
            data = fetch_stats()
            if data and "stats" in data:
                total = next((item for item in data["stats"] if item["name"] == "Total"), None)
                if total:
                    stats.append({
                        "Timestamp": datetime.now().strftime("%H:%M:%S"),
                        "Phase": phase,
                        "Users": total.get("user_count", 0),
                        "RPS": round(total.get("total_rps", 0), 2),
                        "Avg Response": round(total.get("avg_response_time", 0), 2),
                        "Fail %": round(total.get("fail_ratio", 0) * 100, 2),
                        "95%ile": round(total.get("response_time_percentile_95", 0), 2),
                    })
                    
                    with stats_placeholder.container():
                        st.dataframe(
                            pd.DataFrame(stats).tail(5),
                            height=200,
                            use_container_width=True
                        )
            
            # Dashboard link (conditional for Render)
            if SHOW_LOCUST_DASHBOARD:
                dashboard_placeholder.markdown(
                    f'<a href="http://{PUBLIC_HOST}:{LOCUST_PORT}" target="_blank" class="dashboard-btn">📊 Open Live Performance Dashboard</a>',
                    unsafe_allow_html=True
                )
            else:
                dashboard_placeholder.markdown("""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 15px; border-radius: 10px; text-align: center; color: white;">
                    <h4>📊 Live Performance Monitoring</h4>
                    <p>Real-time metrics are displayed below. The full Locust dashboard is available when running locally.</p>
                </div>
                """, unsafe_allow_html=True)
            
            time.sleep(2)  # Update every 2 seconds
        
        # Test completed
        if time.time() >= timeline['test_end'] and st.session_state.get("test_running", False):
            notification_placeholder.markdown(f"""
            <div style="background: rgba(0, 200, 83, 0.15); padding: 15px; border-radius: 8px; border-left: 4px solid #00C853;">
                <h3>✅ Test Completed Successfully</h3>
                <p>Ran for {format_timedelta(timedelta(seconds=duration))}</p>
            </div>
            """, unsafe_allow_html=True)
            st.session_state.test_running = False
    
    except Exception as e:
        logger.error(f"Monitoring error: {str(e)}", exc_info=True)
        notification_placeholder.markdown(f"""
        <div style="background: rgba(255, 82, 82, 0.15); padding: 15px; border-radius: 8px; border-left: 4px solid #FF5252;">
            <h3>❌ Monitoring Error</h3>
            <p>{str(e)}</p>
        </div>
        """, unsafe_allow_html=True)
    
    finally:
        st.session_state.test_running = False
        stop_test()
        
        if st.session_state.get('manual_stop', False):
            notification_placeholder.markdown(f"""
            <div style="background: rgba(255, 171, 0, 0.15); padding: 15px; border-radius: 8px; border-left: 4px solid #FFAB00;">
                <h3>🛑 Test Stopped</h3>
                <p>Stopped after {format_timedelta(timedelta(seconds=elapsed))}</p>
            </div>
            """, unsafe_allow_html=True)
        
        return pd.DataFrame(stats)

# ============================================================================
# TEST HISTORY FUNCTIONS
# ============================================================================

def save_test_history(test_data, graph_filename=None):
    """Save test data to the test history JSON file."""
    history_dir = '/tmp/test_history' if IS_RENDER else 'test_history'
    os.makedirs(history_dir, exist_ok=True)
    history_file = os.path.join(history_dir, 'test_history.json')
    
    if "test_id" not in test_data:
        test_data["test_id"] = f"TEST_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
    
    users = test_data.get("users")
    if users is None or users == "Unknown":
        users = test_data.get("config", {}).get("users", "Not Provided")
    
    try:
        users = int(users)
    except (ValueError, TypeError):
        pass
    
    duration = test_data.get("duration")
    if duration is None or duration == "Unknown":
        stats = test_data.get("stats", {})
        total_requests = stats.get("total_requests", 0)
        rps = stats.get("rps", 0)
        if rps > 0 and total_requests > 0:
            duration_seconds = total_requests / rps
            duration = f"{round(duration_seconds / 60, 2)}"
        else:
            duration = "Not Provided"
    
    test_record = {
        "test_id": test_data.get("test_id"),
        "project_name": test_data.get("project_name", "Unnamed"),
        "test_type": test_data.get("test_type", "Load"),
        "timestamp": test_data.get("timestamp", datetime.now().isoformat()),
        "users": str(users),
        "duration": str(duration),
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
    
    test_history = []
    try:
        if os.path.exists(history_file):
            with open(history_file, "r") as f:
                test_history = json.load(f)
                if not isinstance(test_history, list):
                    test_history = []
    except (json.JSONDecodeError, FileNotFoundError):
        test_history = []
    
    existing_index = next((i for i, t in enumerate(test_history) 
                          if t["test_id"] == test_record["test_id"]), -1)
    
    if existing_index >= 0:
        test_history[existing_index] = test_record
    else:
        test_history.append(test_record)
    
    try:
        with open(history_file, "w") as f:
            json.dump(test_history, f, indent=2)
        st.success(f"Test '{test_record['test_id']}' saved successfully! ✅")
        return True
    except Exception as e:
        st.error(f"Failed to save test history: {e}")
        return False

def delete_test_record(test_id, test_history):
    """Delete a test record and its associated graph file."""
    try:
        test_to_delete = next(t for t in test_history if t['test_id'] == test_id)
        
        if test_to_delete.get('graph_file') and os.path.exists(test_to_delete['graph_file']):
            os.remove(test_to_delete['graph_file'])
        
        updated_history = [t for t in test_history if t['test_id'] != test_id]
        
        history_file = '/tmp/test_history/test_history.json' if IS_RENDER else 'test_history/test_history.json'
        with open(history_file, 'w') as f:
            json.dump(updated_history, f, indent=2)
            
        return True, f"Deleted test {test_id} and associated files"
        
    except Exception as e:
        return False, f"Deletion failed: {str(e)}"

# ============================================================================
# PERFORMANCE GRAPH FUNCTIONS
# ============================================================================

def generate_performance_graph(actual_performance, test_type, total_requests, failures_rate):
    """Generate a performance dashboard with fallback on error."""
    try:
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
        
        normalized_test_type = test_type.lower().strip()
        matched_test = None
        for test_key in STANDARDS:
            if normalized_test_type in [test_key, STANDARDS[test_key]["display_name"].lower()]:
                matched_test = test_key
                break
        if not matched_test:
            matched_test = "load"
        
        test_config = STANDARDS[matched_test]
        metrics_config = test_config["metrics"]
        
        if isinstance(actual_performance, list):
            metric_names = list(metrics_config.keys())
            actual_performance = dict(zip(metric_names, actual_performance))
        
        standardized_data = {}
        for metric, value in actual_performance.items():
            try:
                standardized_data[metric] = float(value)
            except (ValueError, TypeError):
                standardized_data[metric] = 0
        
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
                
                if metric == 'Failure Rate (%)':
                    ratio = 1 - (actual_value / max(1, critical))
                else:
                    if 'Response Time' in metric:
                        ratio = target / max(1, actual_value)
                    else:
                        ratio = actual_value / max(1, target)
                
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
        logger.error(f"Error generating performance graph: {e}")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.text(0.5, 0.5, f"Graph generation failed.\nError: {e}",
                ha='center', va='center', fontsize=14, color='red',
                transform=ax.transAxes)
        ax.set_title("Performance Graph Error", fontsize=16)
        ax.axis('off')
        return fig

# ============================================================================
# HTML REPORT FUNCTIONS (Simplified for brevity)
# ============================================================================

def generate_html_report(test_data):
    """Generate HTML report (simplified version)."""
    test_type = test_data.get("test_type", "Load Test")
    project_name = test_data.get("project_name", "Unnamed")
    test_id = test_data.get("test_id", str(uuid.uuid4())[:8])
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    users = test_data.get("users", "N/A")
    duration = test_data.get("duration", "N/A")
    
    stats = test_data.get("stats", {})
    total_requests = stats.get("total_requests", 0)
    failures_rate = stats.get("failures_rate", 0)
    rps = stats.get("rps", 0)
    avg_response = stats.get("avg_response_time", 0)
    p95_response = stats.get("p95_response_time", 0)
    max_response = stats.get("max_response_time", 0)
    
    overall_status = test_data.get("overall_status", "Unknown")
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Performance Report - {test_id}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
            .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            h1 {{ color: #333; border-bottom: 2px solid #6a00ff; padding-bottom: 10px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; margin-bottom: 30px; }}
            .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 30px 0; }}
            .metric {{ background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; border-left: 4px solid #6a00ff; }}
            .metric-value {{ font-size: 24px; font-weight: bold; color: #6a00ff; }}
            .status {{ display: inline-block; padding: 5px 15px; border-radius: 20px; font-weight: bold; }}
            .status.healthy {{ background: #d4edda; color: #155724; }}
            .status.warning {{ background: #fff3cd; color: #856404; }}
            .status.critical {{ background: #f8d7da; color: #721c24; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background: #6a00ff; color: white; }}
            tr:hover {{ background: #f5f5f5; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Performance Test Report</h1>
                <p><strong>Project:</strong> {project_name}</p>
                <p><strong>Test ID:</strong> {test_id}</p>
                <p><strong>Date:</strong> {timestamp}</p>
            </div>
            
            <div style="margin: 20px 0;">
                <h2>Test Summary</h2>
                <p><strong>Test Type:</strong> {test_type}</p>
                <p><strong>Users:</strong> {users}</p>
                <p><strong>Duration:</strong> {duration}</p>
                <p><strong>Overall Status:</strong> <span class="status {overall_status.lower().replace(' ', '-')}">{overall_status}</span></p>
            </div>
            
            <h2>Performance Metrics</h2>
            <div class="metrics">
                <div class="metric">
                    <div>Total Requests</div>
                    <div class="metric-value">{total_requests:,}</div>
                </div>
                <div class="metric">
                    <div>Requests/sec</div>
                    <div class="metric-value">{rps:.1f}</div>
                </div>
                <div class="metric">
                    <div>Avg Response</div>
                    <div class="metric-value">{avg_response:.1f} ms</div>
                </div>
                <div class="metric">
                    <div>P95 Response</div>
                    <div class="metric-value">{p95_response:.1f} ms</div>
                </div>
                <div class="metric">
                    <div>Max Response</div>
                    <div class="metric-value">{max_response:.1f} ms</div>
                </div>
                <div class="metric">
                    <div>Failure Rate</div>
                    <div class="metric-value">{failures_rate:.2f}%</div>
                </div>
            </div>
            
            <footer style="margin-top: 40px; text-align: center; color: #666; font-size: 12px;">
                <p>Generated by EAII Performance Testing Tool | Ethiopian Artificial Intelligence Institute</p>
            </footer>
        </div>
    </body>
    </html>
    """
    
    return html

def save_report_html(html_content: str, filename: str) -> str:
    """Save HTML report to disk."""
    reports_dir = '/tmp/reports' if IS_RENDER else 'reports'
    os.makedirs(reports_dir, exist_ok=True)
    path = os.path.join(reports_dir, filename)
    try:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(html_content)
        return path
    except Exception as e:
        logger.error(f"Failed to save report file {path}: {e}")
        return ""

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================

with st.sidebar:
    st.markdown(
        '''
        <h1 style="text-align:center; color: #00e5ff;">EAII 🚀 PTT</h1>
        <blockquote style="text-align:center; font-size:0.9rem;">"Quality isn't just a goal — it's our guarantee."</blockquote>
        ''',
        unsafe_allow_html=True
    )
    
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.current_page = "Home"
    
    if st.button("📊 Test History", use_container_width=True):
        st.session_state.current_page = "Test History"
    
    if st.button("❓ Help", use_container_width=True):
        st.session_state.current_page = "Help"
    
    if st.button("ℹ️ About", use_container_width=True):
        st.session_state.current_page = "About System"
    
    st.markdown("---")
    st.markdown("### 🖥️ System Status")
    display_system_status()
    
    st.markdown("---")
    st.markdown(
        """
        <div style="background-color: #6A0DAD; color: white; padding: 8px; border-radius: 5px; text-align: center; font-size: 0.8rem;">
            Ethiopian AI Institute | QA Dept © 2025
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================================
# MAIN CONTENT
# ============================================================================

if st.session_state.current_page == "Home":
    # Header with logo
    col1, col2 = st.columns([1, 4])
    with col1:
        if os.path.exists('image/logo.png'):
            st.image('image/logo.png', width=100)
        else:
            st.markdown("<h1 style='color: #00e5ff;'>EAII</h1>", unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <h2>Performance Testing Tool</h2>
        <p style='color: #d1f7ff;'>Comprehensive performance testing powered by Locust</p>
        """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🧪 Test Configuration", "📊 Performance Analysis"])
    
    with tab1:
        st.markdown("### ⚙️ TEST PARAMETERS")
        
        col1, col2 = st.columns(2)
        with col1:
            project_name = st.text_input("📋 Project Name", value="Test Project")
            target_host = st.text_input("🌐 Target URL", value="http://example.com")
            test_type = st.selectbox(
                "🔧 Test Type",
                list(MAX_USERS_LIMITS.keys()),
                key="test_type_select"
            )
            st.info(TEST_TYPE_DESCRIPTIONS.get(test_type, ""))
        
        with col2:
            max_users = MAX_USERS_LIMITS[test_type]
            users = st.number_input(
                f"👥 Total Users (Max {max_users:,})",
                min_value=1,
                max_value=max_users,
                value=100
            )
            spawn_rate = st.slider(
                "📈 Spawn Rate (users/sec)",
                1, 100,
                value=10
            )
            duration = st.number_input(
                "⏱️ Duration (seconds)",
                min_value=10,
                max_value=86400,
                value=DEFAULT_DURATIONS[test_type]
            )
            st.caption(f"≈ {duration//60} minutes, {duration%60} seconds")
        
        if not st.session_state.test_running:
    if st.button("🚀 Start Performance Test", type="primary", use_container_width=True):
        st.session_state.test_running = True
        st.session_state.config = get_test_config(test_type, users, spawn_rate, duration)
        st.session_state.project_name = project_name
        st.session_state.manual_stop = False
        
        # Create expandable debug section
        with st.expander("🔧 Debug Information", expanded=True):
            st.write("### System Information")
            st.write(f"- Python: {sys.version}")
            st.write(f"- Platform: {platform.platform()}")
            st.write(f"- Render: {IS_RENDER}")
            st.write(f"- Locust Port: {LOCUST_PORT}")
            
            # Check PATH
            st.write("### PATH")
            st.code("\n".join(os.environ.get("PATH", "").split(":")))
            
            # Try to find locust
            st.write("### Locust Location")
            try:
                which_locust = subprocess.run(["which", "locust"], capture_output=True, text=True)
                st.write(f"which locust: {which_locust.stdout}")
                if which_locust.returncode != 0:
                    st.error("locust not found in PATH")
            except Exception as e:
                st.error(f"Error checking locust: {e}")
            
            # Try to run locust --version
            st.write("### Locust Version")
            try:
                result = subprocess.run(["locust", "--version"], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    st.success(f"✅ {result.stdout}")
                else:
                    st.error(f"❌ Error: {result.stderr}")
            except FileNotFoundError:
                st.error("❌ locust command not found")
            except Exception as e:
                st.error(f"❌ Exception: {e}")
            
            # List installed packages
            st.write("### Installed Packages")
            try:
                pip_list = subprocess.run([sys.executable, "-m", "pip", "list"], 
                                         capture_output=True, text=True)
                locust_packages = [line for line in pip_list.stdout.split('\n') 
                                 if 'locust' in line.lower()]
                if locust_packages:
                    st.success("✅ Found: " + "\n".join(locust_packages))
                else:
                    st.error("❌ No locust packages found in pip list")
            except Exception as e:
                st.error(f"Error listing packages: {e}")
        
        # Ask user to check debug info
        st.warning("Please check the debug information above. If locust is not found, the deployment needs to be fixed.")
        st.session_state.test_running = False
                
                # Show test summary
                with st.expander("Test Configuration", expanded=True):
                    cols = st.columns(4)
                    cols[0].metric("Project", project_name)
                    cols[1].metric("Test Type", test_type)
                    cols[2].metric("Users", st.session_state.config['users'])
                    cols[3].metric("Duration", f"{st.session_state.config['duration']}s")
                
                # Progress indicators
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    # Step 1: Check Locust
                    status_text.text("🔍 Checking Locust installation...")
                    locust_ok, version = verify_locust_installation()
                    if not locust_ok:
                        st.error("❌ Locust is not installed or not accessible")
                        st.session_state.test_running = False
                        st.stop()
                    
                    progress_bar.progress(25)
                    
                    # Step 2: Start Locust
                    status_text.text("🚀 Starting Locust server...")
                    process = start_locust_server(target_host)
                    if not process:
                        st.error("❌ Failed to start Locust server")
                        st.session_state.test_running = False
                        st.stop()
                    
                    progress_bar.progress(50)
                    
                    # Step 3: Trigger test
                    status_text.text("🎯 Triggering test...")
                    if not trigger_test(users, spawn_rate, target_host):
                        st.error("❌ Failed to trigger test")
                        st.session_state.test_running = False
                        stop_test()
                        st.stop()
                    
                    progress_bar.progress(75)
                    status_text.text("📊 Test running...")
                    
                    # Step 4: Monitor test
                    df_stats = monitor_test(duration)
                    
                    progress_bar.progress(100)
                    status_text.text("✅ Test completed!")
                    
                    # Show results
                    if not df_stats.empty:
                        st.success("✅ Test completed successfully!")
                        st.dataframe(df_stats, use_container_width=True)
                        
                        # Calculate summary stats
                        total_requests = df_stats["RPS"].sum() * (duration / len(df_stats))
                        failures_rate = df_stats["Fail %"].mean()
                        avg_rps = df_stats["RPS"].mean()
                        avg_response = df_stats["Avg Response"].mean()
                        p95_response = df_stats["95%ile"].mean()
                        
                        # Create test data
                        test_data = {
                            "test_id": str(uuid.uuid4()),
                            "test_type": test_type,
                            "project_name": project_name,
                            "users": users,
                            "duration": f"{duration} seconds",
                            "start_time": datetime.now().isoformat(),
                            "end_time": datetime.now().isoformat(),
                            "stats": {
                                "total_requests": total_requests,
                                "failures_rate": failures_rate,
                                "rps": avg_rps,
                                "avg_response_time": avg_response,
                                "p95_response_time": p95_response,
                                "max_response_time": df_stats["Avg Response"].max()
                            },
                            "overall_status": "✅ Completed"
                        }
                        
                        # Generate graph
                        actual_performance = {
                            "Requests Per Second (RPS)": avg_rps,
                            "Average Response Time (ms)": avg_response,
                            "95th Percentile Response Time (ms)": p95_response,
                            "Max Response Time (ms)": df_stats["Avg Response"].max(),
                            "Failure Rate (%)": failures_rate
                        }
                        
                        graph_dir = '/tmp/test_history' if IS_RENDER else 'test_history'
                        os.makedirs(graph_dir, exist_ok=True)
                        graph_filename = f"{graph_dir}/{test_data['test_id']}_graph.png"
                        
                        fig = generate_performance_graph(actual_performance, test_type, total_requests, failures_rate)
                        fig.savefig(graph_filename, bbox_inches="tight", dpi=100)
                        plt.close(fig)
                        
                        # Save history
                        save_test_history(test_data, graph_filename)
                        
                        # Download buttons
                        col1, col2 = st.columns(2)
                        with col1:
                            if os.path.exists(graph_filename):
                                with open(graph_filename, "rb") as f:
                                    st.download_button(
                                        "📥 Download Graph",
                                        f.read(),
                                        file_name=f"graph_{test_data['test_id']}.png",
                                        mime="image/png"
                                    )
                        
                        with col2:
                            html_report = generate_html_report(test_data)
                            st.download_button(
                                "📥 Download Report",
                                html_report,
                                file_name=f"report_{test_data['test_id']}.html",
                                mime="text/html"
                            )
                
                except Exception as e:
                    st.error(f"❌ Error during test: {str(e)}")
                    logger.error(f"Test error: {str(e)}", exc_info=True)
                
                finally:
                    st.session_state.test_running = False
                    stop_test()
        
        else:
            st.warning("⚠️ A test is currently running. Please wait or stop it.")
    
    with tab2:
        st.markdown("### 📊 Performance Analysis")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("#### Input Metrics")
            graph_test_type = st.selectbox(
                "Test Type",
                ["Load", "Stress", "Spike", "Endurance", "Volume", "Concurrency"],
                key="graph_type"
            )
            
            total_requests = st.number_input("Total Requests", value=10000, min_value=0)
            failures_rate = st.number_input("Failure Rate (%)", value=0.0, min_value=0.0, max_value=100.0, step=0.1)
            
            rps = st.number_input("Requests/sec", value=100, min_value=0)
            avg_response = st.number_input("Avg Response (ms)", value=200, min_value=0)
            p95_response = st.number_input("P95 Response (ms)", value=500, min_value=0)
            max_response = st.number_input("Max Response (ms)", value=2000, min_value=0)
            
            if st.button("Generate Visualization", use_container_width=True):
                actual_performance = {
                    "Requests Per Second (RPS)": rps,
                    "Average Response Time (ms)": avg_response,
                    "95th Percentile Response Time (ms)": p95_response,
                    "Max Response Time (ms)": max_response,
                    "Failure Rate (%)": failures_rate
                }
                
                fig = generate_performance_graph(actual_performance, graph_test_type, total_requests, failures_rate)
                st.session_state.current_fig = fig
        
        with col2:
            if 'current_fig' in st.session_state:
                st.pyplot(st.session_state.current_fig)
            else:
                st.info("👈 Configure metrics and click 'Generate Visualization'")

elif st.session_state.current_page == "Test History":
    st.title("📊 Test History")
    
    history_file = '/tmp/test_history/test_history.json' if IS_RENDER else 'test_history/test_history.json'
    
    try:
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                test_history = json.load(f)
            
            if test_history:
                # Summary stats
                healthy = sum(1 for t in test_history if 'Healthy' in t.get('overall_status', ''))
                warning = sum(1 for t in test_history if 'Warning' in t.get('overall_status', ''))
                critical = sum(1 for t in test_history if 'Critical' in t.get('overall_status', ''))
                
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Total Tests", len(test_history))
                col2.metric("✅ Healthy", healthy)
                col3.metric("⚠️ Warning", warning)
                col4.metric("❌ Critical", critical)
                
                # Display tests
                for test in reversed(test_history):
                    with st.expander(f"{test['test_type']} - {test['project_name']} - {test['test_id']}"):
                        cols = st.columns(4)
                        cols[0].metric("Status", test.get('overall_status', 'Unknown'))
                        cols[0].metric("Users", test.get('users', 'N/A'))
                        cols[1].metric("Duration", format_duration_display(test.get('duration')))
                        cols[1].metric("Requests", test['stats'].get('total_requests', 0))
                        cols[2].metric("RPS", f"{test['stats'].get('rps', 0):.1f}")
                        cols[2].metric("Avg Response", f"{test['stats'].get('avg_response_time', 0):.1f} ms")
                        cols[3].metric("Fail Rate", f"{test['stats'].get('failures_rate', 0):.1f}%")
                        cols[3].metric("P95", f"{test['stats'].get('p95_response_time', 0):.1f} ms")
                        
                        # Actions
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if st.button(f"📄 Report", key=f"report_{test['test_id']}"):
                                html_report = generate_html_report(test)
                                st.download_button(
                                    "⬇️ Download HTML",
                                    html_report,
                                    file_name=f"report_{test['test_id']}.html",
                                    mime="text/html"
                                )
                        
                        with col2:
                            if test.get('graph_file') and os.path.exists(test['graph_file']):
                                with open(test['graph_file'], 'rb') as f:
                                    st.download_button(
                                        "📊 Download Graph",
                                        f.read(),
                                        file_name=f"graph_{test['test_id']}.png",
                                        mime="image/png"
                                    )
                        
                        with col3:
                            if st.button(f"🗑️ Delete", key=f"delete_{test['test_id']}"):
                                success, msg = delete_test_record(test['test_id'], test_history)
                                if success:
                                    st.success(msg)
                                    st.rerun()
                                else:
                                    st.error(msg)
            else:
                st.info("No test history found. Run some tests first!")
        else:
            st.info("No test history found. Run some tests first!")
    
    except Exception as e:
        st.error(f"Error loading test history: {e}")

elif st.session_state.current_page == "Help":
    st.title("❓ Help & Documentation")
    
    tabs = st.tabs(["Getting Started", "Test Configuration", "Understanding Results"])
    
    with tabs[0]:
        st.markdown("""
        ### Getting Started
        
        1. **Enter your project name** - Give your test a meaningful name
        2. **Set the target URL** - The endpoint you want to test (e.g., https://yourapp.com)
        3. **Choose test type** - Select the appropriate test type for your needs
        4. **Configure users** - Set the number of virtual users and spawn rate
        5. **Set duration** - How long the test should run
        6. **Click Start** - Begin the performance test
        
        ### Key Features
        - Multiple test types for different scenarios
        - Real-time metrics visualization
        - Historical test tracking
        - Exportable reports and graphs
        """)
    
    with tabs[1]:
        st.markdown("""
        ### Test Types
        
        - **Load Test**: Simulates expected user load to evaluate normal performance
        - **Stress Test**: Pushes beyond normal capacity to find breaking points
        - **Spike Test**: Sudden bursts of user activity
        - **Endurance Test**: Long-running tests to find memory leaks
        - **Volume Test**: Tests with large amounts of data
        - **Concurrency Test**: High number of simultaneous users
        
        ### Parameters
        - **Users**: Number of virtual users to simulate
        - **Spawn Rate**: How quickly users are added (users/second)
        - **Duration**: Total test duration in seconds
        """)
    
    with tabs[2]:
        st.markdown("""
        ### Understanding Results
        
        - **RPS (Requests Per Second)**: Throughput of your system
        - **Response Time**: How fast your system responds
        - **Failure Rate**: Percentage of failed requests
        - **95th Percentile**: Response time for 95% of requests
        - **Max Response Time**: Slowest request time
        
        ### Status Indicators
        - ✅ **Healthy**: Performance meets or exceeds targets
        - ⚠️ **Warning**: Performance is below optimal levels
        - ❌ **Critical**: Immediate action required
        """)

elif st.session_state.current_page == "About System":
    st.title("ℹ️ About the System")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### EAII Performance Testing Tool
        **Version:** 1.1.0  
        **Release:** June 2025  
        **Developer:** QA Department  
        **Institution:** Ethiopian Artificial Intelligence Institute
        
        A comprehensive performance testing solution designed to:
        - Validate system reliability under various load conditions
        - Identify performance bottlenecks
        - Ensure optimal user experience
        """)
    
    with col2:
        st.markdown("""
        ### Core Technologies
        - Python 3.10+
        - Streamlit 1.28+
        - Locust 2.15+
        - Pandas 2.0+
        - Matplotlib 3.7+
        
        ### System Requirements
        - CPU: 2+ cores
        - RAM: 2+ GB
        - Storage: 1+ GB
        """)
    
    st.markdown("---")
    st.markdown("""
    ### License
    This software is proprietary technology of the Ethiopian Artificial Intelligence Institute.
    Unauthorized use, duplication, or distribution is strictly prohibited.
    
    **Support:** qa-support@eaii.gov.et
    """)

# ============================================================================
# CLEANUP ON EXIT
# ============================================================================

import atexit

def cleanup():
    """Cleanup function to stop Locust on exit"""
    if st.session_state.locust_process:
        logger.info("Cleaning up Locust process...")
        stop_test()

atexit.register(cleanup)


