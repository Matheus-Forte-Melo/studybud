from django.forms import ModelForm
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm 
# ============== Formulario base ==================.
# Transformar modelo em formulário

class RoomForm(ModelForm):
    class Meta: # Fornece Metadados
        model = Room
        fields = '__all__' # Poderia ser uma lista
        exclude = ['host', 'participants'] # Mas podemos deixar alguns itens de forma deste modo

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('email', 'name', 'username', 'bio', 'avatar')
        
class MyUserCreationForm (UserCreationForm):
    class Meta:
        model = User
        fields = ('name', 'username', 'email', 'password1', 'password2')
