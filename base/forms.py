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

    def __init__(self, *args, **kwargs):
        super(MyUserCreationForm, self).__init__(*args, **kwargs)
        
        self.fields['name'].widget.attrs['placeholder'] = 'Your Name'
        self.fields['username'].widget.attrs['placeholder'] = 'your_username'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'
