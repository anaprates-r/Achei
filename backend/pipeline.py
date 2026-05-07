from processamento_2 import limpeza_dos_dados
# from processamento import processar_r84
from models import Medicamento
from config import db, app

def etl(fileName):
    df_limpo = limpeza_dos_dados(fileName)
    df_limpo = df_limpo.fillna('')

    with app.app_context():
        print("Carregando registros existentes...")

        existentes = {
            (m.catmat, m.estabelecimento_saude): m
            for m in Medicamento.query.all()
        }

        novos = []
        contador = 0

        print("Processando DataFrame...")

        for _, row in df_limpo.iterrows():
            chave = (row['catmat'], row['estabelecimento_saude'])

            if chave in existentes:
                existente = existentes[chave]
                existente.quantidade = row['quantidade']
                existente.medicamento = row['medicamento']
            else:
                novos.append(Medicamento(
                    catmat=row['catmat'],
                    medicamento=row['medicamento'],
                    quantidade=row['quantidade'],
                    estabelecimento_saude=row['estabelecimento_saude']
                ))
            contador += 1
            
            # commit em lote
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

