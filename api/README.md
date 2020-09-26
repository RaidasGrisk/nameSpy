# setup envjob_title

Install [conda on Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-install-anaconda-on-ubuntu-18-04-quickstart)

``` bash
conda create --name names_api python=3.7
conda activate names_api
conda env update --file environment.yml

python -m spacy download lt_core_news_sm
python -m spacy download en_core_web_sm

```

# credentials and authentication

All of this is stored in private.py
``` bash
touch private.py

# twitter_keys
# proxy_dict
# ...
```

# serve
``` bash
python endpoint_get_social_score.py
python endpoint_get_job_title.py

```

# TODO

``` bash

Unresolved issues:
what if google results are in fact 0? example "sosicc cequel tycoonkingz"

```
