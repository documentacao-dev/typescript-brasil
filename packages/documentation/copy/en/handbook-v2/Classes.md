---
title: Classes
layout: docs
permalink: /docs/handbook/2/classes.html
oneline: "Como as classes funcionam no TypeScript"
ia-translate: true
---

<blockquote class='bg-reading'>
  <p>Leitura de apoio:<br /><a href='https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes'>Classes (MDN)</a></p>
</blockquote>

O TypeScript oferece suporte completo à palavra-chave `class`, introduzida no ES2015.

Assim como outros recursos da linguagem JavaScript, o TypeScript acrescenta anotações de tipo e outras sintaxes para que você possa expressar relações entre classes e outros tipos.

## Membros de classe {#class-members}

Aqui está a classe mais básica possível, uma vazia:

```ts twoslash
class Point {}
```

Essa classe ainda não é muito útil, então vamos começar a adicionar alguns membros.

### Campos {#fields}

Uma declaração de campo cria uma propriedade pública e gravável na classe:

```ts twoslash
// @strictPropertyInitialization: false
class Point {
  x: number;
  y: number;
}

const pt = new Point();
pt.x = 0;
pt.y = 0;
```

Assim como em outros lugares, a anotação de tipo é opcional, mas, se não for especificada, será um `any` implícito.

Os campos também podem ter _inicializadores_; eles serão executados automaticamente quando a classe for instanciada:

```ts twoslash
class Point {
  x = 0;
  y = 0;
}

const pt = new Point();
// Prints 0, 0
console.log(`${pt.x}, ${pt.y}`);
```

Assim como acontece com `const`, `let` e `var`, o inicializador de uma propriedade de classe será usado para inferir o seu tipo:

```ts twoslash
// @errors: 2322
class Point {
  x = 0;
  y = 0;
}
// ---cut---
const pt = new Point();
pt.x = "0";
```

#### `--strictPropertyInitialization`

