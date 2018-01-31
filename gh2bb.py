import requests

from settings import GH_USER, GH_TOKEN
from settings import BB_USER, BB_TOKEN, BB_TEAM

GH_API = "https://api.github.com"
BB_API = "https://api.bitbucket.org/2.0"


def get_gh_repos():
    gh_repos = []
    url = "%s/user/repos" % GH_API
    params = {"visibility": "all", "affiliation": "owner"}
    auth = (GH_USER, GH_TOKEN)
    r = requests.get(url, auth=auth, params=params)
    while "next" in r.links:
        for repo in r.json():
            gh_repos.append((repo["name"], repo["clone_url"]))
        url = r.links["next"]["url"]
        r = requests.get(url, auth=auth)
    for repo in r.json():
        gh_repos.append((repo["name"], repo["clone_url"]))
    return gh_repos


def create_bb_repo(repo):
    url = "%s/repositories/%s/%s" % (BB_API, BB_TEAM, repo[0])
    auth = (BB_USER, BB_TOKEN)
    headers = {"content-type": "application/json"}
    data = {"scm": "git", "is_private": True, "fork_policy": "no_public_forks"}
    r = requests.get(url, auth=auth)
    if r.status_code == requests.codes.not_found:
        r = requests.post(url, auth=auth, headers=headers, json=data)


def push_gh_to_bb(repo):
    print("git clone %s" % repo[1])
    print(("git remote add bb https://%s:%s@bitbucket.org/%s/%s.git") %
          (BB_USER, BB_TOKEN, BB_USER, repo[0]))
    print("git push --mirror bb")


def make_mirrors(repos):
    for repo in repos:
        create_bb_repo(repo)
        push_gh_to_bb(repo)


def main():
    repos = get_gh_repos()
    repos = [("aaa", ""), ("bbb", ""), ("ccc", "")]
    make_mirrors(repos)

if __name__ == "__main__":
    main()
