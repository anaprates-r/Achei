from processamento_2 import limpeza_dos_dados
# from processamento import processar_r84
from models import Medicamento
from config import db, app

def etl(fileName):
    df_limpo = limpeza_dos_dados(fileName)
    df_limpo = df_limpo.fillna('')

    with app.app_context():
        existentes = {
            (m.catmat, m.estabelecimento_saude): m
            for m in Medicamento.query.all()
        }

        for _, row in df_limpo.iterrows():
            chave = (row['catmat'], row['estabelecimento_saude'])

            if chave in existentes:
                existente = existentes[chave]
                existente.quantidade = row['quantidade']
                existente.medicamento = row['medicamento']
            else:
                novo = Medicamento(
                    catmat=row['catmat'],
                    medicamento=row['medicamento'],
                    quantidade=row['quantidade'],
                    estabelecimento_saude=row['estabelecimento_saude']
                )
                db.session.add(novo)

        db.session.commit()
