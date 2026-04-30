# projeto-edjane

Relatório do Projeto: Sistema de Cadastro de Produtos

Componentes do Grupo:
● Samuel da Rocha Santana
● Arthur Gabriel Silva Pereira
● Luiz Felipe Queiroz Fernandes

1. Descrição do Projeto
O projeto consiste em um aplicativo web desenvolvido em Python utilizando o framework Streamlit para o front-end e SQLite para a persistência de dados. O objetivo é oferecer uma interface intuitiva para o gerenciamento de inventário, permitindo que o usuário realize o ciclo completo de um CRUD (Criação, Leitura, Atualização e Exclusão) de produtos.

2. Funcionalidades Implementadas
● Cadastro de Produtos: Formulário com campos para nome, categoria, preço, quantidade, descrição, URL da imagem e status.
● Listagem Dinâmica: Visualização de todos os itens cadastrados com exibição de imagens e detalhes.
● Edição e Exclusão: Ferramentas para modificar dados existentes ou remover produtos do sistema.
● Filtros e Ordenação: Opções para organizar a visualização por categoria ou critérios específicos.
● Interface Responsiva: Layout que se adapta a diferentes tamanhos de tela.

3. Funcionamento do Armazenamento Local
O sistema utiliza o SQLite como motor de banco de dados local.
● Persistência: Diferente de variáveis temporárias, o SQLite armazena as informações em um arquivo chamado produtos.db na mesma pasta do projeto.
● Integridade: Os dados permanecem salvos mesmo após o encerramento da aplicação ou reinicialização do computador.
● Lógica SQL: O código utiliza comandos SQL (como CREATE TABLE, INSERT, UPDATE e DELETE) para interagir com o arquivo de banco de dados de forma estruturada.