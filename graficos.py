import pandas as pd
import matplotlib.pyplot as plt

def gerar_grafico_interesses():
    df = pd.read_csv('leads.csv')
    contagem = df['Interesse'].value_counts()

    plt.figure(figsize=(6, 4))
    contagem.plot(kind='bar', color='skyblue')
    plt.title('Distribuição de Interesses dos Leads')
    plt.xlabel('Interesse')
    plt.ylabel('Quantidade')
    plt.tight_layout()
    plt.savefig('static/grafico_interesse.png')
