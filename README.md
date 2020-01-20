# Toronto Restaurant Map VDA
## Installation
In order to run this software you'll have to [install yarn](https://yarnpkg.com/lang/en/docs/install/) onto your computer first. Next, I recommend opening up two tabs on your terminal. On your first terminal, navigate to the backend subdirectory and run the following commands:

`pipenv install`

`pipenv run`

`python manage.py runserver`

This should get the backend portion of this software working. On your second terminal navigate to the frontend subdirectory and run:

`yarn start`

If you run into a **yarn command not found** error, then yarn isn't on your path. One way to fix this is by running: 

`export PATH=~/.yarn/bin:$PATH`

## Directory Summary 

A brief overview of what every directy contributes to the overall software. For more information on specific files, refer to the documentation within the files.

Insert tree diagram here.

### backend

This subdirectory supplies the front end with user information, restaurant information, and the machine learning algorithm.

#### backend

The relevant files in this folder are **urls.py** and **settings.py**. 

`settings.py` informs Django: what apps are registered in the backend, what port to run the local server on, and the csrf token. 

`urls.py` directs the flow of control whenever a user visits a different webpage, supplying django with information on what function to call given a http request.

#### barchart

In **barchart**, there is a `models.py` file that describes a single category and probability. There is also an `urls.py` file that handles api requests to "api/barcharts?username=..." by serializing each barchart model before displaying it.

In a similar manner, **heatmap** also contains a `models.py` file that describes a single heatmap square through a (longitiude, latitude, probability) triple. There is also an `urls.py` file that handles api requests to "api/heatmaps?username=..." by serializing each heatmap model before displaying it.


#### heatmap
#### map_view
#### shell
#### toronto_restaurants
#### user_input
#### users
### frontend
#### data
#### public
#### src
