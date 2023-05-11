# Welcome to Zeon

Zeon is an easy to use ecommerce platform! Coming with site verification and ratings for users who sell items!


# Installation


````
=> pipenv install
=> npm install --prefix client
=> npm start --prefix client
New Terminal
=> pipenv shell 
=> cd into /server 
=> python app.py
````


## Update Your Database

````
=> flask db revision --autogenerate -m'<message>' 
=> flask db upgrade head

You can also run "python seed.py" to seed your database
````
