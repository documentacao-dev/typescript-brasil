---
title: Mais sobre Funções
layout: docs
permalink: /docs/handbook/2/functions.html
oneline: "Saiba como as funções funcionam no TypeScript."
ia-translate: true
---

Funções são o bloco básico de construção de qualquer aplicação, sejam elas funções locais, importadas de outro módulo ou métodos de uma classe.
Elas também são valores e, assim como outros valores, o TypeScript tem várias formas de descrever como funções podem ser chamadas.
Vamos aprender a escrever tipos que descrevem funções.

## Expressões de Tipo de Função {#function-type-expressions}

A forma mais simples de descrever uma função é com uma _expressão de tipo de função_.
Esses tipos são sintaticamente parecidos com arrow functions:

```ts twoslash
function greeter(fn: (a: string) => void) {
  fn("Hello, World");
}

function printToConsole(s: string) {
  console.log(s);
}

greeter(printToConsole);
```

A sintaxe `(a: string) => void` significa "uma função com um parâmetro, chamado `a`, do tipo `string`, que não tem valor de retorno".
Assim como nas declarações de função, se o tipo de um parâmetro não for especificado, ele é implicitamente `any`.

> Observe que o nome do parâmetro é **obrigatório**. O tipo de função `(string) => void` significa "uma função com um parâmetro chamado `string` do tipo `any`"!

Claro, podemos usar um type alias para dar nome a um tipo de função:

```ts twoslash
type GreetFunction = (a: string) => void;
function greeter(fn: GreetFunction) {
  // ...
}
```

## Assinaturas de Chamada {#call-signatures}

Em JavaScript, funções podem ter propriedades além de serem chamáveis.
No entanto, a sintaxe de expressão de tipo de função não permite declarar propriedades.
Se quisermos descrever algo chamável que também tem propriedades, podemos escrever uma _assinatura de chamada_ em um tipo objeto:

```ts twoslash
type DescribableFunction = {
  description: string;
  (someArg: number): boolean;
};
function doSomething(fn: DescribableFunction) {
  console.log(fn.description + " returned " + fn(6));
}

function myFunc(someArg: number) {
  return someArg > 3;
}
myFunc.description = "default description";

doSomething(myFunc);
```

Observe que a sintaxe é um pouco diferente da expressão de tipo de função: use `:` entre a lista de parâmetros e o tipo de retorno, em vez de `=>`.

## Assinaturas de Construtor {#construct-signatures}

Funções em JavaScript também podem ser invocadas com o operador `new`.
O TypeScript chama essas funções de _construtores_, porque normalmente criam um novo objeto.
Você pode escrever uma _assinatura de construtor_ adicionando a palavra-chave `new` na frente de uma assinatura de chamada:

```ts twoslash
type SomeObject = any;
// ---cut---
type SomeConstructor = {
  new (s: string): SomeObject;
};
function fn(ctor: SomeConstructor) {
  return new ctor("hello");
}
```

Alguns objetos, como o objeto `Date` do JavaScript, podem ser chamados com ou sem `new`.
Você pode combinar assinaturas de chamada e de construtor no mesmo tipo da forma que quiser:

```ts twoslash
interface CallOrConstruct {
  (n?: number): string;
  new (s: string): Date;
}

function fn(ctor: CallOrConstruct) {
  // Passing an argument of type `number` to `ctor` matches it against
  // the first definition in the `CallOrConstruct` interface.
  console.log(ctor(10));
              // ^?

  // Similarly, passing an argument of type `string` to `ctor` matches it
  // against the second definition in the `CallOrConstruct` interface.
  console.log(new ctor("10"));
                  // ^?
}

fn(Date);
```

## Funções Genéricas {#generic-functions}

É comum escrever uma função em que os tipos da entrada se relacionam com o tipo da saída, ou em que os tipos de duas entradas estão relacionados de alguma forma.
Vamos considerar por um momento uma função que retorna o primeiro elemento de um array:

