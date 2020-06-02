gcloud run deploy namespy-api-gateway \
    --image="gcr.io/endpoints-release/endpoints-runtime-serverless:2" \
    --allow-unauthenticated \
    --platform managed \
    --project=namesapi-1581010760883


<!-- This returns config-id which must be passed to the next steps -->
gcloud endpoints services deploy openapi-run.yaml \
  --project namesapi-1581010760883


chmod +x gcloud_build_image
./gcloud_build_image -s namespy-api-gateway-mu7u3ykctq-lz.a.run.app \
    -c 2020-05-28r6 -p namesapi-1581010760883


gcloud run deploy namespy-api-gateway \
  --image="gcr.io/namesapi-1581010760883/endpoints-runtime-serverless:namespy-api-gateway-mu7u3ykctq-lz.a.run.app-2020-05-28r6" \
  --allow-unauthenticated \
  --platform managed \
  --project=namesapi-1581010760883
