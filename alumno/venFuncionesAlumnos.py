import tkinter as tk
from tkinter import messagebox
from alumno.operaciones import ejecutarBackupAlumnos, eliminarTodosLosAlumnos, restaurarTodosLosAlumnos, Agregar, Actualizar, VerUnAlumno, Limpiar, EliminarAlumno
from alumno.db import Alumnos 
from functools import partial
from alumno.importaciones import importarXmlAlumnos, importarJsonAlumnos, importarCsvAlumnos
from alumno.exportaciones import exportarCsv, exportarJson, exportarXml

ventana = tk.Tk()
ventana.title("Gestión de Alumnos")
ventana.geometry("900x500")
ventana.resizable(0, 0)
ventana.config(cursor="hand2")

# Label - Bienvenida
lbl_Bienvenido = tk.Label(ventana, text="Gestión de Alumnos", font=("Arial", 14, "bold"))
lbl_Bienvenido.grid(row=0, column=0, columnspan=3, pady=10)

# Label - Clave del alumno
lbl_cveAlu = tk.Label(ventana, text="Clave:", font=("Arial", 11, "bold"))
lbl_cveAlu.grid(row=1, column=0, sticky="e", padx=5)

# Label - Nombre del alumno
lbl_nomAlu = tk.Label(ventana, text="Nombre:", font=("Arial", 11, "bold"))
lbl_nomAlu.grid(row=2, column=0, sticky="e", padx=5)

# Label - Edad del alumno
lbl_edaAlu = tk.Label(ventana, text="Edad:", font=("Arial", 11, "bold"))
lbl_edaAlu.grid(row=3, column=0, sticky="e", padx=5)

# Label - Clave del grupo
lbl_cveGru = tk.Label(ventana, text="Grupo:", font=("Arial", 11, "bold"))
lbl_cveGru.grid(row=4, column=0, sticky="e", padx=5)

# Entry - Clave del alumno
ent_cveAlu = tk.Entry(ventana, width=30)
ent_cveAlu.grid(row=1, column=1, padx=10, pady=5)

# Entry - Nombre del alumno
ent_nomAlu = tk.Entry(ventana, width=30)
ent_nomAlu.grid(row=2, column=1, padx=10, pady=5)

# Entry - Edad del alumno
ent_edaAlu = tk.Entry(ventana, width=30)
ent_edaAlu.grid(row=3, column=1, padx=10, pady=5)

# Entry - Clave del grupo
ent_cveGru = tk.Entry(ventana, width=30)
ent_cveGru.grid(row=4, column=1, padx=10, pady=5)

# Botón Agregar
btn_Agregar = tk.Button(ventana, text="Agregar", font=("Arial", 12, "bold"), bg="white", fg="black", command=partial(Agregar, ent_cveAlu, ent_nomAlu, ent_edaAlu, ent_cveGru))
btn_Agregar.grid(row=1, column=2, padx=10, pady=5)

# Botón Actualizar
btn_Actualizar = tk.Button(ventana, text="Actualizar", font=("Arial", 12, "bold"), bg="white", fg="black", command=partial(Actualizar, ent_cveAlu, ent_nomAlu, ent_edaAlu, ent_cveGru))
btn_Actualizar.grid(row=2, column=2, padx=10, pady=5)

# Botón Buscar
btn_buscarAlumno = tk.Button(ventana, text="Buscar", font=("Arial", 12, "bold"), bg="white", fg="black", command=partial(VerUnAlumno, ent_cveAlu, ent_nomAlu, ent_edaAlu, ent_cveGru))
btn_buscarAlumno.grid(row=3, column=2, padx=10, pady=5)

# Botón Limpiar
btn_limpiar = tk.Button(ventana, text="Limpiar", font=("Arial", 12, "bold"), bg="white", fg="black", command=partial(Limpiar, ent_cveAlu, ent_nomAlu, ent_edaAlu, ent_cveGru))
btn_limpiar.grid(row=4, column=2, padx=10, pady=5)

# Botón Eliminar
btn_eliminarAlumno = tk.Button(ventana, text="Eliminar", font=("Arial", 12, "bold"), bg="white", fg="black", command=partial(EliminarAlumno, ent_cveAlu, ent_nomAlu, ent_edaAlu, ent_cveGru))
btn_eliminarAlumno.grid(row=5, column=2, padx=10, pady=5)

# Botón Exportar CSV
btn_exportarCsv = tk.Button(ventana, text="Exportar CSV", font=("Arial", 12, "bold"), bg="white", fg="black", command=exportarCsv)
btn_exportarCsv.grid(row=6, column=0, padx=10, pady=10)

# Botón Exportar JSON
btn_exportarJson = tk.Button(ventana, text="Exportar JSON", font=("Arial", 12, "bold"), bg="white", fg="black", command=exportarJson)
btn_exportarJson.grid(row=6, column=1, padx=10, pady=10)

# Botón Exportar XML
btn_exportarXml = tk.Button(ventana, text="Exportar XML", font=("Arial", 12, "bold"), bg="white", fg="black", command=exportarXml)
btn_exportarXml.grid(row=6, column=2, padx=10, pady=10)

## Botón importar CSV
btn_importarCsv = tk.Button(ventana, text="Importar csv", font=("Arial",12, "bold"), bg="white", fg="black", command=importarCsvAlumnos)
btn_importarCsv.grid(row=5, column=0, padx=10, pady=5)

## Botón importar JSON
btn_importarJson = tk.Button(ventana, text="Importar json", font=("Arial",12, "bold"), bg="white", fg="black", command=importarJsonAlumnos)
btn_importarJson.grid(row=5, column=1, padx=10, pady=5)

## Botón importar XML
btn_importarXml = tk.Button(ventana, text="Importar xml", font=("Arial",12, "bold"), bg="white", fg="black", command=importarXmlAlumnos)
btn_importarXml.grid(row=5, column=2, padx=10, pady=5)

# Botón Backup
btn_backup = tk.Button(ventana, text="Ejecutar Backup", font=("Arial", 12, "bold"), bg="white", fg="black", command=ejecutarBackupAlumnos)
btn_backup.grid(row=7, column=0, columnspan=3, sticky="we", padx=10, pady=10)

# Botón Eliminar todos los Grupos
btn_eliminarTodos = tk.Button(ventana, text="Eliminar todos los Grupos", font=("Arial",12, "bold"), bg="white", fg="black", command=eliminarTodosLosAlumnos)
btn_eliminarTodos.grid(row=7, column=0, columnspan=3, sticky="we", padx=10, pady=5)

# Botón Restaurar todos los Grupos
btn_restaurarTodos = tk.Button(ventana, text="Restaurar todos los Grupos", font=("Arial",12, "bold"), bg="white", fg="black", command=restaurarTodosLosAlumnos)
btn_restaurarTodos.grid(row=8, column=0, columnspan=3, sticky="we", padx=10, pady=5)

ventana.mainloop()
