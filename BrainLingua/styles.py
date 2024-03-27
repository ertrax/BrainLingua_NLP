from tkinter import ttk

def configurar_estilos():
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('Treeview', background='#ffffff', fieldbackground='#ffffff', foreground='#000000', font=('Helvetica', 10))
    style.map('Treeview', background=[('selected', '#0078d7')])
    style.configure('Treeview.Heading', font=('Helvetica', 10, 'bold'))
    style.configure('Treeview', rowheight=25)
