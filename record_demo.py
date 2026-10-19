import os
import sys
import time
import shutil
import subprocess
import requests
from playwright.sync_api import sync_playwright

API = "http://127.0.0.1:8000"
WEB = "http://localhost:5173"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEMO_DIR = os.path.join(BASE_DIR, "demo_video")
CARDS_DIR = os.path.join(DEMO_DIR, "cards")
TEMP_DIR = os.path.join(DEMO_DIR, "temp_rec")

# Find ffmpeg and ffprobe
def get_ffmpeg():
    if shutil.which("ffmpeg"):
        return "ffmpeg"
    winget_link = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Links\ffmpeg.exe")
    if os.path.exists(winget_link):
        return winget_link
    raise RuntimeError("ffmpeg not found! Please install ffmpeg.")

def get_ffprobe():
    if shutil.which("ffprobe"):
        return "ffprobe"
    winget_link = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Links\ffprobe.exe")
    if os.path.exists(winget_link):
        return winget_link
    return "ffprobe"

FFMPEG = get_ffmpeg()
FFPROBE = get_ffprobe()

INJECT_OVERLAYS_JS = """
(() => {
  const isPilgrim = window.location.hash !== '#admin';
  
  // 1. Header Bar
  const topBar = document.createElement('div');
  topBar.id = 'demo-topbar';
  topBar.style.position = 'sticky';
  topBar.style.top = '0';
  topBar.style.left = '0';
  topBar.style.right = '0';
  topBar.style.zIndex = '99999';
  topBar.style.padding = '8px 16px';
  topBar.style.fontWeight = 'bold';
  topBar.style.fontSize = '13px';
  topBar.style.display = 'flex';
  topBar.style.justifyContent = 'space-between';
  topBar.style.alignItems = 'center';
  topBar.style.boxShadow = '0 2px 6px rgba(0,0,0,0.15)';
  
  if (isPilgrim) {
    topBar.style.background = 'linear-gradient(90deg, #1d4ed8, #2563eb)';
    topBar.style.color = '#ffffff';
    topBar.innerHTML = '<span>📱 PILGRIM INTERFACE (Mobile Web)</span><span style="font-size:11px; font-weight:600; opacity:0.9;">Godavari Pushkaralu 2027</span>';
  } else {
    topBar.style.background = 'linear-gradient(90deg, #991b1b, #dc2626)';
    topBar.style.color = '#ffffff';
    topBar.innerHTML = '<span>💻 COMMAND CENTER (Admin & Staff)</span><span style="font-size:11px; font-weight:600; opacity:0.9;">Staff Verification Console</span>';
  }
  document.body.insertBefore(topBar, document.body.firstChild);

  // 2. Amber Simulated Data Badge
  const badge = document.createElement('div');
  badge.id = 'demo-sim-badge';
  badge.style.position = 'fixed';
  badge.style.bottom = '64px';
  badge.style.right = '12px';
  badge.style.background = '#f59e0b';
  badge.style.color = '#0f172a';
  badge.style.fontWeight = '800';
  badge.style.fontSize = '11px';
  badge.style.padding = '4px 10px';
  badge.style.borderRadius = '4px';
  badge.style.boxShadow = '0 2px 8px rgba(0,0,0,0.3)';
  badge.style.zIndex = '99998';
  badge.style.letterSpacing = '0.5px';
  badge.innerText = '⚠️ SIMULATED DATA';
  document.body.appendChild(badge);

  // 3. Bottom Caption Banner
  const caption = document.createElement('div');
  caption.id = 'demo-caption-banner';
  caption.style.position = 'fixed';
  caption.style.bottom = '0';
  caption.style.left = '0';
  caption.style.right = '0';
  caption.style.height = '52px';
  caption.style.background = 'rgba(15, 23, 42, 0.96)';
  caption.style.borderTop = '2px solid #38bdf8';
  caption.style.color = '#ffffff';
  caption.style.fontSize = '13px';
  caption.style.fontWeight = '600';
  caption.style.display = 'flex';
  caption.style.alignItems = 'center';
  caption.style.padding = '0 16px';
  caption.style.boxShadow = '0 -4px 12px rgba(0,0,0,0.3)';
  caption.style.zIndex = '99999';
  
  const tag = isPilgrim ? 
    '<span style="background:#2563eb; color:white; padding:3px 8px; border-radius:4px; font-size:11px; margin-right:8px; font-weight:700;">PILGRIM</span>' :
    '<span style="background:#dc2626; color:white; padding:3px 8px; border-radius:4px; font-size:11px; margin-right:8px; font-weight:700;">ADMIN</span>';
    
  caption.innerHTML = tag + '<span id="caption-text"></span>';
  document.body.appendChild(caption);

  window.setDemoCaption = (text) => {
    const el = document.getElementById('caption-text');
    if (el) el.innerText = text;
  };

  // 4. Custom Cursor & Click Ripple
  const cursor = document.createElement('div');
  cursor.id = 'demo-cursor';
  cursor.style.position = 'fixed';
  cursor.style.width = '20px';
  cursor.style.height = '20px';
  cursor.style.borderRadius = '50%';
  cursor.style.backgroundColor = 'rgba(239, 68, 68, 0.95)';
  cursor.style.border = '2px solid #ffffff';
  cursor.style.boxShadow = '0 0 10px rgba(0,0,0,0.5)';
  cursor.style.pointerEvents = 'none';
  cursor.style.zIndex = '999999';
  cursor.style.transform = 'translate(-50%, -50%)';
  cursor.style.display = 'none';
  document.body.appendChild(cursor);

  document.addEventListener('mousemove', (e) => {
    cursor.style.display = 'block';
    cursor.style.left = e.clientX + 'px';
    cursor.style.top = e.clientY + 'px';
  });

  document.addEventListener('click', (e) => {
    const ring = document.createElement('div');
    ring.style.position = 'fixed';
    ring.style.left = e.clientX + 'px';
    ring.style.top = e.clientY + 'px';
    ring.style.width = '24px';
    ring.style.height = '24px';
    ring.style.borderRadius = '50%';
    ring.style.border = '3px solid #f59e0b';
    ring.style.pointerEvents = 'none';
    ring.style.zIndex = '999998';
    ring.style.transform = 'translate(-50%, -50%) scale(1)';
    ring.style.transition = 'transform 0.4s ease-out, opacity 0.4s ease-out';
    ring.style.opacity = '1';
    document.body.appendChild(ring);
    requestAnimationFrame(() => {
      ring.style.transform = 'translate(-50%, -50%) scale(2.5)';
      ring.style.opacity = '0';
    });
    setTimeout(() => ring.remove(), 450);
  });
})();
"""

