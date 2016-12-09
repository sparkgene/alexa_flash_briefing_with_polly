# audio_generator
Create audio data with Amazon Polly.
https://aws.amazon.com/polly/

For now, boto3 is not the newest version on Lambda function environment.
So we need to include boto3(version 1.4.2) with the lambda functions code.

## configuration

set these Environment variables on lambda function.

### AUDIO_BUCKET

Generated audio data is stored to this S3 bucket.

## Installation

```
cd audio_generator
pip install -r requirements.txt -t $(pwd)
```

compress all files in to zip.
```
zip -r func.zip .
```

This function use long time to convert data.
Set the timeout to 5 minuets.

This function is invoked from feed_generator.
