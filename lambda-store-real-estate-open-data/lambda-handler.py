import os
import zipfile
import boto3
from botocore.vendored.six import BytesIO
from botocore.vendored import requests


def main(event, context):
    print("I'm running!")

    s3 = boto3.resource('s3')

    def real_estate_info_downloader(year, season):
        # download real estate zip file
        res = requests.get(
            f"https://plvr.land.moi.gov.tw/DownloadSeason?season={str(year)}S{str(season)}&type=zip&fileName=lvr_landxml.zip")

        # unzip files
        # ref: https://stackoverflow.com/questions/10908877/extracting-a-zipfile-to-memory
        file = zipfile.ZipFile(BytesIO(res.content))  # unzip files

        for name in file.namelist():
            fp = file.read(name).decode("utf8", errors='replace')
            s3object = s3.Object(os.environ.get('BUCKET_NAME'), name)
            s3object.put(Body=(str(fp)))
            break

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": ""
        }

    return real_estate_info_downloader(101, 4)
