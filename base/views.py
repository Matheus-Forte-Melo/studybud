from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages as flash_message # Também tem a classe Messages, prov pra criar mensagens custom mas eu n sei usar, usar doc
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Room, Message, Topic, User
from .forms import RoomForm, UserForm, MyUserCreationForm

# Funções que são executados ao determinada URL ser acessadas
# Queries de base de dados, templates e etc. Pode ser uma classe tambem
# class views são complicadas mas são boas de usar, pesquisar tut futuramente

def userProfile(request, pk):
    request.session['last_url'] = request.path
    user = User.objects.get(id=pk)
    USER_ROOMS = user.room_set.all()
    rooms_filtered = user.room_set.all() # Pega todos os objetos filhos room pertencentes a usuário
    
    
    q = request.GET.get('q', '') 
    messages = user.message_set.filter(room__topic__name__icontains=q)[0:5] # Pega todos os objetos filhos message pertencentes a usuário

    if q != '': # Evita fazer duas queries caso nenhum filtro esteja selecionado
        rooms_filtered = rooms_filtered.filter(Q(topic__name__icontains=q) | Q(name__icontains=q))
        
    #topics = Topic.objects.filter(room__in=USER_ROOMS) # Filtra os valores que estão relacionados com room utilizando o FK
    hash_topic = {}
    for room in USER_ROOMS:
        hash_topic[room.topic.name] = 0    
    
    for room in USER_ROOMS:
        if str(room.topic) in str(hash_topic.keys()):
            hash_topic[str(room.topic)] += 1

    context = {'user': user, 'rooms': rooms_filtered, 'topics': hash_topic, 'chat_messages': messages, 'selected_topic': q}
    return render(request, 'base/partial/profile.html', context=context)

def loginPage(request):
    page = 'login' 

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try: 
            user = User.objects.get(email=email)
        except: 
            flash_message.error(request, f'This email "{email}" is not valid!')
        
        user = authenticate(request, email=email, password=password) # Retorna um obj user que batem com esse usuario
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else: 
            flash_message.error(request, "Credentials incorrect")

    context = {'page': page} # Joga o nome da pagina para dentro do dict
    return render(request, 'base/partial/login_register.html', context=context)


def logoutPage(request):
    logout(request) 
    return redirect('home')

def registerPage(request):
    default_avatar = "https://res.cloudinary.com/dtg2hqefp/image/upload/v1715298617/zfkqmvyxuv2fqy57z5an.svg"
    
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST) 
        # Instanciamos o formulario com os dados enviados no POST
        if form.is_valid():
            user = form.save(commit=False) 
            # Commit do banco desligado, a formação será salva só posteriormente
            user.username = user.username.lower()
            user.email = user.email.lower()
            # Configurando imagem default
            user.avatar = default_avatar
            user.save()
            login(request, user)
            return redirect('home')
        else: 
            flash_message.error(request, 'An error occured during registration') 

    page = 'register'
    context = {'page': page, 'form': form}
    return render(request, 'base/partial/signup.html', context)

def home(request):
    # rooms = Room.objects.all().order_by('-created')
    q = request.GET.get('q', '') 

    if q.startswith("@"):
        rooms = Room.objects.filter(host__username=q[1:])   
    else:
        rooms = Room.objects.filter(
            Q(topic__name__icontains=q) |
            Q(name__icontains=q) 
            ) 

    messages = Message.objects.filter(room__topic__name__icontains=q)[0:8]
    topics = Topic.objects.all()
    request.session['last_url'] = request.path # Fica de oio nisso, se tiver algo dando errado com redirecioamento, isso é o culpado
    
    context = {'rooms':rooms, 'topics': topics, 'room_count': rooms.count(), 'chat_messages': messages, 'selected_topic': q}
    return render(request, 'base/partial/home.html', context=context) 

def room(request, pk): 
    request.session['return_to_room_after_delete'] = request.path
    room = Room.objects.get(id=pk) 
    messages = Message.objects.filter(room_id=pk) # room.message_set.all().order_by('-created')
    participants = room.participants.all() 

    if request.method == "POST":

        Message.objects.create(
            user = request.user, 
            room = room, # Passa a instância para aqui, ele pega o id automaticamente, mas acho que daria para passar o ID
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        
        return redirect('room', pk=pk) 

    context = {'room': room, 'chat_messages': messages, 'participants': participants}
    
    return render(request, 'base/partial/room.html', context=context)


@login_required(login_url='login') 
def createRoom(request):
    form = RoomForm() 

    if request.method == "POST": 
        form = RoomForm(request.POST) 

        if form.is_valid():
            room = form.save(commit=False) # Botamos os dados do formulario para a var (tem q usar o save eu acho) e desligamos o commit para não mandar para o bd ainda
            room.host = request.user # Setamos nossas paradas
            room.save() # E de fatos mandamos para o bd
            flash_message.success(request, "Room created with sucess!")
            return redirect('home') 

    context = {'form':form,'action': 'Create'} 
    return render(request, 'base/global/room_form.html', context=context)

@login_required(login_url='login') 
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)  # Dados pre preenchidos com base no queryset room. Desde que o valores coincidam com os campos
    form.fields['name'].label = 'Room name'

    if request.user != room.host: 
        return HttpResponse("You are not allowed here!")

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room) 
        # Tem que indicar a instância do modelo que estamos editando. Se não tiver isso ele simplesmente vai duplicar 
        if form.is_valid():
            form.save()
            flash_message.success(request, 'Room updated with sucess')
            return(redirect('home'))

    context = {'room': room, 'form': form, 'action': 'Update'}
    return render(request, 'base/global/room_form.html', context=context)

@login_required(login_url='login') 
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host: 
        return HttpResponse("You are not allowed here!")

    if request.method == 'POST':
       room.delete()
       flash_message.success(request, 'Room deleted with sucess')
       return redirect('home')

    return render(request, 'base/partial/delete.html', {'obj':room, 'type': 'room'})

@login_required(login_url='login') 
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    room = message.room.id

    if request.user != message.user: 
        return HttpResponse("You are not allowed here!")

    if request.method == 'POST':
       message.delete()
       flash_message.success(request, 'Message deleted with sucess')
       print(request.session.get('return_to_message_path', '/'))
       return redirect('room', room)

    return render(request, 'base/partial/delete.html', {'obj':message, 'type': 'message'})

@login_required(login_url='login')
def updateProfile(request, pk):
    user = request.user
    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user) 
        # Precisa passar a instance aparentemente, deve ser necessario para ver se ta valido sla
        if form.is_valid():
            form.save()
        return redirect('profile', pk)

    context = {'form': form}
    return render(request, 'base/partial/edit-user.html', context=context)

def mobileActivity(request):
    messages = Message.objects.all()[0:2]

    t = request.GET.get('t', '') 
    q = request.GET.get('q', '') 
    print(q)


    if q and t != '':
        messages = Message.objects.filter(
            Q(user__id=t) &
            Q(room__topic__name=q)
        )[0:2]
    elif q != '':
        messages = Message.objects.filter(room__topic__name__icontains=q)[0:2]
    
    context = {'chat_messages':messages, }
    return render(request, 'base/partial/activity.html', context=context)

def mobileTopic(request):
    
    q = request.GET.get('q', '') # Pra mim procurar aqui dentro
    topics = Topic.objects.filter(name__icontains=q)
    context = {'topics': topics}
    return render(request, 'base/partial/topics.html', context=context)