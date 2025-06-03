from bs4 import BeautifulSoup
import requests
import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import re
import os




# URL
url = 'https://meteo.ua/ua/34/kiev#2025-01-22--15-00'
response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'lxml')
    temp = soup.find('div', class_='weather-detail__main-temp js-weather-detail-value').text
    loc = soup.find('div', class_='weather-detail__main-title js-weather-detail-value mob-hide').text
    loc1 = loc.split(',')[0]+', '+loc.split(',')[1]
    loc2 = ', '+loc.split(',')[2]
    press = soup.find('div', class_='weather-detail__extra-data js-weather-detail-value').text
    wind_speed = soup.find('span', class_='js-weather-detail-value').text
    wet = soup.find('div', class_='weather-detail__extra-data js-weather-detail-value', attrs={'data-key':'humidity'}).text
    weather = soup.find('div', class_='weather-detail__main-specification js-weather-detail-value', attrs={'data-key':'info'}).text
    image_data = soup.find('div', class_='weather-detail__main-specification js-weather-detail-value', attrs={'data-key':'info'}).text
    svg_element = soup.find('svg', class_='weather-detail__wind-direction')
    style_attribute = svg_element['style']
    rotation_angle = re.findall(r'rotate\((-?\d+deg)\)', style_attribute)[0]
    rotation_angle = int(rotation_angle[:-3])

else:
    temp = "Connection Error"
    loc = "Connection Error"
    press = "Connection Error"
    wind_speed = "Connection Error"
    wet = "Connection Error"
    weather = "Connection Error"

# Window
window = tk.Tk()
window.title('Weather Broadcast')
window.geometry("460x340")
window.resizable(False, False)

# Image
current_directory = os.path.dirname(os.path.abspath(__file__))

sun = PhotoImage(file=os.path.join(current_directory, 'sunny.png'))
cold = PhotoImage(file=os.path.join(current_directory, 'clouds.png'))
heavy_rain = PhotoImage(file=os.path.join(current_directory, 'heavy_rain.png'))
heavy_rain_and_thunder = PhotoImage(file=os.path.join(current_directory, 'heavy_rain_and_thunder.png'))
partly_sunny = PhotoImage(file=os.path.join(current_directory, 'partly_sunny.png'))
rain = PhotoImage(file=os.path.join(current_directory, 'rain.png'))
snow = PhotoImage(file=os.path.join(current_directory, 'snow.png'))
windy = PhotoImage(file=os.path.join(current_directory, 'wind.png'))
arrow = Image.open(os.path.join(current_directory, 'arrow.png'))
rotated_image = arrow.rotate(rotation_angle)
rotated_arrow = ImageTk.PhotoImage(rotated_image)

if image_data == 'сильна хмарність'or image_data == 'помірна хмарність':
    image = cold
elif image_data == 'ясне небо':
    image = sun
elif image_data == 'xxx': # When the program was written, there was no such data, but it is possible that it will appear in the future
    image = heavy_rain
elif image_data == 'похмура погода' or image_data == 'легка хмарність':
    image = partly_sunny
elif image_data == 'невеликий сніг' or image_data == 'дощ зі снігом' or image_data == 'сніг':
    image = snow
elif image_data == 'xxx': # When the program was written, there was no such data, but it is possible that it will appear in the future
    image = heavy_rain_and_thunder
elif image_data == 'невеликий дощ' or image_data == 'помірний дощ':
    image = rain

# Frame
frame = tk.Frame(window, bg='#F7F7F7')
frame.pack(fill=tk.BOTH, expand=True)
frame.lower()

# Widgets
city_label = tk.Label(window, text=f'{loc1}', font=('Gvenetica', 16, 'bold'), bg='#F7F7F7')
city_label.place(x=40, y=20) 

city_label = tk.Label(frame, text=f'{loc2}', font=('Gvenetica', 16, 'bold'), bg='#F7F7F7')
city_label.place(x=280, y=20) 

weather_label = tk.Label(frame, text=weather.capitalize(), font=('Arial', 15, ),bg='#F7F7F7') 
weather_label.place( x=40, y=140)

temp_label = tk.Label(frame, text=f' {temp}°C', font=('Arial', 40, ), bg='#F7F7F7')
temp_label.place(x=50, y=70)

pressure_label = tk.Label(frame, text=f'Тиск: {press}', font=('Arial', 15, ),bg='#F7F7F7')
pressure_label.place(x=40, y=180)

wet_label = tk.Label(frame, text=f'Вологість: {wet}',font=('Arial', 15, ),bg='#F7F7F7')
wet_label.place(x=40, y=220)

wind_label = tk.Label(frame, text=f'Швидкість вітру та напрям: {wind_speed}',font=('Arial', 15, ),bg='#F7F7F7')
wind_label.place(x=40, y=260)

img_label = tk.Label(frame, image=image)
img_label.place(x=250, y=50)

arrow_label = tk.Label(frame, image=rotated_arrow)
arrow_label.place(x=380, y=260)

if __name__ == "__main__":
    window.mainloop()
