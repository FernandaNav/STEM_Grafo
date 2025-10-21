import customtkinter as ctk
from tkinter import messagebox

class FormularioManager:
    def __init__(self, grafo, area):
        self.grafo = grafo
        self.area = area
        self.vars = []

    def abrir_form(self):
        preguntas_dict = {
            "Programación": ["¿Sabes programar?","¿Sabes inglés?","¿Tienes experiencia en bases de datos?",
                             "¿Te interesa desarrollo web?","¿Te interesa inteligencia artificial?"],
            "Ciencia": ["¿Te interesa Biología?","¿Te interesa Química?","¿Tienes recursos para laboratorios?",
                        "¿Te interesa investigación avanzada?","¿Quieres hacer innovación científica?"],
            "Ingeniería": ["¿Te gusta construir cosas?","¿Te interesa Robótica?","¿Te interesa Electrónica?",
                           "¿Tienes habilidades matemáticas?","¿Quieres hacer innovación tecnológica?"]
        }
        top = ctk.CTkToplevel(self.grafo.master)
        top.title(f"Decisiones: {self.area}")
        top.geometry("400x350")
        top.attributes('-topmost', True)
        ctk.CTkLabel(top,text=f"Decisiones para {self.area}",font=("Arial",16,"bold")).pack(pady=10)

        self.vars=[]
        for p in preguntas_dict[self.area]:
            var=ctk.StringVar(value="No")
            self.vars.append(var)
            frame=ctk.CTkFrame(top)
            frame.pack(fill="x", padx=20, pady=5)
            ctk.CTkLabel(frame,text=p).pack(side="left", padx=5)
            ctk.CTkRadioButton(frame,text="Sí",variable=var,value="Sí").pack(side="left", padx=5)
            ctk.CTkRadioButton(frame,text="No",variable=var,value="No").pack(side="left", padx=5)

        ctk.CTkButton(top,text="Confirmar",command=lambda:self.confirmar(top)).pack(pady=10)

    def confirmar(self,top):
        if self.area=="Programación":
            self.grafo.decidir_programacion(self.vars)
        elif self.area=="Ciencia":
            self.grafo.decidir_ciencia(self.vars)
        else:
            self.grafo.decidir_ingenieria(self.vars)
        top.destroy()
