# VerifyBot
Бот для верификации пользователей

## Описание

Этот бот предназначен для автоматизации процесса верификации. Сам бот предназначен для серверов, где требуется голосовая верификация пользователей.

## Основные возможности

    Автоматическое назначение роли при входе нового участника (опционально, через настройки в config).
    Выбор пола: при верификации администратор может назначить роль "Мужской" или "Женский".
    Отказ в доступе: возможность отказа в доступе с указанием причины, которая будет отображена в журнале событий.
    Логирование: бот записывает все действия по верификации и отказам в специально назначенный канал.
## Команды
/action — команда для начала процесса верификации. Только пользователи с правами (роли, указанные в config.command_role_id) могут её использовать.

## Как настроить
Установите необходимые библиотеки:
```
pip install disnake
```

Настройте конфигурацию в файле config.py, указав ID ролей и каналов:

token = 'ТОКЕН БОТА'
guild_id = 123  # Замените на свой ID сервера

# ID ролей
unverified_role_id = 123  # ID роли "unverify"
male_role_id = 123  # ID роли "Мужской"
female_role_id = 123  # ID роли "Женский"
denied_role_id = 123  # ID роли "Недопуск"
command_role_id = 123  # Роль, которая может использовать команду
log_channel_id = 123  # Замените на ID вашего канала для логов

auto_role_enabled = False  # Установите в True, чтобы роль выдавалась автоматически при заходе на сервер
auto_role_id = 1234567890  # ID роли, которая будет выдаваться автоматически

Запустите бота:
```
python main.py
