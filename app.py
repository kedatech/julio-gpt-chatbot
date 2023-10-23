import os
import json

from flask import Flask, request, jsonify
from flask_cors import CORS
from openai_client import queryEmbeddings
from process import process_files, query_collection, speechTotext
from decouple import config

PORT = config('PORT')

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def index():
    return "This is the index :b try with: /query or /process"

@app.route('/process', methods=['POST'])
def process():
    archivos = getDocumets()
    process_files(archivos)
    response = {'success': True}
    return jsonify(response)

@app.route('/query', methods=['GET'])
async def query():
    query = request.args.get('text')
    collections = query_collection(query)
    response = await queryEmbeddings(query, collections)

    return jsonify(json.loads(response))


@app.route("/speech", methods=['GET'])
async def speech():
    return "This is a construct request 🔨"
    # query = request.args.get('text')
    # collections = query_collection(query)
    # response = await queryEmbeddings(query, collections)

    # return jsonify(json.loads(response))


    

def getDocumets():
    carpeta_archivos = 'Markdowns/'
    archivos = []
    nombres_archivos = os.listdir(carpeta_archivos)

    # Recorre la lista de nombres de archivos y abre cada archivo
    for nombre_archivo in nombres_archivos:
        ruta_archivo = os.path.join(carpeta_archivos, nombre_archivo)

        # Verifica si es un archivo (no un directorio) antes de abrirlo
        if os.path.isfile(ruta_archivo):
            with open(ruta_archivo, 'r') as archivo:
                contenido = archivo.read()
                archivos.append({'filename': nombre_archivo, 'content': contenido})

    return archivos


