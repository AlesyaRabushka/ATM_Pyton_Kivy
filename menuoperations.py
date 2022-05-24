from cardSessions import GiveMoney
from cardSessions import ChangePin
from cardSessions import GetMoney
from cardSessions import Telephone, Currency
from cardSessions import Currency_transactions
import typer
from bankomat import Bankomat
import time

class MenuOperations(Bankomat):
    """меню опций"""

    @staticmethod
    def print_menu(card, single_t):
        # приезжают инкассаторы и кладут денежку в банкомат
        storage = Bankomat()
        storage.set_storage_byn(10000)
        storage.set_storage_usd(1000)

        file = open('bankomat.txt', 'w')
        file.write(str(storage.get_storage_byn()))
        file.write(str(storage.get_storage_usd()))
        file.close()

        while 1 == 1:
            time.sleep(4)
            print("\tВыберите операцию:")
            print("\tcard_info - Данные банковской карты")
            print("\tcash_out - Выдача наличных")
            print("\tphone_payment - Оплата телефона")
            print("\tchange_pin - Смена пин-кода")
            print("\tcash_in - Добавить средства на карточку")
            print("\tcurrency_exchange - Обмен валют")
            print("\taccount_transaction - Перевод между счетами")
            print("\texit - Забрать карту и закончить работу")


            #k = int(input())
            operation_name=typer.prompt("Choose operation: ")
            # данные о карточке
            if operation_name == "card_info":
                with typer.progressbar(range(100)) as progress:
                    for value in progress:
                        time.sleep(0.01)
                card.print_card_info()
                single_t.log('Данные банковской карты', True,'')

            # выдача наличных
            elif operation_name == "cash_out":
                #print('Выберите счет: ')
                print('\tBYN')
                print('\tUSD')
                try:
                    value=typer.prompt("Выберите счет:")
                    if value.upper() == "BYN":
                        try:
                            money=typer.prompt("Выберите нужную сумму: ")
                            if money.isdigit():
                                give_money = GiveMoney()
                                give_money.money_out(card, int(money), storage, single_t, 'BYN', 0)
                            else:
                                print('\n----------Неверный формат ввода данных-----------\n')

                        except ValueError:
                            print("\t----------Неверный код операции----------\n\n")
                    elif value.upper() == "USD":

                        try:
                            money=typer.prompt("Выберите нужную сумму: ")
                            if money.isdigit():
                                give_money = GiveMoney()
                                give_money.money_out(card, int(money), storage, single_t, 'USD', 0)
                            else:
                                print('\n----------Неверный формат ввода данных-----------\n')

                        except ValueError:
                            print("\t----------Неверный код операции----------\n\n")

                except ValueError:
                    print("\t----------Неверный код операции----------\n\n")

            # оплата телефона
            elif operation_name == "phone_payment":
                print('+375 44 730 81 28\n+375 33 895 12 04\n+375 25 234 10 23')
                tel = typer.prompt("Выберите номер телефона: ")
                if tel == "+375 44 730 81 28" or tel == "+375 33 895 12 04" or tel == "+375 25 234 10 23":
                    money = int(input("Введите сумму платежа: "))
                    with typer.progressbar(range(100)) as progress:
                        for value in progress:
                            time.sleep(0.01)
                    telephone = Telephone()
                    telephone.telephone_pay(card, money, tel, storage, single_t)

                else:
                    print('\t----------Неверный код операции. Повторите попытку позже.----------\n')
                    single_t.log('Пополнение счета телефона', False, 'Неверный номер операции')

            # смена пин-код
            elif operation_name == "change_pin":
                ChangePin.change_card_pin(card, card.get_pin(), single_t, 0, '')
                with typer.progressbar(range(100)) as progress:
                    for value in progress:
                        time.sleep(0.01)


            # пополнение средств
            elif operation_name == "cash_in":
                #print('Выберите валюту:')
                print('BYN')
                print('USD')
                try:
                    choose_money = typer.prompt("Выберите валюту: ")
                    money = input('Вставьте купюру: ')
                    if money.isdigit():
                        if choose_money.upper() == "BYN":
                            get_money = GetMoney()
                            get_money.money_in(card, int(money), storage, single_t, 'BYN', 0)
                            with typer.progressbar(range(100)) as progress:
                                for value in progress:
                                    time.sleep(0.01)
                        elif choose_money.upper() == "USD":
                            get_money = GetMoney()
                            get_money.money_in(card, int(money), storage, single_t, 'USD', 0)
                    else:
                        print('\t----------Неверный формат ввода данных-----------\n')


                except ValueError:
                    print('\n\t----------Неверный код операции----------\n\n')

            elif operation_name == "currency_exchange":
                currency = Currency()
                money = currency.print()
                if money != 0:
                    currency.moneyOut(card, money)
                else:
                    pass

            elif operation_name == "account_transaction":
                try:
                    print('Выберите счет на который хотите перевести: ')
                    print('BUN')
                    print('USD')
                    account=typer.prompt('Выберите счет на который хотите перевести: ')
                    if account.upper() == "BUN":
                        money=float(input('Введите сумму: '))
                        transaction=Currency_transactions()
                        transaction.fromUSDtoBUN(card,money, 0)
                        with typer.progressbar(range(100)) as progress:
                            for value in progress:
                                time.sleep(0.01)
                    elif account.upper() == "USD":
                        money = float(input('Введите сумму: '))
                        transaction = Currency_transactions()
                        transaction.fromBUNtoUSD(card, money, 0)

                    else:
                        print('----------Неверный код операции----------\n\n')
                except ValueError:
                    print('\n\t----------Неверный код операции----------\n\n')
            # выход из проги
            elif operation_name == "exit":
                single_t.log('Выход из системы', True,'')
                exit()
            else:
                print('----------Неверный код операции----------\n\n')


