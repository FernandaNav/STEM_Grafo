import customtkinter as ctk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time
from tkinter import filedialog
from tkinter import messagebox

class GrafoLogic:
    def __init__(self, master):
        self.master = master
        self.G = nx.DiGraph()
        self.crear_grafo()

        self.fig, self.ax = plt.subplots(figsize=(8,6))
        self.ax.set_title("Mapa de decisiones STEM", color="white", fontsize=16)
        self.fig.patch.set_facecolor('#1a1a1a')
        self.ax.set_facecolor('#1a1a1a')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.pos = {
            "Inicio": (0,0),
            "Programación": (-1,-1), "Python": (-2,-2), "C#": (-2,-1),
            "Web": (-3,-2), "IA": (-3,-1), "Desarrollador Web": (-4,-2),
            "Desarrollador Software": (-4,-1),
            "Ciencia": (0,-1), "Biología": (0,-2), "Química": (1,-2),
            "Investigador": (0,-3), "Analista Laboratorio": (1,-3),
            "Ingeniería": (1,-1), "Mecánica": (2,-2), "Electrónica": (2,-1),
            "Ingeniero Mecánico": (2,-3), "Ingeniero Robótica": (3,-2),
            "Innovador Robótica": (4,-2), "Innovador Mecánico": (3,-3)
        }

        self.colores = ["#3498db" for _ in self.G.nodes()]
        self.dibujar_grafo()

    # ------------------- GRAFO -------------------
    def crear_grafo(self):
        aristas = [
            ("Inicio","Programación"),("Programación","Python"),("Programación","C#"),
            ("Python","Web"),("Python","IA"),("C#","Web"),("C#","IA"),
            ("Web","Desarrollador Web"),("IA","Desarrollador Software"),
            ("Inicio","Ciencia"),("Ciencia","Biología"),("Ciencia","Química"),
            ("Biología","Investigador"),("Química","Analista Laboratorio"),
            ("Inicio","Ingeniería"),("Ingeniería","Mecánica"),("Ingeniería","Electrónica"),
            ("Mecánica","Ingeniero Mecánico"),("Electrónica","Ingeniero Robótica"),
            ("Ingeniero Robótica","Innovador Robótica"),
            ("Ingeniero Mecánico","Innovador Mecánico")
        ]
        for u,v in aristas:
            self.G.add_edge(u,v,weight=1)

    def dibujar_grafo(self,ruta=None):
        self.ax.clear()
        sizes = [800 + len(n)*80 for n in self.G.nodes()]
        nx.draw(
            self.G, self.pos, with_labels=True, labels={n:n for n in self.G.nodes()},
            node_color=self.colores, node_size=sizes,
            font_size=10, font_weight="bold", font_color="white",
            edge_color="gray", arrows=True, ax=self.ax
        )
        # Pesos coloreados y tamaño según dificultad
        for u,v,d in self.G.edges(data=True):
            peso = d['weight']
            if peso <=2:
                color="green"
                fontsize=8
            elif peso <=5:
                color="yellow"
                fontsize=12
            else:
                color="red"
                fontsize=16
            nx.draw_networkx_edge_labels(self.G,self.pos,edge_labels={(u,v):peso},
                                         font_color=color, font_size=fontsize, ax=self.ax)
        if ruta:
            path_edges = list(zip(ruta,ruta[1:]))
            nx.draw_networkx_edges(self.G,self.pos,edgelist=path_edges,edge_color="red",width=3,ax=self.ax)
        self.canvas.draw()

    def reiniciar_grafo(self):
        self.colores = ["#3498db" for _ in self.G.nodes()]
        for u,v in self.G.edges():
            self.G[u][v]['weight']=1
        self.dibujar_grafo()

    # ------------------- DECISIONES -------------------
    def decidir_programacion(self,vars):
        ruta=["Inicio","Programación"]
        pesos = {}
        if vars[0].get()=="Sí":
            ruta.append("Python")
            pesos["Python->Web"]=2 if vars[3].get()=="Sí" else 10
            pesos["Python->IA"]=3 if vars[4].get()=="Sí" else 10
        else:
            ruta.append("C#")
            pesos["C#->Web"]=2 if vars[3].get()=="Sí" else 10
            pesos["C#->IA"]=3 if vars[4].get()=="Sí" else 10
        for key,value in pesos.items():
            u,v=key.split("->")
            self.G[u][v]['weight']=value
        destino = "Desarrollador Web" if pesos.get(f"{ruta[-1]}->Web",0)<10 else "Desarrollador Software"
        camino = nx.dijkstra_path(self.G,"Inicio",destino,weight='weight')
        self.animar_ruta(camino)

    def decidir_ciencia(self,vars):
        ruta=["Inicio","Ciencia"]
        pesos={}
        if vars[0].get()=="Sí":
            ruta.append("Biología")
            pesos["Biología->Investigador"]=5 if vars[3].get()=="Sí" else 6
        elif vars[1].get()=="Sí":
            ruta.append("Química")
            pesos["Química->Analista Laboratorio"]=4 if vars[3].get()=="Sí" else 5
        else:
            ruta.append("Biología")
        for key,value in pesos.items():
            u,v = key.split("->")
            self.G[u][v]['weight']=value
        destino = "Investigador" if ruta[-1]=="Biología" else "Analista Laboratorio"
        camino = nx.dijkstra_path(self.G,"Inicio",destino,weight='weight')
        self.animar_ruta(camino)

    def decidir_ingenieria(self,vars):
        ruta=["Inicio","Ingeniería"]
        pesos={}
        if vars[0].get()=="Sí":
            ruta.append("Mecánica")
            pesos["Mecánica->Ingeniero Mecánico"]=3
        else:
            ruta.append("Electrónica")
            pesos["Electrónica->Ingeniero Robótica"]=4
        for key,value in pesos.items():
            u,v=key.split("->")
            self.G[u][v]['weight']=value
        destino = "Ingeniero Mecánico" if ruta[-1]=="Mecánica" else "Ingeniero Robótica"
        camino = nx.dijkstra_path(self.G,"Inicio",destino,weight='weight')
        self.animar_ruta(camino)

    # ------------------- ANIMACIÓN -------------------
    def animar_ruta(self,camino):
        def run_animation():
            self.colores = ["#3498db" for _ in self.G.nodes()]
            for nodo in camino:
                idx = list(self.G.nodes()).index(nodo)
                self.colores[idx] = "#e74c3c"
                self.dibujar_grafo()
                time.sleep(0.5)
        threading.Thread(target=run_animation).start()

    # ------------------- EXPORTAR PDF -------------------
    def exportar_pdf(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files","*.pdf")])
        if file_path:
            self.fig.savefig(file_path, facecolor=self.fig.get_facecolor())
            messagebox.showinfo("Exportar PDF", f"Grafo exportado como {file_path}")
