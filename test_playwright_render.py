import os
from playwright.sync_api import sync_playwright # type: ignore

def test_render():
    os.makedirs("test_shots", exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        # Test Pilgrim view
        page1 = browser.new_page(viewport={"width": 640, "height": 720})
        page1.goto("http://localhost:5173")
        page1.wait_for_timeout(1000)
        page1.screenshot(path="test_shots/pilgrim_normal.png")
        
        # Test Admin view
        page2 = browser.new_page(viewport={"width": 640, "height": 720})
        page2.goto("http://localhost:5173")
        page2.wait_for_timeout(1000)
        # click Admin view
        page2.click("text=Admin View")
        page2.wait_for_timeout(1000)
        page2.screenshot(path="test_shots/admin_normal.png")
        
        # Test Telugu on Pilgrim
        page1.click("text=తెలుగు")
        page1.wait_for_timeout(1000)
        page1.screenshot(path="test_shots/pilgrim_telugu.png")

        # Test Hindi on Pilgrim
        page1.click("text=हिन्दी")
        page1.wait_for_timeout(1000)
        page1.screenshot(path="test_shots/pilgrim_hindi.png")
        
        browser.close()
        print("Screenshots captured successfully.")

if __name__ == "__main__":
    test_render()
