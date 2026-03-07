import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient as MC

ventana = tk.Tk()
ventana.title("Agregar Grupo")
ventana.geometry("400x200")
ventana.resizable(0,0)
ventana.config(cursor="hand2")

# Conexión a MongoDB
client = MC("mongodb://localhost:27017/")
db = client["BD_GrupoAlumno"]
Grupos = db["Grupo"]

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

# Función para agregar grupo
def Agregar():
    Grupos.insert_one({"cveGru": ent_cveGru.get(), "nomGru": ent_nomGru.get()})
    messagebox.showinfo("Éxito", "Grupo agregado correctamente")
    ent_cveGru.delete(0, tk.END)
    ent_nomGru.delete(0, tk.END)

# Botón Agregar
btn_Agregar = tk.Button(ventana, text="Agregar", font=("Arial", 12, "bold"), bg="white", fg="black", command=Agregar)
btn_Agregar.grid(row=3, column=1)


ventana.mainloop()