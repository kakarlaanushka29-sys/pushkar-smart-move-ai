import time
import requests
from playwright.sync_api import sync_playwright

API = "http://127.0.0.1:8000"

def test_flows():
    # 0. Reset backend data first
    requests.put(f"{API}/parking/1", json={"occupied": 980})
    requests.put(f"{API}/parking/2", json={"occupied": 500})
    requests.put(f"{API}/crowd/1", json={"level": "NORMAL", "approved": False})
    requests.put(f"{API}/crowd/2", json={"level": "NORMAL", "approved": False})
    requests.put(f"{API}/crowd/3", json={"level": "NORMAL", "approved": False})

    with sync_playwright() as p:
        browser = p.chromium.launch()
        pilgrim = browser.new_page(viewport={"width": 640, "height": 720})
        admin = browser.new_page(viewport={"width": 640, "height": 720})

        pilgrim.goto("http://localhost:5173")
        admin.goto("http://localhost:5173")
        admin.click("text=Admin View")

        pilgrim.wait_for_timeout(1000)
        admin.wait_for_timeout(1000)

        # Test 1: Parking update
        print("Testing Parking...")
        # Scroll admin to parking
        admin.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        admin.wait_for_timeout(500)
        # Find Parking A slider
        slider_found = admin.evaluate("""() => {
            const headings = Array.from(document.querySelectorAll('h3'));
            const pA = headings.find(h => h.innerText.includes('Parking A'));
            if (!pA) return false;
            const slider = pA.parentElement.querySelector('input[type="range"]');
            if (!slider) return false;
            slider.value = 1000;
            slider.dispatchEvent(new Event('change', { bubbles: true }));
            return true;
        }""")
        print("Slider found & updated:", slider_found)
        time.sleep(4)
        # Check pilgrim page updated
        pA_text = pilgrim.evaluate("""() => {
            const headings = Array.from(document.querySelectorAll('h3'));
            const pA = headings.find(h => h.innerText.includes('Parking A'));
            return pA ? pA.parentElement.innerText : 'not found';
        }""")
        print("Pilgrim Parking A text after update:", pA_text)

        # Test 2: SOS flow
        print("\nTesting SOS...")
        pilgrim.click("text=SOS")
        pilgrim.wait_for_timeout(500)
        # Click Send SOS
        pilgrim.click("text=SEND SOS")
        pilgrim.wait_for_timeout(1000)
        sos_report_text = pilgrim.evaluate("() => document.body.innerText.includes('Report #')")
        print("SOS report displayed on pilgrim:", sos_report_text)
        
        # Check admin emergency incidents
        admin.evaluate("window.scrollTo(0, 0)")
        admin.wait_for_timeout(4000) # wait for polling
        admin_incident_found = admin.evaluate("() => document.body.innerText.includes('Medical emergency')")
        print("Admin received incident:", admin_incident_found)

        # Admin updates status to Acknowledged
        admin.evaluate("""() => {
            const select = document.querySelector('select:has(option[value="Acknowledged"])');
            if (select) {
                select.value = 'Acknowledged';
                select.dispatchEvent(new Event('change', { bubbles: true }));
            }
        }""")
        time.sleep(4)
        ack_ticked = pilgrim.evaluate("() => document.body.innerText.includes('Acknowledged')")
        print("Pilgrim ticked Acknowledged:", ack_ticked)

        # Test 3: Crowd flow
        print("\nTesting Crowd diversion...")
        pilgrim.click("text=Pilgrim View")
        pilgrim.wait_for_timeout(500)
        
        # Admin sets Ghat A to CRITICAL
        admin.evaluate("""() => {
            const headings = Array.from(document.querySelectorAll('b'));
            const ghatA = headings.find(h => h.innerText.includes('Ghat A'));
            const select = ghatA.parentElement.querySelector('select');
            select.value = 'CRITICAL';
            select.dispatchEvent(new Event('change', { bubbles: true }));
        }""")
        admin.wait_for_timeout(1000)
        suggest_visible = admin.evaluate("() => document.body.innerText.includes('Suggested diversion')")
        print("Admin shows diversion suggestion:", suggest_visible)
        
        # Check pilgrim does NOT show diversion yet
        pilgrim_div_premature = pilgrim.evaluate("() => document.body.innerText.includes('Staff-approved:')")
        print("Pilgrim diversion premature (should be False):", pilgrim_div_premature)

        # Admin approves diversion
        admin.click("text=Approve diversion")
        print("Admin approved diversion.")
        time.sleep(4) # wait for polling
        pilgrim_div_shown = pilgrim.evaluate("() => document.body.innerText.includes('Staff-approved:')")
        print("Pilgrim shows approved diversion (should be True):", pilgrim_div_shown)

        # Test 4: Languages
        print("\nTesting Languages...")
        pilgrim.click("text=తెలుగు")
        pilgrim.wait_for_timeout(500)
        te_found = pilgrim.evaluate("() => document.body.innerText.includes('ప్రయాణ ప్రణాళిక')")
        print("Telugu loaded:", te_found)

        pilgrim.click("text=हिन्दी")
        pilgrim.wait_for_timeout(500)
        hi_found = pilgrim.evaluate("() => document.body.innerText.includes('यात्रा योजना')")
        print("Hindi loaded:", hi_found)

        pilgrim.click("text=English")
        pilgrim.wait_for_timeout(500)
        en_found = pilgrim.evaluate("() => document.body.innerText.includes('Journey Plan')")
        print("English restored:", en_found)

        browser.close()

if __name__ == "__main__":
    test_flows()
