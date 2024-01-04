# Endpoints

Login
http://127.0.0.1:8000/login/

Signup
http://127.0.0.1:8000/signup/

dashboard
http://127.0.0.1:8000/home/

profile
http://127.0.0.1:8000/profile/

Other Users( Profile)


# Run project

1) Clone the repository
https://github.com/AbyvargheseMandapathel/cuvette_task.git

2) Create and activate virtual environment

``` bash
    python -m venv myvenv
    virtualenv env
    .\env\Scripts\Activate.ps1 
```

3) Install dependencies:

```bash
    pip install -r requirements.txt
```

4)Apply migrations:

```bash
    python manage.py makemigrations
    python manage.py migrate
```

5)Run the development server:

```bash
    python manage.py runserver
```

# Screenshots
Login
![Login](image.png)

SignUp
![SignUp](image-1.png)

Dashboard
![Dashaboard](image-2.png)

Profile Page
![Profile Page](image-3.png)

Validation - Login Page
![Validation - Login Page](image-4.png)

Validation - SignUp
![Validation - Signup page](image-5.png)
