from collections import deque
import tkinter as tk
#NEW GLOBAL VARIABLES
CELL_SIZE = 60

window = None
canvas = None

start = None
destination = None
path = []

click_count = 0

BOARD_SIZE = 8

DIRECTIONS = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1)
]
def draw_maze(board, path, start, destination):

    window = tk.Tk()
    window.title("Maze Solver")
    CELL_SIZE = 60#define cell size properly here orelse python will throw up an error again , okay and got it ? 
    canvas = tk.Canvas(
        window,
        width=BOARD_SIZE * CELL_SIZE,
        height=BOARD_SIZE * CELL_SIZE
    )

    canvas.pack()

    # Convert path into a set for fast lookup
    path_set = set(tuple(x) for x in path)

    for row in range(BOARD_SIZE):

        for col in range(BOARD_SIZE):

            x1 = col * CELL_SIZE
            y1 = row * CELL_SIZE

            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE

            # Default color
            color = "white"

            # Wall
            if board[row][col] == "#":
                color = "black"

            # Path
            if (row, col) in path_set:
                color = "skyblue"

            # Start
            if [row, col] == start:
                color = "green"

            # Destination
            if [row, col] == destination:
                color = "red"

            canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=color,
                outline="gray"
            )

    window.mainloop()

def is_inside_board(row, col):
    return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE


def make_board(value):
    board = []
    for _ in range(BOARD_SIZE):
        row = []
        for _ in range(BOARD_SIZE):
            row.append(value)
        board.append(row)
    return board

# def print_board():##############3
#     board = []
#     i=0
#     j=0
#     for i in range(BOARD_SIZE):
#         row = []
#         for j in range(BOARD_SIZE):
#             #value=input("enter the value,of index",i,",",j," either # or .")
#             value = input(f"Enter value for ({i}, {j}) (# or .): ")
#             row.append(value)
#         board.append(row)
#     for i in range(BOARD_SIZE):
#         for j in range(BOARD_SIZE):
#             print(board[i][j],end="\t")
#         print()
#     return board
def print_board():

    board = []

    print("Enter the maze row by row.")
    print("Use '-' for an empty path.")
    print("Use '|' for a wall.")
    print("Example:")
    print("--||----")

    for i in range(BOARD_SIZE):

        row = list(input(f"Row {i}: "))

        board.append(row)

    print("\nMaze:\n")

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            print(board[i][j], end=" ")
        print()

    return board

def reconstruct_path(parent, start, destination):
    path = []
    current = destination

    while current != start:
        path.append(current)
        current = parent[current[0]][current[1]]
        if current is None:
            return []

    path.append(start)
    path.reverse()
    return path
def rewrite_path(parent, start, destination,board):#I modified the above reconstruct function
    #for rewriting the path 
  #path = []
    current = destination

    while current != start:
       # path.append(current)
        board[current[0]][current[1]]="*"
        current = parent[current[0]][current[1]]
        if current is None:
            return []
    if(current==start):
        board[current[0]][current[1]]="*"
                    
                
      # path.append(start)
      # path.reverse()
    return board

def bfs(start, destination):
    queue = deque()
    queue.append(start)
    boardnew=[]
    #boardnew=print_board()###########
    boardnew=make_board("#")

    visited = make_board(False)
    distance = make_board(-1)
    parent = make_board(None)

    visited[start[0]][start[1]] = True
    distance[start[0]][start[1]] = 0
    while queue:
        current = queue.popleft()
        row = current[0]
        col = current[1]

        if current == destination:
            path = reconstruct_path(parent, start, destination)
            #boardnew=rewrite_path(parent, start, destination,boardnew)
            boardnew= draw_maze(boardnew, path, start, destination)
            # print("\nDestination Found!")
            # print("Shortest Distance:", distance[row][col])
            # print("\nShortest Path:")
            # for coordinate in path:
            #     print(coordinate)
            # for coordinate in boardnew:#it's board , not board new0
            #     print(coordinate)
            return boardnew
        
        # endloop=0#write endloop here 
        for dr, dc in DIRECTIONS:
            #endloop=0 dont write endloop here 
            new_row = row + dr
            new_col = col + dc

            if not is_inside_board(new_row, new_col): 
                # endloop+=1
                continue
            # if boardnew[new_row][new_col]=="#":############################3
            #     endloop+=1
            #     continue

            if visited[new_row][new_col]:
                continue
            #if()
            visited[new_row][new_col] = True
            distance[new_row][new_col] = distance[row][col] + 1
            parent[new_row][new_col] = [row, col]
            queue.append([new_row, new_col])
            # if endloop==4:
            #     print("there's a roadblock")
            #     break

    print("Destination cannot be reached.")

# def main():
#     print("=== Shortest Path on an Empty Chessboard ===")
#     start = [int(input("Start Row: ")), int(input("Start Column: "))]
#     destination = [int(input("Destination Row: ")), int(input("Destination Column: "))]
#     bfs(start, destination)

#NEW FUNCTIONS : 
#1
def mouse_click(event):

    global click_count
    global start
    global destination
    global path

    row = event.y // CELL_SIZE
    col = event.x // CELL_SIZE

    if not is_inside_board(row, col):
        return

    if click_count == 0:

        start = [row, col]
        click_count = 1

    elif click_count == 1:

        destination = [row, col]
        click_count = 2

        path = bfs(start, destination)

    draw_board()
#2
def create_window():

    global window
    global canvas

    window = tk.Tk()

    window.title("Maze Solver")

    canvas = tk.Canvas(
        window,
        width=BOARD_SIZE * CELL_SIZE,
        height=BOARD_SIZE * CELL_SIZE
    )

    canvas.pack()

    canvas.bind("<Button-1>", mouse_click)
    #3
def draw_board():

    canvas.delete("all")

    for row in range(BOARD_SIZE):

        for col in range(BOARD_SIZE):

            x1 = col * CELL_SIZE
            y1 = row * CELL_SIZE

            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE

            color = "black"

            if [row, col] == start:
                color = "green"

            elif [row, col] == destination:
                color = "red"

            elif [row, col] in path:
                color = "skyblue"

            canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=color,
                outline="white"
            )
#4
def main2():
    create_window()
    draw_board()
    window.mainloop()

if __name__ == "__main__":
    main2()



# ------------------------
#######################|
#-----------------------
#|######################
#|######################
#|######################
#-------------------------------------

