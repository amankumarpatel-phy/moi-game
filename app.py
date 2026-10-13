import math
import random
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="MOI QUEST | Aman Edge Physics", page_icon="◉", layout="wide", initial_sidebar_state="expanded")

# ---------- Visual system ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;600;700&display=swap');
:root{--bg:#080b12;--panel:#111827;--line:rgba(148,163,184,.18);--cyan:#55f6dc;--violet:#9a7bff;--muted:#9ba8bc;--white:#f4f7ff}
html,body,[class*="css"]{font-family:'Space Grotesk',sans-serif}
.stApp{background:radial-gradient(ellipse at 12% 0%,rgba(78,65,160,.19),transparent 35%),radial-gradient(ellipse at 88% 12%,rgba(28,202,180,.12),transparent 28%),var(--bg);color:var(--white)}
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

# ---------- Physics engine ----------
FORMULAS = {
    "Thin ring (central axis)": ("Ring", lambda m,r,l: m*r*r, "I = MR²", "All the mass lies at approximately the same radius."),
    "Solid disc / cylinder (central axis)": ("Disc", lambda m,r,l: 0.5*m*r*r, "I = ½MR²", "Mass is distributed from the axis to the rim."),
    "Solid sphere (diameter)": ("Sphere", lambda m,r,l: 0.4*m*r*r, "I = ⅖MR²", "For a uniform solid sphere about a diameter."),
    "Thin spherical shell (diameter)": ("Shell", lambda m,r,l: (2/3)*m*r*r, "I = ⅔MR²", "The mass is concentrated on the spherical surface."),
    "Thin rod (centre, perpendicular)": ("Rod", lambda m,r,l: m*l*l/12, "I = ML²/12", "The axis passes through the centre and is perpendicular to the rod."),
    "Thin rod (end, perpendicular)": ("Rod end", lambda m,r,l: m*l*l/3, "I = ML²/3", "The axis is perpendicular to the rod and passes through one end."),
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

def calc_I(shape, mass, radius, length):
    return FORMULAS[shape][1](mass, radius, length)

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
    page = st.radio("NAVIGATION", ["Mission Control", "Spin Lab", "Challenge Arena", "Formula Vault", "How to Play"], label_visibility="collapsed")
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
        radius = st.slider("Radius R (m)", 0.1, 2.0, 0.8, 0.1)
        length = st.slider("Length L (m) — for rods", 0.2, 4.0, 2.0, 0.1)
        torque = st.slider("Net applied torque τ (N·m)", 0.0, 30.0, 8.0, 0.5)
        omega = st.slider("Initial angular speed ω₀ (rad/s)", 0.0, 20.0, 3.0, 0.5)
        duration = st.slider("Simulation time (s)", 1.0, 8.0, 4.0, 0.5)
        friction = st.slider("Opposing friction torque (N·m)", 0.0, 10.0, 0.5, 0.5)
    with b:
        I = calc_I(shape,mass,radius,length)
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
      const kind='{FORMULAS[shape][0]}';
      if(kind==='Rod'||kind==='Rod end'){{x.strokeStyle='#55f6dc';x.lineWidth=10;x.lineCap='round';x.beginPath();x.moveTo(kind==='Rod end'?-R:-R,0);x.lineTo(R,0);x.stroke();for(let i=0;i<9;i++){{let px=-R+2*R*i/8;x.fillStyle='#b8fff4';x.beginPath();x.arc(px,0,3,0,Math.PI*2);x.fill();}}}}
      else if(kind==='Ring'||kind==='Shell'){{x.strokeStyle='#55f6dc';x.lineWidth=8;x.beginPath();x.arc(0,0,R,0,Math.PI*2);x.stroke();for(let i=0;i<20;i++){{let a=i*Math.PI/10;x.fillStyle='#d9fff9';x.beginPath();x.arc(R*Math.cos(a),R*Math.sin(a),3,0,Math.PI*2);x.fill();}}}}
      else if(kind==='Sphere'){{x.strokeStyle='#55f6dc';x.lineWidth=5;x.beginPath();x.arc(0,0,R,0,Math.PI*2);x.stroke();x.strokeStyle='#9a7bff';x.beginPath();x.ellipse(0,0,R*.42,R,0,0,Math.PI*2);x.stroke();x.beginPath();x.ellipse(0,0,R,R*.42,0,0,Math.PI*2);x.stroke();}}
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
      ("Solid disc / cylinder","I = ½MR²","Central symmetry axis."),
      ("Solid sphere","I = ⅖MR²","Axis through a diameter."),
      ("Thin spherical shell","I = ⅔MR²","Axis through a diameter."),
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
    st.markdown("### Footer & credit")
    st.code("© 2026 Aman Edge Physics | Designed & developed by Aman Kumar Patel | Educational use")
    st.caption("The footer is part of the app layout and will appear at the bottom of every section.")

# Footer is intentionally global.
st.markdown("""
<div class="footer">
  <div><strong>MOI QUEST</strong> <span class="accent">×</span> <strong>AMAN EDGE PHYSICS</strong><br>Learn the laws. Feel the motion. Master the spin.</div>
  <div style="text-align:right">Designed &amp; developed by <strong>Aman Kumar Patel</strong><br>© 2026 Aman Edge Physics · For educational use</div>
</div>
""",unsafe_allow_html=True)
