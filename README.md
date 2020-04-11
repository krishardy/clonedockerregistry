# Docker Registy Cloner

The project takes the URLs of two registeries (a source registry and a destnation registry) and enumerates the repositories and tags that need to be migrated from the source to the destination.  The output is a BASH script that can be run to pull, tag and push the missing repositories and tags.

## Setup

`git clone https://github.com/krishardy/clonedockerregistry`

`pip3 install -r requirements.txt`

## Example

```bash
python3 -m clonedockerregistry -f https://myoldregistry.mydomain.com:5000 -fu olduser -t https://mynewregistry.mydomain.com -tu newuser
```

This will connect to myoldregistry.mydomain.com:5000 as olduser and prompt you for the password. It will then connect to mynewregistry.mydomain.com as newuser and prompt you for the password. Both registries will then be scanned. Repositories & tags that are in myoldregistry.mydomain.com:5000 but not in mynewregistry.mydomain.com will be included in the clone.sh script that will be generated.  To do the migration, run `bash clone.sh`.

