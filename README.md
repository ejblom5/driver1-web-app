# Genral workflow for development
1. Create a new branch locally for the feature you want to add
2. Develop the code for your new feature
3. Make sure your code runs locally (python manage.py runserver)
4. Push the branch you created
5. In the github site create a pull request to merge the new branch into main
6. Get some people to review your code, or just go ahead and merge it if it is minor changes

# Database Things
In order to run the django app locally you may have to change what the database is pointing at in the settings.py file. If you change it to run locally make sure you don't commit that change to the master branch since then heroku will try to use a local db instead of the installed postgres one.

#API
base url: https://driver1-web-app.herokuapp.com

Endpoints:

/drivers
  - GET (get a list of all drivers)
  - POST (create a new driver)
    - request body: { "email": "example@example.com", "password": "example password", "name": "example name", "phone": "1111",      "address": "example address" }

/drivers/{driver_id}
  - GET (get a single driver based on the driver id passed into the route)
  - PUT (update a single driver)
    - request body: { "address" : "new address" }

/sponsors
  - GET (get a list of all sponsors)

/sponsors/{sponsor_id}
  - GET (get a single sponsor based on the sponsor id passed into the route)

