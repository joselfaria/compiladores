## analisador sintatico
import sys

alex = __import__("a-lex")


TIPOS = {"int", "float", "char"}
OPERADORES_RELACIONAIS = {"<", ">", "<=", ">="}
OPERADORES_IGUALDADE = {"==", "!="}


class ErroSintatico(Exception):
    pass


class AnalisadorSintatico:

    def __init__(self, tokens):
        self.erros = []
        self.posicao = 0

        tokens_validos = []
        for token in tokens:
            if token[0] == "ERRO":
                self.guardar_erro(
                    token,
                    "token invalido recebido do analisador lexico: {!r}".format(
                        token[1]
                    ),
                    categoria="LEXICO",
                )
            else:
                tokens_validos.append(token)

        ultimo = tokens[-1] if tokens else ("EOF", "", 1, 1)
        coluna_final = ultimo[3] + len(str(ultimo[1]))
        self.tokens = tokens_validos + [("EOF", "EOF", ultimo[2], coluna_final)]

    def token_atual(self):
        return self.tokens[self.posicao]

    def verifica(self, esperado=None, tipo=None):
        encontrado = self.token_atual()
        if esperado is not None and encontrado[1] != esperado:
            return False
        if tipo is not None and encontrado[0] != tipo:
            return False
        return True

    def guardar_erro(self, token, mensagem, categoria="SINTATICO"):
        self.erros.append(
            "ERRO {} - linha {}, coluna {}: {}".format(
                categoria, token[2], token[3], mensagem
            )
        )

    def encontrado(self, token):
        if token[0] == "EOF":
            return "fim do arquivo"
        return "{!r}".format(token[1])

    def erro_sintatico(self, esperado):
        token = self.token_atual()
        self.guardar_erro(
            token,
            "esperado {}, encontrado {}".format(esperado, self.encontrado(token)),
        )
        raise ErroSintatico()

    def consome_token(self, esperado=None, tipo=None, mensagem=None):
        ## consome o token. da erro se for diferente do esperado.
        encontrado = self.token_atual()
        if esperado is not None or tipo is not None:
            if not self.verifica(esperado=esperado, tipo=tipo):
                self.erro_sintatico(mensagem or repr(esperado or tipo))

        if encontrado[0] != "EOF":
            self.posicao += 1
        return encontrado

    def aceita(self, esperado=None, tipo=None):
        if self.verifica(esperado=esperado, tipo=tipo):
            return self.consome_token(esperado=esperado, tipo=tipo)
        return None

    def pular_comando_errado(self, paradas=None):
        ## pula o comando com erro ate ; ou }.
        paradas = paradas or {";", "}"}
        while not self.verifica(tipo="EOF") and self.token_atual()[1] not in paradas:
            self.consome_token()
        if self.verifica(esperado=";"):
            self.consome_token(esperado=";")

    def analisar(self):
        ## analisa tudo ate acabar o arquivo.
        while not self.verifica(tipo="EOF"):
            try:
                self.declaracao_global()
            except ErroSintatico:
                self.pular_comando_errado()
                if self.verifica(esperado="}"):
                    self.consome_token(esperado="}")
        return self.erros

    def declaracao_global(self):
        ## variavel global ou funcao.
        self.tipo()
        self.consome_token(tipo="IDENTIFICADOR", mensagem="identificador")

        if self.aceita(esperado="("):
            self.parametros()
            self.consome_token(esperado=")", mensagem="')'")
            self.bloco()
            return

        self.resto_declaracao()
        while self.aceita(esperado=","):
            self.consome_token(tipo="IDENTIFICADOR", mensagem="identificador")
            self.resto_declaracao()
        self.consome_token(esperado=";", mensagem="';'")

    def tipo(self):
        ## int, float ou char.
        if self.token_atual()[1] not in TIPOS:
            self.erro_sintatico("tipo ('int', 'float' ou 'char')")
        self.consome_token()

    def parametros(self):
        ## parametros separados por virgula.
        if self.verifica(esperado=")"):
            return
        self.parametro()
        while self.aceita(esperado=","):
            self.parametro()

    def parametro(self):
        self.tipo()
        self.consome_token(tipo="IDENTIFICADOR", mensagem="identificador")
        self.vetor()

    def declaracao(self):
        ## declaracao de variavel.
        self.tipo()
        self.consome_token(tipo="IDENTIFICADOR", mensagem="identificador")
        self.resto_declaracao()
        while self.aceita(esperado=","):
            self.consome_token(tipo="IDENTIFICADOR", mensagem="identificador")
            self.resto_declaracao()
        self.consome_token(esperado=";", mensagem="';'")

    def resto_declaracao(self):
        self.vetor()
        if self.aceita(esperado="="):
            self.expressao()

    def vetor(self):
        ## parte entre colchetes de um vetor.
        while self.aceita(esperado="["):
            if not self.verifica(esperado="]"):
                self.expressao()
            self.consome_token(esperado="]", mensagem="']'")

    def bloco(self):
        ## comandos entre { e }.
        self.consome_token(esperado="{", mensagem="'{'")
        while not self.verifica(esperado="}") and not self.verifica(tipo="EOF"):
            inicio = self.posicao
            try:
                self.comando()
            except ErroSintatico:
                self.pular_comando_errado()
            if self.posicao == inicio:
                self.consome_token()
        self.consome_token(esperado="}", mensagem="'}'")

    def comando(self):
        ## escolhe o proximo comando.
        encontrado = self.token_atual()[1]
        if encontrado in TIPOS:
            self.declaracao()
        elif encontrado == "{":
            self.bloco()
        elif encontrado == "if":
            self.comando_if()
        elif encontrado == "while":
            self.comando_while()
        elif encontrado == "for":
            self.comando_for()
        elif encontrado == "return":
            self.comando_return()
        elif encontrado == ";":
            self.consome_token(esperado=";")
        else:
            self.expressao()
            self.consome_token(esperado=";", mensagem="';'")

    def comando_if(self):
        ## if e else se tiver.
        self.consome_token(esperado="if")
        self.condicao()
        self.comando()
        if self.aceita(esperado="else"):
            self.comando()

    def comando_while(self):
        self.consome_token(esperado="while")
        self.condicao()
        self.comando()

    def condicao(self):
        ## expressao entre parenteses.
        self.consome_token(esperado="(", mensagem="'('")
        self.expressao()
        self.consome_token(esperado=")", mensagem="')'")

    def comando_for(self):
        ## inicio, condicao e incremento do for.
        self.consome_token(esperado="for")
        self.consome_token(esperado="(", mensagem="'('")

        if self.token_atual()[1] in TIPOS:
            self.declaracao()
        else:
            if not self.verifica(esperado=";"):
                self.expressao()
            self.consome_token(esperado=";", mensagem="';'")

        if not self.verifica(esperado=";"):
            self.expressao()
        self.consome_token(esperado=";", mensagem="';'")

        if not self.verifica(esperado=")"):
            self.expressao()
        self.consome_token(esperado=")", mensagem="')'")
        self.comando()

    def comando_return(self):
        self.consome_token(esperado="return")
        if not self.verifica(esperado=";"):
            self.expressao()
        self.consome_token(esperado=";", mensagem="';'")

    def expressao(self):
        ## comeca pela atribuicao.
        self.atribuicao()

    def atribuicao(self):
        self.igualdade()
        if self.aceita(esperado="="):
            self.atribuicao()

    def igualdade(self):
        self.relacional()
        while self.token_atual()[1] in OPERADORES_IGUALDADE:
            self.consome_token()
            self.relacional()

    def relacional(self):
        self.soma()
        while self.token_atual()[1] in OPERADORES_RELACIONAIS:
            self.consome_token()
            self.soma()

    def soma(self):
        self.multiplicacao()
        while self.token_atual()[1] in {"+", "-"}:
            self.consome_token()
            self.multiplicacao()

    def multiplicacao(self):
        self.unario()
        while self.token_atual()[1] in {"*", "/"}:
            self.consome_token()
            self.unario()

    def unario(self):
        if self.token_atual()[1] in {"+", "-", "!", "++", "--"}:
            self.consome_token()
            self.unario()
            return
        self.posfixo()

    def posfixo(self):
        self.valor()
        while True:
            if self.aceita(esperado="("):
                if not self.verifica(esperado=")"):
                    self.expressao()
                    while self.aceita(esperado=","):
                        self.expressao()
                self.consome_token(esperado=")", mensagem="')'")
            elif self.aceita(esperado="["):
                self.expressao()
                self.consome_token(esperado="]", mensagem="']'")
            elif self.token_atual()[1] in {"++", "--"}:
                self.consome_token()
            else:
                return

    def valor(self):
        ## identificador, numero, literal ou expressao em parenteses.
        if self.token_atual()[0] in {"IDENTIFICADOR", "NUMERO", "LITERAL"}:
            self.consome_token()
        elif self.aceita(esperado="("):
            self.expressao()
            self.consome_token(esperado=")", mensagem="')'")
        else:
            self.erro_sintatico("identificador, numero, literal ou '('")


def analisar_tokens(tokens):
    return AnalisadorSintatico(tokens).analisar()


def main():
    try:
        nome_arquivo = sys.argv[1]
    except IndexError:
        print("Passe o nome do arquivo como arg.")
        sys.exit(1)

    with open(nome_arquivo, "r") as arquivo:
        codigo = arquivo.read()

    erros = analisar_tokens(alex.analisar_codigo(codigo))
    if erros:
        print("ERRO")
        for erro in erros:
            print(erro)
        sys.exit(1)

    print("SUCESSO")


if __name__ == "__main__":
    main()
