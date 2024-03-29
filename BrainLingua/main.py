import tkinter as tk
from tkinter import ttk
from menu_functions import configurar_menu
from text_analysis import crear_interfaz_texto
from styles import configurar_estilos

def main():
    ventana = tk.Tk()
    ventana.title("BrainLingua NLP")
    ventana.iconbitmap("img/brain.ico")

    # Configuración de la ventana y la barra de menú
    configurar_estilos()
    configurar_menu(ventana)

    # Obtener las dimensiones de la pantalla
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()

    # Configurar el tamaño de la ventana al tamaño máximo de la pantalla
    ventana.geometry(f"{ancho_pantalla}x{alto_pantalla}")

    # Crear la interfaz de análisis de texto
    crear_interfaz_texto(ventana)

    ventana.mainloop()

if __name__ == "__main__":
    main()
