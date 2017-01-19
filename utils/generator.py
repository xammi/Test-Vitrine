import requests
from requests.exceptions import ConnectionError
import sys
import json
from datetime import timedelta, datetime
from random import choice, randrange
from utils.constants import *


def translit(seq):
    result = ''
    for symbol in seq:
        result += translate.get(symbol, symbol)
    return result


def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


user_ids = []
location_ids = []
service_route = 'http://127.0.0.1:8000/'


def send_data(route, data):
    try:
        response = requests.post(route, data=data)
        if response.status_code == 200:
            resp_data = json.loads(response.text)
            if resp_data.get('status', '') == 'OK':
                return resp_data.get('data', None)
            else:
                pass
        else:
            pass
    except ConnectionError:
        pass

    sys.stdout.write('E')
    sys.stdout.flush()
    return None


def generate_users(amount):
    emails = []
    users_route = service_route + 'user/'
    sys.stdout.write('\nUsers: ')
    for i in range(amount):
        gender = choice(['m', 'f'])
        if gender == 'm':
            name = choice(male_names)
            surname = choice(surname_prefix) + choice(surname_root) + choice(surname_suffix_male)
        else:
            name = choice(female_names)
            surname = choice(surname_prefix) + choice(surname_root) + choice(surname_suffix_female)

        email = translit(name[0].lower() + '.' + surname) + '@' + choice(email_domen)
        if email in emails:
            email = choice(translate.values()) + email

        birth_date = random_date(datetime(year=1900, month=1, day=1), datetime(year=2010, month=1, day=1))
        user_data = {
            'email': email,
            'first_name': name,
            'last_name': surname.capitalize(),
            'birth_date': birth_date
        }
        resp_data = send_data(users_route, user_data)
        if resp_data and 'id' in resp_data:
            emails.append(email)
            user_ids.append(resp_data['id'])
            if i % 100 == 0:
                sys.stdout.write('+')
                sys.stdout.flush()


def generate_locations(amount):
    sys.stdout.write('\nLocations: ')
    locations_route = service_route + 'location/'
    for i in range(amount):
        country = choice(countries)
        city = choice(city_prefix) + choice(city_suffix)
        place = choice(locations)
        location_data = {
            'country': country,
            'city': city.capitalize(),
            'place': place.capitalize(),
        }
        resp_data = send_data(locations_route, location_data)
        if resp_data and 'id' in resp_data:
            location_ids.append(resp_data['id'])
            if i % 100 == 0:
                sys.stdout.write('+')
                sys.stdout.flush()


def generate_visits(amount):
    sys.stdout.write('\nVisits: ')
    visit_route = service_route + 'visit/'
    for i in range(amount):
        location = choice(location_ids)
        user = choice(user_ids)
        visited_at = random_date(datetime(year=2000, month=1, day=1), datetime(year=2015, month=1, day=1))
        visit_data = {
            'location': location,
            'user': user,
            'visited_at': visited_at,
        }
        resp_data = send_data(visit_route, visit_data)
        if resp_data:
            if i % 1000 == 0:
                sys.stdout.write('+')
                sys.stdout.flush()


if __name__ == '__main__':
    generate_users(10000)
    generate_locations(10000)
    generate_visits(100000)
