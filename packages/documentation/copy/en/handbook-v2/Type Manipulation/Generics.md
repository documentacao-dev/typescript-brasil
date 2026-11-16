---
title: Genéricos
layout: docs
permalink: /docs/handbook/2/generics.html
oneline: Tipos que recebem parâmetros
ia-translate: true
---

Uma grande parte da engenharia de software é construir componentes que não só têm APIs bem definidas e consistentes, mas também são reutilizáveis.
Componentes capazes de trabalhar com os dados de hoje e com os dados de amanhã vão lhe dar as capacidades mais flexíveis para construir grandes sistemas de software.

Em linguagens como C# e Java, uma das principais ferramentas para criar componentes reutilizáveis são os _genéricos_, ou seja, a capacidade de criar um componente que funciona com uma variedade de tipos, em vez de um único tipo.
Isso permite que quem usa esses componentes utilize os próprios tipos.

## O "Hello World" dos Genéricos {#hello-world-of-generics}

Para começar, vamos fazer o "hello world" dos genéricos: a função identidade.
A função identidade é uma função que devolve de volta qualquer coisa que for passada para ela.
Você pode pensar nela de forma parecida com o comando `echo`.

Sem genéricos, teríamos que dar à função identidade um tipo específico:

```ts twoslash
function identity(arg: number): number {
  return arg;
}
```

Ou poderíamos descrever a função identidade usando o tipo `any`:

```ts twoslash
function identity(arg: any): any {
  return arg;
}
```

Embora o uso de `any` seja certamente genérico, no sentido de que faz a função aceitar todos os tipos possíveis para `arg`, na prática perdemos a informação sobre qual era esse tipo quando a função retorna.
Se passarmos um número, a única informação que temos é que qualquer tipo poderia ser retornado.

Em vez disso, precisamos de uma forma de capturar o tipo do argumento de modo que também possamos usá-lo para indicar o que está sendo retornado.
Aqui, vamos usar uma _variável de tipo_, uma variável especial que trabalha com tipos em vez de valores.

```ts twoslash
function identity<Type>(arg: Type): Type {
  return arg;
}
```

Agora adicionamos uma variável de tipo `Type` à função identidade.
Esse `Type` nos permite capturar o tipo que o usuário fornece (por exemplo, `number`), para que possamos usar essa informação depois.
Aqui, usamos `Type` novamente como tipo de retorno. Ao analisar, podemos ver que o mesmo tipo é usado para o argumento e para o tipo de retorno.
Isso nos permite transportar a informação de tipo de um lado da função até o outro.

Dizemos que esta versão da função `identity` é genérica, pois funciona com uma faixa de tipos.
Diferentemente do uso de `any`, ela também é tão precisa (ou seja, não perde nenhuma informação) quanto a primeira função `identity`, que usava números para o argumento e para o retorno.

Depois de escrever a função identidade genérica, podemos chamá-la de duas formas.
A primeira é passar todos os argumentos, incluindo o argumento de tipo, para a função:

```ts twoslash
function identity<Type>(arg: Type): Type {
  return arg;
}
// ---cut---
let output = identity<string>("myString");
//       ^?
```

Aqui definimos explicitamente `Type` como `string` como um dos argumentos da chamada da função, indicado pelo uso de `<>` em volta dos argumentos, em vez de `()`.

A segunda forma também é talvez a mais comum. Aqui usamos _inferência de argumento de tipo_, ou seja, queremos que o compilador defina o valor de `Type` para nós automaticamente, com base no tipo do argumento que passamos:

```ts twoslash
function identity<Type>(arg: Type): Type {
  return arg;
}
// ---cut---
let output = identity("myString");
//       ^?
```

Observe que não precisamos passar o tipo explicitamente entre os colchetes angulares (`<>`); o compilador apenas olhou para o valor `"myString"` e definiu `Type` como o tipo dele.
Embora a inferência de argumento de tipo possa ser uma ferramenta útil para deixar o código mais curto e legível, talvez seja necessário passar explicitamente os argumentos de tipo, como fizemos no exemplo anterior, quando o compilador não consegue inferir o tipo, o que pode acontecer em exemplos mais complexos.

