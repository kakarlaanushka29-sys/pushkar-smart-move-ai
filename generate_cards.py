import os
from playwright.sync_api import sync_playwright

CARDS = [
    {
        "filename": "00_intro.png",
        "tag": "GODAVARI PUSHKARALU 2027 • PROBLEM PS-05",
        "title": "PUSHKAR SMART MOVE AI",
        "tagline": "Smarter Mobility. Safer Pilgrimages.",
        "desc": "Integrated Pilgrim Mobility, Live Parking, Shuttle Coordination & Emergency Safety System",
        "badge": "STAFF-IN-THE-LOOP DEMO",
        "accent": "#f59e0b"
    },
    {
        "filename": "01_parking.png",
        "tag": "MODULE 01 • INTELLIGENT COMMUTE",
        "title": "Journey Plan & Smart Parking",
        "tagline": "Real-time Occupancy Tracking & Proactive Diversion",
        "desc": "Guides pilgrims to available parking (Parking B) when primary lots (Parking A) reach capacity, coordinating connecting shuttles.",
        "badge": "SIMULATED / STAFF-ENTERED DATA",
        "accent": "#38bdf8"
    },
    {
        "filename": "02_sos.png",
        "tag": "MODULE 02 • EMERGENCY RESPONSE",
        "title": "One-Touch Pilgrim SOS",
        "tagline": "Rapid Incident Reporting with Real-Time Feedback",
        "desc": "Pilgrims report emergencies with GPS/location. Command staff assign teams while pilgrim watches live status progression.",
        "badge": "PROTOTYPE ONLY • IN REAL EMERGENCY CALL 112",
        "accent": "#ef4444"
    },
    {
        "filename": "03_crowd.png",
        "tag": "MODULE 03 • CROWD SAFETY",
        "title": "Staff-Verified Crowd Diversion",
        "tagline": "Human-in-the-Loop Protocol to Prevent Stampedes",
        "desc": "AI suggests diversion when critical crowd density is reported; safety alerts broadcast ONLY after field staff approval.",
        "badge": "ZERO UNVERIFIED ALERTS",
        "accent": "#f97316"
    },
    {
        "filename": "04_languages.png",
        "tag": "MODULE 04 • INCLUSIVE ACCESSIBILITY",
        "title": "Multi-Lingual Localization",
        "tagline": "English • తెలుగు (Telugu) • हिन्दी (Hindi)",
        "desc": "Accessible to millions of regional pilgrims across Andhra Pradesh, Telangana, and pan-India devotees.",
        "badge": "DRAFT TEXTS PENDING NATIVE REVIEW",
        "accent": "#a855f7"
    },
    {
        "filename": "05_outro.png",
        "tag": "PUSHKAR SMART MOVE AI • VISION",
        "title": "Next Milestones: 2027 Pilot",
        "tagline": "From Smart Prototype to Full-Scale Pilgrim Protection",
        "desc": "• Live IoT sensor feeds & ANPR camera integration\n• Interactive GIS map & zone geo-fencing\n• 1-Ghat field pilot at Rajahmundry",
        "badge": "GODAVARI PUSHKARALU 2027",
        "accent": "#10b981"
    }
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    width: 1280px;
    height: 720px;
    background: radial-gradient(circle at 80% 20%, #1e3a8a 0%, #0f172a 60%, #030712 100%);
    color: #ffffff;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 60px 80px;
    overflow: hidden;
    position: relative;
  }}
  .glow {{
    position: absolute;
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, {accent}22 0%, transparent 70%);
    top: -150px;
    right: -150px;
    pointer-events: none;
  }}
  .glow-left {{
    position: absolute;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, #3b82f615 0%, transparent 70%);
    bottom: -100px;
    left: -100px;
    pointer-events: none;
  }}
  .top-bar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    z-index: 2;
  }}
  .tag {{
    font-size: 14px;
    font-weight: 800;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: {accent};
    background: rgba(255, 255, 255, 0.05);
    padding: 8px 18px;
    border-radius: 999px;
    border: 1px solid {accent}44;
  }}
  .badge {{
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1px;
    color: #fbbf24;
    background: rgba(245, 158, 11, 0.15);
    padding: 6px 16px;
    border-radius: 6px;
    border: 1px solid rgba(245, 158, 11, 0.4);
  }}
  .content {{
    position: relative;
    z-index: 2;
    margin-top: auto;
    margin-bottom: auto;
  }}
  .title {{
    font-size: 52px;
    font-weight: 900;
    line-height: 1.15;
    margin-bottom: 16px;
    letter-spacing: -0.5px;
    background: linear-gradient(180deg, #ffffff 40%, #cbd5e1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }}
  .tagline {{
    font-size: 26px;
    font-weight: 600;
    color: {accent};
    margin-bottom: 22px;
  }}
  .desc {{
    font-size: 19px;
    line-height: 1.6;
    color: #94a3b8;
    max-width: 950px;
    white-space: pre-line;
  }}
  .footer {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    padding-top: 24px;
    font-size: 15px;
    color: #64748b;
    position: relative;
    z-index: 2;
  }}
  .footer-highlight {{
    color: #e2e8f0;
    font-weight: 600;
  }}
</style>
</head>
<body>
  <div class="glow"></div>
  <div class="glow-left"></div>
  <div class="top-bar">
    <div class="tag">{tag}</div>
    <div class="badge">⚠️ {badge}</div>
  </div>
  <div class="content">
    <h1 class="title">{title}</h1>
    <div class="tagline">{tagline}</div>
    <div class="desc">{desc}</div>
  </div>
  <div class="footer">
    <div>Project: <span class="footer-highlight">Pushkar Smart Move AI</span></div>
    <div>Safety Protocol: <span class="footer-highlight">Human-in-the-Loop Staff Verification</span></div>
  </div>
</body>
</html>
"""

def generate_cards():
    out_dir = os.path.join(os.path.dirname(__file__), "demo_video", "cards")
    os.makedirs(out_dir, exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        
        for c in CARDS:
            html = HTML_TEMPLATE.format(**c)
            page.set_content(html)
            page.wait_for_timeout(300)
            target = os.path.join(out_dir, c["filename"])
            page.screenshot(path=target)
            print(f"Generated {target}")
            
        browser.close()

if __name__ == "__main__":
    generate_cards()
