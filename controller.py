
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

        self.pin_is_changed = False

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
            return 5


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
        elif self.phone_number[0] == '+' and self.phone_number[1] == '3' and self.phone_number[2] == '7'and self.phone_number[3] == '5':
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
            elif self.money == '0':
                return 6
            else:
                give_money = GiveMoney()
                print(self.card.get_balance_byn())
                flag = give_money.money_out(self.card, int(self.money), self.storage, self.single_t, 'BYN', 1)
                self.last_operation = f'Выдача наличных:\n                  {self.money} BYN'
                self.balance_screen.set_balance(self.card.get_balance_byn(), self.card.get_balance_usd())
                return flag
        except:
            self.screen_manager.change_screen('death_screen')
            return 5

    def money_in(self):
        try:
            if self.money == -1:
                'here <= -1'
                return -1
            elif self.money == '0':
                print('6')
                return 6
            else:
                get_money = GetMoney()

                flag = get_money.money_in(self.card, int(self.money), self.storage, self.single_t, 'BYN', 1)
                self.last_operation = f'Пополнение средств\n                  {self.money} BYN'

                self.balance_screen.set_balance(self.card.get_balance_byn(), self.card.get_balance_usd())

                if flag == 5:
                    self.screen_manager.change_screen('death_screen')
                    return 5
                return flag
        except:
            self.screen_manager.change_screen('death_screen')
            return 5




    def telephone_payment(self,number, money):
        #try:
        telephone = Telephone()
        self.phone_number=number
        if money=="" or int(money) <= 0:
            return 5
        if not self.check_phone_number():
            return 10
        if not telephone.value_check(self.card,money):
            return False
        else:
            telephone.telephone_pay(self.card, int(money), number, self.storage, self.single_t)
            self.last_operation = 'Пополнение средств телефона'
            self.balance_screen.set_balance(self.card.get_balance_byn(), self.card.get_balance_usd())
            return True


        #except:
           # self.screen_manager.change_screen('death_screen')
            #return 5


    def fromBUNtoUSD(self,money):

        print(self.card.get_balance_byn())
        transaction = Currency_transactions()
        if money=="" or int(money) <= 0:
            return 5
        if not transaction.value_check_for_BUNtoUSD(self.card,float(money)):
            return False
        else:
            transaction.fromBUNtoUSD(self.card,float(money), 1)
            self.last_operation = 'Перевод средств\n                  BYN->USD'
            print(self.card.get_balance_byn())
            self.balance_screen.set_balance(self.card.get_balance_byn(), self.card.get_balance_usd())
            return True
        #self.screen_manager.change_screen('death_screen')
        #return 5


    def fromUSDtoBUN(self,money):

        print(self.card.get_balance_byn())
        transaction = Currency_transactions()
        if money=="" or int(money) <= 0:
            return 5
        if not transaction.value_check_for_USDtoBUN(self.card,float(money)):
            return False
        else:
            transaction.fromUSDtoBUN(self.card,float(money), 1)
            self.last_operation = 'Перевод средств\n                  USD->BYN'
            print(self.card.get_balance_byn())
            self.balance_screen.set_balance(self.card.get_balance_byn(), self.card.get_balance_usd())
            return True


    def change_pin(self, new_pin):
        try:
            flag = ChangePin.change_card_pin(self.card, self.card.get_pin(), self.single_t, 1, new_pin)
            print(flag)
            return flag
        except:
            self.screen_manager.change_screen('death_screen')
            return 5