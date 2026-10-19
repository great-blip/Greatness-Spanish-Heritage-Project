import html
import json
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hello World Motion Lab", page_icon="✨", layout="wide")

st.title("✨ Hello World Motion Lab")
st.caption("A tiny app for experimenting with names, typography, backgrounds, and looping motion.")

# -----------------------------
# Controls
# -----------------------------
with st.sidebar:
    st.header("Customize your app")
    name = st.text_input("Your name or message", value="Hello World", max_chars=80)

    font_family = st.selectbox(
        "Font type",
        ["Arial", "Courier New", "Georgia", "Times New Roman", "Verdana", "Trebuchet MS", "Impact"],
    )
    font_size = st.slider("Font size", min_value=20, max_value=100, value=52, step=2)

    background = st.selectbox(
        "Background",
        [
            "Light",
            "Dark",
            "Ocean",
            "Sunset",
            "Forest",
            "Lavender",
            "Midnight Gradient",
            "Candy",
        ],
    )
    display_mode = st.selectbox(
        "Name display mode",
        ["Centered", "Ticker Tape", "Repeated"],
    )
    effect = st.selectbox(
        "Dynamic action",
        ["None", "Rain", "Snow", "Hail", "Wind Gust", "Confetti", "Tornado"],
    )
    speed = st.slider(
        "Animation speed",
        min_value=1,
        max_value=10,
        value=5,
        help="1 is slow and gentle; 10 is fast.",
    )
    effect_amount = st.slider("Effect amount", min_value=10, max_value=80, value=36, step=2)

backgrounds = {
    "Light": ("#f8fafc", "#111827", "linear-gradient(135deg, #f8fafc, #e2e8f0)"),
    "Dark": ("#050816", "#ffffff", "linear-gradient(135deg, #050816, #172033)"),
    "Ocean": ("#063b52", "#f0fdff", "linear-gradient(135deg, #075985, #0f766e)"),
    "Sunset": ("#451a45", "#fff7ed", "linear-gradient(135deg, #7c2d12, #be185d, #312e81)"),
    "Forest": ("#123524", "#f0fdf4", "linear-gradient(135deg, #14532d, #365314)"),
    "Lavender": ("#ede9fe", "#312e81", "linear-gradient(135deg, #ddd6fe, #f5d0fe)"),
    "Midnight Gradient": ("#111827", "#fef3c7", "linear-gradient(135deg, #111827, #312e81, #701a75)"),
    "Candy": ("#fff1f2", "#831843", "linear-gradient(135deg, #fbcfe8, #bfdbfe, #fde68a)"),
}
fallback_bg, text_color, background_css = backgrounds[background]

# Escape user-entered text before inserting it into HTML.
safe_name = html.escape(name or "Hello World", quote=True)
safe_font = font_family.replace("'", "").replace('"', "")
safe_speed = max(1, min(10, int(speed)))
duration = 11 - safe_speed  # 10 seconds at speed 1; 1 second at speed 10

# Font stacks
font_stacks = {
    "Arial": "Arial, Helvetica, sans-serif",
    "Courier New": "'Courier New', Courier, monospace",
    "Georgia": "Georgia, serif",
    "Times New Roman": "'Times New Roman', Times, serif",
    "Verdana": "Verdana, Geneva, sans-serif",
    "Trebuchet MS": "'Trebuchet MS', sans-serif",
    "Impact": "Impact, Haettenschweiler, sans-serif",
}
font_stack = font_stacks.get(safe_font, "Arial, sans-serif")

