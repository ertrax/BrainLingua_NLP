import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from nltk.tokenize import word_tokenize
import nltk
import re
from nltk import pos_tag
from collections import Counter
import spanlp 

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Diccionario de mapeo de etiquetas gramaticales
mapeo_etiquetas_espanol_ingles = {
    'Sustantivo': 'NN',
    'Sustantivo propio': 'NNP',
    'Conjunción de coordinación': 'CC',
    'Preposición': 'IN',
    'Adjetivo': 'JJ'
}

def contar_palabras_texto(texto):
    # Tokeniza el texto y filtra los tokens para eliminar los signos de puntuación
    tokens = [token for token in word_tokenize(texto) if re.match(r'^\w+$', token)]
    num_palabras = len(tokens)  # Cuenta el número de palabras
    return num_palabras

def etiquetar_gramaticalmente_texto(mensaje):
    # Tokeniza el mensaje
    tokens = word_tokenize(mensaje)

    # Filtra los tokens eliminando los signos de puntuación
    tokens_sin_puntuacion = [token for token in tokens if re.match(r'^\w+$', token)]

    # Realiza el etiquetado gramatical (POS tagging)
    tagged_tokens = pos_tag(tokens_sin_puntuacion)

    # Traduce las etiquetas gramaticales al inglés
    tagged_tokens_ingles = [(word, mapeo_etiquetas_espanol_ingles.get(tag, tag)) for word, tag in tagged_tokens]

    # Cuenta la frecuencia de cada etiqueta
    conteo_etiquetas = Counter(tag for word, tag in tagged_tokens_ingles)

    return conteo_etiquetas

def analizar_texto():
    texto = caja_texto.get("1.0", "end-1c")  # Obtener el texto de la caja de texto
    conteo_palabras = contar_palabras_texto(texto)
    etiquetas_gramaticales = etiquetar_gramaticalmente_texto(texto)
    
    # Limpiar la tabla antes de agregar nuevos datos
    limpiar_tabla()
    
    # Insertar datos en la tabla
    tabla.insert("", "end", values=("Número de palabras", conteo_palabras))
    for etiqueta, frecuencia in etiquetas_gramaticales.items():
        tabla.insert("", "end", values=(etiqueta, frecuencia))

def limpiar_tabla():
    # Eliminar todos los elementos de la tabla
    for item in tabla.get_children():
        tabla.delete(item)

def importar_documento():
    ruta_archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    if ruta_archivo:
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                contenido = archivo.read()
            num_palabras = contar_palabras_texto(contenido)
            messagebox.showinfo("Conteo de Palabras", f"El documento tiene {num_palabras} palabras.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{str(e)}")

def salir():
    respuesta = messagebox.askyesno("Salir", "¿Desea salir de la aplicación?")
    if respuesta:
        ventana.quit()
        ventana.destroy()

def acerca_de():
    messagebox.showinfo("Acerca de", "Aplicación desarrollada por: \n\n"
                                    "Pablo Fernández Planas\n"
    )

ventana = tk.Tk()
ventana.title("BrainLingua NLP")

# Obtener las dimensiones de la pantalla
ancho_pantalla = ventana.winfo_screenwidth()
alto_pantalla = ventana.winfo_screenheight()

# Configurar el tamaño de la ventana al tamaño máximo de la pantalla
ventana.geometry(f"{ancho_pantalla}x{alto_pantalla}")

barra_menu = tk.Menu(ventana)
ventana.config(menu=barra_menu)

# Menú Archivo
menu_archivo = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Archivo", menu=menu_archivo)
menu_archivo.add_command(label="Salir", command=salir)
menu_archivo.add_command(label="Importar Documento", command=importar_documento)

# Menu Opciones
menu_opciones = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Opciones", menu=menu_opciones)
menu_opciones.add_command(label="Acerca de", command=acerca_de)

# Menu Diccionarios
menu_diccionarios = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Diccionarios", menu=menu_diccionarios)
menu_diccionarios.add_command(label="Importar Diccionario", command=importar_documento)

# Menu Ayuda
menu_ayuda = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)
menu_ayuda.add_command(label="Acerca de", command=acerca_de)

# Caja de texto
caja_texto = tk.Text(ventana, height=10, width=50)
caja_texto.pack()

# Botón para analizar texto
boton_analizar = tk.Button(ventana, text="Analizar Texto", command=analizar_texto)
boton_analizar.pack()

# Botón para limpiar la búsqueda
boton_limpiar_busqueda = tk.Button(ventana, text="Limpiar Búsqueda", command=limpiar_tabla)
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

# Estilo de la ventana
ventana.configure(bg="#f0f0f0")  # Color de fondo
ventana.option_add('*Font', 'Helvetica 10')  # Fuente y tamaño de letra predeterminados
ventana.option_add('*Button.relief', 'raised')  # Agrega relieve a los botones
ventana.option_add('*Button.activebackground', '#d9d9d9')  # Color de fondo al presionar un botón
ventana.option_add('*Button.highlightbackground', '#f0f0f0')  # Color de fondo del resaltado del botón

# Estilo de la tabla
style = ttk.Style()
style.theme_use('clam')  # Utiliza el tema 'clam' para ttk widgets
style.configure('Treeview', background='#ffffff', fieldbackground='#ffffff', foreground='#000000', font=('Helvetica', 10))  # Estilo de fondo y fuente de la tabla
style.map('Treeview', background=[('selected', '#0078d7')])  # Color de fondo de las filas seleccionadas en la tabla

# Otros estilos específicos según la necesidad, por ejemplo, para centrar el contenido de las celdas de la tabla
style.configure('Treeview.Heading', font=('Helvetica', 10, 'bold'))  # Estilo del encabezado de la tabla
style.configure('Treeview', rowheight=25)  # Altura de fila

ventana.mainloop()
