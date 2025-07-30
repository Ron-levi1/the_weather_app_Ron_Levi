import requests
import matplotlib.pyplot as plt
import streamlit as st

API_KEY = "69fc5c5baeb423ac0f0d33ba2e193c21"

weather_now_url = "http://api.openweathermap.org/data/2.5/weather"
weekly_weather_url = "https://api.openweathermap.org/data/2.5/onecall"

LANGUAGES = {
    "עברית": "he",
    "English": "en"
}

TEXTS = {
    "עברית": {
        "title": "🌦 מה מזג האוויר?",
        "select_language": "בחר/י שפה",
        "enter_city": "🏙️ בחר/י את העיר הרצויה:",
        "show_forecast": "📈 התחזית",
        "current_weather": "מזג האוויר כעת ב",
        "temp": "🌡 טמפרטורה:",
        "humidity": "💧 לחות:",
        "weekly_forecast": "📊 תחזית שבועית ל",
        "no_city": "❗ הקלד/י שם עיר כדי להציג תחזית.",
        "fetch_error": "שגיאה! יש לבדוק את הנתונים שהזנת",
        "graph_label_days": "ימים",
        "graph_label_temp": "טמפרטורה (°C)"
    },
    "English": {
        "title": "🌦 What Is The Weather?",
        "select_language": "Language",
        "enter_city": "🏙️ Enter a city:",
        "show_forecast": "📈 Show Forecast",
        "current_weather": "Current weather in",
        "temp": "🌡 Temperature:",
        "humidity": "💧 Humidity:",
        "weekly_forecast": "📊 Weekly forecast for",
        "no_city": "❗ Please enter a city name to show forecast.",
        "fetch_error": "❌ Could not fetch data. Check city name or API Key.",
        "graph_label_days": "Days",
        "graph_label_temp": "Temperature (°C)"
    }
}

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
    /* מעביר את הסיידבר לצד ימין */
    [data-testid="stSidebar"] {
        right: auto;
        left: 0;
    }
    /* עושה אותו צר יותר */
    section[data-testid="stSidebar"] > div:first-child {
        width: 300px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

language_choice = st.sidebar.selectbox("🌍 עברית / English", options=list(LANGUAGES.keys()))
language = LANGUAGES[language_choice]
text = TEXTS[language_choice]

st.title(text["title"])
city = st.text_input(text["enter_city"])

def weather_now(city, language):
    now_url = f"{weather_now_url}?q={city}&appid={API_KEY}&units=metric&lang={language}"
    response = requests.get(now_url)
    if response.status_code == 200:
        data = response.json()
        city_name = data["name"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"]
        st.subheader(f"{text['current_weather']} {city_name}:")
        st.write(f"{text['temp']} {temp}°C")
        st.write(f"{text['humidity']} {humidity}%")
        st.write(f"{description}")
        return data["coord"]["lat"], data["coord"]["lon"]
    else:
        st.error(text["fetch_error"])
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
            days.append(f"{text['graph_label_days']} {i+1}")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(days, temps, marker="o", linestyle="solid")
        ax.set_title(f"{text['weekly_forecast']} {city}", fontsize=16)
        ax.set_xlabel(text["graph_label_days"], fontsize=12)
        ax.set_ylabel(text["graph_label_temp"], fontsize=12)
        ax.grid(True)
        st.pyplot(fig)
    else:
        st.error(text["fetch_error"])

if st.button(text["show_forecast"]):
    if city:
        lat, lon = weather_now(city, language)
        if lat and lon:
            weekly_weather(lat, lon, city, language)
    else:
        st.warning(text["no_city"])
