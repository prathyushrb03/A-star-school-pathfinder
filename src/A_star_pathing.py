import numpy as np
from school_map import map, label_lookup, valid_entries

def A_star_pathing(start_cord: np.ndarray, end_cord: np.ndarray, map: np.ndarray, valid_path_index: int=0, possible_parent_indices: np.ndarray = np.array([label_lookup["Commons"], label_lookup["Media Center"], label_lookup["Cafeteria"]])):
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

    def is_valid_move(cord, neighbor):
        '''Check whether neighbor can be reached from cord'''
        cord_entries = valid_entries.get(cord, set())
        neighbor_entries = valid_entries.get(neighbor, set())
        if cord_entries or neighbor_entries:
            return neighbor in cord_entries or cord in neighbor_entries
        return True

    def neighbors(cord):
        '''Find valid map coordinates next to cord'''
        x, y = cord
        x = int(x)
        y = int(y)
        possible_neighbors = [ # check the 4 cordinates next to the current one
            (x, y + 1),
            (x + 1, y),
            (x, y - 1),
            (x - 1, y),
        ]
        return [
            neighbor
            for neighbor in possible_neighbors
            if neighbor in valid_coords
            and neighbor not in closed_set
            and is_valid_move(cord, neighbor)
        ] # check if neighbor actually exists on the map and is entered from a valid entry point

    if np.ndim(end_cord) == 2: # only assign the end cord with lowest heuristic to start as a valid pathfinding target
        end_cord = np.asarray(min(end_cord, key=lambda cord: heuristic(cord, start_cord))) 

    def add_entry_chain(valid_coords, cord):
        '''Add room entry coordinates needed to reach cord'''
        coords_to_check = [cord]
        while coords_to_check:
            check = coords_to_check.pop()
            for entry in valid_entries.get(check, set()):
                if entry not in valid_coords:
                    valid_coords.add(entry)
                    coords_to_check.append(entry)

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
    add_entry_chain(valid_coords, start)
    add_entry_chain(valid_coords, end)

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
    print(A_star_pathing(start_cord=np.array([1,0]), end_cord=np.array([-3,1]), map=map))
