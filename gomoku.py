import random

def sq_empty(board, y,x):
    if board[y][x] == " ":
        return True
    return False

def emptysquares(board):
    result = []
    for i in range (len(board)):
        for j in range (len(board)):
            if sq_empty(board, i,j) == True:
                result.append([i,j])
    return result

def randmove(board):
    move_y = emptysquares(board)[random.randrange(0,len(emptysquares(board)))][0]
    move_x = emptysquares(board)[random.randrange(0,len(emptysquares(board)))][1]
    return move_y, move_x


def is_longest_seq(board, col, y_start, x_start, length, d_y, d_x):
    y_end = y_start + (length-1)*d_y
    x_end = x_start + (length-1)*d_x
    endstatus = "continue"
    startstatus = "continue"

    if y_end+d_y > len(board)-1 or x_end+d_x > len(board)-1 or y_end+d_y <0 or x_end+d_x<0:
        endstatus = "stop"

    if y_start - d_y < 0 or x_start-d_x < 0 or y_start-d_y>len(board)-1 or x_start-d_x>len(board)-1:
        startstatus = "stop"
    if startstatus == "continue":
        if board[y_start - d_y][x_start - d_x] == col:
            return False
    if endstatus == "continue":
        if board[y_end+d_y][x_end+d_x] == col:

            return False
    return True

def print_board(board):

    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"

    print(s)

def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board

def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i)
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))


def is_sq_in_board(board, y,x):
    if y <= len(board) and x<= len(board):
        return True
    else:
        return False

def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res





        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res

def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x


#### NEW CODE STARTS ####
def is_empty(board):
    for i in range (len(board)):
        for j in range (len(board)):
            if board[i][j] != " ":
                return False
    return True


def is_bounded(board, y_end, x_end, length, d_y, d_x):
    sides_bounded = 0
    x_start = x_end - (length-1)*d_x
    y_start = y_end - (length-1)*d_y
    statusend = "continue"
    statusstart = "continue"

    if x_start >= 0 and x_start <= len(board)-1 and y_start>=0 and y_start <= len(board)-1 and x_end >= 0 and x_end <= len(board)-1 and y_end>=0 and y_end <= len(board)-1:
        if y_end+d_y > len(board)-1 or x_end+d_x>len(board)-1 or y_end+d_y<0 or x_end+d_x<0:
            sides_bounded = sides_bounded+1
            statusend = "stop"
        if y_start -d_y < 0 or x_start-d_x <0 or y_start-d_y > len(board)-1 or x_start-d_x > len(board)-1:
            sides_bounded = sides_bounded+1
            statusstart = "stop"

        if sides_bounded<2:
            if statusend == "continue":
                if board[y_end+d_y][x_end+d_x] != " ":
                    sides_bounded = sides_bounded+1
            if statusstart == "continue":
                if board[y_start-d_y][x_start-d_x] != " ":
                    sides_bounded = sides_bounded+1



        if sides_bounded == 2:
            return "CLOSED"
        elif sides_bounded == 1:
            return "SEMI-OPEN"
        elif sides_bounded == 0:
            return "OPEN"

def detect_row(board, col, y_start, x_start, length, d_y, d_x):

    i = y_start
    j = x_start

    semi_open_seq_count = 0
    open_seq_count = 0

    while is_sq_in_board(board,i,j) == True:

        if i > len(board)-1 or i < 0:
            break
        elif j > len(board)-1 or j < 0 :
            break
        if board[i][j] == col:

            if is_sequence_complete(board, col,i,j, length, d_y, d_x) == True and is_longest_seq(board,col,i,j,length,d_y,d_x)==True:
                if is_bounded(board, i+((length-1)*d_y), j+((length-1)*d_x), length, d_y, d_x) == "SEMI-OPEN":
                    semi_open_seq_count = semi_open_seq_count+1
                elif is_bounded(board, i+((length-1)*d_y), j+ ((length-1)*d_x), length, d_y, d_x) == "OPEN":
                    open_seq_count = open_seq_count + 1

        i = i + d_y
        j = j + d_x

    return open_seq_count, semi_open_seq_count

