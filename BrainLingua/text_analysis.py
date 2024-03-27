from tkinter import Text, Button, ttk
import tkinter as tk
from nltk.tokenize import word_tokenize
import nltk
import re
from nltk import pos_tag
from collections import Counter

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

mapeo_etiquetas_espanol_ingles = {
    'Sustantivo': 'NN',
    'Sustantivo propio': 'NNP',
    'Conjunción de coordinación': 'CC',
    'Preposición': 'IN',
    'Adjetivo': 'JJ'
}

# Define caja_texto, boton_analizar, boton_limpiar_busqueda y tabla como atributos globales
caja_texto = None
boton_analizar = None
boton_limpiar_busqueda = None
tabla = None

def contar_palabras_texto(texto):
    tokens = [token for token in word_tokenize(texto) if re.match(r'^\w+$', token)]
    num_palabras = len(tokens)
    return num_palabras

def etiquetar_gramaticalmente_texto(mensaje):
    tokens = word_tokenize(mensaje)
    tokens_sin_puntuacion = [token for token in tokens if re.match(r'^\w+$', token)]
    tagged_tokens = pos_tag(tokens_sin_puntuacion)
    tagged_tokens_ingles = [(word, mapeo_etiquetas_espanol_ingles.get(tag, tag)) for word, tag in tagged_tokens]
    conteo_etiquetas = Counter(tag for word, tag in tagged_tokens_ingles)
    return conteo_etiquetas

def analizar_texto():
    texto = caja_texto.get("1.0", "end-1c")
    conteo_palabras = contar_palabras_texto(texto)
    etiquetas_gramaticales = etiquetar_gramaticalmente_texto(texto)
    limpiar_tabla()
    tabla.insert("", "end", values=("Número de palabras", conteo_palabras))
    for etiqueta, frecuencia in etiquetas_gramaticales.items():
        tabla.insert("", "end", values=(etiqueta, frecuencia))

def limpiar_tabla():
    for item in tabla.get_children():
        tabla.delete(item)

# Crea la interfaz de usuario para el análisis de texto
def crear_interfaz_texto(ventana):
    global caja_texto, boton_analizar, boton_limpiar_busqueda, tabla
    # Caja de texto
    caja_texto = Text(ventana, height=10, width=50)
    caja_texto.pack()

    # Botón para analizar texto
    boton_analizar = Button(ventana, text="Analizar Texto", command=analizar_texto)
    boton_analizar.pack()

    # Botón para limpiar la búsqueda
    boton_limpiar_busqueda = Button(ventana, text="Limpiar Búsqueda", command=limpiar_tabla)
    boton_limpiar_busqueda.pack()

    # Creamos el Treeview para mostrar la tabla
    tabla = ttk.Treeview(ventana)
    tabla["columns"] = ("Atributo", "Valor")
    tabla.column("#0", width=0, stretch=tk.NO)  # Columna invisible
    tabla.column("Atributo", anchor=tk.W, width=150)
    tabla.column("Valor", anchor=tk.CENTER, width=150)  # Alineación al centro
    tabla.heading("Atributo", text="Atributo")
    tabla.heading("Valor", text="Valor")
    tabla.pack()
