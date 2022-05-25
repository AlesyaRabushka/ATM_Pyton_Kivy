
from kivy.uix.screenmanager import ScreenManager

import re


from mainscreen import MainScreen
from card import Card
from chosen import Chosen
from menuoperations import MenuOperations
from singleton import Singleton
from cardSessions import GiveMoney, GetMoney, ChangePin, Telephone, Currency_transactions
from bankomat import Bankomat



class Controller:
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager
        
        self.balance_screen = ''
        self.death_screen_value = 0

        self.single_t = Singleton()
        self.storage = Bankomat()
        self.storage.set_storage_byn(10000)
        self.storage.set_storage_usd(1000)

        self.pin = 0
        self.card = 0
        self.money = -1
        self.phone_number = ''
        self.last_operation = ''

    def set_pin(self, pin):
        self.pin = pin
    def set_money(self, money):
        self.money = money
    def set_phone_number(self, phone):
        self.phone_number = phone
    def set_last_operation(self, operation):
        self.last_operation = operation


    def get_card_balance_byn(self):
        return str(self.card.get_balance_byn())

    def get_card_balance_usd(self):
        return str(self.card.get_balance_usd())

    def check_pin(self):
        try:
            if int(self.pin) == int(self.card.get_pin()):
                return True
        except:
            self.screen_manager.change_screen('death_screen')


    def check_phone_number(self):
        plus = 0
        full_number = []
        item = ''
        for i in self.phone_number:
            if i == '+':
                plus += 1
                item += i
            else:
                item += i
        full_number.append(item)

        if len(self.phone_number) != 17:
            return False
        elif full_number[0] == '3' and full_number[1] == '7' and full_number[2] == '5':
            return True


    def choose_card(self, number):
        chosen = Chosen()
        if chosen.choose_card(number):
            self.card = Card(chosen.get_chosen())
            self.balance_screen.set_balance(self.get_card_balance_byn(), self.get_card_balance_usd())



    def money_out(self):
        try:
            if self.money == -1:
                return -1
            else:
                give_money = GiveMoney()
                print(self.card.get_balance_byn())
                flag = give_money.money_out(self.card, int(self.money), self.storage, self.single_t, 'BYN', 1)
                self.last_operation = 'Выдача наличных'
                return flag
        except:
            self.screen_manager.change_screen('death_screen')
            return 5

    def money_in(self):
        try:
            if self.money == '':
                return -1
            else:
                get_money = GetMoney()
                get_money.money_in(self.card, int(self.money), self.storage, self.single_t, 'BYN', 1)
                self.last_operation = 'Пополнение средств'
                return flag
        except:
            self.screen_manager.change_screen('death_screen')
            return 5



    def telephone_payment(self,number, money):
        #try:
        telephone = Telephone()
        if not telephone.value_check(self.card,money):
            return False
        else:
            telephone.telephone_pay(self.card, int(money), number, self.storage, self.single_t)
            self.last_operation = 'Пополнение средств телефона'
            return True


        #except:
           # self.screen_manager.change_screen('death_screen')
            #return 5


    def fromBUNtoUSD(self,money):
        try:
            print(self.card.get_balance_byn())
            transaction = Currency_transactions()
            transaction.fromBUNtoUSD(self.card,float(money), 1)
            self.last_operation = 'Перевод средств\n                  BYN->USD'
            print(self.card.get_balance_byn())
        except:
            self.screen_manager.change_screen('death_screen')
            return 5


    def fromUSDtoBUN(self,money):
        try:
            print(self.card.get_balance_byn())
            transaction = Currency_transactions()
            transaction.fromUSDtoBUN(self.card,float(money), 1)
            self.last_operation = 'Перевод средств\n                  USD->BYN'
            print(self.card.get_balance_byn())
        except:
            self.screen_manager.change_screen('death_screen')
            return 5


    def change_pin(self, new_pin):
        try:
            flag = ChangePin.change_card_pin(self.card, self.card.get_pin(), self.single_t, 1, new_pin)
            print(flag)
            return flag
        except:
            self.screen_manager.change_screen('death_screen')
            return 5