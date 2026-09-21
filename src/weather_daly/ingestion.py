
import requests

import pandas as pd

def  fetch_weather_data(lat, lon, start_date, end_date) -> pd.DataFrame:
    response = requests.get("https://archive-api.open-meteo.com/v1/archive", params={"latitude": lat,"longitude": lon,"start_date": start_date,"end_date": end_date, "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max", "timezone": "America/Sao_Paulo"})
    data = response.json()
    data = pd.DataFrame(data["daily"])

    return data    


