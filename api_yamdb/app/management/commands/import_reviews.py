import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Review, User


class Command(BaseCommand):
    def handle(self, *args, **options):
        if Review.objects.exists():
            print('Файл review.csv уже загружен.')
        with open(
            os.path.join(
                settings.BASE_DIR, 'static/data/review.csv'
            ), newline='', encoding='UTF-8'
        ) as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)
            for row in reader:
                Review.objects.create(
                    title_id=row[1],
                    text=row[2],
                    author=User.objects.get(id=row[3]),
                    score=row[4],
                    pub_date=row[5],
                )
        print(Review.objects.all()[:3])
