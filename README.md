# 🎉 Sistema de Enquetes em Tempo Real 🗳️

Bem-vindo ao **Sistema de Enquetes em Tempo Real**! Este projeto permite que os usuários criem enquetes e votem em tempo real, tornando-o perfeito para eventos, reuniões ou apenas para se divertir! 🚀

## 📦 Funcionalidades

- **Criar Enquetes**: Crie facilmente enquetes com várias opções! 📝
- **Votação em Tempo Real**: Vote e veja os resultados atualizarem em tempo real! 📊
- **Integração com WebSocket**: Gerencie conexões ao vivo para atualizações instantâneas! 🔗
- **Interface Bonita**: Uma interface simples e limpa para melhorar a experiência do usuário! 🎨

## 🚀 Começando

Siga estes passos para configurar o projeto localmente:

### Pré-requisitos

Certifique-se de ter o seguinte instalado:

- Python 3.8+
- pip

### 🔧 Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/thaleson/Real-Time_Polling_System.git
   cd Real-Time_Polling_System
   ```

2. Crie um ambiente virtual:

   ```bash
   python -m venv venv
   ```

3. Ative o ambiente virtual:

   - No Windows:
     ```bash
     venv\Scripts\activate
     ```

   - No macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Instale os pacotes necessários:

   ```bash
   pip install -r requirements.txt
   ```

### 🏃‍♂️ Executando a Aplicação

1. Certifique-se de que seu banco de dados esteja configurado (o padrão é SQLite).
2. Inicie o servidor FastAPI:

   ```bash
   uvicorn app.main:app --reload
   ```

3. Abra seu navegador e acesse [http://127.0.0.1:8000](http://127.0.0.1:8000) para acessar o sistema de enquetes! 🌐

## 📚 Endpoints da API

- `POST /polls/`: Criar uma nova enquete.
- `GET /polls/{poll_id}`: Recuperar uma enquete específica.
- `POST /polls/{poll_id}/vote/`: Votar em uma enquete específica.
- `GET /`: Servir a interface principal de enquetes.

## 👥 Contribuindo

Agradecemos por suas contribuições! Se você deseja contribuir, por favor, faça um fork do repositório e envie um pull request. Sua ajuda é muito apreciada! ❤️

## 📄 Licença

Este projeto é licenciado sob a Licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.



## 🎈 Aproveite a votação! 🗳️

