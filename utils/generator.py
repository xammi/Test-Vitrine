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


users_data = []
locations_data = []


def generate_users(amount):
    emails = []
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
            'birth_date': birth_date.isoformat()
        }
        print(user_data)
        emails.append(email)
        users_data.append(i)


def generate_locations(amount):
    for i in range(amount):
        country = choice(countries)
        city = choice(city_prefix) + choice(city_suffix)
        place = choice(locations)
        location_data = {
            'country': country,
            'city': city.capitalize(),
            'place': place.capitalize(),
        }
        print(location_data)
        locations_data.append(i)


def generate_visitors(amount):
    for i in range(amount):
        location = choice(locations_data)
        user = choice(users_data)
        visited_at = random_date(datetime(year=2000, month=1, day=1), datetime(year=2015, month=1, day=1))
        visit_data = {
            'location': location,
            'user': user,
            'visited_at': visited_at.isoformat(),
        }
        print(visit_data)


if __name__ == '__main__':
    generate_users(10)
    generate_locations(10)
    generate_visitors(10)
