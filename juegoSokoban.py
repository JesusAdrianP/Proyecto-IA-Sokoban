import sys
from collections import deque 


# Parámetros de entrada: s (list)
# Parámetros de salida: result (str)
# Descripción: Convierte una lista de elementos en una cadena de texto concatenada.

def listToString(s):
    return ''.join(str(ele) for ele in s)


# Parámetros de entrada: arreglo (list)
# Parámetros de salida: result (str)
# Descripción: Convierte una lista de tuplas en una cadena de texto que representa la ubicación de cada tupla en el formato (x,y).

def boxLocationToString(arreglo):
    return ''.join(['(' + str(x[0]) + ',' + str(x[1]) + ')' for x in arreglo])


# Parámetros de entrada:
# Ninguno
# Parámetros de salida:
# rows (int): Número de filas en el tablero del juego.
# columns (int): Número de columnas en el tablero del juego.
# position (list): Coordenadas de la posición inicial del jugador en el formato [x, y].
# boxes_positions (list): Lista de coordenadas de la posición de cada caja en el formato [[x1, y1], [x2, y2], ...].
# board (list): Lista de cadenas que representan las filas del tablero.

def readFile():
    rows = 0
    columns = 0
    counter = 0
    position = []
    boxes_positions = []
    board = []

    with open(sys.argv[1], 'r') as file:
        lines = file.readlines()

    # Eliminar los caracteres de salto de línea en cada línea
    lines = [line.rstrip('\n') for line in lines]

    for line in lines:
        if line[0] == 'W' or line[0] == '0':
            rows += 1
            board.append(line)
        elif line[0] != 'W' and line[0] != '0' and counter != 0:
            boxes_positions.append([int(line[0]), int(line[2])])
        elif line[0] != 'W' and line[0] != '0' and counter == 0:
            position.extend([int(line[0]), int(line[2])])
            counter += 1

    columns = len(lines[0])

    return rows, columns, position, boxes_positions, board



