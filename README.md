# Eventex

Sistema de eventos encomendado pela Morena

[![Build Status](https://travis-ci.org/marcos-m-muller/eventex.svg?branch=master)](https://travis-ci.org/marcos-m-muller/eventex)
[![Code Health](https://landscape.io/github/marcos-m-muller/eventex/master/landscape.svg?style=flat)](https://landscape.io/github/marcos-m-muller/eventex/master)

## Como desenvolver?
1. Clone o repositório
2. Crie um virtualenv com Python 3.5
3. Ative o virtualenv
4. Instale as dependências
5. Configure a instância com o .env
6. Execute os testes

````console
git clone git@github.com:marcos-m-muller/eventex.git eventex
cd eventex
python -m venv .eventex
.eventex\Scripts\activate.bat
pip install -r requirements-dev.txt
cp contrib/env-sample .env
python manage.py test
````

## Como fazer o deploy
1. Crie uma instância no Heroku
2. Envie as configurações para o Heroku
3. Defina uma SECRET_KEY segura para a instância
4. Defina DEBUG=False
5. Configure o serviço de email
6. Envia o código para o Heroku

```console
heroku create minhainstancia
heroku config:push
heroku config:set SECRET_KEY=`python contrib/secret_gen.py`
heroku config:set DEBUG=False
# Configure o email
git push heroku master --force
```