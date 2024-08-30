import os
import polib
from django.core.management.base import BaseCommand
from django.conf import settings
from translations.models import Translation
import importlib.util

class Command(BaseCommand):
    help = 'Import PO files from all apps and store translations in the database.'

    def handle(self, *args, **kwargs):
        exclude_dirs = {'venv', '__pycache__'}

        for app in settings.INSTALLED_APPS:
            app_module = importlib.util.find_spec(app)
            if app_module:
                app_path = os.path.dirname(app_module.origin)
            else:
                app_path = os.path.join(settings.BASE_DIR, app.replace('.', '/'))

            locale_dir = os.path.join(app_path, 'locale')

            self.stdout.write(self.style.NOTICE(f"Checking directory: {locale_dir}"))
            if os.path.exists(locale_dir):
                self.stdout.write(self.style.NOTICE(f"Directory exists: {locale_dir}"))
                for root, dirs, files in os.walk(locale_dir):
                    dirs[:] = [d for d in dirs if d not in exclude_dirs]
                    if 'venv' in root:
                        self.stdout.write(self.style.WARNING(f"Skipping directory: {root}"))
                        continue

                    for file in files:
                        if file.endswith('.po'):
                            po_file_path = os.path.join(root, file)
                            relative_path = os.path.relpath(po_file_path, start=app_path)
                            self.stdout.write(self.style.NOTICE(f"Found PO file: {po_file_path}"))
                            self.import_po_file(app, relative_path, po_file_path)
            else:
                self.stdout.write(self.style.WARNING(f"Directory does not exist: {locale_dir}"))

    def import_po_file(self, app, relative_path, po_file_path):
        self.stdout.write(self.style.NOTICE(f"Importing PO file: {po_file_path}"))

        try:
            po = polib.pofile(po_file_path)
            self.stdout.write(self.style.NOTICE(f"Read file: {po_file_path}, Entries count: {len(po)}"))

            for entry in po:
                if not entry.msgid or not entry.msgstr:
                    self.stdout.write(self.style.WARNING(f"Skipping entry with invalid msgid/msgstr: MsgID: {entry.msgid}"))
                    continue

                locations = ', '.join(f"{occ[0]}:{occ[1]}" for occ in entry.occurrences) if entry.occurrences else ''
                if not locations or not relative_path:
                    self.stdout.write(self.style.WARNING(f"Skipping entry with invalid locations/source_file: MsgID: {entry.msgid}"))
                    continue

                translation, created = Translation.objects.get_or_create(
                    msgid=entry.msgid,
                    defaults={
                        'msgstr': entry.msgstr,
                        'locations': locations,
                        'fuzzy': entry.fuzzy,
                        'source_file': f"{app}/{relative_path}",
                    }
                )

                if not created:
                    translation.msgstr = entry.msgstr
                    translation.locations = locations
                    translation.fuzzy = entry.fuzzy
                    translation.source_file = f"{app}/{relative_path}"
                    translation.save()

            self.stdout.write(self.style.SUCCESS(f"Successfully imported {po_file_path}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error processing {po_file_path}: {str(e)}"))
