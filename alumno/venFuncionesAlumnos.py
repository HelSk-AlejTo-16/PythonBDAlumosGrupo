import tkinter as tk
from tkinter import messagebox
from functools import partial

# CORRECCIÓN DE IMPORTACIONES: 
# Como ya estás dentro de la carpeta "alumno", no necesitas el prefijo "alumno."
from dbAlu import Alumnos 
from operacionesAlu import ejecutarBackupAlumnos, eliminarTodosLosAlumnos, restaurarTodosLosAlumnos, Agregar, Actualizar, VerUnAlumno, Limpiar, EliminarAlumno
from importacionesAlu import importarXmlAlumnos, importarJsonAlumnos, importarCsvAlumnos
from exportacionesAlu import exportarCsv, exportarJson, exportarXml

# --- Configuración principal de la ventana ---
ventana = tk.Tk()
ventana.title("Administración de Alumnos")
# Le di un poco más de altura (700) porque tenemos más campos que en grupos
ventana.geometry("700x700")
ventana.resizable(0, 0)

# Paleta de colores
COLOR_FONDO = "#f0f0f0"       
COLOR_FRAME = "#ffffff"       
COLOR_TEXTO = "#333333"       
COLOR_BTN = "#e0e0e0"         
COLOR_BTN_PELIGRO = "#ffe6e6" 

ventana.configure(bg=COLOR_FONDO)

# --- Título Superior ---
lbl_titulo = tk.Label(ventana, text="Gestión de Alumnos", font=("Segoe UI", 16, "bold"), bg=COLOR_FONDO, fg=COLOR_TEXTO)
lbl_titulo.pack(pady=(15, 5))

lbl_Bienvenido = tk.Label(ventana, text="Bienvenido(a) al sistema", font=("Segoe UI", 10), bg=COLOR_FONDO, fg="#666666")
lbl_Bienvenido.pack(pady=(0, 15))


# ==============================================================================
# SECCIÓN 1: DATOS Y OPERACIONES BÁSICAS
# ==============================================================================
frame_datos = tk.LabelFrame(ventana, text="Datos del Alumno", font=("Segoe UI", 10, "bold"), bg=COLOR_FRAME, padx=20, pady=10, relief="groove", borderwidth=2)
frame_datos.pack(fill="x", padx=20, pady=5)

# Frame interno invisible para centrar
inner_datos = tk.Frame(frame_datos, bg=COLOR_FRAME)
inner_datos.pack(anchor="center", pady=5)

# Fila 0: Clave y Botón Buscar
lbl_cveAlu = tk.Label(inner_datos, text="Clave:", font=("Segoe UI", 10, "bold"), bg=COLOR_FRAME)
lbl_cveAlu.grid(row=0, column=0, sticky="e", pady=5)
ent_cveAlu = tk.Entry(inner_datos, width=25, font=("Segoe UI", 10))
ent_cveAlu.grid(row=0, column=1, padx=10, pady=5, sticky="w")

# Fila 1: Nombre y Botón Limpiar
lbl_nomAlu = tk.Label(inner_datos, text="Nombre:", font=("Segoe UI", 10, "bold"), bg=COLOR_FRAME)
lbl_nomAlu.grid(row=1, column=0, sticky="e", pady=5)
ent_nomAlu = tk.Entry(inner_datos, width=25, font=("Segoe UI", 10))
ent_nomAlu.grid(row=1, column=1, padx=10, pady=5, sticky="w")

# Fila 2: Edad
lbl_edaAlu = tk.Label(inner_datos, text="Edad:", font=("Segoe UI", 10, "bold"), bg=COLOR_FRAME)
lbl_edaAlu.grid(row=2, column=0, sticky="e", pady=5)
ent_edaAlu = tk.Entry(inner_datos, width=25, font=("Segoe UI", 10))
ent_edaAlu.grid(row=2, column=1, padx=10, pady=5, sticky="w")

# Fila 3: Clave del Grupo
lbl_cveGru = tk.Label(inner_datos, text="Grupo:", font=("Segoe UI", 10, "bold"), bg=COLOR_FRAME)
lbl_cveGru.grid(row=3, column=0, sticky="e", pady=5)
ent_cveGru = tk.Entry(inner_datos, width=25, font=("Segoe UI", 10))
ent_cveGru.grid(row=3, column=1, padx=10, pady=5, sticky="w")

# Botones Buscar y Limpiar acomodados a la derecha
btn_buscarAlumno = tk.Button(inner_datos, text="Buscar", font=("Segoe UI", 9), bg=COLOR_BTN, width=12, command=partial(VerUnAlumno, ent_cveAlu, ent_nomAlu, ent_edaAlu, ent_cveGru))
btn_buscarAlumno.grid(row=0, column=2, padx=5, pady=5)

btn_limpiar = tk.Button(inner_datos, text="Limpiar", font=("Segoe UI", 9), bg=COLOR_BTN, width=12, command=partial(Limpiar, ent_cveAlu, ent_nomAlu, ent_edaAlu, ent_cveGru))
btn_limpiar.grid(row=1, column=2, padx=5, pady=5)

