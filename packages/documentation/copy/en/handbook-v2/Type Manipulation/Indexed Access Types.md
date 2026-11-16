---
title: Tipos de acesso indexado
layout: docs
permalink: /docs/handbook/2/indexed-access-types.html
oneline: "Usando a sintaxe Type['a'] para acessar um subconjunto de um tipo."
ia-translate: true
---

Podemos usar um _tipo de acesso indexado_ para buscar uma propriedade específica em outro tipo:

```ts twoslash
type Person = { age: number; name: string; alive: boolean };
type Age = Person["age"];
//   ^?
```

O tipo usado no índice também é um tipo, então podemos usar uniões, `keyof` ou qualquer outro tipo:

```ts twoslash
type Person = { age: number; name: string; alive: boolean };
// ---cut---
type I1 = Person["age" | "name"];
//   ^?

type I2 = Person[keyof Person];
//   ^?

type AliveOrName = "alive" | "name";
type I3 = Person[AliveOrName];
//   ^?
```

Você verá um erro se tentar acessar uma propriedade que não existe:

```ts twoslash
// @errors: 2339
type Person = { age: number; name: string; alive: boolean };
// ---cut---
type I1 = Person["alve"];
```

Outro exemplo de indexação com um tipo qualquer é usar `number` para obter o tipo dos elementos de um array.
Podemos combinar isso com `typeof` para capturar, de forma prática, o tipo dos elementos de um literal de array:

```ts twoslash
const MyArray = [
  { name: "Alice", age: 15 },
  { name: "Bob", age: 23 },
  { name: "Eve", age: 38 },
];

type Person = typeof MyArray[number];
//   ^?
type Age = typeof MyArray[number]["age"];
//   ^?
// Or
type Age2 = Person["age"];
//   ^?
```

Você só pode usar tipos na indexação, ou seja, não é possível usar um `const` como referência de variável:

```ts twoslash
// @errors: 2538 2749
type Person = { age: number; name: string; alive: boolean };
// ---cut---
const key = "age";
type Age = Person[key];
```

No entanto, você pode usar um alias de tipo para fazer uma refatoração parecida:

```ts twoslash
type Person = { age: number; name: string; alive: boolean };
// ---cut---
type key = "age";
type Age = Person[key];
```
