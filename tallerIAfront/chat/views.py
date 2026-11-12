"""
Vistas de la app "chat".

Una vista es una funcion que recibe la peticion del navegador (request)
y devuelve una respuesta (normalmente una pagina HTML).

Aqui NO hay logica del chatbot: solo se llama a responder() de chatbot.py,
que esta en la carpeta principal del proyecto.
"""
from django.shortcuts import redirect, render

import chatbot  # nuestro chatbot (chatbot.py), sin modificaciones

SALUDO = "Hola! Preguntame sobre musica."

EJEMPLOS = [
    "¿Quiénes son los integrantes de Nirvana?",
    "¿Qué álbumes tiene Queen?",
    "¿En quiénes influyeron The Beatles?",
    "¿Quién es el vocalista de Coldplay?",
]


def chat(request):
    # 1) Recuperar la conversacion guardada en la sesion (o empezar una nueva)
    historial = request.session.get("historial", [{"autor": "bot", "texto": SALUDO}])
    evidencia = request.session.get("evidencia", False)

    # 2) Si el usuario envio el formulario, procesar su mensaje
    if request.method == "POST":
        mensaje = request.POST.get("mensaje", "").strip()
        evidencia = "evidencia" in request.POST  # True si el checkbox "Mostrar consulta Prolog" esta marcado
        if mensaje:
            respuesta = chatbot.responder(mensaje, mostrar_evidencia=evidencia)
            historial.append({"autor": "usuario", "texto": mensaje})
            historial.append({"autor": "bot", "texto": respuesta})
            request.session["historial"] = historial
            request.session["evidencia"] = evidencia

        # POST -> redirect -> GET: al recargar (F5) no se reenvia el mensaje
        return redirect("chat")

    # 3) Mostrar la pagina con la conversacion
    contexto = {"historial": historial, "ejemplos": EJEMPLOS, "evidencia": evidencia}
    return render(request, "chat/index.html", contexto)


def reiniciar(request):
    """Borra la conversacion en pantalla y la memoria del bot."""
    if request.method == "POST":
        request.session.pop("historial", None)
        chatbot.historial.clear()  # las preguntas anteriores que recuerda el chatbot
    return redirect("chat")