```ts twoslash
function firstElement(arr: any[]) {
  return arr[0];
}
```

Essa função faz o trabalho, mas infelizmente tem o tipo de retorno `any`.
Seria melhor se a função retornasse o tipo do elemento do array.

No TypeScript, _genéricos_ são usados quando queremos descrever uma correspondência entre dois valores.
Fazemos isso declarando um _parâmetro de tipo_ na assinatura da função:

```ts twoslash
function firstElement<Type>(arr: Type[]): Type | undefined {
  return arr[0];
}
```

Ao adicionar um parâmetro de tipo `Type` a essa função e usá-lo em dois lugares, criamos um vínculo entre a entrada da função (o array) e a saída (o valor de retorno).
Agora, quando a chamamos, sai um tipo mais específico:

```ts twoslash
declare function firstElement<Type>(arr: Type[]): Type | undefined;
// ---cut---
// s is of type 'string'
const s = firstElement(["a", "b", "c"]);
// n is of type 'number'
const n = firstElement([1, 2, 3]);
// u is of type undefined
const u = firstElement([]);
```

### Inferência {#inference}

Observe que não precisamos especificar `Type` neste exemplo.
O tipo foi _inferido_ (escolhido automaticamente) pelo TypeScript.

Também podemos usar vários parâmetros de tipo.
Por exemplo, uma versão independente de `map` ficaria assim:

```ts twoslash
// prettier-ignore
function map<Input, Output>(arr: Input[], func: (arg: Input) => Output): Output[] {
  return arr.map(func);
}

// Parameter 'n' is of type 'string'
// 'parsed' is of type 'number[]'
const parsed = map(["1", "2", "3"], (n) => parseInt(n));
```

Observe que, neste exemplo, o TypeScript conseguiu inferir tanto o tipo do parâmetro de tipo `Input` (a partir do array de `string` fornecido) quanto o do parâmetro `Output`, com base no valor de retorno da expressão de função (`number`).

### Restrições {#constraints}

Já escrevemos algumas funções genéricas que funcionam com _qualquer_ tipo de valor.
Às vezes queremos relacionar dois valores, mas só podemos operar sobre um subconjunto específico de valores.
Nesse caso, podemos usar uma _restrição_ para limitar os tipos que um parâmetro de tipo aceita.

Vamos escrever uma função que retorna o maior entre dois valores.
Para isso, precisamos de uma propriedade `length` que seja um número.
Ao _restringir_ o parâmetro de tipo a esse formato, escrevemos uma cláusula `extends`:

```ts twoslash
// @errors: 2345 2322
function longest<Type extends { length: number }>(a: Type, b: Type) {
  if (a.length >= b.length) {
    return a;
  } else {
    return b;
  }
}

// longerArray is of type 'number[]'
const longerArray = longest([1, 2], [1, 2, 3]);
// longerString is of type 'alice' | 'bob'
const longerString = longest("alice", "bob");
// Error! Numbers don't have a 'length' property
const notOK = longest(10, 100);
```

Há algumas coisas interessantes a observar neste exemplo.
Deixamos o TypeScript _inferir_ o tipo de retorno de `longest`.
A inferência do tipo de retorno também funciona em funções genéricas.

Como restringimos `Type` a `{ length: number }`, podemos acessar a propriedade `.length` dos parâmetros `a` e `b`.
Sem a restrição de tipo, não conseguiríamos acessar essas propriedades, porque os valores poderiam ser de algum outro tipo sem a propriedade length.

Os tipos de `longerArray` e `longerString` foram inferidos com base nos argumentos.
Lembre-se: genéricos servem para relacionar dois ou mais valores de mesmo tipo!

Por fim, como esperávamos, a chamada `longest(10, 100)` é rejeitada porque o tipo `number` não tem a propriedade `.length`.

### Trabalhando com Valores Restritos {#working-with-constrained-values}

Aqui está um erro comum ao trabalhar com restrições de tipos genéricos:

