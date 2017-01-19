# encoding: utf-8
from django.db import models


class User(models.Model):
    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    email = models.EmailField(unique=True, verbose_name='Email')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    birth_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата рождения')

    is_active = models.BooleanField(default=True, verbose_name='Активен?')
    registered = models.DateTimeField(verbose_name='Регистрация', auto_now_add=True)

    def get_short_name(self):
        return self.email

    def get_full_name(self):
        result = ''
        if self.first_name:
            result += self.first_name
        elif self.last_name:
            result += ' ' + self.last_name
        return result

    def __str__(self):
        return self.get_short_name()

    def as_json(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birth_date': self.birth_date,
            'is_active': self.is_active,
            'registered': self.registered,
        }


class Visit(models.Model):
    class Meta:
        verbose_name = 'посещение'
        verbose_name_plural = 'посещения'

    location = models.ForeignKey('Location', verbose_name='Что посещал?')
    user = models.ForeignKey('User', verbose_name='Кто?')
    visited_at = models.DateTimeField(verbose_name='Когда?')

    def __str__(self):
        return 'Посещение ID={}'.format(self.id)

    def as_json(self):
        return {
            'id': self.id,
            'location': str(self.location),
            'user': str(self.user),
            'visited_at': self.visited_at.isoformat(),
        }


class Location(models.Model):
    class Meta:
        verbose_name = 'место'
        verbose_name_plural = 'места'

    country = models.CharField(verbose_name='Страна', max_length=100)
    city = models.CharField(verbose_name='Город', max_length=200, null=True, blank=True)
    place = models.CharField(verbose_name='Название', max_length=255)

    def __str__(self):
        return (self.city or self.country) + ', ' + self.place

    def as_json(self):
        return {
            'id': self.id,
            'country': self.country,
            'city': self.city,
            'place': self.place,
        }
