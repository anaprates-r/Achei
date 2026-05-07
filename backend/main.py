# contem as rotas e endpoints
from flask import request, jsonify
from config import app,db
from models import Medicamento
from pipeline import etl
import traceback
import threading

import os
etl_rodando = False

@app.route('/')
def index_page():
    return "<h1> Flask API </h1>"
@app.route('/medicamentos', methods=['GET'])
def listar_medicamentos():
    # 1. Captura parâmetros de paginação
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int) # Itens por página

    # 2. Inicia a query base
    query = Medicamento.query

    # 3. Aplica os filtros dinâmicos (Catmat, estabelecimento, Busca)
    catmat = request.args.get('catmat')
    estabelecimento = request.args.get('estabelecimento')
    q = request.args.get('q')

    if catmat:
        query = query.filter(Medicamento.catmat.ilike(f"%{catmat}%"))
    if estabelecimento:
        query = query.filter(Medicamento.estabelecimento_saude.ilike(f"%{estabelecimento}%"))
    if q:
        query = query.filter(Medicamento.medicamento.ilike(f"%{q}%"))

    # 4. Aplica a PAGINAÇÃO no final da query filtrada
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    # 5. Monta a resposta com metadados
    return jsonify({
        "items": [m.to_json() for m in pagination.items],
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": pagination.page,
        "has_next": pagination.has_next,
        "has_prev": pagination.has_prev
    })

@app.route('/estabelecimentos', methods=['GET'])
def listar_estabelecimentos_unicas():
    # Busca apenas a coluna 'estabelecimento', remove duplicatas e ordena
    estabelecimentos = db.session.query(Medicamento.estabelecimento_saude).distinct().order_by(Medicamento.estabelecimento_saude).all()
    # Retorna uma lista simples: ["UBS Centro", "Hospital Norte", ...]
    return jsonify([u[0] for u in estabelecimentos if u[0]])

@app.route('/upload', methods=['POST', 'OPTIONS'])
def upload():

    global etl_rodando

    # CORS preflight
    if request.method == 'OPTIONS':
        return '', 200

    # impede múltiplos ETLs simultâneos
    if etl_rodando:
        return jsonify({
            "message": "ETL já está em execução"
        }), 400

    # validação arquivo
    if 'file' not in request.files:
        return jsonify({
            "message": "Nenhum arquivo enviado"
        }), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({
            "message": "Arquivo sem nome"
        }), 400

    try:
        # cria pasta uploads
        upload_path = app.config['UPLOAD_FOLDER']

        if not os.path.exists(upload_path):
            os.makedirs(upload_path)

        # salva arquivo
        file_path = os.path.join(
            upload_path,
            file.filename
        )

        file.save(file_path)

        # trava ETL
        etl_rodando = True

        # inicia thread
        thread = threading.Thread(
            target=rodar_etl_background,
            args=(file_path,),
            name="etl-thread"
        )

        thread.daemon = True
        thread.start()

        return jsonify({
            "message": "ETL iniciado com sucesso"
        }), 201
    except Exception as e:
        etl_rodando = False
        traceback.print_exc()
        return jsonify({
            "message": f"Erro ao iniciar ETL: {str(e)}"
        }), 500


def rodar_etl_background(file_path):
    global etl_rodando
    try:
        print(" ETL iniciado em background")
        etl(fileName=file_path)
        print("ETL finalizado")
    except Exception as e:
        print("❌ ERRO NO ETL")
        traceback.print_exc()
    finally:
        etl_rodando = False
        print("Flag ETL liberada")

#To run the aplication:
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
