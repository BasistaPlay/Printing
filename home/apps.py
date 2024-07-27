from django.apps import AppConfig

class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'

    def ready(self):
        from django.template import Engine
        Engine.get_default().template_libraries['icon_tags'] = 'home.templatetags.icon_tags'