## Trabalhando com Variáveis de Tipo Genéricas {#working-with-generic-type-variables}

Ao começar a usar genéricos, você vai perceber que, ao criar funções genéricas como `identity`, o compilador vai exigir que você use os parâmetros tipados genericamente corretamente no corpo da função.
Ou seja, que você de fato trate esses parâmetros como se pudessem ser qualquer tipo.

Vamos pegar a nossa função `identity` de antes:

```ts twoslash
function identity<Type>(arg: Type): Type {
  return arg;
}
```

E se quisermos também registrar no console o tamanho do argumento `arg` a cada chamada?
Podemos ser tentados a escrever isto:

```ts twoslash
// @errors: 2339
function loggingIdentity<Type>(arg: Type): Type {
  console.log(arg.length);
  return arg;
}
```

Ao fazer isso, o compilador vai nos dar um erro dizendo que estamos usando o membro `.length` de `arg`, mas em lugar nenhum dissemos que `arg` tem esse membro.
Lembre-se: dissemos antes que essas variáveis de tipo representam qualquer tipo, então quem usar essa função poderia ter passado um `number`, que não tem um membro `.length`.

Digamos que a nossa intenção era que esta função funcionasse com arrays de `Type`, e não com `Type` diretamente. Como estamos trabalhando com arrays, o membro `.length` deveria estar disponível.
Podemos descrever isso da mesma forma que criaríamos arrays de outros tipos:

```ts twoslash {1}
function loggingIdentity<Type>(arg: Type[]): Type[] {
  console.log(arg.length);
  return arg;
}
```

Você pode ler o tipo de `loggingIdentity` como "a função genérica `loggingIdentity` recebe um parâmetro de tipo `Type` e um argumento `arg` que é um array de `Type`, e retorna um array de `Type`."
Se passarmos um array de números, receberemos de volta um array de números, já que `Type` será vinculado a `number`.
Isso nos permite usar a nossa variável de tipo genérica `Type` como parte dos tipos com que estamos trabalhando, em vez do tipo inteiro, o que nos dá mais flexibilidade.

Também podemos escrever o exemplo anterior desta forma:

```ts twoslash {1}
function loggingIdentity<Type>(arg: Array<Type>): Array<Type> {
  console.log(arg.length); // Array has a .length, so no more error
  return arg;
}
```

Você pode já estar familiarizado com esse estilo de tipo de outras linguagens.
Na próxima seção, vamos ver como criar os seus próprios tipos genéricos, como `Array<Type>`.

## Tipos Genéricos {#generic-types}

Nas seções anteriores, criamos funções identidade genéricas que funcionavam com uma faixa de tipos.
Nesta seção, vamos explorar o tipo das próprias funções e como criar interfaces genéricas.

O tipo de funções genéricas é igual ao de funções não genéricas, com os parâmetros de tipo listados primeiro, de forma semelhante às declarações de função:

```ts twoslash
function identity<Type>(arg: Type): Type {
  return arg;
}

let myIdentity: <Type>(arg: Type) => Type = identity;
```

Também poderíamos ter usado um nome diferente para o parâmetro de tipo genérico no tipo, desde que a quantidade de variáveis de tipo e a forma como elas são usadas se correspondam.

```ts twoslash
function identity<Type>(arg: Type): Type {
  return arg;
}

let myIdentity: <Input>(arg: Input) => Input = identity;
```

Também podemos escrever o tipo genérico como uma assinatura de chamada de um tipo objeto literal:

```ts twoslash
function identity<Type>(arg: Type): Type {
  return arg;
}

let myIdentity: { <Type>(arg: Type): Type } = identity;
```

O que nos leva a escrever a nossa primeira interface genérica.
Vamos pegar o objeto literal do exemplo anterior e movê-lo para uma interface:

```ts twoslash
interface GenericIdentityFn {
  <Type>(arg: Type): Type;
}

function identity<Type>(arg: Type): Type {
  return arg;
}

let myIdentity: GenericIdentityFn = identity;
```

