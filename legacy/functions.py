def calculate_deviation_from_derivatives(deviations, derivatives):
    sum = 0
    for i in range(len(deviations)):
        # print(derivatives[i], deviations[i])
        sum += abs(derivatives[i]) * deviations[i]
        # print(abs(derivatives[i]) * deviations[i])
        # print(sum)
    
    return sum

def calculate_numeric_derivative(top_variables, top_deviations, bottom_variables, bottom_deviations):
    top_1 = top_variables[0]
    top_2 = top_variables[1]
    bot_1 = bottom_variables[0]
    bot_2 = bottom_variables[1]

    deltaTop = top_1 - top_2
    deltaBot = bot_1 - bot_2

    derivatives = [
        1 / (bot_1 - bot_2),
        1 / (bot_2 - bot_1),
        (top_2 - top_1) / ((bot_1 - bot_2) * (bot_1 - bot_2)),
        (top_1 - top_2) / ((bot_1 - bot_2) * (bot_1 - bot_2)),
    ]
    print("Derivative =", derivatives)
    print("top_1 =", top_1)
    print("top_2 =", top_2)
    print("top_1 - top_2 =", (top_1 - top_2))
    print("top_2 - top_1 =", (top_2 - top_1))
    print("bot_1 =", bot_1)
    print("bot_2 =", bot_2)
    print("bot_1 - bot_2 =", (bot_1 - bot_2))
    print("(bot_1 - bot_2)^2 =", (bot_1 - bot_2) * (bot_1 - bot_2))

    deviations = [
        top_deviations[0],
        top_deviations[1],
        bottom_deviations[0],
        bottom_deviations[1],
    ]

    return deltaTop/deltaBot, calculate_deviation_from_derivatives(deviations, derivatives)

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

    deviations = [next[top+'_dev'], prev[top+'_dev'], next[bot+'_dev'], prev[bot+'_dev']]
    derivatives = [
        1/(next[bot] - prev[bot]),
        -1/(next[bot] - prev[bot]),
        (next[top] - prev[top])/( (next[bot] - prev[bot]) * (next[bot] - prev[bot]) ),
        -(next[top] - prev[top])/( (next[bot] - prev[bot]) * (next[bot] - prev[bot]) ),
    ]

    return calculate_deviation_from_derivatives(deviations, derivatives)