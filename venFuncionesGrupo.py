import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient as MC
import csv
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os
from datetime import datetime

ventana = tk.Tk()
ventana.title("Agregar Grupo")
ventana.geometry("800x400")
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
    if not ent_cveGru.get():
        messagebox.showerror("Error", "Por favor, ingresa la clave del grupo")
        return
    
    if not ent_nomGru.get():
        messagebox.showerror("Error", "Por favor, ingresa el nombre del grupo")
        return
    
    if Grupos.find_one({"cveGru": ent_cveGru.get()}) is not None:
        messagebox.showerror("Error", "Ya existe un grupo con la clave proporcionada")
        return
    else:
        Grupos.insert_one({"cveGru": ent_cveGru.get(), "nomGru": ent_nomGru.get()})
        messagebox.showinfo("Éxito", "Grupo agregado correctamente")
        ent_cveGru.delete(0, tk.END)
        ent_nomGru.delete(0, tk.END)

# Función para actualizar grupo
def Actualizar():
    if not ent_cveGru.get():
        messagebox.showerror("Error", "Por favor, ingresa la clave del grupo a actualizar")
        return
    if not ent_nomGru.get():
        messagebox.showerror("Error", "Por favor, ingresa el nuevo nombre del grupo")
        return
    
    if Grupos.find_one({"cveGru": ent_cveGru.get()}) is None:
        messagebox.showerror("Error", "No se encontró un grupo con la clave proporcionada")
        return
    else:
        Grupos.update_one({"cveGru": ent_cveGru.get()}, {"$set": {"nomGru": ent_nomGru.get()}})
        messagebox.showinfo("Éxito", "Grupo actualizado correctamente")
        ent_cveGru.delete(0, tk.END)
        ent_nomGru.delete(0, tk.END)



# Botón Agregar
btn_Agregar = tk.Button(ventana, text="Agregar", font=("Arial", 12, "bold"), bg="white", fg="black", command=Agregar)
btn_Agregar.grid(row=3, column=0)

# Botón Actualizar
btn_Actualizar = tk.Button(ventana, text="Actualizar", font=("Arial", 12, "bold"), bg="white", fg="black", command=Actualizar)
btn_Actualizar.grid(row=3, column=1)


#Función para ver grupo
def VerUnGrupo():
    # .get().strip() elimina espacios accidentales al inicio o final
    clave = ent_cveGru.get().strip()
    nombre = ent_nomGru.get().strip()

    if clave and nombre:
        Grupo_Existente = Grupos.find_one({"cveGru": clave, "nomGru": nombre})
        
        if not Grupo_Existente:
            messagebox.showerror("Error", "No existe un grupo con esos datos.")
            ent_cveGru.delete(0, tk.END)
            ent_nomGru.delete(0, tk.END)
        else:
          
            resumen = f"Clave: {Grupo_Existente['cveGru']}\nNombre: {Grupo_Existente['nomGru']}"
            messagebox.showinfo("Éxito", resumen)
    elif clave or nombre:
        messagebox.showwarning("Atención", "Por favor llene ambos campos.")
    else:
      
        lista_grupos = Grupos.find()
        listado = "--Listado de todos los grupos --\n \n"

        for grupo in lista_grupos:
            listado += f"{grupo['cveGru']} - {grupo['nomGru']}\n"
        messagebox.showinfo("Todos los grupos", listado)
#botón buscar.
btn_buscarGrupo = tk.Button(ventana, text="Buscar",font=("Arial",12, "bold"), bg="white", fg="black", command=VerUnGrupo)
btn_buscarGrupo.grid(row=1, column=2 , padx=10, pady=5)

#Limpiar Grupo.
def Limpiar():
    clave = ent_cveGru.get()
    nombre = ent_nomGru.get()
    if not clave and not nombre:
       messagebox.showerror("Atención", "No hay nada para borrar")

    else:
        
        ent_nomGru.delete(0,tk.END)
        ent_cveGru.delete(0,tk.END)


btn_limpiar = tk.Button(ventana, text="Limpiar", font=("Arial",12, "bold"), bg="white", fg="black", command=Limpiar)
btn_limpiar.grid(row=2, column=2, padx=10, pady=5)


def EliminarGrupo(): 
    clave = ent_cveGru.get().strip()
    nombre = ent_nomGru.get().strip()

    if clave and nombre:
        Grupo_Existente = Grupos.find_one({"cveGru": clave, "nomGru": nombre})

        if not Grupo_Existente:
            messagebox.showerror("Error", "No existe un grupo con esos datos.")
            ent_cveGru.delete(0, tk.END)
            ent_nomGru.delete(0, tk.END)
        
        else:
            Grupos.delete_one({"cveGru":clave, "nomGru":nombre})
            messagebox.showinfo("Éxito", "Se borró exitosamente el grupo")
            ##Falta borrar los alumnos :p
    elif clave or nombre:
            messagebox.showerror("Atención", "Por favor llene ambos campos.")

    else:
        messagebox.showerror("Error", "Llene los dos apartados.")

btn_borrarGrupo= tk.Button(ventana, text="Eliminar", font=("Arial",12,"bold"), bg="white", fg="black", command=EliminarGrupo)
btn_borrarGrupo.grid(row=3, column=2, padx=10, pady=5)


