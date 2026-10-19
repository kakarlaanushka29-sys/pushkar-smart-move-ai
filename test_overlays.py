import os
from playwright.sync_api import sync_playwright

INJECT_JS = """
(() => {
  // 1. Top Header Bar
  const isPilgrim = window.location.hash !== '#admin';
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
  caption.innerHTML = '<span id="caption-text">Caption text here...</span>';
  document.body.appendChild(caption);

  // Helper function to update caption
  window.setDemoCaption = (text) => {
    const el = document.getElementById('caption-text');
    if (el) el.innerText = text;
  };

  // 4. Custom cursor
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
  cursor.style.transition = 'width 0.1s, height 0.1s';
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

def test_overlays():
    os.makedirs("test_shots", exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        # Pilgrim
        page1 = browser.new_page(viewport={"width": 640, "height": 720})
        page1.goto("http://localhost:5173")
        page1.evaluate(INJECT_JS)
        page1.evaluate("window.setDemoCaption('Parking A nearly full, so Parking B is recommended. Data is simulated.')")
        page1.wait_for_timeout(500)
        page1.screenshot(path="test_shots/overlay_pilgrim.png")

        # Admin
        page2 = browser.new_page(viewport={"width": 640, "height": 720})
        page2.goto("http://localhost:5173#admin")
        page2.click("text=Admin View")
        page2.evaluate(INJECT_JS)
        page2.evaluate("window.setDemoCaption('Parking A nearly full, so Parking B is recommended. Data is simulated.')")
        page2.wait_for_timeout(500)
        page2.screenshot(path="test_shots/overlay_admin.png")

        browser.close()
        print("Overlay screenshots captured.")

if __name__ == "__main__":
    test_overlays()
