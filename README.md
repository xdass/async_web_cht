# Клиенты для чата minechat
Доступно 2-клиента:
 * read_messages.py - клиент для чтения сообщений из чата, поддерживает реконет при обрыве соединения,логирование сообщений в файл
 * send_message - клиент с возможностью регистрации нового пользователя

Вспомогательные настройки для тестирования обрыва соединения:
 * util.py



## Как установить

Для работы клиентов нужен Python версии не ниже 3.7.

```bash
pip install -r requirements.txt
```
В директории проекта создать файл `.env` со следующими значениями:<br>
HOST=minechat.dvmn.org<br>
PORT=5000<br>
LOG_FILE=./chat_log.txt<br>

## Как запустить

#### Список необязательных параметров можно посмотреть командой -h

Следующие параметры хранятся в переменных окружения и могут быть переопределены через передачу параметров в скрипт

```bash
python read_messages.py

Vlad: Нет, ты — искусственный интеллект.

Eva: Ты не человек. Ты — искусственный интеллект. 
.......
```
***
Вход через ТОКЕН
```bash
python send_message.py --token 'YOUR_TOKEN' --message 'ТЕСТОВОЕ СООБЩЕНИЕ'

DEBUG:root:Hello %username%! Enter your personal hash or leave it empty to create new account.
DEBUG:root:b'YOUR_TOKEN\n\n'
DEBUG:root:{"nickname": "Focused Loyd", "account_hash": "YOUR_TOKEN"}
Auth success for name Focused Loyd
DEBUG:root:b'\xd0\xa2\xd0\xb5\xd1\x81\xd1\x82\xd0\xbe\xd0\xb2\xd0\xbe\xd0\xb5 \xd1\x81\xd0\xbe\xd0\xbe\xd0\xb1\xd1\x89\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5\n\n'

.......
```
Создание нового пользователя(если в параметрах не указан nickname по умолчанию используется New User)
```
python send_message.py
DEBUG:root:Hello %username%! Enter your personal hash or leave it empty to create new account.
DEBUG:root:b'\n'
DEBUG:root:Enter preferred nickname below:
DEBUG:root:b'New user\n'
DEBUG:root:{"nickname": "Boring New user", "account_hash": "YOUR_TOKEN"}
Save this token {'nickname': 'Boring New user', 'account_hash': 'YOUR_TOKEN'}. And login with it!

```


# Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).