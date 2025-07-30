import requests
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime

import matplotlib
from matplotlib import rcParams

rcParams['font.family'] = 'Arial'
plt.rcParams['axes.unicode_minus'] = False



API_KEY = "69fc5c5baeb423ac0f0d33ba2e193c21"

weather_now_url = "http://api.openweathermap.org/data/2.5/weather"
forecast_url = "http://api.openweathermap.org/data/2.5/forecast"

LANGUAGES = {
    "עברית": "he",
    "English": "en"
}

TEXTS = {
    "עברית": {
        "title": "🌦 מה מזג האוויר?",
        "enter_city": "🏙️ בחר/י את העיר הרצויה:",
        "show_forecast": "📈 התחזית",
        "current_weather": "מזג האוויר כעת ב",
        "temp": "🌡 טמפרטורה:",
        "humidity": "💧 לחות:",
        "description": "☁ עננות:",
        "weekly_forecast": "📊 תחזית לחמשת הימים הקרובים ל",
        "no_city": "❗ הקלד/י שם עיר כדי להציג תחזית.",
        "fetch_error": "שגיאה! יש לבדוק את הנתונים שהזנת",
        "graph_label_days": "ימים",
        "graph_label_temp": "טמפרטורה (°C)"
    },
    "English": {
        "title": "🌦 What Is The Weather?",
        "enter_city": "🏙️ Enter a city:",
        "show_forecast": "📈 Show Forecast",
        "current_weather": "Current weather in",
        "temp": "🌡 Temperature:",
        "humidity": "💧 Humidity:",
        "description": "☁ Cloudiness:",
        "weekly_forecast": "📊 5-day forecast for",
        "no_city": "❗ Please enter a city name to show forecast.",
        "fetch_error": "❌ Could not fetch data. Check the city name.",
        "graph_label_days": "Days",
        "graph_label_temp": "Temperature (°C)"
    }
}

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        right: 0;
        left: auto;
    }
    section[data-testid="stSidebar"] > div:first-child {
        width: 200px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

language_choice = st.sidebar.radio("🌍 עברית / English", options=list(LANGUAGES.keys()))
language = LANGUAGES[language_choice]
text = TEXTS[language_choice]

if language_choice == "עברית":
    st.markdown("<style>body {direction: rtl; text-align: right;}</style>", unsafe_allow_html=True)
else:
    st.markdown("<style>body {direction: ltr; text-align: left;}</style>", unsafe_allow_html=True)

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
        st.write(f"{text['description']} {description}")
    else:
        st.error(text["fetch_error"])

def five_day_forecast(city, language):
    url = f"{forecast_url}?q={city}&appid={API_KEY}&units=metric&lang={language}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        forecast_list = data["list"]

        days = {}
        for entry in forecast_list:
            date = datetime.fromtimestamp(entry["dt"]).strftime("%d/%m")
            temp = entry["main"]["temp"]
            if date not in days:
                days[date] = []
            days[date].append(temp)

        avg_temps = {day: sum(temps) / len(temps) for day, temps in days.items()}
        first_5_days = list(avg_temps.keys())[:5]
        temps_for_graph = [avg_temps[day] for day in first_5_days]

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(first_5_days, temps_for_graph, marker="o", linestyle="solid")
        ax.set_title(f"{text['weekly_forecast']} {city}", fontsize=16)
        ax.set_xlabel(text["graph_label_days"], fontsize=12)
        ax.set_ylabel(text["graph_label_temp"], fontsize=12)
        ax.grid(True)
        st.pyplot(fig)
    else:
        st.error(text["fetch_error"])

if st.button(text["show_forecast"]):
    if city:
        weather_now(city, language)
        five_day_forecast(city, language)
    else:
        st.warning(text["no_city"])
