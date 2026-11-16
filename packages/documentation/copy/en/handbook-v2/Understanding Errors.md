---
title: Entendendo erros
layout: docs
permalink: /docs/handbook/2/understanding-errors.html
oneline: "Como ler os erros do TypeScript."
ia-translate: true
---

# Entendendo erros {#understanding-errors}

Sempre que o TypeScript encontra um erro, ele tenta explicar o que deu errado com o máximo de detalhes possível.
Como o sistema de tipos dele é estrutural, isso muitas vezes significa fornecer descrições um tanto longas sobre onde o problema foi encontrado.

## Terminologia {#terminology}

Há alguma terminologia que você vai ver com frequência nas mensagens de erro, e vale a pena entendê-la.

#### _atribuível a_ {#_assignable-to_}

O TypeScript considera que um tipo é _atribuível a_ outro tipo quando um deles é um substituto aceitável para o outro.
Em outras palavras, um `Cat` é _atribuível a_ um `Animal` porque um `Cat` é um substituto aceitável para um `Animal`.

Como o nome sugere, essa relação é usada para verificar a validade de uma atribuição `t = s;` examinando os tipos de `t` e `s`.
Ela também é usada para verificar a maioria dos outros pontos em que dois tipos interagem.
Por exemplo, ao chamar uma função, o tipo de cada argumento precisa ser _atribuível ao_ tipo declarado do parâmetro.

Informalmente, se você vir `T is not assignable to S`, pode entender isso como o TypeScript dizendo "_`T` e `S` não são compatíveis_".
No entanto, repare que essa é uma relação _direcional_: `S` ser atribuível a `T` não implica que `T` seja atribuível a `S`.

## Exemplos {#examples}

Vamos ver alguns exemplos de mensagens de erro e entender o que está acontecendo.

### Detalhamento de erros {#error-elaborations}

Cada erro começa com uma mensagem principal, às vezes seguida de submensagens.
Você pode pensar em cada submensagem como uma resposta à pergunta "por quê?" sobre a mensagem acima dela.
Vamos ver alguns exemplos para entender como isso funciona na prática.

Aqui está um exemplo que gera uma mensagem de erro maior que o próprio exemplo:

```ts twoslash
// @errors: 2322
let a: { m: number[] };
let b = { m: [""] };
a = b;
```

O TypeScript encontrou um erro ao verificar a última linha.
A lógica para emitir o erro decorre da lógica que ele usa para determinar se a atribuição está correta:

1. O tipo de `b` é atribuível ao de `a`? Não. Por quê?
2. Porque o tipo da propriedade `m` é incompatível. Por quê?
3. Porque a propriedade `m` de `b` (`string[]`) não é atribuível à propriedade `m` de `a` (`number[]`). Por quê?
4. Porque o tipo dos elementos de um array (`string`) não é atribuível ao do outro (`number`)

### Propriedades extras {#extra-properties}

```ts twoslash
// @errors: 2322
type A = { m: number };
const a: A = { m: 10, n: "" };
```

### Atribuições de união {#union-assignments}

```ts twoslash
// @errors: 2322
type Thing = "none" | { name: string };

const a: Thing = { name: 0 };
```
