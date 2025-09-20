"""
USSD (Unstructured Supplementary Service Data) Service
Handles USSD-based emergency reporting for basic phones
"""

import json
import logging
from typing import Optional, Dict, List
from django.utils import timezone

# Configure logging
logger = logging.getLogger(__name__)

class USSDService:
    """Service for handling USSD operations"""
    
    def __init__(self):
        self.session_timeout = 300  # 5 minutes
        self.max_menu_level = 4
    
    def process_ussd_request(self, phone_number: str, session_id: str, 
                           menu_level: int, user_input: str, 
                           session_data: Dict = None) -> Dict:
        """
        Process USSD request and return appropriate response
        
        Args:
            phone_number (str): User's phone number
            session_id (str): USSD session ID
            menu_level (int): Current menu level
            user_input (str): User input
            session_data (Dict): Session data from previous interactions
            
        Returns:
            Dict: USSD response
        """
        try:
            # Initialize session data if not provided
            if session_data is None:
                session_data = {
                    'phone_number': phone_number,
                    'session_id': session_id,
                    'menu_level': menu_level,
                    'category': None,
                    'severity': None,
                    'description': None,
                    'location': None,
                    'created_at': timezone.now()
                }
            
            # Handle different menu levels
            if menu_level == 1:
                return self._handle_main_menu(phone_number, session_id, user_input, session_data)
            elif menu_level == 2:
                return self._handle_category_selection(phone_number, session_id, user_input, session_data)
            elif menu_level == 3:
                return self._handle_severity_selection(phone_number, session_id, user_input, session_data)
            elif menu_level == 4:
                return self._handle_description_input(phone_number, session_id, user_input, session_data)
            else:
                return self._handle_invalid_menu_level(phone_number, session_id, user_input, session_data)
                
        except Exception as e:
            logger.error(f"USSD request processing failed: {str(e)}")
            return self._generate_error_response("An error occurred. Please try again.")
    
    def _handle_main_menu(self, phone_number: str, session_id: str, 
                         user_input: str, session_data: Dict) -> Dict:
        """Handle main menu (level 1)"""
        from .language_support import get_ussd_menu, detect_language_from_phone_number
        
        # Detect language
        language = detect_language_from_phone_number(phone_number)
        
        # Generate main menu
        menu_text = get_ussd_menu(language, 1)
        
        return {
            'status': 'menu',
            'message': menu_text,
            'menu_level': 2,
            'session_data': session_data
        }
    
    def _handle_category_selection(self, phone_number: str, session_id: str, 
                                 user_input: str, session_data: Dict) -> Dict:
        """Handle category selection (level 2)"""
        from .language_support import get_ussd_menu, detect_language_from_phone_number
        
        # Validate input
        if not user_input.isdigit() or int(user_input) not in [1, 2, 3, 4, 5]:
            return self._generate_error_response("Invalid selection. Please choose 1-5.")
        
        # Map selection to category
        category_map = {
            '1': 'medical',
            '2': 'fire',
            '3': 'flood',
            '4': 'earthquake',
            '5': 'other'
        }
        
        selected_category = category_map[user_input]
        session_data['category'] = selected_category
        
        # Detect language
        language = detect_language_from_phone_number(phone_number)
        
        # Generate severity menu
        menu_text = get_ussd_menu(language, 2)
        
        return {
            'status': 'menu',
            'message': menu_text,
            'menu_level': 3,
            'session_data': session_data
        }
    
    def _handle_severity_selection(self, phone_number: str, session_id: str, 
                                 user_input: str, session_data: Dict) -> Dict:
        """Handle severity selection (level 3)"""
        from .language_support import get_ussd_menu, detect_language_from_phone_number
        
        # Validate input
        if not user_input.isdigit() or int(user_input) not in [1, 2, 3, 4]:
            return self._generate_error_response("Invalid severity. Please choose 1-4.")
        
        selected_severity = int(user_input)
        session_data['severity'] = selected_severity
        
        # Detect language
        language = detect_language_from_phone_number(phone_number)
        
        # Generate description prompt
        menu_text = get_ussd_menu(language, 3)
        
        return {
            'status': 'menu',
            'message': menu_text,
            'menu_level': 4,
            'session_data': session_data
        }
    
    def _handle_description_input(self, phone_number: str, session_id: str, 
                                user_input: str, session_data: Dict) -> Dict:
        """Handle description input (level 4)"""
        from .language_support import detect_language_from_phone_number, get_translation
        
        # Validate input
        if not user_input or len(user_input.strip()) < 3:
            return self._generate_error_response("Please provide a description (at least 3 characters).")
        
        session_data['description'] = user_input.strip()
        
        # Create emergency report
        try:
            from .models import EmergencyReport
            from .location_service import LocationService
            
            # Detect location from phone number
            location_info = LocationService.detect_location_from_phone_number(phone_number)
            
            # Create emergency report
            emergency_report = EmergencyReport.objects.create(
                channel='ussd',
                phone_number=phone_number,
                category=session_data['category'],
                severity=session_data['severity'],
                description=session_data['description'],
                district=location_info.get('district') if location_info else None,
                state=location_info.get('state') if location_info else None,
                raw_data={
                    'session_id': session_id,
                    'session_data': session_data
                }
            )
            
            # Calculate priority score
            emergency_report.priority_score = emergency_report.get_priority_score()
            emergency_report.save()
            
            # Generate confirmation message
            language = detect_language_from_phone_number(phone_number)
            confirmation_message = get_translation(language, 'emergency_received')
            
            return {
                'status': 'success',
                'message': f"{confirmation_message}\nReport ID: {emergency_report.report_id}",
                'report_id': emergency_report.report_id,
                'session_data': session_data
            }
            
        except Exception as e:
            logger.error(f"Emergency report creation failed: {str(e)}")
            return self._generate_error_response("Failed to create report. Please try again.")
    
    def _handle_invalid_menu_level(self, phone_number: str, session_id: str, 
                                 user_input: str, session_data: Dict) -> Dict:
        """Handle invalid menu level"""
        return self._generate_error_response("Invalid menu level. Please start over.")
    
    def _generate_error_response(self, message: str) -> Dict:
        """Generate error response"""
        return {
            'status': 'error',
            'message': message
        }
    
    def create_emergency_report_from_ussd(self, session_data: Dict) -> Dict:
        """
        Create emergency report from USSD session data
        
        Args:
            session_data (Dict): USSD session data
            
        Returns:
            Dict: Emergency report data
        """
        try:
            from .models import EmergencyReport
            from .location_service import LocationService
            
            # Extract data from session
            phone_number = session_data.get('phone_number', '')
            category = session_data.get('category', 'other')
            severity = session_data.get('severity', 1)
            description = session_data.get('description', 'Emergency reported via USSD')
            session_id = session_data.get('session_id', '')
            
            # Detect location from phone number
            location_info = LocationService.detect_location_from_phone_number(phone_number)
            
            # Create emergency report
            emergency_report = EmergencyReport.objects.create(
                channel='ussd',
                phone_number=phone_number,
                category=category,
                severity=severity,
                description=description,
                district=location_info.get('district') if location_info else None,
                state=location_info.get('state') if location_info else None,
                raw_data={
                    'session_id': session_id,
                    'session_data': session_data
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
    
    def get_ussd_menu_text(self, language: str = 'en', menu_level: int = 1) -> str:
        """
        Get USSD menu text for specific language and menu level
        
        Args:
            language (str): Language code
            menu_level (int): Menu level
            
        Returns:
            str: Menu text
        """
        from .language_support import get_ussd_menu
        return get_ussd_menu(language, menu_level)
    
    def validate_ussd_input(self, user_input: str, menu_level: int) -> bool:
        """
        Validate USSD user input based on menu level
        
        Args:
            user_input (str): User input
            menu_level (int): Current menu level
            
        Returns:
            bool: True if valid
        """
        if menu_level == 1:
            # Main menu - no input expected
            return True
        elif menu_level == 2:
            # Category selection - expect 1-5
            return user_input.isdigit() and 1 <= int(user_input) <= 5
        elif menu_level == 3:
            # Severity selection - expect 1-4
            return user_input.isdigit() and 1 <= int(user_input) <= 4
        elif menu_level == 4:
            # Description input - expect text
            return len(user_input.strip()) >= 3
        else:
            return False
    
    def get_ussd_session_key(self, phone_number: str, session_id: str) -> str:
        """
        Generate session key for USSD session
        
        Args:
            phone_number (str): User's phone number
            session_id (str): USSD session ID
            
        Returns:
            str: Session key
        """
        return f"ussd_session:{phone_number}:{session_id}"
    
    def cleanup_expired_sessions(self) -> int:
        """
        Clean up expired USSD sessions
        
        Returns:
            int: Number of sessions cleaned up
        """
        try:
            # This would typically use Redis or database to store sessions
            # For now, return 0 as we're not implementing session storage
            return 0
        except Exception as e:
            logger.error(f"Session cleanup failed: {str(e)}")
            return 0


class USSDWebhookHandler:
    """Handle incoming USSD webhooks"""
    
    @staticmethod
    def handle_ussd_request(request_data: Dict) -> Dict:
        """
        Handle USSD request webhook
        
        Args:
            request_data (Dict): Webhook request data
            
        Returns:
            Dict: Response data
        """
        try:
            phone_number = request_data.get('phone_number', '')
            session_id = request_data.get('session_id', '')
            menu_level = int(request_data.get('menu_level', 1))
            user_input = request_data.get('user_input', '')
            session_data = request_data.get('session_data', {})
            
            if not phone_number:
                return {
                    'status': 'error',
                    'message': 'Phone number is required'
                }
            
            # Process USSD request
            ussd_service = USSDService()
            result = ussd_service.process_ussd_request(
                phone_number, session_id, menu_level, user_input, session_data
            )
            
            return result
            
        except Exception as e:
            logger.error(f"USSD request handling failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    @staticmethod
    def handle_ussd_session_end(request_data: Dict) -> Dict:
        """
        Handle USSD session end webhook
        
        Args:
            request_data (Dict): Webhook request data
            
        Returns:
            Dict: Response data
        """
        try:
            phone_number = request_data.get('phone_number', '')
            session_id = request_data.get('session_id', '')
            
            logger.info(f"USSD session ended for {phone_number}: {session_id}")
            
            return {
                'status': 'success',
                'message': 'Session ended'
            }
            
        except Exception as e:
            logger.error(f"USSD session end handling failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