effect_config = {
    "None": {"symbol": "", "kind": "none", "color": "#ffffff"},
    "Rain": {"symbol": "💧", "kind": "rain", "color": "#60a5fa"},
    "Snow": {"symbol": "❄", "kind": "snow", "color": "#ffffff"},
    "Hail": {"symbol": "🧊", "kind": "hail", "color": "#bae6fd"},
    "Wind Gust": {"symbol": "〰", "kind": "wind", "color": "#d1fae5"},
    "Confetti": {"symbol": "🎉", "kind": "confetti", "color": "#f9a8d4"},
    "Tornado": {"symbol": "🌪", "kind": "tornado", "color": "#e5e7eb"},
}
cfg = effect_config[effect]
config_json = json.dumps({
    "kind": cfg["kind"],
    "symbol": cfg["symbol"],
    "count": int(effect_amount),
    "duration": duration,
})

# Display modes use CSS animations; no Python rerun loop is needed.
if display_mode == "Ticker Tape":
    name_markup = f'<div class="ticker-track"><span class="name-text">{safe_name}</span><span class="name-text" aria-hidden="true">{safe_name}</span></div>'
elif display_mode == "Repeated":
    name_markup = '<div class="repeat-grid">' + "".join(
        f'<span class="name-text">{safe_name}</span>' for _ in range(6)
    ) + '</div>'
else:
    name_markup = f'<div class="center-name"><span class="name-text">{safe_name}</span></div>'

html_doc = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  * {{ box-sizing: border-box; }}
  html, body {{ margin: 0; padding: 0; }}
  body {{ font-family: {font_stack}; }}
  .stage {{
    position: relative;
    isolation: isolate;
    height: 620px;
    width: 100%;
    overflow: hidden;
    border-radius: 20px;
    background: {background_css};
    color: {text_color};
    box-shadow: 0 12px 34px rgba(15, 23, 42, .18);
  }}
  .stage::before {{
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at 50% 40%, rgba(255,255,255,.14), transparent 52%);
    pointer-events: none;
    z-index: -1;
  }}
  .effect-layer {{ position: absolute; inset: 0; overflow: hidden; pointer-events: none; z-index: 1; }}
  .particle {{
    position: absolute;
    top: -12%;
    left: var(--x);
    font-size: var(--size);
    opacity: var(--opacity, .85);
    animation: var(--animation) var(--duration) var(--delay) infinite linear;
    filter: drop-shadow(0 2px 3px rgba(0,0,0,.12));
    user-select: none;
    will-change: transform;
  }}
  .center-name {{
    position: absolute; z-index: 5; inset: 0; display: flex;
    align-items: center; justify-content: center; padding: 30px;
    text-align: center; overflow-wrap: anywhere;
  }}
  .name-text {{
    display: inline-block;
    font-size: {font_size}px;
    line-height: 1.15;
    font-weight: 800;
    text-shadow: 0 3px 16px rgba(0,0,0,.22);
  }}
  .center-name .name-text {{ animation: namePulse 3.2s ease-in-out infinite; }}
  .ticker-track {{
    position: absolute; z-index: 5; top: 44%; left: 0; display: flex;
    align-items: center; gap: 80px; white-space: nowrap;
    width: max-content; animation: ticker {max(5, duration * 1.4)}s linear infinite;
  }}
  .ticker-track .name-text {{ padding-right: 18px; }}
  .repeat-grid {{
    position: absolute; z-index: 5; inset: 0; padding: 28px;
    display: grid; grid-template-columns: repeat(2, minmax(0, 1fr));
    grid-template-rows: repeat(3, 1fr); gap: 10px; align-items: center;
    justify-items: center; text-align: center; overflow-wrap: anywhere;
  }}
  .repeat-grid .name-text {{ font-size: {max(16, int(font_size * .62))}px; animation: namePulse 3.2s ease-in-out infinite; }}
  .repeat-grid .name-text:nth-child(even) {{ animation-delay: -1.4s; }}
  .hint {{
    position: absolute; z-index: 6; left: 16px; bottom: 12px;
    font: 12px/1.3 Arial, sans-serif; opacity: .72; letter-spacing: .04em;
  }}
  @keyframes fall {{ from {{ transform: translate3d(0,-5vh,0) rotate(0deg); }} to {{ transform: translate3d(var(--drift), 115vh,0) rotate(360deg); }} }}
  @keyframes snow {{ from {{ transform: translate3d(0,-5vh,0) rotate(0deg); }} 50% {{ transform: translate3d(var(--drift),50vh,0) rotate(180deg); }} to {{ transform: translate3d(calc(var(--drift) * -1),115vh,0) rotate(360deg); }} }}
  @keyframes gust {{ 0% {{ transform: translate3d(-25vw,0,0) rotate(0deg); opacity: 0; }} 15% {{ opacity: .9; }} 100% {{ transform: translate3d(125vw, var(--drift),0) rotate(220deg); opacity: 0; }} }}
  @keyframes confetti {{ 0% {{ transform: translate3d(0,-10vh,0) rotate(0deg); }} 100% {{ transform: translate3d(var(--drift),115vh,0) rotate(900deg); }} }}
  @keyframes tornado {{ 0% {{ transform: translate3d(0,-10vh,0) rotate(0deg) scale(.65); }} 50% {{ transform: translate3d(var(--drift),50vh,0) rotate(360deg) scale(1.1); }} 100% {{ transform: translate3d(0,115vh,0) rotate(720deg) scale(.65); }} }}
  @keyframes namePulse {{ 0%,100% {{ transform: scale(1); }} 50% {{ transform: scale(1.035); }} }}
  @keyframes ticker {{ from {{ transform: translateX(0); }} to {{ transform: translateX(-50%); }} }}
  @media (prefers-reduced-motion: reduce) {{
    .particle, .center-name .name-text, .repeat-grid .name-text, .ticker-track {{ animation-duration: 30s !important; }}
  }}
