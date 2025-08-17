class Minesweeper {
    constructor(rows = 10, cols = 10, mines = 10) {
        this.rows = rows;
        this.cols = cols;
        this.mines = mines;
        this.flagsLeft = mines;
        this.time = 0;
        this.timer = null;
        this.gameOver = false;
        this.firstClick = true;
        this.board = [];
        this.revealed = [];
        this.flagged = [];
        this.minePositions = [];
        
        this.boardElement = document.getElementById('board');
        this.flagsElement = document.getElementById('flags-left');
        this.timeElement = document.getElementById('time');
        this.messageElement = document.getElementById('message');
        
        this.setupEventListeners();
        this.initializeGame();
    }
    
    initializeGame() {
        // Reset game state
        this.board = Array(this.rows).fill().map(() => Array(this.cols).fill(0));
        this.revealed = Array(this.rows).fill().map(() => Array(this.cols).fill(false));
        this.flagged = Array(this.rows).fill().map(() => Array(this.cols).fill(false));
        this.minePositions = [];
        this.flagsLeft = this.mines;
        this.time = 0;
        this.gameOver = false;
        this.firstClick = true;
        
        // Clear timer if running
        if (this.timer) {
            clearInterval(this.timer);
            this.timer = null;
        }
        
        // Update UI
        this.updateFlagsDisplay();
        this.timeElement.textContent = '0';
        this.messageElement.textContent = '';
        this.messageElement.className = 'game-message';
        
        // Create board
        this.createBoard();
    }
    
    createBoard() {
        // Clear the board
        this.boardElement.innerHTML = '';
        this.boardElement.style.gridTemplateColumns = `repeat(${this.cols}, 1fr)`;
        
        // Create cells
        for (let r = 0; r < this.rows; r++) {
            for (let c = 0; c < this.cols; c++) {
                const cell = document.createElement('div');
                cell.className = 'cell';
                cell.dataset.row = r;
                cell.dataset.col = c;
                
                // Add event listeners
                cell.addEventListener('click', () => this.handleLeftClick(r, c));
                cell.addEventListener('contextmenu', (e) => {
                    e.preventDefault();
                    this.handleRightClick(r, c);
                });
                
                // Prevent text selection and drag
                cell.addEventListener('mousedown', (e) => {
                    if (e.button === 0 || e.button === 2) {
                        e.preventDefault();
                    }
                });
                
                this.boardElement.appendChild(cell);
            }
        }
    }
    
    placeMines(firstClickRow, firstClickCol) {
        // Create array of all possible positions
        const positions = [];
        for (let r = 0; r < this.rows; r++) {
            for (let c = 0; c < this.cols; c++) {
                // Don't place a mine on the first click or adjacent to it
                const isFirstClickAdjacent = 
                    Math.abs(r - firstClickRow) <= 1 && 
                    Math.abs(c - firstClickCol) <= 1;
                
                if (!(r === firstClickRow && c === firstClickCol) && !isFirstClickAdjacent) {
                    positions.push({r, c});
                }
            }
        }
        
        // Shuffle and select mine positions
        for (let i = 0; i < this.mines; i++) {
            if (positions.length === 0) break;
            
            const randomIndex = Math.floor(Math.random() * positions.length);
            const {r, c} = positions.splice(randomIndex, 1)[0];
            
            // Place mine
            this.board[r][c] = -1;
            this.minePositions.push({r, c});
            
            // Increment adjacent cells
            this.getAdjacentCells(r, c).forEach(({r: adjR, c: adjC}) => {
                if (this.board[adjR][adjC] !== -1) {
                    this.board[adjR][adjC]++;
                }
            });
        }
    }
    
    getAdjacentCells(r, c) {
        const cells = [];
        for (let dr = -1; dr <= 1; dr++) {
            for (let dc = -1; dc <= 1; dc++) {
                const newR = r + dr;
                const newC = c + dc;
                
                // Skip the cell itself and out of bounds
                if ((dr === 0 && dc === 0) || 
                    newR < 0 || newR >= this.rows || 
                    newC < 0 || newC >= this.cols) {
                    continue;
                }
                
                cells.push({r: newR, c: newC});
            }
        }
        return cells;
    }
    
    startTimer() {
        if (!this.timer) {
            this.timer = setInterval(() => {
                this.time++;
                this.timeElement.textContent = this.time;
            }, 1000);
        }
    }
    
    updateFlagsDisplay() {
        this.flagsElement.textContent = this.flagsLeft;
    }
    
    handleLeftClick(r, c) {
        // Don't process if game is over or cell is flagged
        if (this.gameOver || this.flagged[r][c]) {
            return;
        }
        
        // Start timer on first click
        if (this.firstClick) {
            this.firstClick = false;
            this.placeMines(r, c);
            this.startTimer();
        }
        
        // If it's a mine, game over
        if (this.board[r][c] === -1) {
            this.revealMines();
            this.gameOver = true;
            this.showMessage('Game Over!', 'lose');
            clearInterval(this.timer);
            return;
        }
        
        // Reveal the cell
        this.revealCell(r, c);
        
        // Check for win
        if (this.checkWin()) {
            this.gameOver = true;
            clearInterval(this.timer);
            this.flagAllMines();
            this.showMessage('You Win!', 'win');
        }
    }
    
    handleRightClick(r, c) {
        // Don't process if game is over or cell is already revealed
        if (this.gameOver || this.revealed[r][c]) {
            return;
        }
        
        // Toggle flag
        if (this.flagged[r][c]) {
            // Remove flag
            this.flagged[r][c] = false;
            this.flagsLeft++;
            this.getCellElement(r, c).classList.remove('flagged');
            this.getCellElement(r, c).textContent = '';
        } else if (this.flagsLeft > 0) {
            // Add flag
            this.flagged[r][c] = true;
            this.flagsLeft--;
            this.getCellElement(r, c).classList.add('flagged');
            this.getCellElement(r, c).textContent = '🚩';
        }
        
        this.updateFlagsDisplay();
        
        // Check for win after flag placement
        if (this.checkWin()) {
            this.gameOver = true;
            clearInterval(this.timer);
            this.flagAllMines();
            this.showMessage('You Win!', 'win');
        }
    }
    
    revealCell(r, c) {
        // Skip if already revealed or flagged
        if (this.revealed[r][c] || this.flagged[r][c]) {
            return;
        }
        
        // Mark as revealed
        this.revealed[r][c] = true;
        const cell = this.getCellElement(r, c);
        cell.classList.add('revealed');
        
        // If it's a number, show it
        if (this.board[r][c] > 0) {
            cell.textContent = this.board[r][c];
            cell.dataset.value = this.board[r][c];
            return;
        }
        
        // If it's empty (0), reveal adjacent cells
        if (this.board[r][c] === 0) {
            this.getAdjacentCells(r, c).forEach(({r: adjR, c: adjC}) => {
                this.revealCell(adjR, adjC);
            });
        }
    }
    
    revealMines() {
        this.minePositions.forEach(({r, c}) => {
            const cell = this.getCellElement(r, c);
            cell.classList.add('mine');
            cell.textContent = '💣';
        });
    }
    
    flagAllMines() {
        this.minePositions.forEach(({r, c}) => {
            if (!this.flagged[r][c]) {
                this.flagged[r][c] = true;
                const cell = this.getCellElement(r, c);
                cell.classList.add('flagged');
                cell.textContent = '🚩';
            }
        });
        this.flagsLeft = 0;
        this.updateFlagsDisplay();
    }
    
    checkWin() {
        // Check if all non-mine cells are revealed
        for (let r = 0; r < this.rows; r++) {
            for (let c = 0; c < this.cols; c++) {
                if (this.board[r][c] !== -1 && !this.revealed[r][c]) {
                    return false;
                }
            }
        }
        return true;
    }
    
    getCellElement(r, c) {
        return this.boardElement.querySelector(`[data-row="${r}"][data-col="${c}"]`);
    }
    
    showMessage(message, type = '') {
        this.messageElement.textContent = message;
        this.messageElement.className = `game-message ${type}`;
    }
    
    setupEventListeners() {
        // New game button
        document.getElementById('new-game').addEventListener('click', () => {
            this.initializeGame();
        });
        
        // Difficulty buttons
        document.getElementById('easy').addEventListener('click', () => this.setDifficulty(10, 10, 10));
        document.getElementById('medium').addEventListener('click', () => this.setDifficulty(16, 16, 40));
        document.getElementById('hard').addEventListener('click', () => this.setDifficulty(16, 30, 99));
        
        // Prevent context menu on right click
        document.addEventListener('contextmenu', (e) => {
            if (e.target.classList.contains('cell')) {
                e.preventDefault();
            }
        });
    }
    
    setDifficulty(rows, cols, mines) {
        // Update active button
        document.querySelectorAll('.difficulty-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        event.target.classList.add('active');
        
        // Update game settings
        this.rows = rows;
        this.cols = cols;
        this.mines = mines;
        
        // Reinitialize game
        this.initializeGame();
    }
}

// Initialize the game when the page loads
window.addEventListener('DOMContentLoaded', () => {
    const game = new Minesweeper(10, 10, 10);
});
