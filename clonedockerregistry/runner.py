import asyncio
import json
import urllib
import clonedockerregistry.catalogs as cdr_catalogs

def do_migration(fromurl, fromversion, fromuser, frompass, tourl, toversion, touser, topass, script="clone.sh",
nocertverify=False, loadmanifests=False):
    # Load catalogs in parallel
    #fromtask = asyncio.create_task(load_catalog(fromurl, fromversion, fromuser, frompass, nocertverify: nocertverify))
    #totask = asyncio.create_task(load_catalog(tourl, toversion, touser, topass, nocertverify: nocertverify))

    print("Loading registry information...")
    from_task, to_task = asyncio.run(load_catalogs(fromurl, fromversion, fromuser, frompass, tourl, toversion, touser, topass,
nocertverify=False, loadmanifests=False))

    from_repos = from_task.result()
    to_repos = to_task.result()

    manifest = {}

    missing_repositories = list(set(from_repos.keys()).difference(to_repos.keys()))
    for repo in missing_repositories:
        from_versions = from_repos[repo].keys()
        to_versions = []
        if repo in to_repos:
            to_versions = to_repos[repo].keys()
        missing_versions = list(set(from_versions).difference(to_versions))
        manifest[repo] = missing_versions

    from_uri = urllib.parse.urlparse(fromurl)
    to_uri = urllib.parse.urlparse(tourl)
    with open(script, "w") as fh:
        fh.write("#!/bin/bash\n")
        fh.write("FROM={}\n".format(from_uri.netloc))
        fh.write("TO={}\n".format(to_uri.netloc))
        for repo in manifest:
            for version in manifest[repo]:
                fh.write("docker pull $FROM/{0}:{1}\n".format(repo, version))
                fh.write("docker tag $FROM/{0}:{1} $TO/{0}:{1}\n".format(repo, version))
                fh.write("docker push $TO/{0}:{1}\n".format(repo, version))
                
    print("Cloning script saved as {}".format(script))

    #migrateversion(fromurl, fromversion, fromuser, frompass, tourl, toversion, touser, topass, repo, version)


async def load_catalogs(fromurl, fromversion, fromuser, frompass, tourl, toversion, touser, topass,
nocertverify=False, loadmanifests=False):
    fromtask = asyncio.create_task(
        load_catalog(fromurl, fromversion, fromuser, frompass, nocertverify=nocertverify)
    )
    totask = asyncio.create_task(
        load_catalog(tourl, toversion, touser, topass, nocertverify=nocertverify)
    )
    await fromtask
    await totask
    return (fromtask, totask)


async def load_catalog(url, version, user, password, nocertverify):
    handlers = {
        1: cdr_catalogs.v1.load,
        2: cdr_catalogs.v2.load
    }
    if version not in handlers:
        raise ValueError("Version {} cannot be handled.".format(version))
    return handlers[version](url, user, password, nocertverify=nocertverify)


def migrateversion(fromurl, fromversion, fromuser, frompass, tourl, toversion, touser, topass, repo, version, nocertverify=False):
    docker_pull(repo, version, fromurl, fromuser, frompass)
    docker_tag(repo, version, fromurl, tourl)
    docker_push(repo, version, tourl, fromuser, frompass)
