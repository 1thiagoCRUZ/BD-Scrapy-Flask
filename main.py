from flask import Flask, jsonify, render_template, request
import requests
from bs4 import BeautifulSoup
import mysql.connector

app = Flask(__name__)

# Função para conectar ao banco de dados
def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="bd_navarro",
        charset='utf8'
    )

# Função para inserir informações no banco de dados
def inserir_dados_banco(nome_banco, dados):
    conexao = conectar_bd()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO bancos_consultas (nome, data_publicacao, lucro_liquido, patrimonio_liquido, ativo_total, captacoes, carteira_credito_classificada, patrimonio_referencia_rwa, numero_agencias, numero_pontos_atendimento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                   (nome_banco, dados["Publicação"], dados["Lucro Líquido (R$)"], dados["Patrimônio Líquido (R$)"], dados["Ativo Total (R$)"], dados["Captações (R$)"], dados["Carteira de Crédito Classificada (R$)"], dados["Patrimônio de Referência RWA (R$)"], dados["Número de Agências"], dados["Número de Pontos de Atendimento"]))
    conexao.commit()
    conexao.close()

def extrair_infos_ul(sopa_bonita):
    main_info = sopa_bonita.find_all('div', {"main-info"})
    ul = sopa_bonita.find('ul', {"statistics"})
    span_info = ul.find_all('span')
    dados = {}
    for span, valores in zip(span_info, main_info):
        nome_span = span.text.strip()
        nome_val = valores.find('strong').text.strip()
        dados[nome_span] = nome_val
    return dados

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        nome_banco = request.form["nome"]

        conexao = conectar_bd()
        cursor = conexao.cursor()
        cabecalho = {'user-agent': 'Mozilla/5.0'}
        response = requests.get(f"https://www.bancodata.com.br/relatorio/{nome_banco}/", headers=cabecalho)
        sopa_bonita = BeautifulSoup(response.text, 'html.parser')

        dados = extrair_infos_ul(sopa_bonita)
        inserir_dados_banco(nome_banco, dados)
        mensagem = "Banco cadastrado com sucesso no banco de dados!"
        conexao.close()
        return render_template("index.html", mensagem=mensagem)
   
    else:
        return "Acesse esta página através do método POST para cadastrar um banco."


@app.route("/buscar", methods=["GET", "POST"])
def buscar():
    nome_banco = request.form["nome"]

    conexao = conectar_bd()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM bancos_consultas WHERE nome = %s", (nome_banco,))
    resultados = cursor.fetchall()
    conexao.close()

    linhas = []
    for resultado in resultados:
        linha = {
            "nome": resultado[1],
            "data_publicacao": resultado[2],
            "lucro_liquido": resultado[3],
            "patrimonio_liquido": resultado[4],
            "ativo_total": resultado[5],
            "captacoes": resultado[6],
            "carteira_credito_classificada": resultado[7],
            "patrimonio_referencia_rwa": resultado[8],
            "numero_agencias": resultado[9],
            "numero_pontos_atendimento": resultado[10]
        }
        linhas.append(linha)

    return jsonify(linhas)
        

        

if __name__ == "__main__":
    app.run(debug=True)

    
