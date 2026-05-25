int main()
{
    int valores[3];
    int i = 0;
    int soma = 0;

    while (i < 3) {
        valores[i] = i + 1;
        soma = soma + valores[i];
        i++;
    }

    for (i = 0; i < 3; i++) {
        soma = soma + 1;
    }

    return soma;
}
