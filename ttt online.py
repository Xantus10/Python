import socket
import sys


board = [['.', '.', '.'] for i in range(3)]

def printboard():
    print(f"""
            +-----------------------------+
            |         |         |         |
            |    {board[0][0]}    |    {board[0][1]}    |    {board[0][2]}    |
            |         |         |         |
            ===============================
            |         |         |         |
            |    {board[1][0]}    |    {board[1][1]}    |    {board[1][2]}    |
            |         |         |         |
            ===============================
            |         |         |         |
            |    {board[2][0]}    |    {board[2][1]}    |    {board[2][2]}    |
            |         |         |         |
            +-----------------------------+
            """)


def server_side(sock):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(sock)
    server.listen(1)
    client_socket, addr = server.accept()
    client_socket.send(b'CONF')
    end_of_game = False
    while not end_of_game:
        inpos = client_socket.recv(4096).decode('utf-8')
        board[int(inpos[0])][int(inpos[1])] = 'X'
        end_of_game = checkwin()
        if not end_of_game:
            pos = move('O')
            client_socket.send(bytes(pos, 'utf-8'))
            end_of_game = checkwin()
    client_socket.close()



def client_side(sock):
    end_of_game = False
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(sock)
    conf = client.recv(4096)
    if conf.decode('utf-8') == 'CONF':
        while not end_of_game:
            pos = move('X')
            client.send(bytes(pos, 'utf-8'))
            end_of_game = checkwin()
            if not end_of_game:
                inpos = client.recv(4096).decode('utf-8')
                board[int(inpos[0])][int(inpos[1])] = 'O'
                end_of_game = checkwin()


def getnetwork():
    if len(sys.argv) == 2:
        ip = sys.argv[1]
    else:
        ip = input('input IP or "/" to listen: ')
    if ip is not None:
        if ip[0] == '/':
            ip_port = ('0.0.0.0', 9999)
        else:
            ip_port = (ip, 9999)
    else:
        print('Invalid input information')
        sys.exit(1)
    return ip_port


def move(player):
    printboard()
    print('you are on move')
    active = True
    while active:
        pos = input('enter coordinates (0 - 2 in format "row column" without space - 02): ')
        try:
            if board[int(pos[0])][int(pos[1])] == '.':
                board[int(pos[0])][int(pos[1])] = player
                active = False
                return pos
            else:
                print('place is already taken!')
        except:
            print('invalid input')


def checkwin():
    if board[0][0] == board[1][1] == board[2][2] != '.':
        print(f'{board[1][1]} has won!!!')
        printboard()
        return True
    elif board[2][0] == board[1][1] == board[0][2] != '.':
        print(f'{board[1][1]} has won!!!')
        printboard()
        return True
    else:
        for i in range(len(board)):
            if board[0][i] == board[1][i] == board[2][i] != '.':
                print(f'{board[0][i]} has won!!!')
                printboard()
                return True
            elif board[i][0] == board[i][1] == board[i][2] != '.':
                print(f'{board[i][0]} has won!!!')
                printboard()
                return True
    if '.' not in board[0] and '.' not in board[1] and '.' not in board[2]:
        print('it is a tie')
        printboard()
        return True


def main():
    sock = getnetwork()
    if sock[0] == '0.0.0.0':
        server_side(sock)
    else:
        client_side(sock)


if __name__ == '__main__':
    main()
