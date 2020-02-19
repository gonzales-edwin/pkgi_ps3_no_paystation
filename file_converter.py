#!/usr/bin/python3
import csv
import os
import requests
import ftplib
import sys

base_path = os.path.dirname(os.path.abspath(__file__))
username = 'anonymous'
pkgi_ps3_remote_dir = '/dev_hdd0/game/NP00PKGI3/USRDIR'


def join_path(file_name): return os.path.join(base_path, file_name)


output_file = os.path.join(base_path, 'pkgi.txt')
remote_files = {
    'PS3_GAMES.tsv': 'https://nopaystation.com/tsv/PS3_GAMES.tsv',
    'PS3_DLCS.tsv': 'https://nopaystation.com/tsv/PS3_DLCS.tsv',
    'PS3_THEMES.tsv': 'https://nopaystation.com/tsv/PS3_THEMES.tsv',
    'PS3_AVATARS.tsv': 'https://nopaystation.com/tsv/PS3_AVATARS.tsv'
}
downloaded_tsv_files = {
    'pkgi_games.txt': join_path('PS3_GAMES.tsv'),
    'pkgi_dlcs.txt': join_path('PS3_DLCS.tsv'),
    'pkgi_themes.txt': join_path('PS3_THEMES.tsv'),
    'pkgi_avatars.txt': join_path('PS3_AVATARS.tsv')
}


pkgi_formated_db = []


def get_updated_games():
    for name, url in remote_files.items():
        r = requests.get(url)
        data = r.text.replace('\n', '')
        with open(name, 'w', encoding='utf8') as f:
            f.write(data)


def format_downloaded_tsv(tsv_file):
    with open(tsv_file, 'r', encoding='utf8') as file:
        lines = csv.reader(file)
        for num, line in enumerate(lines):
            new_line = line[0].split('\t')
            try:
                content_id = new_line[5]
                flags = 0
                name = new_line[2]
                description = ''
                rap = new_line[4]
                url = new_line[3]
                size = new_line[8]
                checksum = ''
                line = f'{content_id},{flags},{name},{description},{rap},{url},{size},{checksum}'
                pkgi_formated_db.append(line)
                print(line)
            except IndexError:
                print('line cannot be read')
                continue


def write_to_file(db_file):
    with open(db_file, 'w') as file:
        for line in pkgi_formated_db:
            file.write(f'{line}\n')


def upload_pkgi_db(file_name):
    ftp = ftplib.FTP(str(ps3_ip))
    ftp.login(username)
    ftp.cwd(pkgi_ps3_remote_dir)
    ftp_upload = open(file_name, 'rb')
    ftp.storlines(f'STORE {file_name}', ftp_upload)
    ftp.close()


get_updated_games()
for pkgi_file, tsv_file in downloaded_tsv_files.items():
    format_downloaded_tsv(tsv_file)
    write_to_file(pkgi_file)
    pkgi_formated_db.clear()
    try:
        if sys.argv[1] == '--ftp':
            try:
                ps3_ip = input('Enter PS3 FTP ip address: \n')
                upload_pkgi_db(pkgi_file)
            except:
                print('An error occurred while connecting the ps3 via FTP, please load the databases via USB stick.')
    except IndexError:
        print('''You did not use the ftp flag, script will load files to your local directory only.
If you want the script to automatically upload your files to the ps3 use the following format:
python file_converter --ftp''')
        continue
