import requests
import json
import logging

logger = logging.getLogger(__name__)


def load(url, user, password, nocertverify=False, loadmanifests=False):
    result = {}

    base_url = url.rstrip('/') + "/v2/"
    catalog_url = base_url + "_catalog"
    catalog_resp = requests.get(catalog_url, auth=(user, password), verify=nocertverify)
    if catalog_resp.status_code != 200:
        raise Exception("200 not returned for {}".format(catalog_url))
    catalog = json.loads(catalog_resp.text)
    if isinstance(catalog.get("repositories"), list):
        for repo in catalog["repositories"]:
            result[repo] = {}
            tags_url = base_url + "{}/tags/list".format(repo)
            tags_resp = requests.get(tags_url, auth=(user, password), verify=nocertverify)
            if tags_resp.status_code != 200:
                raise Exception("200 not returned for {}".format(tags_url))
            tags = json.loads(tags_resp.text)
            if isinstance(tags.get("tags"), list):
                for tag in tags["tags"]:
                    manifests = None
                    if loadmanifests:
                        manifest_url = base_url + "{0}/manifests/{1}".format(repo, tag)
                        manifest_resp = requests.get(manifest_url, auth=(user, password), verify=nocertverify)
                        if manifest_resp.status_code != 200:
                            raise Exception("200 not returned for {}".format(manifest_url))
                        manifests = json.loads(manifest_resp.text)
                    result[repo][tag] = manifests
    return result