### SecureMe
**SecureMe** is my entry into the 2024 Congressional App Challenge
It's a short online course site built on flask and the standard frontend languages (HTML, CSS, Javascript.) The database runs off of sqlite.



### Installation
Because of some weird problems with getting a virtual python environment setup, there, well, isn't one setup. Because of this you will need to install the following libs from the flask suite, if you don't already have them installed as they are pretty common:
```
pip install flask
pip install flask_sqlalchemy
pip install flask_login
pip install flask_wtf
```
After installing these libs, _generate a secret key_, run the app.py file, and everything should run as intended.


### Compatible Operating Systems
SecureMe was built and tested on Windows, and because of how file paths are handled in certain areas, at the moment SecureMe is only guaranteed to run without issues on Windows, so use other operating systems with some caution.


### Extra
This project is for a competition, so don't report issues or anything. This is only hosted on GitHub in order to give the judges access to the source code of the application.
