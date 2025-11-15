from django.core.management.base import BaseCommand
from customusers.models import CustomUser
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from faker import Faker
import random

class Command(BaseCommand):
    help = "Generate 10000 random users"

    def handle(self, *args, **kwargs):
        fake = Faker()
        users = []
        roles = ['admin', 'manager', 'employee']
        departments = ['IT', 'HR', 'Sales', 'Finance']
        batch_size = 1000

        for i in range(10000):
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = fake.unique.email()
            username = f"{first_name.lower()}.{last_name.lower()}{i}"
            phone = fake.phone_number()
            city = fake.city()
            country = fake.country()
            department = random.choice(departments)
            role = random.choice(roles)
            birth_date = random.randint(1967, 2007)
            birth_date = fake.date_of_birth(tzinfo=None, minimum_age=18, maximum_age=58)
            salary = random.randint(100000, 2000000)

            user = CustomUser(
                email=email,
                username=username,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                city=city,
                country=country,
                department=department,
                role=role,
                birth_date=birth_date,
                salary=salary,
                password=make_password("12345"),
                is_active=True,
                is_staff=(role == 'admin'),
                date_joined=timezone.now(),
            
            )
            users.append(user)

            if len(users) >= batch_size:
                CustomUser.objects.bulk_create(users)
                self.stdout.write(f"Created {i+1} users")
                users = []

        if users:
            CustomUser.objects.bulk_create(users)
            self.stdout.write(f"Created 10000 users")

