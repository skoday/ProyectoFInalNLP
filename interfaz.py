import streamlit as st
import requests

# Título de la aplicación
st.title("Chat con API de FastAPI")

# Descripción
st.write("Esta aplicación permite hacer preguntas a una API de FastAPI y obtener respuestas.")

# Función para obtener la respuesta de la API
def obtener_respuesta(pregunta):
    api_url = "http://localhost:8000/pregunta"
    payload = {"pregunta": pregunta}
    response = requests.post(api_url, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Error al comunicarse con la API."}

# Interfaz de usuario tipo chat
st.subheader("Chat")

# Lista para almacenar el historial de mensajes
historial = []

# Función para mostrar los mensajes en el formato de chat
def mostrar_mensaje(texto, emisor, identificador):
    if emisor == "Usuario":
        st.text_area(f"Tú escribes {identificador}:", value=texto, height=100, key=f"user_{identificador}")
    elif emisor == "Bot":
        st.text_area(f"Bot responde {identificador}:", value=texto, height=100, key=f"bot_{identificador}")

# Input de usuario
pregunta = st.text_input("Tú escribes:", "")

# Botón para enviar la pregunta
if st.button("Enviar"):
    if pregunta:
        # Agregar pregunta al historial y mostrarla
        historial.append(("Usuario", pregunta))

        # Obtener respuesta del bot
        respuesta = obtener_respuesta(pregunta)
        if "error" in respuesta:
            # Mostrar error si no se pudo obtener la respuesta
            historial.append(("Bot", f"**Error:** {respuesta['error']}"))
        else:
            # Mostrar la respuesta del bot
            respuesta_texto = respuesta.get("answer", "No se obtuvo respuesta.")
            historial.append(("Bot", f"**Respuesta:** {respuesta_texto}"))

    else:
        st.text_area("Bot responde:", "Por favor, ingresa una pregunta.")

# Mostrar historial de mensajes
if historial:
    st.subheader("Historial del Chat")
    for i, mensaje in enumerate(historial):
        mostrar_mensaje(mensaje[1], mensaje[0], i)
