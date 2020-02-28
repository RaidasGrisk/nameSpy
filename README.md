# setup

``` bash
docker build -t social_score -f api-build/social_score/Dockerfile .
docker run -p 8080:8080 social_score:latest

docker build -t job_title -f api-build/job_title/Dockerfile .
docker run -p 8080:8080 job_title:latest

```
