import json
import os
import re
import subprocess
import ollama

# Configuracion
MODELO = "llama3.1:8b"
CARPETA = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_KB = os.path.join(CARPETA, "music_kb.pl")
PUENTE = os.path.join(CARPETA, "puente.pl")
ARCHIVO_EJEMPLOS = os.path.join(CARPETA, "ejemplos.pl")
MAX_TURNOS = 3  # cuantas preguntas anteriores recuerda el bot
SIN_INFO = "No tengo esa informacion en mi base de conocimiento."
SIN_RESULTADOS = "No encontre resultados para eso en mi base de conocimiento."
OPCIONES = {"temperature": 0, "num_ctx": 4096}

# Nombres que existen en la base, para que el LLM escriba bien los atomos (queen, dave_grohl...)
def extraer_nombres(ruta):
    with open(ruta, encoding="utf-8") as f:
        texto = f.read()
    bandas = sorted(set(re.findall(r"^banda\((\w+),", texto, re.M)))
    personas = sorted(set(re.findall(r"^miembro\((\w+),", texto, re.M)))
    generos = sorted(set(re.findall(r"^genero\((\w+)\)", texto, re.M)))
    return bandas, personas, generos

# Ejemplos pregunta -> consulta tomados de ejemplos.pl (aparte de la base, para poder editarla libre)
def extraer_ejemplos(ruta):
    ejemplos, titulo = [], ""
    with open(ruta, encoding="utf-8") as f:
        for linea in f:
            if linea.startswith("% ?-"):
                consulta = linea[4:].strip().rstrip(".")
                ejemplos.append(f'{titulo} -> {json.dumps({"consulta": consulta})}')
            elif linea.startswith("% ") and not linea.startswith("%  "):
                titulo = linea[2:].strip()
    return ejemplos

# Paso 1: el LLM traduce la pregunta a una consulta Prolog (NO recibe la base completa)
def crear_instrucciones_traductor():
    bandas, personas, generos = extraer_nombres(ARCHIVO_KB)
    ejemplos = "\n".join(extraer_ejemplos(ARCHIVO_EJEMPLOS))
    assert ejemplos, f"No hay ejemplos en {ARCHIVO_EJEMPLOS}: sin ellos el LLM traduce muy mal"
    return f"""Traduces preguntas sobre musica a UNA consulta de SWI-Prolog.
Responde SOLO con JSON: {{"consulta": "..."}}. Si la pregunta no se puede responder con
estos predicados, responde {{"consulta": ""}}.

PREDICADOS DISPONIBLES:
banda(Banda, Genero, Pais, AnioFormacion, Estado)   % Estado: activa | separada
miembro(Persona, Banda, Rol, Estado)                % Rol: voz, guitarra, bajo, bateria, teclado...; Estado: actual | ex
album(Titulo, Banda, Anio)                          % Titulo es texto entre comillas simples: 'Nevermind'
genero(G). subgenero(Sub, Padre). carrera_solista(Persona). fallecido(Persona).
influyo(Influyente, Influenciado)       % Influyente influyo directamente en Influenciado
influencia(Influyente, Influenciado)    % igual, pero directa o indirecta
anio_actual(A).
SENTIDO DE LAS INFLUENCIAS: nombra la variable segun lo que se pregunta.
  "¿En quien influyo X?", "X influyo a", "¿A quienes influencio X?" -> influyo(x, Influenciado)
  "¿Quien influyo en X?", "¿Quien influencio a X?", "X fue influenciado por" -> influyo(Influyente, x)
NO HAY CANCIONES en la base, solo albumes: si preguntan por canciones o temas, responde {{"consulta": ""}}.
integrante(P, B). miembro_actual(P, B). exmiembro(P, B). exmiembro_vivo(P, B).
toca(P, Rol). pertenece_a(SubGenero, Genero). estilo(Banda, Genero). pais_de(Banda, Pais).
banda_activa(B). banda_separada(B). mismo_pais(A, B). companeros(A, B).
varias_bandas(P). solista_de_banda(P, B).
activa_en_decada(B, Decada). antiguedad(Titulo, Anios). clasico(Titulo).
cantidad_albumes(B, N). trayectoria(B, Anios). reemplazo(Ex, Nuevo, B).
fallecido_de(P, B). banda_superviviente(B). cantante(P).

NOMBRES (usalos tal cual, en minusculas con guion bajo):
Bandas: {", ".join(bandas)}
Personas: {", ".join(personas)}
Generos: {", ".join(generos)}
Paises: chile, argentina, estados_unidos, reino_unido, francia

Reglas:
- Lo que se pregunta va SIEMPRE como variable con nombre en Mayuscula (nunca _); nunca
  escribas tu la respuesta dentro de la consulta.
- Atomos en minuscula con el nombre COMPLETO (john_deacon, no deacon). Sin punto final.
- Usa la consulta mas simple posible. Puedes combinar con coma (,) y usar findall/3, setof/3,
  aggregate_all/3 y \\+.
- Si una banda o persona no esta en la lista, igual escribe su nombre como atomo (ej: coldplay).
- Si la pregunta es de seguimiento ("¿cuales?", "¿y sus albumes?"), usa los nombres que aparecen
  en "Respuesta anterior del bot" o en la pregunta anterior. Ej: si la respuesta anterior fue
  "Alvaro Henriquez estuvo en varias bandas", "¿Cuales?" -> integrante(alvaro_henriquez, B)
- Si la pregunta se entiende sola (aunque se repita), IGNORA la respuesta anterior: no excluyas
  sus resultados con \\=. Solo excluye si el usuario pide "otros" o "mas".

Ejemplos:
¿De que pais es Queen? -> {{"consulta": "pais_de(queen, P)"}}
{ejemplos}
¿Quien es el vocalista de Coldplay? -> {{"consulta": "miembro(P, coldplay, voz, _)"}}
¿Cual es la capital de Francia? -> {{"consulta": ""}}
"""

