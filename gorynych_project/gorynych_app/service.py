import random
from .models import Word

consonant_letters = ["Б", "В", "Г", "Д", "Ж", "З", "Й",
                     "К", "Л", "М", "Н", "П", "Р", "С", "Т",
                     "Ф", "Х", "Ц", "Ч", "Ш", "Щ", "Ъ", "Ь"]
vowel_letters = ["А", "Е", "Ё", "И", "О", "У", "Ы", "Э", "Ю", "Я"]
choosing_a_number = [0, 1, 2, 3]

deck = random.sample(consonant_letters, 8) + random.sample(vowel_letters, 5)
number = random.choice(choosing_a_number)


def comp_words():
    return [i.word for i in Word.objects.all()]


class Words:
    players_word_list = []
    comp_word_list = []
    final_comp_word_list = []
    temp = 0
    gorynych_user = []
    gorynych_comp = []

    def __init__(self, d: list, n: int):
        self.deck = d
        self.number_user = n
        self.number_comp = n

    def checking_for_all_letters(self, w: str):
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
        if w not in self.players_word_list:
            self.players_word_list.append(w)
        else:
            return 'Такое слово уже есть'

    def words_of_comp(self):
        for word in comp_words():
            for letter in word.upper():
                if letter not in self.deck:
                    break
            else:
                self.comp_word_list.append(word.upper())

    def check_words_of_comp(self):
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


game = Words(deck, number)