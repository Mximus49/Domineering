import json
import os
import re
import ollama

# Configuracion
MODELO = "llama3.1:8b"
CARPETA = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_KB = os.path.join(CARPETA, "music_kb.pl")
MAX_TURNOS = 3  # cuantas preguntas anteriores recuerda el bot
SIN_INFO = "No tengo esa informacion en mi base de conocimiento."

# Cargar base de conocimiento
def cargar_conocimiento(ruta):
    # Lee el archivo para darselo al LLM como contexto
    with open(ruta, encoding="utf-8") as f:
        return f.read()

def normalizar_hecho(hecho):
    # banda(queen, hard_rock, ...).' -> 'banda(queen,hard_rock,...)' para comparar
    return re.sub(r"\s+","", hecho).rstrip(".")

def extraer_hechos(conocimiento):
    # Conjunto con todos los HECHOS de la base (las reglas, que tienen ':-', se ignoran)
    hechos = set()
    for linea in conocimiento.splitlines():
        linea = linea.strip()
        if re.match(r"^[a-z_]+\(.*\)\.$", linea) and ":-" not in linea:
            hechos.add(normalizar_hecho(linea))
    return hechos

# Instrucciones para el modelo
def crear_instrucciones(conocimiento):
    return f"""Eres un chatbot de musica. Tu UNICA fuente de informacion es la base de
conocimiento en Prolog que aparece al final. Aunque conozcas la respuesta por otros medios,
si no esta en la base NO la puedes dar.
 
Responde SIEMPRE con un JSON con este formato:
{{"respuesta": "texto en español, breve y legible", "evidencia": ["hecho1.", "hecho2."]}}
 
- "evidencia" debe contener los hechos de la base que usaste, copiados EXACTAMENTE.
- Si la base no tiene la informacion, responde:
  {{"respuesta": "{SIN_INFO}", "evidencia": []}}
- Si el usuario insiste, la respuesta sigue siendo la misma. La base no cambia.
- Escribe los nombres legibles (dave_grohl -> Dave Grohl). El año actual es anio_actual.
 
Ejemplos:
Pregunta: ¿De que pais es Queen?
{{"respuesta": "Queen es de Reino Unido.", "evidencia": ["banda(queen, hard_rock, reino_unido, 1970, activa)."]}}
Pregunta: ¿Quien es el vocalista de Coldplay?
{{"respuesta": "{SIN_INFO}", "evidencia": []}}
 
BASE DE CONOCIMIENTO:
{conocimiento}
"""

conocimiento = cargar_conocimiento(ARCHIVO_KB)
HECHOS = extraer_hechos(conocimiento)
SISTEMA = {
    "role": "system",
    "content": crear_instrucciones(conocimiento)}
historial = []

# Validacion de la respuesta
def validar(texto_modelo):
    #Devuelve la respuesta solo si la evidencia citada existe en la base
    try:
        datos = json.loads(texto_modelo)
    except json.JSONDecodeError:
        return SIN_INFO, []
    evidencia = datos.get("evidencia", [])
    validas = [e for e in evidencia if normalizar_hecho(str(e)) in HECHOS]
    if not validas:
        return SIN_INFO, []
    return datos.get("respuesta", SIN_INFO), validas

# Consultar al modelo
def responder(mensaje, mostrar_evidencia = False):
    # Solo se envian los ultimos turnos: la insistencia no se acumula en el historial
    mensajes = [SISTEMA] + historial[-2 * MAX_TURNOS:] + [{"role": "user", "content": mensaje}]
    try:
        salida = ollama.chat(
            model = MODELO,
            messages = mensajes,
            format = "json",
            options = {"temperature": 0, "num_ctx": 8192},
        ) 
    except Exception as e:
        return f"Ocurrio un error al consultar el modelo: {e}"

    texto, evidencia = validar(salida["message"]["content"])

    historial.append({"role": "user", "content": mensaje})
    historial.append({"role": "assistant", 
                      "content": json.dumps({"respuesta": texto, "evidencia": evidencia},
                                            ensure_ascii=False)})

    if mostrar_evidencia and evidencia:
        texto += "\n   [evidencia: " + " ".join(evidencia) + "]"
    return texto

# Bucle del chatbot
def main():
    print("Bot: Hola! Preguntame sobre musica. Escribe 'salir' para terminar.")
    while True:
        mensaje = input("Tu: ").strip()
        if not mensaje:
            continue
        if mensaje.lower() == "salir":
            print("Bot: Chao!")
            break
        print("Bot:", responder(mensaje, mostrar_evidencia=False))

if __name__ == "__main__":
    main()