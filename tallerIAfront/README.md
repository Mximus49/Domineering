# Chatbot de Música — Frontend con Django

## Cómo ejecutarlo (Windows, terminal de VSCode)

Requisitos:
- **Python** instalado.
- **SWI-Prolog** instalado y en el PATH (al instalarlo, marcar "Add swipl to the system PATH"). Se comprueba con `swipl --version`.
- **Ollama** abierto y con el modelo descargado (`ollama pull llama3.1:8b`).

```bash
# Parado en la carpeta "TALLER IA" (donde está manage.py)
cd "C:\UNIVERSIDAD\TALLER IA"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate        # solo la primera vez
python manage.py runserver
```

Abrir http://127.0.0.1:8000/ en el navegador. Para detener: `Ctrl + C`.

## Estructura

```
TALLER IA/
├── chatbot.py          <- el chatbot (LLM traduce -> Prolog responde -> LLM redacta). NO se modificó
├── music_kb.pl         <- base de conocimiento
├── puente.pl           <- ejecuta la consulta en SWI-Prolog
├── ejemplos.pl         <- ejemplos pregunta -> consulta para el LLM
├── manage.py           <- comandos de Django (runserver, migrate...)
├── requirements.txt
├── config/             <- configuración general del proyecto
│   ├── settings.py     <- se agregó "chat" a INSTALLED_APPS e idioma español
│   └── urls.py         <- manda la página principal a la app chat
└── chat/               <- la app del frontend
    ├── urls.py         <- qué dirección ejecuta qué vista
    ├── views.py        <- recibe el mensaje y llama a chatbot.responder()
    ├── templates/chat/index.html   <- la página
    └── static/chat/style.css       <- los estilos
```

## Cómo viaja un mensaje

1. El usuario escribe una pregunta y aprieta **Enviar** (el formulario hace un POST).
2. `config/urls.py` → `chat/urls.py` → función `chat` en `chat/views.py`.
3. La vista llama a `chatbot.responder(mensaje)`: el LLM traduce la pregunta a una consulta Prolog, `puente.pl` la ejecuta con la KB y el LLM redacta la respuesta con esos resultados.
4. La pregunta y la respuesta se guardan en la sesión (`request.session`).
5. La vista redirige a `/` y `render()` dibuja `index.html` con la conversación.

## Conceptos de Django que se usan

- **Proyecto y app**: `config` es la configuración general; `chat` es un módulo con una tarea concreta.
- **URL → Vista → Template**: la URL elige la vista, la vista prepara los datos y el template los muestra.
- **Template**: HTML con `{{ variable }}` para mostrar valores y `{% for %}`, `{% if %}`, `{% url %}` como instrucciones.
- **`{% csrf_token %}`**: obligatorio en todo formulario POST (seguridad). Sin él aparece el error 403.
- **Sesión**: diccionario que Django recuerda por cada navegador. Se guarda en `db.sqlite3`, por eso hay que hacer `migrate`.
- **POST → redirect → GET**: tras procesar el formulario se redirige, así al apretar F5 no se reenvía la pregunta.

## Notas

- El checkbox **Mostrar consulta Prolog** muestra la consulta que se ejecutó (útil para la presentación).
- La memoria del chatbot (`historial` en `chatbot.py`) es una sola para todo el servidor. Para una demo en un computador no importa. El botón **Nueva conversación** la borra junto con el chat en pantalla.
- Si se cambia `chatbot.py` o `music_kb.pl`, el servidor se reinicia solo y toma los cambios.
