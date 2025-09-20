#!/usr/bin/env python3
"""
Test MSG91 Configuration
Run this script to test your MSG91 setup
"""

import os
import sys
import django
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Disaster.settings')
django.setup()

from django.conf import settings
from backend.sms_service import SMSService

def test_msg91_config():
    """Test MSG91 configuration"""
    print("🔧 Testing MSG91 Configuration...")
    print("=" * 50)
    
    # Check environment variables
    print("📋 Environment Variables:")
    print(f"MSG91_AUTH_KEY: {'✅ Set' if getattr(settings, 'MSG91_AUTH_KEY', None) else '❌ Not Set'}")
    print(f"MSG91_SENDER_ID: {getattr(settings, 'MSG91_SENDER_ID', 'Not Set')}")
    print(f"MSG91_ROUTE: {getattr(settings, 'MSG91_ROUTE', 'Not Set')}")
    print(f"MSG91_COUNTRY: {getattr(settings, 'MSG91_COUNTRY', 'Not Set')}")
    print()
    
    # Test SMS Service
    print("📱 Testing SMS Service:")
    sms_service = SMSService()
    
    # Check if MSG91 is configured
    if sms_service.msg91_auth_key:
        print("✅ MSG91 Auth Key is configured")
        print(f"   Auth Key: {sms_service.msg91_auth_key[:10]}...")
        print(f"   Sender ID: {sms_service.msg91_sender_id}")
        print(f"   Route: {sms_service.msg91_route}")
        print(f"   Country: {sms_service.msg91_country}")
    else:
        print("❌ MSG91 Auth Key is not configured")
        print("   Please set MSG91_AUTH_KEY environment variable")
    
    print()
    
    # Test phone number formatting
    print("📞 Testing Phone Number Formatting:")
    test_numbers = [
        "+919876543210",
        "919876543210", 
        "9876543210",
        "09876543210"
    ]
    
    for number in test_numbers:
        formatted = sms_service._clean_phone_number(number)
        print(f"   {number} → {formatted}")
    
    print()
    
    # Test SMS sending (dry run)
    print("📤 Testing SMS Sending (Dry Run):")
    if sms_service.msg91_auth_key:
        print("✅ Ready to send SMS via MSG91")
        print("   To test: Run the test_emergency_system.py script")
    else:
        print("❌ Cannot send SMS - MSG91 not configured")
        print("   Please configure MSG91_AUTH_KEY first")
    
    print()
    print("🎯 Next Steps:")
    print("1. Set MSG91_AUTH_KEY environment variable")
    print("2. Run: python test_emergency_system.py")
    print("3. Test SMS emergency reporting")

if __name__ == "__main__":
    test_msg91_config()
