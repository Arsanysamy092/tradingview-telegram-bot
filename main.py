from flask import Flask, request
import requests

app = Flask(__name__)

bot_token = "8073454655:AAGHsfNSJGFSzJLaVroXEFjU57gYtPUsDSA"
chat_id = "1001113272"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    try:
        response = requests.post(url, data=data)
        if response.status_code != 200:
            print("❌ فشل إرسال الرسالة:", response.text)
        else:
            print("✅ تم إرسال الرسالة")
    except Exception as e:
        print("❌ خطأ أثناء الإرسال:", str(e))

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data:
        return {"error": "لا توجد بيانات"}, 400

    try:
        pair = data.get("pair", "زوج غير معروف")
        signal = data.get("signal", "إشارة غير معروفة")
        reason = data.get("reason", "لا يوجد سبب")
        confidence = data.get("confidence", "?")

        message = f"""🔔 إشارة {signal.upper()} على {pair}
نسبة التوافق: {confidence}%
📈 الأسباب:
{reason}"""

        send_telegram_message(message)
        return {"status": "تم الاستلام"}, 200
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
