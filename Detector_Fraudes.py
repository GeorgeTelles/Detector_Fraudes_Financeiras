import pandas as pd
import time
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True) 

class FraudDetector:
    def __init__(self, data_path):
        self.data = pd.read_excel(data_path)
        self.user_profiles = {}
        self.alert_count = 0
        
        # Pré-processamento inicial
        self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])
        self.data = self.data.sort_values('timestamp')
        
    def _update_user_profile(self, transaction):
        user_id = transaction['user_id']
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {
                'transaction_count': 0,
                'avg_amount': 0,
                'common_country': transaction['pais'],
                'common_device': transaction['dispositivo'],
                'last_transaction_time': None
            }
        
        profile = self.user_profiles[user_id]
        
        # Atualizar média de valores
        profile['transaction_count'] += 1
        profile['avg_amount'] = ((profile['avg_amount'] * (profile['transaction_count'] - 1) + 
                                transaction['valor']) / profile['transaction_count'])
        
        # Atualizar país e dispositivo mais comum
        if transaction['pais'] != profile['common_country']:
            profile['common_country'] = max(
                [profile['common_country'], transaction['pais']],
                key=lambda x: list(self.data[self.data['user_id'] == user_id]['pais']).count(x)
            )
        
        if transaction['dispositivo'] != profile['common_device']:
            profile['common_device'] = max(
                [profile['common_device'], transaction['dispositivo']],
                key=lambda x: list(self.data[self.data['user_id'] == user_id]['dispositivo']).count(x)
            )
        
        profile['last_transaction_time'] = transaction['timestamp']

    def _check_anomalies(self, transaction):
        alerts = []
        user_id = transaction['user_id']
        profile = self.user_profiles.get(user_id, {})

        # 1. Valor muito acima da média
        if transaction['valor'] > 3 * profile.get('avg_amount', 0):
            alerts.append(f"Valor {transaction['valor']} > 3x média do usuário ({profile['avg_amount']:.2f})")

        # 2. Mudança de país
        if transaction['pais'] != profile.get('common_country', 'N/A'):
            alerts.append(f"País incomum: {transaction['pais']} (esperado: {profile['common_country']})")

        # 3. Dispositivo diferente
        if transaction['dispositivo'] != profile.get('common_device', 'N/A'):
            alerts.append(f"Dispositivo incomum: {transaction['dispositivo']}")

        # 4. Horário incomum (00h-05h)
        if transaction['timestamp'].hour < 5:
            alerts.append(f"Horário suspeito: {transaction['timestamp'].strftime('%H:%M')}")

        # 5. Categorias de risco
        if transaction['categoria'] in ['Viagens', 'Eletrônicos']:
            alerts.append(f"Categoria de alto risco: {transaction['categoria']}")

        return alerts

    def simulate_real_time_detection(self, delay=1):
        print(Fore.CYAN + "\nIniciando monitoramento de transações em tempo real...\n")
        
        for idx, row in self.data.iterrows():
            transaction = row.to_dict()
            
            # Simular fluxo em tempo real
            time.sleep(delay)
            
            # Atualizar perfil do usuário
            self._update_user_profile(transaction)
            
            # Verificar anomalias
            alerts = self._check_anomalies(transaction)
            
            if alerts:
                self.alert_count += 1
                self._print_alert(transaction, alerts)
                
            if (idx + 1) % 10 == 0:
                print(Fore.YELLOW + f"\nProgresso: {idx + 1}/{len(self.data)} transações analisadas | Alertas: {self.alert_count}")

        print(Fore.GREEN + "\nMonitoramento concluído!")

    def _print_alert(self, transaction, reasons):
        print(Fore.RED + "\n" + "═" * 60)
        print(Fore.RED + Style.BRIGHT + "⚠ ALERTA DE FRAUDE POTENCIAL ⚠")
        print(Fore.WHITE + f"Transação ID: {transaction['transaction_id']}")
        print(Fore.WHITE + f"Usuário: {transaction['user_id']} | Valor: {transaction['valor']} | Data: {transaction['timestamp']}")
        print(Fore.WHITE + f"Comerciante: {transaction['comerciante']} ({transaction['categoria']})")
        
        print(Fore.YELLOW + "\nMotivos do alerta:")
        for i, reason in enumerate(reasons, 1):
            print(Fore.YELLOW + f"{i}. {reason}")
        
        print(Fore.RED + "═" * 60 + "\n")

if __name__ == "__main__":
    detector = FraudDetector("transacoes.xlsx")
    detector.simulate_real_time_detection(delay=2)