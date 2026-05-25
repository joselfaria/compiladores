int soma(int a, int b)
{
    return a + b;
}

int main()
{
    int total = soma(4, 6);

    if (total >= 10) {
        total++;
    } else {
        total = 0;
    }

    return total;
}
