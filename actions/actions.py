# (Capa de Ejecución) :
# * Script en Python que contiene la lógica de backend del asistente.
# * Ejecuta tareas fuera del modelo predictivo de lenguaje.

# -----------------------------------------------------------------------------

import requests
import datetime
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import ReminderScheduled, SlotSet

class ActionConsultarDragonBall(Action):
    def name(self) -> Text:
        return "action_consultar_dragonball"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # 1. Recuperar memoria de los slots
        nombre = tracker.get_slot("nombre_personaje")
        atributo = tracker.get_slot("atributo")

        if not nombre:
            dispatcher.utter_message(text="No especificaste qué personaje buscar.")
            return []

        # 1. Petición inicial para obtener el ID
        url_busqueda = f"https://dragonball-api.com/api/characters?name={nombre}"
        try:
            response_busqueda = requests.get(url_busqueda)
            datos_lista = response_busqueda.json()
            
            if not datos_lista or len(datos_lista) == 0:
                dispatcher.utter_message(text=f"No encontré registros en la base de datos para {nombre}.")
                return [SlotSet("nombre_personaje", None), SlotSet("atributo", None)]
            
            # Extraer el ID numérico
            personaje_id = datos_lista[0].get("id")

            # 2. Petición secundaria para obtener el JSON completo
            url_detalle = f"https://dragonball-api.com/api/characters/{personaje_id}"
            response_detalle = requests.get(url_detalle)
            personaje_completo = response_detalle.json()

            # 3. Lógica condicional de atributos normalizada
            if atributo:
                diccionario_atributos = {
                    "ki": "ki",
                    "raza": "race",
                    "género": "gender",
                    "afiliación": "affiliation",
                    "transformaciones": "transformations"
                }
                clave = diccionario_atributos.get(atributo.lower())
                
                if clave and clave in personaje_completo:
                    valor = personaje_completo[clave]
                    dispatcher.utter_message(text=f"El/la {atributo} de {nombre} es: {valor}.")
                else:
                    dispatcher.utter_message(text=f"El dato '{atributo}' no está disponible para este personaje.")
            else:
                descripcion = personaje_completo.get("description", "Sin descripción.")
                dispatcher.utter_message(text=f"Datos de {nombre}: {descripcion}")

        except Exception as e:
            dispatcher.utter_message(text="Error interno al procesar la API.")

        # 4. Limpiar memoria obligatoriamente para consultas futuras
        return [SlotSet("nombre_personaje", None), SlotSet("atributo", None)]


class ActionProgramarInactividad(Action):
    def name(self) -> Text:
        return "action_programar_inactividad"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Calcular fecha límite agregando 60 segundos al reloj actual
        fecha_desconexion = datetime.datetime.now() + datetime.timedelta(seconds=60)
        
        # Generar evento interno
        reminder = ReminderScheduled(
            "EXTERNAL_no_input",
            trigger_date_time=fecha_desconexion,
            name="timer_inactividad",
            kill_on_user_message=True # Cancela el temporizador si el usuario escribe
        )
        return [reminder]