```ts twoslash
// @errors: 2322
function minimumLength<Type extends { length: number }>(
  obj: Type,
  minimum: number
): Type {
  if (obj.length >= minimum) {
    return obj;
  } else {
    return { length: minimum };
  }
}
```

Pode parecer que essa função está correta: `Type` é restrito a `{ length: number }`, e a função retorna `Type` ou um valor que atende a essa restrição.
O problema é que a função promete retornar o _mesmo_ tipo de objeto que foi passado, e não apenas _algum_ objeto que atenda à restrição.
Se esse código fosse válido, você poderia escrever um código que certamente não funcionaria:

```ts twoslash
declare function minimumLength<Type extends { length: number }>(
  obj: Type,
  minimum: number
): Type;
// ---cut---
// 'arr' gets value { length: 6 }
const arr = minimumLength([1, 2, 3], 6);
// and crashes here because arrays have
// a 'slice' method, but not the returned object!
console.log(arr.slice(0));
```

### Especificando Argumentos de Tipo {#specifying-type-arguments}

O TypeScript normalmente consegue inferir os argumentos de tipo pretendidos em uma chamada genérica, mas nem sempre.
Por exemplo, suponha que você escreveu uma função para combinar dois arrays:

```ts twoslash
function combine<Type>(arr1: Type[], arr2: Type[]): Type[] {
  return arr1.concat(arr2);
}
```

Normalmente, seria um erro chamar essa função com arrays de tipos incompatíveis:

```ts twoslash
// @errors: 2322
declare function combine<Type>(arr1: Type[], arr2: Type[]): Type[];
// ---cut---
const arr = combine([1, 2, 3], ["hello"]);
```

Se você pretende fazer isso, no entanto, pode especificar `Type` manualmente:

```ts twoslash
declare function combine<Type>(arr1: Type[], arr2: Type[]): Type[];
// ---cut---
const arr = combine<string | number>([1, 2, 3], ["hello"]);
```

### Diretrizes para Escrever Boas Funções Genéricas {#guidelines-for-writing-good-generic-functions}

Escrever funções genéricas é divertido, e é fácil se empolgar com parâmetros de tipo.
Ter parâmetros de tipo demais, ou usar restrições onde elas não são necessárias, pode tornar a inferência menos eficiente e frustrar quem chama a sua função.

#### Empurre os Parâmetros de Tipo para Baixo {#push-type-parameters-down}

Aqui estão duas formas de escrever uma função que parecem semelhantes:

```ts twoslash
function firstElement1<Type>(arr: Type[]) {
  return arr[0];
}

function firstElement2<Type extends any[]>(arr: Type) {
  return arr[0];
}

// a: number (good)
const a = firstElement1([1, 2, 3]);
// b: any (bad)
const b = firstElement2([1, 2, 3]);
```

Essas funções podem parecer idênticas à primeira vista, mas `firstElement1` é uma forma muito melhor de escrever essa função.
O tipo de retorno inferido dela é `Type`, mas o de `firstElement2` é `any`, porque o TypeScript precisa resolver a expressão `arr[0]` usando o tipo da restrição, em vez de "esperar" para resolver o elemento durante a chamada.

> **Regra**: Sempre que possível, use o próprio parâmetro de tipo em vez de restringi-lo

#### Use Menos Parâmetros de Tipo {#use-fewer-type-parameters}

Aqui está outro par de funções parecidas:

```ts twoslash
function filter1<Type>(arr: Type[], func: (arg: Type) => boolean): Type[] {
  return arr.filter(func);
}

function filter2<Type, Func extends (arg: Type) => boolean>(
  arr: Type[],
  func: Func
): Type[] {
  return arr.filter(func);
}
```

Criamos um parâmetro de tipo `Func` que _não relaciona dois valores_.
Isso é sempre um sinal de alerta, porque significa que quem quiser especificar argumentos de tipo precisa informar manualmente um argumento extra sem motivo.
`Func` não faz nada além de tornar a função mais difícil de ler e de raciocinar sobre!

