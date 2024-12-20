USE_ROUNDED_COORDINATES = False

SAVE_TO_STORAGE = True

GET_OUTER_IP_URL = "https://ipinfo.io/json"

OPENWEATHER_API = "f478b3c0750f72b08780aa0758a91cc3"

OPENWEATHER_URL_TEMPLATE = (
    "https://api.openweathermap.org/data/2.5/weather?"
    "lat={latitude}&lon={longitude}&"
    "appid=" + OPENWEATHER_API + "&lang=ru&"
    "units=metric"
)
