import os
import base64
import cloudinary.uploader, cloudinary.api
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import random

cloudinary.config(
    cloud_name='dmyufekev',
    api_key='166958157613447',
    api_secret='086xPNR_jROA04gcDSdRnqxf2iE'
)


def get_labels(photo_file):
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('vision', 'v1', credentials=credentials)
    labels = []

    with open(photo_file, 'r') as image:
        image_content = base64.b64encode(image.read())
        service_request = service.images().annotate(body={
            'requests': [{
                'image': {
                    'content': image_content.decode('UTF-8')
                },
                'features': [{
                    'type': 'LABEL_DETECTION',
                    'maxResults': 10
                }]
            }]
        })
        response = service_request.execute()
        for i in range(len(response['responses'][0]['labelAnnotations'])):
            tag = response['responses'][0]['labelAnnotations'][i]['description']
            for word in tag.split(' '):
                labels.append(word)
    return labels


url = '/Users/Toby/Projects/bot/WallpapersBot/resources'
for file in os.listdir(url):
    if file.endswith('.jpg') or file.endswith('.png'):
        full_path = url + '/' + file
        id = str(random.randint(100000, 999999))
        labels = get_labels(full_path)
        cloudinary.uploader.upload(full_path, public_id=id)
        for label in labels:
            result = cloudinary.uploader.add_tag(label, id)
        os.remove(full_path)
        print file + ' uploaded and deleted'
