FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./AIML ./AIML

COPY ./telegram_aiml_bot ./telegram_aiml_bot

CMD [ "python", "./telegram_aiml_bot/aiml_bot.py" ]