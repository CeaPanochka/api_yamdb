import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Category, Title


class Command(BaseCommand):
    def handle(self, *args, **options):
        if Title.objects.exists():
            print('Файл titles.csv уже загружен.')
        with open(
            os.path.join(
                settings.BASE_DIR, 'static/data/titles.csv'
            ), newline='', encoding='utf-8'
        ) as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)
            for row in reader:
                Title.objects.create(
                    id=row[0],
                    name=row[1],
                    year=row[2],
                    category=Category.objects.get(id=row[3]),
                )
        print(Title.objects.all()[:3])
