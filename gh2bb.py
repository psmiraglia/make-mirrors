import logging
import requests
import shutil

from git import Repo
from settings import GH_USER, GH_TOKEN
from settings import BB_USER, BB_TOKEN, BB_TEAM

GH_API = "https://api.github.com"
BB_API = "https://api.bitbucket.org/2.0"


fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
sh.setFormatter(fmt)

log = logging.getLogger('gh2bb')
log.setLevel(logging.DEBUG)
log.addHandler(sh)


def get_gh_repos():
    gh_repos = []
    url = "%s/user/repos" % GH_API
    params = {"visibility": "all", "affiliation": "owner"}
    auth = (GH_USER, GH_TOKEN)
    log.info("Getting repos for '%s'" % GH_USER)
    r = requests.get(url, auth=auth, params=params)
    while "next" in r.links:
        for repo in r.json():
            gh_repos.append((repo["name"], repo["clone_url"]))
            log.debug("Got '%s'" % repo["name"])
        url = r.links["next"]["url"]
        r = requests.get(url, auth=auth)
    for repo in r.json():
        gh_repos.append((repo["name"], repo["clone_url"]))
        log.debug("Got '%s'" % repo["name"])
    return gh_repos


def create_bb_repo(repo):
    url = "%s/repositories/%s/%s" % (BB_API, BB_TEAM, repo[0])
    auth = (BB_USER, BB_TOKEN)
    headers = {"content-type": "application/json"}
    data = {"scm": "git", "is_private": True, "fork_policy": "no_public_forks"}
    r = requests.get(url, auth=auth)
    if r.status_code == requests.codes.not_found:
        r = requests.post(url, auth=auth, headers=headers, json=data)
        log.info("Created %s/%s on BitBucket" % (BB_TEAM, repo[0]))


def push_gh_to_bb(repo):
    #
    # clone repository in /tmp
    #
    #  git clone --mirror https://github.com/<user>/<repo>.git /tmp/<repo>
    #
    r_path = "/tmp/%s" % repo[0]
    log.info("Cloning %s in %s" % (repo[1], r_path))
    r = Repo.clone_from(repo[1], r_path, mirror=True)

    #
    # add BitBucket remote
    #
    #   git remote add bb https://<user>:<token>@bitbucket.org/<team>/<repo>.git
    #
    bb_url = (("https://%(user)s:%(token)s@bitbucket.org/%(team)s/%(repo)s.git") %
              {"user": BB_USER, "token": BB_TOKEN, "team": BB_TEAM, "repo": repo[0]})
    log.info("Setting 'bb' remote to '%s'" % bb_url)
    bb = r.create_remote("bb", bb_url)

    #
    # push
    #
    #   git push --mirror bb
    #
    log.info("Pushing '%s' to '%s'" % (repo[0], bb_url))
    bb.push(mirror=True)

    #
    # cleanup
    #
    #   rm -fr /tmp/<repo>
    #
    log.info("Deleting %s" % r_path)
    shutil.rmtree(r_path)


def make_mirrors(repos):
    for repo in repos:
        log.info("Mirroring %s" % repo[1])
        create_bb_repo(repo)
        push_gh_to_bb(repo)


def main():
    repos = get_gh_repos()
    make_mirrors(repos)

if __name__ == "__main__":
    main()
