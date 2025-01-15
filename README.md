# Cryptotracker

Este é um projeto pessoal que fiz com objetivos de estudo. Nele, pude me aprofundar em conceitos como:  
**Django Avançado** (Channels), **Celery**, **Webhooks**, **Services**, **Notificações em Tempo Real** (WebSockets) e muito mais.  
Espero que goste do resultado! 🚀

---

## Próximas Atualizações  
- Adicionar na tela de detalhes um **gráfico** para acompanhar visualmente o histórico de preços e a taxa de variação da criptomoeda.

---

## Configuração do Projeto

O processo de configuração pode ser um pouco trabalhoso inicialmente, mas prometo que valerá a pena!

### 1. Rodar os containers necessários  
- **Redis**:  
  ```
  docker run --rm -p 6379:6379 redis:7
  ```
- **RabbitMQ**:  
  ```
  docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:4.0-management
  ```

### 2. Configuração de Ambiente Virtual  
Devido a problemas de compatibilidade com Windows, recomenda-se usar Mac/Linux ou o **WSL** no Windows.  

#### Criar e ativar o ambiente virtual:  
1. Na pasta `cryptotracker_app`:  
   ```
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```  
2. Na pasta `notify_alert`:  
   Repita o mesmo processo acima.  

---

### 3. Ativando o Celery  
Certifique-se de que os containers do Redis e RabbitMQ estejam ativos. Em seguida, rode os comandos a partir da pasta `cryptotracker_app`:  

- **Celery Worker**:  
  ```
  celery -A core worker -l INFO
  ```  
- **Celery Beat (Scheduler)**:  
  ```
  celery -A core beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
  ```

---

### 4. Migrar e configurar o projeto  
1. Rode as migrações:  
   ```
   python manage.py migrate
   ```  
   Faça isso tanto em `cryptotracker_app` quanto em `notify_alert`.

2. Configure os arquivos `.env`:  
   Crie os arquivos `.env` nas pastas `cryptotracker_app` e `notify_alert`, baseando-se nos exemplos fornecidos em `.env.example`.  

3. Obtenha a chave de API no [CoinGecko](https://www.coingecko.com/en/api) (é gratuito!) e configure o Webhook em [Webhook.site](https://webhook.site/).  

4. Importe as criptomoedas:  
   ```
   python manage.py import_cryptos
   ```

---

### 5. Iniciar os servidores  
- **Servidor do `notify_alert`**:  
  ```
  python manage.py runserver 8001
  ```  
- **Servidor do `cryptotracker_app`** (porta padrão):  
  ```
  python manage.py runserver
  ```

---

### 6. Configurar o Scheduler no Django Admin  
1. Crie um superusuário:  
   ```
   python manage.py createsuperuser
   ```  
2. Acesse o painel de administrador:  
   - URL: `localhost:8000/admin`  
   - Faça login com o superusuário e configure um **scheduler personalizado** na área do **Django Celery Beat**.

---

Agora, a aplicação está pronta para uso! 🎉

> **Nota:** As instalações de dependências, importações e migrações só precisam ser feitas na primeira vez.
