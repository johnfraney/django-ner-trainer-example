import os
from django.core.management.base import BaseCommand, CommandError
from ner_trainer.models import Phrase


class Command(BaseCommand):
    help = 'Imports phrases from the given file(s), assuming one phrase/line'

    def add_arguments(self, parser):
        parser.add_argument('phrase_file_paths', nargs='+', type=str)

    def handle(self, *args, **options):
        phrase_texts = list(Phrase.objects.values_list('text', flat=True))
        phrases_to_create = []
        for phrase_file_path in options['phrase_file_paths']:
            if not os.path.exists(phrase_file_path):
                raise CommandError('Could not find file "%s"' % phrase_file_path)

            with open(phrase_file_path) as phrase_file:
                for line in phrase_file:
                    if not line in phrase_texts:
                        phrases_to_create.append(Phrase(text=line))
                        phrase_texts.append(line)
        Phrase.objects.bulk_create(phrases_to_create)
        self.stdout.write(self.style.SUCCESS('Added phrases from "%s"' % phrase_file_path))

