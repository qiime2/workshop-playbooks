import sys
from bioblend.galaxy import GalaxyInstance


def parse_accts(fp):
    accts = []
    with open(fp) as fh:
        for line in fh.readlines():
            username, email, password = line.split(',')
            accts.append((username, email, password))
    return accts


if __name__ == '__main__':
    server = sys.argv[1]
    api_key = sys.argv[2]
    accts_csv_fp = sys.argv[3]

    gi = GalaxyInstance(server, key=api_key)
    accounts = parse_accts(accts_csv_fp)
    for (username, email, password) in accounts:
        gi.users.create_local_user(username, email, password)
