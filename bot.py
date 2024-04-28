import telebot
import openai
import os
import requests
import base64
import json
import random
import string

class ChatBot:
    def __init__(self, telegram_token, openai_token):
        self.telegram_token = telegram_token
        self.openai_token = openai_token
        self.bot = telebot.TeleBot(telegram_token)
        openai.api_key = openai_token

    def start_bot(self):
        @self.bot.message_handler(commands=['start'])
        def send_welcome(message):
            self.bot.reply_to(message, "Cześć, jestem Botem czatu Telegram. Używam OpenAI jako źródła wiedzy. Możesz napisać mi cokolwiek chcesz lub skorzystać z polecenia /image, aby wygenerować obraz na podstawie Twojego opisu.")

        @self.bot.message_handler(commands=['image'])
        def generate_image(message):
            try:
                description = message.text[7:]
                response = openai.Image.create(model="clip-draft", prompt=description, response_format="json")
                image_data = response.choices[0]['content']
                img_data = base64.b64decode(image_data['data'])
                img_file_name = self.get_random_string(10) + '.png'
                
                with open(img_file_name, 'wb') as img_file:
                    img_file.write(img_data)
                    
                self.bot.send_photo(message.chat.id, photo=open(img_file_name, 'rb'))
                
                os.remove(img_file_name)
            except Exception as e:
                self.bot.reply_to(message, "Wystąpił błąd podczas generowania obrazu: " + str(e))

        self.bot.polling()

    def get_random_string(self, length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

if __name__ == "__main__":
    telegram_token = input("Podaj token Bota Telegram: ")
    openai_token = input("Podaj token OpenAI: ")
    
    chat_bot = ChatBot(telegram_token, openai_token)
    chat_bot.start_bot()
