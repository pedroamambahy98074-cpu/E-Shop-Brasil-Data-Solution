# Aplicação Prática de Tecnologias de Banco de Dados e Big Data na E-Shop Brasil

## Introdução: Contexto do Problema e Objetivos

Este projeto foi desenvolvido para atender ao desafio proposto pela **E-Shop Brasil**, uma grande plataforma de comércio eletrônico que enfrenta desafios na **gestão eficiente de dados** e na **otimização logística** devido ao seu crescimento exponencial.

O objetivo principal é demonstrar uma solução escalável e flexível, utilizando tecnologias de bancos de dados avançados e Big Data, que permita à equipe de TI da E-Shop Brasil:

1.  **Gerenciar** grandes volumes de dados de clientes e pedidos de forma eficiente.
2.  **Analisar** e **manipular** esses dados para suportar a personalização da experiência do cliente e a otimização da cadeia de suprimentos.
3.  Garantir a **segurança** e a **escalabilidade** da infraestrutura de dados.

## Tecnologias Utilizadas

Para simular um ambiente de Big Data e atender aos requisitos de flexibilidade e escalabilidade, a solução foi construída utilizando as seguintes tecnologias:

| Tecnologia | Função |
| :--- | :--- |
| **Docker** | Containerização do ambiente, garantindo portabilidade e fácil replicação. |
| **MongoDB** | Banco de Dados NoSQL (Documento), escolhido por sua flexibilidade de esquema e alta escalabilidade horizontal, ideal para dados de catálogo de produtos e perfis de clientes. |
| **Streamlit** | Framework Python para criação rápida de interfaces web interativas, servindo como a interface gráfica para a equipe de TI visualizar e manipular os dados. |
| **Python** | Linguagem de programação principal para o desenvolvimento da lógica de manipulação e análise de dados. |

## Descrição da Aplicação

A aplicação, desenvolvida em Python com Streamlit (`app.py`), interage com um banco de dados MongoDB para simular operações críticas de gestão de dados em um cenário de e-commerce.

### 1. Inserção de Dados no MongoDB

A aplicação permite a **inserção de dados** simulados de clientes e pedidos. Os dados são estruturados em formato JSON (documentos), aproveitando a natureza flexível do MongoDB.

### 2. Manipulação e Concatenação de Dados

A interface oferece funcionalidades para:

*   **Edição e Exclusão:** Modificação e remoção de documentos (registros) no banco de dados.
*   **Concatenação de Dados:** Simulação de operações de *join* ou agregação, onde dados de diferentes coleções (ex: `clientes` e `pedidos`) são combinados para gerar *insights* (ex: "Valor total gasto por cliente").

### 3. Realização de Consultas e Exibição na Interface Gráfica

A aplicação permite a execução de **consultas** complexas (simulando a análise de Big Data) e exibe os resultados de forma clara e interativa na interface Streamlit, facilitando a tomada de decisão pela equipe de TI.

## Comandos para Execução

O ambiente é totalmente containerizado para facilitar a execução.

### Pré-requisitos

Certifique-se de ter o **Docker** e o **Docker Compose** instalados em sua máquina.

### 1. Inicialização do Ambiente

Execute o comando abaixo na raiz deste repositório para construir as imagens e iniciar os contêineres do MongoDB e do Streamlit:

```bash
docker-compose up --build
```

Este comando fará o seguinte:
*   Baixará a imagem oficial do MongoDB.
*   Construirá a imagem da aplicação Streamlit, instalando as dependências necessárias.
*   Iniciará os dois serviços, conectando-os na mesma rede Docker.

### 2. Acesso à Aplicação

Após a inicialização, a aplicação Streamlit estará acessível no seu navegador. O terminal indicará a porta, mas por padrão, ela estará em:

[http://localhost:8501](http://localhost:8501)

### 3. Parada do Ambiente

Para parar e remover os contêineres:

```bash
docker-compose down
```

## Testes e Exemplos

Os exemplos de uso (prints de tela ou GIFs) serão fornecidos na pasta `exemplos/` e demonstrarão as seguintes funcionalidades:

*   **Tela Inicial:** Apresentação da interface.
*   **Inserção de Dados:** Demonstração da criação de um novo registro de cliente.
*   **Consulta Agregada:** Exibição de um gráfico ou tabela resultante de uma consulta que concatena dados de pedidos e clientes.
*   **Edição/Exclusão:** Prova da manipulação de um registro existente.
