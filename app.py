import math
import random
import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="MOI QUEST | Aman Edge Physics", page_icon="◉", layout="wide", initial_sidebar_state="expanded")

# ---------- Visual system ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;600;700&display=swap');
:root{--bg:#080b12;--panel:#111827;--line:rgba(148,163,184,.18);--cyan:#55f6dc;--violet:#9a7bff;--muted:#9ba8bc;--white:#f4f7ff}
html,body,[class*="css"]{font-family:'Space Grotesk',sans-serif}
.stApp{background:radial-gradient(ellipse at 12% 0%,rgba(78,65,160,.19),transparent 35%),radial-gradient(ellipse at 88% 12%,rgba(28,202,180,.12),transparent 28%),var(--bg);color:var(--white);overflow:hidden}
.stApp:before{content:"";position:fixed;inset:-30%;pointer-events:none;z-index:0;background:
radial-gradient(ellipse at 18% 28%,rgba(85,246,220,.12) 0%,transparent 17%),
radial-gradient(ellipse at 78% 24%,rgba(154,123,255,.16) 0%,transparent 19%),
radial-gradient(ellipse at 62% 78%,rgba(54,130,255,.10) 0%,transparent 20%),
radial-gradient(ellipse at 28% 82%,rgba(255,73,173,.09) 0%,transparent 17%);
filter:blur(28px);animation:nebulaDrift 22s ease-in-out infinite alternate}
.stApp:after{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;opacity:.5;background-image:
radial-gradient(circle at 12% 22%,rgba(85,246,220,.85) 0 2px,transparent 3px),
radial-gradient(circle at 83% 34%,rgba(154,123,255,.9) 0 3px,transparent 4px),
radial-gradient(circle at 67% 78%,rgba(85,246,220,.8) 0 2px,transparent 3px),
radial-gradient(circle at 32% 67%,rgba(255,255,255,.7) 0 1px,transparent 2px),
radial-gradient(circle at 91% 82%,rgba(154,123,255,.9) 0 2px,transparent 3px),
radial-gradient(circle at 48% 16%,rgba(85,246,220,.8) 0 1px,transparent 2px);
animation:particleFlow 18s linear infinite}
@keyframes nebulaDrift{0%{transform:translate3d(-2%,-1%,0) rotate(0deg) scale(1)}100%{transform:translate3d(3%,2%,0) rotate(8deg) scale(1.08)}}
@keyframes particleFlow{0%{transform:translate3d(0,0,0)}50%{transform:translate3d(-1.5%,2%,0)}100%{transform:translate3d(1.5%,-2%,0)}}
.cosmic-layer{position:fixed;inset:0;width:100vw;height:100vh;overflow:hidden;pointer-events:none;z-index:0;opacity:.78}
.cosmic-layer svg{width:100%;height:100%;display:block}
.block-container,[data-testid="stSidebar"],[data-testid="stHeader"]{position:relative;z-index:1}
@media(prefers-reduced-motion:reduce){.stApp:before,.stApp:after{animation:none!important}.cosmic-layer{display:none}}
.block-container{max-width:1400px;padding-top:1.3rem;padding-bottom:2rem}
[data-testid="stSidebar"]{background:#0b101a;border-right:1px solid var(--line)}
[data-testid="stSidebar"] *{color:var(--white)}
h1,h2,h3{letter-spacing:-.04em}
h1{font-size:clamp(2.5rem,5vw,5rem)!important;line-height:.98!important}
p,li{color:#c7d1e1}
[data-testid="stMetric"]{background:linear-gradient(145deg,rgba(21,31,48,.9),rgba(13,19,31,.9));border:1px solid var(--line);padding:18px 20px;border-radius:18px}
[data-testid="stMetricLabel"]{color:var(--muted)}
[data-testid="stMetricValue"]{font-family:'DM Mono',monospace;color:var(--cyan)}
.stButton>button{border-radius:12px;border:1px solid rgba(85,246,220,.4);background:linear-gradient(120deg,rgba(85,246,220,.13),rgba(154,123,255,.16));color:#f7fbff;font-weight:700;min-height:2.8rem}
.stButton>button:hover{border-color:var(--cyan);color:var(--cyan);transform:translateY(-1px)}
.stRadio label,.stSelectbox label,.stSlider label{color:#dbe5f5}
hr{border-color:var(--line)}
.eyebrow{font-family:'DM Mono',monospace;font-size:.75rem;letter-spacing:.18em;text-transform:uppercase;color:var(--cyan)}
.hero{padding:2.2rem 2.4rem;border:1px solid var(--line);border-radius:28px;background:linear-gradient(125deg,rgba(21,30,48,.92),rgba(15,17,34,.86));position:relative;overflow:hidden}
.hero:after{content:'I = ∫ r² dm';position:absolute;right:3%;bottom:-.3em;font-family:Georgia,serif;font-size:clamp(3rem,8vw,8rem);color:rgba(255,255,255,.035);pointer-events:none}
.card{background:linear-gradient(145deg,rgba(18,27,43,.9),rgba(12,17,29,.94));border:1px solid var(--line);border-radius:20px;padding:1.2rem 1.35rem;height:100%}
.card h3{margin-top:.2rem}
.tag{display:inline-block;border:1px solid rgba(85,246,220,.28);background:rgba(85,246,220,.07);color:var(--cyan);padding:4px 9px;border-radius:99px;font:11px 'DM Mono',monospace;letter-spacing:.08em}
.bigformula{font:clamp(1.7rem,3vw,2.7rem) Georgia,serif;color:var(--cyan);padding:.5rem 0}
.smallmuted{color:var(--muted);font-size:.9rem}
.footer{margin-top:3rem;padding:1.5rem 0 1rem;border-top:1px solid var(--line);display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;color:#8997ac;font-size:.85rem}
.footer strong{color:#f2f5ff}.footer .accent{color:var(--cyan)}
div[data-testid="stAlert"]{border-radius:14px}
</style>
""", unsafe_allow_html=True)

# ---------- Ambient abstract geometry layer ----------
# Inline SVG animation stays behind the Streamlit interface and never captures clicks.
st.markdown("""
<div class="cosmic-layer" aria-hidden="true">
<svg viewBox="0 0 1440 900" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg">
<defs>
 <radialGradient id="orbGlow"><stop offset="0" stop-color="#55f6dc" stop-opacity=".28"/><stop offset="1" stop-color="#55f6dc" stop-opacity="0"/></radialGradient>
 <linearGradient id="wire" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#55f6dc" stop-opacity=".85"/><stop offset="1" stop-color="#9a7bff" stop-opacity=".8"/></linearGradient>
 <filter id="glow"><feGaussianBlur stdDeviation="3" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<circle cx="1120" cy="210" r="190" fill="url(#orbGlow)"/>
<!-- Large drifting orbital gyroscope -->
<g transform="translate(1120 210)" fill="none" stroke="url(#wire)" filter="url(#glow)" opacity=".48">
 <ellipse rx="155" ry="53" stroke-width="1.6"><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="34s" repeatCount="indefinite"/></ellipse>
 <ellipse rx="155" ry="53" stroke-width="1.2" transform="rotate(58)"><animateTransform attributeName="transform" type="rotate" from="58" to="418" dur="27s" repeatCount="indefinite"/></ellipse>
 <ellipse rx="155" ry="53" stroke-width="1" transform="rotate(118)"><animateTransform attributeName="transform" type="rotate" from="118" to="478" dur="42s" repeatCount="indefinite"/></ellipse>
 <circle r="10" fill="#55f6dc" fill-opacity=".6" stroke="none"><animate attributeName="r" values="7;13;7" dur="4s" repeatCount="indefinite"/></circle>
</g>
<!-- Wireframe sphere -->
<g transform="translate(270 640)" fill="none" stroke="url(#wire)" stroke-width="1.3" opacity=".36" filter="url(#glow)">
 <circle r="100"/>
 <ellipse rx="100" ry="35"><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="18s" repeatCount="indefinite"/></ellipse>
 <ellipse rx="100" ry="65"><animateTransform attributeName="transform" type="rotate" from="0" to="-360" dur="25s" repeatCount="indefinite"/></ellipse>
 <ellipse rx="35" ry="100"><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="22s" repeatCount="indefinite"/></ellipse>
 <ellipse rx="65" ry="100"><animateTransform attributeName="transform" type="rotate" from="0" to="-360" dur="31s" repeatCount="indefinite"/></ellipse>
</g>
<!-- Floating abstract polyhedra -->
<g stroke="#55f6dc" stroke-width="1.5" fill="#55f6dc" fill-opacity=".035" opacity=".72">
 <g transform="translate(790 170)"><polygon points="0,-34 30,-15 24,20 -8,34 -31,8 -22,-22"/><path d="M0 -34 L24 20 L-22 -22 L30 -15 L-8 34 L-31 8 L0 -34"/><animateTransform attributeName="transform" type="translate" values="790 170;810 140;790 170" dur="12s" repeatCount="indefinite"/></g>
 <g transform="translate(1300 610)" stroke="#9a7bff"><polygon points="0,-45 39,0 0,45 -39,0"/><path d="M-39 0 L39 0 M0 -45 L0 45 M-39 0 L0 45 L39 0 L0 -45"/><animateTransform attributeName="transform" type="translate" values="1300 610;1278 650;1300 610" dur="15s" repeatCount="indefinite"/></g>
 <g transform="translate(600 770)" stroke="#9a7bff"><polygon points="0,-24 22,12 -22,12"/><path d="M0 -24 L0 24 M-22 12 L22 12"/><animateTransform attributeName="transform" type="rotate" from="0 600 770" to="360 600 770" dur="24s" repeatCount="indefinite"/></g>
</g>
<!-- Fine drifting particles -->
<g fill="#b7fff5" filter="url(#glow)">
 <circle cx="480" cy="250" r="2"><animate attributeName="cy" values="250;210;250" dur="9s" repeatCount="indefinite"/></circle>
 <circle cx="970" cy="470" r="2.5"><animate attributeName="cx" values="970;1000;970" dur="11s" repeatCount="indefinite"/></circle>
 <circle cx="390" cy="420" r="1.5"><animate attributeName="cy" values="420;460;420" dur="8s" repeatCount="indefinite"/></circle>
 <circle cx="1180" cy="760" r="2"><animate attributeName="cy" values="760;720;760" dur="10s" repeatCount="indefinite"/></circle>
</g>
</svg>
</div>
""", unsafe_allow_html=True)

# ---------- Physics engine ----------
FORMULAS = {
    "Thin ring (central axis)": ("Ring", lambda m,r,l,ri=0: m*r*r, "I = MR²", "All the mass lies at approximately the same radius."),
    "Solid cylinder (symmetry axis)": ("Solid cylinder", lambda m,r,l,ri=0: 0.5*m*r*r, "I = ½MR²", "Uniform solid cylinder about its longitudinal symmetry axis."),
    "Thin hollow cylinder (symmetry axis)": ("Thin hollow cylinder", lambda m,r,l,ri=0: m*r*r, "I = MR²", "Thin-walled cylinder; its mass is concentrated at radius R."),
    "Thick hollow cylinder (symmetry axis)": ("Thick hollow cylinder", lambda m,r,l,ri=0: 0.5*m*(r*r+ri*ri), "I = ½M(Rₒ² + Rᵢ²)", "Uniform annular cylinder about its longitudinal symmetry axis. R is outer radius and rᵢ is inner radius."),
    "Solid sphere (diameter)": ("Solid sphere", lambda m,r,l,ri=0: 0.4*m*r*r, "I = ⅖MR²", "Uniform solid sphere about a diameter."),
    "Thin hollow sphere (diameter)": ("Thin hollow sphere", lambda m,r,l,ri=0: (2/3)*m*r*r, "I = ⅔MR²", "Thin spherical shell about a diameter."),
    "Thick hollow sphere (diameter)": ("Thick hollow sphere", lambda m,r,l,ri=0: (2/5)*m*(r**5-ri**5)/(r**3-ri**3) if r>ri else 0, "I = ⅖M(Rₒ⁵ − Rᵢ⁵)/(Rₒ³ − Rᵢ³)", "Uniform-density spherical shell with outer radius R and inner radius rᵢ, about a diameter."),
    "Solid cone (symmetry axis)": ("Solid cone", lambda m,r,l,ri=0: 0.3*m*r*r, "I = 3/10 MR²", "Uniform solid right circular cone about its symmetry axis."),
    "Hollow cone (symmetry axis)": ("Hollow cone", lambda m,r,l,ri=0: 0.5*m*r*r, "I = ½MR²", "Thin conical shell about its symmetry axis; mass is distributed over the conical surface."),
    "Thin rod (centre, perpendicular)": ("Rod", lambda m,r,l,ri=0: m*l*l/12, "I = ML²/12", "The axis passes through the centre and is perpendicular to the rod."),
    "Thin rod (end, perpendicular)": ("Rod end", lambda m,r,l,ri=0: m*l*l/3, "I = ML²/3", "The axis is perpendicular to the rod and passes through one end."),
}

QUESTIONS = [
    {"q":"Two equal point masses are moved from radius r to radius 2r. Their total moment of inertia becomes…","opts":["2 times","4 times","½ times","unchanged"],"ans":1,"why":"For point masses, I = Σmr². Doubling every radius multiplies I by 2² = 4."},
    {"q":"Which has the larger moment of inertia about its central symmetry axis, for the same mass and radius?","opts":["Solid disc","Thin ring","They are equal","Cannot tell"],"ans":1,"why":"The ring places essentially all its mass at radius R: I = MR². A disc has I = ½MR²."},
    {"q":"The SI unit of moment of inertia is…","opts":["kg m","kg m²","N m","kg/m²"],"ans":1,"why":"Moment of inertia is mass × distance², so its SI unit is kg·m²."},
    {"q":"For a fixed net torque, if I doubles, angular acceleration…","opts":["doubles","halves","quadruples","stays the same"],"ans":1,"why":"τ = Iα, therefore α = τ/I. Doubling I halves α for fixed torque."},
    {"q":"The parallel-axis theorem states…","opts":["I = Icm − Md²","I = Icm + Md²","I = MR","I = τω"],"ans":1,"why":"For a parallel axis a distance d from the centre-of-mass axis, I = Icm + Md²."},
    {"q":"Two systems have the same mass. Which generally has greater I about the same axis?","opts":["Mass closer to axis","Mass farther from axis","Always equal","Depends only on torque"],"ans":1,"why":"Each mass contributes mr². Mass farther from the axis contributes more strongly."},
    {"q":"A uniform rod's I about an end is how many times its I about its centre (parallel perpendicular axes)?","opts":["2","3","4","6"],"ans":2,"why":"Iend = ML²/3 and Icentre = ML²/12, so the ratio is 4."},
    {"q":"Moment of inertia depends on…","opts":["Mass only","Angular speed only","Mass distribution and chosen axis","Torque only"],"ans":2,"why":"I is a property of the mass distribution relative to a specified axis."},
    {"q":"For a solid disc, if radius doubles while mass stays fixed, I becomes…","opts":["2I","4I","8I","I/2"],"ans":1,"why":"I = ½MR², so doubling R multiplies I by four."},
    {"q":"A body with larger I under the same torque has…","opts":["larger angular acceleration","smaller angular acceleration","same angular acceleration","zero angular momentum"],"ans":1,"why":"Angular acceleration is inversely proportional to I when net torque is fixed."},
    {"q":"For discrete particles, the moment of inertia is…","opts":["Σmr","Σmr²","Σm/r²","Σmv²"],"ans":1,"why":"I = Σ mi ri², where ri is each particle's perpendicular distance to the axis."},
    {"q":"Rotational kinetic energy is…","opts":["½Iω²","Iω","½Iα²","τω²"],"ans":0,"why":"For rotation about a fixed axis, Krot = ½Iω²."}
]

def calc_I(shape, mass, radius, length, inner_radius=0.0):
    return FORMULAS[shape][1](mass, radius, length, inner_radius)

if "score" not in st.session_state: st.session_state.score = 0
if "answered" not in st.session_state: st.session_state.answered = {}
if "best" not in st.session_state: st.session_state.best = 0
if "challenge_idx" not in st.session_state: st.session_state.challenge_idx = 0
if "quiz_feedback" not in st.session_state: st.session_state.quiz_feedback = None
if "quiz_order" not in st.session_state: st.session_state.quiz_order = list(range(len(QUESTIONS)))

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown('<div class="eyebrow">AMAN EDGE PHYSICS</div>', unsafe_allow_html=True)
    st.markdown("## ◉ MOI QUEST")
    st.caption("ROTATIONAL MECHANICS / GAME LAB")
    nav_options = ["Mission Control", "Spin Lab", "3D Lab", "Dynamics Arena", "Torque Duel", "Challenge Arena", "Formula Vault", "How to Play"]
    jump = st.session_state.pop("nav_jump", None)
    nav_index = nav_options.index(jump) if jump in nav_options else 0
    page = st.radio("NAVIGATION", nav_options, index=nav_index, label_visibility="collapsed")
    st.markdown("---")
    st.markdown("**PLAYER STATUS**")
    st.progress(min(st.session_state.score/120,1.0))
    st.caption(f"XP earned · {st.session_state.score}")
    st.caption(f"Personal best · {st.session_state.best}")
    if st.button("↻ Reset game progress", use_container_width=True):
        st.session_state.score = 0
        st.session_state.answered = {}
        st.session_state.challenge_idx = 0
        st.session_state.quiz_feedback = None
        st.rerun()
    st.markdown("---")
    st.caption("Build intuition. Test predictions. Master the spin.")

# ---------- Header ----------
st.markdown('<div class="eyebrow">INTERACTIVE PHYSICS • SEASON 01</div>', unsafe_allow_html=True)
st.markdown('<div class="hero"><span class="tag">LEARN BY PLAYING</span><h1 style="margin:.8rem 0 .5rem">MOI <span style="color:#55f6dc">QUEST.</span></h1><p style="font-size:1.12rem;max-width:720px;margin-bottom:.7rem">The axis is your choice. The mass distribution is your puzzle. Discover why some objects resist rotational acceleration more than others.</p><span class="smallmuted">A rotational mechanics game by Aman Edge Physics</span></div>', unsafe_allow_html=True)
st.write("")

# ---------- Sound studio: synthesized audio, no external assets ----------
# Browsers require a user gesture before audio can start. The control panel is intentionally opt-in.
SOUND_STUDIO = r"""
<div class="sound-shell">
  <div class="sound-head"><span class="sound-dot"></span><span class="sound-title">MOI AUDIO ENGINE</span><span class="sound-sub">SYNTH · AMBIENCE · MOTION FX</span></div>
  <div class="sound-controls">
    <button id="ambience">◉ AMBIENCE OFF</button>
    <button id="rotor">⟳ ROTOR HUM OFF</button>
    <button id="whoosh">〰 WHOOSH</button>
    <button id="clickfx">✦ UI PULSE</button>
    <button id="successfx">✓ SUCCESS</button>
    <button id="stopfx" class="stop">■ MUTE ALL</button>
  </div>
  <div class="sound-bottom"><label for="vol">MASTER VOLUME</label><input id="vol" type="range" min="0" max="100" value="22"><span id="volread">22%</span><span class="sound-hint">Audio starts only when you press a control.</span></div>
</div>
<style>
*{box-sizing:border-box}body{margin:0;background:transparent;color:#f4f7ff;font-family:Arial,sans-serif}
.sound-shell{padding:13px 15px;border:1px solid rgba(85,246,220,.24);border-radius:16px;background:linear-gradient(110deg,rgba(11,20,34,.94),rgba(24,18,43,.91));box-shadow:0 8px 32px rgba(0,0,0,.18)}
.sound-head{display:flex;align-items:center;gap:9px;margin-bottom:11px;flex-wrap:wrap}.sound-dot{width:8px;height:8px;border-radius:50%;background:#55f6dc;box-shadow:0 0 12px #55f6dc}.sound-title{font-weight:800;letter-spacing:.13em;font-size:12px;color:#55f6dc}.sound-sub{font-size:9px;letter-spacing:.12em;color:#9ba8bc}
.sound-controls{display:flex;gap:7px;flex-wrap:wrap}.sound-controls button{border:1px solid rgba(154,123,255,.4);background:rgba(154,123,255,.09);color:#f4f7ff;border-radius:9px;padding:9px 11px;font-weight:700;font-size:10px;letter-spacing:.04em;cursor:pointer;transition:.18s}
.sound-controls button:hover{border-color:#55f6dc;transform:translateY(-1px)}.sound-controls button.active{border-color:#55f6dc;background:rgba(85,246,220,.13);color:#55f6dc}.sound-controls .stop{border-color:rgba(255,110,130,.4)}
.sound-bottom{display:flex;align-items:center;gap:10px;margin-top:11px;flex-wrap:wrap;font-size:9px;letter-spacing:.1em;color:#9ba8bc}.sound-bottom input{width:115px;accent-color:#55f6dc}.sound-hint{letter-spacing:0;font-size:10px;color:#8795ab;margin-left:auto}
</style>
<script>
(()=>{
let ctx=null, master=null, ambienceOn=false, rotorOn=false, ambienceNodes=[], rotorNodes=[], activeTones=[];
const $=id=>document.getElementById(id);
function init(){if(!ctx){ctx=new (window.AudioContext||window.webkitAudioContext)();master=ctx.createGain();master.gain.value=+$('vol').value/100*.22;master.connect(ctx.destination)}if(ctx.state==='suspended')ctx.resume();return ctx}
function tone(freq,dur,type='sine',gain=.12,slide=null){
 const a=init(),o=a.createOscillator(),g=a.createGain();o.type=type;o.frequency.setValueAtTime(freq,a.currentTime);if(slide)o.frequency.exponentialRampToValueAtTime(Math.max(20,slide),a.currentTime+dur);
 g.gain.setValueAtTime(.0001,a.currentTime);g.gain.exponentialRampToValueAtTime(gain,a.currentTime+.025);g.gain.exponentialRampToValueAtTime(.0001,a.currentTime+dur);
 o.connect(g);g.connect(master);o.start();o.stop(a.currentTime+dur+.04);activeTones.push(o);o.onended=()=>{activeTones=activeTones.filter(n=>n!==o)}
}
function noise(dur,gain=.07,filterFreq=800){
 const a=init(),n=Math.floor(a.sampleRate*dur),buf=a.createBuffer(1,n,a.sampleRate),data=buf.getChannelData(0);
 for(let i=0;i<n;i++)data[i]=(Math.random()*2-1)*(1-i/n);
 const src=a.createBufferSource(),f=a.createBiquadFilter(),g=a.createGain();src.buffer=buf;f.type='lowpass';f.frequency.value=filterFreq;g.gain.setValueAtTime(gain,a.currentTime);g.gain.exponentialRampToValueAtTime(.0001,a.currentTime+dur);src.connect(f);f.connect(g);g.connect(master);src.start();src.stop(a.currentTime+dur)
}
function loopTone(freq,type,gain,detune=0){
 const a=init(),o=a.createOscillator(),g=a.createGain();o.type=type;o.frequency.value=freq;o.detune.value=detune;g.gain.value=gain;o.connect(g);g.connect(master);o.start();return {o,g}
}
function startAmbience(){if(ambienceOn)return;init();ambienceOn=true;ambienceNodes=[loopTone(55,'sine',.18),loopTone(82.4,'triangle',.045),loopTone(164.8,'sine',.025,7)];$('ambience').classList.add('active');$('ambience').textContent='◉ AMBIENCE ON'}
function stopNodes(nodes){nodes.forEach(n=>{try{n.g.gain.setTargetAtTime(.0001,ctx.currentTime,.04);n.o.stop(ctx.currentTime+.2)}catch(e){}})}
function stopAmbience(){ambienceOn=false;stopNodes(ambienceNodes);ambienceNodes=[];$('ambience').classList.remove('active');$('ambience').textContent='◉ AMBIENCE OFF'}
function startRotor(){if(rotorOn)return;init();rotorOn=true;rotorNodes=[loopTone(42,'sawtooth',.025),loopTone(43.7,'triangle',.02),loopTone(86,'sine',.018)];$('rotor').classList.add('active');$('rotor').textContent='⟳ ROTOR HUM ON'}
function stopRotor(){rotorOn=false;stopNodes(rotorNodes);rotorNodes=[];$('rotor').classList.remove('active');$('rotor').textContent='⟳ ROTOR HUM OFF'}
$('ambience').onclick=()=>ambienceOn?stopAmbience():startAmbience();
$('rotor').onclick=()=>rotorOn?stopRotor():startRotor();
$('whoosh').onclick=()=>{noise(.65,.11,1800);tone(180,.55,'sine',.035,55)};
$('clickfx').onclick=()=>{tone(740,.09,'sine',.075);setTimeout(()=>tone(1120,.12,'sine',.045),65)};
$('successfx').onclick=()=>{tone(523.25,.22,'sine',.075);setTimeout(()=>tone(659.25,.22,'sine',.075),100);setTimeout(()=>tone(783.99,.34,'sine',.075),200)};
$('stopfx').onclick=()=>{stopAmbience();stopRotor();activeTones.forEach(o=>{try{o.stop()}catch(e){}});activeTones=[]};
$('vol').oninput=()=>{const v=+$('vol').value;$('volread').textContent=v+'%';if(master)master.gain.setTargetAtTime(v/100*.22,ctx.currentTime,.03)};
})();
</script>
"""
components.html(SOUND_STUDIO, height=142, scrolling=False)

if page == "Mission Control":
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("TOTAL XP", st.session_state.score, "Keep experimenting")
    c2.metric("CHALLENGES", f"{len(st.session_state.answered)}/12", "Knowledge checkpoints")
    c3.metric("BEST RUN", st.session_state.best, "Personal record")
    c4.metric("CORE LAW", "τ = Iα", "Rotational dynamics")
    st.write("")
    left,right = st.columns([1.15,.85], gap="large")
    with left:
        st.markdown('<div class="card"><span class="tag">01 / EXPERIMENT</span><h3>Enter the Spin Lab</h3><p>Change mass, radius, body shape, and torque. Watch the rotor turn and see how moment of inertia changes the angular acceleration.</p></div>',unsafe_allow_html=True)
        if st.button("OPEN SPIN LAB →", use_container_width=True):
            st.session_state.nav_jump = "Spin Lab"
            st.rerun()
        st.markdown('<div class="card"><span class="tag">02 / COMPETE</span><h3>Enter the Challenge Arena</h3><p>Answer conceptual questions, earn XP, build a streak of correct physics, and unlock the final mastery badge.</p></div>',unsafe_allow_html=True)
        if st.button("ENTER CHALLENGE ARENA →", use_container_width=True):
            st.session_state.nav_jump = "Challenge Arena"
            st.rerun()
    with right:
        st.markdown('<div class="card"><span class="tag">YOUR FIRST MISSION</span><h3>Predict before you calculate.</h3><p>A solid disc and a thin ring have equal mass and radius. Both experience the same net torque.</p><div class="bigformula">I<sub>ring</sub> = MR²<br>I<sub>disc</sub> = ½MR²</div><p>Which one gains angular speed faster? Explore the lab to verify your prediction.</p></div>',unsafe_allow_html=True)
        st.markdown("")
        st.markdown("#### THE LEARNING LOOP")
        st.markdown("**01** Predict → **02** Experiment → **03** Explain → **04** Earn XP")
    st.markdown("### Your physics progression")
    progress_cols = st.columns(4)
    stages=[("01","RADIAL INSTINCT","Distance matters"),("02","SHAPE SHIFTER","Geometry matters"),("03","AXIS MASTER","Axis matters"),("04","FINAL BOSS","Apply the laws")]
    for col,(n,title,desc) in zip(progress_cols,stages):
        with col: st.markdown(f'<div class="card"><span class="tag">LEVEL {n}</span><h3>{title}</h3><p class="smallmuted">{desc}</p></div>',unsafe_allow_html=True)

elif page == "Spin Lab":
    st.markdown("## Spin Lab <span style='color:#55f6dc'>/ live experiment</span>",unsafe_allow_html=True)
    st.write("Set the physical parameters. Make a prediction, then inspect the result.")
    a,b = st.columns([.9,1.1],gap="large")
    with a:
        shape = st.selectbox("BODY + ROTATION AXIS", list(FORMULAS.keys()), index=1)
        mass = st.slider("Mass M (kg)", 0.5, 20.0, 4.0, 0.5)
        radius = st.slider("Outer radius Rₒ (m)", 0.1, 2.0, 0.8, 0.1)
        is_thick_shell = shape in ("Thick hollow cylinder (symmetry axis)", "Thick hollow sphere (diameter)")
        inner_radius = st.slider("Inner radius Rᵢ (m)", 0.0, max(0.1, radius-0.05), min(0.4, max(0.0, radius-0.1)), 0.05) if is_thick_shell else 0.0
        length = st.slider("Length L (m) — for rods", 0.2, 4.0, 2.0, 0.1)
        torque = st.slider("Net applied torque τ (N·m)", 0.0, 30.0, 8.0, 0.5)
        omega = st.slider("Initial angular speed ω₀ (rad/s)", 0.0, 20.0, 3.0, 0.5)
        duration = st.slider("Simulation time (s)", 1.0, 8.0, 4.0, 0.5)
        friction = st.slider("Opposing friction torque (N·m)", 0.0, 10.0, 0.5, 0.5)
    with b:
        I = calc_I(shape,mass,radius,length,inner_radius)
        net_tau = torque-friction
        alpha = net_tau/I if I else 0
        omega_final = omega+alpha*duration
        theta = omega*duration+0.5*alpha*duration**2
        st.markdown('<div class="card"><span class="tag">LIVE OUTPUT</span><div class="bigformula">I = '+f'{I:.4f}'+' kg·m²</div><p class="smallmuted">'+FORMULAS[shape][2]+'</p></div>',unsafe_allow_html=True)
        m1,m2 = st.columns(2)
        m1.metric("ANGULAR ACCELERATION",f"{alpha:.3f} rad/s²")
        m2.metric("FINAL ANGULAR SPEED",f"{omega_final:.3f} rad/s")
        m3,m4 = st.columns(2)
        m3.metric("NET TORQUE",f"{net_tau:.2f} N·m")
        m4.metric("ANGLE TRAVELLED",f"{theta:.2f} rad")
        st.info(FORMULAS[shape][3])
        if net_tau > 0: st.success("Prediction check: positive net torque increases angular speed.")
        elif net_tau < 0: st.warning("Prediction check: opposing torque is larger, so the object slows down.")
        else: st.info("Prediction check: net torque is zero, so angular acceleration is zero.")
    # Auto-rotating rotor, drawn in canvas so it animates independently of Streamlit reruns.
    rotor_html = f"""
    <html><body style="margin:0;background:#0b111d;color:#eaf2ff;font-family:Arial,sans-serif">
    <div style="display:flex;gap:18px;align-items:center;flex-wrap:wrap;padding:10px 4px">
      <canvas id="rotor" width="520" height="300" style="width:100%;max-width:520px;border:1px solid #29354a;border-radius:18px;background:radial-gradient(circle,#151e30,#090e17)"></canvas>
      <div style="min-width:150px;flex:1"><div style="color:#55f6dc;font-size:11px;letter-spacing:2px">LIVE ROTOR</div><div style="font-size:28px;margin:7px 0">{FORMULAS[shape][0]}</div><div style="color:#aab8ce;font-size:13px;line-height:1.7">Mass: {mass:.1f} kg<br>Moment of inertia: {I:.3f} kg·m²<br>Net torque: {net_tau:.2f} N·m<br>Angular acceleration: {alpha:.3f} rad/s²</div><div style="margin-top:16px;color:#9a7bff;font-size:12px">WATCH THE MASS DISTRIBUTION</div></div>
    </div>
    <script>
    const c=document.getElementById('rotor'),x=c.getContext('2d');let t=0,ang=0;
    function draw(){{x.clearRect(0,0,c.width,c.height);const cx=260,cy=150,R=82;
      x.strokeStyle='#24344b';x.lineWidth=1;for(let r=25;r<150;r+=25){{x.beginPath();x.arc(cx,cy,r,0,Math.PI*2);x.stroke();}}
      x.strokeStyle='#8a9ab3';x.setLineDash([4,6]);x.beginPath();x.moveTo(cx,22);x.lineTo(cx,278);x.stroke();x.setLineDash([]);
      x.save();x.translate(cx,cy);x.rotate(ang);
      const kind='{FORMULAS[shape][0]}'; const innerR={inner_radius if 'inner_radius' in locals() else 0};
      if(kind==='Rod'||kind==='Rod end'){{x.strokeStyle='#55f6dc';x.lineWidth=10;x.lineCap='round';x.beginPath();x.moveTo(-R,0);x.lineTo(R,0);x.stroke();for(let i=0;i<9;i++){{let px=-R+2*R*i/8;x.fillStyle='#b8fff4';x.beginPath();x.arc(px,0,3,0,Math.PI*2);x.fill();}}}}
      else if(kind.includes('cylinder')){{const ry=R*.42; x.fillStyle='rgba(85,246,220,.10)';x.strokeStyle='#55f6dc';x.lineWidth=2.5;
        x.beginPath();x.ellipse(0,-ry,R,ry,0,0,Math.PI*2);x.fill();x.stroke();x.beginPath();x.moveTo(-R,-ry);x.lineTo(-R,ry);x.ellipse(0,ry,R,ry,0,Math.PI,Math.PI*2);x.lineTo(R,-ry);x.stroke();
        if(kind==='Thick hollow cylinder'){{x.strokeStyle='#9a7bff';x.beginPath();x.ellipse(0,-ry,R*innerR/{radius},ry*innerR/{radius},0,0,Math.PI*2);x.stroke();x.beginPath();x.ellipse(0,ry,R*innerR/{radius},ry*innerR/{radius},0,Math.PI,Math.PI*2);x.stroke();}}
        else if(kind==='Thin hollow cylinder'){{x.setLineDash([4,4]);x.beginPath();x.ellipse(0,0,R,ry,0,0,Math.PI*2);x.stroke();x.setLineDash([]);}}
      }}
      else if(kind.includes('sphere')||kind==='Solid sphere'){{x.strokeStyle='#55f6dc';x.lineWidth=2.5;x.beginPath();x.arc(0,0,R,0,Math.PI*2);x.stroke();x.strokeStyle='#9a7bff';x.beginPath();x.ellipse(0,0,R*.42,R,0,0,Math.PI*2);x.stroke();x.beginPath();x.ellipse(0,0,R,R*.42,0,0,Math.PI*2);x.stroke();
        if(kind==='Thick hollow sphere'){{x.strokeStyle='#9a7bff';x.beginPath();x.arc(0,0,R*innerR/{radius},0,Math.PI*2);x.stroke();}}
        if(kind==='Thin hollow sphere'){{x.setLineDash([3,4]);x.beginPath();x.ellipse(0,0,R*.42,R,0,0,Math.PI*2);x.stroke();x.setLineDash([]);}}
      }}
      else if(kind.includes('cone')){{x.strokeStyle='#55f6dc';x.lineWidth=2.5;x.fillStyle='rgba(85,246,220,.10)';x.beginPath();x.moveTo(0,-R);x.lineTo(-R*.72,R*.55);x.ellipse(0,R*.55,R*.72,R*.25,0,Math.PI,Math.PI*2);x.closePath();x.fill();x.stroke();x.beginPath();x.moveTo(0,-R);x.lineTo(R*.72,R*.55);x.stroke();x.strokeStyle='#9a7bff';x.beginPath();x.ellipse(0,R*.55,R*.72,R*.25,0,0,Math.PI*2);x.stroke();}}
      else{{x.fillStyle='rgba(85,246,220,.13)';x.strokeStyle='#55f6dc';x.lineWidth=3;x.beginPath();x.arc(0,0,R,0,Math.PI*2);x.fill();x.stroke();for(let i=0;i<12;i++){{let a=i*Math.PI/6;x.strokeStyle='#4b8d98';x.beginPath();x.moveTo(0,0);x.lineTo(R*Math.cos(a),R*Math.sin(a));x.stroke();}}}}
      x.fillStyle='#f4f7ff';x.beginPath();x.arc(0,0,7,0,Math.PI*2);x.fill();x.strokeStyle='#9a7bff';x.lineWidth=3;x.beginPath();x.moveTo(0,0);x.lineTo(R*.82,0);x.stroke();x.restore();
      x.fillStyle='#a7b6cb';x.font='12px monospace';x.fillText('AXIS z',cx+12,cy-112);x.fillStyle='#55f6dc';x.fillText('θ = '+ang.toFixed(2)+' rad',18,25);
      ang += Math.max(-.035,Math.min(.035,({omega_final})*.006));requestAnimationFrame(draw);
    }}draw();
    </script></body></html>
    """
    components.html(rotor_html,height=340,scrolling=False)
    st.markdown("#### The physics behind the animation")
    st.latex(r"I=\sum_i m_i r_i^2\qquad\text{or}\qquad I=\int r^2\,dm")
    st.latex(r"\tau_{\mathrm{net}}=I\alpha\qquad\Rightarrow\qquad\alpha=\frac{\tau_{\mathrm{net}}}{I}")
    st.caption("Idealized model: constant net torque, fixed axis, rigid body, and no speed-dependent drag. The rotor is a visual aid; the numerical outputs follow the stated model.")

elif page == "3D Lab":
    st.markdown("## 3D Rotational-Inertia Lab <span style='color:#55f6dc'>/ explore in three dimensions</span>", unsafe_allow_html=True)
    st.write("Orbit the camera, compare solid and hollow mass distributions, and play the rotation animation. The axis shown is the z-axis.")
    left, right = st.columns([0.82, 1.35], gap="large")
    with left:
        body = st.selectbox("BODY GEOMETRY", [
            "Solid cylinder", "Thin hollow cylinder", "Thick hollow cylinder",
            "Solid sphere", "Thin hollow sphere", "Thick hollow sphere",
            "Solid cone", "Hollow cone"
        ], key="lab3d_body")
        M = st.slider("Mass M (kg)", 0.5, 20.0, 4.0, 0.5, key="lab3d_mass")
        R = st.slider("Outer radius Rₒ (m)", 0.2, 2.0, 1.0, 0.1, key="lab3d_radius")
        is_shell = body in ("Thick hollow cylinder", "Thick hollow sphere")
        ri = st.slider("Inner radius Rᵢ (m)", 0.05, max(0.1, R-0.05), min(0.5, R-0.05), 0.05, key="lab3d_inner") if is_shell else 0.0
        H = st.slider("Height / cone height (m)", 0.5, 4.0, 2.0, 0.1, key="lab3d_height") if "cylinder" in body.lower() or "cone" in body.lower() else 2*R
        tau = st.slider("Net torque τ (N·m)", 0.0, 30.0, 8.0, 0.5, key="lab3d_tau")
        omega0 = st.slider("Initial angular speed ω₀ (rad/s)", 0.0, 15.0, 2.0, 0.5, key="lab3d_omega")
        sim_t = st.slider("Prediction time (s)", 0.5, 6.0, 3.0, 0.5, key="lab3d_time")
    # Moments of inertia about the symmetry axis for cylinders/cones and a diameter for spheres.
    if body == "Solid cylinder": I3 = 0.5*M*R**2
    elif body == "Thin hollow cylinder": I3 = M*R**2
    elif body == "Thick hollow cylinder": I3 = 0.5*M*(R**2+ri**2)
    elif body == "Solid sphere": I3 = 0.4*M*R**2
    elif body == "Thin hollow sphere": I3 = (2/3)*M*R**2
    elif body == "Thick hollow sphere": I3 = (2/5)*M*(R**5-ri**5)/(R**3-ri**3)
    elif body == "Solid cone": I3 = 0.3*M*R**2
    else: I3 = 0.5*M*R**2
    alpha3 = tau/I3 if I3 else 0.0
    omega_end = omega0 + alpha3*sim_t
    angle_end = omega0*sim_t + 0.5*alpha3*sim_t**2
    st.session_state["lab3d_I"] = I3
    with right:
        k1,k2,k3=st.columns(3)
        k1.metric("MOMENT OF INERTIA",f"{I3:.4f} kg·m²")
        k2.metric("ANGULAR ACCELERATION",f"{alpha3:.3f} rad/s²")
        k3.metric("FINAL ANGULAR SPEED",f"{omega_end:.3f} rad/s")
        st.caption("Rotate the view by dragging. Scroll to zoom. Use the animation controls to see tracer particles orbit the axis.")
        # Parametric surfaces. z is the rotation axis for every body in this learning lab.
        u=np.linspace(0,2*np.pi,64)
        fig=go.Figure()
        teal="#55f6dc"; purple="#9a7bff"
        def add_surface(x,y,z,color=teal,opacity=0.65,name="surface"):
            fig.add_trace(go.Surface(x=x,y=y,z=z,colorscale=[[0,color],[1,color]],showscale=False,opacity=opacity,hovertemplate=name+"<extra></extra>",name=name,lighting=dict(ambient=0.42,diffuse=0.75,specular=0.8,roughness=0.28)))
        if "cylinder" in body.lower():
            zz=np.linspace(-H/2,H/2,28)
            U,Z=np.meshgrid(u,zz)
            rr=ri if body=="Thick hollow cylinder" else R
            add_surface(R*np.cos(U),R*np.sin(U),Z,teal,0.58,"Outer cylindrical surface")
            if body=="Thick hollow cylinder":
                add_surface(ri*np.cos(U),ri*np.sin(U),Z,purple,0.72,"Inner cylindrical surface")
            for zcap in (-H/2,H/2):
                rradii=np.linspace(0 if body=="Solid cylinder" else (ri if body=="Thick hollow cylinder" else R),R,12)
                U2,RR=np.meshgrid(u,rradii)
                add_surface(RR*np.cos(U2),RR*np.sin(U2),np.full_like(U2,zcap),purple if zcap>0 else teal,0.28,"End face")
        elif "sphere" in body.lower():
            v=np.linspace(0,np.pi,40); U,V=np.meshgrid(u,v)
            rr=R
            add_surface(rr*np.sin(V)*np.cos(U),rr*np.sin(V)*np.sin(U),rr*np.cos(V),teal,0.60,"Outer spherical surface")
            if body=="Thick hollow sphere":
                add_surface(ri*np.sin(V)*np.cos(U),ri*np.sin(V)*np.sin(U),ri*np.cos(V),purple,0.42,"Inner spherical surface")
        else:
            # Right circular cone: z=0 at base and z=H at apex.
            zz=np.linspace(0,H,32); U,Z=np.meshgrid(u,zz); RR=R*(1-Z/H)
            add_surface(RR*np.cos(U),RR*np.sin(U),Z,teal,0.62,"Conical surface")
            if body=="Solid cone":
                U2,RR2=np.meshgrid(u,np.linspace(0,R,14))
                add_surface(RR2*np.cos(U2),RR2*np.sin(U2),np.zeros_like(U2),purple,0.3,"Base")
        # Rotation axis and reference rings
        zmin,zmax=(-H/2,H/2) if "cylinder" in body.lower() else (0,H) if "cone" in body.lower() else (-R,R)
        fig.add_trace(go.Scatter3d(x=[0,0],y=[0,0],z=[zmin*1.15,zmax*1.15],mode="lines",line=dict(color="#ffffff",width=5,dash="dash"),name="Rotation axis z"))
        # A tracer ring makes the angular motion visible even when the body's outline is symmetric.
        frames=[]
        for fi in range(36):
            ang=2*np.pi*fi/36
            tracer_z=(zmin+zmax)*0.12
            tr_x=[R*np.cos(ang),R*np.cos(ang+0.13)]
            tr_y=[R*np.sin(ang),R*np.sin(ang+0.13)]
            tr_z=[tracer_z,tracer_z]
            frames.append(go.Frame(data=[go.Scatter3d(x=tr_x,y=tr_y,z=tr_z,mode="markers+lines",marker=dict(size=[7,3],color=[teal,purple]),line=dict(color=teal,width=7),name="Rotating tracer")],traces=[len(fig.data)],name=str(fi)))
        fig.add_trace(go.Scatter3d(x=[R, R*np.cos(.13)],y=[0,R*np.sin(.13)],z=[(zmin+zmax)*.12]*2,mode="markers+lines",marker=dict(size=[7,3],color=[teal,purple]),line=dict(color=teal,width=7),name="Rotating tracer"))
        # Frames update only the tracer; all body surfaces remain static in their own geometry.
        fig.frames=frames
        fig.update_layout(
            height=570, margin=dict(l=0,r=0,t=18,b=0),
            paper_bgcolor="rgba(5,9,16,0.0)", plot_bgcolor="rgba(5,9,16,0.0)",
            font=dict(color="#eaf2ff",family="Space Grotesk, sans-serif"),
            scene=dict(bgcolor="rgba(5,9,16,0.0)",xaxis=dict(visible=False,range=[-2.4,2.4]),yaxis=dict(visible=False,range=[-2.4,2.4]),zaxis=dict(visible=False,range=[min(-2.4,zmin-0.3),max(2.4,zmax+0.3)]),aspectmode="manual",aspectratio=dict(x=1,y=1,z=max(.7,min(1.7,H/(2*R))))),
            legend=dict(orientation="h",yanchor="bottom",y=0.01,x=0.02,bgcolor="rgba(0,0,0,0)"),
            updatemenus=[dict(type="buttons",showactive=False,x=0.02,y=0.98,xanchor="left",yanchor="top",buttons=[
                dict(label="▶ PLAY ROTATION",method="animate",args=[None,{"frame":{"duration":animation_duration_ms,"redraw":True},"fromcurrent":True,"transition":{"duration":0},"mode":"immediate"}]),
                dict(label="Ⅱ PAUSE",method="animate",args=[[None],{"frame":{"duration":0,"redraw":False},"mode":"immediate","transition":{"duration":0}}])
            ])]
        )
        st.plotly_chart(fig,use_container_width=True,config={"displaylogo":False,"scrollZoom":True})
    st.markdown("### What does the geometry tell you?")
    st.markdown(f'<div class="card"><span class="tag">PHYSICS DEBRIEF</span><h3>{body}</h3><div class="bigformula">I = {I3:.5g} kg·m²</div><p>{FORMULAS.get(body + (" (symmetry axis)" if "cylinder" in body.lower() or "cone" in body.lower() else " (diameter)"), ("",None,"","The formula is evaluated for the selected geometry."))[2] if body + (" (symmetry axis)" if "cylinder" in body.lower() or "cone" in body.lower() else " (diameter)") in FORMULAS else "The moment of inertia depends on the selected body's mass distribution and rotation axis."}</p><p class="smallmuted">For the chosen model, α = τ/I. At fixed torque, a larger I produces a smaller angular acceleration.</p></div>',unsafe_allow_html=True)
    st.markdown("#### Compare the same mass and outer radius")
    comparison = {
        "Solid cylinder":0.5*M*R**2, "Thin hollow cylinder":M*R**2,
        "Thick hollow cylinder":0.5*M*(R**2+ri**2),
        "Solid sphere":0.4*M*R**2, "Thin hollow sphere":(2/3)*M*R**2,
        "Thick hollow sphere":(2/5)*M*(R**5-ri**5)/(R**3-ri**3),
        "Solid cone":0.3*M*R**2, "Hollow cone":0.5*M*R**2
    }
    comp_df={"Body":list(comparison.keys()),"I (kg·m²)":list(comparison.values())}
    st.bar_chart(comp_df,x="Body",y="I (kg·m²)")
    st.caption("Comparison uses the same mass and outer radius. Thick-shell entries use the selected inner radius; bodies have different geometries and idealized mass distributions.")

elif page == "Dynamics Arena":
    st.markdown("## Dynamics Arena <span style='color:#55f6dc'>/ axis • torque • motion</span>", unsafe_allow_html=True)
    st.write("Choose a body and a rotation axis, apply torque against friction, and inspect its motion, energy and angular-velocity history.")
    setup, view = st.columns([0.85, 1.15], gap="large")
    with setup:
        player = st.text_input("PLAYER NAME (for leaderboard)", value=st.session_state.get("dynamics_player",""), max_chars=32, key="dynamics_player")
        body = st.selectbox("BODY", ["Solid cylinder","Thin hollow cylinder","Thick hollow cylinder","Solid sphere","Thin hollow sphere","Thick hollow sphere","Solid cone","Hollow cone"], key="dyn_body")
        axis = st.selectbox("CHOOSE ROTATION AXIS", [
            "Symmetry axis (z)",
            "Central transverse axis (x)",
            "Parallel axis offset by d"
        ], key="dyn_axis")
        M = st.slider("Mass M (kg)", 0.5, 20.0, 4.0, 0.5, key="dyn_mass")
        R = st.slider("Outer radius Rₒ (m)", 0.2, 2.0, 1.0, 0.1, key="dyn_radius")
        hollow = body in ("Thick hollow cylinder","Thick hollow sphere")
        Ri = st.slider("Inner radius Rᵢ (m)", 0.05, max(0.1,R-0.05), min(0.4,R-0.05), 0.05, key="dyn_inner") if hollow else 0.0
        H = st.slider("Length / height L (m)", 0.5, 4.0, 2.0, 0.1, key="dyn_height") if "cylinder" in body.lower() or "cone" in body.lower() else 2*R
        d = st.slider("Parallel-axis offset d (m)", 0.0, 2.0, 0.5, 0.1, key="dyn_offset") if axis == "Parallel axis offset by d" else 0.0
        torque = st.slider("Applied torque τ (N·m)", -20.0, 20.0, 8.0, 0.5, key="dyn_torque")
        friction = st.slider("Friction torque magnitude (N·m)", 0.0, 10.0, 0.5, 0.5, key="dyn_friction")
        omega0 = st.slider("Initial angular velocity ω₀ (rad/s)", -15.0, 15.0, 2.0, 0.5, key="dyn_omega")
        duration = st.slider("Simulation duration (s)", 1.0, 10.0, 5.0, 0.5, key="dyn_duration")
        playback_speed_label = st.select_slider("PLAYBACK SPEED", options=["0.5× — slow", "1× — normal", "2× — fast"], value="1× — normal", key="dyn_playback_speed")
        playback_speed = {"0.5× — slow": 0.5, "1× — normal": 1.0, "2× — fast": 2.0}[playback_speed_label]
    # Inertia about selected centre-of-mass axis; transverse-axis models are explicit idealisations.
    if body == "Solid cylinder":
        Iz, Ix = 0.5*M*R**2, M*(3*R**2+H**2)/12
    elif body == "Thin hollow cylinder":
        Iz, Ix = M*R**2, M*(6*R**2+H**2)/12
    elif body == "Thick hollow cylinder":
        Iz, Ix = 0.5*M*(R**2+Ri**2), M*(3*(R**2+Ri**2)+H**2)/12
    elif body == "Solid sphere":
        Iz = Ix = 0.4*M*R**2
    elif body == "Thin hollow sphere":
        Iz = Ix = (2/3)*M*R**2
    elif body == "Thick hollow sphere":
        Iz = Ix = (2/5)*M*(R**5-Ri**5)/(R**3-Ri**3)
    elif body == "Solid cone":
        Iz, Ix = 0.3*M*R**2, M*(3*R**2/20+3*H**2/80)
    else:
        Iz, Ix = 0.5*M*R**2, M*(R**2/4+H**2/12)
    Icm = Ix if axis == "Central transverse axis (x)" else Iz
    Iaxis = Icm + M*d**2
    # Coulomb-like friction opposes the instantaneous motion; integrate with small fixed time steps.
    times = np.linspace(0.0, duration, 301)
    dt = times[1]-times[0]
    omegas = np.zeros_like(times); angles = np.zeros_like(times); alphas = np.zeros_like(times)
    omegas[0] = omega0
    for j in range(1,len(times)):
        sign = np.sign(omegas[j-1]) if abs(omegas[j-1]) > 1e-8 else np.sign(torque)
        net = torque - friction*sign
        if abs(omegas[j-1]) <= 1e-8 and abs(torque) <= friction:
            net = 0.0
        alphas[j-1] = net/Iaxis
        omegas[j] = omegas[j-1] + alphas[j-1]*dt
        # Static friction can hold the body at rest; prevent numerical overshoot
        # through zero when applied torque cannot overcome friction.
        if omegas[j-1]*omegas[j] < 0 and abs(torque) <= friction:
            omegas[j] = 0.0
            alphas[j-1] = 0.0
        angles[j] = angles[j-1] + 0.5*(omegas[j-1]+omegas[j])*dt
    alphas[-1] = alphas[-2]
    energy = 0.5*Iaxis*omegas**2

    # Physics-linked audio: the rotor pitch follows the simulated angular-speed curve.
    # The user must press PLAY because browsers block unsolicited audio.
    import json
    audio_times = json.dumps(times.tolist())
    audio_omegas = json.dumps(omegas.tolist())
    audio_angles = json.dumps(angles.tolist())
    audio_friction = float(friction)
    audio_torque = float(torque)
    audio_duration = float(duration)
    DYNAMICS_AUDIO = r"""
    <div class="dyn-audio">
      <div class="dyn-audio-top"><span class="live-dot"></span><b>PHYSICS-LINKED AUDIO</b><span id="soundState">STANDBY</span></div>
      <div class="dyn-audio-controls">
        <button id="soundPlay">▶ PLAY SIM + SOUND</button><button id="soundPause">Ⅱ PAUSE</button><button id="soundReset">↺ RESET</button>
        <label>VOLUME <input id="soundVol" type="range" min="0" max="100" value="25"><span id="soundVolText">25%</span></label>
      </div>
      <div class="dyn-audio-readout"><span>TIME <strong id="soundTime">0.00 s</strong></span><span>ANGULAR SPEED <strong id="soundOmega">0.00 rad/s</strong></span><span>ROTOR PITCH <strong id="soundPitch">— Hz</strong></span></div>
      <input id="soundSeek" aria-label="Simulation time" type="range" min="0" max="__DURATION__" step="0.01" value="0">
      <p>Audio pitch follows |ω(t)|. Friction adds a subtle mechanical texture; mute or pause at any time.</p>
    </div>
    <style>
    *{box-sizing:border-box}.dyn-audio{font-family:Arial,sans-serif;color:#eaf2ff;background:linear-gradient(110deg,rgba(8,18,30,.97),rgba(25,17,43,.96));border:1px solid rgba(85,246,220,.28);border-radius:15px;padding:13px 15px}
    .dyn-audio-top,.dyn-audio-controls,.dyn-audio-readout{display:flex;align-items:center;gap:10px;flex-wrap:wrap}.dyn-audio-top{font-size:11px;letter-spacing:.1em;color:#55f6dc}.dyn-audio-top #soundState{margin-left:auto;color:#a8b5c8;font-size:10px}
    .live-dot{width:7px;height:7px;border-radius:50%;background:#55f6dc;box-shadow:0 0 10px #55f6dc}.dyn-audio-controls{margin:12px 0}.dyn-audio button{background:rgba(85,246,220,.08);border:1px solid rgba(85,246,220,.35);border-radius:8px;padding:8px 10px;color:#eaf2ff;font-weight:700;font-size:10px;cursor:pointer}.dyn-audio button:hover{border-color:#9a7bff}.dyn-audio label{display:flex;align-items:center;gap:6px;font-size:9px;color:#a8b5c8}.dyn-audio input[type=range]{accent-color:#55f6dc;width:100px}.dyn-audio-readout{justify-content:space-between;font-size:9px;color:#93a4bb;letter-spacing:.07em}.dyn-audio-readout strong{display:block;color:#fff;font-size:12px;letter-spacing:0;margin-top:3px}.dyn-audio #soundSeek{width:100%;margin:12px 0 2px;accent-color:#55f6dc}.dyn-audio p{font-size:10px;line-height:1.5;color:#8f9db1;margin:5px 0 0}
    </style>
    <script>
    (()=>{
      const ts=__TIMES__, ws=__OMEGAS__, duration=__DURATION__, friction=__FRICTION__, torque=__TORQUE__;
      const $=id=>document.getElementById(id);
      let ctx=null,master=null,osc=null,oscGain=null,noiseGain=null,noiseSrc=null,playing=false,startWall=0,startTime=0,elapsed=0,raf=0;
      function init(){
        if(!ctx){ctx=new (window.AudioContext||window.webkitAudioContext)();master=ctx.createGain();master.gain.value=+$('soundVol').value/100*.28;master.connect(ctx.destination);
          osc=ctx.createOscillator();osc.type='triangle';osc.frequency.value=65;oscGain=ctx.createGain();oscGain.gain.value=0;osc.connect(oscGain);oscGain.connect(master);osc.start();
          const n=Math.floor(ctx.sampleRate*2),buf=ctx.createBuffer(1,n,ctx.sampleRate),data=buf.getChannelData(0);for(let i=0;i<n;i++)data[i]=(Math.random()*2-1)*.35;
          noiseSrc=ctx.createBufferSource();noiseSrc.buffer=buf;noiseSrc.loop=true;const filter=ctx.createBiquadFilter();filter.type='lowpass';filter.frequency.value=Math.min(1400,350+friction*80);noiseGain=ctx.createGain();noiseGain.gain.value=0;noiseSrc.connect(filter);filter.connect(noiseGain);noiseGain.connect(master);noiseSrc.start();
        }if(ctx.state==='suspended')ctx.resume();
      }
      function sample(t){let i=Math.max(0,Math.min(ts.length-2,Math.floor(t/duration*(ts.length-1))));let f=(t-ts[i])/(ts[i+1]-ts[i]||1);return ws[i]+(ws[i+1]-ws[i])*Math.max(0,Math.min(1,f))}
      function draw(){
        if(!playing)return;const t=Math.min(duration,startTime+(performance.now()-startWall)/1000);
        $('soundSeek').value=t;$('soundTime').textContent=t.toFixed(2)+' s';
        const w=sample(t),pitch=Math.max(38,Math.min(420,55+Math.abs(w)*15));
        $('soundOmega').textContent=w.toFixed(2)+' rad/s';$('soundPitch').textContent=pitch.toFixed(0)+' Hz';
        osc.frequency.setTargetAtTime(pitch,ctx.currentTime,.045);
        const amp=Math.min(.16,.018+Math.abs(w)*.004);oscGain.gain.setTargetAtTime(amp,ctx.currentTime,.06);
        noiseGain.gain.setTargetAtTime(Math.min(.045,friction*.003),ctx.currentTime,.08);
        if(t>=duration){playing=false;elapsed=duration;$('soundState').textContent='COMPLETE';oscGain.gain.setTargetAtTime(0,ctx.currentTime,.15);noiseGain.gain.setTargetAtTime(0,ctx.currentTime,.15);return}
        raf=requestAnimationFrame(draw);
      }
      function play(){if(playing)return;init();playing=true;startTime=elapsed;startWall=performance.now();$('soundState').textContent='PLAYING';draw()}
      function pause(){if(playing){elapsed=Math.min(duration,startTime+(performance.now()-startWall)/1000);playing=false;cancelAnimationFrame(raf)}if(ctx){oscGain.gain.setTargetAtTime(0,ctx.currentTime,.04);noiseGain.gain.setTargetAtTime(0,ctx.currentTime,.04)}$('soundState').textContent='PAUSED'}
      $('soundPlay').onclick=play;
      $('soundPause').onclick=pause;
      $('soundReset').onclick=()=>{pause();elapsed=0;$('soundSeek').value=0;$('soundTime').textContent='0.00 s';$('soundOmega').textContent=ws[0].toFixed(2)+' rad/s';$('soundPitch').textContent='— Hz';$('soundState').textContent='STANDBY'};
      $('soundSeek').oninput=()=>{pause();elapsed=+$('soundSeek').value;const w=sample(elapsed);$('soundTime').textContent=elapsed.toFixed(2)+' s';$('soundOmega').textContent=w.toFixed(2)+' rad/s';$('soundPitch').textContent=Math.max(38,Math.min(420,55+Math.abs(w)*15)).toFixed(0)+' Hz';$('soundState').textContent='SCRUBBED'};
      $('soundVol').oninput=()=>{$('soundVolText').textContent=$('soundVol').value+'%';if(master)master.gain.setTargetAtTime(+$('soundVol').value/100*.28,ctx.currentTime,.03)};
      $('soundOmega').textContent=ws[0].toFixed(2)+' rad/s';
    })();
    </script>
    """
    DYNAMICS_AUDIO = DYNAMICS_AUDIO.replace("__TIMES__", audio_times).replace("__OMEGAS__", audio_omegas).replace("__DURATION__", str(audio_duration)).replace("__FRICTION__", str(audio_friction)).replace("__TORQUE__", str(audio_torque))
    components.html(DYNAMICS_AUDIO, height=190, scrolling=False)
    with view:
        m1,m2,m3,m4=st.columns(4)
        m1.metric("MOMENT OF INERTIA",f"{Iaxis:.4f} kg·m²")
        m2.metric("INITIAL α",f"{alphas[0]:.3f} rad/s²")
        m3.metric("FINAL ω",f"{omegas[-1]:.3f} rad/s")
        m4.metric("FINAL Krot",f"{energy[-1]:.3f} J")
        st.caption(f"Axis: {axis}. Icm = {Icm:.4f} kg·m²; parallel-axis contribution Md² = {M*d*d:.4f} kg·m².")
        # One synchronized Plotly timeline: body mesh, omega graph, and kinetic-energy graph.
        # Playback frames use the numerically integrated angle theta(t).
        from plotly.subplots import make_subplots
        u=np.linspace(0,2*np.pi,48)
        fig_sync=make_subplots(
            rows=2, cols=2,
            specs=[[{"type":"scene","colspan":2},None],[{"type":"xy"},{"type":"xy"}]],
            row_heights=[0.60,0.40],
            vertical_spacing=0.17,
            horizontal_spacing=0.12,
            subplot_titles=("3D ROTOR · SELECTED AXIS","ANGULAR VELOCITY ω(t)","ROTATIONAL ENERGY K(t)")
        )
        mesh_coords=[]; mesh_styles=[]
        def add_sync_surface(x,y,z,color="#55f6dc",opacity=0.66,name="Body surface"):
            x,y,z=np.asarray(x),np.asarray(y),np.asarray(z)
            mesh_coords.append((x,y,z))
            mesh_styles.append((color,opacity,name))
            fig_sync.add_trace(go.Surface(x=x,y=y,z=z,colorscale=[[0,color],[1,color]],showscale=False,opacity=opacity,name=name,hovertemplate=name+"<extra></extra>",lighting=dict(ambient=.45,diffuse=.78,specular=.65,roughness=.3)),row=1,col=1)
        if "sphere" in body.lower():
            v=np.linspace(0,np.pi,28); U,V=np.meshgrid(u,v)
            add_sync_surface(R*np.sin(V)*np.cos(U),R*np.sin(V)*np.sin(U),R*np.cos(V),"#55f6dc",.68,body)
            if hollow:
                add_sync_surface(Ri*np.sin(V)*np.cos(U),Ri*np.sin(V)*np.sin(U),Ri*np.cos(V),"#9a7bff",.42,"Inner spherical surface")
        elif "cone" in body.lower():
            zz=np.linspace(-H/2,H/2,28); U,Z=np.meshgrid(u,zz); RR=R*(0.5-Z/H)
            add_sync_surface(RR*np.cos(U),RR*np.sin(U),Z,"#55f6dc",.68,body)
            if body=="Solid cone":
                U2,RR2=np.meshgrid(u,np.linspace(0,R,16))
                add_sync_surface(RR2*np.cos(U2),RR2*np.sin(U2),np.full_like(U2,-H/2),"#9a7bff",.28,"Base")
        else:
            zz=np.linspace(-H/2,H/2,22); U,Z=np.meshgrid(u,zz)
            add_sync_surface(R*np.cos(U),R*np.sin(U),Z,"#55f6dc",.62,body)
            if hollow:
                add_sync_surface(Ri*np.cos(U),Ri*np.sin(U),Z,"#9a7bff",.78,"Inner wall")
        surface_count=len(mesh_coords)
        if axis=="Central transverse axis (x)":
            ax=dict(x=[-R*1.5,R*1.5],y=[0,0],z=[0,0])
        elif axis=="Parallel axis offset by d":
            ax=dict(x=[d,d],y=[0,0],z=[-max(R,H/2)*1.5,max(R,H/2)*1.5])
        else:
            ax=dict(x=[0,0],y=[0,0],z=[-max(R,H/2)*1.5,max(R,H/2)*1.5])
        fig_sync.add_trace(go.Scatter3d(**ax,mode="lines",line=dict(color="white",width=5,dash="dash"),name="Selected axis",hoverinfo="skip"),row=1,col=1)
        tracer_index=len(fig_sync.data)
        fig_sync.add_trace(go.Scatter3d(x=[R,R*np.cos(.18)],y=[0,R*np.sin(.18)],z=[0,0],mode="markers+lines",marker=dict(size=[7,3],color=["#55f6dc","#9a7bff"]),line=dict(color="#55f6dc",width=6),name="Surface tracer",hoverinfo="skip"),row=1,col=1)

        # Full histories stay visible; each frame moves a vertical cursor and a point on both curves.
        fig_sync.add_trace(go.Scatter(x=times,y=omegas,mode="lines",name="ω(t)",line=dict(color="#55f6dc",width=2.5),showlegend=False),row=2,col=1)
        omega_lo=float(np.min(omegas)); omega_hi=float(np.max(omegas))
        omega_pad=max(0.2,(omega_hi-omega_lo)*0.12)
        omega_cursor_index=len(fig_sync.data)
        fig_sync.add_trace(go.Scatter(x=[times[0],times[0]],y=[omega_lo-omega_pad,omega_hi+omega_pad],mode="lines",line=dict(color="white",width=1.7,dash="dash"),showlegend=False,hoverinfo="skip"),row=1,col=2)
        omega_dot_index=len(fig_sync.data)
        fig_sync.add_trace(go.Scatter(x=[times[0]],y=[omegas[0]],mode="markers",marker=dict(size=9,color="#ffffff",line=dict(color="#55f6dc",width=2)),showlegend=False,name="Current ω",hovertemplate="t=%{x:.2f} s<br>ω=%{y:.3f} rad/s<extra></extra>"),row=1,col=2)

        fig_sync.add_trace(go.Scatter(x=times,y=energy,mode="lines",name="Krot(t)",line=dict(color="#9a7bff",width=2.5),fill="tozeroy",fillcolor="rgba(154,123,255,.12)",showlegend=False),row=2,col=2)
        energy_lo=0.0; energy_hi=float(np.max(energy))
        energy_pad=max(0.2,energy_hi*0.12)
        energy_cursor_index=len(fig_sync.data)
        fig_sync.add_trace(go.Scatter(x=[times[0],times[0]],y=[energy_lo,energy_hi+energy_pad],mode="lines",line=dict(color="white",width=1.7,dash="dash"),showlegend=False,hoverinfo="skip"),row=1,col=3)
        energy_dot_index=len(fig_sync.data)
        fig_sync.add_trace(go.Scatter(x=[times[0]],y=[energy[0]],mode="markers",marker=dict(size=9,color="#ffffff",line=dict(color="#9a7bff",width=2)),showlegend=False,name="Current K",hovertemplate="t=%{x:.2f} s<br>K=%{y:.3f} J<extra></extra>"),row=1,col=3)

        # Build animation frames from the simulated angle array, including friction-induced slowdowns.
        sample_indices=np.unique(np.linspace(0,len(times)-1,61).astype(int))
        frames=[]
        frame_labels=[]
        animation_ms=max(25,int(90/playback_speed))
        for fi,si in enumerate(sample_indices):
            ang=float(angles[si]); ct=float(times[si])
            frame_data=[]
            for bx,by,bz in mesh_coords:
                if axis=="Central transverse axis (x)":
                    fx,fy,fz=bx,by*np.cos(ang)-bz*np.sin(ang),by*np.sin(ang)+bz*np.cos(ang)
                elif axis=="Parallel axis offset by d":
                    xx=bx-d
                    fx=d+xx*np.cos(ang)-by*np.sin(ang)
                    fy=xx*np.sin(ang)+by*np.cos(ang)
                    fz=bz
                else:
                    fx=bx*np.cos(ang)-by*np.sin(ang)
                    fy=bx*np.sin(ang)+by*np.cos(ang)
                    fz=bz
                color,opacity,name=mesh_styles[len(frame_data)]
                frame_data.append(go.Surface(x=fx,y=fy,z=fz,colorscale=[[0,color],[1,color]],showscale=False,opacity=opacity,name=name))
            if axis=="Central transverse axis (x)":
                tx=[0,0]; ty=[R*np.cos(ang),R*np.cos(ang+.18)]; tz=[R*np.sin(ang),R*np.sin(ang+.18)]
            elif axis=="Parallel axis offset by d":
                radial=max(0.05,R-d)
                tx=[d+radial*np.cos(ang),d+radial*np.cos(ang+.18)]; ty=[radial*np.sin(ang),radial*np.sin(ang+.18)]; tz=[0,0]
            else:
                tx=[R*np.cos(ang),R*np.cos(ang+.18)]; ty=[R*np.sin(ang),R*np.sin(ang+.18)]; tz=[0,0]
            frame_data.append(go.Scatter3d(x=tx,y=ty,z=tz,mode="markers+lines",marker=dict(size=[7,3],color=["#55f6dc","#9a7bff"]),line=dict(color="#55f6dc",width=6)))
            frame_data.append(go.Scatter(x=[ct,ct],y=[omega_lo-omega_pad,omega_hi+omega_pad],mode="lines",line=dict(color="white",width=1.7,dash="dash"),showlegend=False))
            frame_data.append(go.Scatter(x=[ct],y=[omegas[si]],mode="markers",marker=dict(size=9,color="#ffffff",line=dict(color="#55f6dc",width=2)),showlegend=False))
            frame_data.append(go.Scatter(x=[ct,ct],y=[energy_lo,energy_hi+energy_pad],mode="lines",line=dict(color="white",width=1.7,dash="dash"),showlegend=False))
            frame_data.append(go.Scatter(x=[ct],y=[energy[si]],mode="markers",marker=dict(size=9,color="#ffffff",line=dict(color="#9a7bff",width=2)),showlegend=False))
            target_traces=list(range(surface_count))+[tracer_index,omega_cursor_index,omega_dot_index,energy_cursor_index,energy_dot_index]
            frame_name=f"frame_{fi:02d}"
            frame_labels.append((frame_name,ct))
            frames.append(go.Frame(data=frame_data,traces=target_traces,name=frame_name))
        fig_sync.frames=frames
        slider_steps=[dict(method="animate",args=[[name],{"mode":"immediate","frame":{"duration":0,"redraw":True},"transition":{"duration":0}}],label=f"{tval:.1f}") for name,tval in frame_labels]
        fig_sync.update_layout(
            height=780,margin=dict(l=22,r=22,t=95,b=80),
            paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(10,15,25,.42)",
            font=dict(color="#eaf2ff",family="Space Grotesk, sans-serif"),
            scene=dict(bgcolor="rgba(0,0,0,0)",xaxis=dict(visible=False),yaxis=dict(visible=False),zaxis=dict(visible=False),aspectmode="cube"),
            xaxis=dict(title="Time (s)",gridcolor="rgba(148,163,184,.17)",zerolinecolor="rgba(148,163,184,.25)"),
            yaxis=dict(title="ω (rad/s)",gridcolor="rgba(148,163,184,.17)",zerolinecolor="rgba(148,163,184,.25)",range=[omega_lo-omega_pad,omega_hi+omega_pad]),
            xaxis2=dict(title="Time (s)",gridcolor="rgba(148,163,184,.17)",zerolinecolor="rgba(148,163,184,.25)"),
            yaxis2=dict(title="Krot (J)",gridcolor="rgba(148,163,184,.17)",zerolinecolor="rgba(148,163,184,.25)",range=[energy_lo,energy_hi+energy_pad]),
            updatemenus=[dict(type="buttons",showactive=False,x=0.02,y=1.13,xanchor="left",yanchor="top",direction="right",buttons=[
                dict(label="▶ START",method="animate",args=[None,{"frame":{"duration":animation_ms,"redraw":True},"fromcurrent":True,"transition":{"duration":0},"mode":"immediate"}]),
                dict(label="Ⅱ PAUSE",method="animate",args=[[None],{"frame":{"duration":0,"redraw":False},"mode":"immediate","transition":{"duration":0}}]),
                dict(label="↺ RESET",method="animate",args=[[frame_labels[0][0]],{"frame":{"duration":0,"redraw":True},"mode":"immediate","transition":{"duration":0}}])
            ])],
            sliders=[dict(active=0,currentvalue={"prefix":"Simulation time: ","suffix":" s","font":{"color":"#55f6dc"}},pad={"t":28},x=0.05,y=-0.12,len=0.90,steps=slider_steps)]
        )
        st.plotly_chart(fig_sync,use_container_width=True,config={"displaylogo":False,"scrollZoom":True},key="dynamics_synchronized_timeline")
    st.markdown("### Head-to-head prediction")
    challenge=st.selectbox("Which has greater angular acceleration under the same torque?",["Solid cylinder vs thin hollow cylinder","Solid sphere vs thin hollow sphere","Solid cylinder vs solid cone"],key="dyn_challenge")
    answer=st.radio("Your prediction",["First body","Second body","Equal"],horizontal=True,key="dyn_prediction")
    if st.button("REVEAL DUEL RESULT",key="dyn_reveal"):
        pairs={"Solid cylinder vs thin hollow cylinder":(0.5,1.0),"Solid sphere vs thin hollow sphere":(0.4,2/3),"Solid cylinder vs solid cone":(0.5,0.3)}
        ca,cb=pairs[challenge]
        # For same M,R,tau, smaller I means larger alpha.
        correct="First body" if ca<cb else "Second body" if cb<ca else "Equal"
        if "dyn_duel_history" not in st.session_state: st.session_state.dyn_duel_history={}
        if challenge not in st.session_state.dyn_duel_history:
            st.session_state.dyn_duel_history[challenge]=answer==correct
            if answer==correct:
                st.session_state.score+=15
                st.session_state.best=max(st.session_state.best,st.session_state.score)
        if answer==correct: st.success("Correct prediction — +15 XP!")
        else: st.info(f"Correct answer: {correct}. Since α = τ/I, the smaller I accelerates faster.")
    st.markdown("### Classroom leaderboard")
    st.caption("For a leaderboard shared persistently across devices, configure Supabase secrets as described below. Without database credentials, this leaderboard is saved for this browser session only.")
    if "dyn_leaderboard" not in st.session_state: st.session_state.dyn_leaderboard=[]
    if st.button("SAVE MY SCORE",key="dyn_save_score"):
        entry={"player":player.strip() or "Anonymous","xp":int(st.session_state.score)}
        try:
            import requests
            sb_url=st.secrets["SUPABASE_URL"].rstrip("/")
            sb_key=st.secrets["SUPABASE_ANON_KEY"]
            headers={"apikey":sb_key,"Authorization":f"Bearer {sb_key}","Content-Type":"application/json","Prefer":"return=minimal"}
            post=requests.post(sb_url+"/rest/v1/moi_leaderboard",headers=headers,json=entry,timeout=6)
            if post.ok:
                st.session_state.dyn_db_enabled=True
                st.success("Score saved to the shared leaderboard.")
            else:
                st.session_state.dyn_db_enabled=False
                st.warning(f"Shared save failed (HTTP {post.status_code}); saved to this session instead.")
                st.session_state.dyn_leaderboard.append(entry)
        except Exception:
            st.session_state.dyn_db_enabled=False
            st.session_state.dyn_leaderboard.append(entry)
            st.info("Supabase is not configured; score saved to this browser session.")
        st.rerun()
    shared_rows=None
    try:
        import requests
        sb_url=st.secrets["SUPABASE_URL"].rstrip("/")
        sb_key=st.secrets["SUPABASE_ANON_KEY"]
        resp=requests.get(sb_url+"/rest/v1/moi_leaderboard?select=player,xp,created_at&order=xp.desc&limit=20",
            headers={"apikey":sb_key,"Authorization":f"Bearer {sb_key}"},timeout=6)
        if resp.ok: shared_rows=resp.json()
    except Exception:
        shared_rows=None
    if shared_rows is not None:
        st.caption("Shared leaderboard — persisted in Supabase and visible across devices.")
        st.dataframe(shared_rows,use_container_width=True,hide_index=True)
    else:
        st.session_state.dyn_leaderboard=sorted(st.session_state.dyn_leaderboard,key=lambda x:x["xp"],reverse=True)[:20]
        if st.session_state.dyn_leaderboard:
            st.dataframe(st.session_state.dyn_leaderboard,use_container_width=True,hide_index=True)
    with st.expander("Enable a persistent, shared leaderboard across devices"):
        st.markdown("Create a Supabase table named `moi_leaderboard` with columns `id` (identity primary key), `player` (text), `xp` (integer), and `created_at` (timestamp, default now()). Add `SUPABASE_URL` and `SUPABASE_ANON_KEY` to Streamlit Cloud app secrets and enable INSERT/SELECT policies for that table. The app will use the database once configured; otherwise it keeps a session leaderboard.")
        if st.button("TEST DATABASE CONNECTION",key="dyn_test_db"):
            try:
                import requests
                url=st.secrets["SUPABASE_URL"].rstrip("/")+"/rest/v1/moi_leaderboard?select=player,xp&order=xp.desc&limit=20"
                key=st.secrets["SUPABASE_ANON_KEY"]
                resp=requests.get(url,headers={"apikey":key,"Authorization":f"Bearer {key}"},timeout=5)
                if resp.ok:
                    st.success("Database connection successful.")
                    st.dataframe(resp.json(),use_container_width=True,hide_index=True)
                else: st.error(f"Database returned HTTP {resp.status_code}. Check table policies and secrets.")
            except Exception: st.error("Database is not configured yet. Add SUPABASE_URL and SUPABASE_ANON_KEY to Streamlit Cloud secrets.")

elif page == "Torque Duel":
    st.markdown("## Torque Duel <span style='color:#55f6dc'>/ predict • compare • prove</span>", unsafe_allow_html=True)
    st.write("Two bodies, the same applied torque. Predict which accelerates faster, then reveal the physics.")
    duel_pairs = {
        "Solid cylinder vs thin hollow cylinder": ("Solid cylinder", "Thin hollow cylinder", 0.5, 1.0),
        "Solid sphere vs thin hollow sphere": ("Solid sphere", "Thin hollow sphere", 0.4, 2/3),
        "Solid cylinder vs solid cone": ("Solid cylinder", "Solid cone", 0.5, 0.3),
        "Thick hollow cylinder: inner radius test": ("Thick hollow cylinder (small bore)", "Thick hollow cylinder (large bore)", 0.5*(1+0.25**2), 0.5*(1+0.75**2))
    }
    pair_name = st.selectbox("DUEL SCENARIO", list(duel_pairs.keys()), key="duel_pair")
    body_a, body_b, coeff_a, coeff_b = duel_pairs[pair_name]
    left, right = st.columns(2, gap="large")
    with left:
        st.markdown(f'<div class="card"><span class="tag">ROTOR A</span><h3>{body_a}</h3><p class="smallmuted">Reference object</p></div>',unsafe_allow_html=True)
    with right:
        st.markdown(f'<div class="card"><span class="tag">ROTOR B</span><h3>{body_b}</h3><p class="smallmuted">Challenger object</p></div>',unsafe_allow_html=True)
    mass = st.slider("Same mass for both bodies M (kg)", 1.0, 20.0, 5.0, 0.5, key="duel_mass")
    radius = st.slider("Same outer radius R (m)", 0.2, 2.0, 1.0, 0.1, key="duel_radius")
    torque = st.slider("Same net torque τ (N·m)", 1.0, 30.0, 10.0, 0.5, key="duel_torque")
    prediction_key = "duel_prediction_" + pair_name
    prediction = st.radio("PREDICT FIRST — which body has greater angular acceleration?", [f"Rotor A — {body_a}", f"Rotor B — {body_b}", "They accelerate equally"], horizontal=True, key=prediction_key)
    if "duel_results" not in st.session_state:
        st.session_state.duel_results = {}
    result_key = f"{pair_name}|{mass}|{radius}|{torque}"
    reveal = st.button("REVEAL THE PHYSICS", use_container_width=True, key="duel_reveal")
    if reveal:
        IA, IB = coeff_a*mass*radius**2, coeff_b*mass*radius**2
        aa, ab = torque/IA, torque/IB
        expected = 0 if abs(aa-ab)<1e-9 else (1 if aa>ab else 2)
        selected = 0 if prediction.startswith("Rotor A") else 1 if prediction.startswith("Rotor B") else 2
        correct = selected == expected
        if result_key not in st.session_state.duel_results:
            st.session_state.duel_results[result_key] = correct
            if correct:
                st.session_state.score += 15
                st.session_state.best = max(st.session_state.best, st.session_state.score)
        st.session_state.duel_revealed = {"key":result_key,"correct":correct,"IA":IA,"IB":IB,"aa":aa,"ab":ab,"expected":expected,"a":body_a,"b":body_b}
    result = st.session_state.get("duel_revealed")
    if result and result["key"] == result_key:
        if result["correct"]:
            st.success("CORRECT PREDICTION · +15 XP")
        else:
            st.warning("Prediction missed. Study the comparison below — this is where the intuition develops.")
        ca, cb = st.columns(2)
        ca.metric("ROTOR A — MOMENT OF INERTIA", f'{result["IA"]:.4f} kg·m²')
        cb.metric("ROTOR B — MOMENT OF INERTIA", f'{result["IB"]:.4f} kg·m²')
        ca.metric("ROTOR A — ANGULAR ACCELERATION", f'{result["aa"]:.4f} rad/s²')
        cb.metric("ROTOR B — ANGULAR ACCELERATION", f'{result["ab"]:.4f} rad/s²')
        if result["expected"] == 2:
            st.info("Both accelerate equally: their moments of inertia are equal, and α = τ/I.")
        else:
            winner = result["a"] if result["expected"] == 0 else result["b"]
            st.info(f"{winner} accelerates faster because it has the smaller moment of inertia for the same applied torque.")
        # Side-by-side 3D visualisation with shared scale and axis.
        def duel_cylinder(radius_factor=1.0, hollow=False, sphere=False, cone=False):
            u=np.linspace(0,2*np.pi,48)
            fig=go.Figure()
            teal="#55f6dc"; purple="#9a7bff"
            if sphere:
                v=np.linspace(0,np.pi,32); U,V=np.meshgrid(u,v)
                fig.add_trace(go.Surface(x=radius_factor*np.sin(V)*np.cos(U),y=radius_factor*np.sin(V)*np.sin(U),z=radius_factor*np.cos(V),opacity=.65,colorscale=[[0,teal],[1,teal]],showscale=False))
            elif cone:
                z=np.linspace(0,1.6,28); U,Z=np.meshgrid(u,z); rr=radius_factor*(1-Z/1.6)
                fig.add_trace(go.Surface(x=rr*np.cos(U),y=rr*np.sin(U),z=Z,opacity=.65,colorscale=[[0,teal],[1,teal]],showscale=False))
            else:
                z=np.linspace(-.8,.8,24); U,Z=np.meshgrid(u,z)
                fig.add_trace(go.Surface(x=radius_factor*np.cos(U),y=radius_factor*np.sin(U),z=Z,opacity=.62,colorscale=[[0,teal],[1,teal]],showscale=False))
                if hollow:
                    rinner=radius_factor*.5
                    fig.add_trace(go.Surface(x=rinner*np.cos(U),y=rinner*np.sin(U),z=Z,opacity=.72,colorscale=[[0,purple],[1,purple]],showscale=False))
            fig.add_trace(go.Scatter3d(x=[0,0],y=[0,0],z=[-1.1,1.8],mode="lines",line=dict(color="white",width=4,dash="dash"),name="Axis"))
            fig.update_layout(height=350,margin=dict(l=0,r=0,t=12,b=0),paper_bgcolor="rgba(0,0,0,0)",font=dict(color="#eaf2ff"),showlegend=False,scene=dict(bgcolor="rgba(0,0,0,0)",xaxis=dict(visible=False,range=[-1.5,1.5]),yaxis=dict(visible=False,range=[-1.5,1.5]),zaxis=dict(visible=False,range=[-1.3,1.9]),aspectmode="cube"))
            return fig
        va,vb=st.columns(2)
        with va:
            st.plotly_chart(duel_cylinder(sphere="sphere" in result["a"].lower(),cone="cone" in result["a"].lower(),hollow="hollow" in result["a"].lower()),use_container_width=True,config={"displaylogo":False},key="duel_rotor_a_chart")
        with vb:
            st.plotly_chart(duel_cylinder(sphere="sphere" in result["b"].lower(),cone="cone" in result["b"].lower(),hollow="hollow" in result["b"].lower()),use_container_width=True,config={"displaylogo":False},key="duel_rotor_b_chart")
        st.markdown('<div class="card"><span class="tag">DUEL RULE</span><div class="bigformula">α = τ / I</div><p>With the same net torque, angular acceleration is inversely proportional to moment of inertia. Keep mass and outer radius fixed to isolate the effect of mass distribution.</p></div>',unsafe_allow_html=True)
    st.caption("XP is awarded once per unique combination of scenario and parameter values. The 3D objects are conceptual visualisations; the equations determine the numerical results.")

elif page == "Challenge Arena":
    st.markdown("## Challenge Arena <span style='color:#55f6dc'>/ prove your intuition</span>",unsafe_allow_html=True)
    st.write("One correct answer earns 10 XP. Read the explanation: understanding is the real score.")
    total=len(QUESTIONS)
    idx=st.session_state.challenge_idx % total
    q=QUESTIONS[idx]
    top1,top2,top3=st.columns(3)
    top1.metric("QUESTION",f"{idx+1:02d} / {total}")
    top2.metric("XP",st.session_state.score)
    top3.metric("COMPLETED",f"{len(st.session_state.answered)} / {total}")
    st.progress((idx+1)/total)
    st.markdown(f'<div class="card"><span class="tag">MISSION {idx+1:02d}</span><h3 style="font-size:1.5rem;margin-top:1rem">{q["q"]}</h3></div>',unsafe_allow_html=True)
    key=f"answer_{idx}"
    choice=st.radio("SELECT YOUR ANSWER",q["opts"],key=key,index=None)
    cols=st.columns([1,1,2])
    with cols[0]:
        submit=st.button("LOCK ANSWER",use_container_width=True)
    with cols[1]:
        nextq=st.button("NEXT →",use_container_width=True)
    if submit:
        if choice is None:
            st.warning("Choose an answer first.")
        elif idx not in st.session_state.answered:
            selected=q["opts"].index(choice)
            correct=selected==q["ans"]
            st.session_state.answered[idx]={"correct":correct,"choice":selected}
            if correct:
                st.session_state.score+=10
                st.session_state.best=max(st.session_state.best,st.session_state.score)
                st.session_state.quiz_feedback=("correct",q["why"])
            else:
                st.session_state.quiz_feedback=("wrong",q["why"],q["opts"][q["ans"]])
            st.rerun()
        else:
            st.info("This mission has already been scored. Move to the next question.")
    fb=st.session_state.quiz_feedback
    if fb:
        if fb[0]=="correct": st.success("CORRECT · +10 XP")
        elif fb[0]=="wrong": st.error(f"NOT QUITE · Correct answer: {fb[2]}")
        st.info(f"PHYSICS DEBRIEF: {fb[1]}")
    if nextq:
        st.session_state.challenge_idx=(idx+1)%total
        st.session_state.quiz_feedback=None
        st.rerun()
    if len(st.session_state.answered)==total:
        st.balloons()
        st.success(f"ARENA CLEARED — {sum(1 for v in st.session_state.answered.values() if v['correct'])}/{total} correct. Total XP: {st.session_state.score}.")
        if st.button("PLAY AGAIN — RESET ANSWERS"):
            st.session_state.answered={}
            st.session_state.challenge_idx=0
            st.session_state.quiz_feedback=None
            st.rerun()

elif page == "Formula Vault":
    st.markdown("## Formula Vault <span style='color:#55f6dc'>/ reference archive</span>",unsafe_allow_html=True)
    st.write("Choose the correct formula only after identifying the body and its axis.")
    formulas=[
      ("Point mass","I = mr²","A point mass at perpendicular distance r from the axis."),
      ("Thin ring / hoop","I = MR²","Central symmetry axis, perpendicular to the plane."),
      ("Solid cylinder","I = ½MR²","Longitudinal symmetry axis."),
      ("Thin hollow cylinder","I = MR²","Thin-walled cylinder, symmetry axis."),
      ("Thick hollow cylinder","I = ½M(Rₒ² + Rᵢ²)","Uniform annular cylinder, symmetry axis."),
      ("Solid sphere","I = ⅖MR²","Axis through a diameter."),
      ("Thin hollow sphere","I = ⅔MR²","Thin spherical shell, diameter."),
      ("Thick hollow sphere","I = ⅖M(Rₒ⁵ − Rᵢ⁵)/(Rₒ³ − Rᵢ³)","Uniform-density spherical shell, diameter."),
      ("Solid cone","I = 3/10 MR²","Uniform solid cone, symmetry axis."),
      ("Hollow cone","I = ½MR²","Thin conical shell, symmetry axis."),
      ("Thin rod — centre","I = ML²/12","Axis through centre, perpendicular to rod."),
      ("Thin rod — end","I = ML²/3","Axis through one end, perpendicular to rod."),
      ("Parallel-axis theorem","I = Icm + Md²","Parallel axis offset by distance d from the centre-of-mass axis."),
      ("Discrete system","I = Σmᵢrᵢ²","Sum over all particles; rᵢ is perpendicular distance to the axis."),
      ("Continuous body","I = ∫r² dm","Integrate over the entire mass distribution."),
      ("Rotational kinetic energy","K = ½Iω²","Rotation about a fixed axis."),
      ("Rotational dynamics","τnet = Iα","Net external torque about the axis.")
    ]
    for i in range(0,len(formulas),2):
        cols=st.columns(2)
        for col,item in zip(cols,formulas[i:i+2]):
            with col: st.markdown(f'<div class="card"><span class="tag">FORMULA {i+1:02d}</span><h3>{item[0]}</h3><div class="bigformula">{item[1]}</div><p class="smallmuted">{item[2]}</p></div>',unsafe_allow_html=True)
        st.write("")
    st.warning("Moment of inertia is always specified relative to an axis. Do not compare formulas until the axes are the same.")

elif page == "How to Play":
    st.markdown("## How to play <span style='color:#55f6dc'>/ field manual</span>",unsafe_allow_html=True)
    st.markdown('<div class="card"><span class="tag">THE OBJECTIVE</span><h3>Become the master of rotational inertia.</h3><p>Use the Spin Lab to explore, the Challenge Arena to test your understanding, and the Formula Vault to review equations. Progress is stored for this session.</p></div>',unsafe_allow_html=True)
    st.markdown("### The rules of the universe")
    st.markdown("""
1. **Predict first.** Before moving a slider, state what you expect to happen.
2. **Change one variable.** Keep other parameters fixed to isolate cause and effect.
3. **Explain the result.** Use the squared distance in \(I=\sum mr^2\), not memorization alone.
4. **Respect the axis.** The same body can have different moments of inertia about different axes.
5. **Earn XP.** Each first-time correct arena answer earns 10 XP.
""")
    st.markdown("### Your core equations")
    st.latex(r"I=\sum_i m_i r_i^2")
    st.latex(r"I=\int r^2\,dm")
    st.latex(r"I=I_{\mathrm{cm}}+Md^2")
    st.latex(r"\tau_{\mathrm{net}}=I\alpha")
