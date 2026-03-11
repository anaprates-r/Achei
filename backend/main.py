# contem as rotas e endpoints
from flask import request, jsonify
from config import app,db
from models import Medicamento
from pipeline import processData

import os
print("INICIANDO SERVIDOR")
@app.route("/medicamento", methods=["GET"])
def get_medicamento():
    medicamento = Medicamento.query.all()
    json_medicamento = list(map(lambda x: x.to_json(), medicamento))
    return jsonify({"Medicamento":json_medicamento})

@app.route("/create_medicamento", methods =["POST"])
def create_medicamento():
    codigo_medicamento = request.json.get("codigoMedicamento")
    nome_medicamento = request.json.get("nomeMedicamento")
    quantidade = request.json.get("quantidade")
    estabelecimento_de_saude = request.json.get("estabelecimentoSaude")


    if not codigo_medicamento or not nome_medicamento or not quantidade:
        return (
            jsonify({"message": "Você precisa inserir o codigo, nome e quantidade do medicamento"}),400,#Mensagem de erro
        )
    
    novo_medicamento = Medicamento(
        codigo_medicamento=codigo_medicamento,
        nome_medicamento=nome_medicamento,
        quantidade=quantidade,
        estabelecimento_de_saude = estabelecimento_de_saude
    )

    try: 
        db.session.add(novo_medicamento)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "message": str(e) #mensagem de erro
            }
        ),400
    
    return jsonify(
        {
            "message": "Medicamento criado" # Mensagem sucesso
        }
    ),201
    
@app.route("/update_medicamento/<string:codigo_medicamento>", methods=["PATCH"])
def update_content(codigo_medicamento):
    medicamento = Medicamento.query.get(codigo_medicamento)

    if not Medicamento:
        return jsonify(
            {
                "message": "Medicamento não encontrado" #mensagem de erro
            }
        ),404
    
    data = request.json
    medicamento.nome_medicamento = data.get("nomeMedicamento", medicamento.nome_medicamento)
    medicamento.quantidade = data.get("quantidade", medicamento.quantidade)

    db.session.commit()

    return jsonify(
        {
            "Message": "Medicamento atualizado"
        }
    )
    

@app.route("/delete_medicamento/<string:codigo_medicamento>", methods =["DELETE"])
def delete_medicamento(codigo_medicamento):
    medicamento = Medicamento.query.get(codigo_medicamento)

    if not Medicamento:
        return jsonify(
            {
                "message": "Medicamento não encontrado" #mensagem de erro
            }
        ),404
        
    db.session.delete(medicamento)
    db.session.commit()

    return jsonify({
        "message": "Medicamento deletado"
    })

import os
from flask import request, jsonify

@app.route("/upload", methods=["POST"])
def upload():
    # 1. Validação do arquivo
    if 'file' not in request.files:
        return jsonify({"message": "Nenhum arquivo enviado"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "Arquivo sem nome"}), 400

    # 2. Caminhos (backend/uploads)
    upload_path = os.path.join("uploads")
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)

    file_path = os.path.join(upload_path, file.filename)
    file.save(file_path)

    try:
        # 3. O Pipeline aciona o Banco de Dados
        # Passe o caminho completo do arquivo para o seu processador
        processData(fileName=file_path) 

        # 4. Retorno de sucesso para o React
        # O React receberá esse 201 e saberá que os dados já estão no banco
        return jsonify({
            "message": "Arquivo processado e dados salvos no banco com sucesso!"
        }), 201

    except Exception as e:
        # Se o banco de dados falhar, o erro cai aqui
        print(f"Erro no pipeline: {e}")
        return jsonify({"message": f"Erro ao salvar no banco: {str(e)}"}), 500



#To run the aplication:
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)


