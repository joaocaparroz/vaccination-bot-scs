import logging
import re

import joblib
import requests
from bs4 import BeautifulSoup


def check_website():
    logging.info('Extracting data from website...')
    url = 'https://portais.saocaetanodosul.sp.gov.br/sesaud-agendamentos'

    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'html.parser')

    cards = soup.find('div', {'class': 'portalMainContent'}).find('div', {'class': 'card'}).find('div', {
        'class': 'card-body'}).find_all('div', {'class': 'bg-light border rounded'})

    result_list = []

    for card in cards:
        availability = extract_availability(
            card.find('div', {'class': 'row', 'style': 'width:98%;margin-left:auto;margin-right:auto;'}).find(
                'span').text)
        age, dose = extract_age_and_dose(
            card.find('div', {'class': 'row', 'style': 'margin-top:10px;'}).find('h6').text)

        result_list.append({'availability': availability,
                            'age': age,
                            'dose': dose})

    logging.info('Data successfully extracted.')
    return result_list


def extract_availability(availability_string: str) -> bool:
    return bool(re.match(r'.*Disponível.*', availability_string))


def extract_age_and_dose(age_string: str):
    age = re.search(r'(\d{1,2}) anos', age_string)
    if age:
        age_num = int(age.group(1))
    else:
        age_num = None

    dose = re.search(r'(\d)ª Dose', age_string)
    if dose:
        dose_num = int(dose.group(1))
    else:
        dose_num = None

    return age_num, dose_num


def check_need_to_send_message(vaccine_list: list, save: bool = True):
    try:
        old_vaccine_list = joblib.load('ovl.joblib')
    except FileNotFoundError:
        old_vaccine_list = []

    if save:
        joblib.dump(vaccine_list, 'ovl.joblib')

    need = vaccine_list != old_vaccine_list
    if not save:
        logging.info('Need to send a message: %s', need)
    return need
