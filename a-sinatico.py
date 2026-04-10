import sys

alex = __import__("a-lex")

def main():
    try:
        nome_arquivo = sys.argv[1]
    except IndexError:
        print("Passe o nome do arquivo como arg.")
        sys.exit(1)
    with open(nome_arquivo, 'r') as f:
        codigo = f.read()
    tokens = alex.analisar_codigo(codigo)

    for token in tokens:
        print(token)

if __name__ == "__main__":
    main()