class State:
    def __init__(self, rows, columns, position, boxes_positions, board, movements, depth):
        self.rows = rows
        self.columns = columns
        self.position = position
        self.boxes_positions = boxes_positions
        self.board = board
        self.movements = movements
        self.idealPlaces = self.idealBoxLocation()
        self.depth = depth

    #genera una lista de movimientos que puede realizar el almacenista desde una posición 
    def validPlays(self):
        valid_plays = []

        #verificar que la posición a la que me voy a mover no sea un muro
        if(self.board[self.position[0]-1][self.position[1]] != 'W'):
            valid_plays.append('U')
        if(self.board[self.position[0]+1][self.position[1]] != 'W'):
            valid_plays.append('D')
        if(self.board[self.position[0]][self.position[1]-1] != 'W'):
            valid_plays.append('L')
        if(self.board[self.position[0]][self.position[1]+1] != 'W'):
            valid_plays.append('R')

        #verificar si la poscion donde se va a mover no hay una caja contra un muro o hay dos cajas juntas     
        if([self.position[0]-1,self.position[1]] in self.boxes_positions and (self.board[self.position[0]-2][self.position[1]] == 'W' or [self.position[0]-2,self.position[1]] in self.boxes_positions)):
            valid_plays.remove('U')
        if([self.position[0]+1,self.position[1]] in self.boxes_positions and (self.board[self.position[0]+2][self.position[1]] == 'W' or [self.position[0]+2,self.position[1]] in self.boxes_positions)):
            valid_plays.remove('D')
        if([self.position[0],self.position[1]-1] in self.boxes_positions and (self.board[self.position[0]][self.position[1]-2] == 'W' or [self.position[0],self.position[1]-2] in self.boxes_positions)):
            valid_plays.remove('L')
        if([self.position[0],self.position[1]+1] in self.boxes_positions and (self.board[self.position[0]][self.position[1]+2] == 'W' or [self.position[0],self.position[1]+2] in self.boxes_positions)):
            valid_plays.remove('R')

        return valid_plays
    
    #extraer las posiciones de meta 
    def idealBoxLocation(self):
      idealPlaces = [[i, j] for i in range(self.rows) for j in range(self.columns)  if self.board[i][j] == 'X']
     
      return idealPlaces

    #verificar que todas las cajas estén en las posiciones de meta 
    def winTheGame(self):
        return all(place in self.boxes_positions for place in self.idealPlaces)

    #verificar en qué jugadas no podría hacer ningún otro movimiento válido 
    def Deadlock(self):
        for i in range(0,len(self.boxes_positions)):
            #verificar si abajo y a la derecha de la caja hay muros
            if(self.board[self.boxes_positions[i][0]][self.boxes_positions[i][1]+1] == 'W' and self.board[self.boxes_positions[i][0]+1][self.boxes_positions[i][1]] == 'W'):
                #verificar si esa esquina es posicion de meta 
                if([self.boxes_positions[i][0],self.boxes_positions[i][1]] in self.idealBoxLocation()):
                    return False
                else:
                    return True
            #verificar si abajo y a la izquierda de la caja hay muros
            elif(self.board[self.boxes_positions[i][0]][self.boxes_positions[i][1]-1] == 'W' and self.board[self.boxes_positions[i][0]+1][self.boxes_positions[i][1]] == 'W'):
                #verificar si esa esquina es posicion de meta 
                if([self.boxes_positions[i][0],self.boxes_positions[i][1]] in self.idealBoxLocation()):
                    return False
                else:
                    return True
            #verificar si arriba y a la izquierda de la caja hay muros
            elif(self.board[self.boxes_positions[i][0]][self.boxes_positions[i][1]-1] == 'W' and self.board[self.boxes_positions[i][0]-1][self.boxes_positions[i][1]] == 'W'):
                #verificar si esa esquina es posicion de meta 
                if([self.boxes_positions[i][0],self.boxes_positions[i][1]] in self.idealBoxLocation()):
                    return False
                else:
                    return True
            #verificar si arriba y a la derecha de la caja hay muros
            elif(self.board[self.boxes_positions[i][0]][self.boxes_positions[i][1]+1] == 'W' and self.board[self.boxes_positions[i][0]-1][self.boxes_positions[i][1]] == 'W'):
                #verificar si esa esquina es posicion de meta
                if([self.boxes_positions[i][0],self.boxes_positions[i][1]] in self.idealBoxLocation()):
                    return False
                else:
                    return True
            #verificar si hay dos cajas juntas y no se puede empujar ninguna 
            elif((self.board[self.boxes_positions[i][0]][self.boxes_positions[i][1]+1] == 'W' or [self.boxes_positions[i][0],self.boxes_positions[i][1]+1] in self.boxes_positions) and (self.board[self.boxes_positions[i][0]+1][self.boxes_positions[i][1]] == 'W' or [self.boxes_positions[i][0]+1,self.boxes_positions[i][1]] in self.boxes_positions) and (self.board[self.boxes_positions[i][0]+1][self.boxes_positions[i][1]+1] == 'W' or [self.boxes_positions[i][0]+1,self.boxes_positions[i][1]+1] in self.boxes_positions)):
                if([self.boxes_positions[i][0],self.boxes_positions[i][1]] in self.idealBoxLocation()):
                    return False
                else:
                    return True
            elif((self.board[self.boxes_positions[i][0]][self.boxes_positions[i][1]-1] == 'W' or [self.boxes_positions[i][0],self.boxes_positions[i][1]-1] in self.boxes_positions) and (self.board[self.boxes_positions[i][0]-1][self.boxes_positions[i][1]] == 'W' or [self.boxes_positions[i][0]-1,self.boxes_positions[i][1]] in self.boxes_positions) and (self.board[self.boxes_positions[i][0]-1][self.boxes_positions[i][1]-1] == 'W' or [self.boxes_positions[i][0]-1,self.boxes_positions[i][1]-1] in self.boxes_positions)):
                if([self.boxes_positions[i][0],self.boxes_positions[i][1]] in self.idealBoxLocation()):
                    return False
                else:
                    return True
            else:
                return False

    #genera los nuevos estados dado un movimiento a realizar 
    def newState(self, move):
        #movimiento del almacenista 
        def mover(position, direction):
            return [position[0] + direction[0], position[1] + direction[1]]
    
        #movimiento de las cajas 
        def updateBoxes(boxes_positions, new_position):
            new_boxes = boxes_positions.copy()
            for i, box in enumerate(new_boxes):
                if box == new_position:
                    new_boxes[i] = mover(new_position, direction)
                    
            return new_boxes
        
        #direccion en la que se va a realizar el movimiento 
        direction = {'U': [-1, 0], 'D': [1, 0], 'L': [0, -1], 'R': [0, 1]}[move]
        new_position = mover(self.position, direction)
        
        
        if new_position in self.boxes_positions:
            new_boxes = updateBoxes(self.boxes_positions, new_position)
        else:
            new_boxes = self.boxes_positions.copy()
        
        new_movements = self.movements.copy()
        new_movements.append(move)

        #estado actualizado con el movimiento, las posiciones de las cajas, el recorrido y la profundidad del nodo 
        return State(self.rows, self.columns, new_position, new_boxes, self.board, new_movements, self.depth + 1)

