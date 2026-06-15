# TDE-2 Detecção e recuperação de impasses
Este TDE explora três problemas centrais da programação concorrente — o Jantar dos Filósofos, condições de corrida controladas por semáforos e o tratamento de deadlock — exercitando, na prática, as quatro condições de Coffman e as estratégias clássicas de prevenção e correção.

Grupo: TDE 2
Integrantes: Gabriela Matos, Isabela Mendes, Isabela Zanon Ferrarini e Mariana Cintra.
Linguagem escolhida: Python

## Instruções de compilação e execução

Requisito: Ter instalado Python 3.10+ para complação.

1. Abre o terminal do Windows.
2. Navega até a pasta do projeto, por exemplo: cd Desktop\projeto-tde2
3. Para rodar cada arquivo, entra na pasta certa cd parte-Desejada e python nomeDoArquivo.py
   cd parte1-filosofos
   python versaoQueTrava.py
   python versaoCorrigida.py

   cd parte2-semafaro
   python versaoQueTrava.py
   python versaoCorrigida.py

   cd parte3-deadlock
   python versaoQueTrava.py
   python versaoCorrigida.py

## Relatório técnico de cada parte

## Parte 1 - Filosofos

## O que acontece na prática e o Problema
O problema mostra 5 filósofos sentados em uma mesa redonda, eles passam o tempo pensando ou comendo, para conseguir comer, cada filósofo precisa usar dois garfos ao mesmo tempo: o da sua esquerda e o da sua direita.
O erro (Versão que trava): Se todos os filósofos ficarem com fome juntos e cada um pegar o garfo da sua esquerda ao mesmo tempo, todos vão ficar segurando um garfo só, cada um vai ficar esperando o garfo da direita liberar, como ninguém solta o garfo que já está na mão, a mesa trava, o programa para ali e ninguém consegue comer.

## Por que o código trava? As regras de Coffman
Esse travamento acontece porque o código cumpre 4 regras que geram conflito:
Exclusão Mútua: Os garfos são exclusivos, se um filósofo pegou um garfo, nenhum outro pode mexer nele até que seja solto.
Segurar e Esperar: Cada filósofo segura o garfo da esquerda e fica esperando o da direita, sem soltar o que já tem.
Ninguém tira à força: Um filósofo não pode arrancar o garfo da mão do vizinho.
Espera em Círculo: O Filósofo 1 espera o Filósofo 2, que espera o 3, que espera o 4, que espera o 5, que espera o 1, todos ficam presos em um loop

## Como resolvemos o problema? (A nossa regra de ordem)
Para resolver isso, criamos uma regra de ordem: nós colocamos números de 0 a 4 nos garfos, em vez de pegar sempre o da esquerda primeiro, cada filósofo é obrigado a pegar primeiro o garfo com o número menor, e depois tentar pegar o garfo com o número maior,  faz com que o último filósofo tente pegar os garfos em uma ordem invertida do que os outros, se quatro filósofos pegarem seus garfos menores, o último garfo menor vai estar disputado, fazendo um filósofo esperar antes mesmo de segurar qualquer garfo, isso destrói a espera em círculo e não ocorre o travamento.
Revezamento justo 
Para garantir que nenhum filósofo fique sem comer enquanto os outros comem o tempo todo, o código do Python organiza quem pediu o garfo primeiro, assim que um garfo é liberado, a preferência é de quem estava esperando na fila há mais tempo.

Fotos dos nossos testes (Prints) 

Versão com erro (img/parte1-trava.png)
Versão corrigida (img/parte1-corrigida.png) 


## Parte 2 - Semafaro
O que acontece na prática (O teste do contador)
Nós colocamos 8 threads para aumentar o valor de um contador compartilhado até o total de 1.600.000, rodamos as duas versões no terminal por 3 vezes e coletamos os dados abaixo:

