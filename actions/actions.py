import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionGetWeather(Action):
    def name(self) -> str:
        return "action_get_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:

        city = tracker.latest_message.get("text")

        if not city:
            dispatcher.utter_message(text="No pude identificar la ciudad.")
            return []

        try:
            print("claudio lindo")
            url = f"https://wttr.in/{city}?format=%t,+%C,+humedad+%h"
            response = requests.get(url, timeout=10)

            print("STATUS CODE:", response.status_code)
            print("RESPONSE TEXT:", response.text)

            if response.status_code != 200:
                dispatcher.utter_message(
                    text=f"No pude consultar el clima de {city} en este momento."
                )
                return []

            weather_text = response.text.strip()

            dispatcher.utter_message(
                text=f"En {city} actualmente hay: {weather_text}"
            )
            return []

        except Exception as e:
            print("ERROR EN ACTION SERVER:", e)
            dispatcher.utter_message(
                text="Hubo un problema al consultar la API del clima."
            )
            return []