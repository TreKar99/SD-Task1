from tkinter import *


class InputBox():
    ventana = Tk()
    entrada = Entry(width=30)
    texto = ""

    def input(self):
        self.ventana.geometry("300x200")

        # Crear una etiqueta
        etiqueta = Label(text="Introduce un texto:", font=("Arial", 12))
        etiqueta.pack()

        # Crear una caja de entrada de texto
        self.entrada.pack()

        # Crear un botón
        boton = Button(text="Guardar", command=self.guardar_texto)
        boton.pack()

        self.ventana.mainloop()
        return self.texto

    def guardar_texto(self):
        self.texto = self.entrada.get()
        self.ventana.destroy()

    def kill(self):
        self.ventana.destroy()
