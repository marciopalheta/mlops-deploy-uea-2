# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import xgboost as xgb
import pickle
import os

from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth

colunas = ['RevolvingUtilizationOfUnsecuredLines', 'age',
       'NumberOfTime30-59DaysPastDueNotWorse', 'DebtRatio', 'MonthlyIncome',
       'NumberOfOpenCreditLinesAndLoans', 'NumberOfTimes90DaysLate',
       'NumberRealEstateLoansOrLines', 'NumberOfTime60-89DaysPastDueNotWorse',
       'NumberOfDependents', 'IncomePerPerson', 'NumOfPastDue', 'MonthlyDebt',
       'NumOfOpenCreditLines', 'MonthlyBalance', 'age_sqr']

app = Flask(__name__)
app.config["BASIC_AUTH_USERNAME"] = os.environ.get('BASIC_AUTH_USERNAME')
app.config["BASIC_AUTH_PASSWORD"] = os.environ.get('BASIC_AUTH_PASSWORD')

basic_auth = BasicAuth(app)

def load_model(file_name = 'xgboost_undersampling.pkl'):
    return pickle.load(open(file_name, "rb"))

modelo = load_model(file_name = 'models/xgboost_undersampling.pkl')

@app.route("/score/", methods=["POST"])
def get_score():
    dados = request.get_json()
    payload = np.array([dados[col] for col in colunas])
    payload = xgb.DMatrix([payload], feature_names=colunas)
    _score = np.float64(modelo.predict(payload)[0])
    status = "APROVADO"
    if _score <= 0.3:
        status = "REPROVADO"
    elif _score <= 0.6:
        status = "MESA_DE_AVALIACAO"
    resultado = jsonify(cpf=dados["cpf"], score=_score, status=status)
    print(str(resultado))
    return resultado

@app.route("/score/<cpf>")
@basic_auth.required
def show_cpf(cpf):
    print("Recebido: CPF = %s"%cpf)
    return "CPF = %s"%cpf

@app.route("/")
def home():
    print("Executou a rota padrao")
    return "API de predicao pontuacao de credito"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')