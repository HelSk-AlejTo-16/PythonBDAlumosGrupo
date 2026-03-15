import tkinter as tk
from tkinter import messagebox
from db import Grupos 
from functools import partial
from operaciones import Agregar,Actualizar,VerUnGrupo,Limpiar,EliminarGrupo
from exportaciones import exportarCsv, exportarJson, ejecutarBackup,exportarXml

ventana = tk.Tk()
ventana.title("Agregar Grupo")
ventana.geometry("800x400")
ventana.resizable(0,0)
ventana.config(cursor="hand2")

#Label-Etiquetas
lbl_Bienvenido =tk.Label(ventana, text="Bienvenido(a)", font=("Arial", 11))

lbl_Bienvenido.grid(row=0, column=0)

#Label - Clave del grupo
lbl_cveGru = tk.Label(ventana, text="Clave:", font=("Arial", 11, "bold"))

lbl_cveGru.grid(row=1, column=0)

#Label - Nombre del grupo
lbl_nomGru = tk.Label(ventana, text="Nombre:", font=("Arial", 11, "bold"))
lbl_nomGru.grid(row=2, column=0)

#Cajas de texto

# Entry - Clave del grupo
ent_cveGru = tk.Entry(ventana, width=30)
ent_cveGru.grid(row=1, column=1, padx=10, pady=5)

# Entry - Nombre del grupo
ent_nomGru = tk.Entry(ventana, width=30)
ent_nomGru.grid(row=2, column=1, padx=10, pady=5)

# Botón Agregar
#partial pre-carga los entries para que cuando el botón llame a Agregar() sin argumentos, Python ya sepa cuáles pasarle. Lo mismo aplica para todas las demás funciones de operaciones.py.
btn_Agregar = tk.Button(ventana, text="Agregar", font=("Arial", 12, "bold"), bg="white", fg="black", command=partial(Agregar,ent_cveGru,ent_nomGru))
btn_Agregar.grid(row=3, column=0)

# Botón Actualizar
btn_Actualizar = tk.Button(ventana, text="Actualizar", font=("Arial", 12, "bold"), bg="white", fg="black", command=partial(Actualizar,ent_cveGru,ent_nomGru))
btn_Actualizar.grid(row=3, column=1)

#botón Buscar.
btn_buscarGrupo = tk.Button(ventana, text="Buscar",font=("Arial",12, "bold"), bg="white", fg="black", command=partial(VerUnGrupo,ent_cveGru,ent_nomGru))
btn_buscarGrupo.grid(row=1, column=2 , padx=10, pady=5)

#Botón Limpiar
btn_limpiar = tk.Button(ventana, text="Limpiar", font=("Arial",12, "bold"), bg="white", fg="black", command=partial(Limpiar,ent_cveGru,ent_nomGru))
btn_limpiar.grid(row=2, column=2, padx=10, pady=5)

#Botón Borrar
btn_borrarGrupo= tk.Button(ventana, text="Eliminar", font=("Arial",12,"bold"), bg="white", fg="black", command=partial(EliminarGrupo,ent_cveGru,ent_nomGru))
btn_borrarGrupo.grid(row=3, column=2, padx=10, pady=5)

##Boton exportar CSV
btn_exportarCsv = tk.Button(ventana, text="Exportar csv", font=("Arial",12, "bold"), bg="white", fg="black", command=exportarCsv)
btn_exportarCsv.grid(row=4, column=0,padx=10, pady=5 )

##Botón exportar Json
btn_exportarJson = tk.Button(ventana, text="Exportar json", font=("Arial",12, "bold"), bg="white", fg="black", command=exportarJson)
btn_exportarJson.grid(row=4, column=1,padx=10, pady=5 )

#Botón exportar xml
btn_exportarXml = tk.Button(ventana, text="Exportar xml", font=("Arial",12, "bold"), bg="white", fg="black", command=exportarXml)
btn_exportarXml.grid(row=4, column=2,padx=10, pady=5 )

 ##Botón backup
btn_backup = tk.Button(ventana, text="Ejecutar Backup", font=("Arial",12, "bold"), bg="white", fg="black", command=ejecutarBackup)
btn_backup.grid(row=6, column=0, columnspan=3, sticky="we", padx=10, pady=5)

ventana.mainloop()