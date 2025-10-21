import customtkinter as ctk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import threading
import time
from tkinter import filedialog
from tkinter import messagebox

# Configurar matplotlib correctamente para tkinter
plt.style.use('dark_background')
plt.rcParams['figure.facecolor'] = '#1a1a1a'
plt.rcParams['axes.facecolor'] = '#1a1a1a'
plt.rcParams['text.color'] = 'white'
plt.rcParams['axes.labelcolor'] = 'white'
plt.rcParams['xtick.color'] = 'white'
plt.rcParams['ytick.color'] = 'white'

class GrafoLogic:
    def __init__(self, master):

        self.master = master
        self.G = nx.DiGraph()
        self.crear_grafo()
        
        # Frame contenedor premium para el grafo (más pequeño)
        self.graph_frame = ctk.CTkFrame(master, fg_color="#0D1117", corner_radius=12,
                                       border_width=2, border_color="#30363D", height=450)
        self.graph_frame.pack(fill="x", expand=False, padx=15, pady=(5, 10))
        self.graph_frame.pack_propagate(False)

        # Figura premium con colores modernos
        self.fig = Figure(figsize=(8, 5), dpi=90, facecolor='#0D1117')  # Más pequeño para dejar espacio
        self.ax = self.fig.add_subplot(111, facecolor='#0D1117')
        
        # Configurar el subplot correctamente
        self.ax.set_aspect('equal', adjustable='box')
        self.ax.axis('off')  # Quitar ejes para mejor apariencia
        
        # Configurar el layout de matplotlib
        self.fig.tight_layout(pad=0.5)
        
        # Crear canvas y agregarlo al frame
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.draw()
        
        # Empaquetar el widget de canvas
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Definir posiciones de los nodos para el layout
        self.pos = {
            "Inicio": (0, 0),
            
            # Rama Programación (izquierda) - Mayor separación horizontal
            "Programación": (-3, -0.8),
            "Python": (-5.5, -1.8), 
            "C#": (-5.5, 0.2),
            "Web": (-8, -1.8), 
            "IA": (-8, 0.2),
            "Desarrollador Web": (-10.5, -1.8),
            "Desarrollador Software": (-10.5, 0.2),
            
            # Rama Ciencia (centro-abajo) - Expandida
            "Ciencia": (0, -1.5),
            "Biología": (-1.5, -3), 
            "Química": (1.5, -3),
            "Investigador": (-1.5, -4.5),
            "Analista Laboratorio": (1.5, -4.5),
            
            # Rama Ingeniería (derecha) - Mayor separación horizontal
            "Ingeniería": (3, -0.8),
            "Mecánica": (5.5, -1.8), 
            "Electrónica": (5.5, 0.2),
            "Ing Mecánico": (5.5, -3.5),
            "Ing Robótica": (8, -1.8),
            "Innovador Robótica": (10.5, -1.8),
            "Innovador Mecánico": (8, -3.5)
        }
        
        # Dibujar grafo inicial
        self.dibujar_grafo()

        # Posiciones optimizadas usando algoritmo de NetworkX
        # Usar spring_layout como base y ajustar manualmente
        base_pos = nx.spring_layout(self.G, k=3, iterations=50, seed=42)
        
        # Definir posiciones manually para mejor control visual
        self.pos = {
            "Inicio": (0, 0),
            
            # Rama Programación (izquierda) - Mayor separación horizontal
            "Programación": (-3, -0.5),
            "Python": (-5.5, -1.5), 
            "C#": (-5.5, 0.5),
            "Web": (-8, -1.5), 
            "IA": (-8, 0.5),
            "Desarrollador Web": (-10.5, -1.5),
            "Desarrollador Software": (-10.5, 0.5),
            
            # Rama Ciencia (centro-abajo) - Expandida
            "Ciencia": (0, -2),
            "Biología": (-1.5, -3.5), 
            "Química": (1.5, -3.5),
            "Investigador": (-1.5, -5),
            "Analista Laboratorio": (1.5, -5),
            
            # Rama Ingeniería (derecha) - Mayor separación horizontal
            "Ingeniería": (3, -0.5),
            "Mecánica": (5.5, -1.5), 
            "Electrónica": (5.5, 0.5),
            "Ing Mecánico": (5.5, -3.5),
            "Ing Robótica": (8, -1.5),
            "Innovador Robótica": (10.5, -1.5),
            "Innovador Mecánico": (8, -3.5)
        }

        # Ya no necesitamos self.colores, usamos colores fijos
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
            ("Mecánica","Ing Mecánico"),("Electrónica","Ing Robótica"),
            ("Ing Robótica","Innovador Robótica"),
            ("Ing Mecánico","Innovador Mecánico")
        ]
        for u,v in aristas:
            self.G.add_edge(u,v,weight=1)

    def dibujar_grafo(self, ruta=None, pulse_node=None, pulse_intensity=0):
        # Limpiar y configurar fondo premium
        self.ax.clear()
        
        # Crear gradiente de fondo para mayor profundidad visual
        import numpy as np
        x = np.linspace(-12, 12, 100)
        y = np.linspace(-6, 2, 100)
        X, Y = np.meshgrid(x, y)
        Z = np.sqrt(X**2 + Y**2)
        
        # Aplicar gradiente radial sutil
        self.ax.contourf(X, Y, Z, levels=20, alpha=0.1, cmap='Blues_r')
        
        self.ax.set_facecolor('#0D1117')  # Fondo GitHub dark
        self.ax.axis('off')
        
        # Título premium con estilo moderno
        self.fig.suptitle('MAPA INTERACTIVO DE CARRERAS STEM', 
                         fontsize=18, fontweight='bold',  # Aumentado de 16 a 18 para mejor legibilidad
                         color='#FFFFFF', y=0.95,  # Blanco puro y posición más alta
                         fontfamily='Segoe UI')
        
        # Nodos con tamaño optimizado para legibilidad
        node_sizes = {}
        for node in self.G.nodes():
            # Tamaños ligeramente más grandes para mejor legibilidad
            base_size = 2500  # Aumentado de 2000 a 2500 para mejor legibilidad
            text_length_factor = len(node) * 100  # Aumentado de 80 a 100
            
            # Factores de importancia jerárquica optimizados
            if node == "Inicio":
                hierarchy_factor = 1.6  # Más prominente
            elif node in ["Programación", "Ciencia", "Ingeniería"]:
                hierarchy_factor = 1.4  # Más visibles
            elif "Desarrollador" in node or "Ing" in node or "Analista" in node or "Investigador" in node:
                hierarchy_factor = 1.5  # Carreras más destacadas
            else:  # Pasos intermedios
                hierarchy_factor = 1.3  # Mejor balance
                
            node_sizes[node] = int(base_size + text_length_factor * hierarchy_factor)
        
        # Esquema de colores premium moderno
        node_colors = {}
        color_scheme = {
            # Inicio - Verde GitHub premium
            "Inicio": "#3FB950",
            
            # Programación - Azul GitHub premium  
            "Programación": "#58A6FF", "Python": "#58A6FF", "C#": "#58A6FF", 
            "Web": "#58A6FF", "IA": "#58A6FF",
            "Desarrollador Web": "#58A6FF", "Desarrollador Software": "#58A6FF",
            
            # Ciencia - Naranja GitHub premium
            "Ciencia": "#F78166", "Biología": "#F78166", "Química": "#F78166",
            "Investigador": "#F78166", "Analista Laboratorio": "#F78166",
            
            # Ingeniería - Púrpura GitHub premium
            "Ingeniería": "#A5A5FF", "Mecánica": "#A5A5FF", "Electrónica": "#A5A5FF",
            "Ing Mecánico": "#A5A5FF", "Ing Robótica": "#A5A5FF",
            "Innovador Robótica": "#A5A5FF", "Innovador Mecánico": "#A5A5FF"
        }
        
        # Crear listas para networkx con efectos especiales
        sizes = [node_sizes.get(node, 2000) for node in self.G.nodes()]
        colors = [color_scheme.get(node, '#607D8B') for node in self.G.nodes()]
        
        # Aplicar efecto de pulso si hay nodo seleccionado
        if pulse_node and pulse_node in self.G.nodes():
            node_idx = list(self.G.nodes()).index(pulse_node)
            pulse_multiplier = 1 + (pulse_intensity * 0.3)  # Hasta 30% más grande
            sizes[node_idx] = int(sizes[node_idx] * pulse_multiplier)
            # Cambiar color durante el pulso
            colors[node_idx] = '#FFD700'  # Dorado para destacar
        
        # Dibujar sombras de nodos primero (efecto de profundidad)
        nx.draw_networkx_nodes(
            self.G, self.pos,
            node_color='#000000',  # Sombra negra
            node_size=[s * 1.05 for s in sizes],  # Ligeramente más grande
            alpha=0.3,  # Transparente para efecto sombra
            ax=self.ax
        )
        
        # Dibujar el grafo principal con configuración profesional
        nx.draw_networkx_nodes(
            self.G, self.pos,
            node_color=colors,
            node_size=sizes,
            alpha=0.95,  # Más opaco para mejor contraste
            edgecolors='#FFFFFF',  # Borde blanco
            linewidths=2,  # Grosor de borde
            ax=self.ax
        )
        
        # Dibujar sombras de aristas primero
        nx.draw_networkx_edges(
            self.G, self.pos,
            edge_color='#000000',  # Sombra negra
            arrows=True,
            arrowsize=32,
            arrowstyle='-|>',
            width=4,
            alpha=0.2,  # Transparente para sombra
            ax=self.ax
        )
        
        # Aristas principales con diseño premium moderno
        nx.draw_networkx_edges(
            self.G, self.pos,
            edge_color='#58A6FF',  # Azul GitHub premium
            arrows=True,
            arrowsize=30,
            arrowstyle='-|>',  # Estilo más elegante
            width=3.5,
            alpha=0.9,
            ax=self.ax
        )
        
        # Etiquetas principales con tipografía moderna (sin sombras)
        nx.draw_networkx_labels(
            self.G, self.pos,
            font_size=14,  # Aumentado de 12 a 14 para mejor legibilidad
            font_weight='bold',  # Negrita para mayor impacto visual
            font_color='#FFFFFF',  # Blanco puro para máximo contraste
            font_family='Segoe UI',  # Fuente moderna
            ax=self.ax
        )
        # Dibujar pesos de aristas con mejor visualización
        edge_labels = {}
        for u, v, d in self.G.edges(data=True):
            peso = d['weight']
            edge_labels[(u, v)] = peso
            
        # Configurar colores de pesos según dificultad
        edge_colors = {}
        for (u, v), peso in edge_labels.items():
            if peso <= 2:
                edge_colors[(u, v)] = '#4CAF50'  # Verde
            elif peso <= 5:
                edge_colors[(u, v)] = '#FF9800'  # Naranja
            else:
                edge_colors[(u, v)] = '#F44336'  # Rojo
                
        # Dibujar etiquetas de aristas con mejor visibilidad
        for (u, v), label in edge_labels.items():
            x = (self.pos[u][0] + self.pos[v][0]) / 2
            y = (self.pos[u][1] + self.pos[v][1]) / 2
            self.ax.text(x, y, str(label), 
                        fontsize=10, fontweight='bold',  # Aumentado de 8 a 10 para mejor legibilidad
                        color='#FFFFFF',  # Blanco puro para máximo contraste
                        ha='center', va='center',
                        bbox=dict(boxstyle='round,pad=0.3',  # Más padding para mejor legibilidad
                                facecolor='#000000', alpha=0.8))  # Fondo más opaco
        
        # Resaltar ruta si existe
        if ruta and len(ruta) > 1:
            ruta_edges = [(ruta[i], ruta[i+1]) for i in range(len(ruta)-1)]
            nx.draw_networkx_edges(
                self.G, self.pos,
                edgelist=ruta_edges,
                edge_color='#00E676',
                width=4,
                alpha=0.9,
                ax=self.ax
            )
            
            # Resaltar nodos de la ruta
            ruta_nodes = ruta
            ruta_node_colors = ['#00E676' if node in ruta_nodes else color 
                               for node, color in zip(self.G.nodes(), colors)]
            
            nx.draw_networkx_nodes(
                self.G, self.pos,
                nodelist=ruta_nodes,
                node_color='#00E676',
                node_size=[sizes[list(self.G.nodes()).index(node)] * 1.2 
                          for node in ruta_nodes],
                alpha=0.8,
                ax=self.ax
            )
        
        # Configurar límites del gráfico con mejor padding para pantalla completa
        x_values = [pos[0] for pos in self.pos.values()]
        y_values = [pos[1] for pos in self.pos.values()]
        x_margin = (max(x_values) - min(x_values)) * 0.15  # Más margen para mejor visualización
        y_margin = (max(y_values) - min(y_values)) * 0.15
        
        self.ax.set_xlim(min(x_values) - x_margin, max(x_values) + x_margin)
        self.ax.set_ylim(min(y_values) - y_margin, max(y_values) + y_margin)
        
        # Actualizar canvas
        self.canvas.draw()
        self.canvas.flush_events()

    def reiniciar_grafo(self):
        # Reiniciar pesos y redibujar
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
            pesos["Mecánica->Ing Mecánico"]=3
        else:
            ruta.append("Electrónica")
            pesos["Electrónica->Ing Robótica"]=4
        for key,value in pesos.items():
            u,v=key.split("->")
            self.G[u][v]['weight']=value
        destino = "Ing Mecánico" if ruta[-1]=="Mecánica" else "Ing Robótica"
        camino = nx.dijkstra_path(self.G,"Inicio",destino,weight='weight')
        self.animar_ruta(camino)

    # ------------------- ANIMACIÓN -------------------
    def animar_ruta(self, camino):
        def run_animation():
            # Animación ultra fluida con efectos suaves
            for i in range(len(camino)):
                ruta_parcial = camino[:i+1]
                
                # Efecto de pulso más suave y fluido
                if i < len(camino):
                    current_node = camino[i]
                    # Pulso más fluido con más frames
                    for pulse in range(6):  # Más frames para mayor fluidez
                        intensity = (pulse / 6) * 0.8  # Pulso más sutil
                        self.dibujar_grafo(ruta_parcial, pulse_node=current_node, pulse_intensity=intensity)
                        self.canvas.draw()  # Forzar actualización
                        time.sleep(0.08)  # Animación más rápida y fluida
                
                # Dibujar estado final del paso
                self.dibujar_grafo(ruta_parcial)
                self.canvas.draw()  # Asegurar actualización
                time.sleep(0.4)  # Pausa más corta entre pasos
        
        # Ejecutar animación en thread separado
        animation_thread = threading.Thread(target=run_animation, daemon=True)
        animation_thread.start()

    # ------------------- EXPORTAR PDF -------------------
    def exportar_pdf(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files","*.pdf")])
        if file_path:
            self.fig.savefig(file_path, facecolor=self.fig.get_facecolor())
            messagebox.showinfo("Exportar PDF", f"Grafo exportado como {file_path}")
