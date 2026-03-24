from pymongo import MongoClient as MC

# Conexión a MongoDB
client = MC("mongodb://localhost:27017/")
db = client["BD_GrupoAlumno"]
Alumnos = db["Alumno"]
Grupos = db["Grupo"]
