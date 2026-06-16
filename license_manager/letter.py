import pendulum
from dateutil.relativedelta import relativedelta
import pyperclip
from license_maker import data_dict

# user_name = 'Дмитрий Сергеевич'
user_name = data_dict['user']

letter = f"""{user_name}, добрый день!

Благодарю Вас за интерес проявленный к ExcelComber.
Файл лицензии во вложении.
Саму программу можно загрузить по ссылке.\n\n
Пробный период - до {(pendulum.now('Europe/Moscow') + relativedelta(months=1)).format('D MMMM YYYY', locale='ru')}г.\n\n
Если ExcelComber не подходит для задач, которые Вы собирались с его помощью решить, напишите мне -
я обязательно предложу решение, которое подойдёт именно в Вашем случае.\n\n
Если Вы захотите использовать ExcelComber по истечении пробного периода, свяжитесь со мной ещё раз и я вышлю Вам постоянную лицензию.
За неё я попрошу с Вас вознаграждение, размер которого оставлю на Ваше усмотрение, если Вы частное лицо.
Если Вы представляете организацию, размер вознаграждения определим в ходе обсуждения.\n\n
Вопросы по работе программы можете задавать через электронную почту team@excelcomber.ru\n\n
Буду рад узнать Ваше мнение о ExcelComber - пишите!\n\n\n
С уважением,
разработчик ExcelComber
Цветков Дмитрий
"""
pyperclip.copy(letter)
print(letter)