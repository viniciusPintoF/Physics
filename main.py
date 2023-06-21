import sys
import pandas as pd
import exp_mass_spring
from measure import Measure
from measure import MeasureList

experiment_info = {
    'mass_spring_part1': ('experiments/mass_spring/part1_in_data.csv', 'experiments/mass_spring/part1_out_data.csv', exp_mass_spring.part1),
    'mass_spring_part2': ('experiments/mass_spring/part2_in_data.csv', 'experiments/mass_spring/part2_out_data.csv', exp_mass_spring.part2),
    'mass_spring_part3': ('experiments/mass_spring/part3_in_data.csv', 'experiments/mass_spring/part3_out_data.csv', exp_mass_spring.part3)
}

def read_input():
    if len(sys.argv) < 2 or sys.argv[1] not in experiment_info:
        return None
    id = sys.argv[1]    
    return experiment_info[id]

def get_measures(data):    
    measures = dict()
    for name in data:
        if name.endswith('_dev'): continue
        
        measurement_values = data[name]
        length = len(measurement_values)        
        
        if name + '_dev' in data:            
            deviation_values = data[name + '_dev']
        else:
            deviation_values = [0 for _ in range(length)]             
        
        measures[name] = MeasureList([Measure(measurement_values[i], deviation_values[i]) for i in range(length)])
            
    return measures

def get_output(measures):
    output = dict()
    for name, value in measures.items():
        output[name] = value.m
        output[name+'_dev'] = value.d
        output[name+'_aprox'] = value.formatted_strings()[0]
        output[name+'_majdev'] = value.formatted_strings()[1]
        
    return output

# Main function
inpath, outpath, function = read_input()

if inpath == None:
    print('Could not recognize experiment')
    exit()    

in_data = pd.read_csv(inpath).to_dict()    
in_measures = get_measures(in_data)
print(in_measures)
out_measures = function(in_measures)
out_data = get_output(out_measures)
out_df = pd.DataFrame(out_data).to_csv(outpath, index=False) 
