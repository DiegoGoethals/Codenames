class Game {

    constructor() {

        setInterval(function(){this.status()}.bind(this), 1000);

        document.getElementById("create").onclick = function () {
            this.start();
        }.bind(this);

        document.getElementById("letter").onsubmit = function() {
            this.guess();
        }.bind(this);
    }

    start() {

        let data = {
            "word": document.getElementById("wordToGuess").value
        };

        // Gets all properties from server to start a game
        fetch("cgi-bin/create_game.cgi?data=" + +JSON.stringify(data)).then(resp => resp.json())
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

    guess() {

        let data = {
            "letter": document.getElementById("letter").value
        };

        fetch("cgi-bin/guess.cgi?data=" + JSON.stringify(data)).then(resp => resp.json())
            .then(data => {
               this.progress = data["progress"];
               this.mistakes_left = data["mistakes*left"];
               this.selected = data["selected"];
               this.winner = data["winner"];
            });
    }

    // Returns the current status of the game
    status() {

        let data = {
            "code": this.code
        };

        fetch("cgi-bin/current_state.cgi?data=" + JSON.stringify(data)).then(resp => resp.json())
            .then(data => {
                this.winner = data["winner"];
                this.selected = data["selected"];
                this.progress = data["progress"];
                this.mistakes_left = data["mistakes_left"];
            });


    }
}