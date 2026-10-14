# Mock Bloomberg Terminal

A small Python script that watches one stock and texts you the latest news when the price moves. It pulls daily prices from Alpha Vantage, compares the last two closing prices, gets the top three headlines about the company from NewsAPI, and sends each one as an SMS through Twilio.

Built as part of my 100 Days of Code challenge.

## How it works

1. **Get prices.** Requests the `TIME_SERIES_DAILY` series for `STOCK_NAME` from Alpha Vantage.
2. **Compare closes.** Takes the two most recent trading days and works out the percentage change between their closing prices, marked 🔺 for up or 🔻 for down.
3. **Get news.** Searches NewsAPI for articles with `COMPANY_NAME` in the title and keeps the first three.
4. **Send alerts.** Texts each article as its own SMS:

   ```
   TSLA: 🔺: 3%
   : Headline: <article title>.
   Brief: <article description>
   ```

## Project files

| File | Purpose |
| --- | --- |
| `main.py` | The alert script |
| `eda.ipynb` | Notebook used to explore the Alpha Vantage and NewsAPI responses before writing `main.py` |
| `.env` | API keys, phone numbers and settings (not committed) |
| `.gitignore` | Keeps `.env` and Python/Jupyter cache files out of Git |

## Setup

### 1. Install dependencies

Requires Python 3.9+.

```bash
pip install requests python-dotenv twilio pandas numpy
```

### 2. Get API keys

- **Alpha Vantage** (stock prices): free key at <https://www.alphavantage.co/support/#api-key>
- **NewsAPI** (headlines): free key at <https://newsapi.org/register>
- **Twilio** (SMS): Account SID, Auth Token and a phone number from <https://console.twilio.com>

### 3. Create a `.env` file

Create a `.env` file in the project folder:

```env
STOCK_NAME=TSLA
COMPANY_NAME=Tesla Inc
STOCK_ENDPOINT=https://www.alphavantage.co/query

ALPHAVANTAGE_API_KEY=your_alpha_vantage_key
NEWS_API_KEY=your_newsapi_key

TWILIO_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=+15551234567
MY_PHONE_NUMBER=+15557654321
```

`TWILIO_PHONE_NUMBER` is the Twilio number the alerts come from. `MY_PHONE_NUMBER` is the phone that receives them. Write both in E.164 format: a `+`, the country code, then the number.

`.env` is listed in `.gitignore`, so it won't be committed.

## Usage

```bash
python main.py
```

The script runs once and exits. To get daily alerts, schedule it after market close with Task Scheduler (Windows) or cron (macOS/Linux).

## Known issues and limitations

- **The price threshold is turned off.** The check is `abs(pct_diff) > -10`, which is always true, so news is sent on every run. This was set that way for testing. Change it to `> 5` to alert only on moves bigger than 5%.
- **Twilio trial accounts can't send these messages.** Trial accounts only allow Twilio's predefined SMS templates, so free-form messages fail with *"Invalid template name."* You need an upgraded Twilio account. Sending to US numbers also requires A2P 10DLC registration.
- **The percentage change uses the wrong base.** It divides by yesterday's close. A standard percent change divides by the day before's close.
- **There is no error handling.** If an API rate limit is hit or a key is invalid, the script crashes with a `KeyError` instead of showing a clear message. The Alpha Vantage free tier allows 25 requests per day.

## Possible improvements

- Fix the threshold and percent-change issues above.
- Add a `requirements.txt`.
- Offer a free alert channel (email, Telegram or ntfy) as an alternative to Twilio.
