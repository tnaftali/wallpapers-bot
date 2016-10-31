"""
This script uses the Vision API's label detection capabilities to find a label
based on an image's content.

To run the example, install the necessary libraries by running:

    pip install -r requirements.txt

Run the script on an image to get a label, E.g.:

    ./label.py <path-to-image>
"""

import argparse
import base64

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials


def main(photo_file):
    """Run a label request on a single image"""

    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('vision', 'v1', credentials=credentials)

    with open(photo_file, 'rb') as image:
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
        print response['responses'][0]['labelAnnotations']
        for i in range(len(response['responses'][0]['labelAnnotations'])):
            print response['responses'][0]['labelAnnotations'][i]['description']
            # label = response['responses'][i]['labelAnnotations'][i]['description']
            # print label
            # print('Found label: %s for %s' % (label, photo_file))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('image_file', help='The image you\'d like to label.')
    args = parser.parse_args()
    main(args.image_file)