> **Regra**: Use sempre o menor número possível de parâmetros de tipo

#### Parâmetros de Tipo Devem Aparecer Duas Vezes {#type-parameters-should-appear-twice}

Às vezes esquecemos que uma função pode não precisar ser genérica:

```ts twoslash
function greet<Str extends string>(s: Str) {
  console.log("Hello, " + s);
}

greet("world");
```

Poderíamos ter escrito facilmente uma versão mais simples:

```ts twoslash
function greet(s: string) {
  console.log("Hello, " + s);
}
```

Lembre-se: parâmetros de tipo servem para _relacionar os tipos de múltiplos valores_.
Se um parâmetro de tipo aparece apenas uma vez na assinatura da função, ele não está relacionando nada.
Isso inclui o tipo de retorno inferido: se `Str` fizesse parte do tipo de retorno inferido de `greet`, ele estaria relacionando o argumento e o retorno, e por isso seria usado _duas_ vezes, mesmo aparecendo apenas uma vez no código escrito.

> **Regra**: Se um parâmetro de tipo aparece em apenas um lugar, reconsidere com bastante cuidado se você realmente precisa dele

## Parâmetros Opcionais {#optional-parameters}

Funções em JavaScript muitas vezes recebem um número variável de argumentos.
Por exemplo, o método `toFixed` de `number` recebe uma quantidade opcional de casas decimais:

```ts twoslash
function f(n: number) {
  console.log(n.toFixed()); // 0 arguments
  console.log(n.toFixed(3)); // 1 argument
}
```

Podemos modelar isso no TypeScript marcando o parâmetro como _opcional_ com `?`:

```ts twoslash
function f(x?: number) {
  // ...
}
f(); // OK
f(10); // OK
```

Embora o parâmetro seja especificado com o tipo `number`, o parâmetro `x` terá, na prática, o tipo `number | undefined`, porque parâmetros não informados em JavaScript recebem o valor `undefined`.

Você também pode fornecer um _valor padrão_ para o parâmetro:

```ts twoslash
function f(x = 10) {
  // ...
}
```

Agora, no corpo de `f`, `x` terá o tipo `number`, porque qualquer argumento `undefined` será substituído por `10`.
Observe que, quando um parâmetro é opcional, quem chama sempre pode passar `undefined`, já que isso apenas simula um argumento "ausente":

```ts twoslash
declare function f(x?: number): void;
// ---cut---
// All OK
f();
f(10);
f(undefined);
```

### Parâmetros Opcionais em Callbacks {#optional-parameters-in-callbacks}

Depois de aprender sobre parâmetros opcionais e expressões de tipo de função, é muito fácil cometer os seguintes erros ao escrever funções que invocam callbacks:

```ts twoslash
function myForEach(arr: any[], callback: (arg: any, index?: number) => void) {
  for (let i = 0; i < arr.length; i++) {
    callback(arr[i], i);
  }
}
```

O que as pessoas normalmente querem dizer ao escrever `index?` como parâmetro opcional é que ambas as chamadas abaixo sejam válidas:

```ts twoslash
// @errors: 2532 18048
declare function myForEach(
  arr: any[],
  callback: (arg: any, index?: number) => void
): void;
// ---cut---
myForEach([1, 2, 3], (a) => console.log(a));
myForEach([1, 2, 3], (a, i) => console.log(a, i));
```

O que isso _realmente_ significa é que _`callback` pode ser invocado com apenas um argumento_.
Em outras palavras, a definição da função diz que a implementação pode se parecer com isto:

```ts twoslash
// @errors: 2532 18048
function myForEach(arr: any[], callback: (arg: any, index?: number) => void) {
  for (let i = 0; i < arr.length; i++) {
    // I don't feel like providing the index today
    callback(arr[i]);
  }
}
```

