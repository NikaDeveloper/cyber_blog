from django.core.exceptions import ValidationError
from datetime import date
import re


class DigitValidator:
    """ Валидатор для проверки наличия хотя бы одной цифры в пароле """
    @staticmethod
    def validate(password, user=None):
        if not re.search(r'\d', password):
            raise ValidationError(
                "Пароль должен содержать хотя бы одну цифру",
                code='password_no_digits',
            )
    @staticmethod
    def get_help_text():
        return "Ваш пароль должен содержать хотя бы одну цифру"


def validate_email_domain(value):
    """ Проверяет, что email зарегистрирован на разрешенных доменах """
    allowed_domains = ['mail.ru', 'yandex.ru']
    domain = value.split('@')[-1]
    if domain not in allowed_domains:
        raise ValidationError(f"Разрешены только домены: {', '.join(allowed_domains)}")


def validate_forbidden_words(value):
    """ Проверяет отсутствие запрещенных слов в заголовке поста """
    forbidden = ['ерунда', 'глупость', 'чепуха']
    for word in forbidden:
        if word in value.lower():
            raise ValidationError(f"Заголовок содержит запрещенное слово: {word}")


def validate_author_age(author):
    """ Проверяет, что возраст автора не менее 18 лет"""
    if not author.birth_date:
        raise ValidationError("У автора должна быть указана дата рождения")

    today = date.today()
    age = today.year - author.birth_date.year - (
        (today.month, today.day) < (author.birth_date.month, author.birth_date.day)
    )

    if age < 18:
        raise ValidationError("Автор поста должен быть старше 18 лет")
