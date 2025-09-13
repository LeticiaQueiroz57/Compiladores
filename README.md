# Compilador de Rust
Este projeto contém um compilador básico escrito em Python, focado nas etapas de análise léxica e sintática. Ele foi desenvolvido para processar arquivos de código-fonte inspirados na linguagem de programação Rust. 

## Projeto
O compilador está dividido em duas fases principais:

1. Análise Léxica (Scanning): O código-fonte é lido e tokenizado. O código "let x = 10;", por exemplo, é transformado em uma sequência de tokens, como LET, IDENTIFICADOR (x), OP_ATRIBUICAO (=), NUMERO (10) e PONTO_E_VIRGULA (;). Essa etapa é como traduzir uma frase em palavras individuais.

2. Análise Sintática (Parsing): Após o scanning, o analisador sintático usa a sequência de tokens para verificar se a estrutura do código segue as regras gramaticais da linguagem. Ele constrói uma representação interna do código, como uma "árvore sintática", garantindo que a ordem das palavras e símbolos faz sentido. Por exemplo, ele verifica se cada if tem sua respectiva condição e bloco de código, ou se uma função é declarada corretamente com parênteses e chaves. Se a sintaxe estiver incorreta, ele aponta um erro.
