import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        if User.objects.exists():
            print('Файл users.csv уже загружен.')
        with open(
            os.path.join(
                settings.BASE_DIR, 'static/data/users.csv'
            ), newline=''
        ) as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)
            for row in reader:
                User.objects.create(
                    id=row[0],
                    username=row[1],
                    email=row[2],
                    role=row[3],
                    bio=row[4],
                    first_name=row[5],
                    last_name=row[6],
                )
        print(User.objects.all()[:3])
