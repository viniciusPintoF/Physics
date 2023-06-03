def calculate_deviation_from_derivatives(deviations, derivatives):
    sum = 0
    for i in range(len(deviations)):
        sum += abs(derivatives[i]) * deviations[i] 
    
    return sum

def define_next(data, index, offset):
    if index + offset < len(data):
        return data[index + offset]
    else:
        return data[index]

def define_prev(data, index, offset):
    if index - offset >= 0:
        return data[index - offset]
    else:
        return data[index]

def numeric_derivative(top, bottom, data, index, offset):
    next = define_next(data, index, offset)
    prev = define_prev(data, index, offset)

    deltaTop = next[top] - prev[top]
    deltaBot = next[bottom] - prev[bottom]
 
    return deltaTop/deltaBot

def dev_numeric_derivative(top, bot, data, index, offset):
    next = define_next(data, index, offset)
    prev = define_prev(data, index, offset) 

    deviations = [next['dev_'+top], prev['dev_'+top], next['dev_'+bot], prev['dev_'+bot]]
    derivatives = [
        1/(next[bot] - prev[bot]),
        -1/(next[bot] - prev[bot]),
        (next[top] - prev[top])/( (next[bot] - prev[bot]) * (next[bot] - prev[bot]) ),
        -(next[top] - prev[top])/( (next[bot] - prev[bot]) * (next[bot] - prev[bot]) ),
    ]

    return calculate_deviation_from_derivatives(deviations, derivatives)