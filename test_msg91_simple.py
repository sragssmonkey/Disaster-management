#!/usr/bin/env python3
"""
Simple MSG91 Configuration Test
"""

import os

def test_msg91_config():
    """Test MSG91 configuration"""
    print("🔧 Testing MSG91 Configuration...")
    print("=" * 50)
    
    # Check environment variables
    print("📋 Environment Variables:")
    msg91_auth_key = os.environ.get('MSG91_AUTH_KEY')
    msg91_sender_id = os.environ.get('MSG91_SENDER_ID', 'DISASTER')
    msg91_route = os.environ.get('MSG91_ROUTE', '4')
    msg91_country = os.environ.get('MSG91_COUNTRY', '91')
    
    print(f"MSG91_AUTH_KEY: {'✅ Set' if msg91_auth_key else '❌ Not Set'}")
    print(f"MSG91_SENDER_ID: {msg91_sender_id}")
    print(f"MSG91_ROUTE: {msg91_route}")
    print(f"MSG91_COUNTRY: {msg91_country}")
    print()
    
    if msg91_auth_key:
        print("✅ MSG91 is configured!")
        print(f"   Auth Key: {msg91_auth_key[:10]}...")
        print(f"   Sender ID: {msg91_sender_id}")
        print(f"   Route: {msg91_route}")
        print(f"   Country: {msg91_country}")
    else:
        print("❌ MSG91 Auth Key is not configured")
        print("   Please set MSG91_AUTH_KEY environment variable")
    
    print()
    print("🎯 How to configure:")
    print("1. Get your Auth Key from msg91.com")
    print("2. Set environment variable:")
    print("   export MSG91_AUTH_KEY=your_auth_key_here")
    print("3. Or add to Render.com environment variables")
    print("4. Restart your application")

if __name__ == "__main__":
    test_msg91_config()
