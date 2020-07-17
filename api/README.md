# setup envjob_title

Install conda:
https://www.digitalocean.com/community/tutorials/how-to-install-anaconda-on-ubuntu-18-04-quickstart

``` bash
conda create --name names_api python=3.7
conda activate names_api
conda env update --file environment.yml

python -m spacy download lt_core_news_sm
python -m spacy download en_core_web_sm

wget http://nlp.stanford.edu/software/stanford-corenlp-full-2018-02-27.zip
unzip stanford-corenlp-full-2018-02-27.zip

conda update --all
```

# do credential and auth stuff

All of this is stored in private.py
``` bash
touch private.py
echo "GOOGLE_KEYS = {}" >> private.py
echo "TWITTER_KEYS = {}" >> private.py
echo "proxy_dict = {}" >> private.py
```

# serve
``` bash
python endpoint_get_social_score.py
python endpoint_get_job_title.py

```

# TODO

``` bash

Two issues:
what if google rezults are in fact 0? example "sosicc cequel tycoonkingz"
intagram does not return user data. Not sure what triggers it.

Add explanation popups to landing page to exaplien web score and occupations

```
