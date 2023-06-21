import legacy.functions as f
import math

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

def mass_spring_part1(input_data, length, e):
    data = input_data.copy()

    # F = m*g 
    # F = kx => k = F/x
    # Temos g, m e x. Queremos k.

   
    gravity = 9.7836
    gravity_dev = 0.003
    
    relaxed_position = data[0]['position']  # Posição de relaxamento
    relaxed_position_dev = data[0]['position_dev']

    for i in range(length):
        if i == 0: continue
        print('ROW',i)

        row = data[i]

        print('g',gravity)

        total_mass = row['discs_mass']
        total_mass_dev = row['discs_mass_dev']
        print('m',total_mass)

        position = row['position']
        position_dev = row['position_dev']
        print('p',position)
        print('p0',relaxed_position)

        k = (total_mass * gravity) / (position - relaxed_position)
        print("k",k)

        k_deviations = [total_mass_dev, gravity_dev, position_dev, position_dev]
        k_derivatives = [
            gravity / (position - relaxed_position),
            total_mass / (position - relaxed_position),
            (gravity * total_mass) / ((position - relaxed_position) * (position - relaxed_position)),
            (gravity * total_mass) / ((position - relaxed_position) * (position - relaxed_position)),
        ]
        print("Derivative =", k_derivatives)
        k_dev = f.calculate_deviation_from_derivatives(k_deviations, k_derivatives)

        force = total_mass*gravity
        force_dev = f.calculate_deviation_from_derivatives([total_mass_dev, gravity_dev],[gravity, total_mass])

        x = position - relaxed_position
        x_dev = f.calculate_deviation_from_derivatives([position_dev, relaxed_position_dev],[1, -1])
        
        row['x'] = x
        row['x_dev'] = x_dev
        row['force'] = force
        row['force_dev'] = force_dev
        row['k'] = k
        row['k_dev'] = k_dev
        
    return data
        

def mass_spring_part2(input_data, length, e):
    data = input_data.copy()

    support_mass = 0.0127
    support_mass_dev = 0.0001

    for row in data:
        total_time = (row['final_frame'] - row['initial_frame']) / row['fps']
        total_time_deviations =  [ row['final_frame_dev'], row['initial_frame_dev'], row['fps_dev'] ]
        total_time_derivatives = [ 
            1/row['fps'],
            1/row['fps'],
            (row['final_frame'] - row['initial_frame']) / (row['fps'] * row['fps'])
        ]
        total_time_dev = f.calculate_deviation_from_derivatives(total_time_deviations, total_time_derivatives)

        period = total_time/row['n_oscilations']
        period_dev = total_time_dev/row['n_oscilations']
        
        print(row['mass'])
        print(support_mass)
        total_mass = row['mass'] + support_mass
        print(total_mass)
        total_mass_dev = row['mass_dev'] + support_mass_dev
        

        k = (4*math.pi*math.pi) * total_mass/(period*period)
        k_deviations = [ total_mass_dev, period_dev ]
        k_derivatives = [
            (4*math.pi*math.pi)/(period*period),
            (8*math.pi*math.pi) * total_mass/(period*period*period)
        ]
        k_dev = f.calculate_deviation_from_derivatives(k_deviations, k_derivatives)

        row['total_mass'] = total_mass
        row['total_mass_dev'] = total_mass_dev
        print(row['total_mass'])
        print()

        row['total_time'] = total_time
        row['total_time_dev'] = total_time_dev

        row['period'] = period
        row['period_dev'] = period_dev

        row['k'] = k
        row['k_dev'] = k_dev

    return data
        
def mass_spring_part3(input_data, length, e):
    data = input_data.copy()
    for row in data:
        frame = row['frame']
        fps = row['fps']

        time = frame/fps
        time_deviations = [ row['frame_dev'], row['fps_dev'] ]
        time_derivative = [ 1/fps, -frame/(fps*fps) ]
        time_dev = f.calculate_deviation_from_derivatives(time_deviations, time_derivative)

        row['time'] = time
        row['time_dev'] = time_dev

    for i in range(length):         
        row = data[i]
        for epsilon in range(2,6): 
            print("ROW",i)          
            print("EPSILON",epsilon)
            prev = i - epsilon
            next = i + epsilon            
            if prev < 0: prev = i
            if next > length - 1: next = i

            
            top = [ data[next]['position'], data[prev]['position'] ]
            top_dev = [ data[next]['position_dev'], data[prev]['position_dev'] ]
            bot = [ data[next]['time'], data[prev]['time'] ]
            bot_dev = [ data[next]['time_dev'], data[prev]['time_dev'] ]
            v, v_dev = f.calculate_numeric_derivative(top, top_dev, bot, bot_dev)

            row['velocity_'+str(epsilon)] = v
            row['velocity_'+str(epsilon)+'_dev'] = v_dev

            print()

    for i in range(length):         
        row = data[i]
        for epsilon in range(2,6): 
            prev = i - epsilon
            next = i + epsilon            
            if prev < 0: prev = i
            if next > length - 1: next = i
            
            top = [ data[next]['velocity_5'], data[prev]['velocity_5'] ]
            top_dev = [ data[next]['velocity_5_dev'], data[prev]['velocity_5_dev'] ]
            bot = [ data[next]['time'], data[prev]['time'] ]
            bot_dev = [ data[next]['time_dev'], data[prev]['time_dev'] ]
            v, v_dev = f.calculate_numeric_derivative(top, top_dev, bot, bot_dev)

            row['acceleration_'+str(epsilon)] = v
            row['acceleration_'+str(epsilon)+'_dev'] = v_dev



        



    return data