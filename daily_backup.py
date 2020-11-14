#!/usr/bin/env python3.7
import shutil, os, time, glob

backet = '___________'
datetime = time.strftime('%d-%m-%Y')
wp_path = '/var/www/html/smlzim.com'
path_to_wp_backup = '/tmp/wp_backup/'
path_to_sql_backup = '/tmp/dump/'
path_to_sql_archive = '/tmp/sql_backup/'
path_to_archive = '/tmp/sql_backup/' + datetime + 'sql'
wp_backup_path = path_to_wp_backup + datetime + 'wp'

def upload_cli(backup_file, backet_name, region):
    try:
        copy = 'aws s3 cp ' + backup_file + ' ' + 's3://' + backet_name + ' --region ' + region
        os.system(copy)
    except:
        print('[ERROR] Not download')
def mysql_dump(db_host, db_user, db_name):
    try:
        dumpcmd = "mysqldump -h " + db_host + " -u" + db_user + " " + "-B " + db_name + " > " + path_to_sql_backup + datetime + db_name + ".sql"
        os.system(dumpcmd)
    except Exception as e:
        print('[ERROR] Not loaded' + e)
def cleaning(folder):
    try:
        files = glob.glob(folder)
        for f in files:
            os.remove(f)
    except Exception as e:
        print('[INFO] Not to deleted')

databases = ['___', '___', '___', '___', '___']
for i in databases:
    mysql_dump('localhost', 'root', i)

shutil.make_archive(path_to_archive, 'zip', path_to_sql_backup)
upload_cli(path_to_archive + '.zip', backet + '/sql/', 'af-south-1')

shutil.make_archive(wp_backup_path, 'zip', wp_path)
upload_cli(wp_backup_path + '.zip', backet + '/wordpress/', 'af-south-1')

cleaning('/tmp/wp_backup/*')
cleaning('/tmp/sql_backup/*')
cleaning('/tmp/dump/*')
