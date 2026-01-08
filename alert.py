import json
import requests
import yfinance as yf

# ===============================
# 🔐 텔레그램 정보 (네 걸로 교체)
# ===============================
BOT_TOKEN = "8376732547:AAHFiOcroCr4QzAvK69TDgP3L-629LGHCWM"
CHAT_ID = "7662662191"

# ===============================
# 📂 보유 정보 불러오기
# ===============================
with open("holdings.json", "r") as f:
    holdings = json.load(f)

lines = ["[오늘의 행동 요약]\n"]

# ===============================
# 📊 종목별 판단
# ===============================
for ticker, h in holdings.items():
    data = yf.Ticker(ticker).history(period="1d")

    # 혹시 데이터 없을 때 대비
    if data.empty:
        continue

    price = data["Close"][-1]
    avg_price = h["avg_price"]

    diff = (price - avg_price) / avg_price * 100

    # ===============================
    # 📈📉 시각 표시
    # ===============================
    if diff >= 1:
        sign = f"🔺 +{diff:.1f}% 📈"
    elif diff <= -1:
        sign = f"🔻 {diff:.1f}% 📉"
    else:
        sign = f"➖ {diff:.1f}%"

    # ===============================
    # 🧠 보수형 행동 기준
    # ===============================
    if ticker == "VRT":
        if diff >= 6:
            action = "추가 매수 중단 / 익절 고려"
        elif diff <= -6:
            action = "모으기 유지 (무리한 확대 금지)"
        else:
            action = "모으기 유지"

    elif ticker == "PEP":
        if diff <= -6:
            action = "모으기 유지 (배당 목적)"
        elif diff >= 6:
            action = "모으기 유지 (매도 안 함)"
        else:
            action = "모으기 유지"

    else:  # NVDA, ETN (장기 성장)
        if diff <= -6:
            action = "모으기 유지 또는 50% 축소 고려"
        elif diff >= 6:
            action = "모으기 축소 (익절은 안 함)"
        else:
            action = "모으기 유지"

    lines.append(f"{ti
