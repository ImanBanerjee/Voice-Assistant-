import requests

def get_weather_with_aqi(city):
    try:
        api_key = '57ebaed63fae4c149e5115051231711'
        base_url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=yes'
        response = requests.get(base_url)
        weather_data = response.json()

        if 'error' in weather_data:
            print(f"Failed to fetch weather data. Error: {weather_data['error']['message']}")
            return None
        else:
            # Process weather data
            temperature_celsius = weather_data['current']['temp_c']
            condition = weather_data['current']['condition']['text']
            aqi = weather_data['current']['air_quality']['us-epa-index']
            
            return f"The weather in {city} is {condition} with a temperature of {temperature_celsius} degrees Celsius. AQI: {aqi}"
    except Exception as e:
        print(f"Error fetching weather information: {e}")
        return None

if __name__ == "__main__":
    city = input("Enter the city: ")
    result = get_weather_with_aqi(city)

    if result:
        print(result)
    else:
        print("Weather information not available.")
