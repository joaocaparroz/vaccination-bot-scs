import logging

from functions import check_need_to_send_message, check_website
from message_functions import send_pushbullet_message, send_telegram_message

logging.basicConfig(level=logging.INFO)


def main():
    vaccine_list = check_website()
    if check_need_to_send_message(vaccine_list, False):
        send_pushbullet_message(vaccine_list)
        send_telegram_message(vaccine_list)
        check_need_to_send_message(vaccine_list)


if __name__ == '__main__':
    main()