Em um exemplo parecido, podemos querer mover o parâmetro genérico para ser um parâmetro da interface inteira.
Isso nos permite ver sobre qual(is) tipo(s) somos genéricos (por exemplo, `Dictionary<string>` em vez de apenas `Dictionary`).
Assim, o parâmetro de tipo fica visível para todos os outros membros da interface.

```ts twoslash
interface GenericIdentityFn<Type> {
  (arg: Type): Type;
}

function identity<Type>(arg: Type): Type {
  return arg;
}

let myIdentity: GenericIdentityFn<number> = identity;
```

Observe que o nosso exemplo mudou para algo um pouco diferente.
Em vez de descrever uma função genérica, agora temos uma assinatura de função não genérica que faz parte de um tipo genérico.
Ao usar `GenericIdentityFn`, agora também precisamos especificar o argumento de tipo correspondente (aqui: `number`), o que efetivamente fixa o tipo que a assinatura de chamada subjacente vai usar.
Entender quando colocar o parâmetro de tipo diretamente na assinatura de chamada e quando colocá-lo na própria interface vai ajudar a descrever quais aspectos de um tipo são genéricos.

Além de interfaces genéricas, também podemos criar classes genéricas.
Observe que não é possível criar enums e namespaces genéricos.

## Classes Genéricas {#generic-classes}

Uma classe genérica tem uma forma semelhante a uma interface genérica.
Classes genéricas têm uma lista de parâmetros de tipo entre colchetes angulares (`<>`) logo após o nome da classe.

```ts twoslash
// @strict: false
class GenericNumber<NumType> {
  zeroValue: NumType;
  add: (x: NumType, y: NumType) => NumType;
}

let myGenericNumber = new GenericNumber<number>();
myGenericNumber.zeroValue = 0;
myGenericNumber.add = function (x, y) {
  return x + y;
};
```

Este é um uso bem literal da classe `GenericNumber`, mas talvez você tenha notado que nada a impede de usar apenas o tipo `number`.
Poderíamos ter usado `string` ou até objetos mais complexos.

```ts twoslash
// @strict: false
class GenericNumber<NumType> {
  zeroValue: NumType;
  add: (x: NumType, y: NumType) => NumType;
}
// ---cut---
let stringNumeric = new GenericNumber<string>();
stringNumeric.zeroValue = "";
stringNumeric.add = function (x, y) {
  return x + y;
};

console.log(stringNumeric.add(stringNumeric.zeroValue, "test"));
```

Assim como com interfaces, colocar o parâmetro de tipo na própria classe nos permite garantir que todas as propriedades da classe estão trabalhando com o mesmo tipo.

Como vemos em [nossa seção sobre classes](/docs/handbook/2/classes.html), uma classe tem dois lados em seu tipo: o lado estático e o lado da instância.
Classes genéricas são genéricas apenas em seu lado de instância, e não em seu lado estático; por isso, ao trabalhar com classes, membros estáticos não podem usar o parâmetro de tipo da classe.

## Restrições Genéricas {#generic-constraints}

Se você se lembra de um exemplo anterior, às vezes você pode querer escrever uma função genérica que funciona com um conjunto de tipos sobre os quais você tem _algum_ conhecimento das capacidades que esse conjunto terá.
No nosso exemplo `loggingIdentity`, queríamos poder acessar a propriedade `.length` de `arg`, mas o compilador não conseguia provar que todos os tipos têm a propriedade `.length`, então ele nos avisa que não podemos fazer essa suposição.

```ts twoslash
// @errors: 2339
function loggingIdentity<Type>(arg: Type): Type {
  console.log(arg.length);
  return arg;
}
```

Em vez de trabalhar com qualquer tipo, queremos restringir esta função para trabalhar apenas com os tipos que _também_ têm a propriedade `.length`.
Desde que o tipo tenha esse membro, nós o aceitamos, mas é obrigatório que ele tenha pelo menos esse membro.
Para isso, precisamos declarar nosso requisito como uma restrição sobre o que `Type` pode ser.

Para isso, vamos criar uma interface que descreve a nossa restrição.
Aqui, criaremos uma interface que tem uma única propriedade `.length` e depois usaremos essa interface com a palavra-chave `extends` para indicar a nossa restrição:

