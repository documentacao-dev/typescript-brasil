---
title: Noções básicas
layout: docs
permalink: /docs/handbook/2/basic-types.html
oneline: "Primeiro passo para aprender TypeScript: os tipos básicos."
preamble: >
  <p>Bem-vindo à primeira página do handbook. Se esta é sua primeira experiência com TypeScript, talvez você queira começar por um dos guias de '<a href='https://www.typescriptlang.org/docs/handbook/intro.html#get-started'>Primeiros passos</a>' </a>
ia-translate: true
---

Cada valor em JavaScript tem um conjunto de comportamentos que você pode observar ao executar diferentes operações.
Isso parece abstrato, mas, como exemplo rápido, considere algumas operações que poderíamos executar em uma variável chamada `message`.

```js
// Accessing the property 'toLowerCase'
// on 'message' and then calling it
message.toLowerCase();

// Calling 'message'
message();
```

Se analisarmos isso, a primeira linha executável acessa uma propriedade chamada `toLowerCase` e depois a chama.
A segunda tenta chamar `message` diretamente.

Mas, supondo que não saibamos o valor de `message` (e isso é bastante comum), não podemos dizer com segurança quais resultados vamos obter ao tentar executar qualquer um desses códigos.
O comportamento de cada operação depende inteiramente do valor que tínhamos desde o início.

- `message` é chamável?
- Ele tem uma propriedade chamada `toLowerCase`?
- Se tiver, `toLowerCase` é chamável?
- Se os dois valores forem chamáveis, o que eles retornam?

As respostas a essas perguntas geralmente são coisas que mantemos na cabeça ao escrever JavaScript, e temos que torcer para ter acertado todos os detalhes.

Digamos que `message` tenha sido definida da seguinte forma.

```js
const message = "Hello World!";
```

Como você provavelmente deve imaginar, se tentarmos executar `message.toLowerCase()`, obteremos a mesma string, apenas em minúsculas.

E a segunda linha de código?
Se você conhece JavaScript, sabe que isso falha com uma exceção:

```txt
TypeError: message is not a function
```

Seria ótimo se pudéssemos evitar erros como este.

Quando executamos nosso código, a forma como o runtime JavaScript escolhe o que fazer é descobrindo o _tipo_ do valor: que tipos de comportamentos e capacidades ele tem.
Isso é parte do que o `TypeError` está sugerindo: ele diz que a string `"Hello World!"` não pode ser chamada como função.

Para alguns valores, como os primitivos `string` e `number`, podemos identificar o tipo em tempo de execução usando o operador `typeof`.
Mas, para outras coisas, como funções, não existe um mecanismo de tempo de execução correspondente para identificar seus tipos.
Por exemplo, considere esta função:

```js
function fn(x) {
  return x.flip();
}
```

Podemos _observar_ lendo o código que essa função só vai funcionar se receber um objeto com uma propriedade `flip` chamável, mas o JavaScript não expõe essa informação de uma forma que possamos verificar enquanto o código está rodando.
A única maneira, em JavaScript puro, de saber o que `fn` faz com um determinado valor é chamá-la e ver o que acontece.
Esse tipo de comportamento dificulta prever o que o código vai fazer antes de ele rodar, o que significa que é mais difícil saber o que seu código vai fazer enquanto você o escreve.

Visto dessa forma, um _tipo_ é o conceito que descreve quais valores podem ser passados para `fn` e quais vão quebrar.
O JavaScript oferece apenas tipagem _dinâmica_ de verdade: executar o código para ver o que acontece.

A alternativa é usar um sistema de tipos _estático_ para fazer previsões sobre o que o código deve fazer _antes_ de ele rodar.

## Verificação de tipos estática {#static-type-checking}

Lembre-se daquele `TypeError` que recebemos antes, ao tentar chamar uma `string` como função.
_A maioria das pessoas_ não gosta de ver nenhum tipo de erro ao executar o código, porque eles são considerados bugs!
E, ao escrever código novo, fazemos o nosso melhor para não introduzir novos bugs.

Se adicionarmos só um pouco de código, salvarmos o arquivo, executarmos de novo e vermos o erro imediatamente, talvez consigamos isolar o problema rapidamente; mas nem sempre é assim.
Podemos não ter testado a funcionalidade com profundidade suficiente, então talvez nunca cheguemos a encontrar um possível erro que seria lançado!
Ou, se tivermos a sorte de presenciar o erro, talvez tenhamos feito grandes refatorações e adicionado muito código diferente, no qual somos obrigados a procurar.

