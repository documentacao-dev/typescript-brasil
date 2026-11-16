---
title: Tipos mapeados
layout: docs
permalink: /docs/handbook/2/mapped-types.html
oneline: "Gerando tipos a partir da reutilização de um tipo existente."
ia-translate: true
---

Quando você não quer se repetir, às vezes um tipo precisa ser baseado em outro tipo.

Tipos mapeados são construídos sobre a sintaxe de assinaturas de índice, que servem para declarar os tipos de propriedades que não foram declaradas antecipadamente:

```ts twoslash
type Horse = {};
// ---cut---
type OnlyBoolsAndHorses = {
  [key: string]: boolean | Horse;
};

const conforms: OnlyBoolsAndHorses = {
  del: true,
  rodney: false,
};
```

Um tipo mapeado é um tipo genérico que usa uma união de `PropertyKey`s (geralmente criada [via `keyof`](/docs/handbook/2/indexed-access-types.html)) para percorrer as chaves e criar um tipo:

```ts twoslash
type OptionsFlags<Type> = {
  [Property in keyof Type]: boolean;
};
```

Neste exemplo, `OptionsFlags` pega todas as propriedades do tipo `Type` e muda os valores delas para booleano.

```ts twoslash
type OptionsFlags<Type> = {
  [Property in keyof Type]: boolean;
};
// ---cut---
type Features = {
  darkMode: () => void;
  newUserProfile: () => void;
};

type FeatureOptions = OptionsFlags<Features>;
//   ^?
```

## Modificadores de mapeamento {#mapping-modifiers}

Existem dois modificadores adicionais que podem ser aplicados durante o mapeamento: `readonly` e `?`, que afetam, respectivamente, a mutabilidade e a opcionalidade.

Você pode remover ou adicionar esses modificadores com o prefixo `-` ou `+`. Se você não colocar um prefixo, o `+` é assumido.

```ts twoslash
// Removes 'readonly' attributes from a type's properties
type CreateMutable<Type> = {
  -readonly [Property in keyof Type]: Type[Property];
};

type LockedAccount = {
  readonly id: string;
  readonly name: string;
};

type UnlockedAccount = CreateMutable<LockedAccount>;
//   ^?
```

```ts twoslash
// Removes 'optional' attributes from a type's properties
type Concrete<Type> = {
  [Property in keyof Type]-?: Type[Property];
};

type MaybeUser = {
  id: string;
  name?: string;
  age?: number;
};

type User = Concrete<MaybeUser>;
//   ^?
```

## Remapeamento de chaves via `as` {#key-remapping-via-as}

A partir do TypeScript 4.1, você pode remapear chaves em tipos mapeados com uma cláusula `as` dentro do tipo mapeado:

```ts
type MappedTypeWithNewProperties<Type> = {
    [Properties in keyof Type as NewKeyType]: Type[Properties]
}
```

Você pode usar recursos como [tipos de template literal](/docs/handbook/2/template-literal-types.html) para criar novos nomes de propriedade a partir dos anteriores:

```ts twoslash
type Getters<Type> = {
    [Property in keyof Type as `get${Capitalize<string & Property>}`]: () => Type[Property]
};

interface Person {
    name: string;
    age: number;
    location: string;
}

type LazyPerson = Getters<Person>;
//   ^?
```

Você pode filtrar chaves produzindo `never` por meio de um tipo condicional:

```ts twoslash
// Remove the 'kind' property
type RemoveKindField<Type> = {
    [Property in keyof Type as Exclude<Property, "kind">]: Type[Property]
};

interface Circle {
    kind: "circle";
    radius: number;
}

type KindlessCircle = RemoveKindField<Circle>;
//   ^?
```

Você pode mapear sobre uniões arbitrárias, não apenas uniões de `string | number | symbol`, mas uniões de qualquer tipo:

```ts twoslash
type EventConfig<Events extends { kind: string }> = {
    [E in Events as E["kind"]]: (event: E) => void;
}

type SquareEvent = { kind: "square", x: number, y: number };
type CircleEvent = { kind: "circle", radius: number };

type Config = EventConfig<SquareEvent | CircleEvent>
//   ^?
```

### Exploração adicional {#further-exploration}

Tipos mapeados funcionam bem com outros recursos desta seção de manipulação de tipos. Por exemplo, aqui está [um tipo mapeado que usa um tipo condicional](/docs/handbook/2/conditional-types.html), que retorna `true` ou `false` dependendo de o objeto ter a propriedade `pii` definida com o literal `true`:

```ts twoslash
type ExtractPII<Type> = {
  [Property in keyof Type]: Type[Property] extends { pii: true } ? true : false;
};

type DBFields = {
  id: { format: "incrementing" };
  name: { type: string; pii: true };
};

type ObjectsNeedingGDPRDeletion = ExtractPII<DBFields>;
//   ^?
```
