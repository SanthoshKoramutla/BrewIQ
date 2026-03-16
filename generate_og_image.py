#!/usr/bin/env python3
"""
Generate og-image.png from og-image.html using Playwright.
Run: python3 generate_og_image.py
"""
import subprocess
import sys
import os

def ensure_playwright():
    try:
        from playwright.sync_api import sync_playwright
        return True
    except ImportError:
        print("Installing playwright...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright", "-q"])
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
        return True

ensure_playwright()

from playwright.sync_api import sync_playwright

script_dir = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(script_dir, "og-image.html")
output_path = os.path.join(script_dir, "og-image.png")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1200, "height": 628})
    page.goto(f"file://{html_path}")
    page.wait_for_timeout(300)  # let fonts/gradients settle
    page.screenshot(path=output_path, clip={"x": 0, "y": 0, "width": 1200, "height": 628})
    browser.close()

print(f"✓ Generated: {output_path}")
