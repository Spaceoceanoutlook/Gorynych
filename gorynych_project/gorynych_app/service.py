from django.contrib.auth.models import User

from .models import Word, Record
import random

consonant_letters = ["Б", "В", "Г", "Д", "К", "Л", "М", "Н", "П", "Р", "С", "Т"]
vowel_letters = ["А", "Е", "И", "О", "Я"]
rare_letters = ["Ф", "Х", "Ц", "Ч", "Ж", "З", "Ю", "У"]
the_rarest = ["Й", "Щ", "Ь", "Ё", "Ы", "Э", "Ш"]


def get_rec():
    """ Получает список рекордов из БД """
    r = [i.record for i in Record.objects.all()]
    r.sort(reverse=True)
    return r


def comp_words():
    """ Возвращает множество, составленное из слов из БД """
    res = {i.word for i in Word.objects.all()}
    return res


class Words:
    def __init__(self):
        self.deck = random.sample(consonant_letters, 6) + random.sample(vowel_letters, 3) \
                    + random.sample(rare_letters, 1) + random.sample(the_rarest, 1)
        self.number_user = 3
        self.number_comp = 3
        self.players_word_list = []
        self.comp_word_list = set()
        self.final_comp_word_list = set()
        self.temp = 0
        self.gorynych_user = []
        self.gorynych_comp = []

    def checking_for_all_letters(self, w: str):
        w = w.strip()
        """ Проверка слова игрока """
        if w in self.players_word_list:
            return 'Такое слово уже есть'
        dict_of_letters = {}
        for i in w:
            if i not in self.deck:
                return f'Буквы "{i}" нет в колоде'
            elif i not in dict_of_letters:
                dict_of_letters[i] = 1
            else:
                dict_of_letters[i] += 1
        sum_letters = sum(dict_of_letters.values())  # Количество всех символов
        count_letters = len(dict_of_letters)  # Количество уникальных символов
        if self.number_user == 0 and sum_letters > count_letters:
            return 'Горыныч без голов'
        if self.number_user < sum_letters - count_letters:
            return 'Для этого слова не хватает голов у Горыныча'
        else:
            self.temp = sum_letters - count_letters  # Количество использованных голов Горыныча в данном слове
            self.number_user -= self.temp
            if self.temp != 0:
                self.gorynych_user.append(w)
        self.players_word_list.append(w)
        if self.temp == 0:
            if len(w) == 6:
                if self.number_user < 3:
                    self.number_user += 1
                return 'Круто! Держите голову!'
            if len(w) == 7:
                if self.number_user < 3:
                    self.number_user += 1
                return 'Фантастика! Награждаетесь головой!'
            if len(w) > 7:
                if self.number_user < 3:
                    self.number_user += 1
                return 'Невероятно! Такое слово точно существует? Голова уже на месте!'
        if len(self.players_word_list) % 20 == 0 and self.number_user < 3:
            self.number_user += 1
            return 'Вы вернули одну голову'

    def words_of_comp(self):
        """ Первая проверка слова компьютера """
        for word in comp_words():
            for letter in word.upper():
                if letter not in self.deck:
                    break
            else:
                self.comp_word_list.add(word.upper())

    def check_words_of_comp(self):
        """ Вторая проверка слова компьютера """
        for word in self.comp_word_list:
            dict_of_letters_comp = {}
            for letter in word:
                if letter not in dict_of_letters_comp:
                    dict_of_letters_comp[letter] = 1
                else:
                    dict_of_letters_comp[letter] += 1
            sum_letters = sum(dict_of_letters_comp.values())
            count_letters = len(dict_of_letters_comp)
            if self.number_comp == 0 and sum_letters > count_letters:
                continue
            if self.number_comp < sum_letters - count_letters:
                continue
            else:
                self.number_comp -= sum_letters - count_letters
                if sum_letters - count_letters != 0:
                    self.gorynych_comp.append(word)
            self.final_comp_word_list.add(word)

    def who_won(self):
        """ Определяет победителя """
        if len(self.players_word_list) < len(self.final_comp_word_list):
            return 'Вы проиграли'
        if len(self.players_word_list) == len(self.final_comp_word_list):
            return 'Ничья'
        return 'Вы победили!'

    def all_gorynych_comp(self):
        """ Вовращает полный список слов-голов Горыныча """
        set_final = self.final_comp_word_list
        set_first = self.comp_word_list
        all_word = set_first - set_final
        return list(all_word)

    def save_rec(self):
        """ Сохраняет новый рекорд из БД """
        rec = get_rec()
        if len(self.players_word_list) > rec[-1]:
            r = Record.objects.filter(record=rec[-1])[0]
            r.record = len(self.players_word_list)
            r.save()
