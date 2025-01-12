from django.apps import AppConfig



class NeappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'neapp'
    verbose_name = 'Авторский материал'

    def ready(self):                 #-- мен.
        import neapp.signals         #-- мен.
