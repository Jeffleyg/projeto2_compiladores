from parser_slr import executar_parser

if __name__ == "__main__":
    # Simulação da fita de saída gerada pelo Reconhecedor Léxico
    # Equivalente ao programa fonte: { int x ; x = 10 + 5 ; }
    fita_exemplo = [
        ('{', '{'),
        ('tipo', 'int'),
        ('id', 'x'),
        (';', ';'),
        ('id', 'x'),
        ('=', '='),
        ('num', '10'),
        ('+', '+'),
        ('num', '5'),
        (';', ';'),
        ('}', '}')
    ]
    
    executar_parser(fita_exemplo)