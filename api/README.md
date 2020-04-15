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
```

# serve
``` bash
python endpoint_get_social_score.py
python endpoint_get_job_title.py

```

# TODO

``` bash

Natalija Bunke IG followers	16800
Karolina Meschino IG followers	288800

Edmundas Balčikonis vs Edmundas Balcikonis

language option in occupation API       cannot do as this activates google scrpae detection
carl hust occupation API error    OK
IG user info scrape

github landing page logo and description    OK
DOCS page on WEBSITE

hard match findall fails with iter exception: melissa respondek
Totally lost, now its working, can it be that titles have to be sorted alphabetically?

Alina Kalenkovic vs Alina Kalenkovič list assignment out of range error!

```
