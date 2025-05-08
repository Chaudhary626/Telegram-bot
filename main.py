from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio

BOT_TOKEN = "6883253335:AAE2sv_9YU_2hGphOpjZc2Tj-eC-yVxrepc"
CHANNEL_ID = -1002014635765  # Replace with your private channel ID

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    args = context.args

    if not args:
        await update.message.reply_text("Please access this bot using the blog link.")
        return

    episode_code = args[0].lower()

    try:
        messages = await context.bot.get_chat_history(chat_id=CHANNEL_ID, limit=50)
        for msg in messages:
            if msg.caption and episode_code in msg.caption.lower():
                sent_msg = await context.bot.forward_message(
                    chat_id=user.id,
                    from_chat_id=CHANNEL_ID,
                    message_id=msg.message_id
                )
                await asyncio.sleep(3600)
                try:
                    await context.bot.delete_message(chat_id=user.id, message_id=sent_msg.message_id)
                except:
                    pass
                return

        await update.message.reply_text("Sorry, the requested file was not found.")

    except Exception as e:
        await update.message.reply_text("Something went wrong while fetching the file.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