```ts twoslash
interface Lengthwise {
  length: number;
}

function loggingIdentity<Type extends Lengthwise>(arg: Type): Type {
  console.log(arg.length); // Now we know it has a .length property, so no more error
  return arg;
}
```

Como a função genérica agora está restrita, ela não vai mais funcionar com qualquer tipo:

```ts twoslash
// @errors: 2345
interface Lengthwise {
  length: number;
}

function loggingIdentity<Type extends Lengthwise>(arg: Type): Type {
  console.log(arg.length);
  return arg;
}
// ---cut---
loggingIdentity(3);
```

Em vez disso, precisamos passar valores cujo tipo tenha todas as propriedades exigidas:

```ts twoslash
interface Lengthwise {
  length: number;
}

function loggingIdentity<Type extends Lengthwise>(arg: Type): Type {
  console.log(arg.length);
  return arg;
}
// ---cut---
loggingIdentity({ length: 10, value: 3 });
```

## Usando Parâmetros de Tipo em Restrições Genéricas {#using-type-parameters-in-generic-constraints}

Você pode declarar um parâmetro de tipo que é restrito por outro parâmetro de tipo.
Por exemplo, aqui queremos obter uma propriedade de um objeto a partir do seu nome.
Queremos garantir que não estamos pegando por acidente uma propriedade que não existe em `obj`, então vamos colocar uma restrição entre os dois tipos:

```ts twoslash
// @errors: 2345
function getProperty<Type, Key extends keyof Type>(obj: Type, key: Key) {
  return obj[key];
}

let x = { a: 1, b: 2, c: 3, d: 4 };

getProperty(x, "a");
getProperty(x, "m");
```

## Usando Tipos de Classe em Genéricos {#using-class-types-in-generics}

Ao criar fábricas no TypeScript usando genéricos, é necessário referenciar tipos de classe pelas suas funções construtoras. Por exemplo,

```ts twoslash
function create<Type>(c: { new (): Type }): Type {
  return new c();
}
```

Um exemplo mais avançado usa a propriedade `prototype` para inferir e restringir relações entre a função construtora e o lado da instância dos tipos de classe.

```ts twoslash
// @strict: false
class BeeKeeper {
  hasMask: boolean = true;
}

class ZooKeeper {
  nametag: string = "Mikle";
}

class Animal {
  numLegs: number = 4;
}

class Bee extends Animal {
  numLegs = 6;
  keeper: BeeKeeper = new BeeKeeper();
}

class Lion extends Animal {
  keeper: ZooKeeper = new ZooKeeper();
}

function createInstance<A extends Animal>(c: new () => A): A {
  return new c();
}

createInstance(Lion).keeper.nametag;
createInstance(Bee).keeper.hasMask;
```

Este padrão é usado para sustentar o padrão de design de [mixins](/docs/handbook/mixins.html).

## Padrões de Parâmetros Genéricos {#generic-parameter-defaults}

Ao declarar um padrão para um parâmetro de tipo genérico, você torna opcional informar o argumento de tipo correspondente. Por exemplo, uma função que cria um novo `HTMLElement`. Chamar a função sem argumentos gera um `HTMLDivElement`; chamar a função com um elemento como primeiro argumento gera um elemento do tipo do argumento. Você também pode, opcionalmente, passar uma lista de filhos. Antes, você precisaria definir a função assim:


```ts twoslash
type Container<T, U> = {
  element: T;
  children: U;
};

// ---cut---
declare function create(): Container<HTMLDivElement, HTMLDivElement[]>;
declare function create<T extends HTMLElement>(element: T): Container<T, T[]>;
declare function create<T extends HTMLElement, U extends HTMLElement>(
  element: T,
  children: U[]
): Container<T, U[]>;
```

Com padrões de parâmetros genéricos, podemos reduzir isso para:

```ts twoslash
type Container<T, U> = {
  element: T;
  children: U;
};

// ---cut---
declare function create<T extends HTMLElement = HTMLDivElement, U extends HTMLElement[] = T[]>(
  element?: T,
  children?: U
): Container<T, U>;

const div = create();
//    ^?

const p = create(new HTMLParagraphElement());
//    ^?
```

