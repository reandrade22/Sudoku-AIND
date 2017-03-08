rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

#Create diagonal units
main_diagonal_tuples = [list(zip(rows, cols))]
second_diagonal_tuples = [list(zip(rows, reversed(cols)))]
main_diagonal_units = [[a+b for (a,b)  in main_diagonal_tuples[0]]]
second_diagonal_units = [[a+b for (a,b)  in second_diagonal_tuples[0]]]
diagonal_units = main_diagonal_units + second_diagonal_units

#add diagonal units to unit list
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


assignments = []
def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

    """
    Reduces sudoku grid using the naked twins strategy
    Args:
        grid(string) - A grid in string form.
    Returns:
        grid(string) - A grid in string form. Resulting Sudoku in 
                       dictionary form after reducing based on 
                       naked twins.
    """

    found_twin = False
    twin_sequence = ""
    for box in values:
        twin_peer = []
        if len(values[box]) == 2:
            
            #Find a twin
            for peer in peers[box]:
                if values[box] == values[peer]:
                    found_twin = True
                    twin_sequence = values[box]
                    twin_peer.append(peer)

            #If a twin is count, countinue
            if found_twin:
                #Find the unit they both belong in
                units  = []
                for unit in unitlist:
                    if box in unit:
                          for peer in twin_peer:
                            if peer in unit and peer != box:
                                units.append(unit)
                #remove all elements from the twins that appear in a unit peer
                for unit in units:
                    for peer in unit:
                        if (values[peer] != values[box]) and (len(values[peer]) > 1):
                            for element in twin_sequence:
                                assign_value(values, peer, values[peer].replace(element, ""))


        found_twin = False

    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, 
                    then the value will be '123456789'.
    """
    dictionary = {}
    for key, value in zip(boxes, grid):
        if value != '.':
            dictionary[key] = value
        else:
            dictionary[key] = '123456789'
    
    return dictionary

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    
    # eliminates value from peers 
    for box in values:
        if len(values[box]) == 1:
            for peer in peers[box]:
                assign_value(values, peer, values[peer].replace(values[box], ""))

    return values

def only_choice(values):

    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Args:
        grid(string) - A grid in string form.

    Returns:
        grid(string) - A grid in string form. Resulting Sudoku in 
                       dictionary form after filling in only choices.
    """

    number_list = "123456789"

    for unit in unitlist:
        for number in number_list:
            box_with_number = []
            for box in unit:
                if number in values[box]:
                    box_with_number.append(box)
                    
            if len(box_with_number) == 1:
                #values[box_with_number[0]] = number
                assign_value(values, box_with_number[0], number)

    return values

def reduce_puzzle(values):

    '''Use different techniques to reduce the current sudoku grid

    Args:
        grid(string) - A grid in string form.

    Returns: 
         grid(string) - A grid in string form, reduced using eliminate,
                        only choise and naked twins strategies. Returns
                        False if no new grid can be found.

    '''
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Use the Eliminate Strategy
        values = eliminate(values)

        # Use the Only Choice Strategy
        values = only_choice(values)

        # Use the naked twins strategy
        values  = naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False

    return values

def search(values):

    """
    Using depth-first search and propagation, create a search tree and solve the sudoku.
    Args:
        grid(string): a string representing a sudoku grid.
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values) 
    if values == False:
        return False
    
    elif all(len(values[s]) == 1 for s in boxes): 
        return values
        
    else:
    
        # Choose one of the unfilled squares with the fewest possibilities
        unsolved_boxes = {box:lngth for box,lngth in values.items() if len(values[box]) > 1}
        shortest_possibility = min(unsolved_boxes, key= lambda box: len(unsolved_boxes[box]))
        # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
        for element in values[shortest_possibility]:
            possible_solution = values.copy()
            #possible_solution[shortest_possibility] = element
            assign_value(possible_solution, shortest_possibility, element)
            new_result = search(possible_solution)
            if new_result:
                return new_result

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    values = search(values)

    return values

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
