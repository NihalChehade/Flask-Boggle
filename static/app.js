
class BoggleGame {
    constructor() {
        this.totalSeconds = 60; // game length
        this.score = 0;
        this.foundWords = [];
        this.timer = setInterval(this.decrementSeconds.bind(this), 1000);

        $('#guess-form').on("submit", this.checkGuessed.bind(this));
    }

    decrementSeconds() {
        this.totalSeconds -= 1;
        $('#guessed').focus();
        if (this.totalSeconds === 0) {
            $('#guess-form').hide();
            clearInterval(this.timer);
            this.endGame(this.score);
        }

        $('#secLeft').text("You have " + this.totalSeconds + " seconds left!!");

    }

    async checkGuessed(e) {
        e.preventDefault();

        const guessedWord = $('#guessed').val();


        const in_foundWords = this.foundWords.find(function (word) {
            return guessedWord === word;
        });

        if (!in_foundWords) {
            const res = await axios.get("/check-guessed", { params: { word: guessedWord } });

            if (res.data.result === "ok") {
                this.score += guessedWord.length;
                this.foundWords.push(guessedWord);
                $('#score-div').text('Your score is: ' + this.score)
                $('#msg').text("well done! The word is valid and exist!")
            } else if (res.data.result === "not-on-board") {
                $('#msg').text("The word is invalid, does not exist on board! ")
            } else {
                $('#msg').text("The word does not exist at all.. Try again!")
            }
        } else {
            $('#msg').text("You already found " + guessedWord);
        }

        $('#guessed').val('');
        $('#guessed').focus();
    }

    async endGame(score) {
        const res = await axios.post('/ending-game', { 'score': score });
        if (res.data.brokeRecord) {
            $('#msg').text("Horray!! You Hit A New high Score Of: " + score)
        } else {
            $('#msg').text("Your scored: " + score)
        }

    }
}
let game = new BoggleGame();
