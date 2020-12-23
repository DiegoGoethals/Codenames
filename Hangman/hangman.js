class Game{

    constructor() {

        this.start();
    }

    start() {

        let data = {
            "word": document.getElementById("wordToGuess").value
        };

        // Gets all properties from server to start a game
        fetch("cgi-bin/create_game.cgi?data=" +  + JSON.stringify(data)).then(resp => resp.json())
            .then(data => {

                this.word = data["word"];
                this.code = data["code"];
                this.winner = data["winner"];
                this.selected = data["selected"];
                this.progress = data["progress"];
                this.mistakes_left = data["mistakes_left"];
            });

        document.getElementById("word").innerText = this.word;
    }


}