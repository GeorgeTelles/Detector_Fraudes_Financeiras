import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()
np.random.seed(42)

NUM_USERS = 2500
TRANS_PER_USER_MIN = 4
TRANS_PER_USER_MAX = 15
FILENAME = "transacoes.xlsx"

users = [{
    "user_id": f"USR{str(i).zfill(5)}",
    "pais_base": fake.country_code(),
    "dispositivo_base": fake.user_agent(),
    "media_valor": np.random.lognormal(mean=4.5, sigma=1.2)
} for i in range(NUM_USERS)]

paises = ['US', 'CA', 'GB', 'FR', 'DE', 'BR', 'RU', 'CN', 'JP', 'MX']
categorias = ['Eletrônicos', 'Varejo', 'Viagens', 'Serviços', 'Alimentos']

def gerar_transacoes_usuario(user):
    num_trans = np.random.randint(TRANS_PER_USER_MIN, TRANS_PER_USER_MAX)
    transacoes = []
    
    for _ in range(num_trans):
        data = fake.date_time_between(start_date="-180d", end_date="now")
        
        transacao = {
            "transaction_id": f"TX{fake.unique.random_number(digits=8)}",
            "timestamp": data,
            "user_id": user['user_id'],
            "valor": round(abs(np.random.normal(user['media_valor'], user['media_valor']/3))), 
            "comerciante": fake.company(),
            "categoria": np.random.choice(categorias, p=[0.15, 0.35, 0.1, 0.25, 0.15]),
            "pais": user['pais_base'] if np.random.rand() > 0.1 else np.random.choice(paises),
            "dispositivo": user['dispositivo_base'] if np.random.rand() > 0.05 else fake.user_agent(),
            "ip": fake.ipv4(),
            "is_fraud": 0  
        }
        
        transacoes.append(transacao)
    
    return transacoes

# Gerar todas as transações
todas_transacoes = []
for usuario in users:
    todas_transacoes.extend(gerar_transacoes_usuario(usuario))

df = pd.DataFrame(todas_transacoes)

# Simular padrões de fraude 
fraude_mask = (
    (df['valor'] > df.groupby('user_id')['valor'].transform('mean') * 4) |
    (df['pais'] != df.groupby('user_id')['pais'].transform('first')) |
    (df['dispositivo'].str.contains('Unknown|Emulator')) |
    (df['categoria'].isin(['Viagens', 'Eletrônicos']))
) & (np.random.rand(len(df)) < 0.02) 

df['is_fraud'] = np.where(fraude_mask, 1, 0)

# Reordenar e salvar
df = df.sort_values(['user_id', 'timestamp']).reset_index(drop=True)
df.to_excel(FILENAME, index=False)

print(f"Dataset gerado: {FILENAME}")
print(f"Estatísticas:\n{df['is_fraud'].value_counts(normalize=True)}")
print(f"Exemplo de usuário:\n{df[df['user_id'] == 'USR00042'][['timestamp', 'valor', 'categoria', 'is_fraud']]}")