def calc_direction(current_floor, destination):
    # calculate the direction of movement based on start and end floors
    direction = None
    movement = destination - current_floor
    # calculate floors difference to determine direction:
    if movement > 0:
        direction = +1
    elif movement < 0:
        direction = -1
    else:
        # if destination is same as current floor, stay
        direction = 0
    return direction

#take the max of two lists, but handle empty lists
def custom_max(x,y):
    if not x and len(y)>0:
        maximum = max(y)
    elif not y and len(x)>0:
        maximum = max(x)
    elif not x and not y:
        maximum = 0
    else:
        maximum = max(max(x),max(y))
    return maximum

def custom_min(x,y):
    if not x and len(y)>0:
        minimum = min(y)
    elif not y and len(x)>0:
        minimum = min(x)
    elif not x and not y:
        minimum = 0
    else:
        minimum = min(min(x),min(y))
    return minimum
