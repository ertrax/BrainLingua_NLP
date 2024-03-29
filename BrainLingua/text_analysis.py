from tkinter import Text, Button, messagebox, ttk
import tkinter as tk
from nltk.tokenize import word_tokenize
import nltk
import re
from nltk import pos_tag
from collections import Counter
from nltk.tokenize import sent_tokenize
from palabras_malsonantes import palabras_malsonantes  # Importa la lista de palabras malsonantes
from negaciones import negaciones  # Importa la lista de palabras malsonantes

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


caja_texto = None  
tabla = None  # Define tabla como una variable global y asigna None

# Diccionario de mapeo de etiquetas gramaticales
mapeo_etiquetas_espanol_ingles = {
    'Sustantivo': 'NN',
    'Sustantivo propio': 'NNP',
    'Conjunción de coordinación': 'CC',
    'Preposición': 'IN',
    'Adjetivo': 'JJ',
    'Verbo': 'VB',  
    'Adverbio': 'RB',
    'Pronombre': 'PRP',
    'Determinante': 'DT',
    'Puntuación': '.',
    'Número': 'CD',
    'Interjección': 'UH',
    'Conjunción subordinada': 'IN'
}

# Lista de atributos predefinidos
atributos_predefinidos = ["Número de palabras", "Numero de frases", "Sustantivos", "Sustantivos propios",
                           "Conjunciones de coordinación", "Preposiciones", "Adjetivos",
                           "Verbos", "Adverbios", "Pronombres", "Determinantes",
                           "Puntuación", "Números", "Interjecciones", "Conjunciones subordinadas", "Palabras malsonantes",
                           "Negaciones", "Palabras por frase"]

def contar_palabras_texto(texto):
    tokens = [token for token in word_tokenize(texto) if re.match(r'^\w+$', token)]
    num_palabras = len(tokens)
    return num_palabras

def contar_oraciones(texto):
    # Utiliza sent_tokenize para dividir el texto en oraciones
    oraciones = sent_tokenize(texto)
    # Cuenta cuántas oraciones hay
    num_oraciones = len(oraciones)
    return num_oraciones

def etiquetar_gramaticalmente_texto(mensaje):
    tokens = word_tokenize(mensaje)
    tokens_sin_puntuacion = [token for token in tokens if re.match(r'^\w+$', token)]
    tagged_tokens = pos_tag(tokens_sin_puntuacion)
    tagged_tokens_ingles = [(word, mapeo_etiquetas_espanol_ingles.get(tag, tag)) for word, tag in tagged_tokens]
    conteo_etiquetas = Counter(tag for word, tag in tagged_tokens_ingles)
    return conteo_etiquetas

def obtener_valores_atributos(texto):
    conteo_palabras = contar_palabras_texto(texto)
    conteo_oraciones = contar_oraciones(texto)
    etiquetas_gramaticales = etiquetar_gramaticalmente_texto(texto)
    palabras_malsonantes_detectadas = detectar_palabras_malsonantes(texto)
    palabras_negativas_detectadas = detectar_negaciones(texto)
    palabras_por_frase = contar_palabras_por_frase(texto)
    valores_atributos = {
        "Número de palabras": conteo_palabras,
        "Número de frases": conteo_oraciones,
        "Palabras por frase": palabras_por_frase,
        "Sustantivos": etiquetas_gramaticales.get("NN", 0),
        "Sustantivos propios": etiquetas_gramaticales.get("NNP", 0),
        "Conjunciones de coordinación": etiquetas_gramaticales.get("CC", 0),
        "Preposiciones": etiquetas_gramaticales.get("IN", 0),
        "Adjetivos": etiquetas_gramaticales.get("JJ", 0),
        "Verbos": etiquetas_gramaticales.get("VB", 0),
        "Adverbios": etiquetas_gramaticales.get("RB", 0),
        "Pronombres": etiquetas_gramaticales.get("PRP", 0),
        "Determinantes": etiquetas_gramaticales.get("DT", 0),
        "Puntuación": etiquetas_gramaticales.get(".", 0),
        "Números": etiquetas_gramaticales.get("CD", 0),
        "Interjecciones": etiquetas_gramaticales.get("UH", 0),
        "Conjunciones subordinadas": etiquetas_gramaticales.get("IN", 0),
        "Palabras malsonantes": len(palabras_malsonantes_detectadas),
        "Negaciones": palabras_negativas_detectadas  # Elimina len() aquí
    }
    return valores_atributos


