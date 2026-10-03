---
name: ig-human
description: >-
  Tira a digital de máquina de qualquer rascunho (travessões, clichês de IA,
  caracteres invisíveis de marca d'água) e dá nota a ele num painel de cinco
  checagens antes de sair. Use sempre que um texto precisar soar humano,
  quando o usuário disser "humaniza", "isso tá com cara de IA", "tira os
  travessões", "tira os clichês", "parece texto do ChatGPT", "deixa mais
  natural", ou antes de qualquer legenda, roteiro, comentário, resposta ou DM
  ser mostrado ao usuário.
---

# ig-human

Duas ferramentas moram nesta pasta, e as duas rodam de verdade. Use as duas.
Não faça isso no olho.

```bash
python3 humanize.py rascunho.txt --report       # limpa e mostra o que mudou
python3 detect.py rascunho.txt                   # dá nota, cinco checagens
python3 detect.py antes.txt depois.txt           # prova a diferença
```

As duas leem o `slop.json`: 213 palavras e expressões de clichê em português
do Brasil, 18 classes de caracteres invisíveis, 11 trocas tipográficas e 18
vícios de estrutura. O último bloco de cada
lista é do Instagram brasileiro, o vocabulário que só aparece em legenda e
locução. O arquivo foi feito pra ser editado. Se o usuário tem uma palavra que
ele sempre usa e o léxico arranca, tire do arquivo.

## Por que isso importa mais no Instagram do que parece

Legenda é curta e roteiro é falado em voz alta. Uma frase com cara de texto
escrito numa legenda de 600 caracteres é uma fatia maior do texto do que a
mesma frase numa redação, e uma locução que ninguém conseguiria falar com
naturalidade fica óbvia na primeira gravação. A marca aqui não é um detector
sinalizando o post. A marca é uma pessoa passando direto por algo que soa como
marca, ou um criador tropeçando no próprio roteiro.

## O que é corrigido automaticamente

**1. Caracteres invisíveis.** Espaços e junções de largura zero, word
joiners, hífens suaves, BOMs, caracteres de tag Unicode, separadores
invisíveis, espaços rígidos e estreitos. Teclado não produz isso. Eles
sobrevivem ao copiar e colar, são invisíveis em qualquer editor e são a coisa
mais mecânica de um texto gerado. O `humanize.py` apaga todos, inclusive
qualquer caractere de formatação Unicode que ele não conheça pelo nome.

**2. Tipografia.** Travessão vira vírgula, meia-risca vira hífen, aspas curvas
viram retas, reticências de um caractere viram três pontos, marcador vira
hífen. A passada do travessão é a que importa: ela troca o travessão por
vírgula e depois limpa a pontuação dobrada e os pontos órfãos que sobram.
Travessão de diálogo no começo da linha também sai.

**3. O léxico de clichês.** "Utilizar" vira "usar", "alavancar" e
"potencializar" viram "melhorar", "desvendar" vira "entender", "proporcionar"
vira "oferecer", "no mundo atual" vira "hoje", "vale ressaltar que" vira
"note que". Do bloco do Instagram: "conteúdo de valor" vira "conteúdo útil",
"impactar vidas" vira "ajudar pessoas", "ninguém fala sobre isso" vira "pouca
gente fala disso", e "simplesmente" é apagado. Tudo preservando maiúsculas e
sem mexer em links, hashtags e menções.

**Em português, muita troca automática sai errada.** Verbo conjuga,
adjetivo concorda, preposição contrai ("no", "na", "num"), e muita palavra de
clichê tem um sentido literal normal ("jornada de trabalho"). Por isso 119
dos 213 termos são só **sinalizados**: contam na nota e aparecem no relatório
com "-> (reescreva você)", mas o texto fica como estava. "Mergulhar",
"jornada", "além disso" e "dessa forma" estão nesse grupo, e também os
pedidos prontos do Instagram ("para de rolar", "fica até o final", "salva
esse post", "marca aquele amigo", "segue pra mais", "o algoritmo ama", "corre
que"), porque apagar um deles deixa pedaço de frase pra trás. Frase quebrada
é pior que clichê.

## O que NÃO é corrigido automaticamente

Vícios de estrutura são **apontados, não reescritos**, porque mudar o formato
de uma frase exige julgamento:

- "Não é só X, é Y", "Não só X, mas também Y" e "Não é sobre X. É sobre Y."
- Revelação encenada: "O resultado?", "E o melhor?", "Spoiler:"
- Anúncio antes do ponto: "A verdade é que", "Aqui está o que eu aprendi"
- Trio de palavras: "foco, disciplina e constância"
- Gancho hipotético: "Você já se perguntou...?", "Imagine só"
- "Seja você X ou Y"
- Fecho de redação escolar: "Em resumo", "Para concluir"
- Modelo falando de si: "Como uma IA..."
- O preâmbulo de vídeo: "no vídeo de hoje eu vou te mostrar"
- Abertura "para de rolar o feed"
- Lista com emoji no lugar do marcador, e emoji de foguete, fogo, lâmpada
- Três ou mais palavras gritadas seguidas
- Paredão de hashtags
- Isca no automático: "Concorda?", "Faz sentido?", "segue pra mais", "marca
  alguém que"

Essa lista é trabalho seu. Reescreva cada linha apontada na mão, mantendo o
sentido, e rode o `detect.py` de novo. É essa parte que leva a nota de REVISAR
pra APROVADO, e é a parte que script nenhum faz.

## As cinco checagens

O `detect.py` dá nota a cinco sinais de 0 a 100, quanto maior, mais humano:

| checagem | o que mede | cara de máquina |
| --- | --- | --- |
| RITMO | variação no tamanho das frases | toda frase do mesmo tamanho |
| CONCRETUDE | números, nomes e marcadores concretos a cada 100 palavras | substantivo abstrato, nenhum número |
| CLICHÊS | termos do léxico a cada 100 palavras | vocabulário pronto |
| DIGITAIS | invisíveis, travessões e aspas curvas a cada 1.000 caracteres | tipografia perfeita |
| VOZ | fala informal ("pra", "tá", "a gente", "né"), pessoa do discurso, vícios de estrutura | "para", "nós", "está", revelações encenadas |

O veredito pesa a média em 60% e a **checagem mais fraca** em 40%, porque um
sinal basta. APROVADO precisa de 70 ou mais no geral e nenhuma checagem
abaixo de 55.

Os limites de cada checagem vêm da versão original em inglês e ainda não
foram calibrados com textos brasileiros. A checagem de VOZ, em especial, mede
fala informal: um texto formal escrito por gente (um e-mail pra marca, um
contrato) vai tirar nota baixa nela sem ser de máquina. Leia a nota como
orientação.

## Diga isso com honestidade

São cinco heurísticas locais, modeladas nos sinais que os detectores públicos
observam. Rodam inteiras na máquina do usuário e nada é enviado. **Não** são
GPTZero, Originality, Copyleaks, Winston ou Turnitin, não chamam essas APIs e
não têm como prometer esses vereditos. Corrigir o que elas medem costuma mexer
nesses números, porque elas medem as mesmas coisas por baixo. Essa é a
afirmação. Não faça uma maior em nome do usuário, e não diga a ninguém que o
texto é indetectável.

## Ordem das operações

1. `humanize.py rascunho.txt -o limpo.txt --report`
2. Leia os termos sinalizados e os vícios de estrutura. Reescreva essas
   linhas você mesmo.
3. `detect.py rascunho.txt limpo.txt` pra mostrar o antes e o depois.
4. Se o veredito não for APROVADO, corrija a checagem mais fraca que a saída
   aponta e rode de novo. Duas rodadas é normal. Cinco quer dizer que o
   rascunho foi escrito por fórmula, e a solução é outro rascunho, não mais
   passadas.
5. Mostre ao usuário o texto limpo e a nota. Nunca só a nota.
