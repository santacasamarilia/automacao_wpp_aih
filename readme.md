# Agendador de Notificações WhatsApp (Treble.ai)  
Documentação Completa do Script Python

Esta documentação descreve detalhadamente o funcionamento do script Python responsável por **enviar notificações automáticas via WhatsApp utilizando a Treble.ai**, lendo dados do arquivo `test_data.json`, agrupando pacientes por número de celular e médico, e realizando o envio diariamente no horário configurado.

---

## Visão Geral

O script realiza:

1. Carregamento de configurações do arquivo `config.txt`
2. Leitura dos dados de pacientes no `test_data.json`
3. Agrupamento por número de celular (médicos)
4. Construção do payload JSON no formato aceito pela Treble.ai
5. Envio do payload via API Treble.ai
6. Registro de logs diários em `logs/`
7. Execução contínua, verificando a cada segundo se o horário configurado chegou

O objetivo é automatizar lembretes diários de pendências de Laudo AIH.

---

## Estrutura de Arquivos

projeto/
│
├── script.py
├── config.txt
├── test_data.json
└── logs/
└── log-YYYY-MM-DD.txt (gerado automaticamente)


## Arquivo de Configuração (`config.txt`)

Exemplo:

```
API_KEY=Bearer xxxxx
POLL=1120311
HOUR=19
MINUTE=0
```

**Parâmetros:**

| Chave      | Descrição |
|------------|-----------|
| `API_KEY`  | Chave da API da Treble.ai |
| `POLL`     | ID do fluxo (poll ID) |
| `HOUR`     | Hora do envio (0–23) |
| `MINUTE`   | Minuto do envio (0–59) |

---

## Estrutura do `test_data.json`

Exemplo simplificado:

```json
[
    {
        "NUMERO_CELULAR": "14999999999",
        "NM_PRESTADOR": "Dr. João",
        "NM_PACIENTE": "Maria",
        "CD_ATENDIMENTO": 12345,
        "SITUACAO": "PENDENTE"
    }
]
```
Cada linha representa um paciente vinculado a um médico.

# Funções do Script
## `load_config()`

- Carrega API_KEY, horário e minuto do envio.

## `load_test_data()`

- Lê e retorna o conteúdo de test_data.json.

## `group_by_cellphone(rows)`

- Agrupa pacientes por número de celular do médico.

Retorno:
```
{
  "14999999999": {
      "medico": "Dr. João",
      "patients": [
          {
              "patient_name": "...",
              "atendimento": "...",
              "situacao": "..."
          }
      ]
  }
}
```

## `build_payload(grouped)` 

Monta o JSON no formato exigido pela Treble.ai.


