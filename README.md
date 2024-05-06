## Тестовая программа (Python) для сбора данных о госконтрактах с сайта clearspending.ru при помощи API сайта и внешних библиотек reqests, jinja2 и для защиты пероснальных данных - dotenv.

Список необходимых внешних библиотек виртуального окружения находится в файле requirements.txt.

Действия заносятся в журнал test_log.log.

Для выполнения функции send_mail_contracts необходимо передать из файла .env переменные SENDER_EMAIL и EMAIL_PASSWORD.

Формируемая для записи сообщения таблица записывается в файл по адресу, указанному в строковом типе в переменной PATH_FOR_TABLE, которая также содержится в файле .env.

Поэтому необходимо создать в рабочей директории файл .env, в который поместить содержание пар ключ-значение переменных:
SENDER_EMAIL="значение"
EMAIL_PASSWORD = "значение"
PATH_FOR_TABLE = str("значение")       // нужно указать абсолютный путь, напр. С://User//.....

Переменные SENDER_EMAIL и EMAIL_PASSWORD должны содержать в строковом виде соответственно адрес электронной почты отправителя и пароль для этого приложения (рабочей станции) либо резервный код, сформированные при двухфакторной аутентификации google аккакунта отправителя.

Если python-dotenv в домашней версии Windows не устанавливается - предоставьте себе права, введите в PowerShell следующий скрипт: 

Set-ExecutionPolicy unrestricted -Scope CurrentUser



