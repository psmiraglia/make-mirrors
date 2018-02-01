# make-mirrors

1.	Obtain a [GitHub Personal Token] a [BitBucket App Password] and save
	them in `settings.py` as `GH_TOKEN` and `BB_TOKEN`. Put in `settings.py`
	also the GitHub/BitBucket username (`GH_USER`/`BB_USER`) and the BitBucket
	team (`BB_TEAM`).

2.	Create a virtualenv and install the requirements

		$ virtualenv -p python3 .venv
		$ source .venv/bin/activate
		$ pip install -r requirements.txt

3.	Enjoy...

		$ python gh2bb.py

[GitHub Personal Token]: https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line
[BitBucket App Password]: https://confluence.atlassian.com/bitbucket/app-passwords-828781300.html
