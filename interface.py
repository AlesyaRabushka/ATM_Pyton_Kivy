import os
from datetime import datetime

from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty

from kivymd.uix.screen import MDScreen




class WelcomeScreen(MDScreen):
    controller = ObjectProperty()
    def __init__(self, controller, balance, **kw):
        super().__init__(**kw)
        self.controller = controller
        self.balance = balance
        self.pin_count = 0
        self.death_screen_value = self.controller.death_screen_value





    def set_phone_number(self, phone):
        self.controller.set_phone_number(phone)

    def change_widget_text(self, widget, text):
        self.ids.widget.text = text

    def card_operations(self):
        self.controller.set_screen('card operations')

    def choose_card(self, number):
        self.balance.card = self.controller.choose_card(number)









    def telephone_payment(self):
        self.controller.telephone_payment('+375 25 234 10 23',5)

    def fromBUNtoUSD(self):
        self.controller.fromBUNtoUSD()


class PinScreen(MDScreen):
    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller
        self.pin_count = 0

        self.change_pin = False

        self.not_correct = False


    def set_pin(self, pin):
        self.controller.set_pin(pin)

    def change_pin(self):
        self.controller.change_pin()

    def check_pin(self):
        flag = self.controller.check_pin()
        if flag == True:
            #self.ids.pin_label.text = '[color=#3E769B]Верный пин-код[/color]'
            self.ids.pin_label.text = '[color=#3E769B]Введите пин-код\n[/color]'
            self.clean_input()
            return 1
        elif flag == 5:
            self.ids.pin_label.text = '[color=#3E769B]Введите пин-код\n[/color]'
        else:
            self.ids.pin_label.text = '[color=#FF0000]Неверный пин-код!\nПовторите попытку[/color]'
            self.pin_count += 1

        if self.pin_count == 3:
            self.ids.pin_label.text = '[color=#FF0000]Вы израсходовали допустимое количество попыток[/color]'
            self.pin_count = 0
            self.not_correct = True
            return 2


    def set_change_pin(self):
        self.change_pin = True

    def change_screen(self, screen_name):
        if not self.change_pin:
            self.manager.change_screen(screen_name)
        else:
            self.manager.change_screen('change_pin_screen')

    def clean_input(self):
        self.ids.pin_input.text = ''


class MenuScreen(MDScreen):
    def __init__(self, pin_screen, **kwargs):
        super().__init__(**kwargs)
        self.pin_screen = pin_screen

class MoneyOutChoiceScreen(MDScreen):
    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller



    def set_money(self, money):
        if self.controller.set_money(money) == False:
            self.ids.money_out_label.text = '[color=#FF0000]Неверный ввод данных[/color]'
        else:
            #self.ids.money_out_label.text = '[color=#FF9900]okeyy[/color]'
            self.controller.money_out()

    def money_out(self):
        self.controller.money_out()



class MoneyOutScreen(MDScreen):
    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller
        self.death = False
        self.correct = True
        self.correct_set_money = False


    def set_money(self, money):
        self.controller.set_money(money)
            # self.ids.money_out_label.text = '[color=#FF9900]okeyy[/color]'

    def money_out(self):
        flag = self.controller.money_out()
        self.ids.money_out_input.text = ''
        if flag == -1:
            self.correct = False
            self.ids.money_out_label.text = '[color=#FF0000]Неверный формат ввода[/color]'
            return False
        elif flag == 6:
            self.correct = False
            self.ids.money_out_label.text = '[color=#FF0000]Неверный формат ввода[/color]'
            return False
        elif flag == 4 :
            self.ids.money_out_label.text = '[color=#FF0000]Лимит средств превышен[/color]'
            return False
        elif flag == 2:
            self.ids.money_out_label.text = '[color=#FF0000]Недостаточно средств на счете[/color]'
            return False
        elif flag == 3:
            self.ids.money_out_label.text = '[color=#FF0000]Неверный формат ввода[/color]'
            return False
        elif flag == 5:
            self.death = True
        elif flag == True:
            self.ids.money_out_label.text = '[color=#3E769B]Введите сумму выдачи[/color]'
            self.death = False
            self.correct = True
            return True
        else:
            return False



class MoneyInScreen(MDScreen):
    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller
        self.death = False
        self.correct = True


    def set_money(self, money):
        self.controller.set_money(money)

    def money_in(self):
        flag = self.controller.money_in()
        self.ids.money_in_input.text = ''
        if flag == 5:
            self.ids.money_in_label.text = '[color=#3E769B]Введите сумму выдачи[/color]'
            self.death = True
            self.ids.money_in_input.text = ''
            return False
        elif flag == -1:
            self.correct = False
            self.ids.money_in_label.text = '[color=#FF0000]Неверный формат ввода данных[/color]'
            self.ids.money_in_input.text = ''
            return False
        elif flag == 6:
            self.ids.money_in_label.text = '[color=#FF0000]Неверный формат ввода данных[/color]'
            self.ids.money_in_input.text = ''
            return False
        elif flag == True:
            self.ids.money_in_label.text ='[color=#3E769B]Введите сумму[/color]'
            self.death = False
            self.correct = True
            return True
        else:
            self.ids.money_in_label.text = '[color=#FF0000]Неверный формат ввода данных[/color]'
            self.ids.money_in_input.text = ''
            return False


