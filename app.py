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
    initial_sidebar_state="collapsed",   # hide sidebar entirely — controls are inline
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Share+Tech+Mono&display=swap');

/* ── Dark base ── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"]        { background: #020812 !important; }

section.main > div                  { padding-top: 6px !important; padding-bottom: 0 !important; }

/* Hide Streamlit chrome */
#MainMenu, footer, header,
[data-testid="stSidebar"],
[data-testid="collapsedControl"]    { display: none !important; visibility: hidden !important; }

/* ── Global font ── */
*, p, label, div, span, li         { font-family: 'Share Tech Mono', monospace !important; color: #c8e6ff; }
h1, h2, h3, h4                     { font-family: 'Orbitron', monospace !important; color: #00e5ff !important; }

/* ── Slider ── */
[data-testid="stSlider"] > div > div > div {
    background: rgba(0,229,255,0.2) !important;
}
[data-testid="stSlider"] input[type=range]::-webkit-slider-thumb {
    background: #00e5ff !important;
    box-shadow: 0 0 8px rgba(0,229,255,0.7) !important;
    width: 16px !important; height: 16px !important;
}
[data-testid="stSlider"] label { font-size: 0.7rem !important; color: #c8e6ff !important; }

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {
    background: rgba(0,10,30,0.9) !important;
    border: 1px solid rgba(0,229,255,0.28) !important;
    color: #c8e6ff !important;
    font-size: 0.72rem !important;
}

/* ── Emergency dispatch buttons ── */
.stButton > button {
    background: transparent !important;
    border: 1px solid rgba(255,80,0,0.5) !important;
    color: rgba(255,160,80,0.95) !important;
    font-family: 'Share Tech Mono', monospace !important;
    letter-spacing: 2px !important;
    font-size: 0.65rem !important;
    width: 100% !important;
    border-radius: 5px !important;
    padding: 8px 4px !important;
    transition: all 0.2s !important;
    cursor: pointer !important;
}
.stButton > button:hover {
    background: rgba(255,80,0,0.18) !important;
    border-color: #ff5000 !important;
    color: #ff9050 !important;
    box-shadow: 0 0 12px rgba(255,80,0,0.4) !important;
}

/* Clear / neutral buttons */
.btn-clear button, .btn-reset button {
    border-color: rgba(0,229,255,0.32) !important;
    color: rgba(0,229,255,0.8) !important;
}
.btn-clear button:hover, .btn-reset button:hover {
    background: rgba(0,229,255,0.09) !important;
    box-shadow: 0 0 8px rgba(0,229,255,0.25) !important;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: rgba(0,229,255,0.04) !important;
    border: 1px solid rgba(0,229,255,0.14) !important;
    border-radius: 8px !important;
    padding: 10px 12px !important;
}
[data-testid="stMetricLabel"] { color: rgba(200,230,255,0.45) !important; font-size: 0.6rem !important; letter-spacing:1px; }
[data-testid="stMetricValue"] { color: #00e5ff !important; font-family:'Orbitron',monospace !important; font-size:1rem !important; }
[data-testid="stMetricDelta"]  { font-size: 0.58rem !important; }

/* ── Expander ── */
[data-testid="stExpander"] {
    background: rgba(0,229,255,0.02) !important;
    border: 1px solid rgba(0,229,255,0.1) !important;
    border-radius: 6px !important;
}
[data-testid="stExpander"] summary {
    color: rgba(0,229,255,0.55) !important;
    font-size: 0.7rem !important; letter-spacing:2px;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #020812; }
::-webkit-scrollbar-thumb { background: rgba(0,229,255,0.18); border-radius:2px; }

/* ── HR ── */
hr { border-color: rgba(0,229,255,0.08) !important; }

/* ── Control panel card ── */
.ctrl-card {
    background: linear-gradient(180deg, #050e22 0%, #030b1c 100%);
    border: 1px solid rgba(0,229,255,0.16);
    border-radius: 10px;
    padding: 18px 16px;
    height: 100%;
}
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
#  PAGE HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div style="text-align:center;padding:10px 0 8px;
            border-bottom:1px solid rgba(0,229,255,0.1);margin-bottom:14px;">
    <div style="font-family:'Orbitron',monospace;font-size:1.15rem;
                letter-spacing:4px;color:#00e5ff;
                text-shadow:0 0 28px rgba(0,229,255,0.4);margin-bottom:5px;">
        🚦 &nbsp; AI-ENABLED SMART TRAFFIC LIGHT SIGNAL
    </div>
    <div style="font-size:0.6rem;letter-spacing:3px;color:rgba(0,229,255,0.32);">
        ⬡ &nbsp; REAL-TIME ADAPTIVE CONTROL &nbsp;·&nbsp; COMPUTER VISION + ML &nbsp; ⬡
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  MAIN TWO-COLUMN LAYOUT  (controls | simulation)
# ══════════════════════════════════════════════════════════════════════════════
left_col, right_col = st.columns([1, 2.2], gap="large")

# ─────────────────────────────────────────────────────
#  LEFT — CONTROL PANEL
# ─────────────────────────────────────────────────────
with left_col:

    # Panel header
    st.markdown("""
    <div style="font-family:'Orbitron',monospace;font-size:0.6rem;letter-spacing:3px;
                color:#00e5ff;text-align:center;padding:10px 0 8px;
                border-bottom:1px solid rgba(0,229,255,0.18);margin-bottom:14px;
                text-shadow:0 0 12px rgba(0,229,255,0.35);">
        ⬡ &nbsp; SIGNAL CONTROL PANEL &nbsp; ⬡
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════
    #  SECTION 1 — TRAFFIC VOLUME
    # ══════════════════════════════════════════════
    st.markdown("""
    <div style="font-family:'Orbitron',monospace;font-size:0.52rem;letter-spacing:3px;
                color:rgba(0,229,255,0.7);border-bottom:1px solid rgba(0,229,255,0.12);
                padding-bottom:5px;margin-bottom:10px;">
        📊 &nbsp; TRAFFIC VOLUME
    </div>
    <p style="font-size:0.58rem;color:rgba(200,230,255,0.35);margin:0 0 10px;line-height:1.6;">
        Higher value → longer green phase (5s – 18s).
    </p>
    """, unsafe_allow_html=True)

    road_cfg = {
        "north": {"arrow": "↑", "label": "NORTH ROAD", "color": "#00ff88", "dim": "#005533"},
        "south": {"arrow": "↓", "label": "SOUTH ROAD", "color": "#00aaff", "dim": "#003366"},
        "west":  {"arrow": "←", "label": "WEST ROAD",  "color": "#bb77ff", "dim": "#440077"},
    }

    volumes = {}
    for road, cfg in road_cfg.items():
        vol = st.slider(
            f"{cfg['arrow']}  {cfg['label']}",
            min_value=1, max_value=10,
            value=st.session_state[f"vol_{road}"],
            key=f"sl_{road}",
        )
        st.session_state[f"vol_{road}"] = vol
        volumes[road] = vol

        pct  = int(vol / 10 * 100)
        gdur = int(5 + (vol - 1) / 9 * 13)
        c, d = cfg["color"], cfg["dim"]

        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;
                    font-size:0.56rem;color:rgba(200,230,255,0.35);
                    margin:-6px 0 3px;">
            <span>DENSITY &nbsp;{vol}/10</span>
            <span style="color:{c};">~{gdur}s GREEN</span>
        </div>
        <div style="height:6px;background:rgba(255,255,255,0.05);border-radius:3px;
                    margin-bottom:14px;overflow:hidden;">
            <div style="height:100%;width:{pct}%;border-radius:3px;
                        background:linear-gradient(90deg,{d},{c});
                        box-shadow:0 0 10px {c}55;"></div>
        </div>
        """, unsafe_allow_html=True)

    # Summary
    nd = int(5 + (volumes["north"]-1)/9*13)
    sd = int(5 + (volumes["south"]-1)/9*13)
    wd = int(5 + (volumes["west"]-1)/9*13)
    st.markdown(f"""
    <div style="background:rgba(0,229,255,0.04);border:1px solid rgba(0,229,255,0.1);
                border-radius:7px;padding:10px 12px;font-size:0.58rem;
                color:rgba(200,230,255,0.4);line-height:2.0;margin-bottom:6px;">
        <div style="color:rgba(0,229,255,0.6);font-family:'Orbitron',monospace;
                    font-size:0.48rem;letter-spacing:2px;margin-bottom:5px;">
            GREEN DURATIONS
        </div>
        ↑ North → <span style="color:#00ff88;font-weight:bold;">~{nd}s</span><br>
        ↓ South → <span style="color:#00aaff;font-weight:bold;">~{sd}s</span><br>
        ← West &nbsp;→ <span style="color:#bb77ff;font-weight:bold;">~{wd}s</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ══════════════════════════════════════════════
    #  SECTION 2 — EMERGENCY VEHICLE
    # ══════════════════════════════════════════════
    st.markdown("""
    <div style="font-family:'Orbitron',monospace;font-size:0.52rem;letter-spacing:3px;
                color:rgba(255,120,50,0.8);border-bottom:1px solid rgba(255,80,0,0.18);
                padding-bottom:5px;margin-bottom:10px;">
        🚨 &nbsp; EMERGENCY DISPATCH
    </div>
    <p style="font-size:0.58rem;color:rgba(200,230,255,0.35);margin:0 0 10px;line-height:1.6;">
        Instantly forces GREEN on the chosen road.
    </p>
    """, unsafe_allow_html=True)

    # Quick-dispatch row
    st.markdown("""<div style="font-size:0.5rem;letter-spacing:2px;color:rgba(200,230,255,0.25);
                margin-bottom:6px;">⚡ QUICK DISPATCH</div>""", unsafe_allow_html=True)

    q1, q2, q3 = st.columns(3)
    with q1:
        if st.button("↑ NORTH", key="qn", use_container_width=True):
            st.session_state.emergency = "north"; st.rerun()
    with q2:
        if st.button("↓ SOUTH", key="qs", use_container_width=True):
            st.session_state.emergency = "south"; st.rerun()
    with q3:
        if st.button("← WEST", key="qw", use_container_width=True):
            st.session_state.emergency = "west"; st.rerun()

    st.markdown("""<div style="font-size:0.5rem;letter-spacing:2px;color:rgba(200,230,255,0.25);
                margin:10px 0 5px;">OR MANUAL SELECT</div>""", unsafe_allow_html=True)

    emg_opts = ["— None —", "North ↑", "South ↓", "West ←"]
    emg_map  = {"North ↑": "north", "South ↓": "south", "West ←": "west"}
    cur_idx  = 0
    if st.session_state.emergency:
        cur_idx = {"north":1,"south":2,"west":3}.get(st.session_state.emergency, 0)

    chosen = st.selectbox("Road", options=emg_opts, index=cur_idx,
                          key="emg_sel", label_visibility="collapsed")

    d1, d2 = st.columns([3, 2])
    with d1:
        if st.button("🚨  DISPATCH", key="btn_dispatch", use_container_width=True):
            if chosen != "— None —":
                st.session_state.emergency = emg_map[chosen]; st.rerun()
    with d2:
        st.markdown('<div class="btn-clear">', unsafe_allow_html=True)
        if st.button("✕ CLEAR", key="btn_clear", use_container_width=True):
            st.session_state.emergency = None; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Status badge
    if st.session_state.emergency:
        icons = {"north":"↑","south":"↓","west":"←"}
        ic = icons[st.session_state.emergency]
        st.markdown(f"""
        <div style="background:rgba(255,40,0,0.09);border:1px solid rgba(255,80,0,0.55);
                    border-radius:8px;padding:11px 13px;font-size:0.63rem;
                    color:rgba(255,165,80,0.95);line-height:2.0;margin-top:10px;
                    animation:ep 1.1s infinite alternate;">
            🚨 &nbsp;<b>EMERGENCY ACTIVE</b><br>
            ROAD &nbsp;&nbsp;&nbsp;: &nbsp;{ic} {st.session_state.emergency.upper()}<br>
            STATUS &nbsp;: PRIORITY GRANTED<br>
            SIGNAL &nbsp;: FORCED GREEN ✅
        </div>
        <style>
        @keyframes ep{{
            from{{box-shadow:none;border-color:rgba(255,80,0,0.3);}}
            to{{box-shadow:0 0 20px rgba(255,80,0,0.28);border-color:rgba(255,80,0,0.85);}}
        }}
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:rgba(0,255,136,0.04);border:1px solid rgba(0,255,136,0.15);
                    border-radius:8px;padding:10px 13px;font-size:0.62rem;
                    color:rgba(0,255,136,0.55);margin-top:10px;letter-spacing:1px;">
            ✓ &nbsp; NO EMERGENCY · NORMAL CYCLE
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ══════════════════════════════════════════════
    #  SECTION 3 — SYSTEM STATUS
    # ══════════════════════════════════════════════
    st.markdown("""
    <div style="font-family:'Orbitron',monospace;font-size:0.52rem;letter-spacing:3px;
                color:rgba(0,229,255,0.65);border-bottom:1px solid rgba(0,229,255,0.1);
                padding-bottom:5px;margin-bottom:10px;">
        ⚙ &nbsp; SYSTEM STATUS
    </div>
    """, unsafe_allow_html=True)

    mode_color = "#ff8040" if st.session_state.emergency else "#00e5ff"
    mode_label = "EMERGENCY" if st.session_state.emergency else "ADAPTIVE"
    peak_road  = max(volumes, key=volumes.get)
    peak_color = {"north":"#00ff88","south":"#00aaff","west":"#bb77ff"}[peak_road]

    st.markdown(f"""
    <div style="background:rgba(0,229,255,0.03);border:1px solid rgba(0,229,255,0.1);
                border-radius:7px;padding:11px 14px;font-size:0.62rem;
                color:rgba(200,230,255,0.45);line-height:2.1;">
        <b style="color:rgba(0,229,255,0.62);">MODE</b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;:
            <span style="color:{mode_color};">{mode_label}</span><br>
        <b style="color:rgba(0,229,255,0.62);">PEAK ROAD</b> :
            <span style="color:{peak_color};">{peak_road.upper()} (vol {volumes[peak_road]})</span><br>
        <b style="color:rgba(0,229,255,0.62);">YELLOW</b> &nbsp;&nbsp;&nbsp;&nbsp;: 2.5 s fixed<br>
        <b style="color:rgba(0,229,255,0.62);">ALL-RED</b> &nbsp;&nbsp;&nbsp;: 0.3 s buffer<br>
        <b style="color:rgba(0,229,255,0.62);">SEQUENCE</b> &nbsp;&nbsp;: N → S → W → …<br>
        <b style="color:rgba(0,229,255,0.62);">PRIORITY</b> &nbsp;&nbsp;: highest volume first
    </div>
    <div style="text-align:center;font-size:0.48rem;letter-spacing:2px;
                color:rgba(0,229,255,0.16);padding-top:14px;">
        AI SIGNAL SYSTEM v2.0
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
#  RIGHT — SIMULATION
# ─────────────────────────────────────────────────────
with right_col:

    # Build config payload & inject into simulation HTML
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

    st_html(full_html, height=640, scrolling=False)

# ══════════════════════════════════════════════════════════════════════════════
#  METRICS STRIP (below both columns)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div style="font-size:0.55rem;letter-spacing:2px;color:rgba(0,229,255,0.28);
            text-align:center;padding:8px 0 4px;border-top:1px solid rgba(0,229,255,0.07);">
    ▸ &nbsp; LIVE CONFIGURATION SNAPSHOT
</div>
""", unsafe_allow_html=True)

m1, m2, m3, m4, m5 = st.columns(5)
vn, vs, vw = volumes["north"], volumes["south"], volumes["west"]
busiest = max(volumes, key=volumes.get)

with m1: st.metric("↑ NORTH",    f"{vn}/10", delta=f"~{int(5+(vn-1)/9*13)}s green")
with m2: st.metric("↓ SOUTH",    f"{vs}/10", delta=f"~{int(5+(vs-1)/9*13)}s green")
with m3: st.metric("← WEST",     f"{vw}/10", delta=f"~{int(5+(vw-1)/9*13)}s green")
with m4:
    emg_v = st.session_state.emergency.upper() if st.session_state.emergency else "NONE"
    st.metric("🚨 EMERGENCY", emg_v,
              delta="PRIORITY ACTIVE" if st.session_state.emergency else "Normal mode")
with m5:
    st.metric("⚡ PEAK ROAD", busiest.upper(), delta=f"vol {volumes[busiest]}/10")

# ══════════════════════════════════════════════════════════════════════════════
#  HOW IT WORKS + FOOTER
# ══════════════════════════════════════════════════════════════════════════════
with st.expander("📡  HOW IT WORKS", expanded=False):
    st.markdown("""
    <div style="font-size:0.72rem;color:rgba(200,230,255,0.75);line-height:2.3;padding:4px 2px;">
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

st.markdown("""
<div style="text-align:center;padding:16px 0 6px;
            border-top:1px solid rgba(0,229,255,0.07);margin-top:8px;
            font-size:0.65rem;letter-spacing:2px;color:rgba(0,229,255,0.28);">
    ⬡ &nbsp; Made by <span style="color:#00e5ff;letter-spacing:3px;">Aman Kumar</span> &nbsp; ⬡
</div>
""", unsafe_allow_html=True)
