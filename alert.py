import json, requests, yfinance as yf

BOT_TOKEN = "8376732547:AAHFiOcroCr4QzAvK69TDgP3L-629LGHCWM"
CHAT_ID = "7662662191"

with open("holdings.json") as f:
    holdings = json.load(f)

lines = ["[오늘의 행동 요약]\n"]

for ticker, h in holdings.items():
    price = yf.Ticker(ticker).history(period="1d")["Close"][-1]
    diff = (price - h["avg_price"]) / h["avg_price"] * 100

    if diff <= -6:
        action = "모으기 +50% 고려"
    elif diff >= 6:
        action = "모으기 축소 / 익절 검토"
    else:
        action = "모으기 유지"

    lines.append(
        f"{ticker}: 평단 대비 {diff:.1f}% → {action}"
    )

msg = "\n".join(lines)

requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={"chat_id": CHAT_ID, "text": msg}
)
