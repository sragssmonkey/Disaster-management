"""
IVR (Interactive Voice Response) Service
Handles voice-based emergency reporting through phone calls
"""

import os
import json
import logging
from typing import Optional, Dict, List
from django.conf import settings
from django.utils import timezone

# Configure logging
logger = logging.getLogger(__name__)

class IVRService:
    """Service for handling IVR operations"""
    
    def __init__(self):
        self.twilio_account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', None)
        self.twilio_auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', None)
        self.base_url = getattr(settings, 'BASE_URL', 'http://localhost:8000')
    
    def generate_twiml_response(self, action: str, **kwargs) -> str:
        """
        Generate TwiML response for Twilio
        
        Args:
            action (str): Action to perform
            **kwargs: Additional parameters
            
        Returns:
            str: TwiML XML response
        """
        if action == 'welcome':
            return self._generate_welcome_twiml()
        elif action == 'category_selection':
            return self._generate_category_selection_twiml()
        elif action == 'severity_selection':
            return self._generate_severity_selection_twiml()
        elif action == 'description_prompt':
            return self._generate_description_prompt_twiml()
        elif action == 'location_prompt':
            return self._generate_location_prompt_twiml()
        elif action == 'confirmation':
            return self._generate_confirmation_twiml(kwargs.get('report_id'))
        elif action == 'error':
            return self._generate_error_twiml(kwargs.get('message', 'An error occurred'))
        else:
            return self._generate_error_twiml('Invalid action')
    
    def _generate_welcome_twiml(self) -> str:
        """Generate welcome message TwiML"""
        return '''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice" language="en-IN">Welcome to the Emergency Reporting System.</Say>
    <Say voice="alice" language="en-IN">Please press 1 to report a medical emergency, 2 for fire, 3 for flood, 4 for earthquake, 5 for other emergencies, or 0 to speak to an operator.</Say>
    <Gather numDigits="1" action="/emergency/ivr/category/" method="POST">
        <Say voice="alice" language="en-IN">Please press a number.</Say>
    </Gather>
    <Say voice="alice" language="en-IN">Thank you for calling. Goodbye.</Say>
</Response>'''
    
    def _generate_category_selection_twiml(self) -> str:
        """Generate category selection TwiML"""
        return '''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice" language="en-IN">You have selected an emergency type.</Say>
    <Say voice="alice" language="en-IN">Please rate the severity from 1 to 4, where 1 is low severity and 4 is critical.</Say>
    <Gather numDigits="1" action="/emergency/ivr/severity/" method="POST">
        <Say voice="alice" language="en-IN">Please press a number from 1 to 4.</Say>
    </Gather>
    <Say voice="alice" language="en-IN">Thank you for calling. Goodbye.</Say>
</Response>'''
    
    def _generate_severity_selection_twiml(self) -> str:
        """Generate severity selection TwiML"""
        return '''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice" language="en-IN">You have selected the severity level.</Say>
    <Say voice="alice" language="en-IN">Please describe the emergency in detail. You have 30 seconds to speak.</Say>
    <Record maxLength="30" action="/emergency/ivr/description/" method="POST" finishOnKey="#">
        <Say voice="alice" language="en-IN">Please speak after the beep.</Say>
    </Record>
    <Say voice="alice" language="en-IN">Thank you for calling. Goodbye.</Say>
</Response>'''
    
    def _generate_description_prompt_twiml(self) -> str:
        """Generate description prompt TwiML"""
        return '''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice" language="en-IN">Thank you for providing the description.</Say>
    <Say voice="alice" language="en-IN">Please provide your current location or address. You have 20 seconds to speak.</Say>
    <Record maxLength="20" action="/emergency/ivr/location/" method="POST" finishOnKey="#">
        <Say voice="alice" language="en-IN">Please speak after the beep.</Say>
    </Record>
    <Say voice="alice" language="en-IN">Thank you for calling. Goodbye.</Say>
</Response>'''
    
    def _generate_location_prompt_twiml(self) -> str:
        """Generate location prompt TwiML"""
        return '''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice" language="en-IN">Thank you for providing the location.</Say>
    <Say voice="alice" language="en-IN">Your emergency report has been received and help is on the way.</Say>
    <Say voice="alice" language="en-IN">Please stay safe and follow emergency procedures.</Say>
    <Say voice="alice" language="en-IN">Thank you for calling. Goodbye.</Say>
</Response>'''
    
    def _generate_confirmation_twiml(self, report_id: str) -> str:
        """Generate confirmation TwiML"""
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice" language="en-IN">Your emergency report has been received.</Say>
    <Say voice="alice" language="en-IN">Report ID is {report_id}.</Say>
    <Say voice="alice" language="en-IN">Help is on the way. Please stay safe.</Say>
    <Say voice="alice" language="en-IN">Thank you for calling. Goodbye.</Say>
