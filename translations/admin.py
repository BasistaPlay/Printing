from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from django.core.management import call_command
from .models import Translation

class TranslationAdmin(admin.ModelAdmin):
    list_display = ['msgid', 'msgstr', 'fuzzy']
    search_fields = ['msgid', 'msgstr', 'source_file']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-po/', self.import_po_action, name='import-po'),
            path('export-po/', self.export_po_action, name='export-po'),
        ]
        return custom_urls + urls

    def import_po_action(self, request):
        try:
            call_command('import_po')
            self.message_user(request, "PO failu importēšana veiksmīgi pabeigta.", messages.SUCCESS)
        except Exception as e:
            self.message_user(request, f"Kļūda importējot PO failus: {str(e)}", messages.ERROR)

        return redirect('admin:translations_translation_changelist')  # Pareizais nosaukums

    def export_po_action(self, request):
        try:
            call_command('export_po')
            self.message_user(request, "PO failu eksportēšana veiksmīgi pabeigta.", messages.SUCCESS)
        except Exception as e:
            self.message_user(request, f"Kļūda eksportējot PO failus: {str(e)}", messages.ERROR)

        return redirect('admin:translations_translation_changelist')  # Pareizais nosaukums

admin.site.register(Translation, TranslationAdmin)
