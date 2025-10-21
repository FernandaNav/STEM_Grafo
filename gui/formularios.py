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
        # Ventana premium para formularios
        top = ctk.CTkToplevel(self.grafo.master)
        top.title(f"Evaluacion de {self.area}")
        top.geometry("500x450")
        top.attributes('-topmost', True)
        top.configure(fg_color="#0D1117")
        
        # Header del formulario
        header = ctk.CTkFrame(top, fg_color="#161B22", corner_radius=12)
        header.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(header,
                    text=f"EVALUACION DE {self.area.upper()}",
                    font=("Segoe UI", 18, "bold"),
                    text_color="#58A6FF").pack(pady=15)
        
        ctk.CTkLabel(header,
                    text="Responde las siguientes preguntas para obtener tu ruta personalizada",
                    font=("Segoe UI", 12),
                    text_color="#7D8590").pack(pady=(0, 15))

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
