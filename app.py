import json
import pathlib
import streamlit as st

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AL-Enabled Smart Traffic Light Signal",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Dark theme override ─────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* Global dark */
  html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background-color: #020812 !important;
  }
  [data-testid="stSidebar"] {
    background-color: #040c1a !important;
    border-right: 1px solid rgba(0,229,255,0.15);
  }
  section.main > div { padding-top: 10px !important; }

  /* Sidebar text */
  .sidebar-title {
    font-family: 'Courier New', monospace;
    font-size: 0.65rem;
    letter-spacing: 3px;
    color: #00e5ff;
    margin-bottom: 6px;
    border-bottom: 1px solid rgba(0,229,255,0.15);
    padding-bottom: 6px;
  }
  .road-section {
    background: rgba(0,229,255,0.03);
    border: 1px solid rgba(0,229,255,0.1);
    border-radius: 6px;
    padding: 12px;
    margin-bottom: 12px;
  }
  .road-section.north { border-color: rgba(0,255,136,0.2); }
  .road-section.south { border-color: rgba(0,100,255,0.2); }
  .road-section.west  { border-color: rgba(200,100,255,0.2); }

  /* Streamlit slider track */
  [data-testid="stSlider"] > div > div > div { background: rgba(0,229,255,0.3) !important; }

  /* General text */
  p, label, .stSlider label, .stSelectbox label { color: #c8e6ff !important; }
  h1, h2, h3 { color: #00e5ff !important; font-family: 'Courier New', monospace !important; letter-spacing: 2px; }

  /* Buttons */
  .stButton > button {
    background: transparent !important;
    border: 1px solid rgba(255,80,0,0.5) !important;
    color: rgba(255,150,80,0.9) !important;
    font-family: 'Courier New', monospace !important;
    letter-spacing: 2px !important;
    font-size: 0.65rem !important;
    width: 100%;
    transition: all 0.2s;
  }
  .stButton > button:hover {
    background: rgba(255,80,0,0.15) !important;
    border-color: #ff5000 !important;
    color: #ff8040 !important;
    box-shadow: 0 0 12px rgba(255,80,0,0.3);
  }

  /* Status metric cards */
  [data-testid="stMetric"] {
    background: rgba(0,229,255,0.04) !important;
    border: 1px solid rgba(0,229,255,0.12) !important;
    border-radius: 6px !important;
    padding: 8px !important;
  }
  [data-testid="stMetricLabel"] { color: rgba(200,230,255,0.5) !important; font-size: 0.65rem !important; }
  [data-testid="stMetricValue"] { color: #00e5ff !important; font-family: 'Courier New', monospace !important; }

  /* Hide Streamlit branding */
  #MainMenu, footer, header { visibility: hidden; }

  /* Info boxes */
  .info-box {
    background: rgba(0,229,255,0.04);
    border: 1px solid rgba(0,229,255,0.15);
    border-radius: 6px;
    padding: 10px 14px;
    font-family: 'Courier New', monospace;
    font-size: 0.65rem;
    color: rgba(200,230,255,0.6);
    letter-spacing: 1px;
    line-height: 1.7;
    margin-bottom: 10px;
  }
  .info-box span { color: #00e5ff; }
  .emergency-box {
    background: rgba(255,60,0,0.06);
    border: 1px solid rgba(255,80,0,0.3);
    border-radius: 6px;
    padding: 10px 14px;
    font-family: 'Courier New', monospace;
    font-size: 0.65rem;
    color: rgba(255,150,80,0.8);
    letter-spacing: 1px;
    margin-bottom: 8px;
  }
  .clear-btn > button {
    border-color: rgba(0,229,255,0.3) !important;
    color: #00e5ff !important;
  }
  .clear-btn > button:hover {
    background: rgba(0,229,255,0.08) !important;
    box-shadow: 0 0 8px rgba(0,229,255,0.2) !important;
  }
</style>
""", unsafe_allow_html=True)

# ── Load embedded HTML ──────────────────────────────────────────────────────────
HTML_PATH = pathlib.Path(__file__).parent / "traffic_sim_embed.html"
if not HTML_PATH.exists():
    st.error(f"❌ Could not find `traffic_sim_embed.html` next to this script.\nExpected at: {HTML_PATH}")
    st.stop()

html_source = HTML_PATH.read_text(encoding="utf-8")

# ── Session state defaults ──────────────────────────────────────────────────────
if "emergency" not in st.session_state:
    st.session_state.emergency = None
for road in ["north", "south", "west"]:
    if f"vol_{road}" not in st.session_state:
        st.session_state[f"vol_{road}"] = 5

# ── Sidebar controls ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-title">⬡ TRAFFIC JUNCTION CONTROL</div>', unsafe_allow_html=True)

    # Volume controls
    st.markdown("**TRAFFIC VOLUME**")

    road_meta = {
        "north": {"icon": "↑", "label": "NORTH", "css": "north"},
        "south": {"icon": "↓", "label": "SOUTH", "css": "south"},
        "west":  {"icon": "←", "label": "WEST",  "css": "west"},
    }

    volumes = {}
    for road, meta in road_meta.items():
        with st.container():
            st.markdown(f'<div class="road-section {meta["css"]}">', unsafe_allow_html=True)
            vol = st.slider(
                f"{meta['icon']} {meta['label']}",
                min_value=1, max_value=10,
                value=st.session_state[f"vol_{road}"],
                key=f"slider_{road}",
                help=f"Traffic volume on {meta['label']} road (affects green light duration)"
            )
            st.session_state[f"vol_{road}"] = vol
            volumes[road] = vol
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**🚨 EMERGENCY VEHICLE**")

    emg_road = st.selectbox(
        "Select Road",
        options=["None", "North", "South", "West"],
        index=0 if st.session_state.emergency is None
              else ["None","North","South","West"].index(st.session_state.emergency.capitalize()),
        key="emg_select"
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚨 DISPATCH", key="btn_emg"):
            if emg_road != "None":
                st.session_state.emergency = emg_road.lower()
                st.rerun()

    with col2:
        if st.button("✕ CLEAR", key="btn_clear"):
            st.session_state.emergency = None
            st.rerun()

    # Emergency status
    if st.session_state.emergency:
        st.markdown(
            f'<div class="emergency-box">🚨 EMERGENCY ACTIVE<br>ROAD: {st.session_state.emergency.upper()}<br>STATUS: PRIORITY GRANTED</div>',
            unsafe_allow_html=True
        )

    st.markdown("---")

    # Info
    st.markdown('<div class="info-box">'
                '<span>ADAPTIVE MODE</span><br>'
                'Signal timing adapts to traffic volume.<br>'
                'High volume = longer green phase.<br><br>'
                'Range: <span>5s – 18s</span> per phase<br>'
                'Yellow: <span>2.5s</span> always<br>'
                'Emergency: <span>immediate</span> priority'
                '</div>', unsafe_allow_html=True)

# ── Build JavaScript config payload ────────────────────────────────────────────
config_payload = {
    "type": "config",
    "volumes": volumes,
    "emergency": st.session_state.emergency,
}

# Inject auto-send script into the HTML
inject_script = f"""
<script>
(function() {{
  const iframe = document.querySelector('iframe[title="traffic-sim"]');
  function sendConfig() {{
    if (iframe && iframe.contentWindow) {{
      iframe.contentWindow.postMessage({json.dumps(config_payload)}, '*');
    }} else {{
      setTimeout(sendConfig, 200);
    }}
  }}
  // Send after iframe loads
  if (iframe) {{
    iframe.addEventListener('load', sendConfig);
    sendConfig();
  }} else {{
    setTimeout(sendConfig, 500);
  }}
}})();
</script>
"""

# ── Main area header ────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:4px 0 12px;font-family:'Courier New',monospace;
font-size:0.65rem;letter-spacing:3px;color:rgba(0,229,255,0.5);">
⬡ &nbsp; SMART CITY AI TRAFFIC SIGNAL &nbsp; ⬡ &nbsp; REAL-TIME SIGNAL OPTIMIZATION
</div>
""", unsafe_allow_html=True)

# ── Render iframe with simulation ──────────────────────────────────────────────
# We embed the full HTML directly in a components iframe
from streamlit.components.v1 import html as st_html

# Build final HTML: inject a postMessage sender that fires when iframe loads
# We render the simulation HTML directly (it already has postMessage receiver)

# Wrap with config-sender: after the page loads, it messages itself from parent
full_html = html_source.replace(
    "</body>",
    f"""
<script>
// Auto-apply config sent from Streamlit parent on load
window.addEventListener('load', function() {{
  const cfg = {json.dumps(config_payload)};
  // Apply directly since we're in the same page
  const vols = cfg.volumes;
  if(vols) Object.assign(volumes, vols);
  if(cfg.emergency) {{
    state.emergency = cfg.emergency;
    state.emergencyHandled = false;
    document.getElementById('emg-overlay').className='emergency-overlay active';
  }} else {{
    state.emergency = null;
    state.emergencyHandled = false;
    var overlay = document.getElementById('emg-overlay');
    if(overlay) overlay.className='emergency-overlay';
  }}
}});
</script>
</body>"""
)

st_html(full_html, height=700, scrolling=False)

# ── Live stats display (Streamlit-side) ────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<div style="font-family:Courier New,monospace;font-size:0.6rem;letter-spacing:2px;'
    'color:rgba(0,229,255,0.4);text-align:center;padding-bottom:4px;">CURRENT CONFIGURATION</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)
with col1:
    vol_n = volumes.get("north", 5)
    st.metric("↑ NORTH VOLUME", f"{vol_n}/10",
              delta=f"~{int(5 + ((vol_n-1)/9)*13)}s green")
with col2:
    vol_s = volumes.get("south", 5)
    st.metric("↓ SOUTH VOLUME", f"{vol_s}/10",
              delta=f"~{int(5 + ((vol_s-1)/9)*13)}s green")
with col3:
    vol_w = volumes.get("west", 5)
    st.metric("← WEST VOLUME", f"{vol_w}/10",
              delta=f"~{int(5 + ((vol_w-1)/9)*13)}s green")
with col4:
    emg_display = st.session_state.emergency.upper() if st.session_state.emergency else "NONE"
    st.metric("🚨 EMERGENCY", emg_display)

# ── How it works ───────────────────────────────────────────────────────────────
with st.expander("📡 HOW IT WORKS", expanded=False):
    st.markdown("""
    <div style="font-family:'Courier New',monospace;font-size:0.7rem;color:rgba(200,230,255,0.7);line-height:1.8;">

    - Traffic cameras capture real-time video at intersections.
    - Computer Vision techniques are applied for vehicle detection and lane-wise counting.
    - Machine Learning models analyze traffic density and predict optimal green signal duration.
    - Emergency vehicles are identified using visual cues or priority signaling.
    - The traffic signal controller dynamically updates signal phases in real time. 



    

    </div>
    """, unsafe_allow_html=True)
