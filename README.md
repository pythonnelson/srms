# Create SECRET_KEY using the terminal

    openssl rand -base64 64 | tr -dc 'A-Za-z0-9' | head -c 50; echo

# Create Register from the terminal

    python manage.py create_registrar
