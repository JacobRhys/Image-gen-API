# Team 21 Image API
the image API has 4 functions
## Functions overview 

**request-image** - requests an image of a prompt to be generated and returns an image_ID
**status** - returns the status of an image_ID
**all-status** - returns a list of all the image_ID requested from your IP, and their statuses.
**get-image** - returns the image image_ID, then it erases the image from the status database and deletes it. can only be run on one image once.

The functions **status**, **all-status** and  **get-image** only work if you call them from the same IP as the image was generated for.

## How to use request-image

If you go to e.g. <u>127.0.0.1:5000/request-image/A ferari</u> it will add an image to the request list and return the image_ID. This looks something like this: 
**d4810a62-4287-4154-8f7f-0d567870381e**.


## How to use status

If you go to e.g. <u>127.0.0.1:5000/status/d4810a62-4287-4154-8f7f-0d567870381e</u> and your IP address is the same as the IP where that image request comes from, it will return the image status either "Genirated" or  "Not Genirated". This looks something like this:
**Generated**
If your IP address is different from the IP where the image request comes from, or it can't find the requested image (remember **get-image will delete the image**) it will return "Invalid request"

## How to use all-status

If you go to e.g. <u>127.0.0.1:5000/all-status</u> it will return a List of all the requests from your ip and their status. The requests are separated by a comma and the image_ID and status are separated by a ":". This looks something like this:
**d4810a62-4287-4154-8f7f-0d567870381e:Generated,af139385-b85f-4f34-9d99-151bc9b2d89b:Generated,7b4d5507-3714-45d5-b774-76b0c2817aa1:Generated**
If the system can't find any requests from your IP then it will return "No requests".

## How to use get-image
If you go to e.g. <u>127.0.0.1:5000/get-image/d4810a62-4287-4154-8f7f-0d567870381e</u> and the image has been generated it will return the image as a **.jpg**, it then deletes the image from the file structure and the database. If the image hasn't been generated or it isn't able to find the image it will return "Invalid request".