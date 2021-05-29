# posts-tdd-django
## Application with TDD

[demo in heroku](https://postdd.herokuapp.com/)

##### Use of dev tools for tests development 

* [Coverage](https://coverage.readthedocs.io/en/coverage-5.5/)
* [factory-boy](https://factoryboy.readthedocs.io/en/stable/)
* [mixer](https://pypi.org/project/mixer/)
* [faker](https://faker.readthedocs.io/en/master/)
* [autopep8](https://pypi.org/project/autopep8/)
* [selenium](https://selenium-python.readthedocs.io/installation.html)

#### How to Setup:

 - Copy the file posts/.env.sample to posts/.env and configure you environment variables

 - Install dependencies
  ```` bash
    pip install pipenv
  ````
  
  ```` bash
    pipenv install -d
  ````
  Or
  
  ```` bash
    python -m pipenv install -d
  ````
  
 - Execute your tests with:
 
 ```` bash
   python manage.py test
 ````




