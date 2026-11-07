import os, sys
from playwright.sync_api import sync_playwright
R = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 900, "height": 720})
    pg.goto("file:///" + R + "/_logo_test.html"); pg.screenshot(path=R + "/_logo_cmp.png"); b.close()
