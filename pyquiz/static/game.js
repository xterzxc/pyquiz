document.addEventListener("DOMContentLoaded", () => {
    const roomNameElement = document.getElementById('room-name');
    const roomName = roomNameElement.getAttribute('data-room-name');
    const playerName = new URLSearchParams(window.location.search).get('player');

    const socket = new WebSocket(`ws://${window.location.host}/ws/game/${roomName}/`);

    socket.onopen = function(e) {
        socket.send(JSON.stringify({
            'type': 'join_room',
            'player_name': playerName
        }));
    };

    socket.onmessage = function(e) {
        const data = JSON.parse(e.data);

        if (data.type === 'update_players') {
            const playersList = document.getElementById('players-list');
            playersList.innerHTML = '';
            data.players.forEach(player => {
                const li = document.createElement('li');
                li.textContent = player;
                playersList.appendChild(li);
            });

        } else if (data.type === 'new_question') {
            document.getElementById('question-container').style.display = 'block';
            document.getElementById('results-container').style.display = 'none';
            document.getElementById('question-text').innerText = data.text;
        } else if (data.type === 'answer_result') {
            document.getElementById('question-container').style.display = 'none';
            document.getElementById('results-container').style.display = 'block';
            document.getElementById('result-message').innerText = data.correct ? 'Correct!' : 'Incorrect!';
            console.log('answered');
        } else if (data.type === 'game_started') {
            document.getElementById('lobby-container').style.display = 'none';
            document.getElementById('question-container').style.display = 'block';
            document.getElementById('results-container').style.display = 'block';
        }
    };

    document.getElementById('submit-answer').onclick = function() {
        const code = document.getElementById('answer-code').value;
        socket.send(JSON.stringify({
            'type': 'submit_answer',
            'player_name': playerName,
            'code': code,
            'question_id': 1
        }));
    };

    document.getElementById('start-game').onclick = function() {
        socket.send(JSON.stringify({
            'type': 'start_game',
            'player_name': playerName
        }));
    };
});