# Paso 3: el LLM solo redacta la respuesta con los resultados de Prolog
REDACTOR = f"""Redactas respuestas breves en español para un chatbot de musica.
Recibes la pregunta del usuario, la consulta Prolog ejecutada y sus resultados.
Usa UNICAMENTE los resultados: menciona TODOS, sin omitir ninguno, y no agregues datos que
no esten ahi aunque los conozcas.
- "true" significa que si. "false" significa que no, o que no hay ninguno que cumpla lo preguntado.
- El rol "voz" significa que es vocalista (canta); nunca digas "toca la voz".
- Escribe los nombres legibles (dave_grohl -> Dave Grohl, estados_unidos -> Estados Unidos).
Responde solo con el texto de la respuesta."""

TRADUCTOR = {"role": "system", "content": crear_instrucciones_traductor()}
historial = []

def traducir(mensaje):
    # Se envian los ultimos turnos para entender preguntas de seguimiento ("¿y sus albumes?").
    mensajes = [TRADUCTOR]
    for pregunta, consulta, _ in historial[-MAX_TURNOS:]:
        mensajes += [{"role": "user", "content": pregunta},
                     {"role": "assistant", "content": json.dumps({"consulta": consulta})}]
    mensajes.append({"role": "user", "content": mensaje})
    # num_predict corta consultas desbocadas (el modelo a veces genera cientos de condiciones)
    salida = ollama.chat(model=MODELO, messages=mensajes, format="json",
                         options={**OPCIONES, "num_predict": 150})
    try:
        consulta = json.loads(salida["message"]["content"]).get("consulta", "").strip().rstrip(".")
        # El modelo suele escribir "X /= Y" (no existe en Prolog) en vez de "X \= Y"
        return re.sub(r"(?<![=\\])/=", r"\\=", consulta)
    except (json.JSONDecodeError, AttributeError):
        return ""

