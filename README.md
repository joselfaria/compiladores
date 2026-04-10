# Compilador C Simplificado (UFSJ)

Este repositório contém o desenvolvimento de um compilador para uma linguagem baseada em C simplificado, realizado como parte da disciplina de Compiladores ministrada pelo Professor **Flavio Schiavoni** na **UFSJ**.

## 🚀 Objetivo do Projeto

O objetivo é construir progressivamente um compilador durante ao longo da disciplina.

## 📂 Estrutura do Projeto

-   `a-lex.py`: Analisador Léxico (Scanner). Identifica tokens como palavras reservadas, identificadores, números, operadores e literais.
-   `codigo.c`: Arquivo de teste contendo exemplos de código fonte para validação.

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
python3 a-lex.py codigo.c
```

O script imprime no terminal a lista de tokens da seguinte forma:
`TIPO_TOKEN   VALOR   LINHA   COLUNA`

## 👥 Autor
- Desenvolvido durante a disciplina de Compiladores na UFSJ.
