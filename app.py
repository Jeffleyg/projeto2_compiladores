import sys
from parser_slr import executar_parser

# Caso 1: Sucesso Total (O caso padrão do teu relatório)
# Código original: { int x ; x = 10 + 5 ; }
fita_sucesso = [
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

# Caso 2: Erro Sintático (Falta o ponto e vírgula ';' após a declaração)
# Código: { int x x = 10 + 5 ; }
fita_erro_sintatico = [
    ('{', '{'),
    ('tipo', 'int'),
    ('id', 'x'),
    # ';' removido de propósito para falhar no parser_slr
    ('id', 'x'),
    ('=', '='),
    ('num', '10'),
    ('+', '+'),
    ('num', '5'),
    (';', ';'),
    ('}', '}')
]

# Caso 3: Erro Semântico - Dupla Declaração
# Código: { int x ; int x ; }
fita_dupla_declaracao = [
    ('{', '{'),
    ('tipo', 'int'),
    ('id', 'x'),
    (';', ';'),
    ('tipo', 'int'),
    ('id', 'x'),
    (';', ';'),
    ('}', '}')
]

# Caso 4: Erro Semântico - Variável Não Declarada na Atribuição
# Código: { y = 10 ; }
fita_nao_declarada_atrib = [
    ('{', '{'),
    ('id', 'y'),
    ('=', '='),
    ('num', '10'),
    (';', ';'),
    ('}', '}')
]

# Caso 5: Erro Semântico - Variável Não Declarada na Expressão
# Código: { int x ; x = 10 + y ; }
fita_nao_declarada_exp = [
    ('{', '{'),
    ('tipo', 'int'),
    ('id', 'x'),
    (';', ';'),
    ('id', 'x'),
    ('=', '='),
    ('num', '10'),
    ('+', '+'),
    ('id', 'y'), # 'y' não foi declarada na tabela de símbolos
    (';', ';'),
    ('}', '}')
]

if __name__ == "__main__":
    while True:
        print("\n" + "="*50)
        print("     MENU DE TESTES - PROJETO COMPILADORES")
        print("="*50)
        print("1. [SUCESSO] Cadeia Válida (TAC + Otimização)")
        print("2. [ERRO] Erro Sintático (Falta de ';')")
        print("3. [ERRO] Erro Semântico (Dupla Declaração)")
        print("4. [ERRO] Erro Semântico (Variável Não Declarada na Atribuição)")
        print("5. [ERRO] Erro Semântico (Variável Não Declarada na Expressão)")
        print("0. Sair")
        print("="*50)
        
        opcao = input("Escolha o caso de teste que deseja executar: ").strip()
        
        print("\n" + "-"*50)
        if opcao == "1":
            print("[EXECUTANDO] Caso 1: Cadeia Válida Completa")
            executar_parser(fita_sucesso)
        elif opcao == "2":
            print("[EXECUTANDO] Caso 2: Erro Sintático por falta de ';'")
            executar_parser(fita_erro_sintatico)
        elif opcao == "3":
            print("[EXECUTANDO] Caso 3: Erro Semântico de Dupla Declaração")
            try:
                executar_parser(fita_dupla_declaracao)
            except SystemExit:
                print("\n[Info] O compilador encerrou a execução simulada devido ao erro semântico caught.")
        elif opcao == "4":
            print("[EXECUTANDO] Caso 4: Erro Semântico de Variável Não Declarada (Atribuição)")
            try:
                executar_parser(fita_nao_declarada_atrib)
            except SystemExit:
                print("\n[Info] O compilador encerrou a execução simulada devido ao erro semântico caught.")
        elif opcao == "5":
            print("[EXECUTANDO] Caso 5: Erro Semântico de Variável Não Declarada (Expressão)")
            try:
                executar_parser(fita_nao_declarada_exp)
            except SystemExit:
                print("\n[Info] O compilador encerrou a execução simulada devido ao erro semântico caught.")
        elif opcao == "0":
            print("A sair do programa de testes. Boa sorte na arguição!")
            break
        else:
            print("Opção inválida! Escolha um número de 0 a 5.")
        print("-"*50)