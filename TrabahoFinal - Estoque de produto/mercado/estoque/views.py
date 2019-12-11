from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth.models import User
from django.conf import settings
from random import choice
from django import forms
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from .forms import *


@login_required(login_url='/login/')
def index(request):
    return render(request, 'estoque/home.html')


@login_required(login_url='/login/')
def produtos(request):
    if request.method == 'POST':
        form = AddProdutoForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Produto cadastrado com sucesso.')

    form = AddProdutoForm()
    produto_list = Produto.objects.all().order_by("nome").annotate(estoque=Sum('compra__quantidade'))

    return render(request, 'estoque/produtos.html', {'produto_list': produto_list, 'form': form})


@login_required(login_url='/login/')
def compra(request):
    form = CompraLevaProdutosForm()

    if request.method == 'POST':
        form = CompraLevaProdutosForm(request.POST)
       
        if form.is_valid():
            compra = form.save()
            messages.add_message(request, messages.SUCCESS, 'Compra de ' + compra.__str__() + ' efetuada com sucesso.')
        else:
            return redirect('compra')
        form = CompraLevaProdutosForm()
        
    heading = "Comprando produtos"

    return render(request, 'estoque/compra.html', {'form': form})


@login_required(login_url='/login/')
def compra_edit(request, id):
    compra = get_object_or_404(Compra, id=id)
    form = CompraLevaProdutosForm(request.POST or None, instance=compra)
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Compra editada com sucesso.')
        else:
            return redirect('/compra/' + str(id))

    return render(request, 'estoque/compra_edit.html', {'form': form, 'compra': compra})


@login_required(login_url='/login/')
def listagem_compras(request):
    compra_list = Compra.objects.all()
    return render(request, 'estoque/listagem_compras.html', {'compra_list': compra_list})


@login_required(login_url='/login/')
def deletar_compra(request, id):
    compra = get_object_or_404(Compra, id=id)
    descricao_compra = compra.__str__()
    compra.delete()
    messages.add_message(request, messages.SUCCESS, 'Compra de ' + descricao_compra + ' foi apagada com sucesso.')
    return redirect('listagem_compras')


@login_required(login_url='/login/')

def logout(request):
    messages.add_message(request, messages.SUCCESS, 'Logout efetuado com sucesso.')
    auth_logout(request)
    return redirect('login')


def login(request):
    if request.user.is_authenticated:
        messages.add_message(request, messages.WARNING, 'Você já está logado.')
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.add_message(request, messages.SUCCESS, 'Login efetuado com sucesso.')
                return redirect('home')
        
        messages.add_message(request, messages.ERROR, 'A combinação usuário/senha estão incorretos.')

    form = LoginForm(None)
    return render(request, 'estoque/login.html', {'form': form})


def registrar(request):
    
    if request.user.is_authenticated:
        messages.add_message(request, messages.WARNING, 'Você já está logado.')
        return redirect('home')
    
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user_password = form.cleaned_data['password']
            user.set_password(user_password)
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Cadastro efetuado com sucesso.')
            return redirect('login')

        messages.add_message(request, messages.ERROR, 'Opa, algo aconteceu. Talvez você esteja cadastrando um usuário já existente?')
    
    form = UsuarioForm(None)
    return render(request, 'estoque/registrar.html', {"form": form})


def enviar(request):
    email = request.POST.get('email')     
    if (email != None):
        caracters = '0123456789abcdefghijklmnopqrstuvwxyz'
        senha = ''
        for char in range(8):
            senha += choice(caracters)

        usuario = User.objects.get(email = email)        
        usuario.set_password(senha)
        usuario.save()
        subject  = 'Confirmação.'
        message = senha
        email_from = settings.EMAIL_HOST_USER  
        recipient_list=[email]
        
        send_mail(subject, message, email_from, recipient_list)

    return render(request, 'estoque/enviar.html')