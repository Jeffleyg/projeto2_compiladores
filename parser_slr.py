from config import REGRAS, TABELA_SLR
from suporte_compilador import CompiladorSuporte

def executar_parser(fita_tokens):
    suporte = CompiladorSuporte()
    pilha_estados = [0]
    pilha_valores = []
    
    # Adiciona o token delimitador de fim de fita
    tokens = fita_tokens + [('$', '$')]
    ponteiro = 0
    
    print("--- ETAPA 1: ANÁLISE SINTÁTICA (SLR) ---")
    
    while True:
        estado_atual = pilha_estados[-1]
        token_tipo, token_val = tokens[ponteiro]
        
        # Faz o cruzamento na matriz de parsing
        acao = TABELA_SLR.get(estado_atual, {}).get(token_tipo) or TABELA_SLR.get(estado_atual, {}).get(token_val)
        
        if not acao:
            print(f"[-] ERRO SINTÁTICO: Erro próximo ao token '{token_val}' no estado {estado_atual}") # [cite: 17]
            return False
            
        if acao.startswith('S'):  # Ação: SHIFT (Empilhar)
            proximo_estado = int(acao[1:])
            pilha_estados.append(proximo_estado)
            pilha_valores.append({'valor': token_val, 'lugar': token_val})
            ponteiro += 1
            
        elif acao.startswith('R'):  # Ação: REDUCE (Reduzir por Regra)
            regra_num = int(acao[1:])
            esquerda, direita = REGRAS[regra_num]
            
            nos_reduzidos = []
            for _ in range(len(direita)):
                pilha_estados.pop()
                nos_reduzidos.insert(0, pilha_valores.pop())
                
            # Interceptação e execução das ações semânticas associadas à produção [cite: 21, 25]
            atributo_retorno = suporte.acao_semantica(regra_num, nos_reduzidos)
            
            # Executa a transição GOTO subsequente
            estado_topo = pilha_estados[-1]
            proximo_estado = TABELA_SLR[estado_topo][esquerda]
            pilha_estados.append(proximo_estado)
            pilha_valores.append(atributo_retorno)
            print(f"[Sintático] Reduziu pela Regra: {esquerda} -> {' '.join(direita)}")
            
        elif acao == 'ACC':  # Cadeia Aceita
            print("[+] ACEITO: Cadeia reconhecida com sucesso sintático e semântico!") # [cite: 17, 23]
            
            # Exibição do resultado da Etapa 3 [cite: 26]
            print("\n--- ETAPA 3: CÓDIGO INTERMEDIÁRIO GERADO ---")
            for linha in suporte.codigo_intermediario:
                print(linha)
                
            # Exibição do resultado da Etapa 4 [cite: 30]
            codigo_otimizado = suporte.otimizar_codigo()
            for linha in codigo_otimizado:
                print(linha)
            return True