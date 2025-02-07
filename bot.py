from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import pikepdf
import os
from flask import Flask, jsonify
import threading

TOKEN = '6239054864:AAGrtQ4d9_lzH0eOrrUEmtAdpFWs8sw7I2c'

app = Flask(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Kirimkan file PDF yang ingin Anda kompres.')

def compress_pdf(file_path):
    output_path = 'compressed_' + os.path.basename(file_path)
    with pikepdf.open(file_path) as pdf:
        pdf.save(output_path, compress_streams=True)
    return output_path

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    file = await document.get_file()
    
    # Specify the local path to download the file
    file_path = os.path.join(os.getcwd(), document.file_name)
    await file.download(file_path)

    compressed_file_path = compress_pdf(file_path)

    with open(compressed_file_path, 'rb') as compressed_file:
        await update.message.reply_document(document=compressed_file)

    os.remove(file_path)
    os.remove(compressed_file_path)

@app.route('/')
def index():
    return jsonify({"message": "Bot is running! by @MzCoder"})

def run_flask():
    app.run(host='0.0.0.0', port=8000)

def main():
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Add handlers directly to the application
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Document.MimeType("application/pdf"), handle_document))

    # Start the bot polling
    application.run_polling()

    # Start the Flask app in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

if __name__ == '__main__':
    main()