</Response>'''
    
    def _generate_error_twiml(self, message: str) -> str:
        """Generate error TwiML"""
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice" language="en-IN">{message}</Say>
    <Say voice="alice" language="en-IN">Please try again later.</Say>
    <Say voice="alice" language="en-IN">Thank you for calling. Goodbye.</Say>
</Response>'''
    
    def process_ivr_input(self, call_sid: str, digits: str, category: str = None) -> Dict:
        """
        Process IVR input from user
        
        Args:
            call_sid (str): Twilio call SID
            digits (str): User input digits
            category (str): Emergency category if already selected
            
        Returns:
            Dict: Response data
        """
        try:
            if not category:
                # First level - category selection
                category_map = {
                    '1': 'medical',
                    '2': 'fire',
                    '3': 'flood',
                    '4': 'earthquake',
                    '5': 'other',
                    '0': 'operator'
                }
                
                selected_category = category_map.get(digits, 'other')
                
                if selected_category == 'operator':
                    return {
                        'action': 'transfer',
                        'number': '+911234567890'  # Emergency operator number
                    }
                
                return {
                    'action': 'category_selection',
                    'category': selected_category,
                    'next_step': 'severity'
                }
            
            elif category and not hasattr(self, '_current_severity'):
                # Second level - severity selection
                try:
                    severity = int(digits)
                    if 1 <= severity <= 4:
                        return {
                            'action': 'severity_selection',
                            'severity': severity,
                            'next_step': 'description'
                        }
                    else:
                        return {
                            'action': 'error',
                            'message': 'Invalid severity level'
                        }
                except ValueError:
                    return {
                        'action': 'error',
                        'message': 'Invalid input'
                    }
            
            else:
                return {
                    'action': 'error',
                    'message': 'Invalid state'
                }
                
        except Exception as e:
            logger.error(f"IVR input processing failed: {str(e)}")
            return {
                'action': 'error',
                'message': 'Processing failed'
            }
    
    def process_voice_recording(self, call_sid: str, recording_url: str, recording_type: str) -> Dict:
        """
        Process voice recording from IVR
        
        Args:
            call_sid (str): Twilio call SID
            recording_url (str): URL of the recording
            recording_type (str): Type of recording (description, location)
            
        Returns:
            Dict: Response data
        """
        try:
            # In a real implementation, you would:
            # 1. Download the recording from the URL
            # 2. Convert speech to text using speech recognition
            # 3. Process the text for relevant information
            
            # For now, return mock data
            return {
                'status': 'success',
                'transcript': f'Voice recording processed for {recording_type}',
                'confidence': 0.85,
                'recording_url': recording_url
            }
            
        except Exception as e:
            logger.error(f"Voice recording processing failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def create_emergency_report_from_ivr(self, call_data: Dict) -> Dict:
        """
        Create emergency report from IVR data
        
        Args:
            call_data (Dict): IVR call data
            
        Returns:
            Dict: Emergency report data
        """
        try:
            from .models import EmergencyReport
            from .location_service import LocationService
            
            # Extract data from call
            phone_number = call_data.get('phone_number', '')
            category = call_data.get('category', 'other')
            severity = call_data.get('severity', 1)
            description = call_data.get('description', 'Emergency reported via voice call')
            location = call_data.get('location', '')
            
            # Detect location from phone number if not provided
            location_info = None
            if not location:
                location_info = LocationService.detect_location_from_phone_number(phone_number)
            
            # Create emergency report
            emergency_report = EmergencyReport.objects.create(
                channel='ivr',
                phone_number=phone_number,
                category=category,
                severity=severity,
                description=description,
                address=location or (LocationService.format_location_for_report(location_info) if location_info else ''),
                district=location_info.get('district') if location_info else None,
                state=location_info.get('state') if location_info else None,
                raw_data={
                    'call_sid': call_data.get('call_sid'),
                    'recording_url': call_data.get('recording_url'),
                    'transcript': call_data.get('transcript')
                }
            )
            
            # Calculate priority score
            emergency_report.priority_score = emergency_report.get_priority_score()
            emergency_report.save()
            
            return {
                'status': 'success',
                'report_id': emergency_report.report_id,
                'emergency_report': emergency_report
            }
            
        except Exception as e:
            logger.error(f"Emergency report creation failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def send_ivr_confirmation(self, phone_number: str, report_id: str) -> Dict:
        """
        Send confirmation call for emergency report
        
        Args:
            phone_number (str): Recipient phone number
            report_id (str): Emergency report ID
            
        Returns:
            Dict: Response status
        """
        try:
            if self.twilio_account_sid and self.twilio_auth_token:
                from twilio.rest import Client
                
                client = Client(self.twilio_account_sid, self.twilio_auth_token)
                
                # Create confirmation call
                call = client.calls.create(
                    to=phone_number,
                    from_=self.twilio_phone_number,
                    url=f"{self.base_url}/emergency/ivr/confirmation/{report_id}/"
                )
                
                return {
                    'status': 'success',
                    'call_sid': call.sid
                }
            else:
                logger.info(f"IVR confirmation call to {phone_number} for report {report_id}")
                return {
                    'status': 'success',
                    'call_sid': f"dev_{int(timezone.now().timestamp())}"
                }
                
        except Exception as e:
            logger.error(f"IVR confirmation call failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }


class IVRWebhookHandler:
    """Handle incoming IVR webhooks"""
    
    @staticmethod
    def handle_call_status(request_data: Dict) -> Dict:
        """
        Handle call status webhook
        
        Args:
            request_data (Dict): Webhook request data
            
        Returns:
            Dict: Response data
        """
        try:
            call_sid = request_data.get('CallSid')
            call_status = request_data.get('CallStatus')
            
            logger.info(f"Call {call_sid} status: {call_status}")
            
            return {
                'status': 'success',
                'message': 'Call status updated'
            }
            
        except Exception as e:
            logger.error(f"Call status webhook handling failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    @staticmethod
    def handle_recording_complete(request_data: Dict) -> Dict:
        """
        Handle recording complete webhook
        
        Args:
            request_data (Dict): Webhook request data
            
        Returns:
            Dict: Response data
        """
        try:
            call_sid = request_data.get('CallSid')
            recording_url = request_data.get('RecordingUrl')
            recording_duration = request_data.get('RecordingDuration')
            
            logger.info(f"Recording complete for call {call_sid}: {recording_url}")
            
            # Process the recording
            ivr_service = IVRService()
            result = ivr_service.process_voice_recording(
                call_sid, recording_url, 'description'
            )
            
            return {
                'status': 'success',
                'recording_url': recording_url,
                'duration': recording_duration,
                'processing_result': result
            }
            
        except Exception as e:
            logger.error(f"Recording complete webhook handling failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