</style>
</head>
<body>
<div class="stage">
  <div class="effect-layer" id="effects" aria-hidden="true"></div>
  {name_markup}
  <div class="hint">HELLO WORLD · MOTION LAB</div>
</div>
<script>
(() => {{
  const cfg = {config_json};
  const layer = document.getElementById("effects");
  if (!layer || cfg.kind === "none") return;
  const random = (min, max) => Math.random() * (max - min) + min;
  const colors = ["#f472b6", "#facc15", "#34d399", "#60a5fa", "#c084fc", "#fb7185", "#ffffff"];
  for (let i = 0; i < cfg.count; i++) {{
    const el = document.createElement("span");
    el.className = "particle";
    el.textContent = cfg.kind === "confetti"
      ? ["✦", "●", "■", "▲", "🎉"][Math.floor(Math.random() * 5)]
      : cfg.symbol;
    const x = random(0, 100);
    const size = cfg.kind === "hail" ? random(15, 25) : random(13, 25);
    const delay = random(-cfg.duration, 0);
    let animation = "fall";
    if (cfg.kind === "snow") animation = "snow";
    if (cfg.kind === "wind") animation = "gust";
    if (cfg.kind === "confetti") animation = "confetti";
    if (cfg.kind === "tornado") animation = "tornado";
    el.style.setProperty("--x", x + "%");
    el.style.setProperty("--size", size + "px");
    el.style.setProperty("--delay", delay + "s");
    el.style.setProperty("--duration", (cfg.kind === "wind" ? random(2, 4) : random(cfg.duration * .65, cfg.duration * 1.35)) + "s");
    el.style.setProperty("--drift", random(-110, 110) + "px");
    el.style.setProperty("--opacity", random(.45, .95));
    el.style.setProperty("--animation", animation);
    if (cfg.kind === "confetti") el.style.color = colors[Math.floor(Math.random() * colors.length)];
    if (cfg.kind === "tornado") {{
      el.style.left = (50 + random(-22, 22)) + "%";
      el.style.fontSize = random(16, 32) + "px";
    }}
    layer.appendChild(el);
  }}
}})();
</script>
</body>
</html>
"""

st.markdown("### Live preview")
components.html(html_doc, height=640, scrolling=False)
st.caption("Tip: choose an effect in the sidebar. The particles animate continuously inside the preview without repeatedly rerunning the Streamlit app.")
