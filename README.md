# Price Monitor & Stock Alert Bot

An automated Python tool that checks product prices on e-commerce websites, compares them against your target budget stored in a JSON configuration file, and sends real-time price drop alerts via Telegram.

## Why This Project?

Checking product pages manually for discounts is time-consuming. This bot automates price tracking using clean HTTP requests, HTML parsing, exception handling, and third-party messaging webhooks.

## Key Features

- **Ethical Web Scraping**: Uses `httpx` with custom headers and timeout handling to avoid overloading target servers.
- **Resilient HTML Parsing**: Extracts clean numeric values from formatted price strings using `BeautifulSoup` and regular expressions.
- **Instant Telegram Notifications**: Connects directly to the Telegram Bot API using environment variables.
- **Type-Safe & Tested**: Written with Python static Type Hints and unit-tested with `pytest`.
- **Container Ready**: Includes a lightweight `Dockerfile` for one-command deployment.

## Architecture Workflow

```
+---------------+      +-------------------+      +--------------------+      +------------------+
|  config.json  | ---> |   HTTPX + BS4     | ---> |  Threshold Check   | ---> |   Telegram API   |
| (Target Info) |      | (Fetch & Extract) |      | (Current <= Limit) |      | (Send Notification)|
+---------------+      +-------------------+      +--------------------+      +------------------+
```

## Project Structure

```
price-monitor-bot/
├── main.py              # Core scraping, comparison, and notification logic
├── config.json          # Target product URL, CSS selector, and price threshold
├── requirements.txt     # Project dependencies
├── .env.example         # Template for environment variables
├── Dockerfile           # Container image definition
├── README.md            # Project documentation
└── tests/
    └── test_main.py     # Unit tests with pytest
```

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/price-monitor-bot.git
cd price-monitor-bot
```

### 2. Install Dependencies

Create a virtual environment and install the required packages:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy `.env.example` to `.env` and add your Telegram credentials:

```bash
cp .env.example .env
```

Edit `.env`:

```ini
TELEGRAM_BOT_TOKEN=123456789:ABCDEF_your_token_here
TELEGRAM_CHAT_ID=987654321
```

### 4. Customize Your Target Product

Edit `config.json` with the product URL, CSS selector for the price element, and your target price:

```json
{
  "product_name": "Noise-Canceling Wireless Headphones",
  "url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
  "target_price": 60.00,
  "css_selector": ".price_color"
}
```

### 5. Run the Bot

```bash
python main.py
```

## Running Unit Tests

Run the test suite with `pytest`:

```bash
pytest
```

## Running with Docker

Build and run the container:

```bash
docker build -t price-monitor-bot .
docker run --env-file .env price-monitor-bot
```
