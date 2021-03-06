from turtle import pos
from django.shortcuts import get_object_or_404, render, redirect
#Rentringir algumas views apenas para usuários logados
from django.contrib.auth.decorators import login_required
#Usando autenticação padrão do django para usuários
from django.contrib.auth import authenticate, login, logout
#Módulo para flash messages
from django.contrib import messages
from .models import Post

# View que exibie todos os posts
def blog(request):
    data = {
        'posts': Post.objects.all()[:5],
        'user': request.user
    }
    return render(request, 'blog.html', data)

#View que renderiza post individual
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

#View que renderiza formulário de inserção dos posts
@login_required(login_url='/login/')
def form_posting(request):
    return render(request, 'form_posting.html')

#View que insere postagens no banco
@login_required(login_url='/login/')
def posting(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        conteudo = request.POST.get('conteudo')
        Post.objects.create(titulo=titulo, descricao=descricao, conteudo=conteudo)
    return redirect('/')

#View que renderiza forumlário de edição de post
@login_required(login_url='/login/')
def render_update_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'update_post.html', {'post': post})

#View que salva alteraçõs no post
@login_required(login_url='/login/')
def update_post(request):
    if request.POST:
        post_id = request.POST.get('id')
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        conteudo = request.POST.get('conteudo')
        post = Post.objects.get(id=post_id)
        post.post_id = post_id
        post.titulo = titulo
        post.descricao = descricao
        post.conteudo = conteudo
        post.save()
    return redirect(f'/post/{post_id}')

#View que excluir evento
@login_required(login_url='/login/')
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('/')
