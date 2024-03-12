from django.shortcuts import render, HttpResponse
from .models import *
import telebot
import wikipedia
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.views.decorators.http import require_POST


def home(context):
    return HttpResponse("Salom Dunyo!!!")



BOT_TOKEN = '6719577695:AAGtoIx7smO8T-fDsPHDgQ3AxDeNL1lzOSc'
WEBHOOK_URL = 'https://7f78-84-54-86-60.ngrok-free.app/webhook/'

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Wiki App ga xush kelibsiz!!!\nNima haqida malumot olmoqchisiz?")

@bot.message_handler(func=lambda message: True)
def search_wikipedia(message):
    wikipedia.set_lang("uz")
    search_query = message.text
    try:
        search_results = wikipedia.search(search_query)
        if search_results:
            page = wikipedia.page(search_results[0])
            summary = page.summary
            images = page.images
            response = f"{page.title}\n\n{summary}"
            bot.reply_to(message, response, parse_mode='HTML')
            if images:
                bot.send_message(message.chat.id, "Bu yerda bu mavzuga doir bazi rasmlar bor:")
                for image in images[:3]:
                    try:
                        bot.send_photo(message.chat.id, image)
                    except Exception as e:
                        print(f"Rasm chiqazishda xatolik yuzaga keldi: {e}")
        else:
            bot.reply_to(message, "Hech narsa topilmadi!")
    except wikipedia.exceptions.DisambiguationError as e:
        options = e.options
        bot.reply_to(message, f"Bu bo'yicha bir nechta natijalar topildi. Iltimos tanlang: {', '.join(options)}")
    except wikipedia.exceptions.PageError:
        bot.reply_to(message, "Hech narsa topilmadi!")
    except Exception as e:
        print(f"Hatolik chiqdi: {e}")

@require_POST
@csrf_exempt
def webhook(request):
    update = telebot.types.Update.de_json(request.body.decode('utf-8'))
    bot.process_new_updates([update])
    return JsonResponse({'status': 'ok'})

def set_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)

def remove_webhook(request):
    bot.remove_webhook()
    return JsonResponse({'status': 'ok'})

def home(request):
    return HttpResponse('Wiki App')


set_webhook()