def analizar_texto():
    texto = caja_texto.get("1.0", "end-1c")
    valores_atributos = obtener_valores_atributos(texto)
    limpiar_tabla()
    for atributo, valor in valores_atributos.items():
        tabla.insert("", "end", values=(atributo, valor))

def detectar_palabras_malsonantes(texto):
    # Convertir el texto a minúsculas
    texto_minusculas = texto.lower()
    # Convertir las palabras malsonantes a minúsculas
    palabras_malsonantes_minusculas = [palabra.lower() for palabra in palabras_malsonantes]
    # Tokenizar el texto en palabras
    tokens = word_tokenize(texto_minusculas)
    # Buscar palabras malsonantes en el texto
    palabras_malsonantes_detectadas = [palabra for palabra in tokens if palabra in palabras_malsonantes_minusculas]
    return palabras_malsonantes_detectadas

def detectar_negaciones(texto):
    # Convertir el texto a minúsculas
    texto_minusculas = texto.lower()
    # Convertir las negaciones a minúsculas
    negaciones_minusculas = [negacion.lower() for negacion in negaciones]
    # Tokenizar el texto en frases
    frases = sent_tokenize(texto_minusculas)
    # Contador de negaciones
    contador_negaciones = 0
    # Iterar sobre cada frase
    for frase in frases:
        # Tokenizar la frase en palabras
        tokens = word_tokenize(frase)
        # Buscar negaciones en la frase
        for negacion in negaciones_minusculas:
            if negacion in tokens:
                # Si se encuentra una negación en la frase, sumar 1 al contador y salir del bucle
                contador_negaciones += 1
                break  # Salir del bucle interno
    return contador_negaciones

def contar_palabras_por_frase(texto):
    # Utiliza sent_tokenize para dividir el texto en oraciones
    oraciones = sent_tokenize(texto)
    
    # Crea una lista para almacenar el número de palabras por frase
    num_palabras_por_frase = []
    
    # Itera sobre cada frase y cuenta las palabras
    for frase in oraciones:
        palabras_en_frase = len([token for token in word_tokenize(frase) if re.match(r'^\w+$', token)])
        num_palabras_por_frase.append(palabras_en_frase)
    
    return num_palabras_por_frase



def limpiar_tabla():
    for item in tabla.get_children():
        tabla.delete(item)

from tkinter import Text, Button, ttk, Tk, LEFT, RIGHT, CENTER

def crear_interfaz_texto(ventana):
    global caja_texto, boton_analizar, boton_limpiar_busqueda, tabla

    # Caja de texto
    caja_texto = Text(ventana, height=20, width=50)
    caja_texto.grid(row=0, column=0, padx=10, pady=10, rowspan=2)  # Se extiende desde la fila 0 hasta la 1 y columna 0

    # Botón para analizar texto
    boton_analizar = Button(ventana, text="Analizar Texto", command=analizar_texto)
    boton_analizar.grid(row=0, column=1, padx=10, pady=10, sticky="ew")  # Se encuentra en la fila 0 y columna 1

    # Botón para limpiar la búsqueda
    boton_limpiar_busqueda = Button(ventana, text="Limpiar Búsqueda", command=limpiar_tabla)
    boton_limpiar_busqueda.grid(row=1, column=1, padx=10, pady=10, sticky="ew")  # Se encuentra en la fila 1 y columna 1

    # Creamos el Treeview para mostrar la tabla
    tabla = ttk.Treeview(ventana)
    tabla["columns"] = ("Atributo", "Valor")
    tabla.column("#0", width=0, stretch=tk.NO)  # Columna invisible
    tabla.column("Atributo", anchor=tk.W, width=500)
    tabla.column("Valor", anchor=tk.CENTER, width=200)  # Alineación al centro
    tabla.heading("Atributo", text="Atributo")
    tabla.heading("Valor", text="Valor")
    tabla.grid(row=0, column=2, padx=10, pady=10, rowspan=2)  # Se extiende desde la fila 0 hasta la 1 y columna 2

    # Insertar atributos predefinidos en la tabla
    for atributo in atributos_predefinidos:
        tabla.insert("", "end", values=(atributo, ""))

# Llamada a la función para crear la interfaz
if __name__ == "__main__":
    ventana = tk.Tk()
    ventana.title("BrainLingua NLP")
    crear_interfaz_texto(ventana)
    ventana.mainloop()
