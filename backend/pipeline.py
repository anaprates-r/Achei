from processamento_2 import limpeza_dos_dados
from models import Medicamento
from config import db, app

BATCH_SIZE = 500

def etl(fileName):
    df_limpo = limpeza_dos_dados(fileName)
    df_limpo = df_limpo.fillna('')

    with app.app_context():

        print("Carregando registros existentes...")

        existentes = {}

        for m in db.session.query(Medicamento).yield_per(1000):
            chave = (m.catmat, m.estabelecimento_saude)
            existentes[chave] = m

        novos = []
        contador = 0
        atualizados = 0
        inseridos = 0

        print("Processando DataFrame...")

        for _, row in df_limpo.iterrows():

            chave = (row['catmat'], row['estabelecimento_saude'])

            if chave in existentes:

                existente = existentes[chave]

                existente.quantidade = row['quantidade']
                existente.medicamento = row['medicamento']

                atualizados += 1

            else:

                novo = Medicamento(
                    catmat=row['catmat'],
                    medicamento=row['medicamento'],
                    quantidade=row['quantidade'],
                    estabelecimento_saude=row['estabelecimento_saude']
                )

                novos.append(novo)

                existentes[chave] = novo

                inseridos += 1

            contador += 1

            if contador % BATCH_SIZE == 0:

                if novos:
                    db.session.bulk_save_objects(novos)
                    novos = []

                db.session.commit()

                print(f"Lote {contador} processado")

        if novos:
            db.session.bulk_save_objects(novos)

        db.session.commit()

        print("ETL finalizado")
        print(f"Atualizados: {atualizados}")
        print(f"Inseridos: {inseridos}")
        print(f"Total processado: {contador}")