##Método para todos
def generarNombreArchivo(extension):
    carpeta = r"C:\Backup_Mongo"
    os.makedirs(carpeta, exist_ok=True)  # crea la carpeta si no existe
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    
    return os.path.join(carpeta, f"grupos_{timestamp}.{extension}")


#Exportar csv
def exportarCsv():
    grupos = list(Grupos.find())
 
    if not grupos:
        messagebox.showwarning("Atención", "No hay grupos para exportar.")
        return
 
    nombre_archivo = generarNombreArchivo("csv")
 
    with open(nombre_archivo, mode="w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        # Encabezado
        escritor.writerow(["cveGru", "nomGru"])
        # Filas
        for grupo in grupos:
            escritor.writerow([grupo["cveGru"], grupo["nomGru"]])
 
    ruta = os.path.abspath(nombre_archivo)
    messagebox.showinfo("Exportado", f"Archivo CSV generado exitosamente:\n{ruta}")




btn_exportarCsv = tk.Button(ventana, text="Exportar csv", font=("Arial",12, "bold"), bg="white", fg="black", command=exportarCsv)
btn_exportarCsv.grid(row=4, column=0,padx=10, pady=5 )
#Exportar json
def exportarJson():
    grupos = list(Grupos.find())
 
    if not grupos:
        messagebox.showwarning("Atención", "No hay grupos para exportar.")
        return
 
    # Convertir ObjectId de MongoDB a string para que sea serializable
    for grupo in grupos:
        grupo["_id"] = str(grupo["_id"])
 
    nombre_archivo = generarNombreArchivo("json")
 
    with open(nombre_archivo, mode="w", encoding="utf-8") as archivo:
        json.dump(grupos, archivo, ensure_ascii=False, indent=4)
        ##ensure_ascii permite caracteres especiales y ident
 
    ruta = os.path.abspath(nombre_archivo)
    messagebox.showinfo("Exportado", f"Archivo JSON generado exitosamente:\n{ruta}")
 



btn_exportarJson = tk.Button(ventana, text="Exportar json", font=("Arial",12, "bold"), bg="white", fg="black", command=exportarJson)
btn_exportarJson.grid(row=4, column=1,padx=10, pady=5 )
#Exportar xml
def exportarXml():
    grupos = list(Grupos.find())
 
    if not grupos:
        messagebox.showwarning("Atención", "No hay grupos para exportar.")
        return
 
    # Crear estructura XML
    raiz = ET.Element("Grupos")
 
    for grupo in grupos:
        nodo_grupo = ET.SubElement(raiz, "Grupo")
        nodo_cve = ET.SubElement(nodo_grupo, "cveGru")
        nodo_cve.text = grupo["cveGru"]
        nodo_nom = ET.SubElement(nodo_grupo, "nomGru")
        nodo_nom.text = grupo["nomGru"]
 
    # Formatear el XML con sangría para que sea legible
    xml_str = minidom.parseString(ET.tostring(raiz, encoding="unicode")).toprettyxml(indent="  ")
 
    # Eliminar la línea extra que agrega toprettyxml al inicio
    lineas = xml_str.split("\n")
    xml_formateado = "\n".join(lineas[1:])  # quita '<?xml version="1.0" ?>' duplicado si lo hubiera
 
    nombre_archivo = generarNombreArchivo("xml")
 
    with open(nombre_archivo, mode="w", encoding="utf-8") as archivo:
        archivo.write('<?xml version="1.0" encoding="utf-8"?>\n')
        archivo.write(xml_formateado)
 
    ruta = os.path.abspath(nombre_archivo)
    messagebox.showinfo("Exportado", f"Archivo XML generado exitosamente:\n{ruta}")


btn_exportarXml = tk.Button(ventana, text="Exportar xml", font=("Arial",12, "bold"), bg="white", fg="black", command=exportarXml)
btn_exportarXml.grid(row=4, column=2,padx=10, pady=5 )

def ejecutarBackup():
    grupos = list(Grupos.find())
 
    if not grupos:
        messagebox.showwarning("Atención", "No hay grupos para respaldar.")
        return
 
    # Crear carpeta backups/ si no existe
    carpeta_backup = "C:\Backup_Mongo\Backups_Grupos"
    os.makedirs(carpeta_backup, exist_ok=True)
 
    # Subcarpeta con timestamp para este backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    subcarpeta = os.path.join(carpeta_backup, f"backup_{timestamp}")
    os.makedirs(subcarpeta)
 
    # Convertir ObjectId a string
    for grupo in grupos:
        grupo["_id"] = str(grupo["_id"])
 
    # Guardar como JSON dentro de la subcarpeta
    ruta_archivo = os.path.join(subcarpeta, "grupos.json")
    with open(ruta_archivo, mode="w", encoding="utf-8") as archivo:
        json.dump(grupos, archivo, ensure_ascii=False, indent=4)
 
    ruta = os.path.abspath(subcarpeta)
    messagebox.showinfo("Backup exitoso", f"Backup realizado correctamente.\nUbicación:\n{ruta}")
 
 
btn_backup = tk.Button(ventana, text="Ejecutar Backup", font=("Arial",12, "bold"), bg="white", fg="black", command=ejecutarBackup)
btn_backup.grid(row=6, column=0, columnspan=3, sticky="we", padx=10, pady=5)

ventana.mainloop()