# Fila 4: Botones de Acción centrados abajo
frame_acciones = tk.Frame(inner_datos, bg=COLOR_FRAME)
frame_acciones.grid(row=4, column=0, columnspan=3, pady=(15, 0))

btn_Agregar = tk.Button(frame_acciones, text="Agregar", font=("Segoe UI", 10, "bold"), bg="#d4edda", width=12, command=partial(Agregar, ent_cveAlu, ent_nomAlu, ent_edaAlu, ent_cveGru))
btn_Agregar.pack(side="left", padx=5)

btn_Actualizar = tk.Button(frame_acciones, text="Actualizar", font=("Segoe UI", 10, "bold"), bg="#cce5ff", width=12, command=partial(Actualizar, ent_cveAlu, ent_nomAlu, ent_edaAlu, ent_cveGru))
btn_Actualizar.pack(side="left", padx=5)

btn_eliminarAlumno = tk.Button(frame_acciones, text="Eliminar", font=("Segoe UI", 10, "bold"), bg=COLOR_BTN_PELIGRO, width=12, command=partial(EliminarAlumno, ent_cveAlu, ent_nomAlu, ent_edaAlu, ent_cveGru))
btn_eliminarAlumno.pack(side="left", padx=5)


# ==============================================================================
# SECCIÓN 2: IMPORTAR Y EXPORTAR (Archivos)
# ==============================================================================
frame_archivos = tk.LabelFrame(ventana, text="Manejo de Archivos (I/O)", font=("Segoe UI", 10, "bold"), bg=COLOR_FRAME, padx=20, pady=10, relief="groove", borderwidth=2)
frame_archivos.pack(fill="x", padx=20, pady=10)

inner_archivos = tk.Frame(frame_archivos, bg=COLOR_FRAME)
inner_archivos.pack(anchor="center", pady=5)

tk.Label(inner_archivos, text="Exportar a:", font=("Segoe UI", 9), bg=COLOR_FRAME).grid(row=0, column=0, sticky="e", padx=(0,10), pady=5)
tk.Button(inner_archivos, text="CSV", font=("Segoe UI", 9), bg=COLOR_BTN, width=10, command=exportarCsv).grid(row=0, column=1, padx=5, pady=5)
tk.Button(inner_archivos, text="JSON", font=("Segoe UI", 9), bg=COLOR_BTN, width=10, command=exportarJson).grid(row=0, column=2, padx=5, pady=5)
tk.Button(inner_archivos, text="XML", font=("Segoe UI", 9), bg=COLOR_BTN, width=10, command=exportarXml).grid(row=0, column=3, padx=5, pady=5)

tk.Label(inner_archivos, text="Importar de:", font=("Segoe UI", 9), bg=COLOR_FRAME).grid(row=1, column=0, sticky="e", padx=(0,10), pady=5)
tk.Button(inner_archivos, text="CSV", font=("Segoe UI", 9), bg=COLOR_BTN, width=10, command=importarCsvAlumnos).grid(row=1, column=1, padx=5, pady=5)
tk.Button(inner_archivos, text="JSON", font=("Segoe UI", 9), bg=COLOR_BTN, width=10, command=importarJsonAlumnos).grid(row=1, column=2, padx=5, pady=5)
tk.Button(inner_archivos, text="XML", font=("Segoe UI", 9), bg=COLOR_BTN, width=10, command=importarXmlAlumnos).grid(row=1, column=3, padx=5, pady=5)


# ==============================================================================
# SECCIÓN 3: ADMINISTRACIÓN DE BASE DE DATOS (Backup)
# ==============================================================================
frame_db = tk.LabelFrame(ventana, text="Administración de Base de Datos", font=("Segoe UI", 10, "bold"), bg=COLOR_FRAME, padx=20, pady=10, relief="groove", borderwidth=2)
frame_db.pack(fill="x", padx=20, pady=5)

inner_db = tk.Frame(frame_db, bg=COLOR_FRAME)
inner_db.pack(anchor="center", pady=5)

btn_backup = tk.Button(inner_db, text="Ejecutar Backup de Alumnos", font=("Segoe UI", 10), bg="#e2e3e5", width=45, command=ejecutarBackupAlumnos)
btn_backup.pack(pady=(0, 5))

btn_restaurarTodos = tk.Button(inner_db, text="Restaurar Backup", font=("Segoe UI", 10), bg="#e2e3e5", width=45, command=restaurarTodosLosAlumnos)
btn_restaurarTodos.pack(pady=5)

btn_eliminarTodos = tk.Button(inner_db, text="Eliminar Todos los Alumnos", font=("Segoe UI", 10, "bold"), bg=COLOR_BTN_PELIGRO, fg="#cc0000", width=45, command=eliminarTodosLosAlumnos)
btn_eliminarTodos.pack(pady=(5, 0))

ventana.mainloop()