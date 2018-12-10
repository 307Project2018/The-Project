import re

boardWidth = 8
boardHeight = 8
board = [[None for x in range(boardWidth)] for y in range(boardHeight)]  # fill board with null references (no pieces)


def main():
    result = move_piece((3, 3), (3, 6))  # example move
    print(result)


def move_piece(start, end):
    """returns 1 if chess piece located at start can move to end and 0 otherwise"""
    if start == end:
        return 0
    piece_to_move = board[start[0]][start[1]]
    # query database about piece info, in particular the move_set
    move_set = "(0,4),(4,3),(5,6),(0,3)"  # example move_set
    possible_ends = re.findall(r"\((.,.)\)", move_set)
    possible_ends_tuples = [tuple(int(s) for s in i.split(',')) for i in possible_ends]

    # check if possible to move there for current piece by iterating through move_set
    possible_to_move = 0
    for x in possible_ends_tuples:
        if (x[0] + start[0], x[1] + start[1]) == end:
            possible_to_move = 1

    if possible_to_move == 0:
        return 0

    diff = (end[0] - start[0], end[1] - start[1])

    if piece_to_move == "pawn":  # pawn movement
        if board[end[0], end[1]] is not None:
            return 0

    if diff[0] == 0 or diff[1] == 0:  # crest movement
        min_v = min(diff[0], diff[1])
        max_v = max(diff[0], diff[1])

        if diff[0] == 0:
            for x in range(min_v + 1, max_v):
                if board[start[0]][x] is not None:
                    return 0
        else:
            for x in range(min_v + 1, max_v):
                if board[x][start[0]] is not None:
                    return 0

    if abs(diff[0]) == abs(diff[1]):  # diagonal movement
        a = (diff[0] * 1 / abs(diff[0]), diff[1] * 1 / abs(diff[1]))
        y = lambda z: (a[0] * z + start[0], a[1] * z + start[1])
        for x in range(1, abs(diff[1])):
            if board[y(x)[0]][y(x)[1]] is not None:
                return 0

    end_location = board[end[0]][end[1]]
    if end_location is not None:
        end_piece = board[end[0]][end[1]]
    # query database about endPiece
    # check if end_piece belongs to different player -> attack piece
    # otherwise reuturn 0
    attack_piece(start, end)
    return 1


def attack_piece(start, end):
    """Compares attack of attacking piece to hp of defending piece. If defending piece hp becomes equal or less than 0
    it is removed from the game and function return 1, otherwise it returns 0"""
    # compare attack and hp of attacking piece and defending piece
    # if attack > hp -> remove enemy piece from the game and the database
    board[end[0]][end[1]] = None
    return 1


if __name__ == "__main__":
    main()
