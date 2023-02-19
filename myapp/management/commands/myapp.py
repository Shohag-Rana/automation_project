from django.core.management.base import BaseCommand
from myapp.views import Class1


class Command(BaseCommand, Class1):
    def add_arguments(self, parser):
        parser.add_argument('poll_ids', nargs='+', type=str)

    def handle(self, *args, **options):
        for poll_id in options['poll_ids']:
            print(poll_id)
        obj = Class1()
        return obj.disp_class1()
