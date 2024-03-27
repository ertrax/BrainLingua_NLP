from tkinter import Text, Button, messagebox, ttk
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

# Caja de texto
caja_texto = Text
boton_analizar = Button
boton_limpiar_busqueda = Button
tabla = ttk.Treeview
