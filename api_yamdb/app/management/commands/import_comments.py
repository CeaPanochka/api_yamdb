import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Comment, User


class Command(BaseCommand):
    def handle(self, *args, **options):
        if Comment.objects.exists():
            print('Файл comments.csv уже загружен.')
        with open(
            os.path.join(
                settings.BASE_DIR, 'static/data/comments.csv'
            ), newline=''
        ) as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)
            for row in reader:
                Comment.objects.create(
                    review_id=row[1],
                    text=row[2],
                    author=User.objects.get(id=row[3]),
                    pub_date=row[4],
                )
        print(Comment.objects.all()[:3])
