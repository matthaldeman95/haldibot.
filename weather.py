import requests



def get_weather(location):
    with open('weatherkey.txt') as infile:
        key = infile.read()
    encoded_location = location.replace(' ', '%20') + ',US'
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&APPID={}".format(encoded_location, key)
    r = requests.get(url)
    if r.status_code != 200:
        return "Unable to get weather data"
    data = r.json()
    desc = data['weather'][0]['main']
    temp = int(data['main']['temp'])
    return_string = "In {}, the weather is {} with a temperature of {}.".format(location.title(), desc, temp)
    return return_string

if __name__ == "__main__":
    print(get_weather("san jose"))