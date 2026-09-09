import numpy as np

label_lookup = {
    "Hallway": 0,
    "Restroom": 39,
    "Counselor's": 41,
    "Gym": 42,
    "Commons": 43,
    "Media Center": 44,
    "Courtyard": 45,
    "Cafeteria": 46,
    "Stage": 47,
    "Front Desk": 50,
    "Main Entrance": 51,
    "North Entrance": 52,
}

map=np.array([[2,0,47], # school map, shape = (n,3). [x,y,label]
     [2,1,46],
     [1,0,50],
     [1,1,0],
     [0,0,0],
     [0,-1,51],
     [0,1,0],
     [-1,0,1],
     [-1,1,0],
     [-1,2,42],
     [-2,0,39],
     [-2,1,0],
     [-2,6,0],
     [-2,7,35],
     [-2,8,0],
     [-2,9,38],
     [-3,0,41],
     [-3,1,0],
     [-3,2,42],
     [-3,4,42],
     [-3,6,0],
     [-3,7,34],
     [-3,8,0],
     [-3,9,37],
     [-4,0,0],
     [-4,1,0],
     [-4,2,0],
     [-4,3,0],
     [-4,4,0],
     [-4,5,0],
     [-4,6,0],
     [-4,7,0],
     [-4,8,0],
     [-4,9,36],
     [-5,0,3],
     [-5,1,0],
     [-5,2,4],
     [-5,3,2],
     [-5,4,43],
     [-5,5,32],
     [-5,6,0],
     [-5,7,33],
     [-6,0,5],
     [-6,1,0],
     [-6,2,6],
     [-6,4,45],
     [-6,5,30],
     [-6,6,0],
     [-6,7,31],
     [-7,0,7],
     [-7,1,0],
     [-7,2,8],
     [-7,5,29],
     [-7,6,0],
     [-7,7,28],
     [-8,0,9],
     [-8,1,0],
     [-8,3,45],
     [-8,5,27],
     [-8,6,0],
     [-9,0,11],
     [-9,1,0],
     [-9,2,12],
     [-9,3,44],
     [-9,4,44],
     [-9,5,24],
     [-9,6,0],
     [-9,7,26],
     [-10,1,0],
     [-10,2,0],
     [-10,3,0],
     [-10,4,0],
     [-10,5,0],
     [-10,6,0],
     [-10,7,25],
     [-11,1,0],
     [-11,3,16],
     [-11,5,39],
     [-12,1,0]])

def A_star_pathing(start_cord: np.ndarray, end_cord: np.ndarray, map: np.ndarray, valid_path_index: int=0, possible_parent_indices: np.ndarray = np.array([])):
    '''Find the shortest path from start_cord to end_cord given map
        end_cord can accept shape of:
            -(3,)
            -(n,3) but it only pathfinds to the cordinate with lowest euclidian distance to start_cord
        Pass possible_parent_indices as a array of possible indices with shape (1,) if your target room is only accessable "behind" other rooms.

        Returns a np.array of coordinate tuples from start to end (inclusive)'''

    if np.ndim(start_cord) != 1 or np.ndim(end_cord) not in (1,2) or np.ndim(map) != 2:
        raise ValueError('Inputs are of bad dimentions')

    def coord_key(cord):
        '''Convert [x, y, label] into (x,y)'''
        return tuple(int(value) for value in np.asarray(cord).flatten()[:2])

    def heuristic(input_cord, end_cord):
        '''Euclidean distance from input_cord to end_cord'''
        return np.linalg.norm(np.asarray(input_cord)[:2] - np.asarray(end_cord)[:2])

    def neighbors(cord):
        '''Find valid map coordinates next to cord'''
        x, y = cord
        x = int(x)
        y = int(y)
        possible_neighbors = [ # check the 4 cordinates next to the current one
            (x + 1, y),
            (x, y + 1),
            (x - 1, y),
            (x, y - 1),
        ]
        return [neighbor for neighbor in possible_neighbors if neighbor in valid_coords and neighbor not in closed_set] # check if neighbor actually exists on the map

    if np.ndim(end_cord) == 2: # only assign the end cord with lowest heuristic to start as a valid pathfinding target
        end_cord = np.asarray(min(end_cord, key=lambda cord: heuristic(cord, start_cord))) 

    start = coord_key(start_cord)
    end = coord_key(end_cord)
    possible_parent_indicies = np.append(possible_parent_indices, valid_path_index)
    valid_coords = {
        coord_key(row)
        for row in map
        if coord_key(row) == start 
        or coord_key(row) == end 
        or np.any(possible_parent_indicies == row[2])
    }

    if start not in valid_coords:
        raise ValueError("Start coordinate is not on the map")
    if end not in valid_coords:
        raise ValueError("End coordinate is not on the map")

    open_set = {start}
    closed_set = set() #{} is a empty dictionary not set
    came_from = {}

    # index each node to its corresponding f(n) and g(n) scores
    f_score = {start: heuristic(start, end)} #f(n) = g(n) + h(n) -> distance + heuristic cost to each node
    g_score = {start: int(0)} #g(n) -> pure distance cost to each node

    while open_set: # until open_set is depleated
        # find node with lowest f
        current = min(open_set, key=lambda cord: f_score.get(cord, np.inf)) # find the node with lowest f score. returns np.inf if not present initially

        if current == end: #this is true if we found the final node
            path = [current] #path is assembled as a list to retain ordinality
            construct_check = current
            while construct_check in came_from:
                construct_check = came_from[construct_check] #index current check to find where it came from
                path.append(construct_check)
            path.reverse()
            return np.array(path)

        open_set.remove(current)
        closed_set.add(current)
        possible_neighbors = neighbors(current)

        for neighbor in possible_neighbors:
            if neighbor in closed_set:
                continue #check next neighbor as we have already checked this one

            tentative_g_score = g_score[current] + heuristic(current, neighbor) #find the g score to the next node

            if neighbor in g_score and tentative_g_score >= g_score[neighbor]: # check the next neighbor if current one has too low of a g score
                continue 

            came_from[neighbor] = current # add the history of the parent node, this is what is reconsturcted
            # update f and g score sets
            g_score[neighbor] = tentative_g_score
            f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)

            open_set.add(neighbor)


    raise RuntimeError('No valid path')

if __name__ == "__main__": #this is there cuz my workspace is bloated and I like running what I want to only
    print(A_star_pathing(start_cord=np.array([-7,2]), end_cord=np.array([-6,4]), map=map, possible_parent_indices = np.array([label_lookup["Commons"],label_lookup["Media Center"]])))