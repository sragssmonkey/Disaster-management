#!/usr/bin/env python3
"""
Test script for Emergency Reporting System
Tests SMS, IVR, and USSD emergency reporting functionality
"""

import os
import sys
import django
import json
from datetime import datetime

# Setup Django environment
sys.path.append('/Users/anugrah/Disaster-management')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Disaster.settings')
django.setup()

from backend.models import EmergencyReport, EmergencyResponse
from backend.language_support import get_translation, get_ussd_menu
from backend.location_service import LocationService
from backend.sms_service import SMSService
from backend.ivr_service import IVRService
from backend.ussd_service import USSDService

def test_emergency_report_creation():
    """Test emergency report creation"""
    print("Testing Emergency Report Creation...")
    
    # Test SMS emergency report
    sms_report = EmergencyReport.objects.create(
        channel='sms',
        phone_number='+919876543210',
        category='flood',
        severity=3,
        description='Water level rising fast near main road',
        district='Mumbai',
        state='Maharashtra',
        raw_data={'test': True}
    )
    
    print(f"✓ SMS Report created: {sms_report.report_id}")
    print(f"  Priority Score: {sms_report.priority_score}")
    
    # Test IVR emergency report
    ivr_report = EmergencyReport.objects.create(
        channel='ivr',
        phone_number='+919876543211',
        category='fire',
        severity=4,
        description='Building fire on 3rd floor',
        district='Delhi',
        state='Delhi',
        raw_data={'call_id': 'CA1234567890', 'test': True}
    )
    
    print(f"✓ IVR Report created: {ivr_report.report_id}")
    print(f"  Priority Score: {ivr_report.priority_score}")
    
    # Test USSD emergency report
    ussd_report = EmergencyReport.objects.create(
        channel='ussd',
        phone_number='+919876543212',
        category='medical',
        severity=4,
        description='Person unconscious, needs immediate help',
        district='Bangalore',
        state='Karnataka',
        raw_data={'session_id': 'USS1234567890', 'test': True}
    )
    
    print(f"✓ USSD Report created: {ussd_report.report_id}")
    print(f"  Priority Score: {ussd_report.priority_score}")
    
    return [sms_report, ivr_report, ussd_report]

def test_language_support():
    """Test multi-language support"""
    print("\nTesting Multi-Language Support...")
    
    # Test English
    en_category = get_translation('en', 'medical', category=True)
    print(f"✓ English Medical: {en_category}")
    
    # Test Hindi
    hi_category = get_translation('hi', 'medical', category=True)
    print(f"✓ Hindi Medical: {hi_category}")
    
    # Test Bengali
    bn_category = get_translation('bn', 'flood', category=True)
    print(f"✓ Bengali Flood: {bn_category}")
    
    # Test USSD menu generation
    en_menu = get_ussd_menu('en', 1)
    print(f"✓ English USSD Menu: {en_menu[:50]}...")
    
    hi_menu = get_ussd_menu('hi', 1)
    print(f"✓ Hindi USSD Menu: {hi_menu[:50]}...")

def test_location_detection():
    """Test location detection services"""
    print("\nTesting Location Detection...")
    
    # Test phone number location detection
    location_info = LocationService.detect_location_from_phone_number('+919876543210')
    if location_info:
        print(f"✓ Phone Location Detection: {location_info}")
    else:
        print("⚠ Phone Location Detection: No location found")
    
    # Test address parsing
    address_info = LocationService.detect_location_from_address('123 Main Street, Mumbai, Maharashtra')
    if address_info:
        print(f"✓ Address Parsing: {address_info}")
    else:
        print("⚠ Address Parsing: No location found")
    
    # Test coordinate validation
    valid_coords = LocationService.validate_coordinates(19.0760, 72.8777)  # Mumbai
    print(f"✓ Coordinate Validation (Mumbai): {valid_coords}")
    
    invalid_coords = LocationService.validate_coordinates(40.7128, -74.0060)  # New York
    print(f"✓ Coordinate Validation (New York): {invalid_coords}")

def test_sms_service():
    """Test SMS service functionality"""
    print("\nTesting SMS Service...")
    
    sms_service = SMSService()
    
    # Test phone number validation
    valid_phone = sms_service.validate_phone_number('+919876543210')
    print(f"✓ Phone Validation: {valid_phone}")
    
    # Test SMS parsing
    test_message = "EMERGENCY flood 3 water level rising fast"
    parsed_data = sms_service.parse_emergency_sms(test_message)
    print(f"✓ SMS Parsing: {parsed_data}")
    
    # Test phone number cleaning
    clean_number = sms_service._clean_phone_number('9876543210')
    print(f"✓ Phone Cleaning: {clean_number}")

def test_ivr_service():
    """Test IVR service functionality"""
    print("\nTesting IVR Service...")
    
    ivr_service = IVRService()
    
    # Test TwiML generation
    welcome_twiml = ivr_service.generate_twiml_response('welcome')
    print(f"✓ TwiML Generation: {len(welcome_twiml)} characters")
    
    # Test IVR input processing
    result = ivr_service.process_ivr_input('CA1234567890', '1', 'medical')
    print(f"✓ IVR Input Processing: {result}")

def test_ussd_service():
    """Test USSD service functionality"""
    print("\nTesting USSD Service...")
    
    ussd_service = USSDService()
    
    # Test USSD request processing
    session_data = {
        'phone_number': '+919876543210',
        'session_id': 'USS1234567890',
        'menu_level': 1,
        'category': None,
        'severity': None,
        'description': None,
        'location': None,
        'created_at': datetime.now()
    }
    
    result = ussd_service.process_ussd_request(
        '+919876543210', 'USS1234567890', 1, '', session_data
    )
    print(f"✓ USSD Request Processing: {result['status']}")
    
    # Test input validation
    valid_input = ussd_service.validate_ussd_input('1', 2)
    print(f"✓ USSD Input Validation: {valid_input}")

def test_emergency_responses():
    """Test emergency response creation"""
    print("\nTesting Emergency Responses...")
    
    # Get a test emergency report
    reports = EmergencyReport.objects.filter(raw_data__test=True)
    if reports.exists():
        report = reports.first()
        
        # Create a test response
        response = EmergencyResponse.objects.create(
            emergency_report=report,
            responder_id=1,  # Assuming user ID 1 exists
            response_type='acknowledgment',
            message='Emergency report acknowledged by test system'
        )
        
        print(f"✓ Emergency Response created: {response.id}")
        print(f"  Response Type: {response.response_type}")
        print(f"  Message: {response.message}")
    else:
        print("⚠ No test reports found for response testing")

def cleanup_test_data():
    """Clean up test data"""
    print("\nCleaning up test data...")
    
    # Delete test emergency reports
    test_reports = EmergencyReport.objects.filter(raw_data__test=True)
    count = test_reports.count()
    test_reports.delete()
    
    print(f"✓ Cleaned up {count} test reports")

def main():
    """Main test function"""
    print("Emergency Reporting System Test Suite")
    print("=" * 50)
    
    try:
        # Test emergency report creation
        test_reports = test_emergency_report_creation()
        
        # Test language support
        test_language_support()
        
        # Test location detection
        test_location_detection()
        
        # Test SMS service
        test_sms_service()
        
        # Test IVR service
        test_ivr_service()
        
        # Test USSD service
        test_ussd_service()
        
        # Test emergency responses
        test_emergency_responses()
        
        print("\n" + "=" * 50)
        print("✓ All tests completed successfully!")
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean up test data
        cleanup_test_data()

if __name__ == '__main__':
    main()
