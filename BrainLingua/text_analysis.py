from tkinter import Text, Button, messagebox, ttk
import tkinter as tk
from nltk.tokenize import word_tokenize
import nltk
import re
from nltk import pos_tag
from collections import Counter
from nltk.tokenize import sent_tokenize

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

palabras_malsonantes = [
    "Abuso", "Acojonar", "Afollonada", "Afollonado", "Agilipollada", "Agilipollado", "Agilipollar", "Alamierda", 
    "Amamonada", "Amamonado", "Amargada", "Amargado", "Anárquico", "Anormal", "Asesina", "Asesinar", "Asesino", 
    "Asquerosa", "Asqueroso", "Autoritaria", "Autoritario", "Autoritarismo", "Badajo", "Bastarda", "Bastardo", 
    "Basura", "Berzas", "Berzotas", "Bestia", "Boba", "Bobo", "Bollera", "Boluda", "Boludez", "Boludo", "Borracha", 
    "Borrachaza", "Borrachazo", "Borrachera", "Borracho", "Borrachuza", "Borrachuzo", "Bronca", "Bufón", "Bufona", 
    "Bujarra", "Bujarrilla", "Bujarrón", "Cabreada", "Cabreado", "Cabrear", "Cabreo", "Cabrón", "Cabrona", 
    "Cabronada", "Cabroncete", "Caca", "Cachonda", "Cachondeo", "Cachondo", "Cagada", "Cagado", "Cagar", "Cagarla", 
    "Cagarse", "Cagoen", "Cagón", "Cagona", "Calentorra", "Calentorro", "Calzonazo", "Calzonazos", "Camero", 
    "Capulla", "Capullo", "Carajo", "Carajota", "Carajote", "Carallo", "Carnudo", "Cascar", "Cascarla", "Casquete", 
    "Cateta", "Cateto", "Cazurra", "Cazurro", "Cencular", "Cenutrio", "Cepillar", "Ceporra", "Ceporro", "Chapero", 
    "Chaquetera", "Chaquetero", "Chichi", "Chingada", "Chingar", "Chivata", "Chivato", "Chocho", "Chochona", 
    "Choriza", "Chorizo", "Chorra", "Chorrada", "Chorva", "Chula", "Chulilla", "Chulillo", "Chulita", "Chulito", 
    "Chulo", "Chuloputas", "Chumino", "Chúpame", "Chúpamela", "Chupópteros", "Churra", "Churrita", "Chutarse", 
    "Chute", "Cipote", "Cipotón", "Cojón", "Cojones", "Cojonudo", "Comemierda", "Comino", "Coño", "Cornuda", 
    "Cornudo", "Correrse", "Corrida", "Corrupta", "Corrupto", "Cretina", "Cretino", "Cuerno", "Cuesco", "Culear", 
    "Culero", "Cutre", "Decapitar", "Decojones", "Degollar", "Descojonarse", "Descojone", "Descojono", 
    "Desequilibrada", "Desequilibrado", "Desgraciada", "Desgraciado", "Déspota", "Dictatorial", "Doctorcilla", 
    "Doctorcillo", "Doctorcita", "Doctorcito", "Drogata", "Embustera", "Embustero", "Encabronar", "Encubrimiento", 
    "Enganchada", "Enganchado", "Engañabobos", "Engaño", "Enmascaramiento", "Enmascarar", "Envenenar", "Escocida", 
    "Escocido", "Estafa", "Estafador", "Estafadora", "Estúpida", "Estúpido", "Facha", "Falo", "Farsante", "Folla", 
    "Follada", "Follado", "Follador", "Folladora", "Follamos", "Follando", "Follar", "Follarse", "Follo", "Follón", 
    "Follones", "Friki", "Frustrada", "Frustrado", "Fulanita", "Fulanito", "Fulano", "Furcia", "Gallorda",    "Gamberra", "Gamberro", "Gañán", "Gili", "Gilipolla", "Gilipollas", "Gilipuertas", "Gitaneo", "Granuja", 
    "Greñudo", "Guarra", "Guarrita", "Guarrito", "Guarro", "Guay", "Hijadeputa", "Hijaputa", "Hijodeputa", 
    "Hijoputa", "Hipócrita", "Hostia", "Huevo", "Huevón", "Huevona", "Idiota", "Ignorante", "Imbécil", 
    "Impresentable", "Jiñar", "Jiñarse", "Joder", "Ladrona", "Lameculo", "Litrona", "Loca", "Loco", 
    "Loquera", "Loquero", "Machacarla", "Machorra", "Mafia", "Mafiosa", "Mafioso", "Majadera", "Majadero", 
    "Malafolla", "Malfolla", "Malfollada", "Malfollado", "Malnacida", "Malnacido", "Malparida", "Malparido", 
    "Mamada", "Mámamela", "Mamarla", "Mamarracha", "Mamarracho", "Mameluco", "Mamón", "Mamona", "Mamporrero", 
    "Mangante", "Marica", "Maricón", "Maricona", "Mariconazo", "Marimacha", "Marimacho", "Mariposón", "Masacre", 
    "Matanza", "Matar", "Matasanos", "Mato", "Matón", "Mear", "Mecorro", "Medicucha", "Medicucho", "Mediquilla", 
    "Mediquillo", "Mejiño", "Melapelan", "Memeo", "Mentecata", "Mentecato", "Mentirosa", "Mentiroso", "Mierda", 
    "Minga", "Miserable", "Mocosa", "Mocoso", "Mogollón", "Mojigata", "Mojigato", "Mojino", "Mojón", "Moña", 
    "Morralla", "Mugra", "Mugriente", "Mugrosa", "Mugroso", "Nabo", "Nalgas", "Negligencia", "Negligente", 
    "Negrata", "Negrera", "Negrero", "Opresor", "Opresora", "Paja", "Pajera", "Pajero", "Pajillera", "Pajillero", 
    "Palurda", "Palurdo", "Pamplina", "Panoli", "Papanatas", "Pasota", "Payasa", "Payaso", "Pécora", "Pedo", 
    "Pedorra", "Pedorro", "Pelandrusca", "Pelandrusco", "Pendeja", "Pendejo", "Peo", "Perras", "Perversa", 
    "Perverso", "Pesetera", "Pesetero", "Peta", "Petarda", "Petardo", "Picha", "Pichafloja", "Pija", "Pijar", 
    "Pijo", "Pijotera", "Pijotero", "Pilila", "Pinga", "Piojosa", "Piojoso", "Pipote", "Pirada", "Pirado", "Polla", 
    "Pollada", "Pollón", "Porcojones", "Porculo", "Porelculo", "Porrera", "Porrero", "Porro", "Pringada", 
    "Pringado", "Proxeneta", "Puerca", "Puerco", "Puñeta", "Puñetera", "Puñetero", "Puta", "Putada", "Putero", 
    "Putilla", "Putillo", "Putita", "Putito", "Puto", "Putón", "Putona", "Queosjodan", "Querella", "Rabo", 
    "Ramera", "Ramero", "Ratera", "Ratero", "Reinona", "Reputa", "Roña", "Roñosa", "Roñoso", "Sabandija", 
    "Sangráis", "Sangrantes", "Sarasa", "Sarna", "Sarnosa", "Sarnoso", "Sinvergüenza", "Soplaflautas", 
    "Soplapollas", "Subidón", "Subnormal", "Sudaca", "Tarada", "Tarado", "Taruga", "Tarugo", "Teta", "Tete", 
    "Tocacojones", "Tocapelotas", "Tonta", "Tonto", "Torpe", "Tortillera", "Toto", "Tragapollas", "Zangano", 
    "Zopenca", "Zopenco", "Zorra", "Tragasables", "Trapicheo", "Truño", "Tusmuertos", "Usurera", "Usurero", 
    "Vividor", "Vividora", "Yoya", "Zangana", "Zorrilla", "Zorro", "Zorrón", "Zorrona", "Zurullo"
]



caja_texto = None  # Define caja_texto como una variable global y asigna None

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
                           "Puntuación", "Números", "Interjecciones", "Conjunciones subordinadas"]

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
    valores_atributos = {
        "Número de palabras": conteo_palabras,
        "Número de frases": conteo_oraciones,  
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
        "Palabras malsonantes": len(palabras_malsonantes_detectadas)
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


def limpiar_tabla():
    for item in tabla.get_children():
        tabla.delete(item)

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
    tabla.column("Atributo", anchor=tk.W, width=500)
    tabla.column("Valor", anchor=tk.CENTER, width=200)  # Alineación al centro
    tabla.heading("Atributo", text="Atributo")
    tabla.heading("Valor", text="Valor")
    tabla.pack()

    # Insertar atributos predefinidos en la tabla
    for atributo in atributos_predefinidos:
        tabla.insert("", "end", values=(atributo, ""))


# Llamada a la función para crear la interfaz
if __name__ == "__main__":
    ventana = tk.Tk()
    ventana.title("BrainLingua NLP")
    crear_interfaz_texto(ventana)
    ventana.mainloop()
