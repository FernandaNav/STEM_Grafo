# -*- coding: utf-8 -*-
"""
Sistema de Rutas STEM - Aplicación Principal
Compatible con Windows
"""
import sys
import os

# Configurar codificación para Windows
import locale
locale.setlocale(locale.LC_ALL, 'C')

# Asegurar que el directorio actual esté en el path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from gui.ventana_principal import GrafoApp
except ImportError as e:
    print(f"Error de importación: {e}")
    print("Intentando import alternativo...")
    # Import alternativo directo
    import importlib.util
    spec = importlib.util.spec_from_file_location("ventana_principal", 
                                                 os.path.join(current_dir, "gui", "ventana_principal.py"))
    ventana_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ventana_module)
    GrafoApp = ventana_module.GrafoApp

if __name__ == "__main__":
    print(">>> Iniciando Sistema de Rutas STEM...")
    try:
        app = GrafoApp()
        app.mainloop()
    except Exception as e:
        print(f"Error al ejecutar la aplicacion: {e}")
        import traceback
        traceback.print_exc()
