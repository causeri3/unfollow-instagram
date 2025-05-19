from argparse import ArgumentParser


def get_args_md():
    parser = ArgumentParser()
    parser.add_argument('-d',
                        '--days',
                        required=False,
                        default=None,
                        type=int,
                        help='Number of days for which recent followings shall be excluded')

    args = parser.parse_known_args()
    return args

def get_args_wa():
    parser = ArgumentParser()
    parser.add_argument('-t',
                            '--target-account',
                            required=True,
                            default=None,
                            type=str,
                            help='For which account do you want the unfollowing list. Just the instagram username.')
    parser.add_argument('-u',
                            '--username',
                            required=True,
                            default=None,
                            type=str,
                            help='Instagram username (for scraping account)')
    parser.add_argument('-p',
                            '--password',
                            required=True,
                            default=None,
                            type=str,
                            help='Instagram password (for scraping account)')

    args = parser.parse_known_args()
    return args