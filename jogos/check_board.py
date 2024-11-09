import numpy as np

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

# Example usage:
board = np.array([
    [1, 1, 1, 0, 0],
    [1, 1, 1, 0, 0],
    [1, 1, 0, 1, 0],
    [0, 1, 0, 0, 0],
    [1, 0, 0, 0, 0]
])

piece = np.array([
    [1, 0],
    [0, 1]
])

# Find all fits
fits = find_all_positions(board, piece)

# Apply line elimination
fits_after_lines_elimination = eliminate_lines(fits)

# Display results
print("Possible fits of the piece within the board after eliminating full rows and columns of ones:")
for i, fit in enumerate(fits_after_lines_elimination, 1):
    print(f"Fit {i}:\n{fit}\n")

