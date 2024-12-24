import urllib.request
import json
from django.shortcuts import render

def index(request):
    data = {}
    error_message = None

    if request.method == 'POST':
        city = request.POST['city']

        try:
            source = urllib.request.urlopen(
                'http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=e7eabdf45f0299cd46884cf249371561'
            ).read()
            list_of_data = json.loads(source)

            # Check if the response contains a 404 error
            if list_of_data.get('cod') != 200:
                error_message = list_of_data.get('message', 'City not found.')
            else:
                data = {
                    "country_code": str(list_of_data['sys']['country']),
                    "coordinate": str(list_of_data['coord']['lon']) + ', ' + str(list_of_data['coord']['lat']),
                    "temp": str(list_of_data['main']['temp']) + ' °C',
                    "pressure": str(list_of_data['main']['pressure']),
                    "humidity": str(list_of_data['main']['humidity']),
                    'main': str(list_of_data['weather'][0]['main']),
                    'description': str(list_of_data['weather'][0]['description']),
                    'icon': list_of_data['weather'][0]['icon'],
                }
        except Exception as e:
            error_message = "An error occurred while processing your request."

    context = {
        'data': data,
        'error_message': error_message
    }
    return render(request, "main/index.html", context)
