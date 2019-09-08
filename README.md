Face-BE
[![CircleCI](https://circleci.com/gh/face-ac/face-be/tree/master.svg?style=svg)](https://circleci.com/gh/face-ac/face-be/tree/master)

Lives at http://face-be.herokuapp.com/api 

###To run locally:

```
# Assumes you have git, python3.7, pip, and virtualenv installed.
# If you don't have those, make sure you get them first.
git clone
cd face-be
virtualenv venv
source venv/bin/activate
cd src
pip install -r requirements.txt
python -m run 
```

Run tests:
```
# Assumes you've got MySQL set up locally with correct schemas.
nose2 -v
```

###Using Docker
Build with docker-compose: 
```
# Start
docker-compose up

# Remove
docker-compose down

```
