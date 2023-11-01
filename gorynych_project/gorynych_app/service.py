import random
from .models import Word
from django.contrib.auth.mixins import LoginRequiredMixin

consonant_letters = ["Б", "В", "Г", "Д", "К", "Л", "М", "Н", "П", "Р", "С", "Т"]
vowel_letters = ["А", "Е", "И", "О", "Я"]
rare_letters = ["Ф", "Х", "Ц", "Ч", "Ж", "З", "Ю", "У"]
the_rarest = ["Й", "Щ", "Ь", "Ё", "Ы", "Э", "Ш"]


def comp_words():
    """ Возвращает перемешанный список слов из БД """
    res = [i.word for i in Word.objects.all()]
    random.shuffle(res)
    return res


class Words(LoginRequiredMixin):
    raise_exception = True

    def __init__(self):
        self.deck = random.sample(consonant_letters, 6) + random.sample(vowel_letters, 3) \
                    + random.sample(rare_letters, 1) + random.sample(the_rarest, 1)
        self.number_user = 3
        self.number_comp = 3
        self.players_word_list = []
        self.comp_word_list = []
        self.final_comp_word_list = []
        self.temp = 0
        self.gorynych_user = []
        self.gorynych_comp = []

    def checking_for_all_letters(self, w: str):
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
        sum_letters = sum(dict_of_letters.values())
        count_letters = len(dict_of_letters)
        if self.number_user == 0 and sum_letters > count_letters:
            return 'Горыныч без голов'
        if self.number_user < sum_letters - count_letters:
            return 'Для этого слова не хватает голов у Горыныча'
        else:
            self.number_user -= sum_letters - count_letters
            if sum_letters - count_letters != 0:
                self.gorynych_user.append(w)
            self.temp = sum_letters - count_letters
        self.players_word_list.append(w)

    def words_of_comp(self):
        """ Первая проверка слова компьютера """
        for word in comp_words():
            for letter in word.upper():
                if letter not in self.deck:
                    break
            else:
                self.comp_word_list.append(word.upper())

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
            self.final_comp_word_list.append(word)

    def who_won(self):
        """ Определяет победителя """
        if len(self.players_word_list) < len(self.final_comp_word_list):
            return 'Вы проиграли'
        if len(self.players_word_list) == len(self.final_comp_word_list):
            return 'Ничья'
        return 'Вы победили!'