class MoneyOperations(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ChangePinScreen(MDScreen):
    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller
        self.new_pin = ''
        self.death = False

    def set_pin(self, new_pin):
        self.new_pin = new_pin

    def change_pin(self):
        flag =  self.controller.change_pin(self.new_pin)
        if flag == True:
            self.controller.set_last_operation('Смена пин-код')
            return flag
        elif flag == 5:
            self.death = True
        else:
            return flag





class ContinueScreen(MDScreen):
    pass

class CheckScreen(MDScreen):
    """
    Check screen
    """
    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller

    def show_check(self):
        check = ''
        check += '[color=#000000]---------------------------------------------------[/color]\n'
        check += '[color=#000000]                     ЧЕК[/color]\n'
        check += '[color=#000000]---------------------------------------------------[/color]\n'
        date = datetime.now()
        check += '[color=#000000]Date: ' + date.strftime('%d-%m-%Y') + '[/color]\n'
        check += '[color=#000000]Time: ' + date.strftime('%H:%M:%S') +'[/color]\n'
        check += '[color=#000000]---------------------------------------------------[/color]\n'

        check += '[color=#000000]Operation: ' + self.controller.last_operation + '[/color]\n'
        check += '[color=#000000]---------------------------------------------------[/color]\n'

        self.ids.check_label.text = check



class BalanceScreen(MDScreen):
    """
    Card balance screen
    """
    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller


    def set_balance(self, byn, usd):
        print(byn, usd)
        self.ids.balance_byn_label.text = '[color=#FF8C00]' + str(byn) + '[/color]'
        self.ids.balance_usd_label.text = '[color=#FF8C00]' + str(usd) + '[/color]'







class PhoneInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.phone = ''

    def insert_text(self, string, from_undo = False):
        numbers = '1234567890 '
        if string in numbers:
            new_text = self.text + string
            print(self.text)
            print(new_text)
            if len(new_text) != 0:
                if len(new_text) <= 17:
                    if len(new_text) == 4:
                        string += ' '
                        TextInput.insert_text(self, string, from_undo = from_undo)
                    elif len(new_text) == 7:
                        string += ' '
                        TextInput.insert_text(self, string, from_undo=from_undo)
                    elif len(new_text) == 11:
                        string += ' '
                        TextInput.insert_text(self, string, from_undo=from_undo)
                    elif len(new_text) == 14:
                        string += ' '
                        TextInput.insert_text(self, string, from_undo=from_undo)
                    else:
                        TextInput.insert_text(self, string, from_undo=from_undo)


class TelephonePaymentScreen(MDScreen):
    number = ObjectProperty()
    money = ObjectProperty()
    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller
        self.death = False

    def phone_payment(self):
        number = self.ids.number.text
        money = self.ids.money.text
        flag = self.controller.telephone_payment(number, money)
        if flag == 5:
            self.ids.tel_label.text = '[color=#FF0000]Неверная сумма[/color]'
            return False
        elif flag == 10:
            self.ids.tel_label.text = '[color=#FF0000]Неверный номер[/color]'
            return False
        if not flag:
            self.ids.tel_label.text = '[color=#FF0000]Недостаточно средств[/color]'
            return False
        else:
            return True





class PinInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pin = ''

    def insert_text(self, string, from_undo = False):
        new_text = self.text + string
        if new_text != '':
            if len(new_text) <= 4:
                TextInput.insert_text(self, string, from_undo = from_undo)
            # elif len(new_text) == 4:
            #     self.pin = new_text


class CheckChoiceScreen(MDScreen):
    def __init__(self, check_screen, **kw):
        super().__init__(**kw)
        self.check_screen = check_screen

    def check(self):
        self.check_screen.show_check()


class DeathScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.death_label.text = '[color=#FFFFFF]\
         The problem has been detected and windows has been shut down to \n \
        prevent damage to your computer.\n \
        if this is the first time you\'ve seen this stop error screen,\n \
        restart yor computer. If this screen appears again, follow these steps:\n\n \
        check to make sure any new hardware or software is properly installed.\n  \
        If this is a new installation, asl your hardware or software manufacturer\n \
        for any windows updates you might need.\n\n \
        Beginning drop of physical memory\n\n \
        Press Ctrl + Shift + Alt to continue[/color]'

class WarningScreen(MDScreen):
    pass

class ExitScreen(MDScreen):
    pass

class BYNtoUSD(MDScreen):
    money = ObjectProperty()
    def __init__(self,controller, **kw):
        super().__init__(**kw)
        self.controller = controller
        self.death = False

    def from_byn_to_usd(self):
        money = self.money.text
        flag = self.controller.fromBUNtoUSD(money)
        if flag == 5:
            self.death = True


class USDtoBYN(MDScreen):
    money = ObjectProperty()
    def __init__(self,controller, **kw):
        super().__init__(**kw)
        self.controller = controller
        self.death = False


    def from_usd_to_byn(self):
        money = self.money.text
        flag = self.controller.fromUSDtoBUN(money)
        if flag == 5:
            self.death = True


class RestartScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.restart_label.text = '[color=#FFFFFF]\
        The system has been restarted\n\n \
        Press Space to continue[/color]'


Builder.load_file(os.path.join(os.path.dirname(__file__), "interface.kv"))