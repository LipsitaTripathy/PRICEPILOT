
import streamlit as st
import streamlit.components.v1 as components


INTRO_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
* { box-sizing: border-box; }

html, body {
    margin: 0;
    padding: 0;
    background: #050d1b;
    color: #f4f8ff;
    font-family: Inter, Arial, sans-serif;
}

.scene {
    position: relative;
    height: 560px;
    overflow: hidden;
    border: 1px solid rgba(40, 220, 215, .25);
    border-radius: 22px;
    background:
      radial-gradient(circle at 75% 45%, rgba(0,210,210,.18), transparent 35%),
      radial-gradient(circle at 20% 85%, rgba(100,80,255,.15), transparent 35%),
      linear-gradient(135deg, #071326, #09172b 55%, #050d1b);
}

.grid {
    position: absolute;
    inset: 0;
    opacity: .15;
    background-image:
      linear-gradient(rgba(89,153,190,.3) 1px, transparent 1px),
      linear-gradient(90deg, rgba(89,153,190,.3) 1px, transparent 1px);
    background-size: 42px 42px;
}

.content {
    position: relative;
    z-index: 2;
    height: 100%;
    display: grid;
    grid-template-columns: 1.1fr .9fr;
    align-items: center;
    gap: 20px;
    padding: 45px;
}

.eyebrow {
    color: #42e5d6;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 3px;
    text-transform: uppercase;
    animation: rise .8s both;
}

h1 {
    font-size: clamp(42px, 6vw, 76px);
    line-height: 1;
    letter-spacing: -3px;
    margin: 20px 0;
    animation: rise .9s .15s both;
}

h1 span { color: #28d9cb; }

.tagline {
    max-width: 500px;
    color: #bdcce0;
    font-size: 17px;
    line-height: 1.7;
    animation: rise .9s .3s both;
}

.pills {
    display: flex;
    flex-wrap: wrap;
    gap: 9px;
    margin-top: 25px;
}

.pill {
    padding: 9px 12px;
    border: 1px solid rgba(70,210,220,.3);
    border-radius: 30px;
    background: rgba(10,35,57,.7);
    color: #d2edf0;
    font-size: 11px;
    font-weight: 700;
}

.robot-wrap {
    display: flex;
    justify-content: center;
    align-items: center;
}

.robot {
    width: 230px;
    height: 260px;
    position: relative;
    animation: float 3s ease-in-out infinite;
    filter: drop-shadow(0 15px 30px rgba(0,220,220,.25));
}

.ear {
    position: absolute;
    top: 75px;
    width: 24px;
    height: 55px;
    border-radius: 12px;
    background: linear-gradient(90deg,#6c8da9,#e0f7ff);
    border: 2px solid #c5efff;
}

.ear.left { left: 4px; }
.ear.right { right: 4px; }

.head {
    position: absolute;
    top: 25px;
    left: 20px;
    width: 190px;
    height: 150px;
    border-radius: 45px;
    border: 3px solid #c5efff;
    background: linear-gradient(145deg,#e6f7ff,#7299b7 60%,#34516d);
    box-shadow: inset -10px -10px 20px #294765;
}

.face {
    position: absolute;
    inset: 17px;
    border-radius: 30px;
    background: #071a30;
    border: 2px solid rgba(44,229,226,.7);
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 30px;
}

.eye {
    width: 17px;
    height: 25px;
    border-radius: 50%;
    background: #47fff0;
    box-shadow: 0 0 12px #21f4e5, 0 0 25px #21f4e5;
    animation: blink 4s infinite;
}

.smile {
    position: absolute;
    bottom: 20px;
    left: 77px;
    width: 28px;
    height: 12px;
    border-bottom: 3px solid #48fff0;
    border-radius: 0 0 30px 30px;
}

.body {
    position: absolute;
    top: 170px;
    left: 52px;
    width: 126px;
    height: 80px;
    border-radius: 32px 32px 22px 22px;
    border: 2px solid #bdefff;
    background: linear-gradient(145deg,#d9f2ff,#5e86a7 65%,#274762);
}

.core {
    position: absolute;
    top: 22px;
    left: 47px;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: #20e8d9;
    box-shadow: 0 0 18px #20e8d9;
}

.chart {
    position: absolute;
    top: 35px;
    right: 45px;
    height: 85px;
    width: 115px;
    display: flex;
    align-items: end;
    gap: 8px;
    padding: 12px;
    border: 1px solid rgba(45,226,219,.5);
    border-radius: 12px;
    background: rgba(4,24,43,.7);
    transform: rotate(7deg);
}

.bar {
    flex: 1;
    border-radius: 4px 4px 0 0;
    background: linear-gradient(#3ff5e2,#1688ba);
    animation: grow 1.4s ease-in-out infinite alternate;
}

.bar:nth-child(1) { height: 30%; }
.bar:nth-child(2) { height: 48%; animation-delay: .15s; }
.bar:nth-child(3) { height: 70%; animation-delay: .3s; }
.bar:nth-child(4) { height: 95%; animation-delay: .45s; }

.sound {
    position: absolute;
    z-index: 5;
    right: 25px;
    bottom: 22px;
    padding: 10px 15px;
    border: 1px solid #28d9cb;
    border-radius: 25px;
    background: #0b263b;
    color: #75fff0;
    font-weight: 700;
    cursor: pointer;
}

.sound:hover { background: #123c50; }

.footer {
    position: absolute;
    left: 25px;
    bottom: 28px;
    color: #819ab4;
    font-size: 10px;
    letter-spacing: 1px;
}

@keyframes float {
    0%,100% { transform: translateY(0); }
    50% { transform: translateY(-13px); }
}

@keyframes blink {
    0%,45%,49%,100% { transform: scaleY(1); }
    47% { transform: scaleY(.12); }
}

@keyframes grow {
    from { transform: scaleY(.7); transform-origin: bottom; }
    to { transform: scaleY(1); transform-origin: bottom; }
}

@keyframes rise {
    from { opacity: 0; transform: translateY(18px); }
    to { opacity: 1; transform: translateY(0); }
}

@media(max-width:700px) {
    .content {
        grid-template-columns: 1fr;
        text-align: center;
        padding: 25px;
    }
    .tagline { margin: auto; }
    .pills { justify-content: center; }
    .robot-wrap { transform: scale(.8); }
    .chart { right: 10px; transform: scale(.7); }
}
</style>
</head>

<body>
<div class="scene">
    <div class="grid"></div>

    <div class="chart">
        <div class="bar"></div>
        <div class="bar"></div>
        <div class="bar"></div>
        <div class="bar"></div>
    </div>

    <div class="content">
        <section>
            <div class="eyebrow">Retail Intelligence Platform</div>

            <h1>PRICE<span>PILOT</span></h1>

            <div class="tagline">
                Predict demand. Optimize pricing. Make smarter
                retail decisions with one connected intelligence dashboard.
            </div>

            <div class="pills">
                <div class="pill">DEMAND FORECASTING</div>
                <div class="pill">SCENARIO PRICING</div>
                <div class="pill">MODEL INSIGHTS</div>
            </div>
        </section>

        <section class="robot-wrap">
            <div class="robot">
                <div class="ear left"></div>
                <div class="ear right"></div>
                <div class="head">
                    <div class="face">
                        <div class="eye"></div>
                        <div class="eye"></div>
                        <div class="smile"></div>
                    </div>
                </div>
                <div class="body">
                    <div class="core"></div>
                </div>
            </div>
        </section>
    </div>

    <div class="footer">PRICEPILOT · VERSION 3.0</div>

    <button class="sound" id="soundButton">♪ Enable sound</button>
</div>

<script>
const soundButton = document.getElementById("soundButton");

soundButton.addEventListener("click", async () => {
    const AudioContext = window.AudioContext || window.webkitAudioContext;

    if (!AudioContext) {
        soundButton.textContent = "Sound unavailable";
        return;
    }

    const context = new AudioContext();
    await context.resume();

    const master = context.createGain();
    master.gain.value = 0.07;
    master.connect(context.destination);

    function playTone(frequency, start, duration, type) {
        const oscillator = context.createOscillator();
        const volume = context.createGain();

        oscillator.type = type;
        oscillator.frequency.value = frequency;

        volume.gain.setValueAtTime(0.0001, context.currentTime + start);
        volume.gain.exponentialRampToValueAtTime(
            0.5, context.currentTime + start + 0.04
        );
        volume.gain.exponentialRampToValueAtTime(
            0.0001, context.currentTime + start + duration
        );

        oscillator.connect(volume);
        volume.connect(master);

        oscillator.start(context.currentTime + start);
        oscillator.stop(context.currentTime + start + duration);
    }

    playTone(440, 0, .28, "sine");
    playTone(554, .16, .32, "sine");
    playTone(659, .34, .42, "sine");
    playTone(880, .62, .55, "triangle");

    soundButton.textContent = "♪ Sound played";

    setTimeout(() => context.close(), 1800);
});
</script>
</body>
</html>
"""


def render_intro():
    components.html(INTRO_HTML, height=580, scrolling=False)

    st.markdown(
        """
        <style>
        div.stButton > button {
            min-height: 54px;
            border-radius: 14px;
            background: linear-gradient(100deg,#13cfc0,#397de8);
            border: 1px solid #40e5dc;
            color: #031321 !important;
            font-size: 17px;
            font-weight: 800;
            padding: 12px 24px;
        }
        div.stButton > button p {
            color: #031321 !important;
            font-weight: 800 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    left, center, right = st.columns([1, 2, 1])

    with center:
        return st.button(
            "Launch PRICEPILOT  →",
            key="pricepilot_launch",
            use_container_width=True,
            type="primary"
        )
