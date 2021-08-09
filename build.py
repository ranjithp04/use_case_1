from setup import for_mac
import sys
import hashlib
import requests
import glob, os


username = 'me'
password = 'secrets'

artifactory_url = 'https://artifactory.company.com/artifactory'

def get_md5(fin):
    md5 = hashlib.md5()
    with open(fin, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), ''):
            md5.update(chunk)
    return md5.hexdigest()

def get_sha1(fin):
    sha1 = hashlib.sha1()
    with open(fin, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), ''):
            sha1.update(chunk)
    return sha1.hexdigest()


def upload(fin):
    os.chdir("dist")
    for file in glob.glob(f"*{fin}*"):
        md5hash = get_md5(file)
        sha1hash = get_sha1(file)
        headers = {"X-Checksum-Md5": md5hash, "X-Checksum-Sha1": sha1hash}
        r = requests.put("{0}/{1}/{2}".format(artifactory_url, "yum-local", file),auth=(username,password), headers=headers, verify=False, data=open(file, 'rb'))
        return r


if __name__=="__main__":
    if sys.arg[1].os == "mac":
        for_mac(sys.arg[2])
    elif sys.arg[1].os == "win":
        for_mac(sys.arg[2])
    elif sys.arg[1].os == "upload":
        upload(sys.arg[2])
