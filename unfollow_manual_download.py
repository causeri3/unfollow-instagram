import pandas as pd
from os import path, getcwd
import json
from datetime import timedelta

from args import get_args_md
args, _ = get_args_md()


def load(json_path):
    with open(json_path, 'r') as file:
        loaded_json = json.load(file)
    return loaded_json


# flatten, extract data using json_normalize and transform dates
def transform(json_data):
    df = pd.json_normalize(
        [item for item in json_data for item in item['string_list_data']],
        errors='ignore'
    )[["href", "value", "timestamp"]]
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')

    return df

def only_take_follows_older_than(df, days_to_be_older_than: int =7):
    current_date = pd.Timestamp.today()
    one_week_ago = current_date - timedelta(days=days_to_be_older_than)
    df_older_than_a_week = df[df['datetime'] < one_week_ago]
    return df_older_than_a_week


def get_unfollow():
    dir = getcwd()
    json_following = load(path.join(dir, 'followers_and_following', 'following.json'))
    json_followers = load(path.join(dir, 'followers_and_following', 'followers_1.json'))
    df_followers = transform(json_followers)
    df_following = transform(json_following['relationships_following'])
    return df_following[~df_following['value'].isin(df_followers['value'])].sort_values(by='timestamp')


if __name__ == "__main__":
    df_unfollow = get_unfollow()
    if args.days:
        print(f"Only non-followers of older then {args.days} days chosen")
        df_unfollow = only_take_follows_older_than(df_unfollow, args.days)
    for index, row in df_unfollow.iterrows():
        print(row['href'])

