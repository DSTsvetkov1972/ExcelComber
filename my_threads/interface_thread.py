from PySide6 import QtWidgets, QtCore, QtGui
from colorama import Fore
import global_vars 
import os
import pyperclip
from time import sleep
from my_threads.functions import get_files_and_sheets_from_pyperclip

from my_threads.functions import get_files_and_sheets_from_pyperclip


class InterfaceThread(QtCore.QThread):
    """
    Фоновый поток опрашивает буфер обмена и сообщает главному потоку,
    какие файлы/листы выбраны. Никаких обращений к GUI отсюда — только сигналы.
    """

    # Передаёт в главный поток данные о выбранных файлах/листах.
    # Формат: list[tuple[str, ...]] — тот же, что возвращает
    # get_files_and_sheets_from_pyperclip()
    files_sheet_to_show_signal = QtCore.Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._running = True

    def stop(self):
        """Вызывается из главного потока при закрытии приложения."""
        self._running = False

    def run(self):
        while self._running:
            self.msleep(500)  # прерываемое ожидание вместо sleep(0.5)

            files_sheet_to_show = get_files_and_sheets_from_pyperclip()

            # Единственное, что делает поток — испускает сигнал.
            # Вся работа с GUI будет в главном потоке.
            self.files_sheet_to_show_signal.emit(files_sheet_to_show)