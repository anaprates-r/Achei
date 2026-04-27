from processamento_2 import limpeza_dos_dados
def etl(fileName):
    df_limpo = limpeza_dos_dados(fileName)

    with app.app_context():
        # Carrega tudo do banco de uma vez
        existentes = {
            (m.catmat, m.estabelecimento_saude): m
            for m in Medicamento.query.all()
        }

        novos = []

        # sem query no banco
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
                novos.append(novo)

        # 3. Insere tudo de uma vez
        db.session.bulk_save_objects(novos)

        db.session.commit()
