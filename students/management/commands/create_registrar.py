from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from students.models import Registrar


class Command(BaseCommand):
    help = 'Create a registrar user'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Username for the registrar')
        parser.add_argument('--password', type=str, help='Password for the registrar')
        parser.add_argument('--email', type=str, help='Email for the registrar')

    def handle(self, *args, **options):
        username = options.get('username') or 'nelson'
        password = options.get('password') or 'admin123'
        email = options.get('email') or 'nelson@example.com'

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'User "{username}" already exists.')
            )
            return

        # Create user
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            is_active=True
        )

        # Create registrar profile
        registrar = Registrar.objects.create(user=user)

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created registrar user "{username}" with password "{password}"'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'Registrar profile created with ID: {registrar.id}'
            )
        )