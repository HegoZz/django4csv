import csv

from django.core.management.base import BaseCommand, CommandError

from api_yamdb.reviews import models


class Command(BaseCommand):
    """Записывает в базу данных sqlite из csv-файлов."""
    
    help = 'Writes to sqlite database from csv files.'
    
    def add_arguments(self, parser):
        parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        # Соответствие имён файлов csv названиям таблиц БД
        # Conformity csv-file names to database table names
        CSV_TO_SQL = {
            'category.csv': models.Category,
            'comments.csv': models.Comment,
            'genre_title': models.Genre_title,
            'genre.csv': models.Genre,
            'review.csv': models.Review,
            'titles.csv': models.Title,
            'users.csv': models.User,
        }
        
        for name in CSV_TO_SQL:
            with open(name, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                base = CSV_TO_SQL[name]

                print(csv_reader[0])


