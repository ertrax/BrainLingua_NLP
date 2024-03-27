import tkinter as tk
from tkinter import ttk
from menu_functions import configurar_menu
from text_analysis import caja_texto, boton_analizar, boton_limpiar_busqueda, tabla
from styles import configurar_estilos

def main():
    ventana = tk.Tk()
    ventana.title("BrainLingua NLP")

    # Configuración de la ventana y la barra de menú
    configurar_estilos()
    configurar_menu(ventana)

    # Obtener las dimensiones de la pantalla
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()

    # Configurar el tamaño de la ventana al tamaño máximo de la pantalla
    ventana.geometry(f"{ancho_pantalla}x{alto_pantalla}")

    ventana.mainloop()

if __name__ == "__main__":
    main()
