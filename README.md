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
├── inventory/
│   └── teste.yml
├── playbooks/
│   └── deploy_scripts.yml            
├── role/
│   ├── xerlock.info_maquina/
│   ├── tasks/
│   │   ├── cron.yml
│   │   ├── deps.yml
│   │   ├── env.yml
│   │   ├── exec.yml
│   │   ├── main.yml
│   │   ├── run.yml
│   │   ├── setup.yml
│   │   ├── venv.yml
│   ├── files/
│   │   ├── .env
│   │   ├── dados_maquina.py    
│   │   ├── requirements.txt
│   │   ├── run.sh     
│   ├── template/
│   │   ├── env.j2
├── vault/
│   └── info_maquina.yml                   
├── .gitignore                  
└── README.md
└── vagrantfile
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
# **Melhorias**

### Instalação do mongodb via ansible no master

#### Instalando mongodb na vm master manualmente

- Importar a chave GPG oficial
```bash
curl -fsSL https://pgp.mongodb.com/server-6.0.asc | sudo gpg -o /usr/share/keyrings/mongodb-server-6.0.gpg --dearmor
```

- Adicionar o repositório (usando o de Jammy)
- **“jammy” = Ubuntu 22.04 — compatível com Ubuntu 24.04**

```bash
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
```

- Atualizar pacotes e instalar
```bash
sudo apt update
sudo apt install -y mongodb-org
```

- Habilitar e iniciar o serviço

```bash
sudo systemctl enable mongod
sudo systemctl start mongod
```

- Verificar status
```bash
sudo systemctl status mongod
```

# Correções manuais momentaneas que irão ser via ansible 
```bash
sudo chown -R vagrant:vagrant /opt/info_maquina
sudo chmod -R 755 /opt/info_maquina

cd /opt/info_maquina
source venv/bin/activate
python dados_maquina.py
deactivate

sudo vim /etc/mongod.conf

cat /etc/mongod.conf 
```

# network interfaces

```bash
cat /etc/mongod.conf # Precisa editar isso, talvez vou colocar um script ou template aqui 
```

```
net:
  port: 27017
  bindIp: 0.0.0.0 # Aqui precisa ser 0.0.0.0 para rodar via vagrant 
```  
