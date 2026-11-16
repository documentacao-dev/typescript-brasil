---
title: Tipos de objeto
layout: docs
permalink: /docs/handbook/2/objects.html
oneline: "Como o TypeScript descreve o formato dos objetos JavaScript."
ia-translate: true
---

No JavaScript, a forma fundamental de agrupar e passar dados é por meio de objetos.
No TypeScript, representamos isso com _tipos de objeto_.

Como já vimos, eles podem ser anônimos:

```ts twoslash
function greet(person: { name: string; age: number }) {
  //                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  return "Hello " + person.name;
}
```

ou podem receber um nome usando uma interface:

```ts twoslash
interface Person {
  //      ^^^^^^
  name: string;
  age: number;
}

function greet(person: Person) {
  return "Hello " + person.name;
}
```

ou um alias de tipo:

```ts twoslash
type Person = {
  // ^^^^^^
  name: string;
  age: number;
};

function greet(person: Person) {
  return "Hello " + person.name;
}
```

Nos três exemplos acima, escrevemos funções que recebem objetos com a propriedade `name` (que precisa ser `string`) e `age` (que precisa ser `number`).

## Referência rápida {#quick-reference}

Temos cheat sheets disponíveis para [`type` e `interface`](https://www.typescriptlang.org/cheatsheets), caso você queira dar uma olhada rápida na sintaxe do dia a dia.

## Modificadores de propriedade {#property-modifiers}

Cada propriedade de um tipo de objeto pode especificar algumas coisas: o tipo, se a propriedade é opcional e se ela pode ser escrita.

### Propriedades opcionais {#optional-properties}

Muitas vezes, vamos lidar com objetos que _podem_ ter uma propriedade definida.
Nesses casos, podemos marcar essas propriedades como _opcionais_ adicionando um ponto de interrogação (`?`) no fim do nome delas.

```ts twoslash
interface Shape {}
declare function getShape(): Shape;

// ---cut---
interface PaintOptions {
  shape: Shape;
  xPos?: number;
  //  ^
  yPos?: number;
  //  ^
}

function paintShape(opts: PaintOptions) {
  // ...
}

const shape = getShape();
paintShape({ shape });
paintShape({ shape, xPos: 100 });
paintShape({ shape, yPos: 100 });
paintShape({ shape, xPos: 100, yPos: 100 });
```

Neste exemplo, tanto `xPos` quanto `yPos` são consideradas opcionais.
Podemos escolher fornecer qualquer uma delas, então todas as chamadas de `paintShape` acima são válidas.
Tudo o que a opcionalidade realmente diz é que, se a propriedade _estiver_ definida, ela precisa ter um tipo específico.

Também podemos ler dessas propriedades, mas, quando fazemos isso com [`strictNullChecks`](/tsconfig#strictNullChecks) ativado, o TypeScript avisa que elas podem ser `undefined`.

```ts twoslash
interface Shape {}
declare function getShape(): Shape;

interface PaintOptions {
  shape: Shape;
  xPos?: number;
  yPos?: number;
}

// ---cut---
function paintShape(opts: PaintOptions) {
  let xPos = opts.xPos;
  //              ^?
  let yPos = opts.yPos;
  //              ^?
  // ...
}
```

No JavaScript, mesmo que a propriedade nunca tenha sido definida, ainda podemos acessá-la: ela simplesmente vai retornar o valor `undefined`.
Podemos tratar `undefined` de forma especial, verificando-o.

```ts twoslash
interface Shape {}
declare function getShape(): Shape;

interface PaintOptions {
  shape: Shape;
  xPos?: number;
  yPos?: number;
}

// ---cut---
function paintShape(opts: PaintOptions) {
  let xPos = opts.xPos === undefined ? 0 : opts.xPos;
  //  ^?
  let yPos = opts.yPos === undefined ? 0 : opts.yPos;
  //  ^?
  // ...
}
```

Repare que esse padrão de definir valores padrão para valores não informados é tão comum que o JavaScript tem sintaxe própria para isso.

```ts twoslash
interface Shape {}
declare function getShape(): Shape;

interface PaintOptions {
  shape: Shape;
  xPos?: number;
  yPos?: number;
}

// ---cut---
function paintShape({ shape, xPos = 0, yPos = 0 }: PaintOptions) {
  console.log("x coordinate at", xPos);
  //                             ^?
  console.log("y coordinate at", yPos);
  //                             ^?
  // ...
}
```

Aqui usamos [um padrão de desestruturação](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Destructuring_assignment) para o parâmetro de `paintShape` e fornecemos [valores padrão](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Destructuring_assignment#Default_values) para `xPos` e `yPos`.
Agora `xPos` e `yPos` estão certamente presentes no corpo de `paintShape`, mas são opcionais para quem chama `paintShape`.

> Repare que atualmente não há como colocar anotações de tipo dentro de padrões de desestruturação.
> Isso acontece porque a sintaxe a seguir já tem outro significado no JavaScript.
>
> ```ts twoslash
> // @noImplicitAny: false
> // @errors: 2552 2304
> interface Shape {}
> declare function render(x: unknown);
> // ---cut---
> function draw({ shape: Shape, xPos: number = 100 /*...*/ }) {
>   render(shape);
>   render(xPos);
> }
> ```
>
> Em um padrão de desestruturação de objeto, `shape: Shape` significa "pegue a propriedade `shape` e redefina-a localmente como uma variável chamada `Shape`".
> Da mesma forma, `xPos: number` cria uma variável chamada `number` cujo valor é baseado no `xPos` do parâmetro.

### Propriedades `readonly` {#readonly-properties}

Propriedades também podem ser marcadas como `readonly` para o TypeScript.
Embora isso não mude nenhum comportamento em tempo de execução, uma propriedade marcada como `readonly` não pode ser escrita durante a verificação de tipos.

```ts twoslash
// @errors: 2540
interface SomeType {
  readonly prop: string;
}

function doSomething(obj: SomeType) {
  // We can read from 'obj.prop'.
  console.log(`prop has the value '${obj.prop}'.`);

  // But we can't re-assign it.
  obj.prop = "hello";
}
```

Usar o modificador `readonly` não implica necessariamente que um valor é totalmente imutável, ou seja, que o conteúdo interno dele não pode ser alterado.
Ele significa apenas que a própria propriedade não pode ser reescrita.

```ts twoslash
// @errors: 2540
interface Home {
  readonly resident: { name: string; age: number };
}

function visitForBirthday(home: Home) {
  // We can read and update properties from 'home.resident'.
  console.log(`Happy birthday ${home.resident.name}!`);
  home.resident.age++;
}

function evict(home: Home) {
  // But we can't write to the 'resident' property itself on a 'Home'.
  home.resident = {
    name: "Victor the Evictor",
    age: 42,
  };
}
```

É importante alinhar as expectativas sobre o que `readonly` implica.
Ele é útil para sinalizar a intenção, durante o desenvolvimento, de como o TypeScript deve tratar o uso de um objeto.
O TypeScript não considera se as propriedades de dois tipos são `readonly` ao verificar se esses tipos são compatíveis, então propriedades `readonly` também podem mudar por meio de aliases.

```ts twoslash
interface Person {
  name: string;
  age: number;
}

interface ReadonlyPerson {
  readonly name: string;
  readonly age: number;
}

let writablePerson: Person = {
  name: "Person McPersonface",
  age: 42,
};

// works
let readonlyPerson: ReadonlyPerson = writablePerson;

console.log(readonlyPerson.age); // prints '42'
writablePerson.age++;
console.log(readonlyPerson.age); // prints '43'
```

Usando [modificadores de mapeamento](/docs/handbook/2/mapped-types.html#mapping-modifiers), você pode remover os atributos `readonly`.

### Assinaturas de índice {#index-signatures}

Às vezes você não conhece de antemão todos os nomes das propriedades de um tipo, mas conhece o formato dos valores.

Nesses casos, você pode usar uma assinatura de índice para descrever os tipos dos valores possíveis, por exemplo:

```ts twoslash
declare function getStringArray(): StringArray;
// ---cut---
interface StringArray {
  [index: number]: string;
}

const myArray: StringArray = getStringArray();
const secondItem = myArray[1];
//     ^?
```

Acima, temos uma interface `StringArray` que tem uma assinatura de índice.
Essa assinatura de índice afirma que, quando um `StringArray` é indexado com um `number`, ele retorna uma `string`.

Só alguns tipos são permitidos para propriedades de assinatura de índice: `string`, `number`, `symbol`, padrões de template string e uniões formadas apenas por esses tipos.

<details>
    <summary>É possível oferecer suporte a vários tipos de indexadores...</summary>
    <p>É possível oferecer suporte a vários tipos de indexadores. Repare que, ao usar os indexadores `number` e `string` juntos, o tipo retornado pelo indexador numérico precisa ser um subtipo do tipo retornado pelo indexador de string. Isso acontece porque, ao indexar com um <code>number</code>, o JavaScript converte esse valor para <code>string</code> antes de acessar o objeto. Isso significa que indexar com <code>100</code> (um <code>number</code>) é o mesmo que indexar com <code>"100"</code> (uma <code>string</code>), então os dois precisam ser consistentes.</p>

```ts twoslash
// @errors: 2413
// @strictPropertyInitialization: false
interface Animal {
  name: string;
}

interface Dog extends Animal {
  breed: string;
}

// Error: indexing with a numeric string might get you a completely separate type of Animal!
interface NotOkay {
  [x: number]: Animal;
  [x: string]: Dog;
}
```

</details>

Embora assinaturas de índice de string sejam uma forma poderosa de descrever o padrão de "dicionário", elas também obrigam que todas as propriedades correspondam ao tipo de retorno.
Isso acontece porque uma assinatura de índice de string declara que `obj.property` também está disponível como `obj["property"]`.
No exemplo a seguir, o tipo de `name` não corresponde ao tipo da assinatura de índice de string, e o verificador de tipos dá um erro:

```ts twoslash
// @errors: 2411
// @errors: 2411
interface NumberDictionary {
  [index: string]: number;

  length: number; // ok
  name: string;
}
```

No entanto, propriedades de tipos diferentes são aceitáveis se a assinatura de índice for uma união dos tipos das propriedades:

```ts twoslash
interface NumberOrStringDictionary {
  [index: string]: number | string;
  length: number; // ok, length is a number
  name: string; // ok, name is a string
}
```

Por fim, você pode tornar assinaturas de índice `readonly` para impedir atribuições aos índices delas:

```ts twoslash
declare function getReadOnlyStringArray(): ReadonlyStringArray;
// ---cut---
// @errors: 2542
interface ReadonlyStringArray {
  readonly [index: number]: string;
}

let myArray: ReadonlyStringArray = getReadOnlyStringArray();
myArray[2] = "Mallory";
```

Você não pode definir `myArray[2]` porque a assinatura de índice é `readonly`.

## Verificações de propriedades em excesso {#excess-property-checks}

Onde e como um objeto recebe um tipo pode fazer diferença no sistema de tipos.
Um dos exemplos principais disso é a verificação de propriedades em excesso (_excess property checking_), que valida o objeto com mais rigor quando ele é criado e atribuído a um tipo de objeto na criação.

```ts twoslash
// @errors: 2345 2739
interface SquareConfig {
  color?: string;
  width?: number;
}

function createSquare(config: SquareConfig): { color: string; area: number } {
  return {
    color: config.color || "red",
    area: config.width ? config.width * config.width : 20,
  };
}

let mySquare = createSquare({ colour: "red", width: 100 });
```

Repare que o argumento passado para `createSquare` está escrito _`colour`_ em vez de `color`.
Em JavaScript puro, esse tipo de coisa falha silenciosamente.

Dá para argumentar que esse programa está corretamente tipado, já que as propriedades `width` são compatíveis, não há propriedade `color` presente, e a propriedade extra `colour` é irrelevante.

No entanto, o TypeScript assume que provavelmente há um bug nesse código.
Literais de objeto recebem um tratamento especial e passam por _verificação de propriedades em excesso_ quando são atribuídos a outras variáveis ou passados como argumentos.
Se um literal de objeto tiver alguma propriedade que o "tipo alvo" não tem, você recebe um erro:

```ts twoslash
// @errors: 2345 2739
interface SquareConfig {
  color?: string;
  width?: number;
}

function createSquare(config: SquareConfig): { color: string; area: number } {
  return {
    color: config.color || "red",
    area: config.width ? config.width * config.width : 20,
  };
}
// ---cut---
let mySquare = createSquare({ colour: "red", width: 100 });
```

Contornar essas verificações é, na verdade, bem simples.
O método mais fácil é simplesmente usar uma asserção de tipo:

```ts twoslash
// @errors: 2345 2739
interface SquareConfig {
  color?: string;
  width?: number;
}

function createSquare(config: SquareConfig): { color: string; area: number } {
  return {
    color: config.color || "red",
    area: config.width ? config.width * config.width : 20,
  };
}
// ---cut---
let mySquare = createSquare({ width: 100, opacity: 0.5 } as SquareConfig);
```

No entanto, uma abordagem melhor pode ser adicionar uma assinatura de índice de string, se você tiver certeza de que o objeto pode ter algumas propriedades extras usadas de forma especial.
Se `SquareConfig` pode ter as propriedades `color` e `width` com os tipos acima, mas _também_ pode ter qualquer número de outras propriedades, podemos defini-la assim:

```ts twoslash
interface SquareConfig {
  color?: string;
  width?: number;
  [propName: string]: unknown;
}
```

Aqui estamos dizendo que `SquareConfig` pode ter qualquer número de propriedades e que, desde que elas não sejam `color` ou `width`, os tipos delas não importam.

Mais uma forma de contornar essas verificações, que pode parecer um pouco surpreendente, é atribuir o objeto a outra variável:
Como atribuir `squareOptions` não passa pela verificação de propriedades em excesso, o compilador não vai dar erro:

```ts twoslash
interface SquareConfig {
  color?: string;
  width?: number;
}

function createSquare(config: SquareConfig): { color: string; area: number } {
  return {
    color: config.color || "red",
    area: config.width ? config.width * config.width : 20,
  };
}
// ---cut---
let squareOptions = { colour: "red", width: 100 };
let mySquare = createSquare(squareOptions);
```

O contorno acima funciona enquanto existir uma propriedade em comum entre `squareOptions` e `SquareConfig`.
Neste exemplo, essa propriedade era `width`. No entanto, ele falha se a variável não tiver nenhuma propriedade de objeto em comum. Por exemplo:

```ts twoslash
// @errors: 2559
interface SquareConfig {
  color?: string;
  width?: number;
}

function createSquare(config: SquareConfig): { color: string; area: number } {
  return {
    color: config.color || "red",
    area: config.width ? config.width * config.width : 20,
  };
}
// ---cut---
let squareOptions = { colour: "red" };
let mySquare = createSquare(squareOptions);
```

Tenha em mente que, para um código simples como o acima, você provavelmente não deveria tentar "contornar" essas verificações.
Para literais de objeto mais complexos, que têm métodos e guardam estado, talvez seja preciso lembrar dessas técnicas, mas a maioria dos erros de propriedades em excesso são, na verdade, bugs.

Isso significa que, se você estiver tendo problemas com verificações de propriedades em excesso em algo como objetos de opções, talvez precise revisar algumas das suas declarações de tipo.
Nesse caso, se for aceitável passar para `createSquare` um objeto com uma propriedade `color` ou `colour`, você deve ajustar a definição de `SquareConfig` para refletir isso.

## Estendendo tipos {#extending-types}

É bastante comum ter tipos que são versões mais específicas de outros tipos.
Por exemplo, podemos ter um tipo `BasicAddress` que descreve os campos necessários para enviar cartas e encomendas nos EUA.

```ts twoslash
interface BasicAddress {
  name?: string;
  street: string;
  city: string;
  country: string;
  postalCode: string;
}
```

Em algumas situações, isso é suficiente, mas endereços muitas vezes têm um número de unidade associado quando o prédio do endereço tem várias unidades.
Podemos então descrever um `AddressWithUnit`.

<!-- prettier-ignore -->
```ts twoslash
interface AddressWithUnit {
  name?: string;
  unit: string;
//^^^^^^^^^^^^^
  street: string;
  city: string;
  country: string;
  postalCode: string;
}
```

Isso resolve, mas a desvantagem aqui é que tivemos que repetir todos os outros campos de `BasicAddress`, quando as mudanças eram puramente aditivas.
Em vez disso, podemos estender o tipo original `BasicAddress` e apenas adicionar os novos campos exclusivos de `AddressWithUnit`.

```ts twoslash
interface BasicAddress {
  name?: string;
  street: string;
  city: string;
  country: string;
  postalCode: string;
}

interface AddressWithUnit extends BasicAddress {
  unit: string;
}
```

A palavra-chave `extends` em uma `interface` permite copiar, na prática, os membros de outros tipos nomeados e adicionar quaisquer novos membros que quisermos.
Isso pode ajudar a reduzir a quantidade de código repetitivo de declaração de tipos que precisamos escrever, e a sinalizar que várias declarações diferentes da mesma propriedade podem estar relacionadas.
Por exemplo, `AddressWithUnit` não precisou repetir a propriedade `street` e, como `street` vem de `BasicAddress`, quem lê sabe que esses dois tipos estão relacionados de alguma forma.

`interface`s também podem estender vários tipos.

```ts twoslash
interface Colorful {
  color: string;
}

interface Circle {
  radius: number;
}

interface ColorfulCircle extends Colorful, Circle {}

const cc: ColorfulCircle = {
  color: "red",
  radius: 42,
};
```

## Tipos de interseção {#intersection-types}

As `interface`s nos permitiram construir novos tipos a partir de outros tipos, estendendo-os.
O TypeScript oferece outra construção, chamada _tipos de interseção_, que é usada principalmente para combinar tipos de objeto existentes.

Um tipo de interseção é definido usando o operador `&`.

```ts twoslash
interface Colorful {
  color: string;
}
interface Circle {
  radius: number;
}

type ColorfulCircle = Colorful & Circle;
```

Aqui, combinamos `Colorful` e `Circle` por interseção para produzir um novo tipo que tem todos os membros de `Colorful` _e_ de `Circle`.

```ts twoslash
// @errors: 2345
interface Colorful {
  color: string;
}
interface Circle {
  radius: number;
}
// ---cut---
function draw(circle: Colorful & Circle) {
  console.log(`Color was ${circle.color}`);
  console.log(`Radius was ${circle.radius}`);
}

// okay
draw({ color: "blue", radius: 42 });

// oops
draw({ color: "red", raidus: 42 });
```

## Extensão de interface versus interseção {#interface-extension-vs-intersection}

Acabamos de ver duas formas de combinar tipos que são parecidas, mas que têm diferenças sutis.
Com interfaces, podemos usar uma cláusula `extends` para estender outros tipos, e conseguimos fazer algo semelhante com interseções, dando um nome ao resultado com um alias de tipo.
A principal diferença entre as duas está em como os conflitos são tratados, e essa diferença costuma ser um dos principais motivos para escolher entre uma interface e um alias de tipo de interseção.

Se interfaces forem definidas com o mesmo nome, o TypeScript vai tentar uni-las se as propriedades forem compatíveis. Se as propriedades não forem compatíveis (ou seja, têm o mesmo nome, mas tipos diferentes), o TypeScript vai gerar um erro.

No caso dos tipos de interseção, propriedades com tipos diferentes são unidas automaticamente. Quando o tipo é usado depois, o TypeScript espera que a propriedade satisfaça os dois tipos ao mesmo tempo, o que pode produzir resultados inesperados.

Por exemplo, o código a seguir vai gerar um erro, porque as propriedades são incompatíveis:

```ts
interface Person {
  name: string;
}

interface Person {
  name: number;
}
```

Em contraste, o código a seguir compila, mas resulta em um tipo `never`:

```ts twoslash
interface Person1 {
  name: string;
}

interface Person2 {
  name: number;
}

type Staff = Person1 & Person2

declare const staffer: Staff;
staffer.name;
//       ^?
```
Neste caso, `Staff` exigiria que a propriedade `name` fosse ao mesmo tempo uma string e um number, o que faz com que a propriedade tenha o tipo `never`.

## Tipos de objeto genéricos {#generic-object-types}

Vamos imaginar um tipo `Box` que pode conter qualquer valor: `string`s, `number`s, `Giraffe`s, o que for.

```ts twoslash
interface Box {
  contents: any;
}
```

Agora, a propriedade `contents` está tipada como `any`, o que funciona, mas pode levar a acidentes mais adiante.

Poderíamos usar `unknown`, mas isso significaria que, nos casos em que já sabemos o tipo de `contents`, precisaríamos fazer verificações preventivas ou usar asserções de tipo, que são propensas a erros.

```ts twoslash
interface Box {
  contents: unknown;
}

let x: Box = {
  contents: "hello world",
};

// we could check 'x.contents'
if (typeof x.contents === "string") {
  console.log(x.contents.toLowerCase());
}

// or we could use a type assertion
console.log((x.contents as string).toLowerCase());
```

Uma abordagem segura em termos de tipos seria criar tipos `Box` diferentes para cada tipo de `contents`.

```ts twoslash
// @errors: 2322
interface NumberBox {
  contents: number;
}

interface StringBox {
  contents: string;
}

interface BooleanBox {
  contents: boolean;
}
```

Mas isso significa que teremos que criar funções diferentes, ou sobrecargas de funções, para operar sobre esses tipos.

```ts twoslash
interface NumberBox {
  contents: number;
}

interface StringBox {
  contents: string;
}

interface BooleanBox {
  contents: boolean;
}
// ---cut---
function setContents(box: StringBox, newContents: string): void;
function setContents(box: NumberBox, newContents: number): void;
function setContents(box: BooleanBox, newContents: boolean): void;
function setContents(box: { contents: any }, newContents: any) {
  box.contents = newContents;
}
```

Isso é muito código repetitivo. Além disso, podemos precisar, mais tarde, introduzir novos tipos e sobrecargas.
É frustrante, já que nossos tipos de caixa e as sobrecargas são, na prática, todos iguais.

Em vez disso, podemos criar um tipo `Box` _genérico_, que declara um _parâmetro de tipo_.

```ts twoslash
interface Box<Type> {
  contents: Type;
}
```

Você pode ler isso como “Uma `Box` de `Type` é algo cujo `contents` tem o tipo `Type`”.
Mais adiante, quando nos referirmos a `Box`, precisamos fornecer um _argumento de tipo_ no lugar de `Type`.

```ts twoslash
interface Box<Type> {
  contents: Type;
}
// ---cut---
let box: Box<string>;
```

Pense em `Box` como um modelo para um tipo real, em que `Type` é um marcador que será substituído por outro tipo.
Quando o TypeScript vê `Box<string>`, ele substitui todas as ocorrências de `Type` em `Box<Type>` por `string`, e acaba trabalhando com algo como `{ contents: string }`.
Em outras palavras, `Box<string>` e o nosso `StringBox` de antes funcionam de forma idêntica.

```ts twoslash
interface Box<Type> {
  contents: Type;
}
interface StringBox {
  contents: string;
}

let boxA: Box<string> = { contents: "hello" };
boxA.contents;
//   ^?

let boxB: StringBox = { contents: "world" };
boxB.contents;
//   ^?
```

`Box` é reutilizável porque `Type` pode ser substituído por qualquer coisa. Isso significa que, quando precisamos de uma caixa para um novo tipo, não precisamos declarar um novo tipo `Box` (embora pudéssemos, se quiséssemos).

```ts twoslash
interface Box<Type> {
  contents: Type;
}

interface Apple {
  // ....
}

// Same as '{ contents: Apple }'.
type AppleBox = Box<Apple>;
```

Isso também significa que podemos evitar sobrecargas por completo, usando [funções genéricas](/docs/handbook/2/functions.html#generic-functions).

```ts twoslash
interface Box<Type> {
  contents: Type;
}

// ---cut---
function setContents<Type>(box: Box<Type>, newContents: Type) {
  box.contents = newContents;
}
```

Vale notar que aliases de tipo também podem ser genéricos. Poderíamos ter definido nossa nova interface `Box<Type>`, que era:

```ts twoslash
interface Box<Type> {
  contents: Type;
}
```

usando um alias de tipo:

```ts twoslash
type Box<Type> = {
  contents: Type;
};
```

Como aliases de tipo, ao contrário das interfaces, podem descrever mais do que tipos de objeto, também podemos usá-los para escrever outros tipos auxiliares genéricos.

```ts twoslash
// @errors: 2575
type OrNull<Type> = Type | null;

type OneOrMany<Type> = Type | Type[];

type OneOrManyOrNull<Type> = OrNull<OneOrMany<Type>>;
//   ^?

type OneOrManyOrNullStrings = OneOrManyOrNull<string>;
//   ^?
```

Voltaremos aos aliases de tipo daqui a pouco.

### O tipo `Array` {#the-array-type}

Tipos de objeto genéricos costumam ser algum tipo de contêiner que funciona independentemente do tipo dos elementos que contém.
É ideal que estruturas de dados funcionem assim, para que possam ser reutilizadas com diferentes tipos de dados.

Acontece que temos trabalhado com um tipo assim o tempo todo neste manual: o tipo `Array`.
Sempre que escrevemos tipos como `number[]` ou `string[]`, isso é, na prática, uma forma abreviada de `Array<number>` e `Array<string>`.

```ts twoslash
function doSomething(value: Array<string>) {
  // ...
}

let myArray: string[] = ["hello", "world"];

// either of these work!
doSomething(myArray);
doSomething(new Array("hello", "world"));
```

Assim como o tipo `Box` acima, `Array` em si é um tipo genérico.

```ts twoslash
// @noLib: true
interface Number {}
interface String {}
interface Boolean {}
interface Symbol {}
// ---cut---
interface Array<Type> {
  /**
   * Gets or sets the length of the array.
   */
  length: number;

  /**
   * Removes the last element from an array and returns it.
   */
  pop(): Type | undefined;

  /**
   * Appends new elements to an array, and returns the new length of the array.
   */
  push(...items: Type[]): number;

  // ...
}
```

O JavaScript moderno também oferece outras estruturas de dados genéricas, como `Map<K, V>`, `Set<T>` e `Promise<T>`.
Tudo isso significa que, por causa do comportamento de `Map`, `Set` e `Promise`, elas podem funcionar com qualquer conjunto de tipos.

### O tipo `ReadonlyArray` {#the-readonlyarray-type}

`ReadonlyArray` é um tipo especial que descreve arrays que não devem ser alterados.

```ts twoslash
// @errors: 2339
function doStuff(values: ReadonlyArray<string>) {
  // We can read from 'values'...
  const copy = values.slice();
  console.log(`The first value is ${values[0]}`);

  // ...but we can't mutate 'values'.
  values.push("hello!");
}
```

Assim como o modificador `readonly` de propriedades, ele é principalmente uma ferramenta para sinalizar intenção.
Quando vemos uma função que retorna `ReadonlyArray`s, isso nos diz que não devemos alterar o conteúdo de forma alguma; e quando vemos uma função que consome `ReadonlyArray`s, isso nos diz que podemos passar qualquer array para essa função sem nos preocupar que ela altere o conteúdo.

Diferente de `Array`, não existe um construtor de `ReadonlyArray` que possamos usar.

```ts twoslash
// @errors: 2693
new ReadonlyArray("red", "green", "blue");
```

Em vez disso, podemos atribuir `Array`s comuns a `ReadonlyArray`s.

```ts twoslash
const roArray: ReadonlyArray<string> = ["red", "green", "blue"];
```

Assim como o TypeScript oferece uma sintaxe abreviada para `Array<Type>` com `Type[]`, ele também oferece uma sintaxe abreviada para `ReadonlyArray<Type>` com `readonly Type[]`.

```ts twoslash
// @errors: 2339
function doStuff(values: readonly string[]) {
  //                     ^^^^^^^^^^^^^^^^^
  // We can read from 'values'...
  const copy = values.slice();
  console.log(`The first value is ${values[0]}`);

  // ...but we can't mutate 'values'.
  values.push("hello!");
}
```

Uma última observação: diferente do modificador de propriedade `readonly`, a atribuição não é bidirecional entre `Array`s comuns e `ReadonlyArray`s.

```ts twoslash
// @errors: 4104
let x: readonly string[] = [];
let y: string[] = [];

x = y;
y = x;
```

### Tipos tupla {#tuple-types}

Um _tipo tupla_ é outro tipo de `Array` que sabe exatamente quantos elementos contém e exatamente quais tipos ele contém em posições específicas.

```ts twoslash
type StringNumberPair = [string, number];
//                      ^^^^^^^^^^^^^^^^
```

Aqui, `StringNumberPair` é um tipo tupla de `string` e `number`.
Como `ReadonlyArray`, ele não tem representação em tempo de execução, mas é significativo para o TypeScript.
Para o sistema de tipos, `StringNumberPair` descreve arrays cujo índice `0` contém uma `string` e cujo índice `1` contém um `number`.

```ts twoslash
function doSomething(pair: [string, number]) {
  const a = pair[0];
  //    ^?
  const b = pair[1];
  //    ^?
  // ...
}

doSomething(["hello", 42]);
```

Se tentarmos acessar um índice além do número de elementos, teremos um erro.

```ts twoslash
// @errors: 2493
function doSomething(pair: [string, number]) {
  // ...

  const c = pair[2];
}
```

Também podemos [desestruturar tuplas](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Destructuring_assignment#Array_destructuring) usando a desestruturação de arrays do JavaScript.

```ts twoslash
function doSomething(stringHash: [string, number]) {
  const [inputString, hash] = stringHash;

  console.log(inputString);
  //          ^?

  console.log(hash);
  //          ^?
}
```

> Tipos tupla são úteis em APIs muito baseadas em convenções, nas quais o significado de cada elemento é "óbvio".
> Isso nos dá flexibilidade para dar o nome que quisermos às variáveis na desestruturação.
> No exemplo acima, pudemos dar aos elementos `0` e `1` o nome que quisemos.
>
> No entanto, como nem todo usuário tem a mesma visão do que é óbvio, pode valer a pena reconsiderar se usar objetos com nomes de propriedade descritivos não seria melhor para a sua API.

Além dessas verificações de tamanho, tipos tupla simples como estes são equivalentes a versões de `Array`s que declaram propriedades para índices específicos e declaram `length` com um tipo literal numérico.

```ts twoslash
interface StringNumberPair {
  // specialized properties
  length: 2;
  0: string;
  1: number;

  // Other 'Array<string | number>' members...
  slice(start?: number, end?: number): Array<string | number>;
}
```

Outra coisa que pode interessar a você é que tuplas podem ter propriedades opcionais, escrevendo um ponto de interrogação (`?` depois do tipo do elemento).
Elementos opcionais de tupla só podem aparecer no fim, e também afetam o tipo de `length`.

```ts twoslash
type Either2dOr3d = [number, number, number?];

function setCoordinate(coord: Either2dOr3d) {
  const [x, y, z] = coord;
  //           ^?

  console.log(`Provided coordinates had ${coord.length} dimensions`);
  //                                            ^?
}
```

Tuplas também podem ter elementos rest, que precisam ser de um tipo array/tupla.

```ts twoslash
type StringNumberBooleans = [string, number, ...boolean[]];
type StringBooleansNumber = [string, ...boolean[], number];
type BooleansStringNumber = [...boolean[], string, number];
```

- `StringNumberBooleans` descreve uma tupla cujos dois primeiros elementos são, respectivamente, `string` e `number`, mas que pode ter qualquer número de `boolean`s em seguida.
- `StringBooleansNumber` descreve uma tupla cujo primeiro elemento é `string`, seguido de qualquer número de `boolean`s e terminando com um `number`.
- `BooleansStringNumber` descreve uma tupla cujos elementos iniciais são qualquer número de `boolean`s e que termina com uma `string` seguida de um `number`.

Uma tupla com elemento rest não tem um "length" fixo: ela tem apenas um conjunto de elementos conhecidos em posições diferentes.

```ts twoslash
type StringNumberBooleans = [string, number, ...boolean[]];
// ---cut---
const a: StringNumberBooleans = ["hello", 1];
const b: StringNumberBooleans = ["beautiful", 2, true];
const c: StringNumberBooleans = ["world", 3, true, false, true, false, true];
```

Por que elementos opcionais e rest podem ser úteis?
Bem, eles permitem que o TypeScript relacione tuplas com listas de parâmetros.
Tipos tupla podem ser usados em [parâmetros e argumentos rest](/docs/handbook/2/functions.html#rest-parameters-and-arguments), então o código a seguir:

```ts twoslash
function readButtonInput(...args: [string, number, ...boolean[]]) {
  const [name, version, ...input] = args;
  // ...
}
```

é basicamente equivalente a:

```ts twoslash
function readButtonInput(name: string, version: number, ...input: boolean[]) {
  // ...
}
```

Isso é útil quando você quer aceitar um número variável de argumentos com um parâmetro rest, precisa de um número mínimo de elementos, mas não quer introduzir variáveis intermediárias.

<!--
TODO do we need this example?

For example, imagine we need to write a function that adds up `number`s based on arguments that get passed in.

```ts twoslash
function sum(...args: number[]) {
    // ...
}
```

We might feel like it makes little sense to take any fewer than 2 elements, so we want to require callers to provide at least 2 arguments.
A first attempt might be

```ts twoslash
function foo(a: number, b: number, ...args: number[]) {
    args.unshift(a, b);

    let result = 0;
    for (const value of args) {
        result += value;
    }
    return result;
}
```

-->

### Tipos tupla `readonly` {#readonly-tuple-types}

Uma última observação sobre tipos tupla: eles têm variantes `readonly`, que podem ser especificadas colocando o modificador `readonly` na frente, assim como na sintaxe abreviada de arrays.

```ts twoslash
function doSomething(pair: readonly [string, number]) {
  //                       ^^^^^^^^^^^^^^^^^^^^^^^^^
  // ...
}
```

Como você pode imaginar, escrever em qualquer propriedade de uma tupla `readonly` não é permitido no TypeScript.

```ts twoslash
// @errors: 2540
function doSomething(pair: readonly [string, number]) {
  pair[0] = "hello!";
}
```

Tuplas costumam ser criadas e deixadas sem modificação na maior parte do código, então anotar tipos como tuplas `readonly` sempre que possível é um bom padrão.
Isso também é importante porque literais de array com asserções `const` são inferidos com tipos tupla `readonly`.

```ts twoslash
// @errors: 2345
let point = [3, 4] as const;

function distanceFromOrigin([x, y]: [number, number]) {
  return Math.sqrt(x ** 2 + y ** 2);
}

distanceFromOrigin(point);
```

Aqui, `distanceFromOrigin` nunca modifica os elementos dele, mas espera uma tupla mutável.
Como o tipo de `point` foi inferido como `readonly [3, 4]`, ele não será compatível com `[number, number]`, já que esse tipo não pode garantir que os elementos de `point` não serão modificados.

<!-- ## Other Kinds of Object Members

Most of the declarations in object types:

### Method Syntax

### Call Signatures

### Construct Signatures

### Index Signatures -->
