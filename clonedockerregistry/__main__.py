import sys
import argparse
import logging
import getpass
import clonedockerregistry.runner as cdr_runner

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser("dockerregmigrate", description="Tool to migrate docker repositories from one registry to another.")
    parser.add_argument("-f", "--fromurl", type=str, required=True, help="The base url of the Docker Registry to migrate from (https://mydomain/)")
    parser.add_argument("-fv", "--fromversion", type=int, default=2, help="The Docker Registry API version to migrate from. Default=2")
    parser.add_argument("-fu", "--fromuser", type=str, required=True, help="The user to migrate from.")
    parser.add_argument("-fp", "--frompass", type=str, required=False, help="The password for the user to migrate from.")
    parser.add_argument("-t", "--tourl", type=str, required=True, help="The base url of the Docker Registry to migrate to (https://mydomain/)")
    parser.add_argument("-tv", "--toversion", type=int, default=2, help="The Docker Registry API version version to migrate to. Default=2")
    parser.add_argument("-tu", "--touser", type=str, required=True, help="The user to migrate to.")
    parser.add_argument("-tp", "--topass", type=str, required=False, help="The password for the user to migrate to.")
    parser.add_argument("-k", "--nocertverify", default=False, action="store_const", const=True, help="If set, TLS certificate validation is skipped.")
    parser.add_argument("-m", "--loadmanifests", default=False, action="store_const", const=True, help="Load manifests for all tags.")
    parser.add_argument("-o", "--outscript", type=str, default="clone.sh", help="The file to save the docker clone script to. Default=clone.sh")

    args = parser.parse_args()
    
    frompass = args.frompass
    if frompass is None or len(frompass) == 0:
        frompass = getpass.getpass("Password for {0} for {1}: ".format(args.fromuser, args.fromurl))

    topass = args.topass
    if topass is None or len(topass) == 0:
        topass = getpass.getpass("Password for {0} for {1}: ".format(args.touser, args.tourl))

    cdr_runner.do_migration(fromurl=args.fromurl, fromversion=args.fromversion, fromuser=args.fromuser,
        frompass=frompass, tourl=args.tourl, toversion=args.toversion, touser=args.touser,
        topass=topass, nocertverify=args.nocertverify, loadmanifests=args.loadmanifests, script=args.outscript)

if __name__ == "__main__":
    sys.exit(main())