A configuração [`strictPropertyInitialization`](/tsconfig#strictPropertyInitialization) controla se os campos da classe precisam ser inicializados no construtor.

```ts twoslash
// @errors: 2564
class BadGreeter {
  name: string;
}
```

```ts twoslash
class GoodGreeter {
  name: string;

  constructor() {
    this.name = "hello";
  }
}
```

Observe que o campo precisa ser inicializado _dentro do próprio construtor_.
O TypeScript não analisa os métodos que você invoca a partir do construtor para detectar inicializações, porque uma classe derivada pode sobrescrever esses métodos e deixar de inicializar os membros.

Se você pretende inicializar um campo de forma definitiva por outro meio que não o construtor (por exemplo, uma biblioteca externa que preenche parte da classe para você), pode usar o _operador de asserção de atribuição definida_, `!`:

```ts twoslash
class OKGreeter {
  // Not initialized, but no error
  name!: string;
}
```

### `readonly`

Campos podem ter o modificador `readonly` como prefixo.
Isso impede atribuições ao campo fora do construtor.

```ts twoslash
// @errors: 2540 2540
class Greeter {
  readonly name: string = "world";

  constructor(otherName?: string) {
    if (otherName !== undefined) {
      this.name = otherName;
    }
  }

  err() {
    this.name = "not ok";
  }
}
const g = new Greeter();
g.name = "also not ok";
```

### Constructors

<blockquote class='bg-reading'>
   <p>Leitura de apoio:<br />
   <a href='https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes/constructor'>Construtor (MDN)</a><br/>
   </p>
</blockquote>

Os construtores de classe são muito parecidos com funções.
Você pode adicionar parâmetros com anotações de tipo, valores padrão e overloads:

```ts twoslash
class Point {
  x: number;
  y: number;

  // Normal signature with defaults
  constructor(x = 0, y = 0) {
    this.x = x;
    this.y = y;
  }
}
```

```ts twoslash
class Point {
  x: number = 0;
  y: number = 0;

  // Constructor overloads
  constructor(x: number, y: number);
  constructor(xy: string);
  constructor(x: string | number, y: number = 0) {
    // Code logic here
  }
}
```

Há apenas algumas diferenças entre as assinaturas de construtores de classe e as assinaturas de funções:

- Construtores não podem ter parâmetros de tipo - estes pertencem à declaração da classe externa, que veremos mais adiante
- Construtores não podem ter anotações de tipo de retorno - o tipo da instância da classe é sempre o que é retornado

#### Chamadas a `super` {#super-calls}

Assim como no JavaScript, se você tiver uma classe base, precisará chamar `super();` no corpo do construtor antes de usar qualquer membro `this.`:

```ts twoslash
// @errors: 17009
class Base {
  k = 4;
}

class Derived extends Base {
  constructor() {
    // Prints a wrong value in ES5; throws exception in ES6
    console.log(this.k);
    super();
  }
}
```

Esquecer de chamar `super` é um erro fácil de cometer em JavaScript, mas o TypeScript avisa quando essa chamada é necessária.

### Métodos {#methods}

<blockquote class='bg-reading'>
   <p>Leitura de apoio:<br />
   <a href='https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Method_definitions'>Definições de métodos (MDN)</a><br/>
   </p>
</blockquote>

Uma propriedade de função em uma classe é chamada de _método_.
Métodos podem usar todas as mesmas anotações de tipo que funções e construtores:

```ts twoslash
class Point {
  x = 10;
  y = 10;

  scale(n: number): void {
    this.x *= n;
    this.y *= n;
  }
}
```

Além das anotações de tipo habituais, o TypeScript não acrescenta nada de novo aos métodos.

Observe que, dentro do corpo de um método, ainda é obrigatório acessar campos e outros métodos por meio de `this.`.
Um nome sem qualificação no corpo de um método sempre se refere a algo do escopo externo:

```ts twoslash
// @errors: 2322
let x: number = 0;

class C {
  x: string = "hello";

  m() {
    // This is trying to modify 'x' from line 1, not the class property
    x = "world";
  }
}
```

### Getters / Setters

Classes também podem ter _acessadores_:

```ts twoslash
class C {
  _length = 0;
  get length() {
    return this._length;
  }
  set length(value) {
    this._length = value;
  }
}
```

> Observe que um par get/set apoiado em um campo, sem lógica extra, raramente é útil em JavaScript.
> Não há problema em expor campos públicos se você não precisar adicionar lógica extra nas operações de get/set.

O TypeScript tem algumas regras especiais de inferência para acessadores:

- Se existir `get` mas não `set`, a propriedade será automaticamente `readonly`
- Se o tipo do parâmetro do setter não for especificado, ele é inferido a partir do tipo de retorno do getter

Desde o [TypeScript 4.3](https://devblogs.microsoft.com/typescript/announcing-typescript-4-3/), é possível ter acessadores com tipos diferentes para leitura e escrita.

```ts twoslash
class Thing {
  _size = 0;

  get size(): number {
    return this._size;
  }

  set size(value: string | number | boolean) {
    let num = Number(value);

    // Don't allow NaN, Infinity, etc

    if (!Number.isFinite(num)) {
      this._size = 0;
      return;
    }

    this._size = num;
  }
}
```

### Assinaturas de índice {#index-signatures}

Classes podem declarar assinaturas de índice; elas funcionam da mesma forma que as [assinaturas de índice de outros tipos de objeto](/docs/handbook/2/objects.html#index-signatures):

```ts twoslash
class MyClass {
  [s: string]: boolean | ((s: string) => boolean);

  check(s: string) {
    return this[s] as boolean;
  }
}
```

Como o tipo da assinatura de índice também precisa capturar os tipos dos métodos, não é fácil usar esses tipos de forma útil.
Em geral, é melhor guardar dados indexados em outro lugar, em vez de na própria instância da classe.

## Herança de classes {#class-heritage}

Assim como em outras linguagens com recursos orientados a objetos, classes em JavaScript podem herdar de classes base.

### Cláusulas `implements` {#implements-clauses}

Você pode usar uma cláusula `implements` para verificar se uma classe satisfaz uma determinada `interface`.
Um erro será emitido se a classe não implementar corretamente a interface:

```ts twoslash
// @errors: 2420
interface Pingable {
  ping(): void;
}

class Sonar implements Pingable {
  ping() {
    console.log("ping!");
  }
}

class Ball implements Pingable {
  pong() {
    console.log("pong!");
  }
}
```

Classes também podem implementar várias interfaces, por exemplo, `class C implements A, B {`.

#### Cuidados {#cautions}

É importante entender que uma cláusula `implements` é apenas uma verificação de que a classe pode ser tratada como o tipo da interface.
Ela _não_ altera de forma alguma o tipo da classe nem dos seus métodos.
Uma fonte comum de erros é supor que uma cláusula `implements` mudará o tipo da classe - ela não muda!

```ts twoslash
// @errors: 7006
interface Checkable {
  check(name: string): boolean;
}

class NameChecker implements Checkable {
  check(s) {
    // Notice no error here
    return s.toLowerCase() === "ok";
    //         ^?
  }
}
```

Neste exemplo, talvez esperássemos que o tipo de `s` fosse influenciado pelo parâmetro `name: string` de `check`.
Não é: cláusulas `implements` não mudam a forma como o corpo da classe é verificado nem como o seu tipo é inferido.

Da mesma forma, implementar uma interface com uma propriedade opcional não cria essa propriedade:

```ts twoslash
// @errors: 2339
interface A {
  x: number;
  y?: number;
}
class C implements A {
  x = 0;
}
const c = new C();
c.y = 10;
```

### Cláusulas `extends` {#extends-clauses}

<blockquote class='bg-reading'>
   <p>Leitura de apoio:<br />
   <a href='https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes/extends'>Palavra-chave extends (MDN)</a><br/>
   </p>
</blockquote>

Classes podem usar `extends` para herdar de uma classe base.
Uma classe derivada tem todas as propriedades e métodos da sua classe base e também pode definir membros adicionais.

```ts twoslash
class Animal {
  move() {
    console.log("Moving along!");
  }
}

class Dog extends Animal {
  woof(times: number) {
    for (let i = 0; i < times; i++) {
      console.log("woof!");
    }
  }
}

const d = new Dog();
// Base class method
d.move();
// Derived class method
d.woof(3);
```

#### Sobrescrevendo métodos {#overriding-methods}

<blockquote class='bg-reading'>
   <p>Leitura de apoio:<br />
   <a href='https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/super'>Palavra-chave super (MDN)</a><br/>
   </p>
</blockquote>

Uma classe derivada também pode sobrescrever um campo ou propriedade da classe base.
Você pode usar a sintaxe `super.` para acessar métodos da classe base.
Observe que, como classes em JavaScript são um simples objeto de busca, não existe o conceito de "campo super".

O TypeScript garante que uma classe derivada seja sempre um subtipo da sua classe base.

Por exemplo, esta é uma forma válida de sobrescrever um método:

```ts twoslash
class Base {
  greet() {
    console.log("Hello, world!");
  }
}

class Derived extends Base {
  greet(name?: string) {
    if (name === undefined) {
      super.greet();
    } else {
      console.log(`Hello, ${name.toUpperCase()}`);
    }
  }
}

const d = new Derived();
d.greet();
d.greet("reader");
```

É importante que uma classe derivada respeite o contrato da sua classe base.
Lembre-se de que é muito comum (e sempre válido!) referenciar uma instância de classe derivada por meio de uma referência de classe base:

```ts twoslash
class Base {
  greet() {
    console.log("Hello, world!");
  }
}
class Derived extends Base {}
const d = new Derived();
// ---cut---
// Alias the derived instance through a base class reference
const b: Base = d;
// No problem
b.greet();
```

E se `Derived` não seguisse o contrato de `Base`?

```ts twoslash
// @errors: 2416
class Base {
  greet() {
    console.log("Hello, world!");
  }
}

class Derived extends Base {
  // Make this parameter required
  greet(name: string) {
    console.log(`Hello, ${name.toUpperCase()}`);
  }
}
```

Se compilássemos esse código apesar do erro, este exemplo acabaria falhando:

```ts twoslash
declare class Base {
  greet(): void;
}
declare class Derived extends Base {}
// ---cut---
const b: Base = new Derived();
// Crashes because "name" will be undefined
b.greet();
```

#### Declarações de campo somente de tipo {#type-only-field-declarations}

Quando `target >= ES2022` ou [`useDefineForClassFields`](/tsconfig#useDefineForClassFields) é `true`, os campos da classe são inicializados depois que o construtor da classe pai termina, sobrescrevendo qualquer valor definido pela classe pai. Isso pode ser um problema quando você só quer declarar novamente um tipo mais preciso para um campo herdado. Para esses casos, você pode escrever `declare` para indicar ao TypeScript que essa declaração de campo não deve ter efeito em tempo de execução.

```ts twoslash
interface Animal {
  dateOfBirth: any;
}

interface Dog extends Animal {
  breed: any;
}

class AnimalHouse {
  resident: Animal;
  constructor(animal: Animal) {
    this.resident = animal;
  }
}

class DogHouse extends AnimalHouse {
  // Does not emit JavaScript code,
  // only ensures the types are correct
  declare resident: Dog;
  constructor(dog: Dog) {
    super(dog);
  }
}
```

#### Ordem de inicialização {#initialization-order}

A ordem em que as classes JavaScript são inicializadas pode ser surpreendente em alguns casos.
Vamos considerar este código:

```ts twoslash
class Base {
  name = "base";
  constructor() {
    console.log("My name is " + this.name);
  }
}

class Derived extends Base {
  name = "derived";
}

// Prints "base", not "derived"
const d = new Derived();
```

O que aconteceu aqui?

A ordem de inicialização de classes, como definida pelo JavaScript, é:

- Os campos da classe base são inicializados
- O construtor da classe base é executado
- Os campos da classe derivada são inicializados
- O construtor da classe derivada é executado

Isso significa que o construtor da classe base viu o seu próprio valor de `name` durante o seu construtor, porque as inicializações dos campos da classe derivada ainda não tinham sido executadas.

#### Herdando tipos integrados {#inheriting-built-in-types}

> Observação: se você não pretende herdar de tipos integrados como `Array`, `Error`, `Map`, etc., ou se o seu alvo de compilação for explicitamente `ES6`/`ES2015` ou superior, você pode pular esta seção

No ES2015, construtores que retornam um objeto substituem implicitamente o valor de `this` para qualquer chamador de `super(...)`.
É necessário que o código de construtor gerado capture qualquer possível valor de retorno de `super(...)` e o substitua por `this`.

Como consequência, a subclasse de `Error`, `Array` e outros pode deixar de funcionar como esperado.
Isso acontece porque as funções construtoras de `Error`, `Array` e similares usam o `new.target` do ECMAScript 6 para ajustar a cadeia de protótipos;
porém, não há como garantir um valor para `new.target` ao invocar um construtor no ECMAScript 5.
Outros compiladores de downleveling geralmente têm a mesma limitação por padrão.

Para uma subclasse como a seguinte:

```ts twoslash
class MsgError extends Error {
  constructor(m: string) {
    super(m);
  }
  sayHello() {
    return "hello " + this.message;
  }
}
```

você pode descobrir que:

- métodos podem estar `undefined` em objetos retornados ao instanciar essas subclasses, então chamar `sayHello` resultará em erro.
- `instanceof` deixará de funcionar entre instâncias da subclasse e as suas instâncias, então `(new MsgError()) instanceof MsgError` retornará `false`.

Como recomendação, você pode ajustar manualmente o protótipo imediatamente após qualquer chamada a `super(...)`.

```ts twoslash
class MsgError extends Error {
  constructor(m: string) {
    super(m);

    // Set the prototype explicitly.
    Object.setPrototypeOf(this, MsgError.prototype);
  }

  sayHello() {
    return "hello " + this.message;
  }
}
```

No entanto, qualquer subclasse de `MsgError` também terá que definir o protótipo manualmente.
Para ambientes de execução que não suportam [`Object.setPrototypeOf`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/setPrototypeOf), talvez você consiga usar [`__proto__`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/proto).

Infelizmente, [essas soluções alternativas não funcionam no Internet Explorer 10 e versões anteriores](<https://msdn.microsoft.com/en-us/library/s4esdbwz(v=vs.94).aspx>).
É possível copiar manualmente os métodos do protótipo para a própria instância (ou seja, de `MsgError.prototype` para `this`), mas a cadeia de protótipos em si não pode ser corrigida.

## Visibilidade de membros {#member-visibility}

Você pode usar o TypeScript para controlar se determinados métodos ou propriedades ficam visíveis para código fora da classe.

### `public`

A visibilidade padrão dos membros de classe é `public`.
Um membro `public` pode ser acessado em qualquer lugar:

```ts twoslash
class Greeter {
  public greet() {
    console.log("hi!");
  }
}
const g = new Greeter();
g.greet();
```

Como `public` já é o modificador de visibilidade padrão, você nunca _precisa_ escrevê-lo em um membro de classe, mas pode optar por fazê-lo por questões de estilo ou legibilidade.

### `protected`

Membros `protected` só são visíveis para subclasses da classe em que foram declarados.

```ts twoslash
// @errors: 2445
class Greeter {
  public greet() {
    console.log("Hello, " + this.getName());
  }
  protected getName() {
    return "hi";
  }
}

class SpecialGreeter extends Greeter {
  public howdy() {
    // OK to access protected member here
    console.log("Howdy, " + this.getName());
    //                          ^^^^^^^^^^^^^^
  }
}
const g = new SpecialGreeter();
g.greet(); // OK
g.getName();
```

#### Exposição de membros `protected` {#exposure-of-protected-members}

Classes derivadas precisam respeitar o contrato de suas classes base, mas podem optar por expor um subtipo da classe base com mais capacidades.
Isso inclui tornar `public` os membros `protected`:

```ts twoslash
class Base {
  protected m = 10;
}
class Derived extends Base {
  // No modifier, so default is 'public'
  m = 15;
}
const d = new Derived();
console.log(d.m); // OK
```

Observe que `Derived` já conseguia ler e escrever `m` livremente, então isso não altera de forma significativa a "segurança" da situação.
O ponto principal a notar aqui é que, na classe derivada, devemos ter cuidado para repetir o modificador `protected` se essa exposição não for intencional.

#### Acesso `protected` entre hierarquias {#cross-hierarchy-protected-access}

O TypeScript não permite acessar membros `protected` de uma classe irmã dentro de uma hierarquia de classes:

```ts twoslash
// @errors: 2446
class Base {
  protected x: number = 1;
}
class Derived1 extends Base {
  protected x: number = 5;
}
class Derived2 extends Base {
  f1(other: Derived2) {
    other.x = 10;
  }
  f2(other: Derived1) {
    other.x = 10;
  }
}
```

Isso acontece porque acessar `x` em `Derived2` deveria ser legal apenas a partir das subclasses de `Derived2`, e `Derived1` não é uma delas.
Além disso, se acessar `x` por uma referência de `Derived1` é ilegal (como de fato deveria ser!), então acessá-lo por uma referência de classe base nunca deveria melhorar a situação.

Veja também [Por que não consigo acessar um membro protegido a partir de uma classe derivada?](https://blogs.msdn.microsoft.com/ericlippert/2005/11/09/why-cant-i-access-a-protected-member-from-a-derived-class/), que explica melhor o raciocínio do C# sobre o mesmo tema.

### `private`

`private` é como `protected`, mas não permite acesso ao membro nem mesmo a partir de subclasses:

```ts twoslash
// @errors: 2341
class Base {
  private x = 0;
}
const b = new Base();
// Can't access from outside the class
console.log(b.x);
```

```ts twoslash
// @errors: 2341
class Base {
  private x = 0;
}
// ---cut---
class Derived extends Base {
  showX() {
    // Can't access in subclasses
    console.log(this.x);
  }
}
```

Como membros `private` não são visíveis para classes derivadas, uma classe derivada não pode aumentar a visibilidade deles:

```ts twoslash
// @errors: 2415
class Base {
  private x = 0;
}
class Derived extends Base {
  x = 1;
}
```

#### Acesso `private` entre instâncias {#cross-instance-private-access}

Diferentes linguagens orientadas a objetos discordam sobre se instâncias diferentes da mesma classe podem acessar os membros `private` umas das outras.
Enquanto linguagens como Java, C#, C++, Swift e PHP permitem isso, Ruby não permite.

O TypeScript permite o acesso `private` entre instâncias:

```ts twoslash
class A {
  private x = 10;

  public sameAs(other: A) {
    // No error
    return other.x === this.x;
  }
}
```

#### Ressalvas {#caveats}

Como outros aspectos do sistema de tipos do TypeScript, `private` e `protected` [são aplicados apenas durante a verificação de tipos](https://www.typescriptlang.org/play?removeComments=true&target=99&ts=4.3.4#code/PTAEGMBsEMGddAEQPYHNQBMCmVoCcsEAHPASwDdoAXLUAM1K0gwQFdZSA7dAKWkoDK4MkSoByBAGJQJLAwAeAWABQIUH0HDSoiTLKUaoUggAW+DHorUsAOlABJcQlhUy4KpACeoLJzrI8cCwMGxU1ABVPIiwhESpMZEJQTmR4lxFQaQxWMm4IZABbIlIYKlJkTlDlXHgkNFAAbxVQTIAjfABrAEEC5FZOeIBeUAAGAG5mmSw8WAroSFIqb2GAIjMiIk8VieVJ8Ar01ncAgAoASkaAXxVr3dUwGoQAYWpMHBgCYn1rekZmNg4eUi0Vi2icoBWJCsNBWoA6WE8AHcAiEwmBgTEtDovtDaMZQLM6PEoQZbA5wSk0q5SO4vD4-AEghZoJwLGYEIRwNBoqAzFRwCZCFUIlFMXECdSiAhId8YZgclx0PsiiVqOVOAAaUAFLAsxWgKiC35MFigfC0FKgSAVVDTSyk+W5dB4fplHVVR6gF7xJrKFotEk-HXIRE9PoDUDDcaTAPTWaceaLZYQlmoPBbHYx-KcQ7HPDnK43FQqfY5+IMDDISPJLCIuqoc47UsuUCofAME3Vzi1r3URvF5QV5A2STtPDdXqunZDgDaYlHnTDrrEAF0dm28B3mDZg6HJwN1+2-hg57ulwNV2NQGoZbjYfNrYiENBwEFaojFiZQK08C-4fFKTVCozWfTgfFgLkeT5AUqiAA).

Isso significa que construções do ambiente de execução do JavaScript, como `in` ou a simples busca de propriedade, ainda podem acessar um membro `private` ou `protected`:

```ts twoslash
class MySafe {
  private secretKey = 12345;
}
```

```js
// In a JavaScript file...
const s = new MySafe();
// Will print 12345
console.log(s.secretKey);
```

`private` também permite acesso por notação de colchetes durante a verificação de tipos. Isso torna os campos declarados como `private` potencialmente mais fáceis de acessar para coisas como testes unitários, com a desvantagem de que esses campos são _privados flexíveis_ e não impõem privacidade de forma estrita.

```ts twoslash
// @errors: 2341
class MySafe {
  private secretKey = 12345;
}

const s = new MySafe();

// Not allowed during type checking
console.log(s.secretKey);

// OK
console.log(s["secretKey"]);
```

Diferentemente do `private` do TypeScript, os [campos privados](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes/Private_class_fields) do JavaScript (`#`) continuam privados após a compilação e não oferecem as saídas mencionadas anteriormente, como o acesso por notação de colchetes, por isso são _privados rígidos_.

```ts twoslash
class Dog {
  #barkAmount = 0;
  personality = "happy";

  constructor() {}
}
```

```ts twoslash
// @target: esnext
// @showEmit
class Dog {
  #barkAmount = 0;
  personality = "happy";

  constructor() {}
}
```

Ao compilar para ES2021 ou inferior, o TypeScript usará WeakMaps no lugar de `#`.

```ts twoslash
// @target: es2015
// @showEmit
class Dog {
  #barkAmount = 0;
  personality = "happy";

  constructor() {}
}
```

Se você precisar proteger valores da sua classe contra agentes mal-intencionados, deve usar mecanismos que ofereçam privacidade rígida em tempo de execução, como closures, WeakMaps ou campos privados. Observe que essas verificações de privacidade adicionais em tempo de execução podem afetar o desempenho.

## Membros estáticos {#static-members}

<blockquote class='bg-reading'>
   <p>Leitura de apoio:<br />
   <a href='https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes/static'>Membros estáticos (MDN)</a><br/>
   </p>
</blockquote>

Classes podem ter membros `static`.
Esses membros não estão associados a uma instância específica da classe.
Eles podem ser acessados pelo próprio objeto construtor da classe:

```ts twoslash
class MyClass {
  static x = 0;
  static printX() {
    console.log(MyClass.x);
  }
}
console.log(MyClass.x);
MyClass.printX();
```

Membros estáticos também podem usar os mesmos modificadores de visibilidade `public`, `protected` e `private`:

```ts twoslash
// @errors: 2341
class MyClass {
  private static x = 0;
}
console.log(MyClass.x);
```

Membros estáticos também são herdados:

```ts twoslash
class Base {
  static getGreeting() {
    return "Hello world";
  }
}
class Derived extends Base {
  myGreeting = Derived.getGreeting();
}
```

### Nomes estáticos especiais {#special-static-names}

Em geral, não é seguro/possível sobrescrever propriedades do protótipo `Function`.
Como as próprias classes são funções que podem ser invocadas com `new`, certos nomes `static` não podem ser usados.
Propriedades de função como `name`, `length` e `call` não são válidas para definir como membros `static`:

```ts twoslash
// @errors: 2699
class S {
  static name = "S!";
}
```

### Por que não existem classes estáticas? {#why-no-static-classes}

O TypeScript (e o JavaScript) não têm um construto chamado `static class`, como o que existe em C#, por exemplo.

Esses construtos _só_ existem porque essas linguagens obrigam todos os dados e funções a ficarem dentro de uma classe; como essa restrição não existe no TypeScript, não há necessidade deles.
Uma classe com apenas uma instância normalmente é representada simplesmente como um _objeto_ normal em JavaScript/TypeScript.

Por exemplo, não precisamos de uma sintaxe de "classe estática" no TypeScript, porque um objeto comum (ou até mesmo uma função de nível superior) faz o mesmo trabalho tão bem:

```ts twoslash
// Unnecessary "static" class
class MyStaticClass {
  static doSomething() {}
}

// Preferred (alternative 1)
function doSomething() {}

// Preferred (alternative 2)
const MyHelperObject = {
  dosomething() {},
};
```

## Blocos `static` em classes {#static-blocks-in-classes}

Blocos estáticos permitem escrever uma sequência de instruções com escopo próprio, que pode acessar campos privados da classe que os contém. Isso significa que podemos escrever código de inicialização com todos os recursos de instruções, sem vazamento de variáveis e com acesso total aos internos da nossa classe.

```ts twoslash
declare function loadLastInstances(): any[]
// ---cut---
class Foo {
    static #count = 0;

    get count() {
        return Foo.#count;
    }

    static {
        try {
            const lastInstances = loadLastInstances();
            Foo.#count += lastInstances.length;
        }
        catch {}
    }
}
```

## Classes genéricas {#generic-classes}

Classes, assim como interfaces, podem ser genéricas.
Quando uma classe genérica é instanciada com `new`, seus parâmetros de tipo são inferidos da mesma forma que em uma chamada de função:

```ts twoslash
class Box<Type> {
  contents: Type;
  constructor(value: Type) {
    this.contents = value;
  }
}

const b = new Box("hello!");
//    ^?
```

Classes podem usar restrições e valores padrão de genéricos da mesma forma que interfaces.

### Parâmetros de tipo em membros estáticos {#type-parameters-in-static-members}

Este código não é válido, e pode não ser óbvio o motivo:

```ts twoslash
// @errors: 2302
class Box<Type> {
  static defaultValue: Type;
}
```

Lembre-se de que tipos são sempre totalmente apagados!
Em tempo de execução, existe apenas _um_ espaço de propriedade `Box.defaultValue`.
Isso significa que definir `Box<string>.defaultValue` (se isso fosse possível) _também_ alteraria `Box<number>.defaultValue` - não é bom.
Os membros `static` de uma classe genérica nunca podem se referir aos parâmetros de tipo da classe.

## `this` em tempo de execução nas classes {#this-at-runtime-in-classes}

<blockquote class='bg-reading'>
   <p>Leitura de apoio:<br />
   <a href='https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/this'>Palavra-chave this (MDN)</a><br/>
   </p>
</blockquote>

É importante lembrar que o TypeScript não altera o comportamento em tempo de execução do JavaScript, e que o JavaScript é conhecido por ter alguns comportamentos peculiares em tempo de execução.

O tratamento de `this` no JavaScript é de fato incomum:

```ts twoslash
class MyClass {
  name = "MyClass";
  getName() {
    return this.name;
  }
}
const c = new MyClass();
const obj = {
  name: "obj",
  getName: c.getName,
};

// Prints "obj", not "MyClass"
console.log(obj.getName());
```

Resumindo, por padrão, o valor de `this` dentro de uma função depende de _como a função foi chamada_.
Neste exemplo, como a função foi chamada pela referência `obj`, seu valor de `this` foi `obj` em vez da instância da classe.

Isso raramente é o que se deseja!
O TypeScript oferece algumas formas de mitigar ou prevenir esse tipo de erro.

### Funções arrow {#arrow-functions}

<blockquote class='bg-reading'>
   <p>Leitura de apoio:<br />
   <a href='https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions'>Funções arrow (MDN)</a><br/>
   </p>
</blockquote>

Se você tem uma função que frequentemente será chamada de um jeito que perde o seu contexto de `this`, pode fazer sentido usar uma propriedade de função arrow em vez de uma definição de método:

```ts twoslash
class MyClass {
  name = "MyClass";
  getName = () => {
    return this.name;
  };
}
const c = new MyClass();
const g = c.getName;
// Prints "MyClass" instead of crashing
console.log(g());
```

Isso tem algumas compensações:

- O valor de `this` é garantido como correto em tempo de execução, mesmo para código não verificado pelo TypeScript
- Isso usará mais memória, porque cada instância da classe terá sua própria cópia de cada função definida dessa forma
- Você não pode usar `super.getName` em uma classe derivada, porque não há entrada na cadeia de protótipos de onde buscar o método da classe base

### Parâmetros `this` {#this-parameters}

Em uma definição de método ou função, um parâmetro inicial chamado `this` tem um significado especial no TypeScript.
Esses parâmetros são apagados durante a compilação:

```ts twoslash
type SomeType = any;
// ---cut---
// TypeScript input with 'this' parameter
function fn(this: SomeType, x: number) {
  /* ... */
}
```

```js
// JavaScript output
function fn(x) {
  /* ... */
}
```

O TypeScript verifica se a chamada de uma função com parâmetro `this` é feita com o contexto correto.
Em vez de usar uma função arrow, podemos adicionar um parâmetro `this` às definições de método para garantir estaticamente que o método é chamado corretamente:

```ts twoslash
// @errors: 2684
class MyClass {
  name = "MyClass";
  getName(this: MyClass) {
    return this.name;
  }
}
const c = new MyClass();
// OK
c.getName();

// Error, would crash
const g = c.getName;
console.log(g());
```

Este método tem as compensações opostas à abordagem da função arrow:

- Chamadores JavaScript ainda podem usar o método da classe de forma incorreta sem perceber
- Apenas uma função por definição de classe é alocada, em vez de uma por instância da classe
- Definições de métodos da base ainda podem ser chamadas via `super`.

## Tipos `this` {#this-types}

Em classes, um tipo especial chamado `this` se refere _dinamicamente_ ao tipo da classe atual.
Vamos ver como isso é útil:

<!-- prettier-ignore -->
```ts twoslash
class Box {
  contents: string = "";
  set(value: string) {
//  ^?
    this.contents = value;
    return this;
  }
}
```

Aqui, o TypeScript inferiu o tipo de retorno de `set` como `this`, em vez de `Box`.
Agora vamos criar uma subclasse de `Box`:

```ts twoslash
class Box {
  contents: string = "";
  set(value: string) {
    this.contents = value;
    return this;
  }
}
// ---cut---
class ClearableBox extends Box {
  clear() {
    this.contents = "";
  }
}

const a = new ClearableBox();
const b = a.set("hello");
//    ^?
```

Você também pode usar `this` em uma anotação de tipo de parâmetro:

```ts twoslash
class Box {
  content: string = "";
  sameAs(other: this) {
    return other.content === this.content;
  }
}
```

Isso é diferente de escrever `other: Box` -- se você tiver uma classe derivada, seu método `sameAs` passará a aceitar apenas outras instâncias dessa mesma classe derivada:

```ts twoslash
// @errors: 2345
class Box {
  content: string = "";
  sameAs(other: this) {
    return other.content === this.content;
  }
}

class DerivedBox extends Box {
  otherContent: string = "?";
}

const base = new Box();
const derived = new DerivedBox();
derived.sameAs(base);
```

### Type guards baseados em `this` {#this-based-type-guards}

Você pode usar `this is Type` na posição de retorno de métodos em classes e interfaces.
Quando combinado com um estreitamento de tipo (por exemplo, instruções `if`), o tipo do objeto alvo será estreitado para o `Type` especificado.

<!-- prettier-ignore -->
```ts twoslash
// @strictPropertyInitialization: false
class FileSystemObject {
  isFile(): this is FileRep {
    return this instanceof FileRep;
  }
  isDirectory(): this is Directory {
    return this instanceof Directory;
  }
  isNetworked(): this is Networked & this {
    return this.networked;
  }
  constructor(public path: string, private networked: boolean) {}
}

class FileRep extends FileSystemObject {
  constructor(path: string, public content: string) {
    super(path, false);
  }
}

class Directory extends FileSystemObject {
  children: FileSystemObject[];
}

interface Networked {
  host: string;
}

const fso: FileSystemObject = new FileRep("foo/bar.txt", "foo");

if (fso.isFile()) {
  fso.content;
// ^?
} else if (fso.isDirectory()) {
  fso.children;
// ^?
} else if (fso.isNetworked()) {
  fso.host;
// ^?
}
```

Um caso de uso comum para um type guard baseado em `this` é permitir a validação preguiçosa de um campo específico. Por exemplo, este caso remove um `undefined` do valor guardado dentro de `box` quando `hasValue` foi verificado como verdadeiro:

```ts twoslash
class Box<T> {
  value?: T;

  hasValue(): this is { value: T } {
    return this.value !== undefined;
  }
}

const box = new Box<string>();
box.value = "Gameboy";

box.value;
//  ^?

if (box.hasValue()) {
  box.value;
  //  ^?
}
```

## Propriedades de parâmetro {#parameter-properties}

O TypeScript oferece uma sintaxe especial para transformar um parâmetro do construtor em uma propriedade de classe com o mesmo nome e valor.
Essas são chamadas de _propriedades de parâmetro_ e são criadas prefixando um argumento do construtor com um dos modificadores de visibilidade `public`, `private`, `protected` ou `readonly`.
O campo resultante recebe esse(s) modificador(es):

```ts twoslash
// @errors: 2341
class Params {
  constructor(
    public readonly x: number,
    protected y: number,
    private z: number
  ) {
    // No body necessary
  }
}
const a = new Params(1, 2, 3);
console.log(a.x);
//            ^?
console.log(a.z);
```

## Expressões de classe {#class-expressions}

<blockquote class='bg-reading'>
   <p>Leitura de apoio:<br />
   <a href='https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/class'>Expressões de classe (MDN)</a><br/>
   </p>
</blockquote>

Expressões de classe são muito parecidas com declarações de classe.
A única diferença real é que expressões de classe não precisam de nome, embora possamos nos referir a elas pelo identificador ao qual foram associadas:

```ts twoslash
const someClass = class<Type> {
  content: Type;
  constructor(value: Type) {
    this.content = value;
  }
};

const m = new someClass("Hello, world");
//    ^?
```

## Assinaturas de construtor {#constructor-signatures}

Classes em JavaScript são instanciadas com o operador `new`. Dado o tipo da própria classe, o tipo utilitário [InstanceType](/docs/handbook/utility-types.html#instancetypetype) modela essa operação.

```ts twoslash
class Point {
  createdAt: number;
  x: number;
  y: number
  constructor(x: number, y: number) {
    this.createdAt = Date.now()
    this.x = x;
    this.y = y;
  }
}
type PointInstance = InstanceType<typeof Point>

function moveRight(point: PointInstance) {
  point.x += 5;
}

const point = new Point(3, 4);
moveRight(point);
point.x; // => 8
```

## Classes e membros `abstract` {#abstract-classes-and-members}

Classes, métodos e campos no TypeScript podem ser _abstract_.

Um _método abstrato_ ou _campo abstrato_ é aquele que não teve uma implementação fornecida.
Esses membros devem existir dentro de uma _classe abstrata_, que não pode ser instanciada diretamente.

O papel das classes abstratas é servir como classe base para subclasses que implementam todos os membros abstratos.
Quando uma classe não tem membros abstratos, diz-se que ela é _concreta_.

Vamos ver um exemplo:

```ts twoslash
// @errors: 2511
abstract class Base {
  abstract getName(): string;

  printName() {
    console.log("Hello, " + this.getName());
  }
}

const b = new Base();
```

Não podemos instanciar `Base` com `new` porque ela é abstrata.
Em vez disso, precisamos criar uma classe derivada e implementar os membros abstratos:

```ts twoslash
abstract class Base {
  abstract getName(): string;
  printName() {}
}
// ---cut---
class Derived extends Base {
  getName() {
    return "world";
  }
}

const d = new Derived();
d.printName();
```

Observe que, se esquecermos de implementar os membros abstratos da classe base, receberemos um erro:

```ts twoslash
// @errors: 2515
abstract class Base {
  abstract getName(): string;
  printName() {}
}
// ---cut---
class Derived extends Base {
  // forgot to do anything
}
```

### Assinaturas de construtor abstratas {#abstract-construct-signatures}

Às vezes você quer aceitar alguma função construtora de classe que produza uma instância de uma classe derivada de alguma classe abstrata.

Por exemplo, você pode querer escrever este código:

```ts twoslash
// @errors: 2511
abstract class Base {
  abstract getName(): string;
  printName() {}
}
class Derived extends Base {
  getName() {
    return "";
  }
}
// ---cut---
function greet(ctor: typeof Base) {
  const instance = new ctor();
  instance.printName();
}
```

O TypeScript está corretamente avisando que você está tentando instanciar uma classe abstrata.
Afinal, dada a definição de `greet`, é perfeitamente válido escrever este código, que acabaria construindo uma classe abstrata:

```ts twoslash
declare const greet: any, Base: any;
// ---cut---
// Bad!
greet(Base);
```

Em vez disso, você quer escrever uma função que aceite algo com uma assinatura de construtor:

```ts twoslash
// @errors: 2345
abstract class Base {
  abstract getName(): string;
  printName() {}
}
class Derived extends Base {
  getName() {
    return "";
  }
}
// ---cut---
function greet(ctor: new () => Base) {
  const instance = new ctor();
  instance.printName();
}
greet(Derived);
greet(Base);
```

Agora o TypeScript informa corretamente quais funções construtoras de classe podem ser invocadas - `Derived` pode, porque é concreta, mas `Base` não pode.

## Relações entre classes {#relationships-between-classes}

Na maioria dos casos, classes no TypeScript são comparadas de forma estrutural, como qualquer outro tipo.

Por exemplo, estas duas classes podem ser usadas no lugar uma da outra porque são idênticas:

```ts twoslash
class Point1 {
  x = 0;
  y = 0;
}

class Point2 {
  x = 0;
  y = 0;
}

// OK
const p: Point1 = new Point2();
```

Da mesma forma, relações de subtipo entre classes existem mesmo sem herança explícita:

```ts twoslash
// @strict: false
class Person {
  name: string;
  age: number;
}

class Employee {
  name: string;
  age: number;
  salary: number;
}

// OK
const p: Person = new Employee();
```

Isso parece simples, mas há alguns casos que parecem mais estranhos do que outros.

Classes vazias não têm membros.
Em um sistema de tipos estrutural, um tipo sem membros é geralmente um supertipo de qualquer outro.
Então, se você escrever uma classe vazia (não faça isso!), qualquer coisa pode ser usada no lugar dela:

```ts twoslash
class Empty {}

function fn(x: Empty) {
  // can't do anything with 'x', so I won't
}

// All OK!
fn(window);
fn({});
fn(fn);
```
