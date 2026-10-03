# A skill de Instagram, em português do Brasil

Treze skills do Claude que tocam uma conta de Instagram. De graça, MIT, sem
cadastro, sem chave de API, nada pra conectar.

Uma delas escreve seus Reels a partir de 26 fórmulas de gancho e dá nota pro
gancho antes de você gastar uma gravação nele. Uma vai atrás dos Reels que
estão funcionando de verdade no seu nicho e ranqueia pelo quanto cada um
superou a própria conta. Uma escreve a legenda e mostra exatamente o que o
feed mostra antes do "... mais". Uma dá nota de 0 a 100 pro seu perfil e
reescreve o que perdeu ponto. Uma planeja a semana.

E uma é o humanizador, que é o motivo de as outras serem usáveis. Ele tira os
travessões, os clichês de IA e os caracteres invisíveis de marca d'água de um
rascunho, e depois dá nota ao que sobrou num painel de cinco checagens antes
de você ver.

**Nada é postado até você dizer sim.** Estas skills escrevem. Quem posta é
você.

Esta é a adaptação pro Brasil do
[instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill)
original, de Jake Schincariol. Não é só tradução: as ferramentas leem
português (acento, "R$ 18.000", "doze", "perdi" sem o "eu"), o léxico de
clichês é brasileiro, as 26 fórmulas foram reescritas pra fala brasileira e a
legenda confere a marcação de publi.

## Instalação

Cole isto no Claude:

```
https://github.com/Lantech01/instagram-agent-skill

Instala essa skill e confirma que o /ig-reel funciona.
```

Ou faça você mesmo, no Claude Code:

```bash
git clone https://github.com/Lantech01/instagram-agent-skill.git
cp -r instagram-agent-skill/skills/ig-* ~/.claude/skills/
```

Ou como plugin:

```
/plugin marketplace add Lantech01/instagram-agent-skill
/plugin install instagram-agent
```

Abriu este repositório no Claude Code? As treze já carregam sozinhas, pela
pasta `.claude/skills/`. Pra usar só num projeto seu, copie as mesmas pastas
pro `.claude/skills/` dele. Sem Claude Code? Cole qualquer `SKILL.md` no
começo de uma conversa e ele funciona como um modo. Você perde as ferramentas
em Python, que são a maior parte do valor do `/ig-reel` e do `/ig-human`, mas
o resto funciona.

Depois, gaste dez minutos no `templates/voice.md`. Copie pra
`~/.claude/instagram/voice.md` e preencha, ou mande três Reels seus pro Claude
e diga "escreve meu voice.md a partir desses". Toda skill lê esse arquivo. Ele
importa mais aqui do que em outras redes, porque você vai ter que falar as
palavras em voz alta.

No Claude Code na nuvem, a pasta `~/.claude` é apagada quando a sessão
termina, e o `voice.md`, o swipe file e o histórico de posts vão junto.
Guarde uma cópia do seu `voice.md` em algum lugar seu.

## As treze

| comando | o que faz |
| --- | --- |
| `/ig-reel` | Uma ideia vira um Reels. Três ganchos tirados de [26 fórmulas](skills/ig-reel/hooks.json), com nota, depois o roteiro, o texto na tela e um roteiro cronometrado. |
| `/ig-viral` | Vai atrás do que está funcionando no seu nicho, ranqueia pelo múltiplo sobre a mediana de cada conta, dá nome à fórmula e escreve o swipe file. |
| `/ig-caption` | A legenda, revisada. Mostra os 125 caracteres que o feed realmente mostra antes do toque, e confere a marcação de publi. |
| `/ig-carousel` | Carrossel. A capa que faz arrastar, o texto de cada slide e os arquivos em 1080x1350. |
| `/ig-story` | A sequência de stories do dia, qual figurinha faz qual trabalho, e o funil de DM que começa com a pessoa mandando mensagem primeiro. |
| `/ig-profile` | Dá nota ao seu perfil numa [rubrica de 12 itens](skills/ig-profile/rubric.json), de 0 a 100, e reescreve na ordem do que corrigir primeiro. |
| `/ig-plan` | A semana. O que postar, em que formato, quando (horário de Brasília), e as 10 contas com quem interagir. |
| `/ig-human` | O humanizador. Dois scripts que rodam de verdade. Veja abaixo. |
| `/ig-comment` | Comentários em posts dos outros. Nove tipos, escolhidos pelo que o post realmente é. Nunca "🔥🔥🔥". |
| `/ig-reply` | Os comentários do seu post. Separa em palavra-chave / lead / conteúdo / pergunta / apoio / ruído, e responde nessa ordem. |
| `/ig-dm` | A entrega da palavra-chave, a primeira mensagem, a proposta de parceria (publi paga ou permuta) e os dois follow-ups. Dois. |
| `/ig-repurpose` | Um vídeo, podcast, live ou newsletter vira uma semana de Reels e carrosséis que se sustentam sozinhos. |
| `/ig-audit` | Autópsia do que você já postou. Ranqueia pelo múltiplo e pelos compartilhamentos por alcance, não por views. |

