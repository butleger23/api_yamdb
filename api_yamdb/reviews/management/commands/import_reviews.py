import csv
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime

from reviews.models import Review, Title


YamdbUser = get_user_model()


class Command(BaseCommand):
    help = 'Import review from csv'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file',
            type=str,
            help='the path to the csv file containing reviews'
        )

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        title = Title.objects.get(pk=row['title_id'])
                        author = YamdbUser.objects.get(pk=row['author'])
                        review = Review(
                            id=row['id'],
                            title=title,
                            text=row['text'],
                            author=author,
                            score=int(row['score']),
                            pub_date=parse_datetime(row['pub_date'])
                        )
                        review.clean()
                        review.save()
                        self.stdout.write(self.style.SUCCESS(
                            f'Successfully added review {review.id}'
                        ))
                    except Title.DoesNotExist:
                        self.stdout.write(self.style.ERROR(
                            f'Title with id {row["title_id"]} doesnot exist'
                        ))
                    except YamdbUser.DoesNotExist:
                        self.stdout.write(self.style.ERROR(
                            f'User with id{row["author"]} not found'
                        ))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(
                            f'failed to add review:{str(e)}'
                        ))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'file [{csv_file}] not found'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occured: {str(e)}'))
