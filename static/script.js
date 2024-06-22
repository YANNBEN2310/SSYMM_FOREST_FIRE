document.addEventListener('DOMContentLoaded', () => {
    const forestDiv = document.getElementById('forest');
    const statsDiv = document.getElementById('statistics');
    let interval;
    let isRunning = false;

    document.getElementById('initialize').addEventListener('click', () => {
        const rows = document.getElementById('rows').value;
        const cols = document.getElementById('cols').value;
        const prob = document.getElementById('prob').value;
        const prob_empty = document.getElementById('prob_empty').value;
        initializeForest(rows, cols, prob, prob_empty);
    });

    document.getElementById('play').addEventListener('click', () => {
        if (!isRunning) {
            isRunning = true;
            interval = setInterval(updateForest, 500);
        }
    });

    document.getElementById('pause').addEventListener('click', () => {
        if (isRunning) {
            isRunning = false;
            clearInterval(interval);
        }
    });

    document.getElementById('reset').addEventListener('click', () => {
        clearInterval(interval);
        forestDiv.innerHTML = '';
        statsDiv.innerHTML = '';
        isRunning = false;
    });

    function initializeForest(rows, cols, prob, prob_empty) {
        fetch('/initialize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ rows, cols, prob_tree: prob, prob_empty: prob_empty })
        })
        .then(response => response.json())
        .then(data => {
            renderForest(data, rows, cols);
            updateStatistics();
        });
    }

    function updateForest() {
        fetch('/update', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            const rows = document.getElementById('rows').value;
            const cols = document.getElementById('cols').value;
            renderForest(data, rows, cols);
            updateStatistics();
        });
    }

    function renderForest(grid, rows, cols) {
        forestDiv.innerHTML = '';
        forestDiv.style.gridTemplateRows = `repeat(${rows}, 20px)`;
        forestDiv.style.gridTemplateColumns = `repeat(${cols}, 20px)`;
        grid.forEach(row => {
            row.forEach(cell => {
                const cellDiv = document.createElement('div');
                cellDiv.classList.add('cell');
                switch(cell) {
                    case 0:
                        cellDiv.classList.add('empty');
                        break;
                    case 1:
                        cellDiv.classList.add('healthy');
                        break;
                    case 2:
                        cellDiv.classList.add('burning');
                        break;
                    case 3:
                        cellDiv.classList.add('burnt');
                        break;
                }
                forestDiv.appendChild(cellDiv);
            });
        });
    }

    function updateStatistics() {
        fetch('/statistics', {
            method: 'GET'
        })
        .then(response => response.json())
        .then(data => {
            statsDiv.innerHTML = `
                <p>Total Trees: ${data.total_trees}</p>
                <p>Surface: ${data.surface} cells</p>
                <p>Burnt Trees: ${data.burnt_trees}</p>
                <p>Damage Percentage: ${data.damage_percentage.toFixed(2)}%</p>
            `;
        });
    }
});
