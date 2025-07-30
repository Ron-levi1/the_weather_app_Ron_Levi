
import requests
import matplotlib.pyplot as plt
from ipywidgets import Dropdown
from IPython.display import display

API_KEY = "69fc5c5baeb423ac0f0d33ba2e193c21"

weather_now_url = "http://api.openweathermap.org/data/2.5/weather"
weekly_weather_url = "https://api.openweathermap.org/data/2.5/onecall"

LANGUAGES = {
    "עברית": "he",
    "English": "en",
    "العربية": "ar"
}

language_choice = Dropdown(options=LANGUAGES.keys(), description="🌍 בחרי שפה:")
display(language_choice)

def weather_now(city, language):
    now_url = f"{weather_now_url}?q={city}&appid={API_KEY}&units=metric&lang={language}"
    response = requests.get(now_url)
    if response.status_code == 200:
        data = response.json()
        city_name = data["name"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"]
        print(f"\nמזג האוויר ב-{city_name}:")
        print(f"🌡 טמפרטורה: {temp}°C")
        print(f"💧 לחות: {humidity}%")
        print(f"☁ מצב השמיים: {description}")
        return data["coord"]["lat"], data["coord"]["lon"]
    else:
        print("❌ לא הצלחתי להביא נתונים. בדקי את שם העיר או את ה-API Key.")
        return None, None

def weekly_weather(lat, lon, city, language):
    weekly_url = f"{weekly_weather_url}?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang={language}&exclude=current,minutely,hourly,alerts"
    response = requests.get(weekly_url)
    if response.status_code == 200:
        forecast_data = response.json()
        days = []
        temps = []
        for i, day in enumerate(forecast_data["daily"][:7]):
            temp_day = day["temp"]["day"]
            temps.append(temp_day)
            days.append(f"יום {i+1}")
        plt.figure(figsize=(10,5))
        plt.plot(days, temps, marker="o", linestyle="solid")
        plt.title(f"📊 תחזית שבועית ל-{city}", fontsize=16)
        plt.xlabel("ימים", fontsize=12)
        plt.ylabel("טמפרטורה (°C)", fontsize=12)
        plt.grid(True)
        plt.show()
    else:
        print("❌ שגיאה בשליפת התחזית השבועית.")

city = input("🏙️ הקלידו שם עיר: ")

language = LANGUAGES[language_choice.value]

lat, lon = weather_now(city, language)

if lat and lon:
    print("\n📈 מציגה תחזית שבועית...")
    weekly_weather(lat, lon, city, language)
