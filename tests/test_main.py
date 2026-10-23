"""
Unit tests for Price Monitor & Stock Alert Bot using pytest.
"""

import json
from pathlib import Path
import pytest

from main import extract_price_from_html, load_config, should_send_alert


def test_extract_price_from_html() -> None:
    """Verify that price is accurately parsed from an HTML snippet."""
    sample_html = """
    <html>
        <body>
            <h1>Wireless Headphones</h1>
            <span class="price">$1,249.50</span>
        </body>
    </html>
    """
    price = extract_price_from_html(sample_html, css_selector=".price")
    assert price == 1249.50


def test_should_send_alert() -> None:
    """Verify threshold comparison logic for lower, equal, and higher prices."""
    assert should_send_alert(current_price=79.99, target_price=100.00) is True
    assert should_send_alert(current_price=100.00, target_price=100.00) is True
    assert should_send_alert(current_price=120.00, target_price=100.00) is False


def test_load_config(tmp_path: Path) -> None:
    """Verify configuration JSON loading using a temporary file."""
    sample_config = {
        "product_name": "Mechanical Keyboard",
        "url": "https://example.com/product/keyboard",
        "target_price": 85.0,
        "css_selector": ".product-price",
    }
    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps(sample_config), encoding="utf-8")

    loaded = load_config(str(config_file))
    assert loaded["product_name"] == "Mechanical Keyboard"
    assert loaded["target_price"] == 85.0
