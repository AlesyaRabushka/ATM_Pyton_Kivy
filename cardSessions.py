from exception import MyException
from datetime import datetime
import typer
import time
# здесь собраны все операции с участием карточки
# выдача чека
class CardCheck:
    """Чек"""
    def chek(self, operation):
        #print("Хотите ли вы забрать чек?")
        #print("1 - Да")
        #print("2 - Нет")
        try:
            confirm=typer.confirm("Хотите ли вы забрать чек?")
            if confirm:
                with typer.progressbar(range(100)) as progress:
                    for value in progress:
                        time.sleep(0.01)
                print('\t--------------------------')
                print("\t     Заберите Ваш чек     ")
                print('\t--------------------------')
                date = datetime.now()
                print('\tDate: ', date.strftime('%d-%m-%Y'))
                print('\tTime: ', date.strftime('%H:%M:%S'))
                print('\t---------------------------------')
                print('\tOperation type: ', operation, '\n')
                print('\t---------------------------------')
                #time.sleep(4)
            elif not confirm:
                pass
            else:
                print("\t----------Неверный код операции----------\n")
        except ValueError:
            print("\t----------Неверный код операции----------")

#выдача деняк
class GiveMoney:
    """выдача наличных"""
    def money_out(self, card, money, bankomat_storage, single_t, currency, gui):
        card.copy_data()

        try:
            # ветка BYN
            if currency == 'BYN':
                storage = bankomat_storage.get_storage_byn()

                # проверяем, достаточно ли средств в банкомате

                if money > storage:
                        print('\t----------Лимит средств превышен!----------\n')
                        single_t.log('Выдача наличных', False, ' Лимит средств превышен')
                        if gui == 1:
                            return 4
                else:
                    if money > int(card.get_balance_byn()):
                        print('\t----------Недостаточно средств----------\n')
                        single_t.log('Выдача наличных', False, ' Недостаточно средств')
                        if gui == 1:
                            return 2
                    elif money < 0:
                        print('\t----------Неверный формат ввода----------\n')
                        single_t.log('Выдача наличных', False, ' Неверный формат ввода')
                        if gui == 1:
                            return 3

                    else:
                        # изменяем количество средств хранилища
                        bankomat_storage.set_storage_byn(storage - money)
                        f_storage = open('bankomat.txt', 'w')
                        f_storage.write(str(bankomat_storage.get_storage_byn()))
                        f_storage.write(str(bankomat_storage.get_storage_usd()))
                        f_storage.close()

                        # поиск и изменение средств карточки
                        new_money = float(card.get_balance_byn()) - money
                        new_money = float('{:.2f}'.format(new_money))
                        user = int(card.get_chosen()) - 1#выбор номера карточки

                        from_card = open('newcard.txt')
                        to_card = open('card.txt', 'w')

                        single_t.log('Выдача наличных', True,'')
                        amount = from_card.readline()
                        to_card.write(amount)

                        # поиск нужной нам карточки (записи)
                        for i in range(0, int(amount)):
                            if i == user:
                                from_card.readline()
                                from_card.readline()
                                from_card.readline()
                                from_card.readline()
                                from_card.readline()
                                from_card.readline()
                                from_card.readline()

                                to_card.write(card.get_number())
                                to_card.write(card.get_data())
                                to_card.write(card.get_holder())
                                to_card.write(str(card.get_pin()) + '\n')
                                to_card.write(card.get_cvv())
                                card.set_balance_byn(new_money)
                                to_card.write(str(card.get_balance_byn()) + '\n')
                                to_card.write(str(card.get_balance_usd()) + '\n')
                            else:
                                to_card.write(from_card.readline())
                                to_card.write(from_card.readline())
                                to_card.write(from_card.readline())
                                to_card.write(from_card.readline())
                                to_card.write(from_card.readline())
                                to_card.write(from_card.readline())
                                to_card.write(from_card.readline())

                        from_card.close()
                        to_card.close()
                        # выдача чека
                        if gui == 0:
                            c = CardCheck()
                            c.chek('Выдача наличных')
                        if gui == 1:
                            return True

            # ветка USD
            else:
                storage = bankomat_storage.get_storage_usd()

                # проверяем, достаточно ли средств в банкомате
                if money > storage:
                    print('\t----------Лимит средств превышен!----------\n')
                    single_t.log('Выдача наличных', False, ' Лимит средств превышен')
                else:
                    if money > int(card.get_balance_usd()):
                        print('\t----------Недостаточно средств----------\n')
                        single_t.log('Выдача наличных', False, ' Недостаточно средств')
                    elif money < 0:
                        print('\t----------Неверный формат ввода----------\n')
                        single_t.log('Выдача наличных', False, ' Неверный формат ввода')
                    else:
                        # изменяем количество средств хранилища
                        bankomat_storage.set_storage_usd(storage - money)
                        f_storage = open('bankomat.txt', 'w')
                        f_storage.write(str(bankomat_storage.get_storage_byn())+'\n')
                        f_storage.write(str(bankomat_storage.get_storage_usd()) + '\n')
                        f_storage.close()

                        # поиск и изменение средств карточки
                        new_money = float(card.get_balance_usd()) - money
                        user = int(card.get_chosen()) - 1  # выбор номера карточки

                        from_card = open('newcard.txt')
                        to_card = open('card.txt', 'w')

                        single_t.log('Выдача наличных', True, '')
                        amount = from_card.readline()
                        to_card.write(amount)

                        # поиск нужной нам карточки (записи)
                        for i in range(0, int(amount)):
                            if i == user:
                                from_card.readline()
                                from_card.readline()
                                from_card.readline()
                                from_card.readline()
                                from_card.readline()
                                from_card.readline()
                                from_card.readline()

                                to_card.write(card.get_number())
                                to_card.write(card.get_data())
                                to_card.write(card.get_holder())
                                to_card.write(str(card.get_pin()) + '\n')
                                to_card.write(card.get_cvv())
                                card.set_balance_usd(new_money)
                                to_card.write(str(card.get_balance_byn()) + '\n')
                                to_card.write(str(card.get_balance_usd()) + '\n')
                            else:
                                to_card.write(from_card.readline())
                                to_card.write(from_card.readline())
                                to_card.write(from_card.readline())
                                to_card.write(from_card.readline())
                                to_card.write(from_card.readline())
                                to_card.write(from_card.readline())
                                to_card.write(from_card.readline())

                        from_card.close()
                        to_card.close()
                        # выдача чека
                        if gui == 0:
                            c = CardCheck()
                            c.chek('Выдача наличных')
        except ValueError:
            print('\t----------Неверный код операции----------')


