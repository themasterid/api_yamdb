import csv

from django.conf import settings
from django.core.management import BaseCommand
from reviews.models import (Category, Comments, Genre, GenreTitle, Review,
                            Title, User)

TABLES = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comments: 'comments.csv',
    GenreTitle: 'genre_title.csv'
}


class Command(BaseCommand):
    help = 'Загрузка данных из csv файлов'

    def handle(self, *args, **kwargs):
        for model, base in TABLES.items():
            print(model, base)
            with open(
                f'{settings.BASE_DIR}/static/data/{base}',
                'r', encoding='utf-8'
            ) as csv_file:
                reader = csv.DictReader(csv_file)
        self.stdout.write(self.style.SUCCESS('Все данные загружены'))
