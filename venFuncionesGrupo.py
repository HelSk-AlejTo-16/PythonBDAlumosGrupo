import tkinter as tk
from tkinter import messagebox
from functools import partial

# Tus importaciones
from db import Grupos 
from importaciones import importarCsv, importarJson, importarXml
from operaciones import Agregar, Actualizar, VerUnGrupo, Limpiar, EliminarGrupo, eliminarTodosLosGrupos, restaurarTodosLosGrupos
from exportaciones import exportarCsv, exportarJson, ejecutarBackup, exportarXml

# --- Configuración principal de la ventana ---
ventana = tk.Tk()
ventana.title("Administración de Grupos")
ventana.geometry("700x650") 
ventana.resizable(0,0)

COLOR_FONDO = "#f0f0f0"       
COLOR_FRAME = "#ffffff"       
COLOR_TEXTO = "#333333"       
COLOR_BTN = "#e0e0e0"         
COLOR_BTN_PELIGRO = "#ffe6e6" 

ventana.configure(bg=COLOR_FONDO)

# --- Título Superior ---
lbl_titulo = tk.Label(ventana, text="Gestión de Grupos", font=("Segoe UI", 16, "bold"), bg=COLOR_FONDO, fg=COLOR_TEXTO)
lbl_titulo.pack(pady=(15, 5))

lbl_Bienvenido = tk.Label(ventana, text="Bienvenido(a) al sistema", font=("Segoe UI", 10), bg=COLOR_FONDO, fg="#666666")
lbl_Bienvenido.pack(pady=(0, 15))


# ==============================================================================
# SECCIÓN 1: DATOS Y OPERACIONES BÁSICAS
# ==============================================================================
frame_datos = tk.LabelFrame(ventana, text="Datos del Grupo", font=("Segoe UI", 10, "bold"), bg=COLOR_FRAME, padx=20, pady=10, relief="groove", borderwidth=2)
frame_datos.pack(fill="x", padx=20, pady=5)

# Frame interno invisible para centrar todo el bloque
inner_datos = tk.Frame(frame_datos, bg=COLOR_FRAME)
inner_datos.pack(anchor="center", pady=5)

# Fila 0 y 1: Cajas de texto (Definimos los Entry primero para que el partial no falle)
lbl_cveGru = tk.Label(inner_datos, text="Clave:", font=("Segoe UI", 10, "bold"), bg=COLOR_FRAME)
lbl_cveGru.grid(row=0, column=0, sticky="e", pady=5)
ent_cveGru = tk.Entry(inner_datos, width=25, font=("Segoe UI", 10))
ent_cveGru.grid(row=0, column=1, padx=10, pady=5, sticky="w")

lbl_nomGru = tk.Label(inner_datos, text="Nombre:", font=("Segoe UI", 10, "bold"), bg=COLOR_FRAME)
lbl_nomGru.grid(row=1, column=0, sticky="e", pady=5)
ent_nomGru = tk.Entry(inner_datos, width=25, font=("Segoe UI", 10))
ent_nomGru.grid(row=1, column=1, padx=10, pady=5, sticky="w")

# Botones Buscar y Limpiar
btn_buscarGrupo = tk.Button(inner_datos, text="Buscar", font=("Segoe UI", 9), bg=COLOR_BTN, width=12, command=partial(VerUnGrupo,ent_cveGru,ent_nomGru))
btn_buscarGrupo.grid(row=0, column=2, padx=5, pady=5)

btn_limpiar = tk.Button(inner_datos, text="Limpiar", font=("Segoe UI", 9), bg=COLOR_BTN, width=12, command=partial(Limpiar,ent_cveGru,ent_nomGru))
btn_limpiar.grid(row=1, column=2, padx=5, pady=5)

# Fila 2: Botones de Acción centrados abajo
frame_acciones = tk.Frame(inner_datos, bg=COLOR_FRAME)
frame_acciones.grid(row=2, column=0, columnspan=3, pady=(15, 0))

btn_Agregar = tk.Button(frame_acciones, text="Agregar", font=("Segoe UI", 10, "bold"), bg="#d4edda", width=12, command=partial(Agregar,ent_cveGru,ent_nomGru))
btn_Agregar.pack(side="left", padx=5)