class ChangePin(MyException):
    """смена пин-код"""
    @staticmethod
    def change_card_pin(card, pin: int, single_t, gui, new_pin_gui):
        for i in range(3, 0, -1):
            try:
                if gui == 0:
                    old_pin = int(input('Введите старый пин-код: '))
                else:
                    old_pin = int(card.get_pin())


                if pin == old_pin:
                    card.copy_data()
                    try:
                        if gui == 0:
                            new_pin = int(input('Введите новый пин-код: '))
                        else:
                            new_pin = new_pin_gui

                        # проверка, что пин-код содержит не более 4х символов
                        if len(str(new_pin)) != 4:
                            print('no')
                            raise MyException('Неверный ввод пин-код. Попробуйте ещё раз!')


                        else:
                            card.set_pin(new_pin)
                            single_t.log('Cмена пин-код', True,'')
                            print('we did it')

                            # изменение средств на самой карточке
                            from_card = open('newcard.txt')
                            to_card = open('card.txt', 'w')
                            user = int(card.get_chosen()) - 1
                            amount = from_card.readline()
                            to_card.write(str(amount))
                            for j in range(0, int(amount)):
                                if j == user:
                                    from_card.readline()
                                    from_card.readline()
                                    from_card.readline()
                                    from_card.readline()
                                    from_card.readline()
                                    from_card.readline()
                                    from_card.readline()

                                    to_card.write(card.get_number())
                                    to_card.write(card.get_data())
                                    to_card.write(card.get_holder())
                                    to_card.write(str(card.get_pin()) + '\n')
                                    to_card.write(card.get_cvv())
                                    to_card.write(str(card.get_balance_byn()) + '\n')
                                    to_card.write(str(card.get_balance_usd()) + '\n')
                                else:
                                    to_card.write(from_card.readline())
                                    to_card.write(from_card.readline())
                                    to_card.write(from_card.readline())
                                    to_card.write(from_card.readline())
                                    to_card.write(from_card.readline())
                                    to_card.write(from_card.readline())
                                    to_card.write(from_card.readline())
                            from_card.close()
                            to_card.close()
                            if gui == 1:
                                return True
                            break

                    except:
                        if gui == 0:
                            print('Неверный формат ввода. Осталось попыток: ' + str(i-1))
                        single_t.log('Смена пин-код', False, ' Неверный формат ввода')
                        if gui == 1:
                            return False
                else:
                    if i - 1 == 0:
                        if gui == 0:
                            print('Неверный пин-код. Попробуйте позже!')
                        if gui == 1:
                            return False
                        break
                    else:
                        if gui == 0:
                            print('Попробуйте еще раз! Осталось попыток: ' + str(i-1))
                        single_t.log('Смена пин-код', False,' Неверный пин-код')
                        if gui == 1:
                            return False
            except:
                print('Неверный пин-код. Попробуйте ещё раз! Осталось попыток: ' + str(i-1))
                single_t.log('Смена пин-код', False, ' Неверный пин-код')
                if gui == 1:
                    return False

