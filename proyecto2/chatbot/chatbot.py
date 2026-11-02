import re
import unicodedata
from pyswip import Prolog

#crear un ambiente virtual

prolog = Prolog()
prolog.consult("music_kb.pl")

def normalizar(texto):
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = texto.lower().strip()
    texto = re.sub(r"\s+", "_", texto)
    return texto

def es_atomo_valido(texto):
    return re.fullmatch(r"[a-z0-9_]+", texto) is not None

def bonito(valor):
    s = str(valor)
    if s.islower():
        s = s.replace("_", " ").title()
    return s

def consultar(query):
    try:
        return list(prolog.query(query))
    except Exception as e:
        print(f"[error en Prolog: {e}]")
        return []

def responder(mensaje):
    msg = normalizar(mensaje)

    # Integrantes de
    m = re.search(r"integrantes_de_(.+)", msg)
    if m:
        banda = m.group(1)
        if not es_atomo_valido(banda):
            return "No entendi el nombre de la banda."
        res = consultar(f"miembro_actual(P, {banda})")
        if not res:
            return f"No conozco a {bonito(banda)}"
        personas = ", ".join(bonito(r["P"]) for r in res)
        return f"Los integrantes de {bonito(banda)} tiene: {personas}."


    # Albumes de 
    m = re.search(r"albumes_de_(.+)", msg)
    if m:
        banda = m.group(1)
        if not es_atomo_valido(banda):
            return "No entendi el nombre de la banda."
        res = consultar(f"album(T, {banda}, A)")
        if not res:
            return f"No tengo albumes de {bonito(banda)}."
        albumes = ", ".join(f"{r['T']} ({r['A']})" for r in res)
        return f"Albumes de {bonito(banda)}: {albumes}."

    # Canciones de
    m = re.search(r"canciones_de_(.+)", msg)
    if m:
        banda = m.group(1)
        if not es_atomo_valido(banda):
            return "No entendi el nombre de la banda."
        res = consultar(f"cancion_de(C, {banda})")
        if not res:
            return f"No tengo canciones de {bonito(banda)}."
        canciones = ", ".join(str(r["C"]) for r in res)
        return f"Canciones de {bonito(banda)}: {canciones}."

    # Que genero es
    m = re.search(r"genero_(?:es|de|toca)_(.+)", msg)
    if m:
        banda = m.group(1)
        if not es_atomo_valido(banda):
            return "No entendi el nombre de la banda."
        res = consultar(f"banda({banda}, G, Pais, Anio, _)")
        if not res:
            return f"No conozco a {bonito(banda)}."
        r = res[0]
        return (f"{bonito(banda)} es de {bonito(r['G'])},"
                f"de {bonito(r['Pais'])}, formada en {r['Anio']}.")

    # Estuvo en
    m = re.search(r"(.+)_estuvo_en_(.+)", msg)
    if m:
        persona, banda = m.group(1), m.group(2)
        if not (es_atomo_valido(persona) and es_atomo_valido(banda)):
            return "No entendi la pregunta."
        res = consultar(f"integrante({persona}, {banda})")
        return "Si." if res else "No, o no tengo esa informacion."

    return ("No entendi. Puedes preguntar:\n"
            "  - integrantes de nirvana\n"
            "  - albumes de queen\n"
            "  - canciones de linkin park\n"
            "  - que genero es metallica\n"
            "  - dave grohl estuvo en nirvana?")


def main():
    print("Bot: Hola! Preguntame sobre musica. Escribe 'salir' para terminar.")
    while True:
        mensaje = input("Tu: ")
        if normalizar(mensaje) == "salir":
            print("Bot: Adios!")
            break
        print("Bot:", responder(mensaje))

if __name__ == "__main__":
    main()