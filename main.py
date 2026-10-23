"""
Price Monitor & Stock Alert Bot
A beginner-friendly script that fetches a product's current price from a webpage,
compares it against a target threshold stored in JSON, and sends a Telegram alert.
"""

import json
import os
import re
from pathlib import Path
from typing import Any, Optional

import httpx
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def load_config(config_path: str = "config.json") -> dict[str, Any]:
    """Load product URL and target price configuration from a JSON file."""
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def extract_price_from_html(html_content: str, css_selector: str = ".price") -> Optional[float]:
    """Parse HTML content and extract the numeric product price."""
    soup = BeautifulSoup(html_content, "html.parser")
    price_element = soup.select_one(css_selector)
    if not price_element:
        return None

    raw_text = price_element.get_text(strip=True)
    # Remove currency symbols and commas (e.g., "$1,299.99" -> "1299.99")
    cleaned_text = re.sub(r"[^0-9.]", "", raw_text)
    if not cleaned_text:
        return None

    try:
        return float(cleaned_text)
    except ValueError:
        return None


def fetch_page_html(url: str, timeout: float = 10.0) -> Optional[str]:
    """Fetch HTML content from a webpage using HTTPX with ethical headers and error handling."""
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; PriceMonitorBot/1.0; +https://github.com/your-username)"
    }
    try:
        with httpx.Client(timeout=timeout, headers=headers, follow_redirects=True) as client:
            response = client.get(url)
            response.raise_for_status()
            return response.text
    except httpx.HTTPError as error:
        print(f"[Error] Failed to fetch {url}: {error}")
        return None


def should_send_alert(current_price: float, target_price: float) -> bool:
    """Return True if the current price is equal to or below the target price."""
    if current_price <= 0:
        raise ValueError("Current price must be greater than zero.")
    return current_price <= target_price


def send_telegram_alert(product_name: str, current_price: float, url: str) -> bool:
    """Send a price drop notification via Telegram Bot API."""
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        print("[Warning] Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID in environment.")
        return False

    api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    message = (
        f"Price Drop Alert!\n"
        f"Product: {product_name}\n"
        f"Current Price: ${current_price:.2f}\n"
        f"Link: {url}"
    )

    try:
        response = httpx.post(api_url, json={"chat_id": chat_id, "text": message}, timeout=10.0)
        response.raise_for_status()
        return True
    except httpx.HTTPError as error:
        print(f"[Error] Could not send Telegram message: {error}")
        return False


def run_monitor(config_path: str = "config.json") -> None:
    """Main workflow: load config, scrape current price, and alert if price dropped."""
    config = load_config(config_path)
    product_name: str = config["product_name"]
    url: str = config["url"]
    target_price: float = float(config["target_price"])
    css_selector: str = config.get("css_selector", ".price")

    print(f"Checking price for '{product_name}'...")
    html = fetch_page_html(url)
    if not html:
        return

    current_price = extract_price_from_html(html, css_selector)
    if current_price is None:
        print("[Warning] Could not find a valid price on the page.")
        return

    print(f"Current price: ${current_price:.2f} | Target price: ${target_price:.2f}")
    if should_send_alert(current_price, target_price):
        print("Target reached! Sending Telegram alert...")
        send_telegram_alert(product_name, current_price, url)
    else:
        print("Price is still above target. No alert sent.")


if __name__ == "__main__":
    run_monitor()
