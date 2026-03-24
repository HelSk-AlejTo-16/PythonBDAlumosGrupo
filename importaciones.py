import csv
import json
import xml.etree.ElementTree as ET
from tkinter import filedialog, messagebox
from db import Grupos

# Importar CSV
def importarCsv():
    # Abre la ventana para seleccionar el archivo
    ruta_archivo = filedialog.askopenfilename(
        title="Seleccionar archivo CSV",
        filetypes=(("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*"))
    )
    
    if not ruta_archivo:
        return # Si el usuario cancela, no hace nada

    try:
        agregados = 0
        with open(ruta_archivo, mode="r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                if "cveGru" in fila and "nomGru" in fila:
                    # Validar que la clave no exista ya en la BD para evitar duplicados
                    if not Grupos.find_one({"cveGru": fila["cveGru"]}):
                        Grupos.insert_one({"cveGru": fila["cveGru"], "nomGru": fila["nomGru"]})
                        agregados += 1
                        
        messagebox.showinfo("Importación Exitosa", f"Se importaron {agregados} grupos desde el CSV.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al importar el CSV: {e}")


# Importar JSON
def importarJson():
    ruta_archivo = filedialog.askopenfilename(
        title="Seleccionar archivo JSON",
        filetypes=(("Archivos JSON", "*.json"), ("Todos los archivos", "*.*"))
    )
    
    if not ruta_archivo:
        return

    try:
        agregados = 0
        with open(ruta_archivo, mode="r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
            for grupo in datos:
                cve = grupo.get("cveGru")
                nom = grupo.get("nomGru")
                
                if cve and nom:
                    if not Grupos.find_one({"cveGru": cve}):
                        Grupos.insert_one({"cveGru": cve, "nomGru": nom})
                        agregados += 1
                        
        messagebox.showinfo("Importación Exitosa", f"Se importaron {agregados} grupos desde el JSON.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al importar el JSON: {e}")


# Importar XML
def importarXml():
    ruta_archivo = filedialog.askopenfilename(
        title="Seleccionar archivo XML",
        filetypes=(("Archivos XML", "*.xml"), ("Todos los archivos", "*.*"))
    )
    
    if not ruta_archivo:
        return

    try:
        agregados = 0
        arbol = ET.parse(ruta_archivo)
        raiz = arbol.getroot()

        # Recorrer cada nodo <Grupo>
        for nodo_grupo in raiz.findall("Grupo"):
            cve_nodo = nodo_grupo.find("cveGru")
            nom_nodo = nodo_grupo.find("nomGru")

            if cve_nodo is not None and nom_nodo is not None:
                cve = cve_nodo.text
                nom = nom_nodo.text
                
                if not Grupos.find_one({"cveGru": cve}):
                    Grupos.insert_one({"cveGru": cve, "nomGru": nom})
                    agregados += 1

        messagebox.showinfo("Importación Exitosa", f"Se importaron {agregados} grupos desde el XML.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al importar el XML: {e}")