## As ferramentas que rodam de verdade

Sem dependência, sem rede, nada enviado pra lugar nenhum. Rodam na sua
máquina, no seu texto. Toda a saída é em português, com número no formato
brasileiro.

### Ganchos

```bash
python3 hookscore.py ganchos.txt             # ranqueia as suas opções
python3 beats.py roteiro.txt --target 30     # cronometra antes de gravar
```

```
RANKING DE GANCHOS
==============================================================================
->  84,4 FORTE  Ninguém te conta que os seus primeiros 30 Reels vão flopar.
        mais fraca: TENSÃO (70)
    80,0 FORTE  Perdi R$ 18.000 por causa de uma cláusula que faltava no co...
        mais fraca: DIRECIONAMENTO (70)
    51,6 OK     Para de rolar o feed se você quer crescer no Instagram em 2...
        mais fraca: TENSÃO (70)
        eliminatório: Abre com "para de rolar o feed". Pedir atenção prova que você ainda não conquistou.
        eliminatório: Emoji no gancho. Texto na tela no tamanho de gancho tem espaço pra palavra ou pra emoji, não pros dois.
     9,6 FRACO  Oi gente, hoje eu queria falar sobre estratégia de conteúdo
        mais fraca: ABERTURA (0)
        eliminatório: Saudação. Ninguém abriu o feed pra ser cumprimentado.
```

O `beats.py` estima quanto tempo cada frase leva pra ser dita, empilha tudo em
minutagem e aponta as quatro coisas que matam um Reels na edição: um gancho
que passa de três segundos, uma batida longa o bastante pra pessoa ir embora,
uma sequência de frases sem nada concreto e a falta de um loop de volta pra
primeira frase.

```
ROTEIRO CRONOMETRADO  ·  62 palavras  ·  ~22,6s a 165 ppm  ·  meta 20s
============================================================================
  0:00,0   3,3s  GANCHO     Uma tabela de medidas me custava 12% das vendas.
                            ^ o gancho leva 3,3s, passa da marca de 3s
  0:03,3   3,6s             Doze de cada cem pedidos voltavam. Quase sempre pelo tamanho.
  0:06,9   3,6s             A minha tabela dizia P, M e G. Só isso.
  0:10,6   2,2s  MEIO       Troquei por centímetros. Busto, cintura, quadril.
  0:12,7   3,3s             E coloquei uma foto da peça na fita métrica.
  0:16,0   3,6s             Em dois meses, as devoluções caíram de 12% para 4%.
  0:19,6   2,9s  CTA        Comenta TABELA que eu te mando o modelo.
----------------------------------------------------------------------------
  - A batida 1 leva 3,3s pra ser dita. Corte pra 8 palavras ou menos, ou o gancho chega depois que a decisão já foi tomada.
  - As batidas 3-5 não têm nada concreto. Coloque um número, um nome ou um preço em uma delas.
  - Loop: a última batida repete "tabela" do gancho. Segunda visualização é alcance de graça.
  - 2,5s acima da meta. Corte umas 7 palavras.
```

O ritmo padrão é 165 palavras por minuto. Palavra em português costuma ser
mais comprida que em inglês, então cronometre você lendo um roteiro em voz
alta e passe `--ppm` com o seu número.

### A legenda

```bash
python3 caption.py legenda.txt --keywords "contrato,cláusula de pagamento"
python3 caption.py legenda.txt --publi
```

O Instagram dá uns 125 caracteres pra legenda no feed e esconde o resto atrás
de um toque. Quase toda legenda que falha, falha ali. Então a primeira coisa
que isto imprime é essa janela, numa caixa, do jeito que um estranho rolando o
feed lê:

```
  O QUE O FEED MOSTRA
  +------------------------------------------------------+
  | Perdi R$ 18.000 por causa de uma cláusula que        |
  | faltava no contrato, e o pior é que eu tinha lido o  |
  | documento duas vezes antes                           |
  +-------------------------------------------- ... mais +

  OK    TAMANHO          375 / 2200 caracteres
  AVISO PRIMEIRA LINHA   136 caracteres, então é cortada no 125 no meio da ideia. Tudo bem se o corte for um suspense, ruim se for uma oração subordinada
  OK    GANCHO CONCRETO  3 número(s) ou nome(s) na janela visível
  OK    HASHTAGS         3 tag(s): #freelancer #contratos #prestadordeservico
  OK    LUGAR DAS TAGS   as tags estão depois do corte
  OK    LINKS            nenhum link morto no texto
  OK    UM PEDIDO        uma chamada pra ação: comentar uma palavra-chave
  OK    EMOJI            0 emoji, 0,0 por 100 caracteres
  AVISO BUSCA            1/2 presentes, 1 na janela visível. Faltando: cláusula de pagamento
```

