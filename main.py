import json

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty
from kivymd.uix.list import ThreeLineListItem
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.card import MDCard
from kivymd.uix.list import OneLineIconListItem, MDList

from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.tab import MDTabsBase

from kivymd.font_definitions import fonts
from kivymd.icon_definitions import md_icons

from kivymd.uix.label import MDLabel

from kivymd.uix.menu import MDDropdownMenu
from kivy.clock import Clock

from kivymd.uix.picker import MDDatePicker
import datetime
import calendar
import subprocess
import webbrowser

from kivy.graphics import Color, Rectangle, Ellipse
from random import random as r

from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp

from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.core.text import Label as CoreLabel

from kivy.uix.screenmanager import Screen, ScreenManager

from kivy.uix.textinput import TextInput

# import locale
#
# print(locale.getlocale())
# print(locale.getdefaultlocale())
# locale.setlocale(locale.LC_ALL, ("ru_RU", "UTF-8"))


# internationalized Kivy Application
# https://github.com/tito/kivy-gettext-example
import gettext
from os.path import dirname, join

from kivy.app import App
from kivy.lang import Observable
from kivy.properties import StringProperty

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

sm = ScreenManager


class Lang(Observable):
    observers = []
    lang = None

    def __init__(self, defaultlang):
        super(Lang, self).__init__()
        self.ugettext = None
        self.lang = defaultlang
        self.switch_lang(self.lang)

    def _(self, text):
        return self.ugettext(text)

    def fbind(self, name, func, args, **kwargs):
        if name == "_":
            self.observers.append((func, args, kwargs))
        else:
            return super(Lang, self).fbind(name, func, *args, **kwargs)

    def funbind(self, name, func, args, **kwargs):
        if name == "_":
            key = (func, args, kwargs)
            if key in self.observers:
                self.observers.remove(key)
        else:
            return super(Lang, self).funbind(name, func, *args, **kwargs)

    def switch_lang(self, lang):
        # get the right locales directory, and instanciate a gettext
        locale_dir = join(dirname(__file__), 'data', 'locales')
        locales = gettext.translation('langapp', locale_dir, languages=[lang])
        self.ugettext = locales.gettext
        self.lang = lang

        # update all the kv rules attached to this text
        for func, largs, kwargs in self.observers:
            func(largs, None, None)


tr = Lang("ru")
# internationalized Kivy Application

# 1) download and install! http://gnuwin32.sourceforge.net/packages/gettext.htm
# https://mlocati.github.io/articles/gettext-iconv-windows.html
# 2) Copy files from "C:\Program Files (x86)\gettext-iconv\bin" to project folder!
# 3) run commands from Makefile


# Now all elements of interface are in file app_interface.kv
KV = open('app_interface.kv', 'r').read()
row_data = []


class ContentNavigationDrawer(BoxLayout):
    pass


class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()
    text_color = ListProperty((0, 0, 0, 1))


class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        """Called when tap on a menu item."""

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color


