#Time tracker
- Репозиторий содержит скрипт, который забирает значения у конкретного пользователя из БД и считает его рабочее время за рабочий день с 9:00 до 18:00 и за всю рабочую неделю.

#Структура репозитория:
-**TimeTracking.sql**: База данных, в которой уже созданы тестовые данные для тестирования скрипта.
-**config.py**: Файл конфигурации, в котором хранятся данные для подключения или используемые в скрипте переменные. (Которые можно сделать переменными окружения)
-**requirements.txt**: Файл содержащий необходимые модули и библиотеки для работы скрипта
-**time_tracking.py**: Скрипт считающий отработанные рабочие часы сотрудника за конкретный указанный день и за рабочую неделю, в который входит указанный день (с пн-пт с 9:00 - 18:00)

Шаги запуска:
1. Импортировать репозиторий в виртуальное окружение
2. Установить все зависимости, модули и библиотеки из файла requirements.txt
3. Развернуть БД из репозитория
4. Сконфигурировать данные для подключения в файле config.py
5. Запустить скрипт