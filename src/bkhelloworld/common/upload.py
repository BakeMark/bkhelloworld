#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Lou Viannay <lou@islandtechph.com>
from __future__ import print_function

import logging
from io import StringIO
import os
import ftplib
import tempfile

logger = logging.getLogger(__name__)


class FileDOS(object):
    def __init__(self, fileobject):
        self.fileobj = fileobject

    def readline(self, size, **kwargs):
        line = self.fileobj.readline(size, **kwargs)
        if line == "":
            return ""
        print(line)
        line = line.strip()
        line = line + "\r\n"
        return line


class FTPUloader(object):
    def __init__(self,
                 host=None,
                 port=21,
                 user=None,
                 password=None,
                 remote_dir=None,
                 default_filename=None,
                 keep_files=True,
                 output_dir="."
                 ):
        self.ftp = ftplib.FTP()
        self.ftp.set_debuglevel(logging.DEBUG)
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.remote_dir = remote_dir
        self.connected = False
        self.logged_in = False
        self.default_filename = ""
        self.set_default_filename(default_filename)
        self.filename = ""
        self.keep_files = keep_files
        self.output_folder = os.path.abspath(output_dir)
        assert os.path.exists(self.output_folder), \
            "FTP directory does not exist - {}".format(self.output_folder)

    def is_connected(self):
        return self.connected

    def is_logged_in(self):
        return self.logged_in

    def connect(self, host=None, port=None):
        if port:
            self.port = port
        if host:
            self.host = host
        if self.host is None:
            logger.error("FTP Error - No Host")
            return False
        try:
            self.ftp.connect(
                host=self.host,
                port=self.port,
                timeout=10,
            )
            self.connected = True
        except ftplib.all_errors as e:
            logger.error("ftp error: ({}) - '{}'".format(
                e.errno,
                e.strerror,
            ))
            logger.error("{}".format(str(e)))
            print("{}".format(str(e)))
        return self.connected

    def set_username(self, username):
        if username:
            self.user = username

    def set_password(self, password):
        if password:
            self.password = password

    def login(self, username=None, password=None):
        self.set_username(username)
        self.set_password(password)

        if not self.is_connected():
            self.connect()

        if not self.connected:
            return self.connected

        try:
            self.logged_in = False
            self.ftp.login(self.user, self.password)
            self.logged_in = True
            self.ftp.set_pasv(True)
        except ftplib.all_errors as e:
            # print e.args
            logger.error("{}".format(e))
        return self.logged_in

    def set_remote_dir(self, remote_dir):
        if remote_dir:
            self.remote_dir = remote_dir

    def set_filename(self, filename):
        if filename:
            self.filename = filename
        else:
            self.filename = self.default_filename

    def set_default_filename(self, default_filename):
        if default_filename:
            self.default_filename = default_filename

    def cwd(self, remote_dir):
        self.set_remote_dir(remote_dir)
        logger.debug("changing to - '{}'".format(self.remote_dir))
        result = False
        try:
            self.ftp.cwd(self.remote_dir)
            result = True
        except ftplib.all_errors as e:
            logger.error("FTP Error: {}".format(e))

        return result

    def upload_string(self, content, filename):
        with tempfile.NamedTemporaryFile(
                "wb", delete=False,
                dir=self.output_folder) as f:
            f.write(content)
            name = f.name
        # fobj = StringIO.StringIO()
        # fobj.write(content)
        # fobj.seek(0)
        print("FTP Temp File  = {}".format(name))
        with open(name, "rU") as f:
            result = self.upload_fileobj(f, filename)

        if not self.keep_files:
            os.remove(name)

        return result

    # noinspection PyMethodMayBeStatic
    def callback_block(self, block):
        print("ftp callback: {} ({}) {}".format(
            type(block), len(block), block.strip()
        ))

    def upload_fileobj(self, fileobj, filename=None):
        result = False
        self.set_filename(filename)
        if not self.filename and self.default_filename:
            self.filename = self.default_filename
        if not self.filename:
            self.filename = fileobj.name
        if not self.filename:
            logger.error("FTP Error: upload filename is empty")
            return False
        try:
            logger.info("Uploading - {}".format(self.filename))
            store_cmd = 'STOR {}'.format(self.filename)
            result = self.ftp.storlines(
                store_cmd, FileDOS(fileobj),
                callback=self.callback_block)
        except ftplib.all_errors as e:
            logger.error("FTP Error: {}".format(e))
        return result

    def upload_file(self, filename):
        result = False
        basename = os.path.basename(filename)
        try:
            with open(filename, "rb") as fobj:
                result = self.upload_fileobj(fobj, basename)
        except ftplib.all_errors as e:
            logger.error("FTP Error: {}".format(e))
        return result

    def close(self):
        logger.info("closing FTP connection")
        self.ftp.quit()


def upload(host, data_dict, port=21, use_logger=logger):
    payload = data_dict['msi_data']
    target_fname = data_dict['msi_fname']
    username = data_dict['ftp_user']
    password = data_dict['ftp_password']

    uploader = FTPUloader(
        host=host,
        user=username,
        password=password,
        port=port,
    )
    success = False
    try:
        use_logger.info("connecting to {}".format(host))
        if uploader.connect():
            use_logger.info("connected, logging in as '{}'".format(username))
            if uploader.login():
                uploader.upload_string(payload, target_fname)
                success = True

    finally:
        uploader.close()

    return success


def test2():
    obj = FTPUloader(
        # host='ftpserver',
        # host = '10.111.0.14',
        # port=21,
        host='devserver',
        port=21,
        user='ftp_user',
        password='ftp_user',
    )
    try:
        logger.info("Connecting")
        obj.connect()
        logger.info("logging in")
        if obj.login():
            obj.cwd('\\NDS\\TEMPORARY\\WEST\\I')
            obj.upload_string("This is a test\nwith lines\n", 'testfile.txt')
            obj.upload_file("/home/lou/test.csv")

    finally:
        obj.close()

    return 0


def test1():
    output = StringIO()
    output.write("This is a test string\n")
    output.seek(0)

    ftp = ftplib.FTP()
    ftp.connect(host='ftpserver')
    ftp.login(user='lou', passwd='pass1234')
    ftp.cwd('/home/')
    # noinspection PyTypeChecker
    ftp.storbinary('stor test.txt', output)
    ftp.quit()

    return 0


def main():
    logging.basicConfig(level=logging.DEBUG)
    test2()
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
