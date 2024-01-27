import pandas as pd
import numpy as np 
import time
from unidecode import unidecode
from datetime import datetime




def process_name(input_str):
    '''
    Captains and assistant captains are noted on cap friendly but we will remove this.
    Reverse first and last name to be consistent with hockey reference data
    '''
    clean_str = input_str.replace('(C)', '').strip()


    return clean_str


def get_team_df(team:str) -> pd.DataFrame:
    

    url = 'https://www.hockey-reference.com/teams/'+ team + '/2024.html'


    patterns_to_match = ['Team Statistics','Scoring Regular Season', 'Roster']
    combined_pattern = "|".join(patterns_to_match)

    tables = pd.read_html(url, match=combined_pattern)

    team_stats_df = tables[0]
    roster_df = tables[1]
    scoring_df = tables[2]
    



    # Remove the header above all of the column names
    scoring_df.columns = scoring_df.columns.get_level_values(1)


    # need to match player strings. In scoring df it uses C and A where in roster it doestn 





    # Drop Repeat Columns and merge the dataframes
    roster_initial_drop = ['Age', 'Pos']
    roster_df = roster_df.drop(columns=roster_initial_drop)

    # We first need to remove the "(C)" and normalize names
    # This fixes "Pastrňák" != "Pastrnak"
    roster_df['Player'] = roster_df['Player'].apply(process_name)
    roster_df['Player'] = roster_df['Player'].apply(lambda x: unidecode(x))
    scoring_df['Player'] = scoring_df['Player'].apply(lambda x: unidecode(x))



    merged_df = pd.merge(scoring_df, roster_df, on='Player', how='inner')

    # drop irrelevant data
    merge_drop_columns = ['No.','Flag','Birth Date', 'Summary', 'Draft', 'Rk']
    merged_df = merged_df.drop(columns=merge_drop_columns)

    # Convert the Salary strings to ints
    merged_df['Salary'] = merged_df['Salary'].replace('N/A', np.nan)
    
    merged_df['Salary'] = merged_df['Salary'].dropna().str.replace('[\\$,]','', regex=True).astype(int)

    # Convert Rookie in exp to 0

    merged_df['Exp'] = merged_df['Exp'].replace('R', 0).astype(int)

    merged_df['Team'] = team


    return merged_df, team_stats_df





def main():
    # Each division must be seprately scraped to avoid rate limits on hockeyreference 

    Atlantic = ['BOS', 'FLA', 'TOR', 'DET', 'TBL', 'MTL', 'BUF', 'OTT']
    Metro = ['NYR', 'PHI', 'CAR', 'PIT', 'WSH', 'NYI', 'NJD', 'CBJ']
    Central = ['WPG', 'COL', 'DAL', 'NSH', 'ARI', 'STL', 'MIN', 'CHI']
    Pacific = ['VAN', 'VEG', 'LAK', 'EDM', 'CGY', 'SEA', 'ANA', 'SJS']


    league = [{'file_path':'data/temp_scrapes/hr_atlantic_data.csv', 'teams':Atlantic, 'label':'Atlantic'},
              {'file_path':'data/temp_scrapes/hr_metro_data.csv', 'teams':Metro, 'label':'Metro'},
              {'file_path':'data/temp_scrapes/hr_central_data.csv', 'teams':Central, 'label':'Central'},
              {'file_path':'data/temp_scrapes/hr_pacific_data.csv', 'teams':Pacific, 'label':'Pacific'}]
    


    current_datetime =  datetime.now()
    current_date_str = str(current_datetime.date()).replace('-','_')
    team_stats_output_df = pd.DataFrame()
    team_stats_output_directory = 'data/processed/team_data/'
    team_stats_output_path = team_stats_output_directory + current_date_str + '_team_stats_data.csv'

    for index, division_dict in enumerate(league):
        print(f'Starting scrape on: {division_dict["label"]}')
        teams = division_dict['teams']
        for i in range(len(teams)):
            if i == 0:
                league_df, team_stats_temp  = get_team_df(teams[i])
                team_stats_output_df = pd.concat([team_stats_output_df, team_stats_temp])
            else:
                temp_df, team_stats_temp = get_team_df(teams[i])
                league_df = pd.concat([league_df, temp_df])
                team_stats_output_df = pd.concat([team_stats_output_df, team_stats_temp])

        league_df.to_csv(division_dict['file_path'])
        print(f'{division_dict["label"]} scrape complete. Waiting 60 seconds now')
        if index != 3:
            time.sleep(60)
        else:
            team_stats_clean_output_df = team_stats_output_df.drop_duplicates().reset_index(drop=True)

            team_stats_clean_output_df.to_csv(team_stats_output_path)
            print('Complete!')

        
        


if  __name__ == '__main__':
    main()