rows, columns, position, boxes_positions, board = readFile()

initialState = State(rows, columns, position, boxes_positions, board, [], 0)

#busqueda por amplitud 
def BFS():
    #se crea una cola para expandir los nodos en orden de inserción 
    queue = deque()
    queue.append(initialState)
    #conjunto de nodos visitados 
    visited = set()
    while queue:
        #se extrae el primer estado en la cola 
        currentState = queue.popleft()
        if(currentState.depth> 64):
            continue
        #se añade el estado al conjunto de visitados 
        stateString = str(currentState.position[0]) + "," + str(currentState.position[1]) + boxLocationToString(currentState.boxes_positions)
        visited.add(stateString)
        #verificar si puede continuar o está en un estado en el que ya no puede hacer nada más        
        if(currentState.Deadlock()):
            continue
        else:
            if(currentState.winTheGame()):
                break
            #se generan los estados posibles 
            for move in currentState.validPlays():
                tempState = currentState.newState(move)
                #si ya visitó ese estado lo omite y pasa a insertar el siguiente 
                if(str(tempState.position[0]) + "," + str(tempState.position[1]) + boxLocationToString(tempState.boxes_positions) in visited):
                    continue
                else:
                    queue.append(tempState)
    return currentState

#busqueda por profundidad
def DFS():
    #se crea una pila para almacenar los estados 
    stack = [initialState]
    #conjunto de estados visitados, para evitar expandir nodos repetidos 
    visited = set()
    while stack:
        #se extrae el de mayor profundidad
        currentState = stack.pop()
        #restringir profundidad
        if(currentState.depth > 64):
            continue
        #añadir estado al conjunto de visitados
        visited.add(str(currentState.position[0]) + "," + str(currentState.position[1]) + boxLocationToString(currentState.boxes_positions))
        #verificar si ya perdió para evitar expandir ese estado 
        if(currentState.Deadlock()):
            continue
        else:
            if(currentState.winTheGame()):
                break
            valid_plays = currentState.validPlays()
            valid_plays.reverse()
            #generar los nuevos estados posibles a partir del estdo actual 
            for move in valid_plays:
                tempState = currentState.newState(move)
                #si es un estado repetido lo ommite y pasa al siguiente estado, de lo contrario lo inserta en la pila 
                if(str(tempState.position[0]) + "," + str(tempState.position[1]) + boxLocationToString(tempState.boxes_positions) in visited):
                    continue
                else:
                    stack.append(tempState)
    return currentState

#profundidad iterativa
def IDFS(limit):
    stack = deque()
    stack.append(initialState)
    visited = set()
    while stack:
        currentState = stack.pop()
        if(currentState.depth == limit):
            return currentState
        if(currentState.depth > 64):
            continue
        visited.add(str(currentState.position[0]) + "," + str(currentState.position[1]) + boxLocationToString(currentState.boxes_positions))
        if(currentState.Deadlock()):
            continue
        else:
            if(currentState.winTheGame()):
                break
            valid_plays = currentState.validPlays()
            valid_plays.reverse()
            for move in valid_plays:
                tempState = currentState.newState(move)
                if(str(tempState.position[0]) + "," + str(tempState.position[1]) + boxLocationToString(tempState.boxes_positions) in visited):
                    continue
                else:
                    stack.append(tempState)
    return currentState

def executeIDFS():
    limit = 10
    findSolution = False
    while(not findSolution):
        possibleSolution = IDFS(limit)
        if(possibleSolution.winTheGame()):
            findSolution = True
            return possibleSolution
        else:
            limit = limit + 1

bfsResponse = BFS()
dfsResponse = DFS()
idfsResponse = executeIDFS()

print("DFS:")
print(listToString(dfsResponse.movements))

print("BFS:")
print(listToString(bfsResponse.movements))

print("IDFS:")
print(listToString(idfsResponse.movements))