import os
import time
from buildworker_scripts.utils.logutils import Log
import boto3
import botocore
import botocore.exceptions


class S3Session(object):
    def __init__(self, logger=None, bucket=None):
        self.s3client = None
        if logger is None:
            self.log = Log(name=__name__)
        else:
            self.log = logger
        self.bucket = bucket
        self.makeclient()

    def makeclient(self):
        self.s3client = boto3.Session().client('s3')

    def upload(self, file_name, key_name):
        if self.s3client is None:
            self.makeclient()
        try:
            self.s3client.upload_file(Bucket=self.bucket, Key=key_name, Filename=file_name)
        except botocore.exceptions.ClientError as e:
            err = e.response['Error']
            self.log.warn("{}/{}: {} {}".format(self.bucket, key_name, err['Code'], err['Message']))
            return False
        return True

    def download(self, key_name, file_name, quiet=True):
        if self.s3client is None:
            self.makeclient()
        try:
            info = self.s3client.head_object(Bucket=self.bucket, Key=key_name)
            self.s3client.download_file(Bucket=self.bucket, Key=key_name, Filename=file_name)
            if 'LastModified' in info:
                mtime = int(time.mktime(info['LastModified'].timetuple()))
                os.utime(file_name, (mtime, mtime))
        except botocore.exceptions.ClientError as e:
            err = e.response['Error']
            if quiet and err['Code'] == "404":
                self.log.debug(2, "not found: {}/{}".format(self.bucket, key_name))
            else:
                self.log.warn("{}/{}: {} {}".format(self.bucket, key_name, err['Code'], err['Message']))
            return False
        except OSError as e:
            if quiet:
                pass
            self.log.warn("os.utime({}): {} (errno {})".format(file_name, e.strerror, e.errno))
            return False
        return True

    def get_object_info(self, key_name, quiet=True):
        if self.s3client is None:
            self.makeclient()
        try:
            info = self.s3client.head_object(Bucket=self.bucket, Key=key_name)
        except botocore.exceptions.ClientError as e:
            err = e.response['Error']
            if quiet and err['Code'] == "404":
                self.log.debug(2, "not found: {}/{}".format(self.bucket, key_name))
            else:
                self.log.warn("{}/{}: {} {}".format(self.bucket, key_name, err['Code'], err['Message']))
            return None
        return info
