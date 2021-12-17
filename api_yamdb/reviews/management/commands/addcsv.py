import csv

from django.core.management.base import BaseCommand

from reviews import models
from api_yamdb.settings import STATICFILES_DIRS 


class Command(BaseCommand):
    """Записывает в базу данных sqlite из csv-файлов."""
    
    help = 'Writes to sqlite database from csv files.'
    
    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        # Соответствие имён файлов csv названиям таблиц БД
        # Conformity csv-file names to database table names
        CSV_TO_SQL = {
            'users.csv': models.User,
            'category.csv': models.Category,
            'genre.csv': models.Genre,
            'review.csv': models.Review,       
            'titles.csv': models.Title,
            'comments.csv': models.Comment,
            'genre_title.csv': models.Genre_title,
        }
 
        for name in CSV_TO_SQL:
            print(name, end=' ')
            location_csv = STATICFILES_DIRS[0] + 'data/' + name
            with open(location_csv, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                base = CSV_TO_SQL[name]
                for row in csv_reader:
                    base.objects.get_or_create(**row)
            print(' -- filled')
