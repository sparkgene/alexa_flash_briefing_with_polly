# feed_generator
Create rss feed for Flash Briefing API.
https://developer.amazon.com/alexa-skills-kit/flash-briefing

## configuration

set these Environment variables on lambda function.

### S3_DATA_BUCKET

Generated rss json is stored to this S3 bucket.

### RSS_FEED_URL

Original RSS feed url.

### TEXT_TO_SPEECH_LAMBDA

Lambda function which is invoked from this function after generating rss feed.

## Installation

```
cd feed_generator
pip install -r requirements.txt -t $(pwd)
```

compress all files in to zip.
```
zip -r func.zip .
```

This function use long time to convert data.
Set the timeout to 5 minuets.

This function is invoked from feed_generator.
