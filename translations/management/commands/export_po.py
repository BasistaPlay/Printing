import os
import polib
from django.core.management.base import BaseCommand
from django.conf import settings
from translations.models import Translation
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Export translations from the database to the respective PO files.'

    def handle(self, *args, **kwargs):
        translations = Translation.objects.exclude(locations='').exclude(source_file='')

        if not translations:
            self.stdout.write(self.style.WARNING(f"No valid translations found."))
            return

        self.stdout.write(self.style.NOTICE(f"Exporting {translations.count()} translations..."))

        grouped_translations = {}
        for translation in translations:
            grouped_translations.setdefault(translation.source_file, []).append(translation)

        for source_file, trans in grouped_translations.items():
            correct_path = os.path.relpath(source_file, start=settings.BASE_DIR)
            po_file_path = os.path.join(settings.BASE_DIR, correct_path.replace('/', os.sep))
            po_dir = os.path.dirname(po_file_path)

            if not os.path.exists(po_dir):
                self.stdout.write(self.style.ERROR(f"Directory does not exist: {po_dir}"))
                continue

            if not os.path.exists(po_file_path):
                self.stdout.write(self.style.ERROR(f"PO file does not exist: {po_file_path}"))
                continue

            self.stdout.write(self.style.NOTICE(f"Found PO file: {po_file_path}"))

            try:
                po = polib.pofile(po_file_path)
                self.stdout.write(self.style.NOTICE(f"Loaded existing PO file: {po_file_path}"))
            except polib.POParseError as e:
                self.stdout.write(self.style.ERROR(f"Error loading PO file: {str(e)}"))
                continue

            existing_entries = {entry.msgid: entry for entry in po}
            msgid_to_translation = {translation.msgid: translation.msgstr for translation in trans}

            for msgid, msgstr in msgid_to_translation.items():
                if msgid in existing_entries:
                    entry = existing_entries[msgid]
                    entry.msgstr = msgstr
                else:
                    self.stdout.write(self.style.WARNING(f"MsgID '{msgid}' not found in {po_file_path}. Skipping."))

            try:
                po.save(po_file_path)
                self.stdout.write(self.style.SUCCESS(f'Successfully updated translations in {po_file_path}.'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error saving PO file: {str(e)}'))

        try:
            call_command('compilemessages')
            self.stdout.write(self.style.SUCCESS('Successfully compiled MO files.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error compiling MO files: {str(e)}'))
