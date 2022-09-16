from netmiko import ConnectHandler, file_transfer
from getpass4 import getpass
import logging

api_bdds = {
    'device_type':'linux',
    'host':'10.244.136.135',
    'username': input('Username: '),
    'password': getpass('Password: '),
    'session_log': 'bdds_session_log.txt'
}
logging.basicConfig(filename='netmiko_logging', level=logging.DEBUG)
logger = logging.getLogger('netmiko')


#with ConnectHandler(**api_bdds) as net_connect:
bdds_connection = ConnectHandler(**api_bdds)

def progress_bar(filename, size, sent, peername=None):
    max_width = 50
    if isinstance(filename, bytes):
        filename = filename.decode()
    clear_screen = chr(27) + "[2J"
    terminating_char = "|"

    # Percentage done
    percent_complete = sent / size
    percent_str = f"{percent_complete*100:.2f}%"
    hash_count = int(percent_complete * max_width)
    progress = hash_count * ">"

    if peername is None:
        header_msg = f"Transferring file: {filename}\n"
    else:
        header_msg = f"Transferring file to {peername}: {filename}\n"

    msg = f"{progress:<50}{terminating_char:1} ({percent_str})"
    print(header_msg)
    print(msg)

def scp_get(ssh_conn):
    try:
        get_file = file_transfer(
            ssh_conn = ssh_conn,
            source_file = "backup_default_9.2.1-027.GA.bcn_202204201245.bak",
            dest_file = "Tmp/backup_file.txt",
            direction = "get",
            file_system='/data/backup',
            progress = progress_bar,
        )
        print('File downloaded successfully!')
    except:
        print('Failed to retrieve file')

def scp_put(ssh_conn):
    try:
        put_file = file_transfer(
            ssh_conn = ssh_conn,
            source_file =  'Tmp/put_file.txt',
            dest_file = 'put_file.txt',
            direction='put',
            file_system = '/tmp',
            progress = progress_bar,
        )
        print('File sent successfully!')
    except:
        print('File transfer failed')


scp_get(bdds_connection)
#scp_put(bdds_connection)
#output = bdds_connection.send_command('cat /etc/issue')
#print(output)
bdds_connection.disconnect()