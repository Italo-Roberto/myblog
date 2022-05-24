from django.shortcuts import get_object_or_404, render, redirect
#Rentringir algumas views apenas para usuários logados
from django.contrib.auth.decorators import login_required
#Usando autenticação padrão do django para usuários
from django.contrib.auth import authenticate, login, logout
#Módulo para flash messages
from django.contrib import messages
from .models import Post

# Create your views here.
def blog(request):
    data = {
        'posts': Post.objects.all(),
        'user': request.user
    }
    return render(request, 'blog.html', data)

def post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'post.html', {'post': post})

#View que renderiza a view de login
def login_user(request):
    return render(request, 'login.html')

#View que realiza o login
def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            messages.error(request, "Usuário ou senha inválidos, tente novamente!")
    return redirect('/')

#View para sair (logout)
def logout_user(request):
    logout(request)
    return redirect('/')

#Rota que renderiza formulário de inserção dos posts
@login_required(login_url='/login/')
def form_posting(request):
    return render(request, 'form_posting.html')

#Rota que insere postagens no banco
@login_required(login_url='/login/')
def posting(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        imagem = request.POST.get('imagem')
        conteudo = request.POST.get('conteudo')
        link = request.POST.get('link')
        Post.objects.create(titulo=titulo, descricao=descricao, imagem=imagem, conteudo=conteudo, link=link)
    return redirect('/')