'''
    To send notification to end user:
        1. Head over to the pushover website.
        https://pushover.net/api

        2. Register your application:
            Set its name and upload an icon, and get an API token in return (often referred to as APP_TOKEN in documentation).
        
        3. Once registered , replace USER_KEY with your Pushover User Key (which can be found on your dashboard) to which you are sending, and API_TOKEN with your application's API Token.

'''

import http.client, urllib
import time


def make_request_with_retry(retries=3, delay=5):
    for attempt in range(retries):
        try:
            conn = http.client.HTTPSConnection("api.pushover.net:443")
            conn.request("POST", "/1/messages.json",
                         urllib.parse.urlencode({
                             "token": "APP_TOKEN",
                             "user": "USER_KEY",
                             "message": "Wake up!!! ",
                             "sound": "Alien Alarm",
                             "priority": 1
                         }),
                         {"Content-type": "application/x-www-form-urlencoded"})

            response = conn.getresponse()
            data = response.read()
            # print(data)
            conn.close()
            break  # If successful, exit the loop

        except http.client.ResponseNotReady as e:
            # print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(delay)

        except Exception as e:
            # print(f"An error occurred: {e}")
            break
