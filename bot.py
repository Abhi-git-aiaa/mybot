import requests
import smtplib
from datetime import date
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

GMAIL_SENDER   = os.environ.get("GMAIL_SENDER")
GMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD")
GMAIL_RECEIVER = os.environ.get("GMAIL_RECEIVER")
CITY           = os.environ.get("CITY", "Thiruvananthapuram")

def get_weather():
    url = f"https://wttr.in/{CITY}?format=3"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text.strip()
    except Exception as e:
        return f"Weather unavailable ({e})"

def get_quote():
    url = "https://zenquotes.io/api/random"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        quote = data[0]["q"]
        author = data[0]["a"]
        return f'"{quote}" — {author}'
    except Exception as e:
        return f"Quote unavailable ({e})"

def send_email(summary):
    if not all([GMAIL_SENDER, GMAIL_PASSWORD, GMAIL_RECEIVER]):
        print("Gmail credentials not set. Skipping email.")
        return
    today = date.today().strftime("%A, %d %B %Y")
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Pulse Daily Summary — {today}"
    msg["From"] = GMAIL_SENDER
    msg["To"] = GMAIL_RECEIVER
    msg.attach(MIMEText(summary, "plain"))
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_SENDER, GMAIL_PASSWORD)
            server.sendmail(GMAIL_SENDER, GMAIL_RECEIVER, msg.as_string())
        print(f"Email sent to {GMAIL_RECEIVER}")
    except Exception as e:
        print(f"Email failed: {e}")

def run():
    today = date.today().strftime("%A, %d %B %Y")
    weather = get_weather()
    quote = get_quote()
    summary = f"""
================================
  PULSE - Daily Summary
  {today}
================================

WEATHER
  {weather}

TODAY'S QUOTE
  {quote}

================================
"""
    print(summary)
    with open("daily_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)
    send_email(summary)
    print("Pulse ran successfully.")

if name == "main":
    run()