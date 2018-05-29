# RandomChat
## About
RanomChat is a basic anonymous chat implementation based on many others like Omegle, Chat Roulette etc. 
Basically, two anonymous users connect to each other at random and start texting.
This project is intended to be for learning purposes.

### Server-side
- Server-side logic is built on top of [Flask](http://flask.pocoo.org/);
- As Flask is an MVC microframework, RandomChat's design pattern is based on Blueprints;
- Realtime messaging is handled by SocketIO attached to Flask using [Flask-SocketIO](http://flask-socketio.readthedocs.io/en/latest/).

### Client-side
- Client-side markup is made out of HTML 5;
- Styling is made out of CSS 3;
- Client-side logic is built on top of javascript with the help of [jQuery](https://jquery.com/) and [SocketIO Client](https://socket.io/);

### Automation
- Styling and javascript are made with the help of pre-processing scripts like LESS and Uglify usgin [gulpjs](https://gulpjs.com/) pre-processor.

## Testing
### Steps to run this project locally
#### Requirements
- Python 3.6.4. installed
- Pip

#### Instalation and running
- Clone this repository into your local local drive:
	``` git clone https://github.com/matheus-crivellari/randomchat.git ```
- Enter the working directory:
	``` cd randomchat ```
- Install requirements:
	``` pip install ```
- Run the app:
	``` python run.py ```
- Open your web browser and go to the following address:
	``` localhost:5000 ```

### Steps to run this project on Heroku
This project is Heroku compatible. It was tested and is working.

#### Requirements
- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install).
- [Heroku account](https://signup.heroku.com/).

#### Instalation and running
- Clone this repository into your local drive:
	``` git clone https://github.com/matheus-crivellari/randomchat.git ```
- Enter the working directory:
	``` cd randomchat ```
- Log in to your Heroku account via web browser and create a new app:
- Lets assume your app is called ``` rndchat ```, set heroku's repo as one of your working directory's remote:
	``` heroku git:remote -a rndchat ```
- Push the source to your Heroku app's repository:
	``` git push heroku master ```
- Wait until the installation process is finished, then run your new app:
	``` heroku open ```
	If everything went ok you should be redirected to your web browser.

### Testing the chat
- Open at least two web browser's window with the application runnging on them (either locally or at Heroku);
- Hit Start! on both;
- Send messages from one window toa nother!

#### Plus
- If you're testing this on Heroku or any other live web server, invite some friends and start chatting randomly.

## Licence
Copyright (c) 2018 Matheus Crivellari

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.