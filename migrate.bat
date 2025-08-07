cd "%cd%"
python manage.py makemigrations
python manage.py migrate
python manage.py makemigrations base
python manage.py migrate base
