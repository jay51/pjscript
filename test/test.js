

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
        },
        features: {
            hair: {
                curly: [1, 2, 3],
                notcurly: 0
            }
        }

    };

    log(person.features.hair.curly[1]);
    return;
};

loop();
