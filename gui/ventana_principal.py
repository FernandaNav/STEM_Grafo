import sys
import os
import time
import threading
# Agregar el directorio padre al path para imports relativos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import customtkinter as ctk
from grafo.grafo_logic import GrafoLogic
from gui.formularios import FormularioManager

class GrafoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Rutas STEM - Navegador de Carreras")
        
        # Configurar ventana para experiencia premium
        self.geometry("1800x1100")  # Aún más grande para mejor experiencia
        self.minsize(1600, 1000)
        
        # Maximizar automáticamente para presentaciones
        try:
            self.state('zoomed')  # Maximizar en Windows
        except:
            # Fallback para otros sistemas
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            self.geometry(f"{screen_width}x{screen_height}")
        
        # Configurar tema moderno premium
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Configurar colores personalizados
        self.bg_primary = "#0D1117"      # Fondo principal (GitHub dark)
        self.bg_secondary = "#161B22"    # Fondo secundario
        self.accent_blue = "#58A6FF"     # Azul acento
        self.accent_green = "#3FB950"    # Verde acento  
        self.text_primary = "#F0F6FC"    # Texto principal
        self.text_secondary = "#7D8590"  # Texto secundario

        # Frame principal con diseño premium moderno
        self.configure(fg_color=self.bg_primary)
        self.frame = ctk.CTkFrame(self, corner_radius=16, fg_color=self.bg_secondary, 
                                 border_width=2, border_color=self.accent_blue)
        self.frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Header premium con gradiente visual
        header_frame = ctk.CTkFrame(self.frame, height=100, corner_radius=12,
                                   fg_color=self.bg_primary, border_width=1, 
                                   border_color=self.accent_green)
        header_frame.pack(fill="x", padx=15, pady=(15, 10))
        header_frame.pack_propagate(False)
        
        # Container para título con mejor layout
        title_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_container.pack(expand=True, fill="both", padx=20, pady=15)
        
        # Título principal con estilo premium
        self.label = ctk.CTkLabel(
            title_container, 
            text="SISTEMA DE RUTAS STEM",
            font=("Segoe UI", 32, "bold"), 
            text_color=self.accent_blue
        )
        self.label.pack(side="top", anchor="w")
        
        # Subtítulo elegante con mejor tipografía
        self.subtitle = ctk.CTkLabel(
            title_container,
            text="Navega tu futuro profesional • Tecnología • Ciencia • Ingeniería • Matemáticas",
            font=("Segoe UI", 14),
            text_color=self.text_secondary
        )
        self.subtitle.pack(side="top", anchor="w", pady=(5, 0))
        
        # Barra de progreso animada (inicialmente oculta)
        self.progress_frame = ctk.CTkFrame(title_container, fg_color="transparent")
        self.progress_frame.pack(side="top", anchor="w", pady=(10, 0))
        
        self.progress_label = ctk.CTkLabel(
            self.progress_frame,
            text="Procesando ruta...",
            font=("Segoe UI", 10),
            text_color=self.accent_blue
        )
        
        self.progress_bar = ctk.CTkProgressBar(
            self.progress_frame,
            width=300,
            height=8,
            progress_color=self.accent_green,
            fg_color=self.bg_secondary
        )
        
        # Inicialmente ocultos
        self.progress_frame.pack_forget()
        
        # Indicador de estado
        status_label = ctk.CTkLabel(
            title_container,
            text="● Sistema Activo",
            font=("Segoe UI", 12, "bold"),
            text_color=self.accent_green
        )
        status_label.pack(side="bottom", anchor="e")

        # Panel de control premium (CREAR PRIMERO para garantizar espacio)
        control_panel = ctk.CTkFrame(self.frame, corner_radius=12, height=160,
                                   fg_color=self.bg_primary, border_width=1,
                                   border_color=self.text_secondary)
        control_panel.pack(side="bottom", fill="x", padx=15, pady=(10, 15))
        control_panel.pack_propagate(False)

        # Frame separador entre grafo y controles
        separator_frame = ctk.CTkFrame(self.frame, height=20, fg_color="transparent")
        separator_frame.pack(fill="x", pady=5)

        # Instanciar la lógica del grafo DESPUÉS del panel de control
        self.grafo = GrafoLogic(self.frame)

        # Título del panel de control
        panel_title = ctk.CTkLabel(control_panel, text="PANEL DE CONTROL",
                                  font=("Segoe UI", 14, "bold"),
                                  text_color=self.text_secondary)
        panel_title.pack(pady=(10, 5))
        
        # Container para botones con diseño moderno
        botones_container = ctk.CTkFrame(control_panel, fg_color="transparent")
        botones_container.pack(expand=True, fill="both", padx=25, pady=(0, 15))
        
        # Sección de áreas STEM con diseño premium
        areas_frame = ctk.CTkFrame(botones_container, fg_color="transparent")
        areas_frame.pack(side="left", padx=(0, 30))
        
        areas_title = ctk.CTkLabel(areas_frame, text="ÁREAS STEM", 
                                  font=("Segoe UI", 11, "bold"),
                                  text_color=self.text_secondary)
        areas_title.pack(pady=(0, 8))
        
        areas_buttons = ctk.CTkFrame(areas_frame, fg_color="transparent")
        areas_buttons.pack()
        
        self.crear_boton_premium(
            areas_buttons, "PROGRAMACIÓN", 
            lambda: FormularioManager(self.grafo,"Programación").abrir_form(),
            "#58A6FF", "#388BFD", "💻"
        )
        
        self.crear_boton_premium(
            areas_buttons, "CIENCIA", 
            lambda: FormularioManager(self.grafo,"Ciencia").abrir_form(),
            "#F78166", "#F85149", "🧪"
        )
        
        self.crear_boton_premium(
            areas_buttons, "INGENIERÍA", 
            lambda: FormularioManager(self.grafo,"Ingeniería").abrir_form(),
            "#A5A5FF", "#8B949E", "⚡"
        )
        
        # Separador moderno con gradiente
        separator = ctk.CTkFrame(botones_container, width=3, 
                               fg_color=self.accent_blue, corner_radius=2)
        separator.pack(side="left", fill="y", padx=30, pady=10)
        
        # Sección de herramientas
        tools_frame = ctk.CTkFrame(botones_container, fg_color="transparent")
        tools_frame.pack(side="left")
        
        tools_title = ctk.CTkLabel(tools_frame, text="HERRAMIENTAS", 
                                  font=("Segoe UI", 11, "bold"),
                                  text_color=self.text_secondary)
        tools_title.pack(pady=(0, 8))
        
        tools_buttons = ctk.CTkFrame(tools_frame, fg_color="transparent")
        tools_buttons.pack()
        
        self.crear_boton_premium(
            tools_buttons, "REINICIAR", 
            self.grafo.reiniciar_grafo,
            "#3FB950", "#2EA043", "🔄"
        )
        
        self.crear_boton_premium(
            tools_buttons, "EXPORTAR PDF", 
            self.grafo.exportar_pdf,
            "#FF7B72", "#DA3633", "📊"
        )
    
    def crear_boton_premium(self, parent, texto, comando, color_normal, color_hover, icono=""):
        """Crear botones con diseño premium moderno (version simple sin glassmorphism)"""
        
        # Container para efecto hover
        button_container = ctk.CTkFrame(parent, fg_color="transparent")
        button_container.pack(side="left", padx=8, pady=5)
        
        # Texto del botón con icono
        display_text = f"{icono} {texto}" if icono else texto
        
        boton = ctk.CTkButton(
            button_container,
            text=display_text,
            command=comando,
            fg_color=color_normal,
            hover_color=color_hover,
            font=("Segoe UI", 16, "bold"),  # Fuente más grande
            width=160,  # Más ancho
            height=60,  # Más alto
            corner_radius=12,
            border_width=2,
            border_color=color_hover,
            text_color="#FFFFFF"
        )
        boton.pack()
        
        return boton

    def crear_boton_mejorado(self, parent, texto, comando, color_normal, color_hover):
        """Mantener compatibilidad con función anterior"""
        return self.crear_boton_premium(parent, texto, comando, color_normal, color_hover)
    
    def mostrar_progreso(self, texto="Procesando..."):
        """Mostrar barra de progreso animada"""
        self.progress_label.configure(text=texto)
        self.progress_label.pack(side="left", padx=(0, 10))
        self.progress_bar.pack(side="left")
        self.progress_frame.pack(side="top", anchor="w", pady=(10, 0))
        
        # Animar la barra de progreso
        self.animar_progreso()
    
    def ocultar_progreso(self):
        """Ocultar barra de progreso"""
        self.progress_frame.pack_forget()
        self.progress_bar.set(0)
    
    def animar_progreso(self):
        """Animación de la barra de progreso"""
        def actualizar_progreso():
            for i in range(101):
                self.progress_bar.set(i / 100)
                self.update()
                time.sleep(0.02)  # Animación suave
            
        import threading
        thread = threading.Thread(target=actualizar_progreso, daemon=True)
        thread.start()

if __name__ == "__main__":
    app = GrafoApp()
    app.mainloop()
