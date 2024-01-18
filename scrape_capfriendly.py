import pandas as pd 


def rename_players_column(df):
    '''
    Cap friendly differently names columns by position so This normalized by changing them all to "Player"
    '''
    df['Player'] =  df[df.columns[0]]
    df = df.drop(columns=df.columns[0], inplace=True)

def drop_total_row(df):
    '''
    Cap friendly has a total row for each position which is not relevant to us so it is dropped
    '''
    index = df.shape[0] - 1 
    df = df.drop(index, inplace=True)

def parse_salaries(df):
    '''
    The parsing of the HTML puts all of the future salaries into one column, so this grabs only the first columns
    salary, IE the current salary which is what we are looking for 
    '''
    df['Salary'] = df['2023-24'].str.split('$').str.get(1)
    df['Salary'] = df['Salary'].dropna().str.replace('[\\$,]','', regex=True).astype(int)
 
    df = df.drop(columns=['2023-24'])
    return df 


def process_name(input_str):
    '''
    Captains and assistant captains are noted on cap friendly but we will remove this.
    Reverse first and last name to be consistent with hockey reference data
    '''
    clean_str = input_str.replace('"A"', '').replace('"C"', '')
    parts = clean_str.split(',')
    if len(parts) == 2:
        last, first = parts
        flipped = f'{first} {last}'
        return flipped
    else:
        print(f'Invalid input string: {input_str}')

def scrape_team(team_str):  
    url = 'https://www.capfriendly.com/teams/' + team_str


    patterns_to_match = ['Forwards', 'Defense', 'Goalies']
    combined_pattern = "|".join(patterns_to_match)

    tables = pd.read_html(url, match=combined_pattern)
    valid_tables = tables[:-3]

    for table in valid_tables:
        rename_players_column(table)
        drop_total_row(table)

    players_df = pd.concat(valid_tables).reset_index(drop=True)

    # Drop columns we dont need 
    drop_columns = ['Years Remaining', 'Terms',
       'Status', 'Acquired', 'Age', '2024-25', '2025-26',
       '2026-27', '2027-28', '2028-29']

    players_df = players_df.drop(columns=drop_columns)

    players_df = parse_salaries(players_df)

    players_df['Player'] = players_df['Player'].apply(process_name)

    players_df.rename(columns={'POS':'specific_pos'}, inplace=True)

    return players_df



def main():
    Atlantic  = ['bruins', 'sabres', 'redwings', 'panthers', 'canadiens', 'senators', 'lightning', 'mapleleafs']
    Metro = ['hurricanes', 'bluejackets', 'devils', 'penguins', 'capitals', 'flyers', 'rangers', 'islanders']
    Central = ['coyotes', 'blackhawks', 'avalanche', 'stars', 'wild', 'predators', 'blues', 'jets']
    Pacific = ['ducks', 'flames', 'oilers', 'kings', 'sharks', 'kraken', 'canucks', 'goldenknights']


    league = Atlantic + Metro + Central + Pacific

    
    for index, team_str in enumerate(league):
        # base case
        if index == 0:
            league_df = scrape_team(team_str)
        else:
            temp_df = scrape_team(team_str)
            league_df = pd.concat([league_df, temp_df])
        
        if index % 4 == 0:
            print(f'{index/len(league) * 100}% complete')

    league_df.to_csv('./data/capfriendly.csv')

    print('Success :)')



if __name__ == '__main__':
    main()