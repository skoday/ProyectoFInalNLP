from fastapi import FastAPI, HTTPException, Request
import pandas as pd
from transformers import pipeline

app = FastAPI()

# Global variables
questionanswer = None
clasificador = None
datos = None

# Function to initialize the variables
async def initialize_message():
    global datos
    datos = pd.read_csv("textos.csv")

    global clasificador
    clasificador = pipeline("text-classification", model="piturrolfio/bert-classifier-maths")

    global questionanswer
    questionanswer = pipeline("question-answering", model="piturrolfio/bert-finetuned-squad-es-test")

# Attach the function to the startup event of the FastAPI application
@app.on_event("startup")
async def on_startup():
    await initialize_message()

# Define a POST endpoint to receive the question
@app.post("/pregunta")
async def read_root(request: Request):
    global clasificador
    global datos
    global questionanswer

    try:
        body = await request.json()
        pregunta = body.get("pregunta")
        
        if not pregunta:
            raise HTTPException(status_code=400, detail="La pregunta es obligatoria")

        # Clasificar la pregunta
        clase_label = clasificador(pregunta)[0]["label"]
        clase_int = int(clase_label.split('_')[-1]) 

        # Obtener el texto correspondiente a la clase
        clase_int = int(clase_int)  # Asegurarse de que la clase es un entero
        print(type(clase_int))
        if clase_int in datos["clase"].unique():
            info = datos[datos["clase"] == clase_int]["texto"].values[0]
        else:
            raise HTTPException(status_code=404, detail="Clase no encontrada en los datos")

        # Obtener la respuesta a la pregunta usando el contexto
        final_answer = questionanswer(question=pregunta, context=info)
        return final_answer

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