#деньги на бочку!
class GetMoney:
    """пополнение денежных средств"""
    def money_in(self, card, money: int, bankomat_storage, single_t, currency, gui):
        # ветка бунов
        if currency == 'BYN':
            if gui == 1:
                if money <= 0:
                    return 5
            new_money = float(card.get_balance_byn()) + money
            find = int(card.get_chosen()) - 1
            single_t.log('Пополнение счета', True,'')

            # пополнение средств хранилища
            storage = bankomat_storage.get_storage_byn()
            bankomat_storage.set_storage_byn(storage + money)
            file = open('bankomat.txt', 'w')
            file.write(str(bankomat_storage.get_storage_byn()))
            file.write(str(bankomat_storage.get_storage_usd()))
            file.close()

            # изменение данных о средствах пользователя
            card.copy_data()
            from_card = open('newcard.txt')
            to_card = open('card.txt', 'w')
            amount = from_card.readline()
            to_card.write(amount)
            for i in range(0, int(amount)):
                if i == find:
                    from_card.readline()
                    from_card.readline()
                    from_card.readline()
                    from_card.readline()
                    from_card.readline()
                    from_card.readline()
                    from_card.readline()

                    to_card.write(card.get_number())
                    to_card.write(card.get_data())
                    to_card.write(card.get_holder())
                    to_card.write(str(card.get_pin()) + '\n')
                    to_card.write(card.get_cvv())
                    card.set_balance_byn(new_money)
                    to_card.write(str(new_money) + '\n')
                    to_card.write(str(card.get_balance_usd()) + '\n')

                else:
                    to_card.write(str(from_card.readline()))
                    to_card.write(str(from_card.readline()))
                    to_card.write(str(from_card.readline()))
                    to_card.write(str(from_card.readline()))
                    to_card.write(str(from_card.readline()))
                    to_card.write(str(from_card.readline()))
                    to_card.write(str(from_card.readline()))
            from_card.close()
            to_card.close()
            # выдача чека
            if gui == 0:
                c = CardCheck()
                c.chek('Пополнение счета')
            if gui == 1:
                return True

        # ветка американ деньги
        elif currency == 'USD':
            new_money = float(card.get_balance_usd()) + money
            find = int(card.get_chosen()) - 1
            single_t.log('Пополнение счета', True, '')

            # пополнение средств хранилища
            storage = bankomat_storage.get_storage_usd()
            bankomat_storage.set_storage_usd(storage + money)

            file = open('bankomat.txt', 'w')
            file.write(str(bankomat_storage.get_storage_byn()))
            file.write(str(bankomat_storage.get_storage_usd()))
            file.close()

            # изменение данных о средствах пользователя
            card.copy_data()
            from_card = open('newcard.txt')
            to_card = open('card.txt', 'w')
            amount = from_card.readline()
            to_card.write(amount)
            for i in range(0, int(amount)):
                if i == find:
                    from_card.readline()
                    from_card.readline()
                    from_card.readline()
                    from_card.readline()
                    from_card.readline()
                    from_card.readline()
                    from_card.readline()

                    to_card.write(card.get_number())
                    to_card.write(card.get_data())
                    to_card.write(card.get_holder())
                    to_card.write(str(card.get_pin()) + '\n')
                    to_card.write(card.get_cvv())
                    card.set_balance_usd(new_money)
                    to_card.write(str(card.get_balance_byn()) + '\n')
                    to_card.write(str(new_money) + '\n')

                else:
                    to_card.write(str(from_card.readline()))
                    to_card.write(str(from_card.readline()))
                    to_card.write(str(from_card.readline()))
                    to_card.write(str(from_card.readline()))
                    to_card.write(str(from_card.readline()))
                    to_card.write(str(from_card.readline()))
                    to_card.write(str(from_card.readline()))
            from_card.close()
            to_card.close()
            # выдача чека
            if gui == 0:
                c = CardCheck()
                c.chek('Пополнение счета')

