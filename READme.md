4 задание Морозова Анастасия Валентиновна

Описание функционала приложения:

Сервер:

•  Запуск эксперимента:
  *  Сервер может начать эксперимент по угадыванию числа по команде start от любого из клиентов.
  *  Генерирует случайное число в диапазоне от 1 до 100.
  *  Отправляет сообщение всем подключенным клиентам о начале эксперимента.
•  Обработка предположений клиентов:
  *  Принимает от клиентов предположения о загаданном числе.
  *  Сравнивает предположение клиента с загаданным числом.
  *  Отправляет клиенту ответ:
    *  You guessed it! - если число угадано.
    *  Too high! - если число больше загаданного.
    *  Too low! - если число меньше загаданного.
•  Ведение статистики:
  *  Отслеживает количество попыток, которые потребовались каждому клиенту, чтобы угадать число.
•  Вывод таблицы лидеров:
  *  Выводит в консоль таблицу лидеров по окончании эксперимента, показывающую, сколько попыток понадобилось каждому клиенту.
•  Обработка подключений:
  *  Принимает новые подключения от клиентов.
  *  После начала первого из ряда эспериментов перестает принимать новые подключения чтобы держать правильную таблицу рейтинга.
  *  Создает отдельный поток для обработки каждого клиента, чтобы каждый клиент мог отправлять и получать сообщения независимо от других.

Клиент:

•  Подключение к серверу:
  *  Подключается к серверу по заданному IP-адресу и порту.
•  Получение сообщений от сервера:
  *  Принимает от сервера сообщения о начале и окончании эксперимента, а также ответы на предположения о числе.
  *  Выводит полученные сообщения на экран.
•  Отправка предположений:
  *  Отправляет серверу свои предположения о загаданном числе.
•  Команды:
  *  start: Запускает эксперимент на сервере.
  *  guess: Отправляет серверу предположение о загаданном числе.
  *  history: Показывает историю попыток данного игрока
