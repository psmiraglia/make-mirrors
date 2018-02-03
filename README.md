# make-mirrors

1.  Obtain a [GitHub Personal Token] a [BitBucket App Password] and put
    them in `settings.py` as `GH_TOKEN` and `BB_TOKEN` (or define them as
    envvar). Put in `settings.py` (or define as envvar) also the
    GitHub/BitBucket username (`GH_USER`/`BB_USER`) and the BitBucket
    team (`BB_TEAM`).

2.  Run it

    a.    Create a virtualenv and install the requirements

        $ virtualenv -p python3 .venv
        $ source .venv/bin/activate
        $ pip install -r requirements.txt

    then

        $ python gh2bb.py

    b.    Build the Docker image

        $ docker build --tag psmiraglia/gh2bb .

    and run a container

        $ docker run -ti --rm --env-file settings.env psmiraglia/gh2bb

[GitHub Personal Token]: https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line
[BitBucket App Password]: https://confluence.atlassian.com/bitbucket/app-passwords-828781300.html