# валютные операции
class Currency(CardCheck):
    """валютные операции"""
    def print(self):
        print('КУРС ВАЛЮТ')
        print('\t1 - 174.00 (казахстанский тенге) - \t* минимальная доступная сумма: 1740 тенге')
        print('\t2 - 7.00 (замбийская квача) - \t* минимальная доступная сумма: 70 квач')
        print('\t3 - 35.00 (киргизская сома) - \t*минимальная доступная сумма: 350 сом')
        print('\t4 - 11.00 (украинская гривна) - \t*минимальная доступная сумма: 110 гривен')
        print('\t5 - 777.00 (мьянманский кьят) - \t*минимальная доступная сумма: 7770 кьят')

        a = int(input('Выберите валюту: '))
        value = input('Введите сумму: ')
        if value.isdigit():
            value = int(value)
            if a == 1:
                if value < 1740:
                    print('Минимально допустимая сумма: 1740 тенге. Попробуйте еще раз!')
                    value = 0
                else:
                    value = value / 174
                    value = float('{:.2f}'.format(value))

            elif a == 2:
                if value < 70:
                    print('Минимально допустимая сумма: 70 квач. Попробуйте еще раз!')
                    value = 0
                else:
                    value = value / 7
                    value = float('{:.2f}'.format(value))
            elif a == 3:
                if value < 350:
                    print('Минимально допустимая сумма: 350 сом. Попробуйте еще раз!')
                    value = 0
                else:
                    value = value / 35
                    value = float('{:.2f}'.format(value))
            elif a == 4:
                if value < 110:
                    print('Минимально допустимая сумма: 110 гривен. Попробуйте еще раз!')
                    value = 0
                else:
                    value = value / 11
                    value = float('{:.2f}'.format(value))
            elif a == 5:
                if value < 7770:
                    print('Минимально допустимая сумма: 7770 кьят. Попробуйте еще раз!')
                    value = 0
                else:
                    value = value / 777
                    value = float('{:.2f}'.format(value))
            else:
                print('Неверный номер операции. Попробуйте еще раз!')
        else:
            print('\t----------Неверный формат ввода данных----------')
            return False

        return value

    def moneyOut(self, card, money):
        card.copy_data()

        if money > int(card.get_balance_byn()) or money < 0:
            print('Операция на данный момент недоступна. Повторите попытку позже')
        else:
            new_money = float(card.get_balance_byn()) - money
            new_money = float('{:.2f}'.format(new_money))
            card.set_balance_byn(new_money)
            find = card.get_chosen() - 1

            from_card = open('newcard.txt', 'r')
            to_card = open('card.txt', 'w')
            amount = from_card.readline()
            to_card.write(amount)

            for i in range(0, int(amount)):
                if i == find:
                    from_card.readline()
                    from_card.readline()
                    from_card.readline()
                    from_card.readline()
                    from_card.readline()
                    from_card.readline()
                    from_card.readline()

                    to_card.write(card.get_number())
                    to_card.write(card.get_data())
                    to_card.write(card.get_holder())
                    to_card.write(str(card.get_pin()) + '\n')
                    to_card.write(card.get_cvv())
                    to_card.write(str(card.get_balance_byn()) + '\n')
                    to_card.write(str(card.get_balance_usd()) + '\n')

                else:
                    to_card.write(from_card.readline())
                    to_card.write(from_card.readline())
                    to_card.write(from_card.readline())
                    to_card.write(from_card.readline())
                    to_card.write(from_card.readline())
                    to_card.write(from_card.readline())
                    to_card.write(from_card.readline())
            from_card.close()
            to_card.close()

            # выдача чека
            c = CardCheck()
            c.chek('Валютные операции')


