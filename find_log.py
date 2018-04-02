import re
import os
import paramiko


def auth_data(host):
    return {"Login": 'login', "Password": 'password'}


def get_local_path():
    return os.path.abspath('../')


def get_file_path_by_mask(mask, host):
    path = None
    login = auth_data(host).get('Login')
    password = auth_data(host).get('Password')
    if len(mask) and len(host) and login and password:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=login, password=password, port=22)
        stdin, stdout, stderr = client.exec_command('find /var -name \'*{0}\''.format(mask))
        path = str(stdout.read(), "utf-8").replace('\n', '')
        client.close()
    return path


def download_log_file(local_path, mask, host):
    login = auth_data(host).get('Login')
    password = auth_data(host).get('Password')
    remote_path = get_file_path_by_mask(mask, host)
    remote_file_name = remote_path.split('/')[-1]
    if login and password and len(remote_path):
        transport = paramiko.Transport((host, 22))
        transport.connect(username=login, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.get(remote_path, local_path)
    return local_path + '\\' + str(remote_file_name)


def get_trace_log(id_string, path_to_file):
    list_of_trace = []
    num = 0
    with open(path_to_file) as text:
        rows = text.readlines()
    for i in range(len(rows)):
        if re.match(r'.*{0}.*'.format(id_string), rows[i]):
            break
    list_of_trace.extend(rows[num - 1:num - 3:-1])
    list_of_trace.extend(rows[num:num + 3:1])
    return list_of_trace


ip = "10.0.212.197"
id = 100500
full_path_to_down_file = download_log_file(get_local_path(), 'auth.log', ip)
if os.path.isfile(full_path_to_down_file):
    print(get_trace_log(id, full_path_to_down_file))
else:
    print("Файл не найден")
