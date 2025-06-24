from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.accounts.models import Role
from faker import Faker
import random

fake = Faker()
User = get_user_model()

class Command(BaseCommand):
    help = "Create fake users with random roles"

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, help="Number of users to create")

    def handle(self, *args, **kwargs):
        count = kwargs["count"]
        roles = [role for role, _ in Role.choices]
        created = 0

        for _ in range(count):
            name = fake.user_name()
            email = fake.unique.email()
            password = fake.password(length=10)
            role = random.choice(roles)

            if User.objects.filter(email=email).exists():
                continue

            user = User.objects.create_user(
                username=name,
                email=email,
                password=password,
                role=role
            )

            created += 1
            self.stdout.write(self.style.SUCCESS(
                f"👤 Created user: {user.username} | {user.email} | {role}"
            ))

        self.stdout.write(self.style.SUCCESS(f"\n Total created: {created}"))
