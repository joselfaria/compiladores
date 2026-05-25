# Compilador C Simplificado (UFSJ)

Este repositório contém o desenvolvimento de um compilador para uma linguagem baseada em C simplificado, realizado como parte da disciplina de Compiladores ministrada pelo Professor **Flavio Schiavoni** na **UFSJ**.

## 🚀 Objetivo do Projeto

O objetivo é construir progressivamente um compilador durante ao longo da disciplina.

## 📂 Estrutura do Projeto

-   `a-lex.py`: Analisador Léxico (Scanner). Identifica tokens como palavras reservadas, identificadores, números, operadores e literais.
-   `codigo1.c` a `codigo8.c`: Arquivos de teste contendo exemplos de codigo fonte para validacao.

## 🛠️ Funcionalidades Atuais (Análise Léxica)

O analisador léxico suporta:

-   **Palavras Reservadas**: `int`, `float`, `char`, `return`, `if`, `else`, `while`, `for`.
-   **Operadores**:
    -   Simples: `+`, `-`, `*`, `/`, `=`, `<`, `>`, `!`.
    -   Compostos: `==`, `!=`, `<=`, `>=`, `++`, `--`.
-   **Separadores**: `(`, `)`, `{`, `}`, `[`, `]`, `;`, `,`.
-   **Literais**: Suporte para strings (`"..."`) e caracteres (`'...'`).
-   **Comentários**: 
    -   Linha única: `//`
    -   Bloco: `/* ... */`
-   **Identificação de Erros**: Detecta erros léxicos como números seguidos de letras, literais não fechados ou comentários de bloco não terminados.

## 🏃 Como Executar

Para testar o analisador léxico com um arquivo de código:

```bash
python3 a-lex.py codigo1.c
```

O script imprime no terminal a lista de tokens da seguinte forma:
`TIPO_TOKEN   VALOR   LINHA   COLUNA`

## Analise sintatica

O arquivo `a-sinatico.py` usa diretamente a lista de tokens produzida por
`a-lex.py`. O parser e descendente recursivo: cada construcao da linguagem
possui uma funcao de analise e `consome_token` controla o avanco nos tokens.

A gramatica atualmente cobre:

- funcoes e declaracoes de variaveis dos tipos `int`, `float` e `char`;
- blocos, `if`/`else`, `while`, `for` e `return`;
- expressoes aritmeticas, relacionais, atribuicao, chamadas, vetores,
  negacao `!` e operadores `++`/`--`.

Quando encontra um erro, o parser informa linha e coluna e descarta tokens
ate um ponto seguro (`;` ou `}`) para continuar verificando o restante do
programa. A analise e apenas sintatica; nomes e tipos nao sao validados.

Para executar a analise sintatica:

```bash
python3 a-sinatico.py codigo1.c
```

Um programa valido produz `SUCESSO`. Caso exista erro lexico ou sintatico,
a primeira linha da saida e `ERRO`. Cada diagnostico seguinte e identificado
como `ERRO LEXICO` ou `ERRO SINTATICO`.

## 👥 Autor
- Desenvolvido durante a disciplina de Compiladores na UFSJ.
