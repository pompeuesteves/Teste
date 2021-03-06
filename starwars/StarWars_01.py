import requests
import time
import logging as log
from google.cloud import storage
import os


def get_starwarspeople(numpeople):
    global response
    for i in range(3):
        try:
            response = requests.request("GET", url + numpeople + "/")
            break
        except requests.exceptions.RequestException:
            log.exception("Error {} when trying to get response!".format(str(i + 1)))
            time.sleep(1)

    if response.status_code == 200:
        starwars_list = response.json()
        return starwars_list
    else:
        print("Error from Job API")


def catchall():
    arraycast=[]
    for i in range(1,numcasts):
        print(str(i)+")")
        print(get_starwarspeople(str(i)))
        arraycast.append(get_starwarspeople(str(i)))
    return arraycast


def catchone(num_actor):
    actor = get_starwarspeople(str(num_actor))
    return actor


# Save request results to google storage
def save_applications_bucket(app_json):
    if os.environ.get('PRODUCTION'):
        client = storage.Client()
    else:
        client = storage.Client.from_service_account_json("../storage2bq.json")

    try:
        bucket = client.create_bucket("bucket_starwars")
    except:
        print("bucket já existe")

    bucket = client.get_bucket("bucket_starwars")
    file_name = 'people'
    blob = bucket.blob(file_name)
    blob.upload_from_string(str(app_json))


# Google function main method
def get_starwars():
    getthem = catchall()
    save_applications_bucket(getthem)
    return "Job done!"


# for local test
if __name__ == "__main__":
    # Get all people from StarWars
    # people--83, planets--60, starships--17
    url = "https://swapi.dev/api/people/"
    numcasts = 10
    get_starwars()
