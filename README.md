# Automação de Coleta de Dados de Máquinas com Ansible e MongoDB

## Visão Geral
Este repositório contém a lógica de automação e o script Python para coletar informações de hardware e sistema operacional de máquinas Linux (e estender em VMs) e armazená-las de forma estruturada em um banco de dados MongoDB.

O deployment do projeto no servidor de destino é totalmente gerenciado pelo Ansible, garantindo segurança e idempotência.

### Como Executar o Deployment

- Pré-requisitos
Ansible instalado no controlador (sua máquina).
- MongoDB instalado e configurado (com autenticação ativada) no servidor de destino.
- Conexão SSH configurada para o servidor de destino (ou localhost).

```bash
ansible-playbook playbooks/deploy_scripts.yml --ask-become-pass 
```
- so colocar a senha definida na variavel 

### Tecnologias Utilizadas
- **Automação:** Ansible 2.9+
- **Segurança:** Ansible Vault (criptografia de segredos)
- **Linguagem:** Python 3.x
- **Dependências Python:** pymongo, python-dotenv
- **Banco de Dados:** MongoDB
- **Agendamento:** Cron

### Estrutura do Repositório
```
/datalake-playbooks/
├── playbooks/
│   └── deploy_scripts.yml     
├── vars/
│   └── info_maquina.yml        
├── role/
│   ├── xerlock.info_maquina/
│   ├── main.yml              
│   ├── files/
│   │   ├── .env
│   │   ├── dados_maquina.py    
│   │   ├── requirements.txt
│   │   ├── run.sh     
│   ├── template/
│   │   ├── env.j2
│   └── run.sh                  
├── .gitignore                  
└── README.md
```


### Passos
- Configurar o Ansible Vault:
Crie o arquivo de segredos (será solicitada uma senha):
```Bash
ansible-vault encrypt info_maquina.yml
```


### Insira as variáveis de conexão do MongoDB (com credenciais fortes) neste arquivo:

```YAML
mongo_user: "root" # (Ajustar para usuário com menos privilégios em produção)
mongo_password: "SUA_SENHA_FORTE" 
mongo_host_port: "localhost:27017"
```
### Utilizando e fazendo uma query via mongosh:
```bash
mongosh

show dbs
db.maquina_dados.find().pretty()
```
