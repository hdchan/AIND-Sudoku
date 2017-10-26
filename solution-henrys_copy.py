assignments = []

letters = 'ABCDEFGHI'
numbers = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return  [a + b for a in A for b in B]

boxes = cross(letters, numbers)
unit_rows = [cross(l, numbers) for l in letters]
unit_columns = [cross(letters, n) for n in numbers]
unit_boxes = [cross(l, n) for l in ('ABC', 'DEF', 'GHI') for n in ('123', '456', '789')]
all_units = unit_rows + unit_columns + unit_boxes
units = dict((s, [u for u in all_units if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

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



def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    
    return {box:(numbers if grid[idx] == '.' else grid[idx]) for idx, box in enumerate(boxes)}

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    print("Displaying board")
    for idx, unit_row in enumerate(unit_rows):
        row_string = ""
        for idx2, box in enumerate(unit_row):
            row_string += values[box]
            row_string += (9 - len(values[box])) * ' ' + ' '
            if ((idx2 + 1) % 3 == 0 and idx2 + 1 != 9):
                row_string += ' | '
        print('\n' + row_string)
        if ((idx + 1) % 3 == 0 and idx + 1 != 9):
            print('\n' + '-' * len(row_string))
            

def eliminate(values):
    for box in boxes:
        if (len(values[box]) == 1):
            for peer_box in peers[box]:
                values[peer_box] = values[peer_box].replace(values[box], '')
    return values

def only_choice(values):
    for unit in all_units:
        for digit in '123456789':
            dplaces =[]
            for box in unit:
                if digit in values[box]:
                    dplaces.append(box)
            if (len(dplaces) == 1):
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        solved_before = len([box for box, value in values.items() if len(value) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_after = len([box for box, value in values.items() if len(value) == 1])
        stalled = solved_after == solved_before
        if len([box for box, value in values.items() if len(value) == 0]):
            return False
    return values

def search(values):
    values = reduce_puzzle(values)
    if values == False:
        return False
    if all(len(v) == 1 for box, v in values.items()):
        return values

    l, b = min((len(values[box]), box) for box in boxes if len(values[box]) > 1)
    for v in values[b]:
        temp_values = values.copy()
        temp_values[b] = v
        attempt = search(temp_values)
        if (attempt):
            return attempt

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
    # diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    diag_sudoku_grid = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
    display(solve(diag_sudoku_grid))
    
    # try:
    #     from visualize import visualize_assignments
    #     visualize_assignments(assignments)

    # except SystemExit:
    #     pass
    # except:
    #     print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