def reset_backend_data():
    """Reset backend state to clean default values"""
    print("Resetting backend demo data...")
    try:
        requests.put(f"{API}/parking/1", json={"occupied": 980}, timeout=5)
        requests.put(f"{API}/parking/2", json={"occupied": 500}, timeout=5)
        requests.put(f"{API}/crowd/1", json={"level": "NORMAL", "approved": False}, timeout=5)
        requests.put(f"{API}/crowd/2", json={"level": "NORMAL", "approved": False}, timeout=5)
        requests.put(f"{API}/crowd/3", json={"level": "NORMAL", "approved": False}, timeout=5)
        requests.put(f"{API}/shuttle/1", json={"waiting": 30, "running": 2, "status": "Running"}, timeout=5)
        requests.put(f"{API}/shuttle/2", json={"waiting": 40, "running": 2, "status": "Running"}, timeout=5)
        requests.put(f"{API}/traffic/1", json={"level": "HIGH", "closed": False, "time_min": 25}, timeout=5)
        requests.put(f"{API}/traffic/2", json={"level": "MODERATE", "closed": False, "time_min": 18}, timeout=5)
        requests.put(f"{API}/traffic/3", json={"level": "LOW", "closed": False, "time_min": 22}, timeout=5)
    except Exception as e:
        print("Warning resetting backend:", e)

