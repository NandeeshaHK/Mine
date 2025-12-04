# Modern Minesweeper

A sleek, modern implementation of the classic Minesweeper game, featuring a dark mode UI, custom icons, and an integrated auto-solver.

## Features

- **Modern UI**: Built with `customtkinter` for a clean, dark-themed look.
- **Auto-Solver**: Includes a built-in solver that can give hints or play the game for you.
- **Safe Start**: The first click is always safe.
- **Responsive**: Adapts to different grid sizes.

## Installation

You can install the package directly using `pip` or `uv`:

```bash
# Using pip
pip install .

# Using uv
uv pip install .
```

## Usage

### CLI

To start the game from the command line:

```bash
# If installed
mine

# Or using python directly
python -m mine
```

### Options

You can customize the grid size and number of mines:

```bash
mine --size 20 --mines 50
```

- `--size`: Grid size (default: 16)
- `--mines`: Number of mines (default: 40)

## How to Play

- **Left Click**: Reveal a cell.
- **Right Click**: Flag a cell as a mine.
- **Hint**: Click the "Hint" button to highlight a safe move.
- **Auto Solve**: Click "Auto Solve" to watch the AI play.

## Algorithm

The solver uses a Constraint Satisfaction Problem (CSP) approach:
1. **Basic Rules**:
   - If a cell has `N` flags around it and its number is `N`, all other neighbors are safe.
   - If a cell has `N` hidden neighbors and its number is `N` + existing flags, all hidden neighbors are mines.
2. **Backtracking** (Future Work): For complex situations where basic rules fail, a backtracking algorithm or probability estimation could be added.

## Development

To run locally without installing:

```bash
uv run python -m src.mine.__main__
```
