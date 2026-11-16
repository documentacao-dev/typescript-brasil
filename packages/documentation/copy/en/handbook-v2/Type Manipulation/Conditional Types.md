---
title: Tipos condicionais
layout: docs
permalink: /docs/handbook/2/conditional-types.html
oneline: "Crie tipos que funcionam como instruções if no sistema de tipos."
ia-translate: true
---

No centro da maioria dos programas úteis, precisamos tomar decisões com base na entrada.
Programas JavaScript não são diferentes, mas, como os valores podem ser facilmente inspecionados, essas decisões também se baseiam nos tipos das entradas.
_Tipos condicionais_ ajudam a descrever a relação entre os tipos de entradas e saídas.

```ts twoslash
interface Animal {
  live(): void;
}
interface Dog extends Animal {
  woof(): void;
}

type Example1 = Dog extends Animal ? number : string;
//   ^?

type Example2 = RegExp extends Animal ? number : string;
//   ^?
```

Tipos condicionais têm uma forma parecida com expressões condicionais (`condição ? expressãoVerdadeira : expressãoFalsa`) do JavaScript:

```ts twoslash
type SomeType = any;
type OtherType = any;
type TrueType = any;
type FalseType = any;
type Stuff =
  // ---cut---
  SomeType extends OtherType ? TrueType : FalseType;
```

Quando o tipo à esquerda de `extends` é atribuível ao da direita, você recebe o tipo do primeiro ramo (o ramo "verdadeiro"); caso contrário, recebe o tipo do ramo final (o ramo "falso").

Pelos exemplos acima, tipos condicionais podem não parecer úteis de imediato: podemos verificar se `Dog extends Animal` e escolher `number` ou `string`!
Mas o poder dos tipos condicionais vem de usá-los com genéricos.

Por exemplo, vamos pegar a seguinte função `createLabel`:

```ts twoslash
interface IdLabel {
  id: number /* some fields */;
}
interface NameLabel {
  name: string /* other fields */;
}

function createLabel(id: number): IdLabel;
function createLabel(name: string): NameLabel;
function createLabel(nameOrId: string | number): IdLabel | NameLabel;
function createLabel(nameOrId: string | number): IdLabel | NameLabel {
  throw "unimplemented";
}
```

Essas sobrecargas de `createLabel` descrevem uma única função JavaScript que faz uma escolha com base nos tipos de suas entradas. Observe alguns pontos:

1. Se uma biblioteca precisa fazer o mesmo tipo de escolha repetidas vezes ao longo da sua API, isso fica trabalhoso.
2. Precisamos criar três sobrecargas: uma para cada caso em que _temos certeza_ do tipo (uma para `string` e outra para `number`), e uma para o caso mais geral (que recebe `string | number`). Para cada novo tipo que `createLabel` passa a tratar, o número de sobrecargas cresce exponencialmente.

Em vez disso, podemos codificar essa lógica em um tipo condicional:

```ts twoslash
interface IdLabel {
  id: number /* some fields */;
}
interface NameLabel {
  name: string /* other fields */;
}
// ---cut---
type NameOrId<T extends number | string> = T extends number
  ? IdLabel
  : NameLabel;
```

Podemos então usar esse tipo condicional para reduzir nossas sobrecargas a uma única função, sem sobrecargas.

```ts twoslash
interface IdLabel {
  id: number /* some fields */;
}
interface NameLabel {
  name: string /* other fields */;
}
type NameOrId<T extends number | string> = T extends number
  ? IdLabel
  : NameLabel;
// ---cut---
function createLabel<T extends number | string>(idOrName: T): NameOrId<T> {
  throw "unimplemented";
}

let a = createLabel("typescript");
//  ^?

let b = createLabel(2.8);
//  ^?

let c = createLabel(Math.random() ? "hello" : 42);
//  ^?
```

## Restrições em tipos condicionais {#conditional-type-constraints}

Muitas vezes, as verificações em um tipo condicional nos dão alguma informação nova.
Assim como o estreitamento com type guards pode nos dar um tipo mais específico, o ramo verdadeiro de um tipo condicional restringe ainda mais os genéricos pelo tipo com que verificamos.

Por exemplo, considere o seguinte:

```ts twoslash
// @errors: 2536
type MessageOf<T> = T["message"];
```

Neste exemplo, o TypeScript gera erro porque não se sabe que `T` tem uma propriedade chamada `message`.
Poderíamos restringir `T`, e o TypeScript deixaria de reclamar:

```ts twoslash
type MessageOf<T extends { message: unknown }> = T["message"];

interface Email {
  message: string;
}

type EmailMessageContents = MessageOf<Email>;
//   ^?
```

