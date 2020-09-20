function loop(){

    var person = {
        age: { born: 23, died: 28 },
        features: {
            hair: { curly: [1, 2, 3], notcurly: 0 }
        },

        printname: function(){
            log("printname inside object person");
            return "working fine";
        }
    };

    log(person.features.hair.curly[1]);
    log(person.printname());
    return;
};

loop();
