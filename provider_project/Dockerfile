FROM python:3.11-slim

# Создаём рабочую директорию и устанавливаем её как текущую
RUN mkdir /provider
WORKDIR /provider

# Устанавливаем переменные окружения для Python:
ENV PYTHONDONTWRITEBYTECODE 1

# Копируем файл entrypoint.sh в контейнер и устанавливаем права на выполнение
COPY ./entrypoint.sh /provider/entrypoint.sh
RUN chmod +x /provider/entrypoint.sh

# Копируем остальные файлы проекта в рабочую директорию контейнера
COPY . /provider/

# Обновляем pip и устанавливаем зависимости из файла requirements.txt
RUN pip install --upgrade pip &&\
    pip install -r requirements.txt

# Указываем, что при запуске контейнера нужно выполнить entrypoint.sh
# Здесь мы явно указываем, что запускать его нужно через bash,
# на случай если в entrypoint.sh используются специфичные для bash конструкции.
ENTRYPOINT ["/bin/bash", "/provider/entrypoint.sh"]
