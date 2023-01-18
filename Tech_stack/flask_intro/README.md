# Flask Introduction 
- modified from from https://github.com/jakerieger/FlaskIntroduction

## How to Run in python3
1. install `virtualenv`
` pip3 install virtualenv`
2. Open a terminal and switch in to the project root and run
` virtualenv env`
3. Then run the command to activate the virtual environment
`source env/bin/activate`
4. Then install the dependencies
` pip3 install -r requirements.txt`
5. Set the environment variable
`export FLASK_APP=app`
6. Create the database by opening a flask shell:
` flask shell`
7. Create the database object
```
from app import db, Todo
db.create_all()
```