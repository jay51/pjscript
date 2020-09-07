

function loop(){
    /* var i = 0;
    for(;;){
        log("yes");
    };
     */
    var person = {
        name: "jack",
        age: {
            born: 23,
            died: 28
        }
    };

    log(person.name);
    log(person.age.born);
    return;
};

loop();
