#!/usr/bin/env python

import csv
import json
import os
import random
import sys

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

def generate_names(count=1):
    usernames = []
    for i in range(count):
        username = None
        while not username or (username in usernames):
            username = _make_name()
        usernames.append(username)
    return usernames

if __name__=='__main__':
    host_data = json.loads(sys.argv[1])
    accts_per_host = int(sys.argv[2])
    count = int(host_data[0]['exact_count'])
    names = generate_names(count * accts_per_host)
    csv_users = []
    json_users = []
    for i, name in enumerate(names):
        password_hash = sha512_crypt.encrypt(name)
        group = 'worker%d' % int((i / accts_per_host))
        uid = i + 2000
        csv_record = {
            'name': name,
            'password': password_hash,
            'group': group,
        }
        csv_users.append(csv_record)
        json_record = {
            'name': name,
            'hash': password_hash,
            'group': group,
            'uid': uid,
        }
        json_users.append(json_record)
    with open('../tmp/roster.csv', 'w') as fh:
        w = csv.DictWriter(fh, ['name', 'password', 'group'])
        w.writeheader()
        w.writerows(csv_users)
    with open('../tmp/roster.json', 'w') as fh:
        json.dump(json_users, fh)
