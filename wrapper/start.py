import argparse
import requests
import zipfile
import logging

from os import environ, path, walk, sep
from traceback import format_exc

from subprocess import Popen, PIPE

GALLOPER_URL = environ.get("galloper_url", None)
TOKEN = environ.get("token", None)
BUCKET = environ.get("bucket")
NAME = environ.get("filename")
PROJECT = environ.get("project_id")
VIEWPORT = environ.get("view", "1920x1080")
ITERATIONS = environ.get("tests", "1")

parser = argparse.ArgumentParser(description='Browsertime Args Parser')
parser.add_argument('--browser', '-b', type=str, nargs="?", default='chrome', help='Broser to be tested, chrome and firefox are allowed')
parser.add_argument('--headers', '-H', type=str, nargs="*", help='Headers in construct of KEY:VALUE')
parser.add_argument('url', type=str, help='URL to be tested')

def get_headers():
    if TOKEN:
        return {'Authorization': 'Bearer {}'.format(TOKEN)}
    logging.warning("=====> Auth TOKEN is not set!")
    return None

def upload_artifacts(file_path):
    try:
        file = {'file': open(file_path, 'rb')}
        requests.post('{}/api/v1/artifacts/{}/{}/{}.json'.format(GALLOPER_URL, PROJECT, BUCKET, NAME),
                      files=file,
                      headers=get_headers())
    except Exception:
        from time import sleep
        print(format_exc())
        sleep(120)


def zipdir(p, zf):
    for root, dirs, files in walk(p):
        for file in files:
            if file.endswith(".jpg"):
                _p = sep.join(root.split("/")[-2:])
            elif file.endswith(".mp4"):
                _p = "video"
            else:
                _p = ""
            zf.write(path.join(root, file), arcname=path.join(_p, file))

def run():
    args = parser.parse_args()
    exec_string = '/start.sh --useSameDir --visualMetrics true --visuaElements true -o {} --skipHar -b {} --viewPort {} -n {} '.format(NAME, args.browser, VIEWPORT, int(ITERATIONS))
    if args.headers:
        exec_string += '-r {} '.format(' -r '.join(args.headers))
    exec_string += args.url
    p = Popen(exec_string, stdout=PIPE, stderr=PIPE, shell=True)
    p.communicate()
    zf = zipfile.ZipFile('/browsertime/{}.zip'.format(NAME), 'w', zipfile.ZIP_DEFLATED)
    zipdir('browsertime-results/', zf)
    zf.close()
    upload_artifacts('/browsertime/{}.zip'.format(NAME))


if __name__ == "__main__":
    run()