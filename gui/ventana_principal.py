import customtkinter as ctk
from grafo.grafo_logic import GrafoLogic
from gui.formularios import FormularioManager

class GrafoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Rutas STEM")
        self.geometry("1000x750")
        self.minsize(900,650)

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.label = ctk.CTkLabel(self.frame, text="Sistema de Rutas STEM",
                                  font=("Arial",22,"bold"), text_color="#00bfff")
        self.label.pack(pady=10)

        # Instanciamos la lógica del grafo
        self.grafo = GrafoLogic(self.frame)

        # Botones
        boton_frame = ctk.CTkFrame(self.frame)
        boton_frame.pack(pady=10)
        ctk.CTkButton(boton_frame, text="Programación", 
                      command=lambda: FormularioManager(self.grafo,"Programación").abrir_form(),
                      fg_color="#1e90ff").pack(side="left", padx=10)
        ctk.CTkButton(boton_frame, text="Ciencia", 
                      command=lambda: FormularioManager(self.grafo,"Ciencia").abrir_form(),
                      fg_color="#32cd32").pack(side="left", padx=10)
        ctk.CTkButton(boton_frame, text="Ingeniería", 
                      command=lambda: FormularioManager(self.grafo,"Ingeniería").abrir_form(),
                      fg_color="#ffa500").pack(side="left", padx=10)
        ctk.CTkButton(boton_frame, text="Reiniciar", command=self.grafo.reiniciar_grafo,
                      fg_color="#e74c3c").pack(side="left", padx=10)
        ctk.CTkButton(boton_frame, text="Exportar PDF", command=self.grafo.exportar_pdf,
                      fg_color="#8e44ad").pack(side="left", padx=10)
