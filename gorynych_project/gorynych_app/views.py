from django.shortcuts import render, redirect
from .service import Words


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
    return render(request, 'gorynych_app/index.html', context=context)


game = Words()


def new_game():
    global game
    del game
    game = Words()








