FROM python:3.11-slim
WORKDIR /client

# Устанавливаем необходимые переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1

# Копируем только entrypoint.sh и устанавливаем ему права на выполнение
COPY ./entrypoint.sh /client/entrypoint.sh
RUN chmod +x /client/entrypoint.sh

# Копируем остальные файлы
COPY . /client/

# Устанавливаем зависимости
RUN pip install --upgrade pip &&\
    pip install -r requirements.txt

# Явно указываем интерпретатор для entrypoint.sh
ENTRYPOINT ["/bin/bash", "/client/entrypoint.sh"]
