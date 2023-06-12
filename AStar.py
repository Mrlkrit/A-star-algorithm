

#read data from file
def readDataset(path):
    
    with open(path, 'r') as file:

        line = file.readline()

        # remove haracters and read coordinates
        characters = "(),"
        for char in characters:
            line = line.replace(char, "")
        # read numbers separated by " "
        numbers = [int(i) for i in line.split() if i.isdigit()]

        coordinates = []
        count = 1
        temp = 1
        count2 = 1

        for i in numbers:
            if count == 0:
                coordinates.append((temp,i))
                count = 1
                count2= count2 +1
            else:
                temp=i
                count = 0
                
        #search for start and stop points
        line = file.readline()
        num = [int(i) for i in line.split() if i.isdigit()]
        
        start = num[0]
        stop = num[1]

        # read weights matrix

        line = file.readline()
        matrix = []
        
        while line:
            
            matrix.append([str(i) for i in line.split() ])
            line = file.readline()

    #return graph elements, start point, end point, weights matrix
    return coordinates,start,stop,matrix

# calculate heuristic
def heuristic(currentPoint,targetPoint,graph):
    heuristic = ((graph[targetPoint][0]-graph[currentPoint][0])**2.0 + (graph[targetPoint][1]-graph[currentPoint][1])**2.0)**0.5

    return heuristic

# find node with lowest route(f) cost
def findNode(considered,f):

    value = float("inf")#initialize value as inf
    temp = considered[0]

    for i in considered:
        if f[i] <= value:
            value = f[i]
            temp = i
    #return number of the lowest cost element
    return temp


def calculateWeight(point1,point2,matrix):

    val1 = float(matrix[point2][point1])
    val2 = float(matrix[point1][point2])

    val = 0
    
    if val1 == 0:
        val = val2
    else:
        val = val1

    
    return val
# reconstruct algorithm path 
def reconstructPath(cameFrom,stop):
    counter = 0
    path=[]
    node = cameFrom[stop]
    path.append(stop+1)
    
    while not(node == None):
        path.append(node+1)
        node = cameFrom[node]
        
    # reverse list
    path.reverse()
    
    return path
    
# Complete A* implementation
def astar(graph,start,stop,matrix):

    considered = []
    cameFrom = [] 
    g = []
    f = [] 
    path = [] 
    # initialize f and g values as inf
    for i in graph:
        g.append(float('inf'))
        f.append(float('inf'))
        cameFrom.append(None)
    # append start element
    g[start-1] = 0;
    f[start-1] = heuristic(start-1,stop-1,graph)
    considered.append(start-1)

    # while considered nodes list is not empty
    while len(considered) > 0:
        # find lowest cost element
        currentNode = findNode(considered,f) 
        # if found node is destination -> reconstruct path 
        if currentNode == stop-1:
            path=reconstructPath(cameFrom,stop-1)
            return path
        # remove lowest cost element from considered elements list
        considered.remove(currentNode)
       
        neighbours =[]
        weight = []
        counter = 0
        # find neighbours of lowest cost element
        for point in matrix[currentNode]:
            if not (float(point) == 0):
                neighbours.append(graph[counter])               
            if not(float(matrix[counter][currentNode]) == 0) :
                neighbours.append(graph[currentNode])  

            counter = counter+1

        
        for i in neighbours:

            x = i[0]
            y = i[1]
            #get index of the neighbour
            holder = graph.index((x,y))
            #calculate new g
            gTemp = g[currentNode] + float(calculateWeight(currentNode,holder,matrix))
                
            # if cost is lower than previous cost
            if gTemp < g[holder]:
                # we came here from currentNode - lowest f(x) element
                cameFrom[holder] = currentNode
                # update g and f
                g[holder] = gTemp
                f[holder] = gTemp + heuristic(holder,stop-1,graph)
                    
                # add neighbour to considered elements list if not in considered
                if holder not in considered:
                    considered.append(holder)
                        
        # clear neighbours list
        neighbours.clear()

        # if there is no path found return Brak
    return "Brak"


# enter path
path = input()
# read dataset
graph,start,stop,matrix = readDataset(path)
# calculate path
visitedList = astar(graph,start,stop,matrix)
# print path without additional elements
output = ' '.join([str(elem) for elem in visitedList])
print(output)



