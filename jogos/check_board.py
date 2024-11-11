from flask import Flask, render_template, request, jsonify
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

def find_min_sum_path(plays):
    def helper(plays, min_sum = float('inf')):
        return_path = []
        for play in plays:
            if play['next'] is None and play['pieces_ahead'] == 0:
                if play['sum'] < min_sum:
                    min_sum = play['sum']
                    return_path = [play]
                elif play['sum'] == min_sum:
                    return_path.append(play)
            elif play['next'] is not None:
                path, new_min_sum = helper(play['next'], min_sum)
                if path:
                    play['next'] = path
                    if new_min_sum < min_sum:
                        min_sum = new_min_sum
                        return_path = [play]
                    elif new_min_sum == min_sum:
                        return_path.append(play)
        return return_path, min_sum
    return helper(plays)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the board data from the form
        board_data = request.form.get('boardData')
        pieces_input = request.form.get('pieces')

        # Process the board input into a numpy array
        try:
            board_list = ast.literal_eval(board_data)
            board = np.array(board_list)
        except Exception as e:
            print(f"Error parsing board data: {e}")
            return render_template('index.html', message='Invalid board input.')

        # Process the pieces input into list of numpy arrays
        try:
            pieces_list = ast.literal_eval(pieces_input)
            pieces = [np.array(piece) for piece in pieces_list]
        except Exception as e:
            print(f"Error parsing pieces data: {e}")
            return render_template('index.html', message='Invalid pieces input.')

        # Run the functions
        plays = place_pieces_sequentially(board, pieces)
        plays_min, min_sum = find_min_sum_path(plays)
        # make the "board" key in each play a list of lists for easier rendering in the template
        def convert_board_to_list(plays):
            for play in plays:
                play["board"] = play["board"].tolist()
                play["sum"] = int(play["sum"])
                if play["next"]:
                    convert_board_to_list(play["next"])
            return plays
        plays_min = convert_board_to_list(plays_min)

        return render_template('index.html', plays_min=plays_min, min_sum=min_sum)
    else:
        return render_template('index.html')

@app.route('/generate_board', methods=['POST'])
def generate_board():
    rows = int(request.form.get('rows', 5))
    cols = int(request.form.get('cols', 5))
    board = [[0 for _ in range(cols)] for _ in range(rows)]
    return jsonify(board=board)

if __name__ == '__main__':
    app.run(debug=True)
