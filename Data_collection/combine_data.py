import pandas as pd 
import glob 
from datetime import datetime
import os 



def main():

    hr_df = pd.DataFrame()

    file_pattern = 'data/hr_*.csv'
    file_paths = glob.glob(file_pattern)

    for file_path in file_paths:
        df = pd.read_csv(file_path)
        hr_df = pd.concat([hr_df, df], ignore_index=True)

    capfriendly_path = 'data/capfriendly.csv'

    cap_df = pd.read_csv(capfriendly_path)

    hr_drop = ['Unnamed: 0', 'Salary']
    hr_df = hr_df.drop(columns=hr_drop)
    cap_drop = ['Unnamed: 0']
    cap_df = cap_df.drop(columns=cap_drop)

  




    complete_df = pd.merge(hr_df, cap_df, how='outer', on='Player')


    current_datetime =  datetime.now()
    current_date_str = str(current_datetime.date()).replace('-','_')
    output_directory = './data/processed/'
    output_filename = current_date_str + '_clean_player_data.csv'
    output_path = output_directory + output_filename


    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        complete_df.to_csv(output_path)
    else:
        complete_df.to_csv(output_path)


if __name__ == '__main__':
    main()