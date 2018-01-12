# ASG Spincycle

Rotates instances in autoscaling groups that are using an outdated launch configuration

## Usage

The script assumes you have the below required environment variables set so boto3 can authenticate to AWS.  You can read more about the boto3 auth requirements [here](http://boto3.readthedocs.io/en/latest/guide/configuration.html)

* AWS_ACCESS_KEY_ID
* AWS_SECRET_ACCESS_KEY
* AWS_DEFAULT_REGION

```shell
pip install -r requirements.txt
python3 spincycle.py
```

The script takes the following command line arguments

```
usage: spincycle.py [-h] --asg-name ASG_NAME [--sleep-time SLEEP_TIME]

Rotate old instances from an ASG

optional arguments:
  -h, --help            show this help message and exit
  --asg-name ASG_NAME, -a ASG_NAME
                        The name of the ASG you want to rotate
  --sleep-time SLEEP_TIME, -s SLEEP_TIME
                        The time you want to wait between rotating instances
```

--sleep-time is technically not required and defaults to 600 seconds if not specified.

If you prefer to run the script via docker

```shell
docker run -it -e AWS_ACCESS_KEY_ID=xxx \
-e AWS_SECRET_ACCESS_KEY=yyy \
-e AWS_DEFULT_REGION=us-west-2 \
jensendw/asg-spincycle -a myawesomeasg -s 500
```


## Contributing

1. Fork it ( https://github.com/jensendw/asg-spincycle )
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create a new Pull Request
# asg-spincycle
