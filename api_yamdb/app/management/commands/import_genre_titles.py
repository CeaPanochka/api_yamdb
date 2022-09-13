import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import GenreTitle


class Command(BaseCommand):
    def handle(self, *args, **options):
        if GenreTitle.objects.exists():
            print('Файл genre_title.csv уже загружен.')
        with open(
            os.path.join(
                settings.BASE_DIR, 'static/data/genre_title.csv'
            ), newline=''
        ) as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)
            for row in reader:
                GenreTitle.objects.create(
                    title_id=row[1],
                    genre_id=row[2],
                )
        print(GenreTitle.objects.all()[:3])
