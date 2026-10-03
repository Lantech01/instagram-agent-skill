---
name: ig-comment
description: >-
  Escreve comentários nos posts e Reels dos outros que soam como uma pessoa com
  opinião, não como robô. Use quando o usuário colar um post ou um Reels e
  quiser um comentário, disser "comenta nesse post", "o que eu comento aqui",
  "escreve um comentário pra esse reels", "quero engajar nesse perfil", ou
  quiser um lote pra rodada diária de engajamento.
---

# ig-comment

Comentar são os vinte minutos de maior retorno no Instagram e os mais fáceis
de fazer mal. Um comentário no topo de um Reels com 40.000 visualizações é
visto por mais gente do que a maioria dos posts da maioria das contas, e é o
único lugar onde um estranho pode tocar e cair direto num perfil.

Um comentário genérico é pior do que nenhum. Ele gasta um toque que não leva a
lugar nenhum e marca a conta como conta de grupo de engajamento pra única
pessoa cuja opinião importava, que é quem fez o post.

## Entrada

O usuário cola o texto do post ou do Reels, ou um print, com o nome da conta.
Se ele mandar uma URL que você não consegue abrir, peça pra colar. Não use
ferramenta de navegador pra raspar o feed e não poste nada.

## Os nove tipos de comentário

Escolha pelo que o post é de verdade. Nunca caia no tipo 1 por padrão.

| # | tipo | quando | formato |
| --- | --- | --- | --- |
| 1 | **Acrescente um dado** | o post faz uma afirmação que você consegue sustentar com um número | "Aqui foi igual: 40% dos..." |
| 2 | **Acrescente o caso que faltou** | o post está certo, mas incompleto | "Isso vale até {condição}." |
| 3 | **Discorde com respeito** | você acha de verdade que está errado | diga primeiro onde concorda, depois onde diverge |
| 4 | **Estenda uma frase** | uma frase do post é a boa | cite, construa em cima |
| 5 | **Faça a pergunta de verdade** | o post pulou a parte difícil | uma pergunta, específica |
| 6 | **O relato** | você já fez o que o post descreve | o que aconteceu, em duas frases |
| 7 | **A correção** | tem um erro factual | esteja certo, seja breve, seja gentil, tenha certeza |
| 8 | **O outro ângulo** | fatos certos, leitura errada | "Outro jeito de ler isso:" |
| 9 | **A frase curta** | o post não precisa de nada, você quer marcar presença | menos de 10 palavras, tem que ser engraçada ou verdadeira |

## Regras

- **Uma a três frases.** Comentário no Instagram é lido numa coluna estreita
  embaixo de um vídeo. Um parágrafo fica escondido atrás do "mais" e ninguém
  toca.
- **Nunca abra com** "Amei", "Que conteúdo!", "Perfeito", "Arrasou", "Isso
  👏", "Precisava ler isso hoje", "Salvando!" ou o primeiro nome de quem
  postou com ponto de exclamação. Todos são invisíveis.
- **Nada de comentário só com emoji** e nada de emoji como primeiro caractere.
  "😍😍😍" e "🔥🔥" estão embaixo de todo post brasileiro, e é exatamente por
  isso que ninguém lê.
- **"kkkk" sozinho é emoji com outro nome.** Se a piada foi boa, diga qual
  parte. Rir no fim de uma frase que tem conteúdo tudo bem; rir no lugar da
  frase, não.
- **Escreva como gente fala.** "Pra", "tá", "a gente". Um comentário com cara
  de e-mail corporativo destoa embaixo de um Reels tanto quanto um robô.
- **Nunca resuma o Reels.** Todo mundo que está vendo acabou de assistir.
- **Uma ideia.** Um comentário com dois pontos parece que está sequestrando o
  post.
- **Diga a coisa específica.** Se o comentário caberia embaixo de qualquer
  post sobre o assunto, não é comentário, é ruído.
- **Nunca venda nada.** Nem a oferta, nem o link, nem "dá uma olhada no meu
  perfil", nem "segue que eu sigo de volta". É o jeito mais rápido de ser
  bloqueado justamente pela pessoa que você queria alcançar.
- **Chegar cedo importa mais aqui do que em qualquer outro lugar.** Um
  comentário na primeira hora de um Reels que depois viraliza vai junto com
  ele.

## Saída

Dê **duas opções de tipos diferentes**, com rótulo, mais uma linha dizendo
qual você postaria e por quê. Passe as duas pelo `/ig-human` antes: comentário
é curto, então um travessão ou uma frase pronta grita proporcionalmente mais do
que numa legenda.

```
OPÇÕES DE COMENTÁRIO  (no Reels da @conta sobre preço)

[6 · Relato]
A gente subiu o preço 40% em março do ano passado e perdeu um cliente só, justo
o que ocupava metade da caixa de entrada. Levei oito meses pra parar de ter
medo disso.

[3 · Discordância respeitosa]
Concordo com a ancoragem. Onde eu discordo é fazer isso no meio do projeto. A
gente tentou e perdeu uma renovação que estava tranquila.

Posta o primeiro. Ele admite uma coisa e tem um número.
```

## Modo lote

Pra uma rodada de engajamento, peça os 5 a 10 posts como texto colado numa
mensagem só, devolva um comentário pra cada num bloco único e mantenha uma
nota corrente em `~/.claude/instagram/log.md` de quem já recebeu comentário
nesta semana. Comentar nas mesmas três contas todo dia aparece, e parece
exatamente o que é.

## Nunca

Não poste automaticamente, não automatize comentários e não use ferramenta de
navegador pra publicar no lugar do usuário. Engajamento automatizado viola os
Termos de Uso do Instagram e leva a conta a bloqueio de ação. Esta skill
escreve o comentário. Quem posta é o usuário.
