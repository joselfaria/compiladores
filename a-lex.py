## analisador lexico
import sys
import re

OPERADORES_DUPLOS = {'==', '!=', '<=', '>=', '++', '--'}
OPERADORES_SIMPLES  = ['+', '-', '*', '/', '=', '<', '>', '!']
SEPARADORES         = ['(', ')', '{', '}', '[', ']', ';', ',']
PALAVRAS_RESERVADAS = {'int', 'float', 'char', 'return', 'if', 'else', 'while', 'for'}




def ler_comentario_linha(codigo, scout, linha, coluna):
    ## pula tudo ate o fim da linha  .
    while scout < len(codigo) and codigo[scout] != '\n':
        scout += 1
        coluna += 1
    return scout, linha, coluna


def ler_comentario_bloco(codigo, scout, linha, coluna, tokens):
    ## pula /* ... */. erro se nao fechar.
    scout += 2
    coluna += 2
    fechou = False

    scoutbackup = scout
    linhabackup = linha
    colunabackup = coluna

    while scout < len(codigo) - 1:
        if codigo[scout] == '\n':
            linha += 1
            coluna = 1
            scout += 1
        elif codigo[scout] == '*' and codigo[scout + 1] == '/':
            scout += 2
            coluna += 2
            fechou = True
            break
        else:
            scout += 1
            coluna += 1

    if not fechou:
        tokens.append(('ERRO', 'Cade /*', linhabackup, colunabackup))
        scout = scoutbackup +1
        linha = linhabackup
        coluna = colunabackup


    return scout, linha, coluna


def ler_literal(codigo, scout, linha, coluna, tokens):
    ## le string delimitada por ' ou ". erro se nao fechar."



    ''' ta ruim tem que melhorar por que tipo eu posso abrir um literal simples com varios chars e ele ta cagando pra quebra de linha e pa'''

    
    col_inicio = coluna
    delimitador = codigo[scout]
    scout += 1
    coluna += 1
    start = scout

    
    while scout < len(codigo) and codigo[scout] != delimitador:
        if codigo[scout] == '\n':
            tokens.append(('ERRO', codigo[start - 1:scout], linha, col_inicio))
            return scout, linha, coluna
        scout += 1
        coluna += 1

    if scout >= len(codigo):
        tokens.append(('ERRO', codigo[start - 1:scout], linha, col_inicio))
        return scout, linha, coluna

    tokens.append(('LITERAL', codigo[start:scout], linha, col_inicio))
    scout += 1
    coluna += 1
    return scout, linha, coluna


def ler_numero(codigo, scout, linha, coluna, tokens, com_sinal=False):
    ## le inteiro ou decimal. erro se seguido de letra (ex: 123abc).
    start = scout
    col_inicio = coluna

    # consome o sinal negativo se vier
    if com_sinal and codigo[scout] == '-':
        scout += 1
        coluna += 1

    while scout < len(codigo) and codigo[scout].isdigit():
        scout += 1
        coluna += 1

    # parte decimal opcional
    if scout < len(codigo) and codigo[scout] == '.' \
            and scout + 1 < len(codigo) and codigo[scout + 1].isdigit():
        scout += 1
        coluna += 1
        while scout < len(codigo) and codigo[scout].isdigit():
            scout += 1
            coluna += 1

    # numero colado em letra: 123abc ou -123abc
    if scout < len(codigo) and re.match(r'[A-Za-z_]', codigo[scout]):
        while scout < len(codigo) and re.match(r'[A-Za-z0-9_]', codigo[scout]):
            scout += 1
            coluna += 1
        tokens.append(('ERRO', codigo[start:scout], linha, col_inicio))
        return scout, linha, coluna

    tokens.append(('NUMERO', codigo[start:scout], linha, col_inicio))
    return scout, linha, coluna

def ler_identificador(codigo, scout, linha, coluna, tokens):
    ## le identificador ou palavra reservada.
    start = scout
    col_inicio = coluna

    while scout < len(codigo) and re.match(r'[A-Za-z0-9_]', codigo[scout]):
        scout += 1
        coluna += 1

    token = codigo[start:scout]
    tipo = 'PALAVRA_RESERVADA' if token in PALAVRAS_RESERVADAS else 'IDENTIFICADOR'
    tokens.append((tipo, token, linha, col_inicio))
    return scout, linha, coluna


def ler_operador(codigo, scout, linha, coluna, tokens, esperando_valor):
    ## le operador simples ou duplo. trata // e /* como comentarios.*/
    char = codigo[scout]
    col_inicio = coluna

    if scout + 1 < len(codigo) and (char + codigo[scout + 1]) in OPERADORES_DUPLOS:
        tokens.append(('OPERADOR', char + codigo[scout + 1], linha, col_inicio))
        return scout + 2, linha, coluna + 2

    if char == '/' and scout + 1 < len(codigo) and codigo[scout + 1] == '/':
        return ler_comentario_linha(codigo, scout, linha, coluna)

    if char == '/' and scout + 1 < len(codigo) and codigo[scout + 1] == '*':
        return ler_comentario_bloco(codigo, scout, linha, coluna, tokens)

    if char == '-' and esperando_valor:
        if scout + 1 < len(codigo) and codigo[scout + 1].isdigit():
            return ler_numero(codigo, scout, linha, coluna, tokens, com_sinal=True)

    if char == '!':
        tokens.append(('ERRO', char, linha, col_inicio))
        return scout + 1, linha, coluna + 1

    tokens.append(('OPERADOR', char, linha, col_inicio))
    return scout + 1, linha, coluna + 1


def analisar_codigo(codigo):
    tokens = []
    linha  = 1
    coluna = 1
    scout  = 0
    esperando_valor = True

    while scout < len(codigo):
        char = codigo[scout]

        if char.isspace():
            if char == '\n':
                linha += 1
                coluna = 1
            else:
                coluna += 1
            scout += 1
            continue

        if re.match(r'[A-Za-z_]', char):
            scout, linha, coluna = ler_identificador(codigo, scout, linha, coluna, tokens)
            esperando_valor = False

        elif char.isdigit():
            scout, linha, coluna = ler_numero(codigo, scout, linha, coluna, tokens)
            esperando_valor = False

        elif char in OPERADORES_SIMPLES:
            scout, linha, coluna = ler_operador(codigo, scout, linha, coluna, tokens, esperando_valor)
            esperando_valor = True

        elif char in SEPARADORES:
            tokens.append(('SEPARADOR', char, linha, coluna))
            scout  += 1
            coluna += 1
            esperando_valor = char not in (')', ']')

        elif char in ('"', "'"):
            scout, linha, coluna = ler_literal(codigo, scout, linha, coluna, tokens)
            esperando_valor = False

        else:
            tokens.append(('ERRO', char, linha, coluna))
            scout  += 1
            coluna += 1

    return tokens


def main():
    try:
        nome_arquivo = sys.argv[1]
    except IndexError:
        print("Passe o nome do arquivo como arg.")
        sys.exit(1)

    with open(nome_arquivo, 'r') as f:
        codigo = f.read()

    tokens = analisar_codigo(codigo)
    for i in tokens:
        if i[0] == 'ERRO':
             print(f"ERRO '{i[1]}' na linha {i[2]}, coluna {i[3]}")
    for i in tokens:
        if i[0] != 'ERRO':
            print("{}   {}  {}  {}".format(i[0], i[1], i[2], i[3]))



if __name__ == '__main__':
    main()