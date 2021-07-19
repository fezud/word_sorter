class Item: # класс для хранения слова и числа его встречаемости в тексте, использую для добавления в массив
    def __init__(self, word, number):
        self.word = word
        self.number = number


class Sorter: #класс, реализующий сортировку словаря
    from collections import Counter
    def __init__(self, word_map, output_order):
        self.word_map = word_map
        self.items_sorted = []
        self.output_order = output_order


    def sorting(self):
        if self.output_order == 1:
            self.__numberOfCharSorting()

        if self.output_order == 2:
            self.__frequencySorting()

        if self.output_order == 3:
            self.__alphabeticalSorting()
        

    def __numberOfCharSorting(self): #здесь и далее функции объявлены как private, чтобы взаимодействие с классом пользователь
#выполнял только посредством вызова метода sorting. Данные приватные функции также возвращают значение, чтобы их можно было использовать внутри класса
        words_unsorted = []

        for word, number in self.word_map.items():
            words_unsorted.append(word)
    
        starting_index = 0
        number_of_char = 1

        words_half_sorted = sorted(words_unsorted, key=len)

        words_sorted = []

        number_of_words = len(words_half_sorted)

        for i in range(0, number_of_words):
            if len(words_half_sorted[i]) > number_of_char and i != (number_of_words-1): #данная проверка проходит в случае, если данное слово - не последнее в массиве
                number_of_char += 1
                wordline = self.__alphabeticalSorting(words_half_sorted[starting_index:i])
                for j in range(0, len(wordline)):
                    words_sorted.append(wordline[j].word)
                starting_index = i
            
            
            if i == (number_of_words-1): #для того, чтобы учесть последнее в массиве слово
                end = number_of_words-1
                if len(words_half_sorted[end]) == len(words_half_sorted[end-1]):
                    i = number_of_words
                else:
                    wordline = self.__alphabeticalSorting(words_half_sorted[starting_index:i])
                    for j in range(0, len(wordline)):
                        words_sorted.append(wordline[j].word)
                    i = number_of_words
                    starting_index = i-1
                wordline = self.__alphabeticalSorting(words_half_sorted[starting_index:i])
                for j in range(0, len(wordline)):
                    words_sorted.append(wordline[j].word)



        words_sorted.reverse()
        self.items_sorted = []

        for i in range(0, len(words_sorted)):
            word = words_sorted[i]
            number = self.word_map[word]
            self.items_sorted.append(Item(word, number))

        return self.items_sorted

    def __frequencySorting(self):
        maximum_number = max(self.word_map.values())
        
        self.items_sorted = []
        for i in range(maximum_number, 0, -1):
            for word, number in self.word_map.items():
                if number == i:
                    self.items_sorted.append(Item(word, number))

        return self.items_sorted
            

    def __alphabeticalSorting(self, words_unsorted=None):
        if words_unsorted is None:
            words_unsorted = []
            for word, number in self.word_map.items():
                words_unsorted.append(word)
        
        words_sorted = sorted(words_unsorted)

        self.items_sorted = []
        
        for i in range(0, len(words_sorted)):
            word = words_sorted[i]
            number = self.word_map[word]
            self.items_sorted.append(Item(word, number))

        return self.items_sorted

    def get_sorted(self):
        return self.items_sorted


class Input: #класс, хранящий в себе строку с исходными данными и имеющий метод считывания этих данных из файла
    import codecs
    def __init__(self, path):
        self.file = self.codecs.open(path, mode='r', encoding='utf-8', errors='strict', buffering=-1)
        self.raw_data = ""

    def reading(self):
        raw_data = self.file.read()
        self.raw_data = raw_data

    def get_data(self):
        return self.raw_data
        
class Output: # выводит уже отсортированные слова
    def __init__(self, items, top):
        self.items = items
        self.top = top

    def print_items(self):
        number_of_prints = min(self.top, len(self.items))
        for i in range(0, number_of_prints):
            print(f'{self.items[i].word}: {self.items[i].number}')



class DataProcessing:
    def words_from_string(raw_data):
        clean_data = raw_data
        words = clean_data.split()
        words = [word.strip('.,!;()[]:-—«»') for word in words] #можно дописать сюда цифры и программа не будет их рассматривать как слова
        words = [word.replace("'s", '') for word in words] #для английского
        return words
    def unique_words_processing(words):
        word_map = dict()
        for word in words:
            if word != '':
                word = word.lower()
                if word in word_map:
                    word_map[word] += 1
                else:
                    word_map[word] = 1
        
        return word_map

class Filter:
    def __init__(self, string_of_data):
        data_split = string_of_data.split('/')
        self.path = data_split[0]
        self.output_order = int(data_split[1])
        self.top = int(data_split[2])
    def get_path(self):
        return self.path
    def get_output_order(self):
        return self.output_order
    def get_top(self):
        return self.top



print("Input path: ", end = '')
path = input()
print("Input output_order: ")
print("'1' for sorting by number of characters, '2' for sorting by frequency of word occurance, '3' for sorting aplhabetically", end=': ')
output_order = int(input())
print("Input top: ", end = '')
top = int(input())
print()
print("Input filter (not required): ", "format is: 'path/output_order/top'")
print("For example for filename 'ex.txt' with alphabetical sorting and listing only top 5 words the filter is 'ex.txt/3/5'")
opt_filter = input()

if opt_filter:
    try:
        filterr = Filter(opt_filter) #т.к. имя filter зарезервировано
        path = filterr.get_path()
        output_order = filterr.get_output_order()
        top = filterr.get_top()
    except:
        print("Unknown formatting")

print()
print()



inp = Input(path)
inp.reading()
processor = DataProcessing

raw_string = inp.get_data()
words = processor.words_from_string(raw_string)
word_map = processor.unique_words_processing(words)


sorter = Sorter(word_map, output_order)

sorter.sorting()

sorted_items = sorter.get_sorted()

out = Output(sorted_items, top)
out.print_items()















