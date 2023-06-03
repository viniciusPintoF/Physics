import functions as f

def free_fall_f2(input_data, length, e):
    data = input_data.copy()

    for row in data:
        row['h'] = row['p_f_topo'] + row['s']/2 - row['p_i']
        deviations = [row['dev_p_f_topo'], row['dev_s'], row['dev_p_i']]
        derivatives = [1, 1/2, -1]        
        row['dev_h'] = f.calculate_deviation_from_derivatives(deviations, derivatives)


    for i in range(length): 
        row = data[i]
        row['v'] = f.numeric_derivative('h', 't', data, i, e)
        row['dev_v'] = f.dev_numeric_derivative('h', 't', data, i, e)

    for i in range(length):
        row = data[i]
        row['a'] = f.numeric_derivative('v', 't', data, i, e)
        row['dev_a'] = f.dev_numeric_derivative('v', 't', data, i, e)


    for row in data:
        row['invariant'] = 2*row['h']*row['a'] - row['v']*row['v']
        deviations = [
            row['dev_h'], 
            row['dev_a'], 
            row['dev_v']
        ]
        derivatives = [
            2*row['a'], 
            2*row['h'], 
            -2*row['v']
        ]        
        row['dev_invariant'] = f.calculate_deviation_from_derivatives(deviations, derivatives)

    return data

def free_fall_f1(input_data, length, e):
    data = input_data.copy()

    for row in data:
        row['h'] = row['p_f_topo'] + row['s']/2 - row['p_i'] - row['s']/2
        deviations = [row['dev_p_f_topo'], row['dev_s'], row['dev_p_i'], row['dev_s']]
        derivatives = [1, 1/2, -1, -(1/2)]
        row['dev_h'] = f.calculate_deviation_from_derivatives(deviations, derivatives)


    for i in range(length): 
        row = data[i]
        row['v'] = f.numeric_derivative('h', 't', data, i, e)
        row['dev_v'] = f.dev_numeric_derivative('h', 't', data, i, e)

    for i in range(length):
        row = data[i]
        row['a'] = f.numeric_derivative('v', 't', data, i, e)
        row['dev_a'] = f.dev_numeric_derivative('v', 't', data, i, e)


    for row in data:
        row['invariant'] = 2*row['h']*row['a'] - row['v']*row['v']
        deviations = [
            row['dev_h'], 
            row['dev_a'], 
            row['dev_v']
        ]
        derivatives = [
            2*row['a'], 
            2*row['h'], 
            -2*row['v']
        ]        
        row['dev_invariant'] = f.calculate_deviation_from_derivatives(deviations, derivatives)

    return data

def spring_mass_exp1():
    return
        