Por consequência, o TypeScript vai aplicar esse significado e emitir erros que não são realmente possíveis:

<!-- prettier-ignore -->
```ts twoslash
// @errors: 2532 18048
declare function myForEach(
  arr: any[],
  callback: (arg: any, index?: number) => void
): void;
// ---cut---
myForEach([1, 2, 3], (a, i) => {
  console.log(i.toFixed());
});
```

Em JavaScript, se você chamar uma função com mais argumentos do que parâmetros, os argumentos extras são simplesmente ignorados.
O TypeScript se comporta da mesma forma.
Funções com menos parâmetros (dos mesmos tipos) sempre podem ocupar o lugar de funções com mais parâmetros.

> **Regra**: Ao escrever um tipo de função para um callback, _nunca_ escreva um parâmetro opcional, a menos que você pretenda _chamar_ a função sem passar aquele argumento

## Overloads de Função {#function-overloads}

Algumas funções em JavaScript podem ser chamadas com diferentes quantidades e tipos de argumentos.
Por exemplo, você pode escrever uma função para produzir um `Date` que aceita um timestamp (um argumento) ou uma especificação de mês/dia/ano (três argumentos).

No TypeScript, podemos especificar uma função que pode ser chamada de diferentes formas escrevendo _assinaturas de overload_.
Para isso, escreva algumas assinaturas de função (normalmente duas ou mais), seguidas do corpo da função:

```ts twoslash
// @errors: 2575
function makeDate(timestamp: number): Date;
function makeDate(m: number, d: number, y: number): Date;
function makeDate(mOrTimestamp: number, d?: number, y?: number): Date {
  if (d !== undefined && y !== undefined) {
    return new Date(y, mOrTimestamp, d);
  } else {
    return new Date(mOrTimestamp);
  }
}
const d1 = makeDate(12345678);
const d2 = makeDate(5, 5, 5);
const d3 = makeDate(1, 3);
```

Neste exemplo, escrevemos dois overloads: um que aceita um argumento e outro que aceita três.
Essas duas primeiras assinaturas são chamadas de _assinaturas de overload_.

Em seguida, escrevemos uma implementação da função com uma assinatura compatível.
Funções têm uma assinatura de _implementação_, mas essa assinatura não pode ser chamada diretamente.
Mesmo que tenhamos escrito uma função com dois parâmetros opcionais depois do obrigatório, ela não pode ser chamada com dois parâmetros!

### Assinaturas de Overload e a Assinatura de Implementação {#overload-signatures-and-the-implementation-signature}

Esta é uma fonte comum de confusão.
Muitas vezes, as pessoas escrevem código assim e não entendem por que há um erro:

```ts twoslash
// @errors: 2554
function fn(x: string): void;
function fn() {
  // ...
}
// Expected to be able to call with zero arguments
fn();
```

De novo: a assinatura usada para escrever o corpo da função não pode ser "vista" de fora.

> A assinatura da _implementação_ não é visível de fora.
> Ao escrever uma função com overloads, você deve sempre ter _duas_ ou mais assinaturas acima da implementação da função.

A assinatura de implementação também precisa ser _compatível_ com as assinaturas de overload.
Por exemplo, estas funções têm erros porque a assinatura de implementação não corresponde aos overloads de forma correta:

```ts twoslash
// @errors: 2394
function fn(x: boolean): void;
// Argument type isn't right
function fn(x: string): void;
function fn(x: boolean) {}
```

```ts twoslash
// @errors: 2394
function fn(x: string): string;
// Return type isn't right
function fn(x: number): boolean;
function fn(x: string | number) {
  return "oops";
}
```

### Escrevendo Bons Overloads {#writing-good-overloads}

Assim como os genéricos, há algumas diretrizes que você deve seguir ao usar overloads de função.
Seguir esses princípios vai tornar sua função mais fácil de chamar, de entender e de implementar.

Vamos considerar uma função que retorna o tamanho de uma string ou de um array:

