from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

class RosettaAdmin(admin.ModelAdmin):
    def rosetta_link(self, request):
        url = reverse("rosetta-home")
        return format_html('<a href="{}">Tulkojumi (Rosetta)</a>', url)

admin.site.register_view('rosetta-link', view=RosettaAdmin, name="rosetta-link")
