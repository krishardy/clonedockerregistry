import subprocess


def docker_pull(repo, version, fromurl):
    subprocess.run(["docker", "pull", "{0}/{1}:{2}".format(fromurl, repo, version)])

def docker_tag(repo, version, fromurl, tourl):
    subprocess.run(["docker", "tag", "{0}/{1}:{2}".format(fromurl, repo, version), "{0}/{1}:{2}".format(tourl, repo, version)])

def docker_push(repo, version, tourl):
    subprocess.run(["docker", "push", "{0}/{1}:{2}".format(tourl, repo, version)])