def atomos_desconocidos(consulta):
    # Atomos de la consulta (no predicados ni textos entre comillas) que no aparecen en la base.
    # Evita responder "no" a algo que la base simplemente no conoce (ej: fallecido(deacon)).
    with open(ARCHIVO_KB, encoding="utf-8") as f:
        palabras_kb = set(re.findall(r"\b[a-z]\w*", f.read()))
    sin_textos = re.sub(r"'[^']*'", "", consulta)
    atomos = re.findall(r"\b[a-z]\w*\b(?!\s*\()", sin_textos)
    return [a for a in atomos if a not in palabras_kb]

# Paso 2: Prolog hace el trabajo pesado
def consultar_prolog(consulta):
    # Devuelve el texto de resultados, o None si la consulta es invalida, insegura o usa nombres desconocidos
    if atomos_desconocidos(consulta):
        return None
    try:
        r = subprocess.run(["swipl", PUENTE, consulta], capture_output=True,
                           text=True, encoding="utf-8", timeout=10)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return r.stdout.strip() if r.returncode == 0 else None

# El LLM de 8B invierte a menudo el sentido de influyo/influencia (al traducir y al redactar).
# Como la pregunta suele dejarlo claro, se corrige en Python, que no se equivoca.
PATRON_INFLUENCIA = r"(influ\w*)\((\w+),\s*(\w+)\)"

def es_variable(termino):
    return termino[0].isupper() or termino[0] == "_"

def corregir_sentido(mensaje, consulta):
    m = mensaje.lower()
    pide_influenciado = re.search(r"en qui[eé]n(es)? influy|influy\w* (a|en) qui[eé]n", m)
    pide_influyente = re.search(r"qui[eé]n(es)? (lo |la |los |las )?influy\w* (en|a)\b", m)
    def girar(g):
        pred, a, b = g.groups()
        if (pide_influenciado and es_variable(a) and not es_variable(b)) or \
           (pide_influyente and es_variable(b) and not es_variable(a)):
            return f"{pred}({b}, {a})"
        return g.group(0)
    return re.sub(PATRON_INFLUENCIA, girar, consulta)

def frases_influencia(consulta, resultados):
    # influyo(nirvana, X) + "X = foo_fighters" -> "nirvana influyo en foo_fighters"
    frases = []
    for linea in resultados.splitlines():
        c = consulta
        for var, valor in re.findall(r"(\w+) = (\S+)", linea):
            c = re.sub(rf"\b{var}\b", valor, c)
        frases += [f"{a} influyo en {b}" for _, a, b in re.findall(PATRON_INFLUENCIA, c)]
    return frases

def redactar(mensaje, consulta, resultados):
    # Indicar la cantidad evita que el modelo omita resultados que "no le suenan"
    n = len(resultados.splitlines())
    contenido = f"Pregunta: {mensaje}\nConsulta: {consulta}\nResultados:\n{resultados}"
    if n > 1:
        contenido += f"\nMenciona los {n} resultados."
    if "voz" in resultados:  # en el system prompt el modelo lo ignoraba
        contenido += '\n"voz" significa que es vocalista (canta); no digas "toca la voz".'
    if "influ" in consulta:  # el modelo invertia el sentido: se le da la frase ya armada
        contenido += "\nEs decir: " + "; ".join(frases_influencia(consulta, resultados))
    salida = ollama.chat(model=MODELO, options=OPCIONES, messages=[
        {"role": "system", "content": REDACTOR},
        {"role": "user", "content": contenido}])
    return salida["message"]["content"].strip()

