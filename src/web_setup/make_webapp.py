#!/usr/bin/env python

import os
import argparse
from pprint import PrettyPrinter
from string import Template


def check_dir(dirname):
    if os.path.exists(dirname):
        if os.path.isdir(dirname):
            return 1
        else:
            return 2
    else:
        return 0


def make_dir(dirname):
    retval = check_dir(dirname)
    if retval == 0:
        print("Creating directory '{}'".format(dirname))
        os.makedirs(dirname)
    elif retval == 1:
        print("Directory '{}' exists, doing nothing".format(dirname))
    else:
        print("'{}' exists but is NOT a directory, exiting".format(dirname))
        sys.exit(-1)


def init_dirs(basename):
    make_dir(os.path.join(basename, 'run'))
    make_dir(os.path.join(basename, 'logs'))
    make_dir(os.path.join(basename, 'conf'))


def init_logs(basename):
    logdir = os.path.join(basename, 'logs')

    # initialize supervisord app log file
    logfile = os.path.join(logdir, 'gunicorn.log')
    print("Creating log file {}".format(logfile))
    open(logfile, 'a').close()

    # initialize nginx access log file
    logfile = os.path.join(logdir, 'nginx-access.log')
    print("Creating log file {}".format(logfile))
    open(logfile, 'a').close()


def get_test_mapping():
    return {
        "BASEDIR": "/webapps/",
        "APPNAME": "my_new_app",
    }


def load_template(template):
    template_path = os.path.dirname(os.path.realpath(__file__))
    template_name = os.path.join(template_path, template + ".conf.template")
    if not os.path.exists(template_name):
        print("template '{}' NOT found, exiting".format(template_name))
        sys.exit(-1)
    print("opening template {}".format(template_name))
    f = open(template_name, "rt")
    try:
        return Template(f.read())
    finally:
        f.close()


def write_config(config_name, content, maps):
    base = maps['BASEDIR']
    app = maps['APPNAME']
    target_dir = os.path.join(base, 'conf')
    target_file = os.path.join(target_dir, "{}-{}.conf".format(app, config_name))
    print("writing config file - {}".format(target_file))
    f = open(target_file, "wt")
    try:
        f.write(content)
    finally:
        f.close()


def make_config(config_name, maps):
    tmpl = load_template(config_name)
    content = tmpl.substitute(maps)
    write_config(config_name, content, maps)


def get_app_name():
    current_dir, folder_name = os.path.split(os.getcwd())

    while folder_name:
        check_path = os.path.join(current_dir, folder_name, 'src')
        if os.path.isdir(check_path):
            return folder_name
        current_dir, folder_name = os.path.split(current_dir)

    return os.path.split(os.getcwd())[1]


def get_base_name():
    current_dir, folder_name = os.path.split(os.getcwd())

    while folder_name:
        check_path = os.path.join(current_dir, folder_name, 'src')
        if os.path.isdir(check_path):
            return os.path.join(current_dir, folder_name)
        current_dir, folder_name = os.path.split(current_dir)

    return os.path.split(os.getcwd())[0]


def parse_arguments():
    parser = argparse.ArgumentParser(description="Script to create webapps")

    parser.add_argument('SERVERNAME', type=str, metavar="ServerName",
                        help='server hostname to respond to in nginx',
                        )

    parser.add_argument('-b', '--basedir', default=get_base_name(),
                        metavar='basedir', type=str, dest='BASEDIR',
                        help='base directory of all webapps [default={}]'.format(os.getcwd()),
                        )
    parser.add_argument('-A', '--appname',
                        default=get_app_name(),
                        type=str, dest='APPNAME',
                        help='name of the application to initialize',
                        )
    parser.add_argument('-t', '--test',
                        action="store_true",
                        help='display gathered data'
                        )

    return vars(parser.parse_args())


def validate_data(data):
    base = os.path.join(os.path.normpath(data['BASEDIR']), '')
    if not (os.path.exists(base) and os.path.isdir(base)):
        print("directory '{}' does not exist".format(base))
        sys.exit(-2)
    data['BASEDIR'] = base

    print("Appname = '{}'".format(data['APPNAME']))

    djangodir = find_manage_py(data['BASEDIR'])
    data['DJANGODIR'] = djangodir

    data['USERNAME'] = os.environ.get('USER')
    data['VENVDIR'] = os.environ.get('VIRTUALENVWRAPPER_HOOK_DIR')

    return data


def print_reminders(data):
    appname = data['APPNAME']
    basedir = os.path.join(os.path.normpath(data['BASEDIR']), '')
    appdir = os.path.join(basedir, 'src', appname, '')
    settingsdir = os.path.join(appdir, appname, '')
    servername = data['SERVERNAME']
    print("""\n\nREMINDERS: (as root, do the following)
(1)  Create links for config files from {BASEDIR}conf 
     (a) {APPNAME}-supervisord.conf into /etc/supervisor/conf.d/
     (b) {APPNAME}-nginx.conf into /etc/nginx/conf.d/
     excute:
        sudo ln -s {BASEDIR}conf/{APPNAME}-supervisord.conf /etc/supervisor/conf.d/
        sudo ln -s {BASEDIR}conf/{APPNAME}-nginx.conf /etc/nginx/conf.d/
(2)  Add '{SERVERNAME}' to ALLOWED_HOSTS in settings.py
     edit {SETTINGSDIR}settings.py

(3)  Restart or reload supervirsord
     service supervisord reload 

(4)  Restart or reload nginx 
     service nginx reload

""".format(APPNAME=appname,
           BASEDIR=basedir,
           SETTINGSDIR=settingsdir,
           SERVERNAME=servername)
          )


def find_manage_py(basedir):
    for root, dirs, files in os.walk(basedir):
        if 'manage.py' in files:
            return root
    return basedir


def main():
    pp = PrettyPrinter()
    data = parse_arguments()
    data = validate_data(data)

    pp.pprint(data)
    if data['test']:
        return 0

    init_dirs(data['BASEDIR'])
    init_logs(data['BASEDIR'])

    # tmpl = load_template("supervisord")
    # data = get_test_mapping()

    # content = tmpl.substitute(data)

    # write_config("supervisord", content, data)

    make_config("supervisord", data)
    make_config("nginx", data)
    make_config("gunicorn", data)

    print_reminders(data)


if __name__ == "__main__":
    import sys

    sys.exit(main())
