# skbinday

Stockport Bin Days Notification Service.

Due to the 'rona the schedule has changed from that which was published. Some councils do offer an email service, Stockport Council doesn't currently. 

We retrieve the unique identifier for our address and setup a cron for Thursdays that emails out the next day's collections. 

YMMV with different parts of the area having different collection days but the process will still work, just choose a different day to run it.

## Environment variables

### Settings

```
export FROM_ADDRESS=noreply@example.com
```

### Mailgun

```
export MAILGUN_API_KEY=key-fo
export MAILGUN_DOMAIN=example.com
```

### Recipients

```
export SKBINDAY_RECIPIENTS=you@example.com
```

or for multiple recipients:

```
export SKBINDAY_RECIPIENTS=you@example.com,other@example.com
```

## Arguments

Requires the URN for your address which you can retrieve from the URL after submitting your address on the Council's website.

https://www.stockport.gov.uk/find-your-collection-day

```bash
$ skbinday -u 1000000042
```

## Installation

With a venv or clone the repo and run:

```bash
$ python3 setup.py install
```

Optional cron entry, the bash script merely sets the environment variables and calls `skbinday` with the appropriate URN.

```
0 9 * * THU /opt/skbinday/wrapper.sh
```
