"""
Leticia Oliveira de Queiroz
Igor Cavalcante de Albuquerque Moratas
Pedro Oliveira Saraiva Girão
Eduardo Francisco Lopes Nunes
João Marcelo Silva Basílio
"""

atomo_EOS = 0
IDENTIFICADOR = 1
FN = 2
MAIN = 3
LET = 4
MUT = 5
IF = 6
ELSE = 7
WHILE = 8
RETURN = 9
PRINTLN = 10
TRUE = 11
FALSE = 12
I32 = 13
BOOL = 14
STRING_TYPE = 15
F32 = 16
F64 = 17
OP_ATRIBUICAO = 18
OP_SOMA = 19
OP_SUBTRACAO = 20
OP_MULTIPLICACAO = 21
OP_DIVISAO = 22
OP_MODULO = 23
OP_IGUAL = 24
OP_DIFERENTE = 25
OP_MENOR = 26
OP_MENOR_IGUAL = 27
OP_MAIOR = 28
OP_MAIOR_IGUAL = 29
OP_E = 30
OP_OU = 31
OP_NAO = 32
OP_REFERENCIA = 33
OP_SETA = 34
ABRE_PAR = 35
FECHA_PAR = 36
ABRE_CHAVES = 37
FECHA_CHAVES = 38
PONTO_E_VIRGULA = 39
VIRGULA = 40
DOIS_PONTOS = 41
NUMERO = 42
STRING = 43
CARACTER = 44
AT_ERRO = 45

# Variáveis globais
i = 0
codigo = ''
lookahead = 0
valor_atual = ''

# Analisador Léxico
def proximo_caractere():
    global i
    if i >= len(codigo):
        return '\0'
    c = codigo[i]
    i += 1
    return c

def caractere_atual():
    global i
    if i >= len(codigo):
        return '\0'
    return codigo[i]

def pular_espacos():
    global i
    while i < len(codigo) and codigo[i] in ' \t\n\r':
        i += 1

def ler_identificador():
    global i, valor_atual
    valor_atual = ''
    while (i < len(codigo) and
           (codigo[i].isalnum() or codigo[i] in '_!')):
        valor_atual += codigo[i]
        i += 1
    return valor_atual

def ler_numero():
    global i, valor_atual
    valor_atual = ''
    while i < len(codigo) and (codigo[i].isdigit() or codigo[i] == '.'):
        valor_atual += codigo[i]
        i += 1
    return valor_atual

def ler_string():
    global i, valor_atual
    valor_atual = ''
    i += 1
    while i < len(codigo) and codigo[i] != '"':
        if codigo[i] == '\\' and i + 1 < len(codigo):
            i += 1
            if codigo[i] == 'n': valor_atual += '\n'
            elif codigo[i] == 't': valor_atual += '\t'
            elif codigo[i] == '\\': valor_atual += '\\'
            elif codigo[i] == '"': valor_atual += '"'
            else: valor_atual += codigo[i]
        else:
            valor_atual += codigo[i]
        i += 1
    if i < len(codigo):
        i += 1
    return valor_atual

def pular_comentarios():
    global i
    if i < len(codigo) - 1:
        if codigo[i:i+2] == '//':
            while i < len(codigo) and codigo[i] != '\n':
                i += 1
            return True
        elif codigo[i:i+2] == '/*':
            i += 2
            while i < len(codigo) - 1:
                if codigo[i:i+2] == '*/':
                    i += 2
                    break
                i += 1
            return True
    return False

# Analisador léxico
def proximo_atomo():
    global i, valor_atual
    while True:
        pular_espacos()
        if pular_comentarios():
            continue
        if i >= len(codigo):
            return atomo_EOS
        c = caractere_atual()
        if c == '\0': return atomo_EOS
        if i + 1 < len(codigo):
            dois_chars = codigo[i:i+2]
            if dois_chars == '==': i += 2; return OP_IGUAL
            elif dois_chars == '!=': i += 2; return OP_DIFERENTE
            elif dois_chars == '<=': i += 2; return OP_MENOR_IGUAL
            elif dois_chars == '>=': i += 2; return OP_MAIOR_IGUAL
            elif dois_chars == '&&': i += 2; return OP_E
            elif dois_chars == '||': i += 2; return OP_OU
            elif dois_chars == '->': i += 2; return OP_SETA
        if c == '+': i += 1; return OP_SOMA
        elif c == '-': i += 1; return OP_SUBTRACAO
        elif c == '*': i += 1; return OP_MULTIPLICACAO
        elif c == '/': i += 1; return OP_DIVISAO
        elif c == '%': i += 1; return OP_MODULO
        elif c == '=': i += 1; return OP_ATRIBUICAO
        elif c == '<': i += 1; return OP_MENOR
        elif c == '>': i += 1; return OP_MAIOR
        elif c == '!': i += 1; return OP_NAO
        elif c == '&': i += 1; return OP_REFERENCIA
        elif c == '(': i += 1; return ABRE_PAR
        elif c == ')': i += 1; return FECHA_PAR
        elif c == '{': i += 1; return ABRE_CHAVES
        elif c == '}': i += 1; return FECHA_CHAVES
        elif c == ';': i += 1; return PONTO_E_VIRGULA
        elif c == ',': i += 1; return VIRGULA
        elif c == ':': i += 1; return DOIS_PONTOS
        elif c == '"': ler_string(); return STRING
        elif c == "'":
            i += 1
            if i < len(codigo):
                valor_atual = codigo[i]
                i += 1
                if i < len(codigo) and codigo[i] == "'":
                    i += 1
                    return CARACTER
        elif c.isdigit(): ler_numero(); return NUMERO
        elif c.isalpha() or c == '_':
            valor = ler_identificador()
            if valor == 'fn': return FN
            elif valor == 'main': return MAIN
            elif valor == 'let': return LET
            elif valor == 'mut': return MUT
            elif valor == 'if': return IF
            elif valor == 'else': return ELSE
            elif valor == 'while': return WHILE
            elif valor == 'return': return RETURN
            elif valor == 'println!': return PRINTLN
            elif valor == 'true': return TRUE
            elif valor == 'false': return FALSE
            elif valor == 'i32': return I32
            elif valor == 'bool': return BOOL
            elif valor == 'String': return STRING_TYPE
            elif valor == 'f32': return F32
            elif valor == 'f64': return F64
            else: return IDENTIFICADOR
        else:
            i += 1
            return AT_ERRO

