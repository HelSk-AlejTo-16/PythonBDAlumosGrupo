import csv
import json
import os
from operaciones import generarNombreArchivo
from db import Grupos
from tkinter import messagebox
import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom


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



def ejecutarBackup():
    grupos = list(Grupos.find())
 
    if not grupos:
        messagebox.showwarning("Atención", "No hay grupos para respaldar.")
        return
 
    # Crear carpeta backups/ si no existe
    carpeta_backup = r"C:\Backup_Mongo\Backups_Grupos"
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