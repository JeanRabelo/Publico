from flask import Flask, render_template, request
import numpy as np
import ast

app = Flask(__name__)

def can_place(board, piece, x, y):
    """Check if the piece can be placed at (x, y) on the board without overlap of filled spaces (ones)."""
    rows, cols = piece.shape
    sub_board = board[x:x + rows, y:y + cols]
    # Ensure the piece fits within board bounds and no overlap of '1's
    if sub_board.shape == piece.shape and np.all((sub_board + piece) <= 1):
        return True
    return False

def place_piece(board, piece, x, y):
    """Place the piece on the board at position (x, y) and return the new board configuration."""
    rows, cols = piece.shape
    new_board = board.copy()
    new_board[x:x + rows, y:y + cols] += piece
    return new_board

def find_all_positions(board, piece):
    """Find all positions where the piece can fit within the board."""
    board_rows, board_cols = board.shape
    piece_rows, piece_cols = piece.shape
    fits = []

    for x in range(board_rows - piece_rows + 1):
        for y in range(board_cols - piece_cols + 1):
            if can_place(board, piece, x, y):
                new_board = place_piece(board, piece, x, y)
                fits.append(new_board)

    return fits

def eliminate_lines(fits):
    """Substitute rows and columns with all ones by zeroes in each fit."""
    fits_after_lines_elimination = []
    for fit in fits:
        fit_copy = fit.copy()
        
        # Replace rows with all ones by zeroes
        row_mask = np.all(fit_copy == 1, axis=1)
        fit_copy[row_mask, :] = 0
        
        # Replace columns with all ones by zeroes
        col_mask = np.all(fit_copy == 1, axis=0)
        fit_copy[:, col_mask] = 0
        
        fits_after_lines_elimination.append(fit_copy)
    
    return fits_after_lines_elimination

def place_pieces_sequentially(board, pieces):
    """Place each piece consecutively on the board, updating and eliminating lines after each placement."""
    current_board = board.copy()
    plays = []

    for i, piece in enumerate(pieces, 1):
        fits = find_all_positions(current_board, piece)
        
        if not fits:
            print(f"No fit found for piece {i}.\n")
            return []
        
        # Apply line elimination
        fits_after_elimination = eliminate_lines(fits)
        for j, fit in enumerate(fits_after_elimination, 1):
            current_play = {
                "pieces_ahead": len(pieces) - 1,
                "placement": j,
                "board": fit,
                "sum": np.sum(fit)
            }
            # if the last piece was placed, current_play["next"] will be None, otherwise, it will be a list of plays, to be filled in the next iteration
            if len(pieces) == 1:
                current_play["next"] = None
            else:
                current_play["next"] = place_pieces_sequentially(fit, pieces[:i-1] + pieces[i:])
            plays.append(current_play)
    
    return plays

def print_board(board, indent=0):
    """Print the board in a nested format."""
    indent_str = "  " * indent
    for row in board:
        print(indent_str, row)

def print_plays(plays, indent=0):
    """Print the plays in a nested format."""
    for play in plays:
        print("  " * indent, f"Pieces ahead {play['pieces_ahead']} - Placement {play['placement']} - Sum {play['sum']}")
        print_board(play["board"], indent)
        if play["next"]:
            print_plays(play["next"], indent + 1)

def find_min_sum(plays, plays_min, min_sum):
    """Find the minimum sum of the final board configuration and the corresponding plays."""
    for play in plays:
        if play["next"]:
            old_plays_min = plays_min.copy()
            min_sum, plays_min = find_min_sum(play["next"], plays_min, min_sum)
            if plays_min != old_plays_min:
                if np.array([play["next"][0]["board"] == plays_min[-1]["board"]]).any():
                    play['next'] = [plays_min[-1]]
                    plays_min[-1] = play
        elif play["pieces_ahead"] == 0:
            if play["sum"] < min_sum:
                min_sum = play["sum"]
                plays_min = [play]
            elif play["sum"] == min_sum:
                plays_min.append(play)
    
    return min_sum, plays_min

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the board and pieces from the form
        board_input = request.form.get('board')
        pieces_input = request.form.get('pieces')

        # Process the board input into a numpy array
        try:
            board_list = ast.literal_eval(board_input)
            board = np.array(board_list)
        except:
            return render_template('index.html', message='Invalid board input.')

        # Process the pieces input into list of numpy arrays
        try:
            pieces_list = ast.literal_eval(pieces_input)
            pieces = [np.array(piece) for piece in pieces_list]
        except:
            return render_template('index.html', message='Invalid pieces input.')

        # Run the functions
        plays = place_pieces_sequentially(board, pieces)

        plays_min = []
        min_sum = float('inf')
        min_sum, plays_min = find_min_sum(plays, plays_min, min_sum)

        print(f"\nMinimum sum: {min_sum}")
        print("Paths with minimum sum:")
        print_plays(plays_min)

        return render_template('index.html', message='Processing complete. Check console for output.')
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

