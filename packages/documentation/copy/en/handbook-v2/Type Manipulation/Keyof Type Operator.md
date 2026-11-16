---
title: Operador de tipo keyof
layout: docs
permalink: /docs/handbook/2/keyof-types.html
oneline: "Usando o operador keyof em contextos de tipo."
ia-translate: true
---

## O operador de tipo `keyof` {#the-keyof-type-operator}

O operador `keyof` recebe um tipo de objeto e produz uma união de literais de string ou numéricos com as chaves dele.
O tipo `P` a seguir é o mesmo tipo que `type P = "x" | "y"`:

```ts twoslash
type Point = { x: number; y: number };
type P = keyof Point;
//   ^?
```

Se o tipo tiver uma assinatura de índice `string` ou `number`, o `keyof` retorna esses tipos:

```ts twoslash
type Arrayish = { [n: number]: unknown };
type A = keyof Arrayish;
//   ^?

type Mapish = { [k: string]: boolean };
type M = keyof Mapish;
//   ^?
```

Repare que, neste exemplo, `M` é `string | number`. Isso acontece porque as chaves de objetos em JavaScript são sempre convertidas para string, então `obj[0]` é sempre igual a `obj["0"]`.

Os tipos criados com `keyof` ficam especialmente úteis quando combinados com tipos mapeados, que veremos com mais detalhes adiante.
