##### URL_SHORTENER

Still a work in progress, but to run 

    pip install -e .
    export FLASK_APP=shortener
    flask run

Migrations and DB config still need to be completed.


##### Testing


    pip install -e '.[test]'
    pytest
    
Or to get a coverage report:

    coverage run -m pytest
    coverage report
    coverage html # open htmlcov/index.html in a browser