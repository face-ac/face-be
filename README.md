Face-BE

To Run on the web, go to http://x.herokuapp.com/login  

User Name: test

Password: test

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
Build with docker: 
```
git clone
cd face-be

# Start
docker-compose up

# Remove
docker-compose down

```
