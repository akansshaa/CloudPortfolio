import requests
import customtkinter as ctk
from tkinter import messagebox


def get_weather():
    city = city_entry.get()

    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name")
        return

    try:
        # Geo API - Cloud Call
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
        geo_response = requests.get(geo_url).json()

        if "results" not in geo_response:
            messagebox.showerror("Error", "City not found")
            return

        lat = geo_response["results"][0]["latitude"]
        lon = geo_response["results"][0]["longitude"]

        # Weather API - Cloud Call
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
            "&current_weather=true"
        )
        weather_response = requests.get(weather_url).json()

        weather = weather_response["current_weather"]
        temp = weather["temperature"]
        wind = weather["windspeed"]

        result_label.configure(
            text=(
                f"📍 City: {city}\n\n"
                f"🌡 Temperature: {temp}°C\n"
                f"💨 Wind Speed: {wind} km/h"
            )
        )

    except Exception:
        messagebox.showerror("Error", "Unable to fetch weather information")


# ---------------- GUI Setup ----------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.title("🌤️ Cloud Weather App")
root.geometry("460x500")
root.resizable(False, False)


# Main outer frame (glass effect)
outer_frame = ctk.CTkFrame(root, corner_radius=25, fg_color="#1B1F24")
outer_frame.pack(padx=30, pady=30, fill="both", expand=True)


# Header
header = ctk.CTkLabel(
    outer_frame,
    text="🌤️ Live Cloud Weather",
    font=("Arial Rounded MT Bold", 26),
    text_color="white",
)
header.pack(pady=25)


# City Input Box
city_frame = ctk.CTkFrame(outer_frame, fg_color="#2B323A", corner_radius=15)
city_frame.pack(pady=10)

city_icon = ctk.CTkLabel(city_frame, text="🏙️", font=("Arial", 20))
city_icon.pack(side="left", padx=10)

city_entry = ctk.CTkEntry(
    city_frame,
    placeholder_text="Enter city name...",
    width=250,
    height=40,
    font=("Arial", 15),
)
city_entry.pack(side="left", padx=10, pady=5)


# Search Button
search_button = ctk.CTkButton(
    outer_frame,
    text="Search Weather",
    width=230,
    height=45,
    corner_radius=15,
    font=("Arial Bold", 17),
    fg_color="#00A86B",
    hover_color="#009960",
    command=get_weather,
)
search_button.pack(pady=20)


# Result Display Card
result_card = ctk.CTkFrame(
    outer_frame, fg_color="#23282F", corner_radius=20, width=300, height=180
)
result_card.pack(pady=25)

result_label = ctk.CTkLabel(
    result_card,
    text="",
    font=("Arial Rounded MT Bold", 18),
    justify="center",
    text_color="#E9E9E9",
)
result_label.pack(pady=20)


root.mainloop()
