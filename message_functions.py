import logging
import os

import telegram
from pushbullet import Pushbullet

PUSHBULLET_API_KEY = os.environ['PUSHBULLET_API_KEY']
PUSHBULLET_CHAT_ID = os.environ['PUSHBULLET_CHAT_ID']
TELEGRAM_API_KEY = os.environ['TELEGRAM_API_KEY']
TELEGRAM_CHAT_ID = os.environ['TELEGRAM_CHAT_ID']


def send_pushbullet_message(vaccine_list: list):
    logging.info('Trying to send message to the Pushbullet channel...')
    api_key = PUSHBULLET_API_KEY

    message_to_send = build_message(vaccine_list)
    pb = Pushbullet(api_key)
    vaccine_channel = pb.get_channel(PUSHBULLET_CHAT_ID)
    vaccine_channel.push_note("Novas informações sobre vacina em São Caetano do Sul!", message_to_send)


def build_message(vaccine_list: list):
    message_list = []
    for vaccine in vaccine_list:
        message = ''
        if vaccine['availability']:
            message += 'Disponível'
        else:
            message += 'Indisponível'

        message += f' - {vaccine["age"]} anos ou mais - {vaccine["dose"]}ª dose.'
        message_list.append(message)

    message_list.append('Faça seu agendamento em https://portais.saocaetanodosul.sp.gov.br/sesaud-agendamentos')

    logging.info('Message sent successfully.')
    return '\n'.join(message_list)


def send_telegram_message(vaccine_list: list):
    logging.info('Trying to send message to the Telegram group...')
    bot = telegram.Bot(token=TELEGRAM_API_KEY)
    bot.send_message(text=build_message(vaccine_list), chat_id=int(TELEGRAM_CHAT_ID))
    logging.info('Message sent successfully.')
