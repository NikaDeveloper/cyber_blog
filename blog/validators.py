from django.core.exceptions import ValidationError
from datetime import date
import re


def validate_password_digits(value):
    if not re.search(r'\d', value):
        raise ValidationError("Пароль должен содержать хотя бы одну цифру")


def validate_email_domain(value):
    allowed_domains = ['mail.ru', 'yandex.ru']
    domain = value.split('@')[-1]
    if domain not in allowed_domains:
        raise ValidationError(f"Разрешены только домены: {', '.join(allowed_domains)}")


def validate_forbidden_words(value):
    forbidden = ['ерунда', 'глупость', 'чепуха']
    for word in forbidden:
        if word in value.lower():
            raise ValidationError(f"Заголовок содержит запрещенное слово: {word}")


def validate_author_age(author):
    if not author.birth_date:
        raise ValidationError("У автора должна быть указана дата рождения")

    today = date.today()
    age = today.year - author.birth_date.year - (
        (today.month, today.day) < (author.birth_date.month, author.birth_date.day)
    )

    if age < 18:
        raise ValidationError("Автор поста должен быть старше 18 лет")