def nome_token(token):
    nomes = {
        0: 'FIM_CODIGO', 1: 'IDENTIFICADOR', 2: 'FN', 3: 'MAIN', 4: 'LET', 5: 'MUT',
        6: 'IF', 7: 'ELSE', 8: 'WHILE', 9: 'RETURN', 10: 'PRINTLN', 11: 'TRUE',
        12: 'FALSE', 13: 'I32', 14: 'BOOL', 15: 'STRING_TYPE', 16: 'F32', 17: 'F64',
        18: '=', 19: '+', 20: '-', 21: '*', 22: '/', 23: '%', 24: '==', 25: '!=',
        26: '<', 27: '<=', 28: '>', 29: '>=', 30: '&&', 31: '||', 32: '!', 33: '&',
        34: '->', 35: '(', 36: ')', 37: '{', 38: '}', 39: ';', 40: ',', 41: ':',
        42: 'NUMERO', 43: 'STRING', 44: 'CARACTER', 45: 'ERRO'
    }
    return nomes.get(token, f'TOKEN_{token}')

def consome(token_esperado):
    global lookahead
    if token_esperado != lookahead:
        print(f'Erro sintático: esperado {nome_token(token_esperado)}, encontrado {nome_token(lookahead)}')
        if valor_atual:
            print(f'Valor atual: "{valor_atual}"')
        exit(1)
    elif token_esperado != atomo_EOS:
        lookahead = proximo_atomo()


def programa():
    consome(FN)
    consome(MAIN)
    consome(ABRE_PAR)
    consome(FECHA_PAR)
    bloco()
    while lookahead == FN:
        funcao()
    consome(atomo_EOS)

def funcao():
    consome(FN)
    consome(IDENTIFICADOR)
    consome(ABRE_PAR)
    if lookahead == IDENTIFICADOR:
        parametros()
    consome(FECHA_PAR)
    if lookahead == OP_SETA:
        consome(OP_SETA)
        tipo()
    bloco()
def parametros():
    consome(IDENTIFICADOR)
    consome(DOIS_PONTOS)
    tipo()
    while lookahead == VIRGULA:
        consome(VIRGULA)
        consome(IDENTIFICADOR)
        consome(DOIS_PONTOS)
        tipo()

def tipo():
    if lookahead == I32:
        consome(I32)
    elif lookahead == BOOL:
        consome(BOOL)
    elif lookahead == STRING_TYPE:
        consome(STRING_TYPE)
    elif lookahead == F32:
      consome(F32)
    elif lookahead == F64:
      consome(F64)
    else:
      print(f"Erro sintatico: tipo esperado, encontrado {nome_token(lookahead)}")
      exit(1)
def bloco():
    global i, lookahead, valor_atual
    consome(ABRE_CHAVES)
    while lookahead in [LET, IDENTIFICADOR, IF, WHILE, PRINTLN, RETURN, ABRE_CHAVES]:
        if lookahead == IDENTIFICADOR:
            pos_backup = i
            lookahead_backup = lookahead
            valor_backup = valor_atual
            consome(IDENTIFICADOR)
            if lookahead == OP_ATRIBUICAO:
                i = pos_backup
                lookahead = lookahead_backup
                valor_atual = valor_backup
                comando()
            else:
                i = pos_backup
                lookahead = lookahead_backup
                valor_atual = valor_backup
                break
        else:
            comando()
    if lookahead not in [FECHA_CHAVES, atomo_EOS]:
        expressao()
    consome(FECHA_CHAVES)

