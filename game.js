class Game {

    constructor() {

        // Automatically updates the game every 0.8 second
        setInterval(function(){this.status()}.bind(this), 800);

        document.getElementById("spymaster").addEventListener("change", this.setTeamLeader.bind(this));

        document.getElementById("connect").addEventListener("click", this.connect.bind(this));

        document.getElementById("create").addEventListener("click", this.start.bind(this));

        document.getElementById("end_turn").addEventListener("click", this.end_turn.bind(this));
    }

    // Fills the board so the game can be played
    fill_board(data) {
        this.words = data["words"];
        this.red = data["red_team"];
        this.blue = data["blue_team"];
        this.neutral = data["neutral"];
        this.assassin = data["assassin"];
        this.code = data["code"];
        this.current_player = data["current_player"];
        this.winner = data["winner"];
        this.selected = data["selected"];

        // Shows code on screen so people can use it to join the game
        document.getElementById("code").innerHTML = `Share this code: ${this.code}`;

        // Shows current player on screen
        this.showCurrentPlayer();

        // Places words on the game board
        const board = this.words;

        document.getElementById("board").innerHTML = board.map(word => `<div class="word">${word}</div>`).join("");

        // Makes all words clickable
        document.querySelectorAll(".word").forEach(word => 
            word.addEventListener("click", this.move.bind(this))
        );
    }

    // Adds word to selected words and shows the color of the word on the board
    selectWord(word) {
        word.classList.add("selected");
        if (this.blue.includes(word.innerText)) {
            word.style.cssText = "background-color: blue";
        } else if (this.red.includes(word.innerText)) {
            word.style.cssText = "background-color: red";
        } else if(this.neutral.includes(word.innerText)) {
            word.style.cssText = "background-color: navajowhite;"
        }
    }

    start() {

        // Gets all properties from server to start a game
        fetch("cgi-bin/create_game.cgi?data=").then(resp => resp.json())
            .then(data => {
                this.fill_board(data);

                const checkbox = document.getElementById("spymaster");

                if (checkbox.checked) {
                    checkbox.checked = false;
                    checkbox.disabled = false;
                }
            });
    }

    // Makes it possible to join another game
    connect() {

        let data = {
            "code": document.getElementById("code2connect").value
        };

        fetch(`cgi-bin/current_state.cgi?data=${JSON.stringify(data)}`).then(resp => resp.json())
            .then(data => {
                this.fill_board(data);

                document.querySelectorAll(".word")
                    .forEach(word => {
                        if (this.selected.includes(word.innerHTML)) {
                            this.selectWord(word);
                        }
                    });
            });
    }

    setWinner(winner) {
        if (winner) {
            alert(`Congratulations ${winner} you won the game!`);
            this.start();
        } else {
            this.showCurrentPlayer();
        }
    }

    showCurrentPlayer() {
        const element = document.getElementById("player");
        element.innerHTML = `Current player: ${this.current_player}`;
        if (this.current_player === "red") {
            element.style.cssText = "color: red;";
        } else {
            element.style.cssText = "color: blue;";
        }
    }

    // Makes it possible to select words
    move(event) {

        const word = event.target;
        const text = word.innerText;

        if (word.classList.contains("spymaster") || word.classList.contains("selected")) {
            return;
        }

        let data = {
            "word": text,
            "words": this.words,
            "red": this.red,
            "blue": this.blue,
            "selected": this.selected,
            "assassin": this.assassin,
            "neutral": this.neutral,
            "current_player": this.current_player,
            "code": this.code
        };

        // Gets all properties needed to make a move from server and than makes a move
        fetch(`cgi-bin/move.cgi?data=${JSON.stringify(data)}`).then(resp => resp.json())
            .then(data => {
                this.selected = data["selected"];
                this.current_player = data["current_player"];
                this.winner = data["winner"];

                this.setWinner(this.winner);
            });

        this.selectWord(word);
    }

    // Makes it possible to end the turn for the current player
    end_turn() {

        const checkbox = document.getElementById("spymaster");

        if (checkbox.checked) {
            return;
        }

        let data = {
            "words": this.words,
            "red": this.red,
            "blue": this.blue,
            "selected": this.selected,
            "assassin": this.assassin,
            "neutral": this.neutral,
            "current_player": this.current_player,
            "code": this.code
        };

        // Gets data from server so the turn can be ended and ends turn
        fetch(`cgi-bin/end_turn.cgi?data=${JSON.stringify(data)}`).then(resp => resp.json())
            .then(data => {
                this.current_player = data["current_player"];

                this.showCurrentPlayer();
            });
    }

    // Makes it possible to make you the spymaster
    setTeamLeader(event) {

        const checkbox = event.target;
        if (checkbox.checked) {

            document
                .querySelectorAll(".word")
                .forEach(word => {
                    word.classList.add("spymaster");
                    if (this.blue.includes(word.innerText)) {
                        word.style.cssText = "background-color: blue;";
                    } else if (this.red.includes(word.innerText)) {
                        word.style.cssText = "background-color: red;";
                    } else if(this.neutral.includes(word.innerText)) {
                        word.style.cssText = "background-color: navajowhite;";
                    }
                });
            checkbox.disabled = true;
        }
    }

    // Returns the current status of the game
    status() {

        let data = {
            "code": this.code
        };

        fetch(`cgi-bin/current_state.cgi?data=${JSON.stringify(data)}`).then(resp => resp.json())
            .then(data => {
                this.winner = data["winner"];
                this.selected = data["selected"];
                this.current_player = data["current_player"];

                this.setWinner(this.winner);

                this.showCurrentPlayer();

                document.querySelectorAll(".word")
                    .forEach(word => {
                        if (this.selected.includes(word.innerText)) {
                            this.selectWord(word);
                        }

                        if (word.classList.contains("selected") && word.classList.contains("spymaster")) {
                            if (this.blue.includes(word.innerText)) {
                                word.style.cssText = "background-color: blue; text-decoration: line-through;";
                            } else if (this.red.includes(word.innerText)) {
                                word.style.cssText = "background-color: red; text-decoration: line-through;";
                            } else if(this.neutral.includes(word.innerText)) {
                                word.style.cssText = "background-color: navajowhite; text-decoration: line-through;"
                            }
                        }
                    });
            });
    }
}