```ts twoslash
function len(s: string): number;
function len(arr: any[]): number;
function len(x: any) {
  return x.length;
}
```

Esta função está correta: podemos invocá-la com strings ou com arrays.
No entanto, não podemos invocá-la com um valor que pode ser uma string _ou_ um array, porque o TypeScript só consegue resolver uma chamada de função para um único overload:

```ts twoslash
// @errors: 2769
declare function len(s: string): number;
declare function len(arr: any[]): number;
// ---cut---
len(""); // OK
len([0]); // OK
len(Math.random() > 0.5 ? "hello" : [0]);
```

Como os dois overloads têm a mesma quantidade de argumentos e o mesmo tipo de retorno, podemos escrever uma versão sem overloads da função:

```ts twoslash
function len(x: any[] | string) {
  return x.length;
}
```

Isso é muito melhor!
Quem chama pode invocá-la com qualquer um dos dois tipos de valor e, como bônus, não precisamos descobrir uma assinatura de implementação correta.

> Sempre prefira parâmetros com tipos união em vez de overloads, quando possível

## Declarando `this` em uma Função {#declaring-this-in-a-function}

O TypeScript vai inferir qual deve ser o `this` em uma função por meio de análise de fluxo de código, por exemplo no caso a seguir:

```ts twoslash
const user = {
  id: 123,

  admin: false,
  becomeAdmin: function () {
    this.admin = true;
  },
};
```

O TypeScript entende que a função `user.becomeAdmin` tem um `this` correspondente, que é o objeto externo `user`. `this`, _ah, sim_, pode ser suficiente para muitos casos, mas há muitas situações em que você precisa de mais controle sobre qual objeto o `this` representa. A especificação do JavaScript diz que você não pode ter um parâmetro chamado `this`, então o TypeScript usa essa posição de sintaxe para permitir que você declare o tipo de `this` no corpo da função.

```ts twoslash
interface User {
  id: number;
  admin: boolean;
}
declare const getDB: () => DB;
// ---cut---
interface DB {
  filterUsers(filter: (this: User) => boolean): User[];
}

const db = getDB();
const admins = db.filterUsers(function (this: User) {
  return this.admin;
});
```

Esse padrão é comum em APIs no estilo callback, em que outro objeto normalmente controla quando a sua função é chamada. Observe que você precisa usar `function` e não arrow functions para obter esse comportamento:

```ts twoslash
// @errors: 7041 7017
interface User {
  id: number;
  admin: boolean;
}
declare const getDB: () => DB;
// ---cut---
interface DB {
  filterUsers(filter: (this: User) => boolean): User[];
}

const db = getDB();
const admins = db.filterUsers(() => this.admin);
```

## Outros Tipos que Você Deve Conhecer {#other-types-to-know-about}

Há alguns tipos adicionais que você vai querer reconhecer, pois aparecem com frequência ao trabalhar com tipos de função.
Como todos os tipos, você pode usá-los em qualquer lugar, mas estes são especialmente relevantes no contexto de funções.

### `void`

`void` representa o valor de retorno de funções que não retornam um valor.
É o tipo inferido sempre que uma função não tem nenhum `return` ou não retorna nenhum valor explícito nessas instruções:

```ts twoslash
// The inferred return type is void
function noop() {
  return;
}
```

Em JavaScript, uma função que não retorna nenhum valor vai retornar implicitamente o valor `undefined`.
No entanto, `void` e `undefined` não são a mesma coisa no TypeScript.
Há mais detalhes no final deste capítulo.

> `void` não é o mesmo que `undefined`.

### `object`

O tipo especial `object` se refere a qualquer valor que não seja primitivo (`string`, `number`, `bigint`, `boolean`, `symbol`, `null` ou `undefined`).
Ele é diferente do _tipo objeto vazio_ `{ }` e também é diferente do tipo global `Object`.
É muito provável que você nunca vá usar `Object`.

> `object` não é `Object`. **Sempre** use `object`!

