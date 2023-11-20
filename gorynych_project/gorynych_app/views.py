from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from .forms import UserRegForm, UserLoginForm
from .models import UserGame
from .service import Words, get_rec
from django.contrib import messages
import pickle


def index(request):
    try:
        # Получаем запись по id игрока
        games = UserGame.objects.get(user_id=User.objects.get(username=request.user).id)
        # Десериализуем состояние игры игрока из БД
        game = pickle.loads(games.game)
    except ObjectDoesNotExist:
        # Если игрок не авторизован, то отправляется на страницу авторизации
        return redirect('login')
    context = {'game': game}
    if request.method == 'POST' and 'add' in request.POST:
        # При нажатии ДОБАВИТЬ
        word = request.POST.get('word').upper()
        res = game.checking_for_all_letters(word)
        new_context = {'res': res} | context
        # обновляем состояние игры в БД
        games.game = pickle.dumps(game)
        games.save()
        return render(request, 'gorynych_app/index.html', context=new_context)
    if request.method == 'POST' and 'cancel' in request.POST:
        # При нажатии УБРАТЬ
        # Убрать голову Горыныча если удалил 20-е слово, за которое ее дали
        if len(game.players_word_list) % 20 == 0:
            game.number_user += game.temp
            game.players_word_list.pop()
            if game.number_user > 0:
                game.number_user -= 1
            game.temp = 0
        elif len(game.players_word_list) >= 1:
            if len(game.players_word_list[-1]) > 5 and len(game.players_word_list[-1]) == len(set(game.players_word_list[-1])):
                if game.number_user > 0:
                    game.number_user -= 1
            game.number_user += game.temp  # Возврат Горыныча при отмене слова
            game.players_word_list.pop()
            game.temp = 0
        # обновляем состояние игры в БД
        games.game = pickle.dumps(game)
        games.save()
    if request.method == 'POST' and 'count' in request.POST:
        res = f'Количество ваших слов: {len(game.players_word_list)}'
        new_context = {'res': res} | context
        return render(request, 'gorynych_app/index.html', context=new_context)
    if request.method == 'POST' and 'check' in request.POST:
        game.words_of_comp()
        game.check_words_of_comp()
        count_new_words_for_comp = len(game.final_comp_word_list) // 20
        while len(game.all_gorynych_comp()) > 0 and count_new_words_for_comp > 0:
            new_word = game.all_gorynych_comp().pop()
            game.gorynych_comp.append(new_word)
            game.final_comp_word_list.add(new_word)
            count_new_words_for_comp -= 1
        return render(request, 'gorynych_app/final.html', context=context)
    if request.method == 'POST' and 'end' in request.POST:
        game.save_rec()
        # Получаем запись
        games = UserGame.objects.get(user_id=User.objects.get(username=request.user).id)
        # Удаляем запись
        games.delete()
        # Создаем новую запись
        UserGame.objects.create(game=pickle.dumps(Words()), user_id=User.objects.get(username=request.user).id)
        return redirect('index')
    if request.method == 'POST' and 'doc' in request.POST:
        return render(request, 'gorynych_app/rules.html', context=context)
    if request.method == 'POST' and 'logout' in request.POST:
        user_logout(request)
        return redirect('login')
    if request.method == 'POST' and 'rec' in request.POST:
        new_context = {'get_rec': get_rec} | context
        return render(request, 'gorynych_app/rec.html', context=new_context)
    return render(request, 'gorynych_app/index.html', context=context)


def register(request):
    if request.method == 'POST':
        form = UserRegForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            print(user)
            messages.success(request, 'Успешная регистрация')
            UserGame.objects.create(game=pickle.dumps(Words()), user_id=User.objects.get(username=user).id)
            return redirect('index')
        else:
            messages.error(request, 'Что-то пошло не так')
    else:
        form = UserRegForm()
    context = {'form': form}
    return render(request, 'gorynych_app/register.html', context=context)


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'gorynych_app/login.html', context=context)


def user_logout(request):
    logout(request)
    return redirect('login')
