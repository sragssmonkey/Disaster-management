"""
SMS Gateway Integration Service
Handles SMS sending and receiving for emergency reporting system
"""

import os
import re
import json
import logging
from typing import Optional, Dict, List
from django.conf import settings
from django.utils import timezone

# Configure logging
logger = logging.getLogger(__name__)

class SMSService:
    """Service for handling SMS operations"""
    
    def __init__(self):
        self.twilio_account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', None)
        self.twilio_auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', None)
        self.twilio_phone_number = getattr(settings, 'TWILIO_PHONE_NUMBER', None)
        self.sms_gateway_url = getattr(settings, 'SMS_GATEWAY_URL', None)
        self.sms_gateway_api_key = getattr(settings, 'SMS_GATEWAY_API_KEY', None)
    
    def send_sms(self, to_number: str, message: str, language: str = 'en') -> Dict:
        """
        Send SMS message
        
        Args:
            to_number (str): Recipient phone number
            message (str): Message content
            language (str): Language code
            
        Returns:
            Dict: Response with status and message ID
        """
        try:
            # Clean phone number
            clean_number = self._clean_phone_number(to_number)
            
            # Try Twilio first if configured
            if self.twilio_account_sid and self.twilio_auth_token:
                return self._send_via_twilio(clean_number, message)
            
            # Try custom SMS gateway if configured
            elif self.sms_gateway_url and self.sms_gateway_api_key:
                return self._send_via_custom_gateway(clean_number, message)
            
            # Fallback to logging (for development)
            else:
                logger.info(f"SMS to {clean_number}: {message}")
                return {
                    'status': 'success',
                    'message_id': f"dev_{int(timezone.now().timestamp())}",
                    'provider': 'development'
                }
                
        except Exception as e:
            logger.error(f"Failed to send SMS: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _send_via_twilio(self, to_number: str, message: str) -> Dict:
        """Send SMS via Twilio"""
        try:
            from twilio.rest import Client
            
            client = Client(self.twilio_account_sid, self.twilio_auth_token)
            
            message_obj = client.messages.create(
                body=message,
                from_=self.twilio_phone_number,
                to=to_number
            )
            
            return {
                'status': 'success',
                'message_id': message_obj.sid,
                'provider': 'twilio'
            }
            
        except Exception as e:
            logger.error(f"Twilio SMS failed: {str(e)}")
            raise
    
    def _send_via_custom_gateway(self, to_number: str, message: str) -> Dict:
        """Send SMS via custom gateway"""
        try:
            import requests
            
            payload = {
                'to': to_number,
                'message': message,
                'api_key': self.sms_gateway_api_key
            }
            
            response = requests.post(
                self.sms_gateway_url,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'status': 'success',
                    'message_id': data.get('message_id', 'unknown'),
                    'provider': 'custom_gateway'
                }
            else:
                raise Exception(f"Gateway returned status {response.status_code}")
                
        except Exception as e:
            logger.error(f"Custom gateway SMS failed: {str(e)}")
            raise
    
    def _clean_phone_number(self, phone_number: str) -> str:
        """Clean and format phone number"""
        # Remove all non-digit characters except +
        clean_number = re.sub(r'[^\d+]', '', phone_number)
        
        # Add country code if missing
        if not clean_number.startswith('+'):
            if clean_number.startswith('91'):
                clean_number = '+' + clean_number
            elif clean_number.startswith('0'):
                clean_number = '+91' + clean_number[1:]
            else:
                clean_number = '+91' + clean_number
        
        return clean_number
    
    def parse_emergency_sms(self, message: str) -> Dict:
        """
        Parse emergency SMS message
        
        Expected format: "EMERGENCY <category> <severity> <description>"
        Example: "EMERGENCY flood 3 water level rising fast"
        
        Args:
            message (str): SMS message content
            
        Returns:
            Dict: Parsed emergency data
        """
        try:
            # Convert to uppercase and split
            parts = message.upper().split()
            
            if len(parts) < 3 or parts[0] != 'EMERGENCY':
                return {
                    'valid': False,
                    'error': 'Invalid format. Use: EMERGENCY <category> <severity> <description>'
                }
            
            # Extract category
            category = parts[1].lower()
            valid_categories = ['medical', 'fire', 'flood', 'earthquake', 'cyclone', 'landslide', 'roadblock', 'other']
            
            if category not in valid_categories:
                category = 'other'
            
            # Extract severity
            try:
                severity = int(parts[2])
                if severity not in [1, 2, 3, 4]:
                    severity = 1
            except (ValueError, IndexError):
                severity = 1
            
            # Extract description
            description = ' '.join(parts[3:]) if len(parts) > 3 else 'Emergency reported via SMS'
            
            return {
                'valid': True,
                'category': category,
                'severity': severity,
                'description': description,
                'original_message': message
            }
            
        except Exception as e:
            return {
                'valid': False,
                'error': f'Failed to parse SMS: {str(e)}'
            }
    
    def send_emergency_confirmation(self, phone_number: str, report_id: str, language: str = 'en') -> Dict:
        """
        Send confirmation SMS for emergency report
        
        Args:
            phone_number (str): Recipient phone number
            report_id (str): Emergency report ID
            language (str): Language code
            
        Returns:
            Dict: Response status
        """
        from .language_support import get_translation, format_emergency_message
        
        # Get language-specific messages
        if language == 'hi':
            message = f"आपातकाल रिपोर्ट {report_id} प्राप्त हुई। सहायता रास्ते में है।"
        elif language == 'bn':
            message = f"জরুরি রিপোর্ট {report_id} পেয়েছি। সাহায্য আসছে।"
        elif language == 'te':
            message = f"అత్యవసర నివేదిక {report_id} అందింది। సహాయం వస్తోంది।"
        else:  # Default to English
            message = f"Emergency report {report_id} received. Help is on the way."
        
        return self.send_sms(phone_number, message, language)
    
    def send_emergency_update(self, phone_number: str, report_id: str, status: str, language: str = 'en') -> Dict:
        """
        Send status update SMS for emergency report
        
        Args:
            phone_number (str): Recipient phone number
            report_id (str): Emergency report ID
            status (str): Status update
            language (str): Language code
            
        Returns:
            Dict: Response status
        """
        from .language_support import get_translation
        
        status_messages = {
            'acknowledged': get_translation(language, 'report_acknowledged'),
            'in_progress': get_translation(language, 'report_in_progress'),
            'resolved': get_translation(language, 'report_resolved')
        }
        
        message = f"Report {report_id}: {status_messages.get(status, status)}"
        
        return self.send_sms(phone_number, message, language)
    
    def send_emergency_instructions(self, phone_number: str, category: str, language: str = 'en') -> Dict:
        """
        Send emergency instructions based on category
        
        Args:
            phone_number (str): Recipient phone number
            category (str): Emergency category
            language (str): Language code
            
        Returns:
            Dict: Response status
        """
        instructions = {
            'medical': {
                'en': "MEDICAL EMERGENCY: Stay calm. Call 102 for ambulance. Provide clear location. Do not move patient if injured.",
                'hi': "चिकित्सा आपातकाल: शांत रहें। एम्बुलेंस के लिए 102 पर कॉल करें। स्पष्ट स्थान बताएं।",
                'bn': "চিকিৎসা জরুরি: শান্ত থাকুন। অ্যাম্বুলেন্সের জন্য ১০২ ডাকুন। স্পষ্ট অবস্থান দিন।"
            },
            'fire': {
                'en': "FIRE EMERGENCY: Evacuate immediately. Call 101 for fire department. Do not use elevators. Stay low if smoke present.",
                'hi': "आग का आपातकाल: तुरंत निकलें। फायर डिपार्टमेंट के लिए 101 पर कॉल करें।",
                'bn': "আগুনের জরুরি: সঙ্গে সঙ্গে বেরিয়ে আসুন। ফায়ার ডিপার্টমেন্টের জন্য ১০১ ডাকুন।"
            },
            'flood': {
                'en': "FLOOD EMERGENCY: Move to higher ground. Avoid walking through floodwater. Call 100 for rescue. Stay informed.",
                'hi': "बाढ़ का आपातकाल: ऊंची जगह पर जाएं। बाढ़ के पानी से बचें। बचाव के लिए 100 पर कॉल करें।",
                'bn': "বন্যার জরুরি: উঁচু জায়গায় যান। বন্যার পানিতে হাঁটবেন না। উদ্ধারের জন্য ১০০ ডাকুন।"
            },
            'earthquake': {
                'en': "EARTHQUAKE: Drop, Cover, Hold. Stay indoors if safe. Avoid windows. Call 100 if trapped.",
                'hi': "भूकंप: बैठ जाएं, ढकें, पकड़ें। सुरक्षित हो तो घर के अंदर रहें। खिड़कियों से बचें।",
                'bn': "ভূমিকম্প: বসুন, ঢাকুন, ধরে রাখুন। নিরাপদ হলে ঘরের ভিতরে থাকুন। জানালা এড়িয়ে চলুন।"
            }
        }
        
        message = instructions.get(category, {}).get(language, instructions.get(category, {}).get('en', 'Follow emergency procedures.'))
        
        return self.send_sms(phone_number, message, language)
    
    def validate_phone_number(self, phone_number: str) -> bool:
        """
        Validate phone number format
        
        Args:
            phone_number (str): Phone number to validate
            
        Returns:
            bool: True if valid
        """
        try:
            import phonenumbers
            parsed_number = phonenumbers.parse(phone_number, None)
            return phonenumbers.is_valid_number(parsed_number)
        except:
            # Fallback to regex validation
            pattern = r'^\+?[1-9]\d{1,14}$'
            return bool(re.match(pattern, phone_number))
    
    def get_sms_status(self, message_id: str) -> Dict:
        """
        Get SMS delivery status
        
        Args:
            message_id (str): SMS message ID
            
        Returns:
            Dict: Status information
        """
        # This would typically query the SMS provider's API
        # For now, return a mock response
        return {
            'status': 'delivered',
            'delivered_at': timezone.now().isoformat(),
            'message_id': message_id
        }


class SMSWebhookHandler:
    """Handle incoming SMS webhooks"""
    
    @staticmethod
    def handle_incoming_sms(request_data: Dict) -> Dict:
        """
        Handle incoming SMS webhook
        
        Args:
            request_data (Dict): Webhook request data
            
        Returns:
            Dict: Response data
        """
        try:
            # Extract SMS data from webhook
            phone_number = request_data.get('From', '')
            message = request_data.get('Body', '')
            
            if not phone_number or not message:
                return {
                    'status': 'error',
                    'message': 'Missing phone number or message'
                }
            
            # Parse emergency SMS
            sms_service = SMSService()
            parsed_data = sms_service.parse_emergency_sms(message)
            
            if not parsed_data['valid']:
                # Send error message back
                error_message = parsed_data.get('error', 'Invalid format')
                sms_service.send_sms(phone_number, error_message)
                
                return {
                    'status': 'error',
                    'message': error_message
                }
            
            # Create emergency report (this would typically be done in the view)
            # For now, return the parsed data
            return {
                'status': 'success',
                'parsed_data': parsed_data,
                'phone_number': phone_number
            }
            
        except Exception as e:
            logger.error(f"SMS webhook handling failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