Observe que, em JavaScript, valores de função são objetos: têm propriedades, têm `Object.prototype` na cadeia de protótipos, são `instanceof Object`, você pode chamar `Object.keys` neles, e assim por diante.
Por esse motivo, tipos de função são considerados `object`s no TypeScript.

### `unknown`

O tipo `unknown` representa _qualquer_ valor.
É semelhante ao tipo `any`, mas é mais seguro, porque não é válido fazer nada com um valor `unknown`:

```ts twoslash
// @errors: 2571 18046
function f1(a: any) {
  a.b(); // OK
}
function f2(a: unknown) {
  a.b();
}
```

Isso é útil ao descrever tipos de função porque você pode descrever funções que aceitam qualquer valor sem ter valores `any` no corpo da função.

Por outro lado, você pode descrever uma função que retorna um valor de tipo unknown:

```ts twoslash
declare const someRandomString: string;
// ---cut---
function safeParse(s: string): unknown {
  return JSON.parse(s);
}

// Need to be careful with 'obj'!
const obj = safeParse(someRandomString);
```

### `never`

Algumas funções _nunca_ retornam um valor:

```ts twoslash
function fail(msg: string): never {
  throw new Error(msg);
}
```

O tipo `never` representa valores que _nunca_ são observados.
Em um tipo de retorno, isso significa que a função lança uma exceção ou encerra a execução do programa.

`never` também aparece quando o TypeScript determina que não sobrou nada em uma união.

```ts twoslash
function fn(x: string | number) {
  if (typeof x === "string") {
    // do something
  } else if (typeof x === "number") {
    // do something else
  } else {
    x; // has type 'never'!
  }
}
```

### `Function`

O tipo global `Function` descreve propriedades como `bind`, `call`, `apply` e outras presentes em todos os valores de função em JavaScript.
Ele também tem a propriedade especial de que valores do tipo `Function` podem sempre ser chamados; essas chamadas retornam `any`:

```ts twoslash
function doSomething(f: Function) {
  return f(1, 2, 3);
}
```

Esta é uma _chamada de função não tipada_ e, em geral, é melhor evitá-la por causa do tipo de retorno `any`, que não é seguro.

Se você precisa aceitar uma função arbitrária, mas não pretende chamá-la, o tipo `() => void` costuma ser mais seguro.

## Parâmetros Rest e Argumentos {#rest-parameters-and-arguments}

<blockquote class='bg-reading'>
   <p>Leitura complementar:<br />
   <a href='https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/rest_parameters'>Parâmetros rest</a><br/>
   <a href='https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax'>Sintaxe de spread</a><br/>
   </p>
</blockquote>

### Parâmetros Rest {#rest-parameters}

Além de usar parâmetros opcionais ou overloads para criar funções que aceitam uma variedade de quantidades fixas de argumentos, também podemos definir funções que recebem um número _ilimitado_ de argumentos usando _parâmetros rest_.

Um parâmetro rest aparece depois de todos os outros parâmetros e usa a sintaxe `...`:

```ts twoslash
function multiply(n: number, ...m: number[]) {
  return m.map((x) => n * x);
}
// 'a' gets value [10, 20, 30, 40]
const a = multiply(10, 1, 2, 3, 4);
```

No TypeScript, a anotação de tipo desses parâmetros é implicitamente `any[]` em vez de `any`, e qualquer anotação de tipo informada deve ter a forma `Array<T>` ou `T[]`, ou ser um tipo tupla (sobre o qual vamos aprender mais adiante).

### Argumentos Rest {#rest-arguments}

Por outro lado, podemos _fornecer_ um número variável de argumentos a partir de um objeto iterável (por exemplo, um array) usando a sintaxe de spread.
Por exemplo, o método `push` de arrays aceita qualquer número de argumentos:

```ts twoslash
const arr1 = [1, 2, 3];
const arr2 = [4, 5, 6];
arr1.push(...arr2);
```

