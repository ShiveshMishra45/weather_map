from django.http import HttpResponse
import os
import requests
import folium
from django.views.decorators.csrf import csrf_exempt

def fetch_live_weather_data_by_city(api_key, city_name):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

@csrf_exempt  # This disables CSRF protection for this view
def index(request):
    if request.method == 'POST':
        city_name = request.POST.get('city')
        api_key = '45a9478f21851ae5fbc7ef7a6620e15c'
        weather_data = fetch_live_weather_data_by_city(api_key, city_name)

        if weather_data and 'main' in weather_data and 'coord' in weather_data:
            temperature = weather_data['main']['temp']
            lat = weather_data['coord']['lat']
            lon = weather_data['coord']['lon']

            # Create a map centered around the city
            m = folium.Map(location=[lat, lon], zoom_start=10)
            
            # Add a marker with the temperature
            folium.Marker(
                [lat, lon],
                popup=f"{city_name}: {temperature}°C"
            ).add_to(m)

            # Save the map to an HTML file
            map_filename = f'{city_name}_temperature_map.html'
            file_path = os.path.join(os.getcwd(), map_filename)
            m.save(file_path)

            # Return the file content as an HTTP response
            with open(file_path, 'r') as file:
                html_content = file.read()

            return HttpResponse(html_content)
        else:
            return HttpResponse("Could not retrieve weather data for the city.")
    else:
        form_html = '''
            <html>
            <body>
                <h1>Weather Finder</h1>
                <form method="post">
                    <label for="city">Enter city name:</label>
                    <input type="text" id="city" name="city" required>
                    <button type="submit">Get Weather</button>
                </form>
            </body>
            </html>
        '''
        return HttpResponse(form_html)