def smooth_move(page, target_selector, steps=25):
    el = page.wait_for_selector(target_selector)
    box = el.bounding_box()
    if box:
        tx = box["x"] + box["width"] / 2
        ty = box["y"] + box["height"] / 2
        page.mouse.move(tx, ty, steps=steps)
        return tx, ty
    return 0, 0

def smooth_click(page, target_selector, steps=25, delay=1.5):
    tx, ty = smooth_move(page, target_selector, steps=steps)
    page.wait_for_timeout(300)
    page.mouse.click(tx, ty)
    page.wait_for_timeout(int(delay * 1000))

def smooth_scroll(page, delta_y, steps=12, step_delay=50):
    per_step = delta_y / steps
    for _ in range(steps):
        page.mouse.wheel(0, per_step)
        page.wait_for_timeout(step_delay)
    page.wait_for_timeout(1000)

def set_caption(pilgrim_page, admin_page, text):
    if pilgrim_page:
        pilgrim_page.evaluate("(t) => window.setDemoCaption(t)", text)
    if admin_page:
        admin_page.evaluate("(t) => window.setDemoCaption(t)", text)

def make_card_video(png_name, duration_sec, out_mp4):
    in_png = os.path.join(CARDS_DIR, png_name)
    cmd = [
        FFMPEG, "-y",
        "-loop", "1",
        "-t", str(duration_sec),
        "-i", in_png,
        "-c:v", "libx264",
        "-crf", "30",
        "-preset", "slow",
        "-pix_fmt", "yuv420p",
        "-r", "24",
        out_mp4
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Generated card clip: {out_mp4} ({duration_sec}s)")

def hstack_videos(video_left, video_right, out_mp4):
    cmd = [
        FFMPEG, "-y",
        "-i", video_left,
        "-i", video_right,
        "-filter_complex", "[0:v][1:v]hstack=inputs=2[v]",
        "-map", "[v]",
        "-c:v", "libx264",
        "-crf", "30",
        "-preset", "slow",
        "-pix_fmt", "yuv420p",
        "-r", "24",
        out_mp4
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Hstacked into: {out_mp4}")

def record_scene1(playwright):
    """SCENE 1: PARKING (32s)"""
    print("\n--- Recording Scene 1: Parking ---")
    reset_backend_data()
    rec_dir = os.path.join(TEMP_DIR, "s1")
    os.makedirs(rec_dir, exist_ok=True)

    browser = playwright.chromium.launch()
    c_p = browser.new_context(viewport={"width": 640, "height": 720}, record_video_dir=rec_dir, record_video_size={"width": 640, "height": 720})
    c_a = browser.new_context(viewport={"width": 640, "height": 720}, record_video_dir=rec_dir, record_video_size={"width": 640, "height": 720})
    
    p = c_p.new_page()
    a = c_a.new_page()

    p.goto(WEB)
    a.goto(WEB + "#admin")
    a.click("text=Admin View")
    
    p.evaluate(INJECT_OVERLAYS_JS)
    a.evaluate(INJECT_OVERLAYS_JS)

    set_caption(p, a, "Parking A nearly full, so Parking B is recommended. Data is simulated.")
    p.wait_for_timeout(2000)

    # 1. Pilgrim examines Journey Plan
    smooth_move(p, "text=Journey Plan", steps=20)
    p.wait_for_timeout(2000)
    smooth_move(p, "text=Park at: Parking B", steps=20)
    p.wait_for_timeout(2000)

    # 2. Pilgrim scrolls to Parking Status
    smooth_scroll(p, 360, steps=10)
    p.wait_for_timeout(1500)
    smooth_move(p, "text=Recommended: Parking B", steps=20)
    p.wait_for_timeout(2500)

    # 3. Admin scrolls to Parking Controls
    smooth_scroll(a, 480, steps=10)
    a.wait_for_timeout(1500)

    # 4. Admin updates Parking A to 1000 (Full)
    set_caption(p, a, "Admin updates Parking A to 1000/1000 capacity. System polls every 3s.")
    smooth_move(a, "text=Admin: Update Parking", steps=15)
    a.wait_for_timeout(1000)

    # Drag slider / update via API
    a.evaluate("""() => {
        const headings = Array.from(document.querySelectorAll('h3'));
        const pA = headings.find(h => h.innerText.includes('Parking A'));
        if (pA) {
            const slider = pA.parentElement.querySelector('input[type="range"]');
            slider.value = 1000;
            slider.dispatchEvent(new Event('input', { bubbles: true }));
            slider.dispatchEvent(new Event('change', { bubbles: true }));
        }
    }""")
    requests.put(f"{API}/parking/1", json={"occupied": 1000})
    a.wait_for_timeout(1500)

    # 5. Wait for 4s polling update on Pilgrim side
    p.wait_for_timeout(4500)
    set_caption(p, a, "Parking A is 100% full. Parking B remains the recommended destination.")
    smooth_move(p, "text=0 / 1000", steps=15)
    p.wait_for_timeout(4000)

    p_vid = p.video.path()
    a_vid = a.video.path()
    c_p.close()
    c_a.close()
    browser.close()

    out_mp4 = os.path.join(TEMP_DIR, "scene1_parking.mp4")
    hstack_videos(p_vid, a_vid, out_mp4)
    return out_mp4

def record_scene2(playwright):
    """SCENE 2: SOS EMERGENCY (32s)"""
    print("\n--- Recording Scene 2: SOS ---")
    reset_backend_data()
    rec_dir = os.path.join(TEMP_DIR, "s2")
    os.makedirs(rec_dir, exist_ok=True)

    browser = playwright.chromium.launch()
    c_p = browser.new_context(viewport={"width": 640, "height": 720}, record_video_dir=rec_dir, record_video_size={"width": 640, "height": 720})
    c_a = browser.new_context(viewport={"width": 640, "height": 720}, record_video_dir=rec_dir, record_video_size={"width": 640, "height": 720})
    
    p = c_p.new_page()
    a = c_a.new_page()

    p.goto(WEB)
    a.goto(WEB + "#admin")
    a.click("text=Admin View")
    
    p.evaluate(INJECT_OVERLAYS_JS)
    a.evaluate(INJECT_OVERLAYS_JS)

    set_caption(p, a, "Prototype only. In a real emergency, call 112.")
    p.wait_for_timeout(1500)

    # 1. Pilgrim clicks SOS tab
    smooth_click(p, "button:has-text('SOS')", steps=20, delay=1.5)
    smooth_move(p, "text=Call 112 immediately", steps=15)
    p.wait_for_timeout(2000)

    # 2. Pilgrim selects category and location (default is Medical emergency, Ghat A)
    smooth_click(p, "button:has-text('SEND SOS')", steps=20, delay=2.0)

    # 3. Report appears with checklist
    set_caption(p, a, "SOS Incident dispatched. Command Center receives report instantly.")
    smooth_move(p, "text=Report #", steps=15)
    p.wait_for_timeout(3000)

    # 4. Admin sees incident and updates status to Acknowledged
    a.evaluate("""() => {
        const select = document.querySelector('select:has(option[value="Acknowledged"])');
        if (select) {
            select.value = 'Acknowledged';
            select.dispatchEvent(new Event('change', { bubbles: true }));
        }
    }""")
    set_caption(p, a, "Staff acknowledges incident. Pilgrim status ticks 'Acknowledged' live.")
    smooth_move(a, "text=Emergency Incidents", steps=15)
    a.wait_for_timeout(4500) # wait for polling

    # 5. Admin updates status to Team Assigned
    a.evaluate("""() => {
        const select = document.querySelector('select:has(option[value="Team Assigned"])');
        if (select) {
            select.value = 'Team Assigned';
            select.dispatchEvent(new Event('change', { bubbles: true }));
        }
    }""")
    set_caption(p, a, "Response team assigned. Pilgrim checklist confirms live dispatch.")
    a.wait_for_timeout(4500) # wait for polling
    smooth_move(p, "text=Team Assigned", steps=15)
    p.wait_for_timeout(4000)

    p_vid = p.video.path()
    a_vid = a.video.path()
    c_p.close()
    c_a.close()
    browser.close()

    out_mp4 = os.path.join(TEMP_DIR, "scene2_sos.mp4")
    hstack_videos(p_vid, a_vid, out_mp4)
    return out_mp4

def record_scene3(playwright):
    """SCENE 3: CROWD DIVERSION (37s)"""
    print("\n--- Recording Scene 3: Crowd Diversion ---")
    reset_backend_data()
    rec_dir = os.path.join(TEMP_DIR, "s3")
    os.makedirs(rec_dir, exist_ok=True)

    browser = playwright.chromium.launch()
    c_p = browser.new_context(viewport={"width": 640, "height": 720}, record_video_dir=rec_dir, record_video_size={"width": 640, "height": 720})
    c_a = browser.new_context(viewport={"width": 640, "height": 720}, record_video_dir=rec_dir, record_video_size={"width": 640, "height": 720})
    
    p = c_p.new_page()
    a = c_a.new_page()

    p.goto(WEB)
    a.goto(WEB + "#admin")
    a.click("text=Admin View")
    
    p.evaluate(INJECT_OVERLAYS_JS)
    a.evaluate(INJECT_OVERLAYS_JS)

    set_caption(p, a, "Zero unverified alerts. Pilgrim view shows NO diversion until staff approve.")
    p.wait_for_timeout(2000)

    # 1. Pilgrim observes normal crowd
    smooth_move(p, "text=Crowd Status", steps=15)
    p.wait_for_timeout(2000)
    smooth_move(p, "text=Ghat A: NORMAL", steps=15)
    p.wait_for_timeout(2500)

    # 2. Admin sets Ghat A to CRITICAL
    set_caption(p, a, "Field report indicates high surge. Admin marks Ghat A as CRITICAL.")
    smooth_move(a, "text=Admin: Crowd Zones", steps=15)
    a.wait_for_timeout(1000)

    a.evaluate("""() => {
        const headings = Array.from(document.querySelectorAll('b'));
        const ghatA = headings.find(h => h.innerText.includes('Ghat A'));
        const select = ghatA.parentElement.querySelector('select');
        select.value = 'CRITICAL';
        select.dispatchEvent(new Event('change', { bubbles: true }));
    }""")
    a.wait_for_timeout(2000)

    # 3. Highlight: Admin sees suggestion, but Pilgrim sees NOTHING yet!
    set_caption(p, a, "AI suggests diversion to Ghat B. Notice: Pilgrim screen shows NO alert yet.")
    smooth_move(a, "text=Suggested diversion", steps=15)
    a.wait_for_timeout(2000)
    smooth_move(p, "text=Ghat A: CRITICAL", steps=15)
    p.wait_for_timeout(3500)

    # 4. Admin clicks "Approve diversion (staff verified)"
    set_caption(p, a, "Staff verifies on-site and approves diversion advisory.")
    smooth_click(a, "button:has-text('Approve diversion')", steps=20, delay=1.5)

    # 5. Wait 4s polling -> Pilgrim receives alert!
    set_caption(p, a, "Diversion is shown to pilgrims only after staff approve.")
    p.wait_for_timeout(4500)
    smooth_move(p, "text=Staff-approved:", steps=15)
    p.wait_for_timeout(5000)

    p_vid = p.video.path()
    a_vid = a.video.path()
    c_p.close()
    c_a.close()
    browser.close()

    out_mp4 = os.path.join(TEMP_DIR, "scene3_crowd.mp4")
    hstack_videos(p_vid, a_vid, out_mp4)
    return out_mp4

def record_scene4(playwright):
    """SCENE 4: MULTI-LINGUAL ACCESSIBILITY (18s)"""
    print("\n--- Recording Scene 4: Multi-Lingual ---")
    rec_dir = os.path.join(TEMP_DIR, "s4")
    os.makedirs(rec_dir, exist_ok=True)

    browser = playwright.chromium.launch()
    c_p = browser.new_context(viewport={"width": 640, "height": 720}, record_video_dir=rec_dir, record_video_size={"width": 640, "height": 720})
    c_a = browser.new_context(viewport={"width": 640, "height": 720}, record_video_dir=rec_dir, record_video_size={"width": 640, "height": 720})
    
    p = c_p.new_page()
    a = c_a.new_page()

    p.goto(WEB)
    a.goto(WEB + "#admin")
    a.click("text=Admin View")
    
    p.evaluate(INJECT_OVERLAYS_JS)
    a.evaluate(INJECT_OVERLAYS_JS)

    set_caption(p, a, "Telugu and Hindi texts are drafts pending native-speaker review.")
    p.wait_for_timeout(1500)

    # 1. Switch to Telugu
    smooth_click(p, "button:has-text('తెలుగు')", steps=20, delay=1.5)
    set_caption(p, a, "Full Telugu localization: ప్రయాణ ప్రణాళిక, జన సమూహ స్థితి, పార్కింగ్ స్థితి.")
    smooth_scroll(p, 300, steps=8)
    p.wait_for_timeout(2500)
    smooth_scroll(p, -300, steps=8)
    p.wait_for_timeout(1500)

    # 2. Switch to Hindi
    smooth_click(p, "button:has-text('हिन्दी')", steps=20, delay=1.5)
    set_caption(p, a, "Hindi localization: यात्रा योजना, भीड़ की स्थिति, पार्किंग स्थिति.")
    p.wait_for_timeout(3000)

    # 3. Switch back to English
    smooth_click(p, "button:has-text('English')", steps=20, delay=1.5)
    set_caption(p, a, "Instant multi-lingual switching for diverse devotees across India.")
    p.wait_for_timeout(2500)

    p_vid = p.video.path()
    a_vid = a.video.path()
    c_p.close()
    c_a.close()
    browser.close()

    out_mp4 = os.path.join(TEMP_DIR, "scene4_languages.mp4")
    hstack_videos(p_vid, a_vid, out_mp4)
    return out_mp4

def build_final_video():
    """Concatenate all scene cards and interaction recordings into final_demo.mp4"""
    print("\n--- Generating Title & Transition Cards ---")
    card0 = os.path.join(TEMP_DIR, "card00_intro.mp4")
    card1 = os.path.join(TEMP_DIR, "card01_parking.mp4")
    card2 = os.path.join(TEMP_DIR, "card02_sos.mp4")
    card3 = os.path.join(TEMP_DIR, "card03_crowd.mp4")
    card4 = os.path.join(TEMP_DIR, "card04_languages.mp4")
    card5 = os.path.join(TEMP_DIR, "card05_outro.mp4")

    make_card_video("00_intro.png", 4, card0)
    make_card_video("01_parking.png", 3, card1)
    make_card_video("02_sos.png", 3, card2)
    make_card_video("03_crowd.png", 3, card3)
    make_card_video("04_languages.png", 3, card4)
    make_card_video("05_outro.png", 6, card5)

    playlist = [
        card0,
        card1,
        os.path.join(TEMP_DIR, "scene1_parking.mp4"),
        card2,
        os.path.join(TEMP_DIR, "scene2_sos.mp4"),
        card3,
        os.path.join(TEMP_DIR, "scene3_crowd.mp4"),
        card4,
        os.path.join(TEMP_DIR, "scene4_languages.mp4"),
        card5
    ]

    concat_list_file = os.path.join(TEMP_DIR, "concat_list.txt")
    with open(concat_list_file, "w") as f:
        for clip in playlist:
            f.write(f"file '{clip.replace(chr(92), '/')}'\n")

    final_mp4 = os.path.join(DEMO_DIR, "final_demo.mp4")
    print(f"\nConcatenating {len(playlist)} clips into {final_mp4}...")
    
    # Encode with CRF 30, slow preset, yuv420p to guarantee size < 10 MB and high quality
    cmd = [
        FFMPEG, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list_file,
        "-c:v", "libx264",
        "-crf", "30",
        "-preset", "slow",
        "-pix_fmt", "yuv420p",
        "-r", "24",
        final_mp4
    ]
    subprocess.run(cmd, check=True)
    
    # Check size
    size_mb = os.path.getsize(final_mp4) / (1024 * 1024)
    print(f"\nCreated final_demo.mp4: {size_mb:.2f} MB")
    
    if size_mb > 9.8:
        print("Size slightly high, re-compressing with CRF 34...")
        recompressed = os.path.join(DEMO_DIR, "final_demo_opt.mp4")
        subprocess.run([
            FFMPEG, "-y",
            "-i", final_mp4,
            "-c:v", "libx264",
            "-crf", "34",
            "-preset", "slow",
            "-pix_fmt", "yuv420p",
            recompressed
        ], check=True)
        shutil.move(recompressed, final_mp4)
        size_mb = os.path.getsize(final_mp4) / (1024 * 1024)
        print(f"Optimized final_demo.mp4 size: {size_mb:.2f} MB")

    return final_mp4

def verify_video(video_path):
    print("\n--- Verifying Video with ffprobe & frame extraction ---")
    probe_cmd = [
        FFPROBE, "-v", "error",
        "-show_entries", "format=duration,size:stream=width,height,r_frame_rate",
        "-of", "default=noprint_wrappers=1",
        video_path
    ]
    res = subprocess.run(probe_cmd, capture_output=True, text=True)
    print(res.stdout)
    
    # Extract 8 frames for inspection
    frames_dir = os.path.join(DEMO_DIR, "verification_frames")
    os.makedirs(frames_dir, exist_ok=True)
    
    # Get duration
    duration = 140.0
    for line in res.stdout.splitlines():
        if line.startswith("duration="):
            duration = float(line.split("=")[1])
            
    timestamps = [
        2,                   # Scene 0: Intro card
        5,                   # Scene 1: Card 01
        18,                  # Scene 1: Parking live
        38,                  # Scene 2: Card 02
        55,                  # Scene 2: SOS live
        75,                  # Scene 3: Card 03
        95,                  # Scene 3: Crowd live
        115,                 # Scene 4: Card 04
        125,                 # Scene 4: Telugu live
        min(138, duration - 1) # Scene 5: Outro card
    ]
    
    for i, ts in enumerate(timestamps):
        out_frame = os.path.join(frames_dir, f"frame_{i:02d}_{int(ts)}s.png")
        subprocess.run([
            FFMPEG, "-y",
            "-ss", str(ts),
            "-i", video_path,
            "-vframes", "1",
            out_frame
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Extracted verification frame at {ts}s -> {out_frame}")

def main():
    os.makedirs(TEMP_DIR, exist_ok=True)
    os.makedirs(DEMO_DIR, exist_ok=True)
    
    with sync_playwright() as playwright:
        s1 = record_scene1(playwright)
        s2 = record_scene2(playwright)
        s3 = record_scene3(playwright)
        s4 = record_scene4(playwright)

    final_video = build_final_video()
    verify_video(final_video)
    
    # Final reset of backend data to leave clean app state
    reset_backend_data()
    print("\nSUCCESS: All video production steps completed cleanly.")

if __name__ == "__main__":
    main()
