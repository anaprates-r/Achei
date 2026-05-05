from processamento_2 import limpeza_dos_dados
# from processamento import processar_r84
from models import Medicamento
from config import db, app

def etl(fileName):
    # Chama o processamento do arquivo e retorna um DataFrame limpo
    print("1. Iniciando ETL")
    df_limpo = limpeza_dos_dados(fileName)
    print("2. DataFrame carregado")
    df_limpo = df_limpo.head(100)

    print("Total de linhas após limite:", len(df_limpo))

    df_limpo = df_limpo.fillna('')
    print(df_limpo.head())
    
    with app.app_context():
        for _, row in df_limpo.iterrows():
            # Busca se o par (catmat, estabelecimento) já existe
            existente = Medicamento.query.filter_by(
                catmat=row['catmat'], 
                estabelecimento_saude=row['estabelecimento_saude']
            ).first()

            if existente:
                # Atualiza a quantidade se já existir
                existente.quantidade = row['quantidade']
                existente.medicamento = row['medicamento']
            else:
                # Cria novo se não existir
                novo = Medicamento(
                    catmat=row['catmat'],
                    medicamento=row['medicamento'],
                    quantidade=row['quantidade'],
                    estabelecimento_saude=row['estabelecimento_saude']
                )
                db.session.add(novo)
        
        db.session.commit()