btn_Actualizar = tk.Button(frame_acciones, text="Actualizar", font=("Segoe UI", 10, "bold"), bg="#cce5ff", width=12, command=partial(Actualizar,ent_cveGru,ent_nomGru))
btn_Actualizar.pack(side="left", padx=5)

btn_borrarGrupo = tk.Button(frame_acciones, text="Eliminar", font=("Segoe UI", 10, "bold"), bg=COLOR_BTN_PELIGRO, width=12, command=partial(EliminarGrupo,ent_cveGru,ent_nomGru))
btn_borrarGrupo.pack(side="left", padx=5)


# ==============================================================================
# SECCIÓN 2: IMPORTAR Y EXPORTAR (Archivos)
# ==============================================================================
frame_archivos = tk.LabelFrame(ventana, text="Manejo de Archivos (I/O)", font=("Segoe UI", 10, "bold"), bg=COLOR_FRAME, padx=20, pady=10, relief="groove", borderwidth=2)
frame_archivos.pack(fill="x", padx=20, pady=10)

# Frame interno para centrar botones
inner_archivos = tk.Frame(frame_archivos, bg=COLOR_FRAME)
inner_archivos.pack(anchor="center", pady=5)

tk.Label(inner_archivos, text="Exportar a:", font=("Segoe UI", 9), bg=COLOR_FRAME).grid(row=0, column=0, sticky="e", padx=(0,10), pady=5)
tk.Button(inner_archivos, text="CSV", font=("Segoe UI", 9), bg=COLOR_BTN, width=10, command=exportarCsv).grid(row=0, column=1, padx=5, pady=5)
tk.Button(inner_archivos, text="JSON", font=("Segoe UI", 9), bg=COLOR_BTN, width=10, command=exportarJson).grid(row=0, column=2, padx=5, pady=5)
tk.Button(inner_archivos, text="XML", font=("Segoe UI", 9), bg=COLOR_BTN, width=10, command=exportarXml).grid(row=0, column=3, padx=5, pady=5)

tk.Label(inner_archivos, text="Importar de:", font=("Segoe UI", 9), bg=COLOR_FRAME).grid(row=1, column=0, sticky="e", padx=(0,10), pady=5)
tk.Button(inner_archivos, text="CSV", font=("Segoe UI", 9), bg=COLOR_BTN, width=10, command=importarCsv).grid(row=1, column=1, padx=5, pady=5)
tk.Button(inner_archivos, text="JSON", font=("Segoe UI", 9), bg=COLOR_BTN, width=10, command=importarJson).grid(row=1, column=2, padx=5, pady=5)
tk.Button(inner_archivos, text="XML", font=("Segoe UI", 9), bg=COLOR_BTN, width=10, command=importarXml).grid(row=1, column=3, padx=5, pady=5)


# ==============================================================================
# SECCIÓN 3: ADMINISTRACIÓN DE BASE DE DATOS (Backup)
# ==============================================================================
frame_db = tk.LabelFrame(ventana, text="Administración de Base de Datos", font=("Segoe UI", 10, "bold"), bg=COLOR_FRAME, padx=20, pady=10, relief="groove", borderwidth=2)
frame_db.pack(fill="x", padx=20, pady=5)

# Frame interno para darle un ancho fijo y centrado a los botones de DB
inner_db = tk.Frame(frame_db, bg=COLOR_FRAME)
inner_db.pack(anchor="center", pady=5)

# Agregué un width=45 para que los botones tengan un tamaño uniforme y no se estiren de lado a lado
btn_backup = tk.Button(inner_db, text="Ejecutar Backup", font=("Segoe UI", 10), bg="#e2e3e5", width=45, command=ejecutarBackup)
btn_backup.pack(pady=(0, 5))

btn_restaurarTodos = tk.Button(inner_db, text="Restaurar Backup", font=("Segoe UI", 10), bg="#e2e3e5", width=45, command=restaurarTodosLosGrupos)
btn_restaurarTodos.pack(pady=5)

btn_eliminarTodos = tk.Button(inner_db, text="Eliminar Todos los Grupos", font=("Segoe UI", 10, "bold"), bg=COLOR_BTN_PELIGRO, fg="#cc0000", width=45, command=eliminarTodosLosGrupos)
btn_eliminarTodos.pack(pady=(5, 0))


ventana.mainloop()