#!/usr/bin/python3
#
# Get matrix for CI GitHub Actions workflow.
#
# Return a JSON-formatted matrix, a list of distributions where CI workflow
# should run.
#


import json
import requests
import argparse


def get_fedora_releases(type, exclude=[]):
    r = requests.get(f'https://bodhi.fedoraproject.org/releases?state={type}')
    r.raise_for_status()

    versions = [x['version'] for x in r.json()['releases'] if x['id_prefix'] == 'FEDORA']
    versions = list(set(versions) - set(exclude))
    versions.sort()

    return versions


def get_fedora_matrix():
    fedora_stable = get_fedora_releases('current')
    fedora_devel = get_fedora_releases('pending', exclude=['eln'])

    matrix = []
    matrix.extend(['fedora-{0}'.format(x) for x in fedora_stable])
    matrix.extend(['fedora-{0}'.format(x) for x in fedora_devel])

    return matrix


def get_centos_matrix():
    return ['centos-8', 'centos-9']


def get_other_matrix():
    return ['debian-latest']


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get GitHub actions CI matrix')
    parser.add_argument('--action', action='store_true', help='It is run in GitHub actions mode')
    args = parser.parse_args()

    fedora = get_fedora_matrix()
    centos = get_centos_matrix()
    other = get_other_matrix()

    matrix = {
        'intgcheck': [*fedora, *centos, *other],
        'multihost': [*fedora, *centos],
    }

    print(json.dumps(matrix, indent=2))

    if args.action:
        print(f'::set-output name=matrix::{json.dumps(matrix)}')