Um padrão de parâmetro genérico segue as seguintes regras:

- Um parâmetro de tipo é considerado opcional se tiver um padrão.
- Parâmetros de tipo obrigatórios não podem vir depois de parâmetros de tipo opcionais.
- Os tipos padrão de um parâmetro de tipo devem satisfazer a restrição do parâmetro de tipo, se ela existir.
- Ao especificar argumentos de tipo, você só precisa informar os argumentos dos parâmetros de tipo obrigatórios. Os parâmetros de tipo não informados vão resolver para os seus tipos padrão.
- Se um tipo padrão for especificado e a inferência não conseguir escolher um candidato, o tipo padrão é inferido.
- Uma declaração de classe ou interface que se mescla com uma classe ou interface já existente pode introduzir um padrão para um parâmetro de tipo existente.
- Uma declaração de classe ou interface que se mescla com uma classe ou interface já existente pode introduzir um novo parâmetro de tipo, desde que especifique um padrão.

## Anotações de Variância {#variance-annotations}

> Este é um recurso avançado para resolver um problema muito específico, e deve ser usado apenas em situações em que você tenha identificado um motivo para usá-lo

[Covariância e contravariância](https://en.wikipedia.org/wiki/Covariance_and_contravariance_(computer_science)) são termos da teoria de tipos que descrevem qual é a relação entre dois tipos genéricos.
Aqui vai uma breve introdução ao conceito.

Por exemplo, se você tem uma interface que representa um objeto que pode `make` (fabricar) um certo tipo:
```ts
interface Producer<T> {
  make(): T;
}
```
Podemos usar um `Producer<Cat>` onde um `Producer<Animal>` é esperado, porque um `Cat` é um `Animal`.
Essa relação se chama *covariância*: a relação de `Producer<T>` para `Producer<U>` é a mesma relação de `T` para `U`.

Por outro lado, se você tem uma interface que pode `consume` (consumir) um certo tipo:
```ts
interface Consumer<T> {
  consume: (arg: T) => void;
}
```
Então podemos usar um `Consumer<Animal>` onde um `Consumer<Cat>` é esperado, porque qualquer função capaz de aceitar um `Animal` também precisa ser capaz de aceitar um `Cat`.
Essa relação se chama *contravariância*: a relação de `Consumer<T>` para `Consumer<U>` é a mesma relação de `U` para `T`.
Observe a inversão de direção em comparação com a covariância! É por isso que a contravariância "se anula" e a covariância não.

Em um sistema de tipos estrutural, como o do TypeScript, covariância e contravariância são comportamentos que surgem naturalmente das definições dos tipos.
Mesmo sem genéricos, veríamos relações covariantes (e contravariantes):
```ts
interface AnimalProducer {
  make(): Animal;
}

// A CatProducer can be used anywhere an
// Animal producer is expected
interface CatProducer {
  make(): Cat;
}
```

O TypeScript tem um sistema de tipos estrutural, então, ao comparar dois tipos, por exemplo para verificar se um `Producer<Cat>` pode ser usado onde um `Producer<Animal>` é esperado, o algoritmo usual expandiria estruturalmente as duas definições e compararia as suas estruturas.
No entanto, a variância permite uma otimização extremamente útil: se `Producer<T>` é covariante em `T`, podemos simplesmente verificar `Cat` e `Animal`, já que sabemos que eles terão a mesma relação que `Producer<Cat>` e `Producer<Animal>`.

Observe que essa lógica só pode ser usada quando estamos examinando duas instanciações do mesmo tipo.
Se temos um `Producer<T>` e um `FastProducer<U>`, não há garantia de que `T` e `U` se referem necessariamente às mesmas posições nesses tipos, então essa verificação sempre será feita de forma estrutural.

Como a variância é uma propriedade que surge naturalmente dos tipos estruturais, o TypeScript *infere* automaticamente a variância de todo tipo genérico.
**Em casos extremamente raros**, envolvendo certos tipos circulares, essa medição pode ser imprecisa.
Se isso acontecer, você pode adicionar uma anotação de variância a um parâmetro de tipo para forçar uma variância específica:
```ts
// Contravariant annotation
interface Consumer<in T> {
  consume: (arg: T) => void;
}

// Covariant annotation
interface Producer<out T> {
  make(): T;
}

// Invariant annotation
interface ProducerConsumer<in out T> {
  consume: (arg: T) => void;
  make(): T;
}
```
Faça isso apenas se você estiver escrevendo a mesma variância que *deveria* ocorrer estruturalmente.

> Nunca escreva uma anotação de variância que não corresponda à variância estrutural!

É fundamental reforçar que as anotações de variância só têm efeito durante uma comparação baseada em instanciação.
Elas não têm efeito durante uma comparação estrutural.
Por exemplo, você não pode usar anotações de variância para "forçar" um tipo a ser de fato invariante:
```ts
// DON'T DO THIS - variance annotation
// does not match structural behavior
interface Producer<in out T> {
  make(): T;
}

// Not a type error -- this is a structural
// comparison, so variance annotations are
// not in effect
const p: Producer<string | number> = {
    make(): number {
        return 42;
    }
}
```
Aqui, a função `make` do objeto literal retorna `number`, o que poderíamos esperar que causasse um erro, porque `number` não é `string | number`.
No entanto, isso não é uma comparação baseada em instanciação, porque o objeto literal é um tipo anônimo, não um `Producer<string | number>`.

> Anotações de variância não mudam o comportamento estrutural e só são consideradas em situações específicas

É muito importante escrever anotações de variância apenas se você tiver certeza absoluta do motivo, de quais são as suas limitações e de quando elas não estão em vigor.
Se o TypeScript usa uma comparação baseada em instanciação ou uma comparação estrutural não é um comportamento especificado e pode mudar de versão para versão por motivos de correção ou desempenho; por isso, você só deve escrever anotações de variância quando elas corresponderem ao comportamento estrutural de um tipo.
Não use anotações de variância para tentar "forçar" uma variância particular; isso vai causar um comportamento imprevisível no seu código.

> NÃO escreva anotações de variância a menos que elas correspondam ao comportamento estrutural de um tipo

Lembre-se: o TypeScript consegue inferir automaticamente a variância a partir dos seus tipos genéricos.
Quase nunca é necessário escrever uma anotação de variância, e você só deve fazê-lo quando tiver identificado uma necessidade específica.
Anotações de variância *não* mudam o comportamento estrutural de um tipo e, dependendo da situação, você pode ver uma comparação estrutural sendo feita quando esperava uma comparação baseada em instanciação.
Anotações de variância não podem ser usadas para modificar como os tipos se comportam nesses contextos estruturais e não devem ser escritas, a menos que a anotação seja igual à definição estrutural.
Como isso é difícil de acertar, e como o TypeScript consegue inferir corretamente a variância na grande maioria dos casos, você não deveria se ver escrevendo anotações de variância em código comum.

> Não tente usar anotações de variância para mudar o comportamento de verificação de tipos; essa não é a finalidade delas

Você *pode* achar úteis anotações de variância temporárias em uma situação de "depuração de tipos", porque as anotações de variância são verificadas.
O TypeScript vai emitir um erro se a variância anotada estiver claramente errada:
```ts
// Error, this interface is definitely contravariant on T
interface Foo<out T> {
  consume: (arg: T) => void;
}
```
No entanto, anotações de variância podem ser mais restritivas do que o necessário (por exemplo, `in out` é válido se a variância real for covariante).
Lembre-se de remover suas anotações de variância quando terminar a depuração.

Por fim, se você estiver tentando maximizar o desempenho da verificação de tipos, *e* já tiver rodado um profiler, *e* tiver identificado um tipo específico que é lento, *e* tiver identificado que a inferência de variância especificamente é lenta, *e* tiver validado cuidadosamente a anotação de variância que deseja escrever, você *pode* ver um pequeno ganho de desempenho em tipos extraordinariamente complexos ao adicionar anotações de variância.

> Não tente usar anotações de variância para mudar o comportamento de verificação de tipos; essa não é a finalidade delas
