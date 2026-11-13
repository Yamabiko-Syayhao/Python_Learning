abstract class Animal {
    abstract makeSound():void;
}

class Cat extends Animal{
        makeSound(): void {
            console.log("mew~\n");                
        }
}
class Dog extends Animal{
    makeSound(): void {
        throw new Error("Method not implemented.");
    }
    "text":string;
    "walk":void;
    "bark":void;
}

var cat1 = new Cat
let cat2 = new Cat
let dog1 = new Dog
cat1.makeSound()
cat2.makeSound()
dog1.text = "bark!!"
console.log(dog1.text)