Ele aplica o limite atual de hashtags, que é **cinco por post**, não trinta. O
Instagram cortou em 18 de dezembro de 2025.

**Publi.** Se o post é pago ou permuta, passe `--publi`. O Código do CONAR
(art. 28) diz que anúncio tem que ser claramente identificado como anúncio. A
checagem `PUBLI` confere se "publi", "publicidade" ou "parceria paga" aparece
antes do "... mais", e roda sozinha quando a legenda já menciona publi em
algum lugar. Ela confere o texto; não é parecer jurídico.

### O humanizador

```bash
python3 humanize.py rascunho.txt --report    # limpa e mostra cada troca
python3 detect.py rascunho.txt                # dá nota, cinco checagens
python3 detect.py antes.txt depois.txt        # prova a diferença
```

<<HUMANIZADOR>>

### O swipe file

```bash
python3 swipe.py coletados.tsv --out ~/.claude/instagram/swipe.md
```

View bruta não é evidência. Uma conta de 2.000.000 de seguidores fazendo
400.000 views teve uma terça fraca. Uma conta de 4.000 seguidores fazendo
400.000 views achou alguma coisa. O `swipe.py` ranqueia pelo múltiplo sobre a
mediana da própria conta, dá nome à fórmula do gancho e mostra o que separa o
terço de cima do terço de baixo. Cabeçalho em português ou inglês, números
como "412.000", "412 mil", "48k" ou "1,2 mi".

```
SWIPE FILE  ·  4 reels  ·  4 contas  ·  base: mediana da conta
================================================================================
    38,5x  gancho  79  #3  Ninguém Te Conta       @conta_a            412.000
           "ninguém te conta que os seus primeiros 30 reels são pra flopar mesmo"
    11,2x  gancho  51  #9  Rouba Isso             @conta_c            180.000
           "rouba esse follow-up de quatro linhas que eu levei dois anos pra montar"
     7,5x  gancho  51  #2  Pare de Fazer Isso     @conta_d             71.000
           "para de postar todo dia e começa a responder comentário"
     1,3x  gancho  34  -   sem classificação      @conta_e             52.000
           "eu tava conversando com uma amiga outro dia sobre isso"
```

## O que foi medido, e o que ainda não foi

Esta é a parte que vale ler.

**A versão original, em inglês, foi testada.** O autor, Jake Schincariol,
transcreveu os três primeiros segundos de 74 ganchos reais de vídeos curtos:
os oito melhores e os oito piores de cinco canais, de 931 a 550.000 views.
Foram YouTube Shorts, porque o Instagram não entrega contagem de views que dê
pra coletar sem entrar na conta de alguém.

- **Pega gancho ruim bem.** Contra dez ganchos escritos de propósito pra ser
  ruins, AUC 0,83, e nove dos dez ficaram abaixo da mediana do acervo real.
- **Não escolhe vencedor.** Separando os acertos de um bom criador dos
  fracassos do mesmo criador: AUC 0,56, onde 0,50 é cara ou coroa. Das cinco
  checagens, só a de concretude separou os grupos de forma relevante.
- **O classificador de fórmulas estava quebrado, e foi o teste que pegou.** As
  regex nomeavam 8% dos ganchos reais. Reescritas contra fala transcrita,
  chegaram a 49%. Nos outros 51% ele se abstém, o que é o certo: muito vídeo
  curto é corte de podcast sem fórmula nenhuma.

**A versão brasileira ainda não foi medida.** As cinco checagens são as
mesmas, com listas de palavras em português, mas os limites vêm do original e
ninguém ainda rodou isto contra ganchos brasileiros reais. As regex das 26
fórmulas foram escritas pra fala brasileira e testadas só contra frases
escritas por quem escreveu as regex. Na primeira passada, antes de qualquer
ajuste, nomearam uns 77% a 79% desses ganchos e acertaram a fórmula em uns
97% dos que nomearam. Isso é checagem de sanidade, não medição: fala real vai
dar menos, e o original em inglês chegou a 49%.

Então o uso honesto é o mesmo: mate os ganchos obviamente fracos antes de
gravar, e depois confie no seu gráfico de retenção. Nada que lê texto
consegue dizer qual de dois ganchos decentes vai rodar, porque isso depende
do seu rosto, da sua edição, do seu áudio e de pra quem o Instagram mostra.

