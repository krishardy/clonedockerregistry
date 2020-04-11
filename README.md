# Docker Registy Cloner

The project takes the URLs of two registeries (a source registry and a destnation registry) and enumerates the repositories and tags that need to be migrated from the source to the destination.  The output is a BASH script that can be run to pull, tag and push the missing repositories and tags.

## Setup

`git clone https://github.com/krishardy/clonedockerregistry`

`pip3 install -r requirements.txt`

## Usage

```
usage: python3 -m clonedockerregistry [-h] -f FROMURL [-fv FROMVERSION] -fu FROMUSER
                        [-fp FROMPASS] -t TOURL [-tv TOVERSION] -tu TOUSER
                        [-tp TOPASS] [-k] [-m] [-o OUTSCRIPT]

Tool to migrate docker repositories from one registry to another.

optional arguments:
  -h, --help            show this help message and exit
  -f FROMURL, --fromurl FROMURL
                        The base url of the Docker Registry to migrate from
                        (https://mydomain/)
  -fv FROMVERSION, --fromversion FROMVERSION
                        The Docker Registry API version to migrate from.
                        Default=2
  -fu FROMUSER, --fromuser FROMUSER
                        The user to migrate from.
  -fp FROMPASS, --frompass FROMPASS
                        The password for the user to migrate from.
  -t TOURL, --tourl TOURL
                        The base url of the Docker Registry to migrate to
                        (https://mydomain/)
  -tv TOVERSION, --toversion TOVERSION
                        The Docker Registry API version version to migrate to.
                        Default=2
  -tu TOUSER, --touser TOUSER
                        The user to migrate to.
  -tp TOPASS, --topass TOPASS
                        The password for the user to migrate to.
  -k, --nocertverify    If set, TLS certificate validation is skipped.
  -m, --loadmanifests   Load manifests for all tags.
  -o OUTSCRIPT, --outscript OUTSCRIPT
                        The file to save the docker clone script to.
                        Default=clone.sh
```

## Example

```bash
python3 -m clonedockerregistry -f https://myoldregistry.mydomain.com:5000 -fu olduser -t https://mynewregistry.mydomain.com -tu newuser
```

This will connect to `myoldregistry.mydomain.com:5000` as `olduser` and prompt you for the password. It will then connect to `mynewregistry.mydomain.com` as `newuser` and prompt you for the password. Both registries will then be scanned. Repositories & tags that are in `myoldregistry.mydomain.com:5000` but not in `mynewregistry.mydomain.com` will be included in the `clone.sh` script that will be generated.

To complete the migration (pull images from the old registry, retag the images, and push them to the new registry), run `bash clone.sh`.

