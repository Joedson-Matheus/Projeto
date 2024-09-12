from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from .forms import UserCreationForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

#-------------- REDIRECIONAMENTOS ----------------#

#-------------- PARA PAGINA INICIAL ----------------#
def index(request):
    filmes = Filme.objects.all()
    return render(request, 'index.html', {'filmes': filmes})

#-------------- PARA PAGINA DE LOGIN ----------------#
def page_accontLogin(request):
    return render(request, 'Accont/Login/index.html')

#-------------- PARA PAGINA DE CRIAR CONTA ----------------#
def page_accontCreate(request):
    
    return render(request, 'Accont/Create/index.html')


#-------------- PARA PAGINA HOME ----------------#
def page_home(request):
    if not request.user.is_authenticated:
        return redirect(reverse('page_accontLogin'))

    # Pegue os dados do usuário autenticado
    usuario = request.user
    request.session['id_usuario'] = usuario.id
    filmes = Filme.objects.all()

    # Pode adicionar mais dados se necessário
    context = {
        'usuario': usuario,
        'filmes': filmes
    }

    return render(request, "Home/index.html", context)
    
    
#-------------- PARA PAGINA DE INFORMAÇÕES DO FILME ----------------#
def page_move(request,id):
    
    filme = Filme.objects.get(id=id)
    avaliacoes = Avaliacao.objects.filter(filme=filme)
    request.session['filme_id'] = id

    context = {
        'filme': filme,
        'avaliacoes': avaliacoes
    }
    return render(request, 'ViewMove/index.html', context)
 

#-------------- PARA PAGINA DE PLANOS ----------------#
def page_planos(request):
    planos = Plano.objects.all()
    
    filme_id = request.session.get('filme_id')
    if filme_id:
        filme = Filme.objects.get(id=filme_id)
    else:
        filme = None

    context = {
        'planos': planos,
        'filme': filme
    }

    return render(request, 'Plan/index.html', context)

#-------------- PARA PAGINA DE ATUALIZAR PLANOS ----------------#

def updatePlano(request,id):
    id_user = request.session.get('id_usuario')
    ProfileUser.objects.filter(id=id_user).update(status_assinatura=id)

    return redirect('page_move', id=id) 


#-------------- PARA PAGINA DE PERFIL DO USUARIO ----------------#
def page_profileUser(request):
    if not request.user.is_authenticated:
        return redirect(reverse('page_accontLogin'))
    

    filmes = Filme.objects.filter(criado_por=request.user.id)
    

    context = {
        'usuario': request.user,
        'myfilmes':filmes
    }
    return render(request, 'ProfileUser/index.html',context)

#-------------- PARA PAGINA DE VER USUARIO ----------------#
def page_viewProfileUser(request):
    return render(request,'ViewUser/index.html')

#-------------- VERIFICAÇÕES ----------------#
def run_accontLogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        user = authenticate(request, username=email, password=senha)
        if user is not None:
            login(request, user)
            return redirect(reverse('page_home'))
        else:
            messages.error(request, 'Dados incorretos')
            return render(request, 'Accont/Login/index.html', {'error': 'Dados incorretos'})
    else:
        return render(request, 'Accont/Login/index.html')


def run_CreateAccont(request):
    if request.method == 'POST':
        
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        password = request.POST.get('password')
 
        get_value_basic = Plano.objects.get(nome='Básico')

        # Cria  um novo usuário
        user = ProfileUser.objects.create_user(
            email=email,
            password=password,
            nome=nome,
            sobrenome=sobrenome,
            status_assinatura=get_value_basic
        )
        login(request, user)

        messages.success(request, 'Conta criada com sucesso! Você pode fazer login agora.')
        return redirect(reverse('page_home'))
    else:
        return render(request, 'Accont/Create/index.html')

#-------------- CRIAÇÕES ----------------#
# Aqui você pode adicionar funções para criar novos recursos
@csrf_exempt
def avaliarFilme(request, id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = data.get('title')
            comment = data.get('comment')
            rating = data.get('rating')
            filme = Filme.objects.get(id=id)
            id_user = request.session.get('id_usuario')
            
            # Verifica se o usuário está logado
            if id_user is None:
                return JsonResponse({'error': 'Usuário não autenticado'}, status=401)
            
            # Cria a avaliação
            Avaliacao.objects.create(
                filme=filme,
                usuario_id=id_user,  # Supondo que o campo `usuario` seja um FK para o modelo `User`
                titulo=title,
                comentario=comment,
                nota=rating
            )
            return JsonResponse({'message': 'Avaliação criada com sucesso!'}, status=201)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return redirect('page_move', id=id)

#-------------- MODIFICAÇÕES ----------------#
# Aqui você pode adicionar funções para modificar recursos existentes

#-------------- EXCLUÇÕES ----------------#
# Aqui você pode adicionar funções para excluir recursos existentes
