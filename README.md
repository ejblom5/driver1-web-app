# Genral workflow for development
1. Create a new branch locally for the feature you want to add
2. Develop the code for your new feature
3. Make sure your code runs locally (python manage.py runserver)
4. Push the branch you created
5. In the github site create a pull request to merge the new branch into main
6. Get some people to review your code, or just go ahead and merge it if it is minor changes

# Database Things
In order to run the django app locally you may have to change what the database is pointing at in the settings.py file. If you change it to run locally make sure you don't commit that change to the master branch since then heroku will try to use a local db instead of the installed postgres one.
