from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import pikepdf
import os
from flask import Flask, jsonify
import threading

TOKEN = '6239054864:AAGrtQ4d9_lzH0eOrrUEmtAdpFWs8sw7I2c'

app = Flask(__name__)

def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    update.message.reply_text('Kirimkan file PDF yang ingin Anda kompres.')

def compress_pdf(file_path):
    output_path = 'compressed_' + os.path.basename(file_path)
    with pikepdf.open(file_path) as pdf:
        pdf.save(output_path, compress_streams=True)
    return output_path

def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    file = document.get_file()
    file_path = file.download()

    compressed_file_path = compress_pdf(file_path)

    with open(compressed_file_path, 'rb') as compressed_file:
        update.message.reply_document(document=compressed_file)

    os.remove(file_path)
    os.remove(compressed_file_path)

@app.route('/')
def index():
    return jsonify({"message": "Bot is running! by @MzCoder"})

def run_flask():
    app.run(host='0.0.0.0', port=8000)

def main():
    application = ApplicationBuilder().token(TOKEN).build()
    dp = application.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(filters.Document.MimeType("application/pdf"), handle_document))

    application.run_polling()

    # Start the Flask app in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

if __name__ == '__main__':
    main()
