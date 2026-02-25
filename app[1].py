"""
AI-Enabled Smart Traffic Light Signal
======================================
Run:  streamlit run app.py
Deps: pip install streamlit
"""

import json
import pathlib
import streamlit as st
from streamlit.components.v1 import html as st_html

# ── Page setup ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI-Enabled Smart Traffic Light Signal",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Inject CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Fonts & base ── */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Share+Tech+Mono&display=swap');

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stHeader"],
[data-testid="stToolbar"]          { background:#020812 !important; }

[data-testid="stSidebar"],
[data-testid="stSidebar"] > div    {
    background: #030d20 !important;
    border-right: 1px solid rgba(0,229,255,0.15) !important;
}
[data-testid="stSidebarContent"]   { padding-top: 0 !important; }
section.main > div                 { padding-top: 0 !important; }

/* hide default Streamlit chrome */
#MainMenu, footer, header          { visibility: hidden; }

/* ── Sidebar: all text ── */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div      { color: #c8e6ff !important; font-family:'Share Tech Mono',monospace !important; }

/* ── Sidebar: slider track ── */
[data-testid="stSidebar"] [data-testid="stSlider"] > div > div > div {
    background: rgba(0,229,255,0.22) !important;
}
/* thumb */
[data-testid="stSidebar"] [data-testid="stSlider"] input[type=range]::-webkit-slider-thumb {
    background: #00e5ff !important;
    box-shadow: 0 0 8px rgba(0,229,255,0.7) !important;
}

/* ── Sidebar: selectbox ── */
[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {
    background: rgba(0,10,30,0.8) !important;
    border: 1px solid rgba(0,229,255,0.25) !important;
    color: #c8e6ff !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.75rem !important;
}

/* ── Sidebar: buttons (emergency) ── */
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: 1px solid rgba(255,80,0,0.45) !important;
    color: rgba(255,160,80,0.9) !important;
    font-family: 'Share Tech Mono', monospace !important;
    letter-spacing: 2px !important;
    font-size: 0.62rem !important;
    width: 100% !important;
    border-radius: 5px !important;
    padding: 7px 0 !important;
    transition: all 0.2s !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,80,0,0.15) !important;
    border-color: #ff5000 !important;
    color: #ff9050 !important;
    box-shadow: 0 0 10px rgba(255,80,0,0.35) !important;
}

/* clear / reset buttons */
[data-testid="stSidebar"] .btn-clear button,
[data-testid="stSidebar"] .btn-reset button {
    border-color: rgba(0,229,255,0.3) !important;
    color: rgba(0,229,255,0.75) !important;
}
[data-testid="stSidebar"] .btn-clear button:hover,
[data-testid="stSidebar"] .btn-reset button:hover {
    background: rgba(0,229,255,0.08) !important;
    box-shadow: 0 0 8px rgba(0,229,255,0.2) !important;
}

/* ── Metrics (main area) ── */
[data-testid="stMetric"] {
    background: rgba(0,229,255,0.04) !important;
    border: 1px solid rgba(0,229,255,0.13) !important;
    border-radius: 8px !important;
    padding: 10px 14px !important;
}
[data-testid="stMetricLabel"] { color: rgba(200,230,255,0.45) !important; font-size: 0.62rem !important; letter-spacing:1px; }
[data-testid="stMetricValue"] { color: #00e5ff !important; font-family:'Orbitron',monospace !important; font-size:1.05rem !important; }
[data-testid="stMetricDelta"] { font-size: 0.6rem !important; }

/* ── Expander ── */
details, [data-testid="stExpander"] {
    background: rgba(0,229,255,0.02) !important;
    border: 1px solid rgba(0,229,255,0.1) !important;
    border-radius: 6px !important;
}
[data-testid="stExpander"] summary {
    color: rgba(0,229,255,0.55) !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 2px;
}

/* ── HR divider ── */
hr { border-color: rgba(0,229,255,0.08) !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #020812; }
::-webkit-scrollbar-thumb { background: rgba(0,229,255,0.2); border-radius: 2px; }
</style>
""", unsafe_allow_html=True)

# ── Load simulation HTML ────────────────────────────────────────────────────────
HTML_PATH = pathlib.Path(__file__).parent / "traffic_sim_embed.html"
if not HTML_PATH.exists():
    st.error(f"❌ `traffic_sim_embed.html` not found at: {HTML_PATH}")
    st.stop()
html_source = HTML_PATH.read_text(encoding="utf-8")

# ── Session state ──────────────────────────────────────────────────────────────
if "emergency" not in st.session_state:
    st.session_state.emergency = None
for r in ["north", "south", "west"]:
    if f"vol_{r}" not in st.session_state:
        st.session_state[f"vol_{r}"] = 5


# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:

    # ── Panel title ─────────────────────────────────────────────────────────
    st.markdown("""
    <div style="
        text-align:center;
        font-family:'Orbitron',monospace;
        font-size:0.6rem;
        letter-spacing:3px;
        color:#00e5ff;
        padding:14px 0 10px;
        border-bottom:1px solid rgba(0,229,255,0.18);
        margin-bottom:16px;
        text-shadow:0 0 14px rgba(0,229,255,0.4);
    ">⬡ &nbsp; SIGNAL CONTROL PANEL &nbsp; ⬡</div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════
    #  SECTION 1 — TRAFFIC VOLUME
    # ══════════════════════════════════════════════════════
    st.markdown("""
    <div style="font-family:'Orbitron',monospace;font-size:0.52rem;letter-spacing:3px;
    color:rgba(0,229,255,0.65);border-bottom:1px solid rgba(0,229,255,0.1);
    padding-bottom:6px;margin-bottom:12px;">
    📊 &nbsp; TRAFFIC VOLUME CONTROL
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style="font-size:0.58rem;color:rgba(200,230,255,0.38);margin:0 0 12px;line-height:1.7;">
    Set vehicle density per road.<br>Higher value → longer green phase.
    </p>
    """, unsafe_allow_html=True)

    # ── Road configs ──
    road_cfg = {
        "north": {"arrow": "↑", "label": "NORTH ROAD", "color": "#00ff88", "dim": "#006633"},
        "south": {"arrow": "↓", "label": "SOUTH ROAD", "color": "#00aaff", "dim": "#004477"},
        "west":  {"arrow": "←", "label": "WEST ROAD",  "color": "#bb77ff", "dim": "#551188"},
    }

    volumes = {}
    for road, cfg in road_cfg.items():
        # Slider
        vol = st.slider(
            f"{cfg['arrow']}  {cfg['label']}",
            min_value=1, max_value=10,
            value=st.session_state[f"vol_{road}"],
            key=f"sl_{road}",
        )
        st.session_state[f"vol_{road}"] = vol
        volumes[road] = vol

        # Animated fill bar
        pct  = int(vol / 10 * 100)
        gdur = int(5 + (vol - 1) / 9 * 13)
        c, d = cfg["color"], cfg["dim"]
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;
                    font-size:0.55rem;color:rgba(200,230,255,0.35);
                    margin:-4px 0 3px;">
            <span>DENSITY &nbsp; {vol}/10</span>
            <span style="color:{c};">~{gdur}s GREEN</span>
        </div>
        <div style="height:5px;background:rgba(255,255,255,0.05);border-radius:3px;
                    margin-bottom:14px;overflow:hidden;">
            <div style="height:100%;width:{pct}%;border-radius:3px;
                        background:linear-gradient(90deg,{d},{c});
                        box-shadow:0 0 8px {c}44;transition:width .4s;"></div>
        </div>
        """, unsafe_allow_html=True)

    # Green duration summary card
    nd = int(5 + (volumes["north"]-1)/9*13)
    sd = int(5 + (volumes["south"]-1)/9*13)
    wd = int(5 + (volumes["west"]-1)/9*13)
    st.markdown(f"""
    <div style="background:rgba(0,229,255,0.04);border:1px solid rgba(0,229,255,0.1);
                border-radius:6px;padding:9px 12px;font-size:0.58rem;
                color:rgba(200,230,255,0.4);line-height:2.0;margin-bottom:6px;">
        <div style="color:rgba(0,229,255,0.6);font-family:'Orbitron',monospace;
                    font-size:0.5rem;letter-spacing:2px;margin-bottom:4px;">
            GREEN PHASE DURATIONS
        </div>
        ↑ North &nbsp;→&nbsp; <span style="color:#00ff88;font-weight:bold;">~{nd}s</span>
        &nbsp;&nbsp;
        ↓ South &nbsp;→&nbsp; <span style="color:#00aaff;font-weight:bold;">~{sd}s</span>
        &nbsp;&nbsp;
        ← West &nbsp;→&nbsp; <span style="color:#bb77ff;font-weight:bold;">~{wd}s</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ══════════════════════════════════════════════════════
    #  SECTION 2 — EMERGENCY VEHICLE
    # ══════════════════════════════════════════════════════
    st.markdown("""
    <div style="font-family:'Orbitron',monospace;font-size:0.52rem;letter-spacing:3px;
    color:rgba(255,120,40,0.75);border-bottom:1px solid rgba(255,80,0,0.15);
    padding-bottom:6px;margin-bottom:12px;">
    🚨 &nbsp; EMERGENCY VEHICLE DISPATCH
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style="font-size:0.58rem;color:rgba(200,230,255,0.38);margin:0 0 10px;line-height:1.7;">
    Dispatch instantly overrides the current cycle<br>
    and forces a <span style="color:#ff8040;">GREEN signal</span> on that road.
    </p>
    """, unsafe_allow_html=True)

    # Quick-dispatch 3 buttons
    st.markdown("""
    <div style="font-size:0.5rem;letter-spacing:2px;color:rgba(200,230,255,0.25);
                margin-bottom:6px;">QUICK DISPATCH</div>
    """, unsafe_allow_html=True)

    q1, q2, q3 = st.columns(3)
    with q1:
        if st.button("↑ N", key="qn", help="Emergency on North road"):
            st.session_state.emergency = "north"
            st.rerun()
    with q2:
        if st.button("↓ S", key="qs", help="Emergency on South road"):
            st.session_state.emergency = "south"
            st.rerun()
    with q3:
        if st.button("← W", key="qw", help="Emergency on West road"):
            st.session_state.emergency = "west"
            st.rerun()

    # Manual selector
    st.markdown("""
    <div style="font-size:0.5rem;letter-spacing:2px;color:rgba(200,230,255,0.25);
                margin:10px 0 5px;">MANUAL SELECTION</div>
    """, unsafe_allow_html=True)

    emg_opts = ["— None —", "North ↑", "South ↓", "West ←"]
    emg_map  = {"North ↑": "north", "South ↓": "south", "West ←": "west"}
    cur_idx  = 0
    if st.session_state.emergency:
        cur_idx = {"north":1,"south":2,"west":3}.get(st.session_state.emergency, 0)

    chosen = st.selectbox(
        "Road",
        options=emg_opts,
        index=cur_idx,
        key="emg_sel",
        label_visibility="collapsed",
    )

    d1, d2 = st.columns([3, 2])
    with d1:
        if st.button("🚨  DISPATCH", key="btn_dispatch"):
            if chosen != "— None —":
                st.session_state.emergency = emg_map[chosen]
                st.rerun()
    with d2:
        st.markdown('<div class="btn-clear">', unsafe_allow_html=True)
        if st.button("✕ CLEAR", key="btn_clear"):
            st.session_state.emergency = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Status badge
    if st.session_state.emergency:
        icons = {"north": "↑", "south": "↓", "west": "←"}
        ic = icons[st.session_state.emergency]
        st.markdown(f"""
        <div style="
            background:rgba(255,50,0,0.09);
            border:1px solid rgba(255,80,0,0.5);
            border-radius:7px;padding:10px 12px;
            font-size:0.62rem;color:rgba(255,160,80,0.9);
            line-height:1.9;margin-top:8px;
            animation:epulse 1.1s infinite alternate;
        ">
            🚨 &nbsp;<b>EMERGENCY ACTIVE</b><br>
            ROAD &nbsp;&nbsp;&nbsp;: &nbsp;{ic} {st.session_state.emergency.upper()}<br>
            STATUS &nbsp;: PRIORITY GRANTED<br>
            SIGNAL &nbsp;: FORCED GREEN ✅
        </div>
        <style>
        @keyframes epulse{{
            from{{box-shadow:none;border-color:rgba(255,80,0,0.3);}}
            to{{box-shadow:0 0 18px rgba(255,80,0,0.25);border-color:rgba(255,80,0,0.8);}}
        }}
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="
            background:rgba(0,255,136,0.03);
            border:1px solid rgba(0,255,136,0.14);
            border-radius:7px;padding:9px 12px;
            font-size:0.6rem;color:rgba(0,255,136,0.5);
            margin-top:8px;letter-spacing:1px;
        ">✓ &nbsp; NO EMERGENCY · NORMAL CYCLE</div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ══════════════════════════════════════════════════════
    #  SECTION 3 — SYSTEM STATUS
    # ══════════════════════════════════════════════════════
    st.markdown("""
    <div style="font-family:'Orbitron',monospace;font-size:0.52rem;letter-spacing:3px;
    color:rgba(0,229,255,0.65);border-bottom:1px solid rgba(0,229,255,0.1);
    padding-bottom:6px;margin-bottom:10px;">
    ⚙ &nbsp; SYSTEM STATUS
    </div>
    """, unsafe_allow_html=True)

    mode_color = "#ff8040" if st.session_state.emergency else "#00e5ff"
    mode_label = "EMERGENCY" if st.session_state.emergency else "ADAPTIVE"
    peak_road  = max(volumes, key=volumes.get)
    peak_color = {"north":"#00ff88","south":"#00aaff","west":"#bb77ff"}[peak_road]

    st.markdown(f"""
    <div style="
        background:rgba(0,229,255,0.03);
        border:1px solid rgba(0,229,255,0.1);
        border-radius:6px;padding:10px 13px;
        font-size:0.6rem;color:rgba(200,230,255,0.45);
        line-height:2.0;
    ">
        <b style="color:rgba(0,229,255,0.6);">MODE</b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;:
            <span style="color:{mode_color};">{mode_label}</span><br>
        <b style="color:rgba(0,229,255,0.6);">PEAK ROAD</b> :
            <span style="color:{peak_color};">{peak_road.upper()} (vol {volumes[peak_road]})</span><br>
        <b style="color:rgba(0,229,255,0.6);">YELLOW</b> &nbsp;&nbsp;&nbsp;: 2.5s fixed<br>
        <b style="color:rgba(0,229,255,0.6);">ALL-RED</b> &nbsp;&nbsp;: 0.3s buffer<br>
        <b style="color:rgba(0,229,255,0.6);">SEQUENCE</b> &nbsp;: N → S → W → …<br>
        <b style="color:rgba(0,229,255,0.6);">PRIORITY</b> &nbsp;: highest volume next
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;font-size:0.5rem;letter-spacing:2px;
                color:rgba(0,229,255,0.18);padding-top:16px;">
    AI SIGNAL SYSTEM v2.0
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN AREA
# ══════════════════════════════════════════════════════════════════════════════

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:10px 0 8px;
            border-bottom:1px solid rgba(0,229,255,0.08);margin-bottom:10px;">
    <div style="font-family:'Orbitron',monospace;font-size:1.05rem;
                letter-spacing:4px;color:#00e5ff;
                text-shadow:0 0 24px rgba(0,229,255,0.35);margin-bottom:4px;">
        AI-ENABLED SMART TRAFFIC LIGHT SIGNAL
    </div>
    <div style="font-size:0.58rem;letter-spacing:3px;color:rgba(0,229,255,0.3);">
        ⬡ &nbsp; REAL-TIME ADAPTIVE CONTROL &nbsp; · &nbsp; COMPUTER VISION + ML &nbsp; ⬡
    </div>
</div>
""", unsafe_allow_html=True)

# ── Build config & inject into simulation HTML ─────────────────────────────────
config_payload = {
    "type": "config",
    "volumes": volumes,
    "emergency": st.session_state.emergency,
}

full_html = html_source.replace(
    "</body>",
    f"""
<script>
window.addEventListener('load', function() {{
  var cfg = {json.dumps(config_payload)};
  if (cfg.volumes) Object.assign(volumes, cfg.volumes);
  if (cfg.emergency) {{
    state.emergency = cfg.emergency;
    state.emgHandled = false;
    var o = document.getElementById('emg-ov');
    if (o) o.className = 'emg-ov on';
  }} else {{
    state.emergency = null;
    state.emgHandled = false;
    var o = document.getElementById('emg-ov');
    if (o) o.className = 'emg-ov';
  }}
}});
</script>
</body>""",
)

# ── Render simulation ──────────────────────────────────────────────────────────
st_html(full_html, height=640, scrolling=False)

# ── Live metrics row ───────────────────────────────────────────────────────────
st.markdown("""
<div style="font-size:0.55rem;letter-spacing:2px;color:rgba(0,229,255,0.28);
            text-align:center;padding:6px 0 4px;">
▸ LIVE CONFIGURATION SNAPSHOT
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4, c5 = st.columns(5)
vn, vs, vw = volumes["north"], volumes["south"], volumes["west"]
busiest = max(volumes, key=volumes.get)

with c1: st.metric("↑ NORTH",    f"{vn}/10",  delta=f"~{int(5+(vn-1)/9*13)}s green")
with c2: st.metric("↓ SOUTH",    f"{vs}/10",  delta=f"~{int(5+(vs-1)/9*13)}s green")
with c3: st.metric("← WEST",     f"{vw}/10",  delta=f"~{int(5+(vw-1)/9*13)}s green")
with c4:
    emg_v = st.session_state.emergency.upper() if st.session_state.emergency else "NONE"
    st.metric("🚨 EMERGENCY", emg_v, delta="PRIORITY ACTIVE" if st.session_state.emergency else "Normal mode")
with c5:
    st.metric("⚡ PEAK ROAD", busiest.upper(), delta=f"vol {volumes[busiest]}/10")

# ── How it works ───────────────────────────────────────────────────────────────
st.markdown("---")
with st.expander("📡  HOW IT WORKS", expanded=False):
    st.markdown("""
    <div style="font-family:'Share Tech Mono',monospace;font-size:0.72rem;
                color:rgba(200,230,255,0.75);line-height:2.3;padding:4px 2px;">
    <span style="color:#00e5ff;font-size:1rem;">📷</span>
    &nbsp; Traffic cameras capture real-time video at intersections.<br><br>
    <span style="color:#00e5ff;font-size:1rem;">🔍</span>
    &nbsp; Computer vision techniques are applied for vehicle detection and lane-wise counting.<br><br>
    <span style="color:#00e5ff;font-size:1rem;">🤖</span>
    &nbsp; Machine learning models analyze traffic density and predict optimal green signal duration.<br><br>
    <span style="color:#00e5ff;font-size:1rem;">🚨</span>
    &nbsp; Emergency vehicles are identified using visual cues or priority signaling.<br><br>
    <span style="color:#00e5ff;font-size:1rem;">⚡</span>
    &nbsp; The traffic signal controller dynamically updates signal phases in real time.
    </div>
    """, unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:18px 0 8px;
            border-top:1px solid rgba(0,229,255,0.07);margin-top:6px;
            font-family:'Share Tech Mono',monospace;font-size:0.65rem;
            letter-spacing:2px;color:rgba(0,229,255,0.28);">
    ⬡ &nbsp; Made by <span style="color:#00e5ff;letter-spacing:3px;">Aman Kumar</span> &nbsp; ⬡
</div>
""", unsafe_allow_html=True)
