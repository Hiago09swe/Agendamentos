# 📅 Sistema de Agendamento de Instalações

Este é um sistema web simplificado e eficiente para gerenciar agendamentos de serviços técnicos, focado em agilidade e organização. Desenvolvido com **Python** e **Streamlit**, ele permite cadastrar veículos, locais, clientes e técnicos, mantendo tudo salvo em um banco de dados local (CSV).

## 🚀 Funcionalidades

* **Cadastro de Agendamentos:** Interface amigável para inserir novos serviços.
* **Visualização em Cards:** Lista organizada em tons de azul para fácil leitura.
* **Botão de Concluir:** Remove serviços da lista assim que finalizados.
* **Links Diretos:** Integração com links do Google Maps para facilitar o deslocamento do técnico.
* **Persistência de Dados:** Os dados não somem ao fechar o navegador, pois ficam salvos no arquivo `agendamentos.csv`.

## 🛠️ Tecnologias Utilizadas

* [Python](https://www.python.org/)
* [Streamlit](https://streamlit.io/) (Interface Web)
* [Pandas](https://pandas.pydata.org/) (Manipulação de Dados)

## 📦 Como Instalar e Rodar

Siga os passos abaixo para rodar o projeto localmente no seu VS Code:

1.  **Clone o repositório ou baixe os arquivos.**
2.  **Instale as dependências necessárias:**
    ```bash
    pip install streamlit pandas
    ```
3.  **Certifique-se de que o logo está na pasta:**
    O arquivo de imagem deve se chamar `logo_empresa.png`.
4.  **Execute o sistema:**
    ```bash
    streamlit run app.py
    ```
    *Nota: Não rode usando o botão "Play" do Python ou o comando `python app.py`. Use sempre o comando do streamlit acima.*

## 📂 Estrutura do Projeto

* `app.py`: Código fonte principal do sistema.
* `logo_empresa.png`: Logomarca exibida no painel.
* `agendamentos.csv`: Arquivo onde os dados são armazenados (gerado automaticamente).
* `requirements.txt`: Lista de bibliotecas para instalação rápida.

---
Desenvolvido para otimizar a rotina de instalações técnicas.