Idealmente, teríamos uma ferramenta que nos ajudasse a encontrar esses bugs _antes_ de o código rodar.
É isso que um verificador de tipos estático como o TypeScript faz.
_Sistemas de tipos estáticos_ descrevem a forma e os comportamentos que nossos valores terão quando rodarmos nossos programas.
Um verificador de tipos como o TypeScript usa essas informações e nos avisa quando as coisas podem estar saindo do trilho.

```ts twoslash
// @errors: 2349
const message = "hello!";

message();
```

Executar esse último exemplo com o TypeScript vai nos dar uma mensagem de erro antes mesmo de rodarmos o código.

## Falhas que não são exceções {#non-exception-failures}

Até agora falamos de coisas como erros de tempo de execução: casos em que o runtime JavaScript nos informa que acha algo sem sentido.
Esses casos aparecem porque [a especificação do ECMAScript](https://tc39.github.io/ecma262/) tem instruções explícitas sobre como a linguagem deve se comportar quando encontra algo inesperado.

Por exemplo, a especificação diz que tentar chamar algo que não é chamável deve lançar um erro.
Talvez isso pareça um "comportamento óbvio", mas você poderia imaginar que acessar uma propriedade que não existe em um objeto também deveria lançar um erro.
Em vez disso, o JavaScript nos dá outro comportamento e retorna o valor `undefined`:

```js
const user = {
  name: "Daniel",
  age: 26,
};

user.location; // returns undefined
```

No fim das contas, um sistema de tipos estático precisa decidir quais códigos devem ser sinalizados como erro no próprio sistema, mesmo que sejam JavaScript "válido" que não vai lançar erro imediatamente.
No TypeScript, o código a seguir produz um erro dizendo que `location` não está definido:

```ts twoslash
// @errors: 2339
const user = {
  name: "Daniel",
  age: 26,
};

user.location;
```

Embora isso às vezes implique um compromisso sobre o que você consegue expressar, a intenção é capturar bugs legítimos nos nossos programas.
E o TypeScript captura _muitos_ bugs legítimos.

Por exemplo: erros de digitação,

```ts twoslash
// @noErrors
const announcement = "Hello World!";

// How quickly can you spot the typos?
announcement.toLocaleLowercase();
announcement.toLocalLowerCase();

// We probably meant to write this...
announcement.toLocaleLowerCase();
```

funções não chamadas,

```ts twoslash
// @noUnusedLocals
// @errors: 2365
function flipCoin() {
  // Meant to be Math.random()
  return Math.random < 0.5;
}
```

ou erros básicos de lógica.

```ts twoslash
// @errors: 2367
const value = Math.random() < 0.5 ? "a" : "b";
if (value !== "a") {
  // ...
} else if (value === "b") {
  // Oops, unreachable
}
```

## Tipos para ferramentas {#types-for-tooling}

O TypeScript consegue capturar bugs quando cometemos erros no código.
Isso é ótimo, mas o TypeScript _também_ pode nos impedir de cometer esses erros para início de conversa.

O verificador de tipos tem informações para checar coisas como se estamos acessando as propriedades certas de variáveis e de outras propriedades.
Com essas informações, ele também pode começar a _sugerir_ quais propriedades você pode querer usar.

Isso significa que o TypeScript também pode ser aproveitado para editar código, e o verificador de tipos central pode fornecer mensagens de erro e autocompletar enquanto você digita no editor.
É parte do que as pessoas costumam chamar de ferramentas (tooling) no TypeScript.

<!-- prettier-ignore -->
```ts twoslash
// @noErrors
// @esModuleInterop
import express from "express";
const app = express();

app.get("/", function (req, res) {
  res.sen
//       ^|
});

app.listen(3000);
```

O TypeScript leva as ferramentas a sério, e isso vai além de autocompletar e erros enquanto você digita.
Um editor que suporta TypeScript pode oferecer "correções rápidas" para corrigir erros automaticamente, refatorações para reorganizar o código com facilidade e recursos úteis de navegação, como pular para a definição de uma variável ou encontrar todas as referências a uma determinada variável.
Tudo isso é construído sobre o verificador de tipos e é totalmente multiplataforma, então é provável que [o seu editor favorito tenha suporte a TypeScript disponível](https://github.com/Microsoft/TypeScript/wiki/TypeScript-Editor-Support).

## `tsc`, o compilador do TypeScript {#tsc-the-typescript-compiler}

Estivemos falando de verificação de tipos, mas ainda não usamos nosso _verificador_ de tipos.
Vamos conhecer nosso novo amigo `tsc`, o compilador do TypeScript.
Primeiro, precisamos obtê-lo pelo npm.

```sh
npm install -g typescript
```

> Isso instala o compilador do TypeScript `tsc` globalmente.
> Você pode usar `npx` ou ferramentas semelhantes se preferir executar o `tsc` a partir de um pacote local em `node_modules`.

Agora vamos para uma pasta vazia e tentar escrever nosso primeiro programa em TypeScript: `hello.ts`:

```ts twoslash
// Greets the world.
console.log("Hello world!");
```

Repare que não há firulas aqui; esse programa "hello world" é idêntico ao que você escreveria para um programa "hello world" em JavaScript.
Agora vamos verificar os tipos executando o comando `tsc`, que foi instalado para nós pelo pacote `typescript`.

```sh
tsc hello.ts
```

Pronto!

Espera, "pronto" _o quê_, exatamente?
Executamos o `tsc` e nada aconteceu!
Bem, não houve erros de tipo, então não apareceu nenhuma saída no console, já que não havia nada para relatar.

Mas olhe de novo: obtivemos alguma _saída de arquivo_.
Se olharmos no diretório atual, veremos um arquivo `hello.js` ao lado de `hello.ts`.
Essa é a saída do nosso arquivo `hello.ts` depois que o `tsc` _compila_ ou _transforma_ o arquivo em JavaScript puro.
E, se conferirmos o conteúdo, veremos o que o TypeScript gera depois de processar um arquivo `.ts`:

```js
// Greets the world.
console.log("Hello world!");
```

Neste caso, havia pouco para o TypeScript transformar, então o arquivo ficou idêntico ao que escrevemos.
O compilador tenta emitir código limpo e legível, parecido com o que uma pessoa escreveria.
Embora nem sempre seja tão fácil, o TypeScript mantém a indentação consistente, cuida de quando o nosso código se estende por várias linhas e tenta preservar os comentários.

E se nós _introduzíssemos_ um erro de verificação de tipos?
Vamos reescrever o `hello.ts`:

```ts twoslash
// @noErrors
// This is an industrial-grade general-purpose greeter function:
function greet(person, date) {
  console.log(`Hello ${person}, today is ${date}!`);
}

greet("Brendan");
```

Se executarmos `tsc hello.ts` de novo, repare que recebemos um erro na linha de comando!

```txt
Expected 2 arguments, but got 1.
```

O TypeScript está nos avisando que esquecemos de passar um argumento para a função `greet`, e com razão.
Até agora, escrevemos apenas JavaScript padrão, e mesmo assim a verificação de tipos conseguiu encontrar problemas no nosso código.
Obrigado, TypeScript!

## Emitindo com erros {#emitting-with-errors}

Uma coisa que você talvez não tenha notado no último exemplo é que o nosso arquivo `hello.js` mudou de novo.
Se abrirmos esse arquivo, veremos que o conteúdo continua basicamente igual ao do arquivo de entrada.
Isso pode ser um pouco surpreendente, já que o `tsc` relatou um erro no nosso código, mas isso se baseia em um dos valores centrais do TypeScript: na maior parte do tempo, _você_ sabe mais do que o TypeScript.

Para reforçar o que vimos antes, verificar tipos limita os tipos de programas que você pode executar, então existe um compromisso sobre quais coisas o verificador de tipos considera aceitáveis.
Na maioria das vezes isso está tudo bem, mas há cenários em que essas verificações atrapalham.
Por exemplo, imagine que você está migrando código JavaScript para TypeScript e introduzindo erros de verificação de tipos.
Eventualmente você vai chegar a limpar as coisas para o verificador de tipos, mas aquele código JavaScript original já funcionava!
Por que converter para TypeScript deveria impedir você de executá-lo?

Então, o TypeScript não atrapalha o seu caminho.
Claro que, com o tempo, você pode querer se proteger mais contra erros e fazer o TypeScript agir de forma mais rigorosa.
Nesse caso, você pode usar a opção de compilador [`noEmitOnError`](/tsconfig#noEmitOnError).
Tente alterar seu arquivo `hello.ts` e executar o `tsc` com essa flag:

```sh
tsc --noEmitOnError hello.ts
```

Você vai notar que o `hello.js` nunca é atualizado.

## Tipos explícitos {#explicit-types}

Até agora, não dissemos ao TypeScript o que são `person` ou `date`.
Vamos editar o código para informar ao TypeScript que `person` é uma `string` e que `date` deve ser um objeto `Date`.
Também vamos usar o método `toDateString()` em `date`.

```ts twoslash
function greet(person: string, date: Date) {
  console.log(`Hello ${person}, today is ${date.toDateString()}!`);
}
```

O que fizemos foi adicionar _anotações de tipo_ em `person` e `date` para descrever quais tipos de valores `greet` pode receber.
Você pode ler essa assinatura assim: "`greet` recebe um `person` do tipo `string` e uma `date` do tipo `Date`".

Com isso, o TypeScript consegue nos avisar sobre outros casos em que `greet` possa ter sido chamada incorretamente.
Por exemplo...

```ts twoslash
// @errors: 2345
function greet(person: string, date: Date) {
  console.log(`Hello ${person}, today is ${date.toDateString()}!`);
}

greet("Maddison", Date());
```

Hein?
O TypeScript relatou um erro no nosso segundo argumento, mas por quê?

Talvez surpreendentemente, chamar `Date()` em JavaScript retorna uma `string`.
Por outro lado, construir um `Date` com `new Date()` nos dá exatamente o que esperávamos.

De qualquer forma, podemos corrigir o erro rapidamente:

```ts twoslash {4}
function greet(person: string, date: Date) {
  console.log(`Hello ${person}, today is ${date.toDateString()}!`);
}

greet("Maddison", new Date());
```

Tenha em mente que nem sempre precisamos escrever anotações de tipo explícitas.
Em muitos casos, o TypeScript consegue até _inferir_ (ou "descobrir") os tipos para nós, mesmo que os omitamos.

```ts twoslash
let msg = "hello there!";
//  ^?
```

Mesmo sem termos dito ao TypeScript que `msg` tem o tipo `string`, ele conseguiu descobrir isso.
Isso é um recurso, e o melhor é não adicionar anotações quando o sistema de tipos acabaria inferindo o mesmo tipo de qualquer forma.

> Observação: o balão de mensagem dentro do exemplo de código anterior é o que o seu editor mostraria se você passasse o mouse sobre a palavra.

## Tipos apagados {#erased-types}

Vamos ver o que acontece quando compilamos a função `greet` acima com o `tsc` para gerar JavaScript:

```ts twoslash
// @showEmit
// @target: es5
function greet(person: string, date: Date) {
  console.log(`Hello ${person}, today is ${date.toDateString()}!`);
}

greet("Maddison", new Date());
```

Repare em duas coisas aqui:

1. Os parâmetros `person` e `date` não têm mais anotações de tipo.
2. Nosso "template string" (aquela string que usa crases, o caractere `` ` ``) foi convertido em strings simples com concatenações.

Falaremos mais sobre o segundo ponto depois, mas vamos focar agora no primeiro.
Anotações de tipo não fazem parte do JavaScript (ou do ECMAScript, para ser preciso), então realmente não há navegadores ou outros runtimes que consigam rodar TypeScript sem modificação.
É por isso que o TypeScript precisa de um compilador para começar: ele precisa de alguma forma de remover ou transformar qualquer código específico do TypeScript para que você possa executá-lo.
A maior parte do código específico do TypeScript é apagada e, da mesma forma, aqui nossas anotações de tipo foram completamente removidas.

> **Lembre-se**: anotações de tipo nunca mudam o comportamento em tempo de execução do seu programa.

## Rebaixamento (downleveling) {#downleveling}

Outra diferença em relação ao exemplo acima foi que nosso template string foi reescrito de

```js
`Hello ${person}, today is ${date.toDateString()}!`;
```

para

```js
"Hello ".concat(person, ", today is ").concat(date.toDateString(), "!");
```

Por que isso aconteceu?

Template strings são um recurso de uma versão do ECMAScript chamada ECMAScript 2015 (também conhecida como ECMAScript 6, ES2015, ES6 etc. - _não pergunte_).
O TypeScript tem a capacidade de reescrever código de versões mais novas do ECMAScript para versões mais antigas, como ECMAScript 3 ou ECMAScript 5 (também conhecido como ES5).
Esse processo de passar de uma versão mais nova ou "mais alta" do ECMAScript para uma mais antiga ou "mais baixa" às vezes é chamado de _rebaixamento_ (downleveling).

Por padrão, o TypeScript tem como alvo o ES5, uma versão bem antiga do ECMAScript.
Poderíamos ter escolhido algo um pouco mais recente usando a opção [`target`](/tsconfig#target).
Executar com `--target es2015` faz o TypeScript ter como alvo o ECMAScript 2015, o que significa que o código deve conseguir rodar onde o ECMAScript 2015 for suportado.
Então, executar `tsc --target es2015 hello.ts` nos dá a seguinte saída:

```js
function greet(person, date) {
  console.log(`Hello ${person}, today is ${date.toDateString()}!`);
}
greet("Maddison", new Date());
```

> Embora o alvo padrão seja o ES5, a grande maioria dos navegadores atuais suporta o ES2015.
> A maioria dos desenvolvedores pode, portanto, especificar com segurança o ES2015 ou superior como alvo, a menos que a compatibilidade com certos navegadores muito antigos seja importante.

## Rigor (strictness) {#strictness}

Diferentes usuários chegam ao TypeScript procurando coisas diferentes em um verificador de tipos.
Algumas pessoas querem uma experiência mais flexível, de adesão opcional, que ajuda a validar apenas algumas partes do programa e ainda assim ter boas ferramentas.
Essa é a experiência padrão do TypeScript, em que os tipos são opcionais, a inferência assume os tipos mais permissivos e não há verificação de valores potencialmente `null`/`undefined`.
Assim como o modo como o `tsc` emite código mesmo diante de erros, esses padrões existem para não atrapalhar você.
Se você está migrando um JavaScript existente, isso pode ser um primeiro passo desejável.

Em contraste, muitos usuários preferem que o TypeScript valide o máximo possível desde o início, e é por isso que a linguagem também oferece configurações de rigor.
Essas configurações transformam a verificação de tipos estática de um interruptor (ou seu código é verificado ou não) em algo mais próximo de um botão de ajuste.
Quanto mais você aumenta esse botão, mais o TypeScript verifica por você.
Isso pode exigir um pouco de trabalho extra, mas, de modo geral, compensa a longo prazo e permite verificações mais completas e ferramentas mais precisas.
Sempre que possível, uma base de código nova deve ativar essas verificações de rigor.

O TypeScript tem várias flags de rigor da verificação de tipos que podem ser ativadas ou desativadas, e todos os nossos exemplos serão escritos com todas elas ativadas, salvo indicação em contrário.
A flag [`strict`](/tsconfig#strict) na CLI, ou `"strict": true` em um [`tsconfig.json`](https://www.typescriptlang.org/docs/handbook/tsconfig-json.html), ativa todas de uma vez, mas podemos desativá-las individualmente.
As duas mais importantes que você deve conhecer são [`noImplicitAny`](/tsconfig#noImplicitAny) e [`strictNullChecks`](/tsconfig#strictNullChecks).

## `noImplicitAny`

Lembre-se de que, em alguns lugares, o TypeScript não tenta inferir tipos para nós e, em vez disso, recorre ao tipo mais permissivo: `any`.
Isso não é a pior coisa que pode acontecer; afinal, recorrer a `any` é simplesmente a experiência de JavaScript puro de qualquer forma.

No entanto, usar `any` muitas vezes anula o propósito de usar TypeScript para início de conversa.
Quanto mais tipado for o seu programa, mais validação e ferramentas você terá, o que significa que vai encontrar menos bugs enquanto programa.
Ativar a flag [`noImplicitAny`](/tsconfig#noImplicitAny) vai gerar um erro em qualquer variável cujo tipo seja inferido implicitamente como `any`.

## `strictNullChecks`

Por padrão, valores como `null` e `undefined` são atribuíveis a qualquer outro tipo.
Isso pode facilitar a escrita de alguns códigos, mas esquecer de tratar `null` e `undefined` é a causa de incontáveis bugs no mundo; alguns consideram isso um [erro de um bilhão de dólares](https://www.youtube.com/watch?v=ybrQvs4x0Ps)!
A flag [`strictNullChecks`](/tsconfig#strictNullChecks) torna o tratamento de `null` e `undefined` mais explícito, e _nos poupa_ de nos preocupar se _esquecemos_ de tratar `null` e `undefined`.
