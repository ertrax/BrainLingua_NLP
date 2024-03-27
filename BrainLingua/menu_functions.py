from tkinter import messagebox, filedialog, Menu
from text_analysis import contar_palabras_texto, limpiar_tabla, analizar_texto, caja_texto, tabla

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

def salir(ventana):
    respuesta = messagebox.askyesno("Salir", "¿Desea salir de la aplicación?")
    if respuesta:
        ventana.quit()
        ventana.destroy()

def acerca_de():
    messagebox.showinfo("Acerca de", "Aplicación desarrollada por: \n\n"
                                    "Pablo Fernández Planas\n"
    )

def limpiar_busqueda():
    limpiar_tabla()

def configurar_menu(ventana):
    barra_menu = Menu(ventana)
    ventana.config(menu=barra_menu)

    # Menú Archivo
    menu_archivo = Menu(barra_menu, tearoff=0)
    barra_menu.add_cascade(label="Archivo", menu=menu_archivo)
    menu_archivo.add_command(label="Importar Documento", command=importar_documento)
    menu_archivo.add_separator()
    menu_archivo.add_command(label="Salir", command=lambda: salir(ventana))

    # Menú Opciones
    menu_opciones = Menu(barra_menu, tearoff=0)
    barra_menu.add_cascade(label="Opciones", menu=menu_opciones)
    menu_opciones.add_command(label="Acerca de", command=acerca_de)

    # Menú Diccionarios
    menu_diccionarios = Menu(barra_menu, tearoff=0)
    barra_menu.add_cascade(label="Diccionarios", menu=menu_diccionarios)
    menu_diccionarios.add_command(label="Importar Diccionario", command=importar_documento)

    # Menú Ayuda
    menu_ayuda = Menu(barra_menu, tearoff=0)
    barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)
    menu_ayuda.add_command(label="Acerca de", command=acerca_de)
    
