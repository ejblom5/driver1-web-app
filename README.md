# Genral workflow for development
1. Create a new branch locally for the feature you want to add
2. Develop the code for your new feature
3. Make sure your code runs locally (python manage.py runserver)
4. Push the branch you created
5. In the github site create a pull request to merge the new branch into main
6. Get some people to review your code, or just go ahead and merge it if it is minor changes

# Database Things
In order to run the django app locally you may have to change what the database is pointing at in the settings.py file. If you change it to run locally make sure you don't commit that change to the master branch since then heroku will try to use a local db instead of the installed postgres one.

When you make changes to a model, you also need to migrate those changes to the corresponding database tables. This is done by runing `manage.py makemigrations` then `manage.py migrate`

# API
base url: https://driver1-web-app.herokuapp.com

All responses should be returned as {"resposne": response_body}
  - Ex: retreiving one driver would return { "response": {"id" : 1, "name" : "driver bill", ...} }

Endpoints:

/api/drivers/
  - GET (get a list of all drivers)
  - POST (create a new driver)
    - request body: { 
      "email": "example@example.com" (required), 
      "password": "example password" (required), 
      "name": "some name", 
      "qualifications": "some quals", 
      "address": "some lane SC", 
      "phone": "1212121212", 
    }

/api/drivers/{driver_id}
  - GET (get a single driver based on the driver id passed into the route)
  - PATCH (update a single driver)
    - request body: { 
      "name": "some name", 
      "qualifications": "some quals", 
      "address": "some lane SC", 
      "phone": "1212121212", 
    }

/api/sponsors/
  - GET (get a list of all sponsors)
    - You can also sort the list of sponsors by some value if you pass in the value you want to sort by in the url such as...
      /api/sponsors/?sort=id (this will get the list of sponsors, and sort by the sponsor id)
    - By default the sponsor list will be sorted by the sponsor name

/api/sponsors/{sponsor_id}
  - GET (get a single sponsor based on the sponsor id passed into the route)

/api/authenticate/
  - POST (checks if the credentials passed into the request are authorized driver credentials)
    - request body: { "email": "example@example.com", "password": "example password" }
    - request response: JSON for driver object upon sucessful authenticate

/api/application/
  - Get (retreives a list of all applications)
  - POST (upload a new aplication)
    - request body: {"driver_id": 1, "sponsor_id": 2}


