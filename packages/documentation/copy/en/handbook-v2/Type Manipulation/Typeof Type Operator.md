---
title: Operador de tipo typeof
layout: docs
permalink: /docs/handbook/2/typeof-types.html
oneline: "Usando o operador typeof em contextos de tipo."
ia-translate: true
---

## O operador de tipo `typeof` {#the-typeof-type-operator}

O JavaScript já tem um operador `typeof` que você pode usar em um contexto de _expressão_:

```ts twoslash
// Prints "string"
console.log(typeof "Hello world");
```

O TypeScript adiciona um operador `typeof` que você pode usar em um contexto de _tipo_ para se referir ao _tipo_ de uma variável ou propriedade:

```ts twoslash
let s = "hello";
let n: typeof s;
//  ^?
```

Isso não é muito útil para tipos básicos, mas combinado com outros operadores de tipo, você pode usar `typeof` para expressar muitos padrões de forma prática.
Como exemplo, vamos começar olhando para o tipo predefinido `ReturnType<T>`.
Ele recebe um _tipo de função_ e produz o tipo de retorno dela:

```ts twoslash
type Predicate = (x: unknown) => boolean;
type K = ReturnType<Predicate>;
//   ^?
```

Se tentarmos usar `ReturnType` em um nome de função, vemos um erro instrutivo:

```ts twoslash
// @errors: 2749
function f() {
  return { x: 10, y: 3 };
}
type P = ReturnType<f>;
```

Lembre-se de que _valores_ e _tipos_ não são a mesma coisa.
Para se referir ao _tipo_ que o _valor `f`_ tem, usamos `typeof`:

```ts twoslash
function f() {
  return { x: 10, y: 3 };
}
type P = ReturnType<typeof f>;
//   ^?
```

### Limitações {#limitations}

O TypeScript limita intencionalmente os tipos de expressão em que você pode usar `typeof`.

Mais especificamente, só é válido usar `typeof` em identificadores (ou seja, nomes de variáveis) ou nas propriedades deles.
Isso evita a armadilha confusa de escrever código que você acha que está sendo executado, mas não está:

```ts twoslash
// @errors: 1005
declare const msgbox: (prompt: string) => boolean;
// type msgbox = any;
// ---cut---
// Meant to use = ReturnType<typeof msgbox>
let shouldContinue: typeof msgbox("Are you sure you want to continue?");
```