def detect_rows(board, col, length):
    ####CHANGE ME
    open_seq_count, semi_open_seq_count = 0, 0

    for i in range (len(board)):

        for n in range (-1, 2):

            for m in range (-1,2):

                #GO ALONG LEFT SIDE, DO ALL DIAGONALS AND HORIZONTAL
                #WILL COVER X X X X X
                #           X X X X
                #           X X X
                #           X X X X
                #           X X X X X
                if n == 1 and m == 0:
                    continue
                if n == -1 and m == 0:
                    continue
                if m == 0 and n == 0:
                    continue

                resulty = detect_row(board, col, i, 0, length, n, m)

                open_seq_count = open_seq_count + resulty[0]
                semi_open_seq_count = semi_open_seq_count + resulty[1]

        #GO ALONG TOP, DO ALL VERTICALS
        resultx = detect_row(board, col,0,i,length,1,0)

        open_seq_count = open_seq_count +resultx[0]
        semi_open_seq_count = semi_open_seq_count+resultx[1]

    for i in range (1, len(board)-1):
        #RIGHT SIDE, FINISH DIAGONALS
        resultdown = detect_row(board, col, i, len(board)-1, length, -1, -1)
        resultup = detect_row(board, col, i, len(board)-1, length, 1,-1)

        open_seq_count = open_seq_count + resultup[0]
        semi_open_seq_count = semi_open_seq_count + resultup[1]
        open_seq_count = open_seq_count + resultdown[0]
        semi_open_seq_count = semi_open_seq_count + resultdown[1]


    return open_seq_count, semi_open_seq_count
#includes closed sequences
def search_row(board, col, y_start, x_start, length, d_y, d_x):

    i = y_start
    j = x_start


    num = 0
    while is_sq_in_board(board,i,j) == True:

        if i > len(board)-1 or i < 0:
            break
        elif j > len(board)-1 or j < 0 :
            break
        if board[i][j] == col:

            if is_sequence_complete(board, col,i,j, length, d_y, d_x) == True and is_longest_seq(board,col,i,j,length,d_y,d_x)==True:
                num = num +1

        i = i + d_y
        j = j + d_x

    return num
#includes closed sequences
def search_rows(board, col, length):
    ####CHANGE ME
    num = 0
    for i in range (len(board)):

        for n in range (-1, 2):

            for m in range (-1,2):

                #GO ALONG LEFT SIDE, DO ALL DIAGONALS AND HORIZONTAL
                #WILL COVER X X X X X
                #           X X X X
                #           X X X
                #           X X X X
                #           X X X X X
                if n == 1 and m == 0:
                    continue
                if n == -1 and m == 0:
                    continue
                if m == 0 and n == 0:
                    continue

                resulty = search_row(board, col, i, 0, length, n, m)
                num = num + resulty
        #GO ALONG TOP, DO ALL VERTICALS
        resultx = search_row(board, col,0,i,length,1,0)

        num = num + resultx

    for i in range (2, len(board)-1):
        resultdown = search_row(board, col, i, len(board)-1, length, -1, -1)
        resultup = search_row(board, col, i, len(board)-1, length, 1,-1)

        num = num + resultdown + resultup

    return num
def search_max(board):
    initscore = score(board)
    curmax = initscore
    move_y, move_x = randmove(board)

    for i in range (len(board)-1):
        for j in range (len(board)-1):
            if sq_empty(board,i,j) == True:

                board[i][j] = "b"

                if score(board) > curmax:
                    curmax = score(board)
                    move_y = i
                    move_x = j
                if is_win(board) == "Black won":
                    board[i][j] = " "
                    return i, j
                board[i][j] = " "

    return move_y, move_x

def is_win(board):
    if search_rows(board,'w', 5)>0:
        return "White won"
    if search_rows(board,'b',5)>0:
        return "Black won"
    elif len(emptysquares(board)) == 0:
        return "Draw"
    else:
        return "Continue playing"
def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):

        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)


    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])


def is_sequence_complete(board, col, y_start, x_start, length, d_y, d_x):
    y = y_start
    x = x_start
    if x_start+length*d_x > len(board) or y_start+length*d_y > len(board):
        return False
    for i in range (length):
        if board[y][x] == col:
            x = x + d_x
            y = y + d_y
        else:
            return False
    return True

def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print(is_longest_seq(board,"w",5,2,2,1,0))
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3; x = 5; d_x = -1; d_y = 1; length = 2

    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #

    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);

    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #
    #
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0


if __name__ == "__main__":
    play_gomoku(8)


