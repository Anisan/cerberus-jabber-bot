# -*- coding: UTF-8 -*-
import xmpp
import os
import sys
import subprocess

name = 'Gerberus'
version='1.07'
os_info=None

def init(bot):
  bot.RegisterHandler('iq', _VersionCB, 'get', xmpp.NS_VERSION)
  return -1 #system

def _VersionCB(con, iq_obj):
        iq_obj = iq_obj.buildReply('result')
        qp = iq_obj.getTag('query')
        qp.setTagData('name', name)
        qp.setTagData('version', version)
        python_ver = 'Python: ' + sys.version.split(' ')[0]
        info = get_os_info() + ' ('+python_ver+')'
        qp.setTagData('os', info)
        con.send(iq_obj)
        raise xmpp.NodeProcessed

def is_in_path(command, return_abs_path=False):
    """
    Return True if 'command' is found in one of the directories in the user's
    path. If 'return_abs_path' is True, return the absolute path of the first
    found command instead. Return False otherwise and on errors
    """
    for directory in os.getenv('PATH').split(os.pathsep):
        try:
            if command in os.listdir(directory):
                if return_abs_path:
                    return os.path.join(directory, command)
                else:
                    return True
        except OSError:
            # If the user has non directories in his path
            pass
    return False

def get_output_of_command(command):
    try:
        child_stdin, child_stdout = os.popen2(command)
    except ValueError:
        return None

    output = child_stdout.readlines()
    child_stdout.close()
    child_stdin.close()

    return output

def temp_failure_retry(func, *args, **kwargs):
    while True:
        try:
            return func(*args, **kwargs)
        except (os.error, IOError, select.error), ex:
            if ex.errno == errno.EINTR:
                continue
            else:
                raise
                
distro_info = {
        'Arch Linux': '/etc/arch-release',
        'Aurox Linux': '/etc/aurox-release',
        'Conectiva Linux': '/etc/conectiva-release',
        'CRUX': '/usr/bin/crux',
        'Debian GNU/Linux': '/etc/debian_release',
        'Debian GNU/Linux': '/etc/debian_version',
        'Fedora Linux': '/etc/fedora-release',
        'Gentoo Linux': '/etc/gentoo-release',
        'Linux from Scratch': '/etc/lfs-release',
        'Mandrake Linux': '/etc/mandrake-release',
        'Slackware Linux': '/etc/slackware-release',
        'Slackware Linux': '/etc/slackware-version',
        'Solaris/Sparc': '/etc/release',
        'Source Mage': '/etc/sourcemage_version',
        'SUSE Linux': '/etc/SuSE-release',
        'Sun JDS': '/etc/sun-release',
        'PLD Linux': '/etc/pld-release',
        'Yellow Dog Linux': '/etc/yellowdog-release',
        # many distros use the /etc/redhat-release for compatibility
        # so Redhat is the last
        'Redhat Linux': '/etc/redhat-release'
}
        
def get_os_info():
    global os_info
    if os_info:
        return os_info
    if os.name == 'nt':
        # platform.release() seems to return the name of the windows
        ver = sys.getwindowsversion()
        ver_format = ver[3], ver[0], ver[1]
        win_version = {
                (1, 4, 0): '95',
                (1, 4, 10): '98',
                (1, 4, 90): 'ME',
                (2, 4, 0): 'NT',
                (2, 5, 0): '2000',
                (2, 5, 1): 'XP',
                (2, 5, 2): '2003',
                (2, 6, 0): 'Vista',
                (2, 6, 1): '7',
        }
        if ver_format in win_version:
            os_info = 'Windows' + ' ' + win_version[ver_format]
        else:
            os_info = 'Windows'
        os_info = os_info
        return os_info
    elif os.name == 'posix':
        executable = 'lsb_release'
        params = ' --description --codename --release --short'
        full_path_to_executable = is_in_path(executable, return_abs_path = True)
        if full_path_to_executable:
            command = executable + params
            p = subprocess.Popen([command], shell=True, stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE, close_fds=True)
            p.wait()
            output = temp_failure_retry(p.stdout.readline).strip()
            # some distros put n/a in places, so remove those
            output = output.replace('n/a', '').replace('N/A', '')
            os_info = output
            return output

        # lsb_release executable not available, so parse files
        for distro_name in distro_info:
            path_to_file = distro_info[distro_name]
            if os.path.exists(path_to_file):
                if os.access(path_to_file, os.X_OK):
                    # the file is executable (f.e. CRUX)
                    # yes, then run it and get the first line of output.
                    text = get_output_of_command(path_to_file)[0]
                else:
                    fd = open(path_to_file)
                    text = fd.readline().strip() # get only first line
                    fd.close()
                    if path_to_file.endswith('version'):
                        # sourcemage_version and slackware-version files
                        # have all the info we need (name and version of distro)
                        if not os.path.basename(path_to_file).startswith(
                        'sourcemage') or not\
                        os.path.basename(path_to_file).startswith('slackware'):
                            text = distro_name + ' ' + text
                    elif path_to_file.endswith('aurox-release') or \
                    path_to_file.endswith('arch-release'):
                        # file doesn't have version
                        text = distro_name
                    elif path_to_file.endswith('lfs-release'): # file just has version
                        text = distro_name + ' ' + text
                os_info = text.replace('\n', '')
                os_info = os_info
                return os_info

        # our last chance, ask uname and strip it
        uname_output = get_output_of_command('uname -sr')
        if uname_output is not None:
            os_info = uname_output[0] # only first line
            os_info = os_info
            return os_info
    os_info = 'N/A'
    os_info = os_info
    return os_info

