from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.users.models import Profile


class Command(BaseCommand):
    help = "Create a superuser with super_admin profile role"

    def add_arguments(self, parser):
        parser.add_argument("--username", required=True)
        parser.add_argument("--email", required=True)
        parser.add_argument("--password", required=True)

    def handle(self, *args, **options):
        username = options["username"]
        email = options["email"]
        password = options["password"]

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR(f'User "{username}" already exists.'))
            return

        user = User.objects.create_superuser(username=username, email=email, password=password)
        Profile.objects.create(user=user, role="super_admin")

        self.stdout.write(self.style.SUCCESS(f'Super admin "{username}" created successfully.'))
