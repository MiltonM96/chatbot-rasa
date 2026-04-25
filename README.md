# chatbot-rasa

<br>

## ¿Qué es Rasa?
* **Framework de código abierto:** Basado en aprendizaje automático (Machine Learning) para la creación de asistentes conversacionales.
* **Estructura lógica:** Utiliza archivos de configuración para organizar la comprensión del lenguaje y la toma de decisiones.
* **Capacidades externas:** Permite la conexión a APIs para dotar al bot de funciones transaccionales y acceso a datos en tiempo real.

<br>

## ¿Qué es un chatbot y cómo funciona?
* **Definición:** Sistema de software diseñado para procesar lenguaje natural y simular interacciones lógicas con humanos.
* **Motores de Rasa:**
  * **NLU (Natural Language Understanding):** Interpreta el texto para extraer la intención del usuario y datos clave (entidades).
  * **Core:** Gestor de diálogo que evalúa el contexto histórico para predecir la siguiente acción.
* **Arquitectura modular:** Separa estrictamente la comprensión lingüística de la lógica de negocio técnica.

<br>

## Arquitectura de archivos en Rasa

### `nlu.yml` (Datos de Entrenamiento)
* Almacena ejemplos de frases para entrenar los modelos de clasificación.
* Ayuda al bot a identificar la intención real (*intent*) detrás de diversas formas de escribir.

### `domain.yml` (Registro de Componentes)
* Funciona como el inventario central o manifiesto del sistema.
* Declara intenciones, acciones y plantillas de respuesta (*utterances*) que el bot puede utilizar.

### `rules.yml` (Lógica Invariable)
* Establece reglas rígidas que fuerzan acciones específicas ante condiciones exactas.
* Se utiliza para flujos que no requieren predicción estadística, como el *chit-chat* o la inactividad.

### `config.yml` (Pipeline de Procesamiento)
* Define los hiperparámetros y algoritmos de IA (tokenizadores, clasificadores como *DIETClassifier*).
* Configura cómo se procesará el texto durante la fase de entrenamiento.

### `endpoints.yml` (Enrutamiento de Servicios)
* Gestiona las conexiones entre el núcleo de Rasa y servicios externos.
* Especifica la ubicación del servidor de acciones personalizadas (Action Server).

### `credentials.yml` (Autenticación de Canales)
* Centraliza tokens y claves de seguridad.
* Habilita la integración con plataformas como Slack, Telegram o interfaces web.

### `actions.py` (Capa de Ejecución)
* Script en Python que contiene la lógica de backend del asistente.
* Ejecuta tareas fuera del modelo predictivo de lenguaje.

<br>

## Rol de la integración con API
* **Desacoplamiento:** Separa la comprensión del diálogo de la gestión técnica de datos.
* **Flujo asíncrono:** El bot predice la necesidad de datos y delega la petición HTTP al script `actions.py`.
* **Procesamiento de datos:** El servidor de acciones maneja la respuesta de la API (JSON) y devuelve la información procesada al núcleo.
* **Estabilidad:** Evita bloqueos en la interfaz de usuario ante latencias o errores en servicios externos.

<br>

## Pasos para ejecutar el Bot

### `Entrenar el modelo`: rasa train
* Aguarde hasta que el proceso finalice y la consola indique que un nuevo modelo ha sido empaquetado y guardado exitosamente.

### `Iniciar el servidor de acciones (Action Server)`: rasa run actions
* La terminal quedará en ejecución continua y mostrará un mensaje indicando que el servidor está escuchando en el puerto 5055.

### `Iniciar la interfaz de chat`: rasa shell
* Cuando aparezca el prompt Your input ->, el sistema estará listo. Puede proceder a escribir "conectar a la api" para evaluar el requerimiento de red, "hace calor hoy" para verificar la interrupción por chit-chat, o esperar 60 segundos sin ingresar texto para comprobar el cumplimiento de la regla de no-input.