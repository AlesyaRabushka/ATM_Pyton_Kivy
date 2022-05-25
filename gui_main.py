from kivy.core.window import Window

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import NoTransition

from controller import Controller

from interface import WelcomeScreen, PinScreen, MenuScreen, MoneyOperations, MoneyOutScreen, MoneyOutChoiceScreen,\
    ContinueScreen, CheckScreen, CheckChoiceScreen, MoneyInScreen, BalanceScreen, WarningScreen, ExitScreen, DeathScreen
from interface import *

# kv = Builder.load_file(os.path.join(os.path.dirname(__file__), "interface.kv"))

class Manager(ScreenManager):
    def change_screen(self, name):
        self.current = name

class MyApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down = self._on_keyboard_down)
        self._keyboard.bind(on_key_up = self._on_keyboard_up)
        self.make_alive = []


        self.sm = Manager(transition=NoTransition())
        self.controller = Controller(screen_manager = self.sm)

        pin_screen = PinScreen(name='pin_screen', controller=self.controller)

        bs = BalanceScreen(name='balance_screen', controller=self.controller)
        self.controller.balance_screen = bs
        self.sm.add_widget(WelcomeScreen(name='welcome_screen', controller = self.controller, balance=bs))
        self.sm.add_widget(bs)
        self.sm.add_widget(pin_screen)
        self.sm.add_widget(MenuScreen(name='menu_screen', pin_screen=pin_screen))
        self.sm.add_widget(MoneyOutChoiceScreen(name = 'money_out_choice_screen', controller=self.controller))
        self.sm.add_widget(MoneyOutScreen(name='money_out_screen', controller=self.controller))
        self.sm.add_widget(MoneyOperations(name='operations_screen'))
        self.sm.add_widget(ContinueScreen(name='continue_screen'))
        check = CheckScreen(name='check_screen', controller=self.controller)
        self.sm.add_widget(check)
        self.sm.add_widget(CheckChoiceScreen(name='check_choice_screen', check_screen=check))
        self.sm.add_widget(MoneyInScreen(name='money_in_screen', controller=self.controller))
        self.sm.add_widget(BalanceScreen(name='balance_screen', controller=self.controller))
        self.sm.add_widget(WarningScreen(name='warning_screen'))
        self.sm.add_widget(ExitScreen(name='exit_screen'))
        self.sm.add_widget(DeathScreen(name='death_screen'))
        self.sm.add_widget(TelephonePaymentScreen(name='telephone_payment', controller=self.controller))
        self.sm.add_widget(BYNtoUSD(name='byn_to_usd', controller=self.controller))
        self.sm.add_widget(USDtoBYN(name='usd_to_byn', controller=self.controller))
        self.sm.add_widget(ChangePinScreen(name='change_pin_screen', controller=self.controller))
        self.sm.add_widget(RestartScreen(name='restart_screen'))
        self.sm.current = 'welcome_screen'

    def _keyboard_closed(self):
        if self.sm.current == 'death_screen':
            self._keyboard.unbind(on_key_down = self._on_keyboard_down)
            self._keyboard = None

    def _on_keyboard_down(self, *args):
        if self.sm.current == 'death_screen':
            if len(self.make_alive) < 3:
                self.make_alive.append(args[2])

            if len(self.make_alive) == 3:
                string = str(self.make_alive)
                if 'İ' in string and 'ı' in string and 'Ĵ' in string:
                    self.sm.current = 'restart_screen'
                    self.make_alive = []
                else:
                    self.make_alive = []

            # if args[2] == ' ':
            #     #print('yes',args[2])
            #     self.sm.current = 'restart_screen'
        elif self.sm.current == 'restart_screen':
            if args[2] == ' ':
                #print('yes',args[2])
                self.sm.current = 'pin_screen'

        #print('down', args)

    def _on_keyboard_up(self, *args):
        pass
        #print('up', args)


    def build(self):
        #return self.controller.get_screen()
        return self.sm


MyApp().run()