No entanto, e se quiséssemos que `MessageOf` aceitasse qualquer tipo, e usasse como padrão algo como `never` caso a propriedade `message` não esteja disponível?
Podemos fazer isso movendo a restrição para fora e introduzindo um tipo condicional:

```ts twoslash
type MessageOf<T> = T extends { message: unknown } ? T["message"] : never;

interface Email {
  message: string;
}

interface Dog {
  bark(): void;
}

type EmailMessageContents = MessageOf<Email>;
//   ^?

type DogMessageContents = MessageOf<Dog>;
//   ^?
```

No ramo verdadeiro, o TypeScript sabe que `T` _vai_ ter uma propriedade `message`.

Como outro exemplo, poderíamos também escrever um tipo chamado `Flatten` que achata tipos de array para os tipos de seus elementos, mas deixa os demais tipos como estão:

```ts twoslash
type Flatten<T> = T extends any[] ? T[number] : T;

// Extracts out the element type.
type Str = Flatten<string[]>;
//   ^?

// Leaves the type alone.
type Num = Flatten<number>;
//   ^?
```

Quando `Flatten` recebe um tipo de array, ele usa um acesso indexado com `number` para obter o tipo do elemento de `string[]`.
Caso contrário, simplesmente retorna o tipo que recebeu.

## Inferindo dentro de tipos condicionais {#inferring-within-conditional-types}

Acabamos de usar tipos condicionais para aplicar restrições e depois extrair tipos.
Essa operação acaba sendo tão comum que os tipos condicionais facilitam isso.

Tipos condicionais nos dão uma forma de inferir a partir dos tipos com que comparamos, no ramo verdadeiro, usando a palavra-chave `infer`.
Por exemplo, poderíamos ter inferido o tipo do elemento em `Flatten` em vez de buscá-lo "manualmente" com um tipo de acesso indexado:

```ts twoslash
type Flatten<Type> = Type extends Array<infer Item> ? Item : Type;
```

Aqui, usamos a palavra-chave `infer` para introduzir de forma declarativa uma nova variável de tipo genérica chamada `Item`, em vez de especificar como recuperar o tipo do elemento de `Type` no ramo verdadeiro.
Isso nos poupa de pensar em como percorrer e desmontar a estrutura dos tipos que nos interessam.

Podemos escrever alguns aliases de tipo auxiliares úteis usando a palavra-chave `infer`.
Por exemplo, em casos simples, podemos extrair o tipo de retorno de tipos de função:

```ts twoslash
type GetReturnType<Type> = Type extends (...args: never[]) => infer Return
  ? Return
  : never;

type Num = GetReturnType<() => number>;
//   ^?

type Str = GetReturnType<(x: string) => string>;
//   ^?

type Bools = GetReturnType<(a: boolean, b: boolean) => boolean[]>;
//   ^?
```

Ao inferir a partir de um tipo com várias assinaturas de chamada (como o tipo de uma função sobrecarregada), as inferências são feitas a partir da _última_ assinatura (que, presumivelmente, é o caso geral mais permissivo). Não é possível fazer resolução de sobrecarga com base em uma lista de tipos de argumentos.

```ts twoslash
declare function stringOrNum(x: string): number;
declare function stringOrNum(x: number): string;
declare function stringOrNum(x: string | number): string | number;

type T1 = ReturnType<typeof stringOrNum>;
//   ^?
```

## Tipos condicionais distributivos {#distributive-conditional-types}

Quando tipos condicionais atuam sobre um tipo genérico, eles se tornam _distributivos_ quando recebem um tipo união.
Por exemplo, considere o seguinte:

```ts twoslash
type ToArray<Type> = Type extends any ? Type[] : never;
```

Se passarmos um tipo união para `ToArray`, o tipo condicional será aplicado a cada membro da união.

```ts twoslash
type ToArray<Type> = Type extends any ? Type[] : never;

type StrArrOrNumArr = ToArray<string | number>;
//   ^?
```

O que acontece aqui é que `ToArray` distribui sobre:

```ts twoslash
type StrArrOrNumArr =
  // ---cut---
  string | number;
```

e mapeia cada tipo membro da união, resultando efetivamente em:

```ts twoslash
type ToArray<Type> = Type extends any ? Type[] : never;
type StrArrOrNumArr =
  // ---cut---
  ToArray<string> | ToArray<number>;
```

o que nos deixa com:

```ts twoslash
type StrArrOrNumArr =
  // ---cut---
  string[] | number[];
```

Normalmente, a distributividade é o comportamento desejado.
Para evitar esse comportamento, você pode colocar colchetes em cada lado da palavra-chave `extends`.

```ts twoslash
type ToArrayNonDist<Type> = [Type] extends [any] ? Type[] : never;

// 'ArrOfStrOrNum' is no longer a union.
type ArrOfStrOrNum = ToArrayNonDist<string | number>;
//   ^?
```
