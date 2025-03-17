import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from home.models import CustomDesign

class Command(BaseCommand):
    help = "Generates a static manifest.json file"

    def handle(self, *args, **kwargs):
        icon = CustomDesign.objects.first()
        icon_url = icon.image.url if icon and icon.image else "/static/default-icon.png"

        manifest_data = {
            "name": "EricPrint",
            "short_name": "EricPrint",
            "start_url": "/",
            "display": "standalone",
            "background_color": "#ffffff",
            "theme_color": "#b6c816",
            "icons": [
                {"src": icon_url, "sizes": "192x192", "type": "image/png"},
                {"src": icon_url, "sizes": "512x512", "type": "image/png"}
            ]
        }

        manifest_path = os.path.join(settings.BASE_DIR, "static", "manifest.json")
        with open(manifest_path, "w") as f:
            json.dump(manifest_data, f, indent=4)

        self.stdout.write(self.style.SUCCESS(f"✅ Manifest.json has been generated at {manifest_path}"))
