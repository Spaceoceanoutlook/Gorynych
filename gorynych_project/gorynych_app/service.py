import random
from .models import Word

consonant_letters = ["Б", "В", "Г", "Д", "Ж", "З", "Й",
                     "К", "Л", "М", "Н", "П", "Р", "С", "Т",
                     "Ф", "Х", "Ц", "Ч", "Ш", "Щ", "Ъ", "Ь"]
vowel_letters = ["А", "Е", "Ё", "И", "О", "У", "Ы", "Э", "Ю", "Я"]
choosing_a_number = [0, 1, 2, 3]

deck = random.sample(consonant_letters, 6) + random.sample(vowel_letters, 4)
number = random.choice(choosing_a_number)


def comp_words():
    return [i.word for i in Word.objects.all()]


class Words:
    players_word_list = []
    comp_word_list = []

    def __init__(self, d, n):
        self.deck = d
        self.number = n

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
        if self.number == 0 and sum_letters > count_letters:
            return 'Горыныч без голов'
        if self.number < sum_letters - count_letters:
            return 'Ваше слово превышает количество голов Горыныча'
        else:
            self.number -= sum_letters - count_letters
        Words.players_word_list.append(w)
        return 'Слово прошло проверку'

    def words_of_comp(self):
        for word in comp_words():
            for letter in word.upper():
                if letter not in self.deck:
                    break
            else:
                self.comp_word_list.append(word.upper())


game = Words(deck, number)
