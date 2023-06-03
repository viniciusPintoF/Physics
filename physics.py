import sys
import pandas as pd
import experiments as exp

experiment_to_func = {
    'free_fall_f2': exp.free_fall_f2,
    'free_fall_f1': exp.free_fall_f1
}

if len(sys.argv) < 2 or sys.argv[1] not in experiment_to_func:
    print('Could not recognize experiment')
    exit()

experiment = sys.argv[1]
func = experiment_to_func[experiment]

data = pd.read_csv(experiment + '_in_data.csv').to_dict('records')
out_data = func(data, len(data), 3)

result_df = pd.DataFrame(out_data)
result_df.to_csv(experiment + '_out_data.csv', index=False) 
