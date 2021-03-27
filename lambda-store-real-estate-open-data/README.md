
scripts for environment variables:

lambda:

aws lambda update-function-configuration \
  --function-name ${your-lambda-fn-name} \
  --environment "Variables={BUCKET_NAME=s3bucket-real-estate-record}"

cdk deploy:

export BUCKET_NAME=s3bucket-real-estate-record
