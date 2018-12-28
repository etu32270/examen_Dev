"""Diagnose script for checking OS/hardware/python/pip/network.
"""
import platform, subprocess, sys, os
import socket, time
try:
    from urllib.request import urlopen
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
    from urllib2 import urlopen
import argparse


def parse_args():
    """Parse arguments."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Diagnose script for checking the current system.')
    choices = ['python', 'pip', 'mxnet', 'os', 'hardware', 'network']
    for choice in choices:
        parser.add_argument('--' + choice, default=1, type=int,
                            help='Diagnose {}.'.format(choice))
    parser.add_argument('--region', default='', type=str,
                        help="Additional sites in which region(s) to test. \
                        Specify 'cn' for example to test mirror sites in China.")
    parser.add_argument('--timeout', default=10, type=int,
                        help="Connection test timeout threshold, 0 to disable.")
    args = parser.parse_args()
    return args


URLS = {
    'GitHub': 'https://github.com/',
    'Facebook': 'https://www.facebook.com',
    'Henallux': 'https://henallux.be',
    'Google': 'https://google.be',
    'Amazon': 'https://www.amazon.fr',
    'Vmware': 'https://www.vmware.com',
}


def test_connection(name, url, timeout=10):
    """Simple connection test"""
    urlinfo = urlparse(url)
    start = time.time()
    try:
        ip = socket.gethostbyname(urlinfo.netloc)
    except Exception as e:
        print('Error resolving DNS for {}: {}, {}'.format(name, url, e))
        return
    dns_elapsed = time.time() - start
    start = time.time()
    try:
        _ = urlopen(url, timeout=timeout)
    except Exception as e:
        print("Error open {}: {}, {}, DNS finished in {} sec.".format(name, url, e, dns_elapsed))
        return
    load_elapsed = time.time() - start
    print("Timing for {}: {}, DNS: {:.4f} sec, LOAD: {:.4f} sec.".format(name, url, dns_elapsed, load_elapsed))


def check_python():
    print('----------Python Info----------')
    print('Version      :', platform.python_version())
    print('Compiler     :', platform.python_compiler())
    print('Build        :', platform.python_build())
    print('Arch         :', platform.architecture())


def check_pip():
    print('------------Pip Info-----------')
    try:
        import pip
        print('Version      :', pip.__version__)
        print('Directory    :', os.path.dirname(pip.__file__))
    except ImportError:
        print('No corresponding pip install for current python.')


def check_os():
    print('----------System Info----------')
    print('Platform     :', platform.platform())
    print('System       :', platform.system())
    print('Node         :', platform.node())
    print('Release      :', platform.release())
    print('Version      :', platform.version())


def check_hardware():
    print('----------Hardware Info----------')
    print('Machine      :', platform.machine())
    print('CPU          :', platform.processor())
    if sys.platform.startswith('darwin'):
        pipe = subprocess.Popen(('sysctl', '-a'), stdout=subprocess.PIPE)
        output = pipe.communicate()[0]
        for line in output.split(b'\n'):
            if b'brand_string' in line or b'features' in line:
                print(line.strip())
    elif sys.platform.startswith('linux'):
        subprocess.call(['lscpu'])
    elif sys.platform.startswith('win32'):
        subprocess.call(['wmic', 'cpu', 'get', 'name'])


def check_network(args):
    print('----------Network Test----------')
    print('IP:', socket.gethostbyname(socket.gethostname()))

    if args.timeout > 0:
        print('Setting timeout: {}'.format(args.timeout))
        socket.setdefaulttimeout(10)
    for name, url in URLS.items():
        test_connection(name, url, args.timeout)


if __name__ == '__main__':
    args = parse_args()
    if args.python:
        check_python()

    if args.pip:
        check_pip()

    if args.os:
        check_os()

    if args.hardware:
        check_hardware()

    if args.network:
        check_network(args)
