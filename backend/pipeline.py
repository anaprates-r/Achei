import os
import pandas as pd
from sqlalchemy import create_engine
from config import app ,db


BASE_PATH = 'uploads'
def processData(fileName):
    dataframe = pd.read_excel(os.path.join(fileName))
    print(dataframe)

    colunas = dataframe.iloc[2,].dropna().to_dict()
    print()
    print()
    print(colunas)
    print()
    print()
    dataframe = dataframe.rename(columns=colunas)


    #____EXTRAÇÃO DA DESCRIÇÃO DOS MEDICAMENTOS____
    medicamentos_df = dataframe[dataframe['Produto'].astype(str).str.contains('BR', case=True, na=False, regex=True)].dropna(axis=1, how='all').reset_index(drop=True)

    medicamentos_df = medicamentos_df.rename(columns={'Produto': 'nome_medicamento'})

    medicamentos_df[['codigo_medicamento','nome_medicamento']] = medicamentos_df['nome_medicamento'].str.split(' ', n=1, expand=True)
    print()
    print()
    print(medicamentos_df)


    #____EXTRAÇÃO DAS QUANTIDADES____
    quantidade_df = dataframe[dataframe['Produto'].astype(str).str.contains('Total', case=True, na=False, regex=True)].dropna(axis=1, how='all').reset_index(drop=True)
    
    quantidade_df = quantidade_df.drop(columns=['Produto'])
    quantidade_df = quantidade_df.rename(columns={ 'Unnamed: 12': 'quantidade'})
    quantidade_df["quantidade"] = quantidade_df["quantidade"].astype(int)
    print()
    print()
    print( quantidade_df )
    # ____MERGE DOS MEDICAMENTOS E SUAS QUANTIDADES___
    medicamentos = pd.merge(medicamentos_df, quantidade_df, left_index=True, right_index=True, how='inner')

    medicamentos = medicamentos[['codigo_medicamento','nome_medicamento','quantidade']]
    
    
    # verifica se há medicamentos duplicados e soma as quantidades
    medicamentos = medicamentos.groupby(['codigo_medicamento', 'nome_medicamento'], as_index=False)['quantidade'].sum()

    #____Extrai o nome do estabelecimento_______
   # 1. Filtra as linhas que contêm 'Estabelecimento'
    # Dica: use copy() para evitar o erro de 'SettingWithCopyWarning' mais tarde
    estabelecimento_row = dataframe[dataframe['Produto'].astype(str).str.contains('Estabelecimento', na=False)].copy()

    if not estabelecimento_row.empty:
        # 2. Faz o split e expand=True transforma em um DataFrame de 2 colunas
        # Ex: "Estabelecimento: Farmácia Central" -> Column 0: "Estabelecimento", Column 1: "Farmácia Central"
        split_data = estabelecimento_row['Produto'].str.split(": ", n=1, expand=True)
        
        # 3. Extrai o nome do campo (chave) e o valor (nome do local)
        # iloc[0] pega a primeira ocorrência encontrada
        # chave_bruta = split_data.iloc[0, 0]
        # chave = chave_bruta.lower().replace(" ", "_")  # "Estabelecimento"
        valor = split_data.iloc[0, 1]  # "Farmácia Central" (ou o que vier após o ":")

        # 4. Atribui ao seu dataframe de medicamentos
        medicamentos['estabelecimento_de_saude'] = valor
        
    else:
        print("Nenhum estabelecimento encontrado no dataframe.")

    print(medicamentos.head())





    #_____SALVA INFORMAÇÕES EM FORMATO JSON NA PASTA DADOS_______

   
    # save_path = 'site_achei/backend/dados'
    # if not os.path.exists(save_path):
    #     os.makedirs(save_path)
    
    # medicamentos.to_json(os.path.join(save_path,'new_data.json'), orient='records')
    # print(quantidade_df)


    #____CARREGA AS INFORMAÇÕES NO BANCO DE DADOS____________

    # Configuração da conexão
    engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    try:
        medicamentos.to_sql('medicamento', con=db.engine, if_exists='replace', index=False)
        print("Pipeline finalizado: Dados inseridos no banco.")
    except Exception as e:
        print(f"Erro ao inserir no banco: {e}")
        raise e # Relança o erro para o Flask capturar no bloco try/except dele


    # print(medicamentos_df)

    #__Salva os dados no bd







