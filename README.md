# ImagesAPI
* API created in Django and Django Rest Framework for uploading JPG and PNG images


## Tech stack
* Python 3.9
* Django 3.2
* Django REST Framework
* PostgreSQL
* Docker with Docker Compose


## Functionalities
* User registration is skipped, they are created in django-admin panel.
* Each user need to have their own account with dedicated account tier. Except for 3 built-in tiers: Basic, Premium and Enterprise, admins are able to create custom tiers.
* Users can upload images and list uploaded ones. Moreover, they can get thumbnail links with sizes stated in their tier settings.
* Some users have permission to create expiring links to original photo with expiration time (Access token is required to create such links).
* If access token is expired, the link is being deleted, when user try to click that link.


## Project setup
### IMPORTANT:
In order to execute commands with 'make' in Windows you need to install Chocolatey Package Manager
https://chocolatey.org/

1. Clone repository:
`$ git clone https://github.com/mmyszak999/ImagesAPI/`
2. In the 'config' directory create '.env' file
3. Set the values of environmental variables (you can copy the content from '.env.template' file)
4. In the root directory type:
`$ make build`
5. In order to run project type: 
`$ make up`


## Migrations
`$ make migrations`

## Fixtures (creates 3 built-in account tiers)
`$ make fixtures`

## Tests
`$ make test`

## Create admin
`$ make superuser`