# hotel
Course project "Hotel" based on Django

Installation
============
Firstly, install a virtual environment. Virtualenv will isolate your Python/Django setup on a per-project basis
```bash
  $ python3 -m venv .env
```
Start your virtual environment by running :
```bash
  $ source venv/bin/activate # For linux 
  venv\Scripts\activate # For Windows
```
Then you can install all the requirements
```bash
pip install -r requirements.txt
```
You have to create local_settings.py according to the template **local_settings.example.py**

After that install required node modules
```bash
yarn
```

And finally create database and run the server
```bash
python manage.py migrate
python manage.py runserver
```

Preprocessors
============
Frond-end of the project is compiled via [Webpack](https://webpack.js.org/concepts) as a bundler, which uses template engine [PugJS](https://pugjs.org/language/attributes.html) and style sheet language [SASS](https://sass-lang.com/documentation/file.SASS_REFERENCE.html).

Django-webpack-loader [official documentation](https://github.com/owais/django-webpack-loader).