from measure import Measure
from measure import MeasureList
from measure import numeric_derivative
from matplotlib import pyplot
from scipy.optimize import curve_fit
from math import pi
import numpy 

def linear_curve(x,a,b): return a * x + b

def save_curve_plot(x, y, x_label, y_label, parameters, curvetype, filepath):    
    x_line = numpy.linspace(min(x), max(x), num=100)
    y_line = curvetype(x_line, *parameters)    
    pyplot.xlabel(x_label)
    pyplot.ylabel(y_label)
    pyplot.plot(x_line, y_line, '--', color='red')    
    pyplot.scatter(x,y)    
    pyplot.savefig(filepath)
    pyplot.show()
    pyplot.cla()

def part1(input_data):
    data = input_data.copy()
    
    init_position = Measure(0.21,0.002)
    gravity = Measure(9.7836, 0.003)
    
    data['force'] = data['discs_mass'] * gravity
    data['x'] = data['position'] - init_position
    data['k'] = data['force'] / data['x']
    
    x, y = data['x'].m, data['force'].m
    parameters, _ = curve_fit(linear_curve, x, y)

    save_curve_plot(
        x, y,
        'x (m)',
        'F (N)',
        parameters,
        linear_curve,         
        'experiments/mass_spring/part1_x_force_graph.png'
    )

    return data

def part2(input_data):
    data = input_data.copy()

    support_mass = Measure(0.0127, 0.0001)
    
    data['total_mass'] =  data['mass'] + support_mass
    data['time'] = (data['final_frame'] - data['initial_frame'])/data['fps']
    data['period'] = data['time']/data['n_oscilations']        
    data['k'] = (4*pi**2)*data['total_mass']/data['period']**2
    
    x, y = data['period'].m, data['total_mass'].m
    function = lambda x,a: a * x**2
    parameters, _ = curve_fit(function, x, y)
    save_curve_plot(
        x, y, 
        'T (s)',
        'm (kg)',
        parameters,
        function,
        'experiments/mass_spring/part2_mass_period_graph.png'
    )
    
    return data

def part3(input_data): 
    data = input_data.copy()    
    data['time'] = data['frame']/data['fps']

    x, y = data['time'].m, data['position'].m
    function = lambda x,a,w,p,c: a*numpy.cos(w*x + p) + c
    parameters, _ = curve_fit(function, x, y, p0=[0.06, 10, 0.1, 0])
    save_curve_plot(x, y, 't (s)','x (m)', parameters, function, 'experiments/mass_spring/part3_x_time_graph.png')   
    
    for epsilon_v in range(1,11):
        velocity = numeric_derivative(data['position'], data['time'], epsilon_v)    
        data['velocity_'+str(epsilon_v)] = velocity
        
        # -Awsen(wt+p)
        parameters, _ = curve_fit(lambda x,a,w,p: -a*w*numpy.sin(w*x + p), data['time'].m, velocity.m, p0=[0.06, 10, 0.1])
        save_curve_plot(x, y, 't (s)','v (m/s)', parameters, function, 'experiments/mass_spring/part3_v'+str(epsilon_v)+'_time_graph.png')  
        
        
        for epsilon_a in range(3,8):
            acceleration = numeric_derivative(velocity, data['time'], epsilon_a)
            data['acceleration_'+str(epsilon_v)+'_'+str(epsilon_a)] = acceleration
    
    
    
    
    return data
    
        
        
            