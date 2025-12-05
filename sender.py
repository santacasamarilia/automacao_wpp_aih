import json
import time
import requests
from datetime import datetime
import os

def load_config():
    config = {}
    with open("config.txt", "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line:
                key, val = line.strip().split("=", 1)
                config[key.strip()] = val.strip()

    api_key = config.get("API_KEY", "")
    poll = int(config.get("POLL", 1120311))
    hour = int(config.get("HOUR", 19))
    minute = int(config.get("MINUTE", 0))

    return api_key, hour, minute

def load_test_data():
    with open("test_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

def group_by_cellphone(rows):
    grouped = {}

    for row in rows:
        phone = row["NUMERO_CELULAR"]
        medico = row["NM_PRESTADOR"]

        patient_entry = {
            "patient_name": row["NM_PACIENTE"],
            "atendimento": row["CD_ATENDIMENTO"],
            "situacao": row["SITUACAO"]
        }

        if phone not in grouped:
            grouped[phone] = {"medico": medico, "patients": []}

        grouped[phone]["patients"].append(patient_entry)

    return grouped

def build_payload(grouped):
    SEP = "\u2028"

    users_list = []

    for cellphone, data in grouped.items():
        medico = data["medico"]
        patients = data["patients"]

        patient_text = f"*Pacientes com Laudo AIH Pendente:*{SEP}"

        for p in patients:
            patient_text += (
                f" *{p['patient_name']}* At. {p['atendimento']} - {p['situacao']} |{SEP}{SEP}{SEP}{SEP}"
            )

        users_list.append({
            "cellphone": cellphone,
            "country_code": "+55",
            "user_session_keys": [
                {"key": "nm_medico", "value": medico},
                {"key": "patient_list", "value": patient_text}
            ]
        })

    return {"users": users_list}

def escrever_log(texto):
    os.makedirs("logs", exist_ok=True)
    nome = datetime.now().strftime("logs/log-%Y-%m-%d.txt")
    with open(nome, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().strftime('%H:%M:%S')} - {texto}\n")

def send_to_treble(payload, api_key):
    url = "https://main.treble.ai/deployment/api/poll/1120311"

    headers = {
        "Content-Type": "application/json",
        "Authorization": api_key
    }

    escrever_log("Enviando JSON para a Treble")
    escrever_log("JSON enviado: " + json.dumps(payload, ensure_ascii=False))

    try:
        response = requests.post(url, headers=headers, json=payload)
        escrever_log(f"Status da resposta: {response.status_code}")
        escrever_log("Resposta: " + response.text)
    except Exception as e:
        escrever_log("Erro ao enviar requisição: " + str(e))

def run_forever():
    escrever_log("Agendamento iniciado")

    while True:
        api_key, target_hour, target_minute = load_config()

        escrever_log("Configuração carregada: " + str(load_config()))

        now = datetime.now()

        if now.hour == target_hour and now.minute == target_minute:
            escrever_log("Iniciando envio das notificações")

            try:
                rows = load_test_data()
                escrever_log("Dados carregados do test_data.json")
            except Exception as e:
                escrever_log("Erro ao carregar test_data.json: " + str(e))
                time.sleep(60)
                continue

            grouped = group_by_cellphone(rows)
            payload = build_payload(grouped)

            send_to_treble(payload, api_key)

            escrever_log("Mensagens enviadas. Aguardando 60 segundos")
            time.sleep(60)
            continue

        time.sleep(1)

if __name__ == "__main__":
    run_forever()
