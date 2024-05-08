from django.contrib import admin
from .models import Room, Topic, Message, User # Importa o modelo

# Register your models here.
admin.site.register(User)
admin.site.register(Room) # Registra o modelo no site admin do django
admin.site.register(Topic)
admin.site.register(Message)

