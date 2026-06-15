from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
import on

TOKEN = os.getenv "8619693580:AAEUH8qwj056kRr6gL5fl5whDYeUzRvq-a0"

ADMIN_CHAT_ID = 6345498497

esperando_solicitud = set()

def cargar_catalogo():
    catalogo = []

    try:
        with open("catalogo.csv", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)

            for fila in lector:
                catalogo.append(fila)

    except:
        pass

    return catalogo

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    teclado = [
        ["🎬 Películas", "📺 Series"],
        ["🎌 Anime", "🇰🇷 Doramas"],
        ["📚 Comics", "📖 Mangas"],
        ["🎮 Juegos", "📝 Solicitar"]
    ]

    markup = ReplyKeyboardMarkup(
        teclado,
        resize_keyboard=True
    )

    await update.message.reply_text(
        "Bienvenido a Stickman 🎬",
        reply_markup=markup
    )

async def buscar(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) == 0:
        await update.message.reply_text(
            "Uso: /buscar nombre"
        )
        return

    consulta = " ".join(context.args).lower()

    catalogo = cargar_catalogo()

    resultados = []

    for item in catalogo:
        if consulta in item["titulo"].lower():
            resultados.append(
                f"🎬 {item['titulo']} ({item['año']})"
            )

    if resultados:
        await update.message.reply_text(
            "\n".join(resultados)
        )
    else:
        await update.message.reply_text(
            "No encontrado."
        )

async def solicitar(update: Update, context: ContextTypes.DEFAULT_TYPE):

    esperando_solicitud.add(update.effective_user.id)

    await update.message.reply_text(
        "Escribe el contenido que deseas solicitar."
    )

async def mensajes(update: Update, context: ContextTypes.DEFAULT_TYPE):

    usuario = update.effective_user

    if usuario.id in esperando_solicitud:

        texto = update.message.text

        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=(
                f"📨 Nueva solicitud\n\n"
                f"Usuario: @{usuario.username}\n"
                f"ID: {usuario.id}\n\n"
                f"Contenido:\n{texto}"
            )
        )

        esperando_solicitud.remove(usuario.id)

        await update.message.reply_text(
            "Solicitud enviada correctamente."
        )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("buscar", buscar))
app.add_handler(CommandHandler("solicitar", solicitar))

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        mensajes
    )
)

print("Stickman iniciado...")

app.run_polling(
    drop_pending_updates=True,
    allowed_updates=None
)