# Saludos y despedidas: se responden directo, sin LLM ni Prolog
# shortcut: solo frases exactas; si piden mas variantes, agregarlas aqui
CHARLA = {
    "hola": "¡Hola! Pregúntame sobre bandas, integrantes, álbumes o géneros.",
    "gracias": "¡De nada! ¿Quieres saber algo más de música?",
    "adios": "¡Chao! Gracias por conversar.",
    "chao": "¡Chao! Gracias por conversar.",
    "salir": "¡Chao! Gracias por conversar.",
}
DESPEDIDAS = ("adios", "chao", "salir")

def normalizar(mensaje):
    # "¡Adiós!" -> "adios"
    return mensaje.lower().translate(str.maketrans("áéíóú", "aeiou")).strip(" ¡!¿?.,")

def tiene_variables(consulta):
    # Variables de Prolog (Mayuscula o _), ignorando textos entre comillas como 'Nevermind'
    return bool(re.search(r"\b[A-Z_]", re.sub(r"'[^']*'", "", consulta)))

def es_pregunta_abierta(mensaje):
    # ¿Quien...?, ¿Que...?, ¿Cuantos...? piden un dato, no un si/no
    return bool(re.match(r"\W*(qui[eé]n|qu[eé]|cu[aá]l|cu[aá]nt|d[oó]nde|cu[aá]ndo)", mensaje, re.I))

def responder(mensaje, mostrar_evidencia=False):
    if normalizar(mensaje) in CHARLA:
        return CHARLA[normalizar(mensaje)]
    try:
        # La respuesta anterior va como contexto, para que "¿cuales?" sepa de quien se hablaba
        # (como texto y no como turno de chat: si no, el modelo la imita en vez de traducir)
        # Las respuestas fijas (sin info / sin resultados) no se pasan: el modelo las imitaba y
        # devolvia una consulta vacia en la pregunta siguiente
        anterior = historial[-1][2] if historial else ""
        pregunta = mensaje if anterior in ("", SIN_INFO, SIN_RESULTADOS) else \
            f"(Respuesta anterior del bot: {anterior})\n{mensaje}"
        if historial and normalizar(mensaje) == normalizar(historial[-1][0]):
            # Pregunta repetida (insistencia): misma consulta. El LLM creia que pedian "otras"
            consulta = historial[-1][1]
        else:
            consulta = traducir(pregunta)
        # Pregunta abierta sin variables = el LLM escribio la respuesta de memoria
        # (ej: "¿Quien toca bateria en Queen?" -> toca(roger_taylor, bateria)). Se reintenta una vez.
        if consulta and es_pregunta_abierta(mensaje) and not tiene_variables(consulta):
            consulta = traducir(pregunta + "\n(Lo que se pregunta debe ir como Variable en Mayuscula)")
            if not tiene_variables(consulta):
                consulta = ""
        consulta = corregir_sentido(mensaje, consulta)
        resultados = consultar_prolog(consulta) if consulta else None
        # None = consulta invalida o con nombres que la base no conoce.
        # "false" en una pregunta con variables (¿quienes...?) no se le pasa al LLM: si la consulta
        # estaba mal traducida, el LLM inventaba "ninguno" o un numero ("tienen 12 albumes").
        if resultados is None:
            texto = SIN_INFO
        elif resultados == "false" and tiene_variables(consulta):
            texto = SIN_RESULTADOS
        else:
            # Solo la pregunta actual: con la respuesta anterior incluida, el redactor la repetia
            texto = redactar(mensaje, consulta, resultados)
    except Exception as e:
        return f"Ocurrio un error al consultar el modelo: {e}"

    historial.append((mensaje, consulta, texto))

    if mostrar_evidencia and consulta:
        texto += f"\n   [consulta: {consulta}]"
    return texto

# Bucle del chatbot
def main():
    print("Bot: Hola! Preguntame sobre musica. Escribe 'salir' para terminar.")
    while True:
        mensaje = input("Tu: ").strip()
        if not mensaje:
            continue
        print("Bot:", responder(mensaje, mostrar_evidencia=False))
        if normalizar(mensaje) in DESPEDIDAS:
            break

if __name__ == "__main__":
    main()