Se você rodar isto contra ganchos brasileiros reais e tiver um número, abra
uma issue. O método está descrito no [`/ig-viral`](skills/ig-viral/SKILL.md).

## As letras miúdas, que são a parte honesta

**Estas skills não postam no Instagram.** Existe uma API oficial de
publicação pra contas profissionais, e ela exige um app de desenvolvedor na
Meta, uma página vinculada, um token de longa duração e revisão do app, o
que não é algo que uma skill consegue te entregar. Todo o resto que as
pessoas usam pra automatizar postagem, comentário, follow ou DM é automação
de navegador ou ferramenta de terceiros, e as duas coisas violam os
[Termos de Uso do Instagram](https://help.instagram.com/581066165581870) e
fazem contas levarem bloqueio de ação. Então toda skill aqui termina do mesmo
jeito: um bloco pronto pra copiar, e você posta. Isso não é limitação colada
depois, é o desenho, e é por isso que a aprovação é de verdade e não uma
configuração.

A única exceção são as respostas automáticas por palavra-chave na DM, que o
Instagram permite pelas ferramentas dele e por parceiros aprovados, e que só
disparam depois que a pessoa comenta primeiro. O `/ig-dm` diz onde fica essa
linha.

**O `/ig-viral` lê, não raspa.** Dez contas, uma dúzia de Reels cada, em
velocidade de gente, com você no controle do seu próprio navegador. Ele nunca
pede sua senha e nunca entra como você. Coleta automatizada em volume é o que
faz conta ser restringida, e um crawler não é o que isto é.

**As cinco checagens de detecção são heurísticas locais, não APIs de
detector.** Foram modeladas nos sinais que os detectores públicos observam e
rodam inteiras na sua máquina. Não são GPTZero, Originality, Copyleaks,
Winston nem Turnitin, não chamam esses serviços e não têm como prometer o
veredito deles. Corrigir o que elas medem costuma mexer nesses números,
porque elas medem as mesmas coisas por baixo. Essa é a afirmação inteira.
Ninguém consegue te vender "indetectável" com honestidade, e quem vende está
te vendendo outra coisa.

**A limpeza de caracteres invisíveis é real e é estreita.** Ela remove os
caracteres de largura zero e de formatação que acabam em texto gerado e
sobrevivem ao copiar e colar. É uma marca real e verificável. Não é uma
afirmação de derrotar um esquema criptográfico de marca d'água, e este
repositório não faz essa afirmação.

**Nada aqui inventa.** Nenhuma métrica, cliente ou resultado inventado vai
pro seu nome. Se o rascunho precisa de um número que você não deu, ele volta
com `{{seu número}}` e um aviso, sempre.

**Publi é publicidade.** Se o conteúdo é pago ou permuta, ele precisa ser
identificado como publicidade (Código do CONAR, art. 28). O `/ig-caption` e o
`/ig-dm` lembram disso, e o `caption.py --publi` confere a legenda. Isso não
substitui orientação jurídica.

**Número de plataforma envelhece.** O limite de hashtags caiu de 30 pra 5 em
dezembro de 2025 enquanto o original era escrito, e o revisor ainda tinha o
número antigo até alguém conferir. Se alguma coisa aqui contradiz o que o
Instagram está fazendo quando você ler, o Instagram está certo.

## Arquivos

```
skills/ig-reel/hooks.json          26 fórmulas de gancho: modelo, exemplo, versão pra tela,
                                   pra que serve, como estraga, e uma regex de reconhecimento
skills/ig-reel/hookscore.py        o painel de cinco propriedades do gancho
skills/ig-reel/beats.py            roteiro pra roteiro cronometrado
skills/ig-caption/caption.py       a prévia do corte e o revisor de legenda
skills/ig-human/slop.json          <<LEXICO>>
skills/ig-human/humanize.py        as três passadas de limpeza
skills/ig-human/detect.py          o painel de cinco checagens
skills/ig-viral/swipe.py           ranking por múltiplo e classificação de fórmula
skills/ig-profile/rubric.json      a nota de 100 pontos do perfil
templates/voice.md                 o seu perfil de voz. Preencha primeiro.
.claude/skills/                    atalhos pras 13 skills, pra elas carregarem neste repositório
```

## Créditos

Original de Jake Schincariol, [opusjake.ai](https://opusjake.ai):
[instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill).
Repositório irmão, mesma ideia pra outra rede:
[linkedin-agent-skill](https://github.com/Jakeschincariol/linkedin-agent-skill).

Adaptação pro português do Brasil neste fork.

## Licença

MIT. Pegue, mude, publique.
