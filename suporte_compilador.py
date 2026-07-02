import sys

class CompiladorSuporte:
    def __init__(self):
        self.tabela_simbolos = {} 
        self.codigo_intermediario = []
        self.temp_count = 0

    def novo_temporario(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def acao_semantica(self, regra_num, nos_reduzidos):
        if regra_num == 8:  # Comando -> tipo id ;
            tipo = nos_reduzidos[0]['valor']
            id_nome = nos_reduzidos[1]['valor']
            if id_nome in self.tabela_simbolos:
                print(f"[-] ERRO SEMÂNTICO: Variável '{id_nome}' já declarada.")
                sys.exit(1)
            self.tabela_simbolos[id_nome] = {'tipo': tipo}
            print(f"[Semântico] Declarado com sucesso: {id_nome} ({tipo})")

        elif regra_num == 7:  # Comando -> id = Exp ;
            id_nome = nos_reduzidos[0]['valor']
            if id_nome not in self.tabela_simbolos:
                print(f"[-] ERRO SEMÂNTICO: Variável '{id_nome}' não foi declarada.")
                sys.exit(1)
            exp_lugar = nos_reduzidos[2]['lugar']
            self.codigo_intermediario.append(f"{id_nome} = {exp_lugar}")

        elif regra_num in [10, 11, 13, 14]:  # Operações Matemáticas (+, -, *, /)
            op1 = nos_reduzidos[0]['lugar']
            operador = nos_reduzidos[1]['valor']
            op2 = nos_reduzidos[2]['lugar']
            temp = self.novo_temporario()
            self.codigo_intermediario.append(f"{temp} = {op1} {operador} {op2}")
            return {'lugar': temp}

        elif regra_num in [17, 18]:  # F -> id ou F -> num
            val = nos_reduzidos[0]['valor']
            if regra_num == 17 and val not in self.tabela_simbolos:
                print(f"[-] ERRO SEMÂNTICO: Variável '{val}' não declarada na expressão.")
                sys.exit(1)
            return {'lugar': val}
            
        elif regra_num == 9:  # Exp -> E
            return {'lugar': nos_reduzidos[0]['lugar']}
        elif regra_num == 12: # E -> T
            return {'lugar': nos_reduzidos[0]['lugar']}
        elif regra_num == 15: # T -> F
            return {'lugar': nos_reduzidos[0]['lugar']}
            
        return {'lugar': None}

    def otimizar_codigo(self):
        otimizado = []
        valores_conhecidos = {}

        for linha in self.codigo_intermediario:
            if "=" in linha and not any(op in linha for op in ["+", "-", "*", "/"]):
                esq, dir_ = [x.strip() for x in linha.split("=")]
                if dir_.isdigit():
                    valores_conhecidos[esq] = dir_
                elif dir_ in valores_conhecidos:
                    dir_ = valores_conhecidos[dir_]
                    valores_conhecidos[esq] = dir_
                otimizado.append(f"{esq} = {dir_}")
            elif any(op in linha for op in ["+", "-", "*", "/"]):
                esq, dir_ = [x.strip() for x in linha.split("=")]
                tokens_dir = dir_.split()
                op1, op, op2 = tokens_dir[0], tokens_dir[1], tokens_dir[2]
                
                if op1 in valores_conhecidos: op1 = valores_conhecidos[op1]
                if op2 in valores_conhecidos: op2 = valores_conhecidos[op2]
                
                if op1.isdigit() and op2.isdigit():
                    resultado = eval(f"{op1} {op} {op2}")
                    valores_conhecidos[esq] = str(int(resultado))
                    otimizado.append(f"{esq} = {int(resultado)}")
                else:
                    otimizado.append(f"{esq} = {op1} {op} {op2}")
            else:
                otimizado.append(linha)
                
        return otimizado