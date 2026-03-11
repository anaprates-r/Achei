# contem os modelos de banco de dados

from config import db

class Medicamento(db.Model):
    codigo_medicamento = db.Column(db.String(50), primary_key=True)
    nome_medicamento = db.Column(db.String(100), unique = False, nullable = False)
    quantidade = db.Column(db.Integer, unique=False, nullable = False)
    estabelecimento_de_saude = db.Column(db.String(200), unique=False, nullable = False)

    def to_json(self):
        return {
            "codigoMedicamento" : self.codigo_medicamento,
            "nomeMedicamento" : self.nome_medicamento,
            "quantidade" : self.quantidade,
            "estabelecimentoSaude": self.estabelecimento_de_saude
        }

