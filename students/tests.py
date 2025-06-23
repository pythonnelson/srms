from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Registrar  

def test_registrar_setup():
    """Test and setup registrar functionality"""
    
    print("=== REGISTRAR SETUP TEST ===\n")
    
    # 1. Check existing users
    print("1. Checking existing users...")
    users = User.objects.all()
    print(f"Total users: {users.count()}")
    for user in users:
        has_registrar = hasattr(user, 'registrar')
        print(f"  - {user.username} (Active: {user.is_active}, Registrar: {has_registrar})")
    
    # 2. Check existing registrars
    print("\n2. Checking existing registrars...")
    registrars = Registrar.objects.all()
    print(f"Total registrars: {registrars.count()}")
    for reg in registrars:
        print(f"  - {reg.user.username}")
    
    # 3. Create a test registrar if none exists
    if registrars.count() == 0:
        print("\n3. No registrars found. Creating test registrar...")
        try:
            # Create user
            username = "admin"
            password = "admin123"
            
            if User.objects.filter(username=username).exists():
                print(f"  User '{username}' already exists")
                user = User.objects.get(username=username)
            else:
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email="admin@example.com",
                    is_active=True
                )
                print(f"  Created user: {username}")
            
            # Create registrar if doesn't exist
            if not hasattr(user, 'registrar'):
                registrar = Registrar.objects.create(user=user)
                print(f"  Created registrar for: {username}")
            else:
                print(f"  Registrar already exists for: {username}")
                
        except Exception as e:
            print(f"  Error creating registrar: {e}")
    
    # 4. Test authentication
    print("\n4. Testing authentication...")
    test_users = [
        ("registrar", "Login@2024"),
        # Add your registrar credentials here
    ]
    
    for username, password in test_users:
        try:
            user = authenticate(username=username, password=password)
            if user:
                has_registrar = hasattr(user, 'registrar')
                print(f"  ✓ {username}: Authentication successful, Registrar: {has_registrar}")
            else:
                print(f"  ✗ {username}: Authentication failed")
        except Exception as e:
            print(f"  ✗ {username}: Error - {e}")
    
    print("\n=== TEST COMPLETE ===")

# Run the test
test_registrar_setup()