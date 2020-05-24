import os
import pickle # библиотека для сохранения любых типов данных
from datetime import datetime # класс для работы с датой
from time import sleep


class Library:
    def __init__(self):
        self.card_list = []
    # region Карточка
    class Card:
        def __init__(
                self,
                name,
                order_year,
                order_month,
                order_day,
                delivery_year,
                delivery_month,
                delivery_day
        ):
            self.first_name = name
            self.date_order = datetime(
                order_year,
                order_month,
                order_day
            )
            self.date_delivery = datetime(
                delivery_year,
                delivery_month,
                delivery_day
            )
    # endregion
    # region Основные методы
    def init_card(self):
        name = input("Введите фамилию: ")
        print("Введите дату заказа (год месяц день): ")
        while True:
            try:
                date_order = [int(item) for item in input().split()]
                break
            except Exception:
                print('Неверный формат.')
        print("Введите дату доставки (год месяц день): ")
        while True:
            try:
                date_delivery = [int(item) for item in input().split()]
                if date_delivery < date_order:
                    print('Дата заказа не может быть позже даты получения.')
                else:
                    break
            except Exception:
                print('Неверный формат.')
        try:
            return self.Card(name, *date_order, *date_delivery)
        except Exception:
            print('Неверный формат.')
    def is_minimal_order(self):
        try:
            min = self.card_list[0].date_delivery - self.card_list[0].date_order
        except:
            print('Нет карточек')
            return
        for card in self.card_list:
            if card.date_delivery - card.date_order < min:
                min = card.date_delivery - card.date_order
        return min.days
    def is_unready_orders(self):
        counter = 0
        for card in self.card_list:
            if card.date_delivery > datetime.now():
                counter += 1
        return counter
    def is_reading_most(self):
        if len(self.card_list) != 0:
            readers = {}
            for new_card in self.card_list:
                if new_card in readers:
                    readers[new_card.first_name] += 1
                else:
                    readers[new_card.first_name] = 1
            max_val = max(readers.values())
            return({k: v for k, v in readers.items() if v == max_val})
        else:
            print('Нет карточек')
    def is_delivery_in_1990(self):
        card_owner = []
        for card in self.card_list:
            if card.date_delivery == datetime(1990, 9, 15):
                card_owner.append(card.first_name)
        if len(card_owner) != 0:
            return(card_owner)
        else:
            print('Никто не брал книгу')
    def is_order_in_1990(self):
        readers = {}
        for card in self.card_list:
            if card.date_order == datetime(1990, 4, 25):
                readers[card.first_name] = True
        readers_amount = len(readers)
        return readers_amount
    def save_card_list(self):
        if len(self.card_list) != 0:
            with open(input('Сохранить как: ').strip() + '.pkl', 'wb') as file:
                pickle.dump(self.card_list, file)
        else:
            print('Сохранять нечего.')
    def exctract_card_list(self):
        filename = input("Введите название файла: ") + '.pkl'
        if os.path.exists(filename):
            with open(filename, 'rb') as file:
                self.card_list = pickle.load(file)
        else:
            print('Файл с таким названием отсутствует')
    def menu(self):
        print('┌', " Меню ".center(51, '—'), '┐', sep='')
        print("│ •1 Создать карточку                               │")
        print("│ •2 Самый маленький срок, за который нашли книгу   │")
        print("│ •3 Cколько заказов было неудовлетворено           │")
        print("│ •4 Вывести того, чаще всего берет книги           │")
        print("│ •5 Кто книгу взял 15.09.90                        │")
        print("│ •6 Сколько человек заказывали книги 25.04.90      │")
        print('├', '—' * 51, '┤', sep='')
        print("│ •7 Сохранить список карточек                      │")
        print("│ •8 Загрузить список карточек                      │")
        print('├', '—' * 51, '┤', sep='')
        print("│ •9 Вывести меню                                   │")
        print("│ •10 Вывести все карточки                          │")
        print("│ •0 Выход                                          │")
        print('└', '—' * 51, '┘', sep='')
    # endregion
    # region Меню
    def wtopa(self):
        self.menu()
        while True:
            try:
                try:
                    p = int(input('Введите номер пункта: '))
                except ValueError:
                    print("Введите цифру, а не символ/букву!")
                    continue
                if p == 1:
                    # добавить карточку;
                    add_card = self.init_card()
                    if add_card != None:
                        self.card_list.append(add_card)
                elif p == 2:
                    # найти самый маленький срок, за который нашли книгу.
                    min_order = self.is_minimal_order()
                    if min_order != None:
                        print('Количество дней: ',min_order)
                    print()
                elif p == 3:
                    # сколько заказов было неудовлетворено;
                    print('Количество неудовлетворенных заказов: ', self.is_unready_orders())
                elif p == 4:
                    # кто чаще всего берет книги?;
                    if len(self.card_list) > 0:
                        reader = self.is_reading_most()
                        print(*reader.keys(), '— чаще всего берет книги, их количество: ', *reader.values())
                    else:
                        print('Нет карточек.')
                elif p == 5:
                    # кто книгу взял 15.09.90;
                    if len(self.card_list) > 0:
                        print(*self.is_delivery_in_1990())
                elif p == 6:
                    # сколько человек заказывали книги 25.04.90;
                    print(self.is_order_in_1990(), 'человек заказывал(и) книги 25.04.1990.')
                elif p == 7:
                    # сохранить все карточки;
                    self.save_card_list()
                elif p == 8:
                    # извлечь список карточек из файла;
                    self.exctract_card_list()
                elif p == 9:
                    # вывести меню;
                    self.menu()
                elif p == 10:
                    # вывести все текущие записи;
                    for card in self.card_list:
                        print('Имя: ', card.first_name)
                        print('Дата заказа: ', card.date_order.strftime('%d %m %Y'))
                        print('Дата получения: ', card.date_delivery.strftime('%d %m %Y'))
                        print()
                elif p == 0:
                    # выйти из программы;
                    print("Выход из программы", end='')
                    sleep(0.3)
                    for j in range(3):
                        print('.', end='')
                        sleep(0.25)
                    return
                else:
                    print("Нет такого пункта меню!\n")
                    sleep(1)
            except Exception as e:
                print('Ошибка: ', e)
    # endregion



Library = Library()
Library.wtopa()
