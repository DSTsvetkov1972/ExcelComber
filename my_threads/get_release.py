from PySide6 import QtWidgets, QtCore, QtGui
from colorama import Fore
import global_vars 
import os
import requests
from bs4 import BeautifulSoup
from time import sleep
from my_threads.functions import get_license_data
from colorama import Fore


class GetReleaseThread(QtCore.QThread):
    def __init__ (self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.message_title = "Открываем выбранные файлы:"

    mysignal = QtCore.Signal(str)

    def on_signal(self, mysignal):
        global_vars.ui.info_label.setStyleSheet('color: blue')            
        global_vars.ui.info_label.setText(mysignal)

    def get_current_release(self):
        

        session = requests.Session()
        session.trust_env = False  # Важно! Игнорирует системные настройки прокси
        
        try:
            print(Fore.YELLOW, 'подключаемся к http://www.excelcomber.ru', Fore.RESET)
            url = 'http://www.excelcomber.ru'
            response = session.get(url)
            print(Fore.GREEN, 'подключились http://www.excelcomber.ru', Fore.RESET)
            #response = requests.get(url)

            # Проверка статуса ответа
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                current_release = soup.find(id="current-release")
                if current_release:
                    print(Fore.BLUE, current_release.text, Fore.RESET)
                    return current_release.text
                else:
                    return "Не удалось проверить релиз - нет информации об актуальном релизе на excelcomber.ru"
            else:
                print(f"Ошибка! Статус код: {response.status_code}")
                return "Не удалось проверить релиз - excelcomber.ru не отвечает"
        except requests.exceptions.ConnectionError:
            return "Не удалось проверить релиз - нет подключения к интернету или excelcomber.ru не отвечает"
            

    
    def run(self):
        license_data = get_license_data()
        license_str = f"; Пользователь: {license_data['user']}; Активировано до: {license_data['trial_finish'][:16]};"
        print(Fore.MAGENTA, license_data, Fore.RESET)
        
        print(Fore.MAGENTA, 'Запустили определение текущего релиза', Fore.RESET)
        current_release = self.get_current_release()
        
        if current_release and 'Не удалось проверить релиз - ' not in current_release:
            if current_release == global_vars.version:
                global_vars.title = f"ExcelComber {global_vars.version}; Актуальный релиз" + license_str
            else:
                global_vars.title = f"ExcelComber {global_vars.version}; Доступен новый релиз {current_release}" + license_str
        else:
            global_vars.title = f"ExcelComber {global_vars.version}; {current_release}" + license_str        

        self.mysignal.emit(None)