Observe que, em geral, o TypeScript não assume que arrays são imutáveis.
Isso pode levar a um comportamento surpreendente:

```ts twoslash
// @errors: 2556
// Inferred type is number[] -- "an array with zero or more numbers",
// not specifically two numbers
const args = [8, 5];
const angle = Math.atan2(...args);
```

A melhor correção para essa situação depende um pouco do seu código, mas, em geral, um contexto `const` é a solução mais direta:

```ts twoslash
// Inferred as 2-length tuple
const args = [8, 5] as const;
// OK
const angle = Math.atan2(...args);
```

Usar argumentos rest pode exigir ativar [`downlevelIteration`](/tsconfig#downlevelIteration) ao compilar para runtimes mais antigos.

<!-- TODO link to downlevel iteration -->

## Desestruturação de Parâmetros {#parameter-destructuring}

<blockquote class='bg-reading'>
   <p>Leitura complementar:<br />
   <a href='https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Destructuring_assignment'>Atribuição via desestruturação</a><br/>
   </p>
</blockquote>

Você pode usar a desestruturação de parâmetros para desempacotar de forma conveniente objetos fornecidos como argumento em uma ou mais variáveis locais no corpo da função.
Em JavaScript, fica assim:

```js
function sum({ a, b, c }) {
  console.log(a + b + c);
}
sum({ a: 10, b: 3, c: 9 });
```

A anotação de tipo do objeto vai depois da sintaxe de desestruturação:

```ts twoslash
function sum({ a, b, c }: { a: number; b: number; c: number }) {
  console.log(a + b + c);
}
```

Isso pode parecer um pouco verboso, mas você também pode usar um tipo nomeado aqui:

```ts twoslash
// Same as prior example
type ABC = { a: number; b: number; c: number };
function sum({ a, b, c }: ABC) {
  console.log(a + b + c);
}
```

## Atribuição de Funções {#assignability-of-functions}

### Tipo de retorno `void` {#return-type-void}

O tipo de retorno `void` para funções pode produzir alguns comportamentos incomuns, mas esperados.

A tipagem contextual com tipo de retorno `void` **não** obriga as funções a **não** retornarem nada. Dito de outra forma: um tipo de função contextual com retorno `void` (`type voidFunc = () => void`), quando implementado, pode retornar _qualquer outro valor_, mas esse valor será ignorado.

Assim, as seguintes implementações do tipo `() => void` são válidas:

```ts twoslash
type voidFunc = () => void;

const f1: voidFunc = () => {
  return true;
};

const f2: voidFunc = () => true;

const f3: voidFunc = function () {
  return true;
};
```

E quando o valor de retorno de uma dessas funções é atribuído a outra variável, ele mantém o tipo `void`:

```ts twoslash
type voidFunc = () => void;

const f1: voidFunc = () => {
  return true;
};

const f2: voidFunc = () => true;

const f3: voidFunc = function () {
  return true;
};
// ---cut---
const v1 = f1();

const v2 = f2();

const v3 = f3();
```

Esse comportamento existe para que o código a seguir seja válido, mesmo que `Array.prototype.push` retorne um número e o método `Array.prototype.forEach` espere uma função com tipo de retorno `void`.

```ts twoslash
const src = [1, 2, 3];
const dst = [0];

src.forEach((el) => dst.push(el));
```

Há mais um caso especial a conhecer: quando uma definição de função literal tem tipo de retorno `void`, essa função **não** deve retornar nada.

```ts twoslash
function f2(): void {
  // @ts-expect-error
  return true;
}

const f3 = function (): void {
  // @ts-expect-error
  return true;
};
```

Para saber mais sobre `void`, consulte estas outras entradas da documentação:

- [FAQ - "Por que funções que retornam não-void são atribuíveis a funções que retornam void?"](https://github.com/Microsoft/TypeScript/wiki/FAQ#why-are-functions-returning-non-void-assignable-to-function-returning-void)
