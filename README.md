A single file, dependency free language written in python. The goal of this project is to show that
programming languages are not a black box and that you could learn the basic concpets required to implement your own language.
While this language is not a real programming language however a lot of the internal concepts displayed in this
language is taken from other real programming languages.

### Basic statemnets
```js
/* this is a comment */
var age = 2;
var name = "jack";
var newage = age;
name = "jack and me";
log(1, "it's working fuck yea", name);
var x = add(age, add(2,3));
log(x);
```



### Functions and Scope

```js
var x = "hello world";

function printme(st1, st2, st3){
    log(st1);
    log(st2);
    log(st3);
};

function testfunc(){
    var x = "new thing";
    printme(x, 1, 3);
};

testfunc();
log(x);
```

### Expressions
```js
var x = 0 + add(2, 3);
var x = x + add(2, 3);
var x = (x * 2) / 2;
log(x); /* should log 10*/

function Mul(){
    return add(2, add(2 * 3, 2));
};

var result = Mul();
log(result);


/* post-increment and decrement */
var x = 2;
log("x: ", x);

var y = x++ * 2;
log("y: ", y); /* output y: 4 */
log("x: ", x); /* output y: 3 */

/* pre-increment and decrement */
var x = 2;
log("x: ", x);

var y = ++x * 2;
log("y: ", y);/* output y: 6 */
log("x: ", x);/* output y: 3 */


/* Comparison Operators */

var x = 2;
var y = x >= 2;
log("y: ", y); /* True */
log("x: ", x); /* 2 */
```

### For Loops

```js
for(var i = 0; i < 5; i++){
    log(i);
};

/* or */
var i = 0;
for(i = 2; i < 5; i++){
    log(i);
};

/* infinite loop */
var i = 0;
for(; ; i++){
    log(i);
};
```
