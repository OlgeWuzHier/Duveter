# Duveter
Game of making duvets. 

# How to run game

## Backend
- Install python (recommended 3.10.2)
- Install requirements from back/requirements.txt using `pip install -r requirements.txt`
- Set required environmental variables - either set them manually, or create `.env` file in back/ folder
```
CONNECTION_STRING=  # Connection string to MongoDB database
JWT_SECRET_KEY=     # Secret key used to generate JWT tokens
SOCKET_SECRET_KEY=  # Secret key used for socket connections
```
- run `app.py` from back/app.py

## Frontend
- Install node.js (recommended 16.13.2)
- run `npm install` in `front/` folder
- run `npm start` in `front/` folder
