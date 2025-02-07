from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import pikepdf
import os
from flask import Flask, jsonify
import threading

TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

app = Flask(__name__)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Kirimkan file PDF yang ingin Anda kompres.')

def compress_pdf(file_path: str) -> str:
    output_path = 'compressed_' + os.path.basename(file_path)
    # Menggunakan pikepdf untuk mengompres PDF
    with pikepdf.open(file_path) as pdf:
        pdf.save(output_path, compress_streams=True)
    return output_path

def handle_document(update: Update, context: CallbackContext) -> None:
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

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.document.mime_type("application/pdf"), handle_document))

    updater.start_polling()

    # Start the Flask app in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

if __name__ == '__main__':
    main()