def comando():
    if lookahead == LET: declaracao()
    elif lookahead == IF: comando_if()
    elif lookahead == WHILE: comando_while()
    elif lookahead == PRINTLN: comando_print()
    elif lookahead == RETURN: comando_return()
    elif lookahead == ABRE_CHAVES: bloco()
    elif lookahead == IDENTIFICADOR: atribuicao()
    else:
        print(f'Erro sintático: comando inválido, encontrado {nome_token(lookahead)}')
        exit(1)

def declaracao():
    consome(LET)
    if lookahead == MUT:
        consome(MUT)
    consome(IDENTIFICADOR)
    if lookahead == DOIS_PONTOS:
        consome(DOIS_PONTOS)
        tipo()
    consome(OP_ATRIBUICAO)
    expressao()
    consome(PONTO_E_VIRGULA)

def atribuicao():
    consome(IDENTIFICADOR)
    consome(OP_ATRIBUICAO)
    expressao()
    consome(PONTO_E_VIRGULA)

def comando_if():
    consome(IF)
    expressao()
    bloco()
    if lookahead == ELSE:
        consome(ELSE)
        bloco()

def comando_while():
    consome(WHILE)
    expressao()
    bloco()

def comando_print():
    consome(PRINTLN)
    consome(ABRE_PAR)
    expressao()
    consome(FECHA_PAR)
    consome(PONTO_E_VIRGULA)

def comando_return():
    consome(RETURN)
    if lookahead != PONTO_E_VIRGULA:
        expressao()
    consome(PONTO_E_VIRGULA)

def expressao():
    expressao_logica()

def expressao_logica():
    expressao_igualdade()
    while lookahead in [OP_E, OP_OU]:
        consome(lookahead)
        expressao_igualdade()

def expressao_igualdade():
    expressao_relacional()
    while lookahead in [OP_IGUAL, OP_DIFERENTE]:
        consome(lookahead)
        expressao_relacional()

def expressao_relacional():
  expressao_aditiva()
  while lookahead in [OP_MENOR, OP_MENOR_IGUAL, OP_MAIOR, OP_MAIOR_IGUAL]:
    consome(lookahead)
    expressao_aditiva()

def expressao_aditiva():
  expressao_multiplicativa()
  while lookahead in [OP_SOMA, OP_SUBTRACAO]:
    consome(lookahead)
    expressao_multiplicativa()

def expressao_multiplicativa():
    expressao_unaria()
    while lookahead in [OP_MULTIPLICACAO, OP_DIVISAO, OP_MODULO]:
        consome(lookahead)
        expressao_unaria()


def expressao_unaria():
    if lookahead == OP_SUBTRACAO:
        consome(OP_SUBTRACAO)
        expressao_unaria()
    elif lookahead == OP_NAO:
        consome(OP_NAO)
        expressao_unaria()
    elif lookahead == OP_REFERENCIA:
        consome(OP_REFERENCIA)
        if lookahead == MUT:
            consome(MUT)
        expressao_unaria()
    else:
        expressao_primaria()

def expressao_primaria():
    global i, lookahead, valor_atual
    if lookahead == IDENTIFICADOR:
        pos_backup = i
        lookahead_backup = lookahead
        valor_backup = valor_atual
        consome(IDENTIFICADOR)
        if lookahead == ABRE_PAR:
            i = pos_backup
            lookahead = lookahead_backup
            valor_atual = valor_backup
            chamada_funcao()
    elif lookahead == NUMERO: consome(NUMERO)
    elif lookahead == STRING: consome(STRING)
    elif lookahead == CARACTER: consome(CARACTER)
    elif lookahead == TRUE: consome(TRUE)
    elif lookahead == FALSE: consome(FALSE)
    elif lookahead == ABRE_PAR:
        consome(ABRE_PAR)
        expressao()
        consome(FECHA_PAR)
    else:
        print(f'Erro sintático: expressão inválida, encontrado {nome_token(lookahead)}')
        exit(1)

def chamada_funcao():
  consome(IDENTIFICADOR)
  consome(ABRE_PAR)
  if lookahead != FECHA_PAR:
    lista_de_argumentos()
  consome(FECHA_PAR)


def lista_de_argumentos():
  expressao()
  while lookahead == VIRGULA:
    consome(VIRGULA)
    expressao()



def sintatico():
    global lookahead, codigo, i, valor_atual
    print("Iniciando análise sintática...")
    lookahead = proximo_atomo()
    programa()
    print('Análise sintática concluída com sucesso!')

path = r'AP1 - Analisador\Codigo_teste.rs'
with open(path, 'r', encoding='utf-8') as f:
    codigo_exemplo = f.read()

def main():
    global codigo, i, lookahead, valor_atual

    i = 0
    lookahead = 0
    valor_atual = ''
    codigo = codigo_exemplo

    try:
        sintatico()
    except SystemExit:
        print("Análise interrompida devido a erro sintático.")

if __name__ == "__main__":
    main()
