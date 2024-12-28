import csv

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime

from reviews.models import Category, Genre, Title, Review, Comment, GenreTitle
#from users.models import YamdbUser


YamdbUser = get_user_model()

BASE_DIR = 'static/data/'

TASKS = [
    ('users.csv', YamdbUser, {
        'id': int,
        'username': str,
        'email': str,
        'role': str,
        'bio': str,
        'first_name': str,
        'last_name': str
    }, None),

    ('category.csv', Category, {
        'id': int,
        'name': str,
        'slug': str
    }, None),

    ('genre.csv', Genre, {
        'id': int,
        'name': str,
        'slug': str
    }, None),

    ('titles.csv', Title, {
        'id': int,
        'name': str,
        'year': int
    }, {
        'category': (Category, 'id')
    }),

    ('genre_title.csv', GenreTitle, {
        'id': int,
        'title_id': int,
        'genre_id': int
    }, None),

    ('review.csv', Review, {
        'id': int,
        'text': str,
        'score': int,
        'pub_date': parse_datetime,
        'title_id': int,
    }, {
        'author': (YamdbUser, 'id')
    }),

    ('comments.csv', Comment, {
        'id': int,
        'text': str,
        'pub_date': parse_datetime,
        'review_id': int,
    }, {
        'author': (YamdbUser, 'id')
    }),
]


class Command(BaseCommand):
    help = 'Import all data from CSV files located in static/data'

    def handle(self, *args, **kwargs):
        try:
            for file_name, model_class, cast_fields, related_fields in TASKS:
                file_path = f'{BASE_DIR}{file_name}'
                self.import_model(
                    file_path, model_class, cast_fields, related_fields)

            self.stdout.write(self.style.SUCCESS('Successfully imported data'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'An error occurred: {str(e)}'))

    def import_model(self, file_path, model_class, cast_fields, related_fields):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                instances = []
                for row in reader:
                    try:
                        instance = self.general_mapper(
                            row, model_class, cast_fields, related_fields)
                        if instance:
                            instances.append(instance)
                    except Exception as e:
                        self.stderr.write(self.style.ERROR(
                            f'Failed to map row: {row}. Error: {str(e)}'
                        ))
                model_class.objects.bulk_create(instances)
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f'File [{file_path}] not found'))

    def general_mapper(self, row, model_class, cast_fields=None, related_fields=None):
        try:
            instance_data = {}

            if cast_fields:
                for field, cast_func in cast_fields.items():
                    instance_data[field] = cast_func(row[field])

            if related_fields:
                for field, (related_model, lookup_field) in related_fields.items():
                    instance_data[field] = related_model.objects.get(**{lookup_field: row[field]})

            return model_class(**instance_data)
        except KeyError as e:
            raise ValueError(f"Missing field in row: {str(e)}")
        except model_class.DoesNotExist as e:
            raise ValueError(f"Related object does not exist: {str(e)}")
