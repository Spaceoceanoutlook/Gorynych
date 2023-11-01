from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from .forms import UserRegForm, UserLoginForm
from .service import Words
from django.contrib import messages

game = Words()


def index(request):
    context = {'game': game}
    if request.method == 'POST' and 'add' in request.POST:
        word = request.POST.get('word').upper()
        res = game.checking_for_all_letters(word)
        new_context = {'res': res} | context
        return render(request, 'gorynych_app/index.html', context=new_context)
    if request.method == 'POST' and 'cancel' in request.POST:
        if len(game.players_word_list) >= 1:
            game.number_user += game.temp    # Возврат Горыныча при отмене слова
            game.players_word_list.pop()
            game.temp = 0
    if request.method == 'POST' and 'count' in request.POST:
        res = f'Количество ваших слов: {len(game.players_word_list)}'
        new_context = {'res': res} | context
        return render(request, 'gorynych_app/index.html', context=new_context)
    if request.method == 'POST' and 'check' in request.POST:
        game.words_of_comp()
        game.check_words_of_comp()
        return render(request, 'gorynych_app/final.html', context=context)
    if request.method == 'POST' and 'end' in request.POST:
        new_game()
        return redirect('index')
    if request.method == 'POST' and 'doc' in request.POST:
        return render(request, 'gorynych_app/rules.html', context=context)
    if request.method == 'POST' and 'logout' in request.POST:
        user_logout(request)
    return render(request, 'gorynych_app/index.html', context=context)


def new_game():
    global game
    del game
    game = Words()


def register(request):
    if request.method == 'POST':
        form = UserRegForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Успешная регистрация')
            return redirect('index')
        else:
            messages.error(request, 'Что-то пошло не так')
    else:
        form = UserRegForm()
    title = 'Регистрация'
    context = {'form': form, 'title': title}
    return render(request, 'gorynych_app/register.html', context=context)


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            new_game()
            return redirect('index')
    else:
        form = UserLoginForm()
    title = 'Авторизация'
    context = {'form': form, 'title': title}
    return render(request, 'gorynych_app/login.html', context=context)


def user_logout(request):
    logout(request)
    return redirect('login')