class Telephone(GiveMoney):
    """оплата телефона"""
    def value_check(self,card,money):
        if int(money) > int(card.get_balance_byn()):
            return False
        else:
            return True
    def telephone_pay(self, card, money: int, tel_number: str, bankomat_storage, single_t):
        self.value_check(card,money)
        self.copy_data()
        new_money = float(card.get_balance_byn()) - money
        card.set_balance_byn(new_money)
        find = card.get_chosen() - 1
        from_card = open('newcard.txt', 'r')
        to_card = open('card.txt', 'w')
        amount = from_card.readline()
        to_card.write(amount)

        for i in range(0, int(amount)):
            if i == find:
                from_card.readline()
                from_card.readline()
                from_card.readline()
                from_card.readline()
                from_card.readline()
                from_card.readline()
                from_card.readline()

                to_card.write(card.get_number())
                to_card.write(card.get_data())
                to_card.write(card.get_holder())
                to_card.write(str(card.get_pin()) + '\n')
                to_card.write(card.get_cvv())
                to_card.write(str(card.get_balance_byn()) + '\n')
                to_card.write(str(card.get_balance_usd()) + '\n')

            else:
                to_card.write(from_card.readline())
                to_card.write(from_card.readline())
                to_card.write(from_card.readline())
                to_card.write(from_card.readline())
                to_card.write(from_card.readline())
                to_card.write(from_card.readline())
                to_card.write(from_card.readline())
        from_card.close()
        to_card.close()
        tel_number=tel_number+'\n'
        from_card = open('newtelephone.txt', 'r')
        to_card = open('telephone.txt', 'w')
        k = from_card.readline()
        to_card.write(k)
        single_t.log('Пополнение счета телефона', True,'')
        for i in range(int(k)):
            telephone = from_card.readline()
            balance = int(from_card.readline())
            if tel_number == telephone:
                to_card.write(telephone)
                to_card.write(str(balance + money) + '\n')
            else:
                to_card.write(telephone)
                to_card.write(str(balance)+'\n')
        from_card.close()
        to_card.close()

    @staticmethod
    def copy_data():
        card = open("telephone.txt", "r")
        new_card = open("newtelephone.txt", "w")

        k = int(card.readline())
        new_card.write(str(k) + '\n')
        for i in range(0, k):
            new_card.write(str(card.readline()))
            new_card.write(str(card.readline()))
        card.close()
        new_card.close()

class Currency_transactions:
    def fromBUNtoUSD(self,card,value:float, gui):
        card.copy_data()
        if float(value) * 3.31 > float(card.get_balance_byn()) or float(value) < 0:
            print('ERROR')
        else:
            new_value = float(card.get_balance_byn())-(value*3.31)
            new_value = float('{:.2f}'.format(new_value))
            cur_new_value=float(card.get_balance_usd())+value
            card.set_balance_usd(cur_new_value)
            card.set_balance_byn(new_value)
            find = card.get_chosen() - 1

            from_card = open('newcard.txt', 'r')
            to_card = open('card.txt', 'w')
            amount = from_card.readline()
            to_card.write(amount)

            for i in range(0, int(amount)):
                if i == find:
                    from_card.readline()
                    from_card.readline()
                    from_card.readline()
                    from_card.readline()
                    from_card.readline()
                    from_card.readline()
                    from_card.readline()

                    to_card.write(card.get_number())
                    to_card.write(card.get_data())
                    to_card.write(card.get_holder())
                    to_card.write(str(card.get_pin()) + '\n')
                    to_card.write(card.get_cvv())
                    to_card.write(str(card.get_balance_byn()) + '\n')
                    to_card.write(str(card.get_balance_usd()) + '\n')

                else:
                    to_card.write(from_card.readline())
                    to_card.write(from_card.readline())
                    to_card.write(from_card.readline())
                    to_card.write(from_card.readline())
                    to_card.write(from_card.readline())
                    to_card.write(from_card.readline())
                    to_card.write(from_card.readline())
            from_card.close()
            to_card.close()

            # выдача чека
            if gui == 0:
                c = CardCheck()
                c.chek('Валютные переводы')

    def fromUSDtoBUN(self, card, value: float, gui):
        card.copy_data()
        if value / 3.31 > card.get_balance_usd() or value < 0:
            print('ERROR')
        else:
            new_value = float(card.get_balance_usd()) - (value / 3.31)
            cur_new_value = float(card.get_balance_byn()) + value
            new_value = float('{:.2f}'.format(new_value))
            card.set_balance_usd(new_value)
            card.set_balance_byn(cur_new_value)
            find = card.get_chosen() - 1

            from_card = open('newcard.txt', 'r')
            to_card = open('card.txt', 'w')
            amount = from_card.readline()
            to_card.write(amount)

            for i in range(0, int(amount)):
                if i == find:
                    from_card.readline()
                    from_card.readline()
                    from_card.readline()
                    from_card.readline()
                    from_card.readline()
                    from_card.readline()
                    from_card.readline()

                    to_card.write(card.get_number())
                    to_card.write(card.get_data())
                    to_card.write(card.get_holder())
                    to_card.write(str(card.get_pin()) + '\n')
                    to_card.write(card.get_cvv())
                    to_card.write(str(card.get_balance_byn()) + '\n')
                    to_card.write(str(card.get_balance_usd()) + '\n')

                else:
                    to_card.write(from_card.readline())
                    to_card.write(from_card.readline())
                    to_card.write(from_card.readline())
                    to_card.write(from_card.readline())
                    to_card.write(from_card.readline())
                    to_card.write(from_card.readline())
                    to_card.write(from_card.readline())
            from_card.close()
            to_card.close()

            # выдача чека
            if gui == 0:
                c = CardCheck()
                c.chek('Валютные переводы')