class Tab(FloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''


class ContentDialogSend(BoxLayout):
    pass


# https://stackoverflow.com/questions/2249956/how-to-get-the-same-day-of-next-month-of-a-given-day-in-python-using-datetime
def next_month_date(d):
    _year = d.year + (d.month // 12)
    _month = 1 if (d.month // 12) else d.month + 1
    next_month_len = calendar.monthrange(_year, _month)[1]
    next_month = d
    if d.day > next_month_len:
        next_month = next_month.replace(day=next_month_len)
    next_month = next_month.replace(year=_year, month=_month)
    return next_month


# https://kivy.org/doc/stable/examples/gen__canvas__canvas_stress__py.html
# def show_canvas_stress(wid):
#     with wid.canvas:
#         for x in range(10):
#             Color(r(), 1, 1, mode='hsv')
#             Rectangle(pos=(r() * wid.width + wid.x, r() * wid.height + wid.y), size=(20, 20))

def draw_chart(wid, total_amount_of_payments, loan, percent):
    interest_chart = ((total_amount_of_payments - loan) * 360) / total_amount_of_payments
    circle_width = wid.width
    center_x = 0
    center_y = wid.height // 2 - circle_width // 2
    if (wid.width > wid.height):
        circle_width = wid.height
        center_x = wid.width // 2 - circle_width // 2
        center_y = 0
    # print(wid.x, wid.y)
    with wid.canvas:
        Color(0, 0, 1, 1)
        Ellipse(pos=(wid.x + center_x, wid.y + center_y), size=(circle_width, circle_width),
                angle_start=360 - int(interest_chart), angle_end=360)
        Color(1, 0, 0, 1)
        Ellipse(pos=(wid.x + center_x, wid.y + center_y), size=(circle_width, circle_width), angle_start=0,
                angle_end=360 - int(interest_chart))
        Color(0, 0, 0, 1)


# https://pypi.org/project/kivy-ios/
# https://github.com/kivy/kivy-ios/issues/411
# -----------------
# https://stackoverflow.com/questions/38983649/kivy-android-share-image
# https://stackoverflow.com/questions/63322944/how-to-use-share-button-to-share-content-of-my-app
# Native method for Android.
def share(title, text):
    from kivy import platform

    print(platform)
    if platform == 'android':
        from jnius import autoclass

        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        Intent = autoclass('android.content.Intent')
        String = autoclass('java.lang.String')
        intent = Intent()
        intent.setAction(Intent.ACTION_SEND)
        intent.putExtra(Intent.EXTRA_TEXT, String('{}'.format(text)))
        intent.setType('text/plain')
        chooser = Intent.createChooser(intent, String(title))
        PythonActivity.mActivity.startActivity(chooser)


class MortgageCalculator(MDApp):
    # title = "Mortgage Calculator"
    # by_who = "by Rustem Giniyatov"
    dialog = None
    lang = StringProperty('ru')
    data_tables = None
    current_tab = 'tab1'
    payment_annuity = True
    menu = None  # for recreate menu on lang change

    class credit_list(Screen):
        pass

    def change_screen_to_main(self, instance):
        self.root.current = 'main'


    def change_screen_to_credit_list(self, instance):
        self.root.current = 'credit_list'


    def on_lang(self, instance, lang):
        print('switched')
        tr.switch_lang(lang)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.theme_cls.primary_palette = "Brown"
        self.theme_cls.primary_hue = "A100"
        self.data_for_calc_is_changed = True

        self.screen = Builder.load_string(KV)
        # https://kivymd.readthedocs.io/en/latest/components/menu/?highlight=MDDropDownItem#center-position
        # menu_items = [{"icon": "git", "text": f"Item {i}"} for i in range(5)]
        menu_items = [{"icon": "format-text-rotation-angle-up", "text": tr._('annuity')},
                      {"icon": "format-text-rotation-angle-down", "text": tr._('differentiated')}]
        self.menu = MDDropdownMenu(
            caller=self.screen.ids.payment_type,
            items=menu_items,
            position="auto",
            width_mult=4,
        )
        self.menu.bind(on_release=self.set_item)

        # https://kivymd.readthedocs.io/en/latest/components/pickers/?highlight=date%20picker#
        self.date_dialog = MDDatePicker(
            callback=self.get_date,
        )

        self.screen.ids.loan.bind(
            on_touch_down=self.validate_on_nums_input,
            focus=self.on_focus,
        )

        self.screen.ids.months.bind(
            on_touch_down=self.validate_on_nums_input,
            focus=self.on_focus,
        )

        self.screen.ids.interest.bind(
            on_touch_down=self.validate_on_nums_input,
            focus=self.on_focus,
        )

    # https://kivymd.readthedocs.io/en/latest/components/menu/?highlight=MDDropdownMenu#create-submenu
    def update_menu(self):
        self.menu = None
        menu_items = [{"icon": "format-text-rotation-angle-up", "text": tr._('annuity')},
                      {"icon": "format-text-rotation-angle-down", "text": tr._('differentiated')}]
        self.menu = MDDropdownMenu(
            caller=self.screen.ids.payment_type,
            items=menu_items,
            position="auto",
            width_mult=4,
        )
        self.menu.bind(on_release=self.set_item)
        if self.payment_annuity:
            self.screen.ids.payment_type.text = tr._('annuity')
        else:
            self.screen.ids.payment_type.text = tr._('differentiated')

    def on_focus(self, instance, value):
        if value:
            print('User focused', instance.name, instance.text)
            if instance.name == 'loan':
                self.screen.ids.loan.helper_text = "Вводите ТОЛЬКО числа, максимум 999 999 999"
            elif instance.name == 'months':
                self.screen.ids.months.helper_text = "Вводите ТОЛЬКО числа, максимум 1200"
            elif instance.name == 'interest':
                self.screen.ids.interest.helper_text = "Вводите ТОЛЬКО числа, максимум 1000"
        else:
            print('User defocused', instance.name, instance.text)
            if instance.name == 'loan':
                self.screen.ids.loan.helper_text = ""
                if len(self.screen.ids.loan.text) > 9:
                    self.screen.ids.loan.text = self.screen.ids.loan.text[0:9]
                self.calc_1st_screen()
                self.data_for_calc_is_changed = True
            elif instance.name == 'months':
                self.screen.ids.months.helper_text = ""
                if len(self.screen.ids.months.text) > 4:
                    self.screen.ids.months.text = self.screen.ids.months.text[0:4]
                if int(self.screen.ids.months.text) > 1200:
                    self.screen.ids.months.text = "1200"
                self.calc_1st_screen()
                self.data_for_calc_is_changed = True
            elif instance.name == 'interest':
                self.screen.ids.interest.helper_text = ""
                if len(self.screen.ids.interest.text) > 4:
                    self.screen.ids.interest.text = self.screen.ids.interest.text[0:4]
                if float(self.screen.ids.interest.text) > 1000:
                    self.screen.ids.interest.text = "1000"
                self.calc_1st_screen()
                self.data_for_calc_is_changed = True

    def validate_on_nums_input(self, instance_textfield, value):
        print(instance_textfield, value)
        # self.screen.ids.loan.error = True

    def set_item(self, instance_menu, instance_menu_item):
        def set_item(interval):
            self.screen.ids.payment_type.text = instance_menu_item.text
            instance_menu.dismiss()
            before_change = self.payment_annuity
            if tr._(self.screen.ids.payment_type.text) == tr._('annuity'):
                self.payment_annuity = True
            else:
                self.payment_annuity = False
            print(self.payment_annuity)
            if before_change != self.payment_annuity:
                print("value is changed for payment type")
                self.calc_1st_screen()
                self.data_for_calc_is_changed = True

        Clock.schedule_once(set_item, 0.5)

    def get_date(self, date):
        '''
        :type date: <class 'datetime.date'>
        '''
        pre_start_date = datetime.datetime.strptime(self.screen.ids.start_date.text, "%d-%m-%Y").date()
        print("Before: ", date, self.data_for_calc_is_changed, pre_start_date == date)
        self.screen.ids.start_date.text = date.strftime("%d-%m-%Y")  # str(date)
        if (pre_start_date != date):
            self.data_for_calc_is_changed = True
        print("After: ", date, self.data_for_calc_is_changed, pre_start_date == date)




    def build(self):
        self.theme_cls.theme_style = "Light"  # "Dark"  # "Light"

        return self.screen

    def switch_screen(self, screen_name):
        screen_manager = self.root.ids.screen_manager
        screen_manager.current = screen_name

    def change_screen_to_main(self, *args):
        self.switch_screen('main')

    def save_credit(self):
        loan = self.screen.ids.loan.text
        months = self.screen.ids.months.text
        interest = self.screen.ids.interest.text
        methode = self.screen.ids.sum_payments_type_label.text
        loan = float(loan)
        months = int(months)
        interest = float(interest)

        try:
            with open('credits.json', 'r') as file:
                data = json.load(file)
                if data:
                    last_id = data[-1]['id'] + 1
                else:
                    last_id = 1
        except FileNotFoundError:
            data = []
            last_id = 1

        credit_data = {
            'id': last_id,
            'loan':  loan,
            'months': months,
            'interest': interest,
            'methode': methode
        }
        print(credit_data)
        try:
            with open('credits.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []

        data.append(credit_data)

        with open('credits.json', 'w') as file:
            json.dump(data, file, indent=4)

        self.switch_screen('credlist')

    def calc_1st_screen(self):
        loan = self.screen.ids.loan.text
        months = self.screen.ids.months.text
        interest = self.screen.ids.interest.text
        loan = float(loan)
        months = int(months)
        interest = float(interest)
        percent = interest / 100 / 12

        if self.payment_annuity:
            monthly_payment = loan * (percent + percent / ((1 + percent) ** months - 1))
            total_amount_of_payments = monthly_payment * months
            overpayment_loan = total_amount_of_payments - loan
            effective_interest_rate = ((total_amount_of_payments / loan - 1) / (months / 12)) * 100
            self.screen.ids.payment_label.text = str(round(monthly_payment, 2))
        else:
            repayment_of_interest = loan * percent
            repayment_of_loan_body = loan / months
            max_monthly_payment = repayment_of_interest + repayment_of_loan_body

            total_amount_of_payments = 0
            overpayment_loan = 0

            debt_end_month = loan
            for i in range(0, months):
                repayment_of_interest = debt_end_month * percent
                debt_end_month = debt_end_month - repayment_of_loan_body
                monthly_payment = repayment_of_interest + repayment_of_loan_body
                total_amount_of_payments += monthly_payment
                overpayment_loan += repayment_of_interest
            min_monthly_payment = monthly_payment

            effective_interest_rate = ((total_amount_of_payments / loan - 1) / (months / 12)) * 100
            self.screen.ids.payment_label.text = str(round(min_monthly_payment, 2)) + " ... " + str(
                round(max_monthly_payment, 2))

        # self.screen.ids.payment_label.text = str(round(monthly_payment, 2))
        self.screen.ids.total_amount_of_payments_label.text = str(round(total_amount_of_payments, 2))
        self.screen.ids.overpayment_loan_label.text = str(round(overpayment_loan, 2))
        self.screen.ids.effective_interest_rate_label.text = str(round(effective_interest_rate, 2))

    def on_start(self):
        self.screen.ids.start_date.text = datetime.date.today().strftime("%d-%m-%Y")
        self.screen.ids.loan.text = "50000"
        self.screen.ids.months.text = "12"
        self.screen.ids.interest.text = "22"
        # self.screen.ids.payment_type.text = "annuity"

        self.calc_1st_screen()
        # icons names you can get here: https://materialdesignicons.com/
        # icons_item_menu_lines = {
        #     "information": "О приложении",
        #     "cash-multiple": "Взять кредит",
        # }
        # icons_item_menu_tabs = {
        #     "calculator-variant": "Input",  # ab-testing
        #     "table-large": "Table",
        #     "chart-pie": "Chart",  # chart-arc
        #     "book-open-variant": "Sum",
        # }
        # for icon_name in icons_item_menu_lines.keys():
        #     self.root.ids.content_drawer.ids.md_list.add_widget(
        #         OneLineIconListItem(icon=icon_name, text=icons_item_menu_lines[icon_name])
        #     )

        # To auto generate tabs
        # for icon_name, name_tab in icons_item_menu_tabs.items():
        #     self.root.ids.tabs.add_widget(
        #         Tab(
        #             text=f"[size=20][font={fonts[-1]['fn_regular']}]{md_icons[icon_name]}[/size][/font] {name_tab}"
        #         )
        #     )

        # for tab_act in self.root.ids.tabs.get_tab_list():
        #     print(tab_act.text)
        #     if tab_act.text.find("Active") != -1:
        #         tab_act.text = "* ACTIVE *"
        #         # tab_act.add_widget(
        #         #     MDLabel(
        #         #         text="TEST OK!",
        #         #         halign="right",
        #         #     )
        #         # )

        # print(self.root.ids.tabs.get_tab_list())
        pass

    def on_tab_switch(self, *args):
        # def on_tab_switch(self, instance_tabs, instance_tab, instance_tabs_label, tab_text):
        '''Called when switching tabs.

                :type instance_tabs: <kivymd.uix.tab.MDTabs object>;
                :param instance_tab: <__main__.Tab object>;
                :param instance_tab_label: <kivymd.uix.tab.MDTabsLabel object>;
                :param tab_text: text or name icon of tab;
                '''
        # print(instance_tab.name + " : " + tab_text)
        self.current_tab = args[1].name
        # print(args)
        # print("tab clicked!" + instance_tab.ids.label.text)
        ############# instance_tab.ids.label.text = tab_text
        # print(instance_tab.ids.label.text)
        if self.data_for_calc_is_changed:
            row_data.clear()
            self.calc_table(row_data, args)
            self.data_for_calc_is_changed = False
        pass

    # def on_star_click(self):
    #     if self.lang == 'en':
    #         locale.setlocale(locale.LC_ALL, ("ru_RU", "UTF-8"))
    #         self.lang = 'ru'
    #     elif self.lang == 'ru':
    #         locale.setlocale(locale.LC_ALL, ("en_US", "UTF-8"))
    #         self.lang = 'en'
    #     print(self.current_tab)
    #     self.screen.ids.tabs.switch_tab(self.current_tab)
    #     self.calc_table(self)
    #     self.update_menu()
    #     pass

    def calc_table(self, row_data_for_tab, *args):
        print("button1 pressed")
        start_date = self.screen.ids.start_date.text
        loan = self.screen.ids.loan.text
        months = self.screen.ids.months.text
        interest = self.screen.ids.interest.text
        payment_type = self.screen.ids.payment_type.text
        print(start_date + " " + loan + " " + months + " " + interest + " " + payment_type)
        # convert to date object, float, and so on
        start_date = datetime.datetime.strptime(self.screen.ids.start_date.text, "%d-%m-%Y").date()
        loan = float(loan)
        months = int(months)
        interest = float(interest)

        # annuity payment
        # https://temabiz.com/finterminy/ap-formula-i-raschet-annuitetnogo-platezha.html
        percent = interest / 100 / 12

        next_date = start_date
        next_prev_date = next_date

        min_monthly_payment = 0
        max_monthly_payment = 0

        if self.payment_annuity:
            monthly_payment = loan * (percent + percent / ((1 + percent) ** months - 1))
            # print(monthly_payment)
            debt_end_month = loan
            for i in range(0, months):
                repayment_of_interest = debt_end_month * percent
                repayment_of_loan_body = monthly_payment - repayment_of_interest
                debt_end_month = debt_end_month - repayment_of_loan_body
                # print(monthly_payment, repayment_of_interest, repayment_of_loan_body, debt_end_month)
                row_data_for_tab.append(
                    [i + 1, next_date.strftime("%d-%m-%Y"), round(monthly_payment, 2), round(repayment_of_interest, 2),
                     round(repayment_of_loan_body, 2), round(debt_end_month, 2)])
                next_prev_date = next_date
                next_date = next_month_date(next_date)
            total_amount_of_payments = monthly_payment * months
            overpayment_loan = total_amount_of_payments - loan
            effective_interest_rate = ((total_amount_of_payments / loan - 1) / (months / 12)) * 100
            # print(total_amount_of_payments, overpayment_loan, effective_interest_rate)
        else:
            repayment_of_interest = loan * percent
            repayment_of_loan_body = loan / months
            max_monthly_payment = repayment_of_interest + repayment_of_loan_body
            # print(monthly_payment)
            total_amount_of_payments = 0
            overpayment_loan = 0
            debt_end_month = loan
            for i in range(0, months):
                repayment_of_interest = debt_end_month * percent
                debt_end_month = debt_end_month - repayment_of_loan_body
                monthly_payment = repayment_of_interest + repayment_of_loan_body
                total_amount_of_payments += monthly_payment
                overpayment_loan += repayment_of_interest
                # print(monthly_payment, repayment_of_interest, repayment_of_loan_body, debt_end_month)
                row_data_for_tab.append(
                    [i + 1, next_date.strftime("%d-%m-%Y"), round(monthly_payment, 2), round(repayment_of_interest, 2),
                     round(repayment_of_loan_body, 2), round(debt_end_month, 2)])
                next_prev_date = next_date
                next_date = next_month_date(next_date)
            min_monthly_payment = monthly_payment

            effective_interest_rate = ((total_amount_of_payments / loan - 1) / (months / 12)) * 100
            # print(total_amount_of_payments, overpayment_loan, effective_interest_rate)

        # show_canvas_stress(self.screen.ids.graph)
        # show_canvas_stress(self.screen.ids.chart)

        # tab4
        self.screen.ids.chart.canvas.clear()
        draw_chart(self.screen.ids.chart, total_amount_of_payments, loan, self.screen.ids.interest.text)

        # tab2
        # https://kivymd.readthedocs.io/en/latest/components/datatables/?highlight=datatable
        self.data_tables = MDDataTable(
            rows_num=months,
            column_data=[
                ("№", dp(10)),
                (tr._('Date'), dp(20)),
                (tr._('Payment'), dp(20)),
                (tr._('Interest'), dp(20)),
                (tr._('Principal'), dp(20)),
                (tr._('Debt'), dp(20)),
            ],
            row_data=row_data_for_tab,

        )
        self.screen.ids.calc_data_table.clear_widgets()
        self.screen.ids.calc_data_table.add_widget(self.data_tables)

        # tab5
        if self.payment_annuity:
            self.screen.ids.sum_payment_label.text = str(round(monthly_payment, 2))
        else:
            self.screen.ids.sum_payment_label.text = str(round(min_monthly_payment, 2)) + " ... " + str(
                round(max_monthly_payment, 2))

        self.screen.ids.sum_total_amount_of_payments_label.text = str(round(total_amount_of_payments, 2))
        self.screen.ids.sum_overpayment_loan_label.text = str(round(overpayment_loan, 2))
        self.screen.ids.sum_effective_interest_rate_label.text = str(round(effective_interest_rate, 2))

        self.screen.ids.sum_term_length_label.text = str(round(months, 2)) + " мес."
        self.screen.ids.sum_interest_label.text = str(round(interest, 2)) + " %"
        self.screen.ids.sum_property_value_label.text = str(round(loan, 2))

        self.screen.ids.sum_start_date_label.text = start_date.strftime("%d-%m-%Y")
        self.screen.ids.sum_end_date_label.text = next_prev_date.strftime("%d-%m-%Y")

        self.screen.ids.sum_payments_type_label.text = payment_type

        pass

    def print_pdf(self):
        filename = datetime.datetime.now().strftime('%d-%m-%Y_%H%M%S') + ".pdf"
        document = SimpleDocTemplate(filename, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        summary = {
            "Стоимость объекта:": self.screen.ids.sum_property_value_label.text,
            "Ежемесячный платеж:": self.screen.ids.sum_payment_label.text,
            "Процент:": self.screen.ids.sum_interest_label.text,
            "Переплата по процентам:": self.screen.ids.sum_overpayment_loan_label.text,
            "Дата начала:": self.screen.ids.sum_start_date_label.text,
            "Тип платежа:": self.screen.ids.sum_payments_type_label.text,
            "Дата окончания:": self.screen.ids.sum_end_date_label.text,
            "Эффективный %:": self.screen.ids.sum_effective_interest_rate_label.text,
            "Общая сумма выплат:": self.screen.ids.sum_total_amount_of_payments_label.text,
            "Срок кредита:": self.screen.ids.sum_term_length_label.text
        }

        # Заголовки таблицы
        table_data = [['№', 'Дата', 'Платеж', 'Процент', 'Кредит', 'Долг']] + row_data

        pdfmetrics.registerFont(TTFont('DejaVuSerif', 'DejaVuSerif.ttf', 'UTF-8'))
        styles["Normal"].fontName = 'DejaVuSerif'

        # Создание таблицы
        table = Table(table_data, colWidths=[20 * mm, 30 * mm, 30 * mm, 30 * mm, 30 * mm, 30 * mm])

        # Стиль таблицы
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSerif'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('FONTNAME', (0, 1), (-1, -1), 'DejaVuSerif'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])

        table.setStyle(style)

        # Добавление таблицы в элементы документа
        elements.append(table)

        elements.append(Spacer(1, 12))

        for key, value in summary.items():
            text = f'{key}: {value}'
            paragraph = Paragraph(text, styles['Normal'])
            elements.append(paragraph)
            elements.append(Spacer(1, 12))

        # Сохранение PDF-документа
        document.build(elements)
        subprocess.Popen(filename, shell=True)
        print("pdf created")

    def get_credit_link(self):
        webbrowser.open("https://sravni.ru", new=0, autoraise=True)

    def open_about_app(self, *args):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Работу выполнил\n"
                      "студент 451 группы\n"
                      "ГАПОУ \"Арский педагогический колледж\n"
                      "имени Габдуллы Тукая\"\n"
                      "Гиниятнов Рустем",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=self.dialog_close
                    )
                ])
        self.dialog.open()

    def dialog_close(self, *args):
        self.dialog.dismiss(force=True)

    def exit_app(self):
        self.stop()

    # def share_it(self, *args):
    #     share("title_share", "this content to share!")


MortgageCalculator().run()
