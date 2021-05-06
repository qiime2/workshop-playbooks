# !/usr/bin/env python

# ----------------------------------------------------------------------------
# Copyright (c) 2016-2021, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import csv
import json
import math
import os
import random
import sys
import uuid

from passlib.hash import sha512_crypt


ADJECTIVES = ['astute', 'nocturnal', 'migratory', 'happy', 'focused', 'clever',
              'snazzy', 'zippy', 'silly']

ANIMALS = ['anteater', 'armadillo', 'axolotl', 'bairusa', 'bandicoot', 'bongo',
           'capybara', 'chameleon', 'chinchilla', 'coati', 'colugo', 'dragon',
           'echidna', 'emu', 'gecko', 'gerenuk', 'hedgehog', 'hoatzin',
           'hyena', 'iguana', 'iriomote', 'javelina', 'jellyfish', 'kanchil',
           'kangaroo', 'koala', 'lamprey', 'lemming', 'lemur', 'lobster',
           'meerkat', 'mole', 'nautilus', 'ocelot', 'octopus', 'okapi', 'owl',
           'pangolin', 'penguin', 'quail', 'quokka', 'quoll', 'reindeer',
           'ringtail', 'salamander', 'seahorse', 'shoebill', 'shrimp', 'sloth',
           'spider', 'squid', 'stoat', 'tapir', 'turtle', 'uakari', 'vaquita',
           'wallaby', 'wombat', 'woylie', 'xenopus', 'zebra', 'zebu']


def _make_name():
    name = []
    for list_ in (ADJECTIVES, ANIMALS):
        part = None
        while not part or (part in name):
            part = random.choice(list_)
        name.append(part)
    return '-'.join(name)


def _make_pass():
    password = str(uuid.uuid4())
    for val in '-01':
        password = password.replace(val, '')
    return password[0:20]


def generate_accounts(count=1):
    usernames = set()
    for i in range(count):
        username = _make_name()
        while username in usernames:
            username = _make_name()
        usernames.add(username)
    return [(x, _make_pass()) for x in usernames]


if __name__ == '__main__':
    host_data = json.loads(sys.argv[1])
    group_data = json.loads(sys.argv[2])
    workers = {'worker%d' % i: ip for i, ip in enumerate(group_data)}

    count = int(host_data[0]['exact_count'])
    if os.path.exists(sys.argv[3]):
        with open(sys.argv[3]) as fh:
            names = list(csv.reader(fh))[1:]  # skip header
        num_per_host = math.ceil(len(names)/float(count))  # Py2, float div!
    else:
        num_per_host = int(sys.argv[3])
        accounts = generate_accounts(count * num_per_host)

    csv_users = []
    json_users = []
    for i, (username, passwd) in enumerate(accounts):
        password_hash = sha512_crypt.encrypt(passwd)
        group = 'worker%d' % int((i // num_per_host))
        uid = i + 2000
        csv_record = {
            'username': username,
            'password': passwd,
            'group': group,
            'worker_ip': workers[group],
        }
        csv_users.append(csv_record)
        json_record = {
            'name': username,
            'hash': password_hash,
            'group': group,
            'uid': uid,
            'worker_ip': workers[group],
        }
        json_users.append(json_record)
    with open('../tmp/roster.csv', 'w') as fh:
        w = csv.DictWriter(fh, ['username', 'password', 'group', 'worker_ip'])
        w.writeheader()
        w.writerows(csv_users)
    with open('../tmp/roster.json', 'w') as fh:
        json.dump(json_users, fh)
