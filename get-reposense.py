#!/usr/bin/env python

import argparse
import sys
import os
import shutil
import requests
import subprocess

JAR_FILENAME = 'RepoSense.jar'

def parse_args():
    parser = argparse.ArgumentParser(description='Downloads a specific version of RepoSense.jar from our repository.')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-r', '--release', action='store_true', help='Get RepoSense.jar from the latest release (Stable)')
    group.add_argument('-m', '--master', action='store_true', help='Get RepoSense.jar from the latest master (Beta)')
    group.add_argument('-t', '--tag', help='Get RepoSense.jar of a specific release version tag')
    group.add_argument('-c', '--commit', help='Get RepoSense.jar of a specific commit')

    parser.add_argument('-o', '--overwrite', action='store_true', help='Overwrite RepoSense.jar file, if exists. Default: false')

    return parser.parse_args()

def handle_specific_commit(commit):
    get_reposense_jar('https://api.github.com/repos/reposense/RepoSense/commits/' + commit, commit=commit)

def handle_specific_release(tag):
    get_reposense_jar('https://api.github.com/repos/reposense/RepoSense/releases/tags/' + tag, tag=tag)

def handle_latest_release():
    get_reposense_jar('https://api.github.com/repos/reposense/RepoSense/releases/latest')

def get_reposense_jar(url, tag=None, commit=None):
    response = requests.get(url)

    if tag and response.status_code == 404:
        print('Error, the provided tag does not exist!')
        exit(1)

    if commit and response.status_code in [404, 422]:
        print('Error, the provided commit does not exist!')
        exit(1)

    if response.status_code in [403, 500]:
        print('GitHub API has exceed the rate limit. Falling back to alternative method...')
        clone_and_make_reposense(tag=tag, commit=commit)
        return

    if commit:
        clone_and_make_reposense(commit=commit)
        return

    url = response.json()['assets'][0]['browser_download_url']
    download_file(url)

def clone_and_make_reposense(tag=None, commit=None):

    # Cleanup cached RepoSense folder
    shutil.rmtree('RepoSense', ignore_errors=True)

    command = \
    '''
    git clone 'https://github.com/reposense/RepoSense.git' &&
    cd RepoSense &&
    '''

    if tag:
        command += 'git checkout tags/{} -b deploy &&'.format(tag)
    elif commit:
        command +=  'git checkout {} -b deploy &&'.format(commit)

    command += \
    '''
    ./gradlew zipreport shadowjar &&
    mv build/jar/RepoSense.jar ../
    '''

    subprocess.check_call(command, shell=True)

def download_file(url):
    response = requests.get(url, allow_redirects=True)
    open(JAR_FILENAME, 'wb').write(response.content)

if __name__ == "__main__":
    args = parse_args()

    if os.path.exists(JAR_FILENAME) and args.overwrite is False:
        print(JAR_FILENAME + ' already exists. Quitting.')
        exit()

    if args.tag:
        handle_specific_release(args.tag)
        exit()

    if args.commit:
        handle_specific_commit(args.commit)
        exit()

    if args.master:
        clone_and_make_reposense()
        exit()

    # If no arguments are provided or --release
    handle_latest_release()
