import streamlit as st
import requests

st.title("Chat Conceptos Matematicos")

st.write("Pregunta lo conceptos fundamentales sobre aritmetica, algebra lineal, probabilidad, calculo y geometria analitica")

# Función para obtener la respuesta de la API
def obtener_respuesta(pregunta):
    api_url = "http://localhost:8000/pregunta"
    payload = {"pregunta": pregunta}
    response = requests.post(api_url, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Error al comunicarse con la API."}

st.subheader("Chat")

historial = []

def mostrar_mensaje(texto, emisor, identificador):
    if emisor == "Usuario":
        st.text_area(f"Tu mensaje {identificador}:", value=texto, height=100, key=f"user_{identificador}")
    elif emisor == "Bot":
        st.text_area(f"Respuesta {identificador}:", value=texto, height=100, key=f"bot_{identificador}")

# Input de usuario
pregunta = st.text_input("Tu mensaje:", "")

# Botón para enviar la pregunta
if st.button("Enviar"):
    if pregunta:
        # Agregar pregunta al historial y mostrarla
        historial.append(("Usuario", pregunta))

        respuesta = obtener_respuesta(pregunta)
        if "error" in respuesta:
            historial.append(("Bot", f"**Error:** {respuesta['error']}"))
        else:
            respuesta_texto = respuesta.get("answer", "No se obtuvo respuesta.")
            historial.append(("Bot", f"Respuesta: {respuesta_texto}"))

    else:
        st.text_area("Bot responde:", "Por favor, ingresa una pregunta.")

if historial:
    st.subheader("Historial del Chat")
    for i, mensaje in enumerate(historial):
        mostrar_mensaje(mensaje[1], mensaje[0], i)
