# Location Services Demo

## Creating a Geofence collection

aws location create-geofence-collection --region ap-northeast-1 \
--collection-name summit \
--description "a geofence for my Sydney Summit talk" \
--pricing-plan RequestBasedUsage --output text

## Creating a Geofence

aws location put-geofence --region ap-northeast-1 \
--collection-name summit \
--geofence-id park \
--geometry file://enmore-park.json --output text

## Create a Tracker

aws location create-tracker --region ap-northeast-1 \
--description "my mobile phone" \
--pricing-plan RequestBasedUsage \
--tracker-name my-mobile --output text

## Associate Tracker Consumer

aws location associate-tracker-consumer --region ap-northeast-1 \
--consumer-arn arn:aws:geo:ap-northeast-1:${account_id}:geofence-collection/summit \
--tracker-name my-mobile --output text

## Create an IoT Thing

You will need to run the following bash script:

```bash
openssl pkcs12 -export -in summit.cert.pem -inkey summit.private.key -out private.otrp
```


## Update iot policy with the following

```json
    {
      "Effect": "Allow",
      "Action": [
        "iot:*"
      ],
      "Resource": [
        "*"
      ]
    }
```



# Create a rule

Again go to the console... I've called mine `sydneysummit` and hooked it up to the IoT Lambda which i will deploy
