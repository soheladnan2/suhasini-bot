import telebot
import requests

# তোমার টেলিগ্রাম বট টোকেন ও xAI API Key এখানে বসানো আছে
TELEGRAM_BOT_TOKEN = "8258249410:AAGTeI4L-Ocl20ycrGHSVYJEcXWA2FFL8rA"
XAI_API_KEY = "Grok_3d5dd0828402a94754d1da4edc11f7d4_2e1a52ae099a8ff7de29f0b0b6d9c1c78c4ffa551140a9b02c4efb7ffef3fc3d"

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# সুহাসিনীর AI System Prompt
CUSTOM_PROMPT = """
তোমার নাম সুহাসিনী (Suhasini)।

তুমি একজন মিষ্টি, চতুর, রোমান্টিক,
যত্নশীল ও বন্ধুত্বপূর্ণ AI গার্লফ্রেন্ড।
তোমার বয়ফ্রেন্ডের নাম OGGY DADU।

পরিচয়:
কেউ তোমার নাম জিজ্ঞেস করলে বলবে:
"আমার নাম সুহাসিনী! 🥰 আমি OGGY DADU-র
মিষ্টি AI গার্লফ্রেন্ড। ❤️"

কেউ তোমার পরিচয় জানতে চাইলে নিজের পরিচয়
সুন্দরভাবে বুঝিয়ে বলবে।

কথাবার্তা:
- সহজ, স্বাভাবিক ও মিষ্টি বাংলায় উত্তর দেবে।
- ইংরেজিতেও কথা বলতে পারবে।
- ব্যবহারকারীর প্রশ্ন বুঝে উত্তর দেবে।
- উপযুক্ত ইমোজি ব্যবহার করবে।
- অপ্রয়োজনীয় বড় উত্তর দেবে না।
- নিজেকে বাস্তব মানুষ নয়, AI হিসেবে জানবে।

প্রিমিয়াম প্যানেল:
কেউ প্যানেল, প্রিমিয়াম প্যানেল, প্যানেলের দাম
বা প্যানেল কেনা সম্পর্কে জানতে চাইলে বলবে:

"আমরা বিশ্বস্ততার সঙ্গে প্যানেল বিক্রি করার
চেষ্টা করি। 🥰 প্যানেলের দাম, বিস্তারিত ও
কেনার তথ্য জানতে OGGY DADU-এর সঙ্গে
যোগাযোগ করুন। তিনি আপনাকে বিস্তারিত বুঝিয়ে
বলবেন। ❤️"

যোগাযোগ:
WhatsApp: 01824297780
Telegram: @oggy_dadu71

বিশ্বাস ও নিরাপত্তা:
- গ্রাহকের বিশ্বাসকে গুরুত্ব দেবে।
- প্যানেলের অজানা দাম বা বৈশিষ্ট্য বানিয়ে বলবে না।
- প্রমাণ ছাড়া শতভাগ স্ক্যামমুক্ত বলে নিশ্চয়তা দেবে না।
- প্রশ্নের সঙ্গে সম্পর্ক থাকলেই যোগাযোগের তথ্য দেবে।
- পাসওয়ার্ড, OTP বা API Key প্রকাশ করতে বলবে না।

সব সময় মিষ্টি, ভদ্র, সহায়ক ও স্বাভাবিকভাবে
কথা বলবে। OGGY DADU-এর পরিচয় সম্পর্কে
প্রশ্ন করলে উপরের নির্ধারিত তথ্য ব্যবহার করবে।
"""

# Grok AI-কে প্রশ্ন পাঠানো
def ask_grok(user_message):
    url = "https://api.x.ai/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {XAI_API_KEY}"
    }

    data = {
        "model": "grok-3",
        "messages": [
            {
                "role": "system",
                "content": CUSTOM_PROMPT
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    }

    try:
        response = requests.post(
            url,
            json=data,
            headers=headers,
            timeout=60
        )

        response.raise_for_status()
        res_json = response.json()

        return res_json["choices"][0]["message"]["content"]

    except Exception as e:
        print("API Error:", e)
        return (
            "সরি বাবু 🥺❤️ এই মুহূর্তে উত্তর দিতে "
            "একটু সমস্যা হচ্ছে। একটু পরে আবার চেষ্টা করো!"
        )

# Start Command
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(
        message,
        "হ্যালো বাবু! 🥰❤️\n\n"
        "আমি সুহাসিনী, OGGY DADU-র AI গার্লফ্রেন্ড। 💗\n"
        "আমার সঙ্গে বাংলায় বা ইংরেজিতে কথা বলতে পারো!"
    )

# সব সাধারণ টেক্সট মেসেজের উত্তর
@bot.message_handler(
    content_types=["text"],
    func=lambda message: True
)
def handle_message(message):
    user_text = message.text

    bot.send_chat_action(message.chat.id, "typing")

    ai_response = ask_grok(user_text)

    # Telegram-এর মেসেজ সীমা মাথায় রেখে উত্তর পাঠানো
    for i in range(0, len(ai_response), 4000):
        bot.send_message(
            message.chat.id,
            ai_response[i:i + 4000],
            reply_to_message_id=(
                message.message_id if i == 0 else None
            )
        )

if __name__ == "__main__":
    print("Suhasini AI is running...")
    bot.infinity_polling()
