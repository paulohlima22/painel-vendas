import pandas as pd
import yagmail

def enviar_emails():
    df = pd.read_csv('leads.csv')
    yag = yagmail.SMTP("seuemail@gmail.com", "sua_senha_app")

    for _, lead in df.iterrows():
        if lead['Interesse'] == "emagrecimento":
            assunto = "Plano de emagrecimento gratuito"
            conteudo = f"Olá {lead['Nome']}, veja este método: [SEU LINK]"
        elif lead['Interesse'] == "ganhar_dinheiro":
            assunto = "Como fazer R$500 por dia"
            conteudo = f"{lead['Nome']}, conheça o método: [SEU LINK]"
        elif lead['Interesse'] == "beleza":
            assunto = "Segredo da beleza revelado"
            conteudo = f"Olá {lead['Nome']}, veja essa dica: [SEU LINK]"

        yag.send(to=lead['E-mail'], subject=assunto, contents=conteudo)
        print(f"✅ E-mail enviado para {lead['Nome']}")
