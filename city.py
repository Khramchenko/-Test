
import pprint
import requests
from dateutil.parser import parse

class YahooWeatherForecast:

# cach данных по городам
    def __init__(self):
        # dict 
        self._city_cache = {}

# делать запросы к API Yahoo для получения данных
    def get(self, city): # принимает город
        # если город есть в словаре возвращаем данные 
        if city in self._city_cache:
            return self._city_cache[city]
        print("sending HTTP request")
        url = f"https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22{city}%22)%20and%20u%3D%22c%22&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"
        data = requests.get(url).json() #преобразуем json данные в python словарь
        forecast_data = data["query"]["results"]["channel"]["item"]["forecast"]
        forecast = []
        for day_data in forecast_data:
            # выбираем из словаря forecast_data необходимые данные и ложим их в словарь forecast
            forecast.append({"date": parse(day_data["date"]), 
            "high_temp": day_data["high"]
            })
        # каждый раз получения данных обновляем словарь 
        self._city_cache[city] = forecast
        return forecast

class CityInfo:

# принимает название города
    def __init__(self, city, weather_forecast=None):
        self.city = city
        # приватная переманная для экземпляра класса
        self._weather_forecast = weather_forecast or YahooWeatherForecast() # инициализация?

# метод будет возвращать прогноз погоды
    def weather_forecast(self):
        # обращаемся к приватной переменной и вызываем метог get и передаем ему город self city
        return self._weather_forecast.get(self.city)

def _main():
    weather_forecast = YahooWeatherForecast()
    # симмулируем несколько запросов
    for i in range(5):
        city_info= CityInfo("moscow", weather_forecast = weather_forecast)
    # метод weather_forecast вернет прогноз погоды на несколько дней вперед
        city_info.weather_forecast() 
    #pprint.pprint(forecast)

if __name__ == "__main__":
    _main()