Versão do Código
Execução
Valor Esperado
Valor Obtido (Real)
Tempo de Execução
Sem Sincronização (versaoQueTrava.py)
1ª vez
1600000
1600000
0.0835s
Sem Sincronização (versaoQueTrava.py)
2ª vez
1600000
1600000
0.0896s
Sem Sincronização (versaoQueTrava.py)
3ª vez
1600000
1600000
0.0850s
Com Semáforo (versaoCorrigida.py)
1ª vez
1600000
1600000
1.7204s
Com Semáforo (versaoCorrigida.py)
2ª vez
1600000
1600000
1.6000s
Com Semáforo (versaoCorrigida.py)
3ª vez
1600000
1600000
1.6400s


## Análise dos Resultados e o Efeito do GIL no Python
Em outros sistemas, rodar várias threads juntas sem proteção faz com que uma atropele a outra, fazendo o contador perder as contas a chamada condição de corrida.
No nosso teste em Python, a versão sem proteção deu o valor certinho 1.600.000, isso aconteceu por causa de um mecanismo do próprio Python chamado GIL Trava Global do Interpretador, o GIL funciona como um guarda de trânsito que só deixa uma thread se mexer por vez no processador, como a nossa conta de somar 1 (count = count + 1) é muito simples e rápida, o Python conseguiu começar e terminar a soma de cada thread sem que outra entrasse no meio para atrapalhar.

## Por que a versão com Semáforo é correta e qual o seu preço (Trade-off)?
O semáforo garante que o código funcione de forma segura em qualquer situação, porque ele funciona como um cadeado, só deixa uma única thread mexer no contador por vez, O preço disso (Trade-off): O código fica seguro, mas o programa ficou mais lento, o tempo de execução subiu de 0.08 segundos para a faixa de 1.6 segundos, isso acontece porque as threads perdem a liberdade de rodar juntas, elas são obrigadas a parar em uma fila organizada, esperando a sua vez de pegar a "chave" do semáforo.

## Visibilidade e Ordenação (Barreiras de Memória)
O semáforo do Python também funciona como uma barreira de memória, ela garante uma visibilidade, isso significa que tudo o que uma thread somou no contador enquanto estava segurando a chave é atualizado na mesma hora, assim que ela solta o semáforo, a próxima thread da fila vai ver o valor novo e atualizado, impedindo que o computador use números velhos ou perdidos na memória.

Foto do teste (img/parte2.png)

## Parte 3 - DeadLock
Código que funciona (versaoCorrigida.py): Roda sem nenhum problema. Ele mostra as mensagens das duas threads na tela e termina com a frase "Programa concluiu". 

Código que trava (versaoQueTrava.py): O programa congela. Ele avisa que a Thread 1 pegou o Lock A e que a Thread 2 pegou o Lock B, mas por causa do tempo de espera, nenhuma das duas consegue continuar. O programa fica parado ali para sempre. 
Por que o código trava? As 4 regras de Coffman
O travamento acontece porque o código realiza corretamente as 4 regras que criam um deadlock:
Exclusão Mútua: Os locks cadeados são exclusivos. Se uma thread pegou o Lock A, nenhuma outra pode mexer nele até que ele seja solto.
Segurar e Esperar: A Thread 1 pega o Lock A e fica segurando ele enquanto tenta pegar o Lock B. Do outro lado, a Thread 2 faz o contrário: segura o Lock B e fica esperando o Lock A liberar.
Ninguém tira à força: O sistema não tira o cadeado de uma thread para dar para a outra. O cadeado só é solto se a própria thread mandar abrir.
Espera em Círculo: A Thread 1 está travada esperando a Thread 2 soltar o Lock B. E a Thread 2 está travada esperando a Thread 1 soltar o Lock A. Uma fica dependendo da outra e ninguém sai do lugar.

## Como resolvemos o problema?
No código versaoCorrigida.py, nós resolvemos isso criando uma regra de ordem, onde as duas threads são obrigadas a pegar o Lock A primeiro, e depois tentar pegar o Lock B, se a Thread 1 chegar primeiro e pegar o Lock A, a Thread 2 vai ter que esperar na primeira linha de código dela, sem conseguir pegar nada, isso dá tempo para a Thread 1 pegar o Lock B, fazer o seu trabalho, terminar e soltar os dois cadeados, com essa regra,  destruímos a espera em círculo, porque não foi possível uma thread prender a outra em um ciclo sem fim

Foto do teste(img/parte3.png)


## Link do vídeo no YouTube:
