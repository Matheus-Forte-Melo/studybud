from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True, unique=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default="avatar.svg")
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name 

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) 
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True) 
    # Se a classe topic tivesse abaixo dessa teria que usar essa referencia entre parenteses
    name = models.CharField(max_length=200) 
    participants = models.ManyToManyField(User, related_name='participants', blank=True) 
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True) 
    created = models.DateTimeField(auto_now_add=True)

    # Metadados 
    class Meta:
        # Seta a ordem do queryset quando fazemos uma query
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name
        # Se fosse um númeo teria que wrappar. Ex int(id)
    
class Message(models.Model): # Mensagem que poderá ser escrita dentro de uma sala
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE) 
    body = models.TextField() # A mensagem em si
    updated = models.DateTimeField(auto_now=True) 
    created = models.DateTimeField(auto_now_add=True) 

    class Meta:
        # Seta a ordem do queryset quando fazemos uma query
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50] 
    

    
    