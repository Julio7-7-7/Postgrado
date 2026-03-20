from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def saludar():
  return {"message":"Hola Mundo"}

@app.get("/login")
def login():
  return("Ingrese su usuario y contraseña")