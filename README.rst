Telegram AIML Bot

This project is a boilerplate for creating a simple AIML bot that can be containerised and deployed anywhere.

Usage
To use, copy sample.env to .env and fill in the details.

Then run: python telegram_aiml_bot/aiml_bot.py to run locally.

Kubernetes deployment
kubectl create secret generic prod-secrets --from-env-file=.env
kubectl apply -f deployment.yaml 