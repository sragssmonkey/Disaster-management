"""
Location detection and validation service for emergency reports
Handles location detection from phone numbers, addresses, and coordinates
"""

import re
import requests
from typing import Optional, Dict, Tuple
from django.conf import settings

class LocationService:
    """Service for handling location detection and validation"""
    
    # India state and district mapping (simplified)
    INDIA_STATES = {
        'andhra_pradesh': ['visakhapatnam', 'vijayawada', 'guntur', 'tirupati'],
        'arunachal_pradesh': ['itanagar', 'namsai', 'pasighat'],
        'assam': ['guwahati', 'silchar', 'dibrugarh', 'jorhat'],
        'bihar': ['patna', 'gaya', 'bhagalpur', 'muzaffarpur'],
        'chhattisgarh': ['raipur', 'bilaspur', 'durg', 'rajnandgaon'],
        'goa': ['panaji', 'margao', 'vasco_da_gama'],
        'gujarat': ['ahmedabad', 'surat', 'vadodara', 'rajkot'],
        'haryana': ['gurgaon', 'faridabad', 'panipat', 'karnal'],
        'himachal_pradesh': ['shimla', 'dharamshala', 'manali', 'solan'],
        'jharkhand': ['ranchi', 'jamshedpur', 'dhanbad', 'bokaro'],
        'karnataka': ['bangalore', 'mysore', 'hubli', 'mangalore'],
        'kerala': ['thiruvananthapuram', 'kochi', 'kozhikode', 'thrissur'],
        'madhya_pradesh': ['bhopal', 'indore', 'gwalior', 'jabalpur'],
        'maharashtra': ['mumbai', 'pune', 'nagpur', 'nashik'],
        'manipur': ['imphal', 'thoubal', 'bishnupur'],
        'meghalaya': ['shillong', 'tura', 'jowai'],
        'mizoram': ['aizawl', 'lunglei', 'saiha'],
        'nagaland': ['kohima', 'dimapur', 'mokokchung'],
        'odisha': ['bhubaneswar', 'cuttack', 'rourkela', 'berhampur'],
        'punjab': ['chandigarh', 'ludhiana', 'amritsar', 'jalandhar'],
        'rajasthan': ['jaipur', 'jodhpur', 'udaipur', 'kota'],
        'sikkim': ['gangtok', 'namchi', 'gyalshing'],
        'tamil_nadu': ['chennai', 'coimbatore', 'madurai', 'tiruchirapalli'],
        'telangana': ['hyderabad', 'warangal', 'nizamabad', 'khammam'],
        'tripura': ['agartala', 'dharmanagar', 'udaypur'],
        'uttar_pradesh': ['lucknow', 'kanpur', 'agra', 'varanasi'],
        'uttarakhand': ['dehradun', 'haridwar', 'roorkee', 'haldwani'],
        'west_bengal': ['kolkata', 'howrah', 'durgapur', 'asansol']
    }
    
    @staticmethod
    def detect_location_from_phone_number(phone_number: str) -> Optional[Dict]:
        """
        Detect location from phone number using area code mapping
        
        Args:
            phone_number (str): Phone number with country code
            
        Returns:
            Dict: Location information or None
        """
        # Remove any non-digit characters except +
        clean_number = re.sub(r'[^\d+]', '', phone_number)
        
        # India area code mapping (simplified)
        area_codes = {
            '11': {'state': 'Delhi', 'district': 'New Delhi'},
            '22': {'state': 'Maharashtra', 'district': 'Mumbai'},
            '20': {'state': 'Maharashtra', 'district': 'Pune'},
            '40': {'state': 'Telangana', 'district': 'Hyderabad'},
            '44': {'state': 'Tamil Nadu', 'district': 'Chennai'},
            '80': {'state': 'Karnataka', 'district': 'Bangalore'},
            '33': {'state': 'West Bengal', 'district': 'Kolkata'},
            '79': {'state': 'Gujarat', 'district': 'Ahmedabad'},
            '141': {'state': 'Rajasthan', 'district': 'Jaipur'},
            '161': {'state': 'Punjab', 'district': 'Ludhiana'},
            '172': {'state': 'Punjab', 'district': 'Chandigarh'},
            '135': {'state': 'Uttarakhand', 'district': 'Dehradun'},
            '133': {'state': 'Uttar Pradesh', 'district': 'Lucknow'},
            '512': {'state': 'Uttar Pradesh', 'district': 'Kanpur'},
            '542': {'state': 'Uttar Pradesh', 'district': 'Varanasi'},
            '562': {'state': 'Uttar Pradesh', 'district': 'Agra'},
            '120': {'state': 'Uttar Pradesh', 'district': 'Noida'},
            '124': {'state': 'Haryana', 'district': 'Gurgaon'},
            '129': {'state': 'Haryana', 'district': 'Faridabad'},
            '186': {'state': 'Jammu and Kashmir', 'district': 'Srinagar'},
            '191': {'state': 'Jammu and Kashmir', 'district': 'Jammu'},
            '265': {'state': 'Gujarat', 'district': 'Surat'},
            '278': {'state': 'Gujarat', 'district': 'Rajkot'},
            '261': {'state': 'Gujarat', 'district': 'Vadodara'},
            '281': {'state': 'Gujarat', 'district': 'Bhavnagar'},
            '361': {'state': 'Assam', 'district': 'Guwahati'},
            '384': {'state': 'Assam', 'district': 'Silchar'},
            '373': {'state': 'Assam', 'district': 'Dibrugarh'},
            '376': {'state': 'Assam', 'district': 'Jorhat'},
            '385': {'state': 'Assam', 'district': 'Tezpur'},
            '364': {'state': 'Meghalaya', 'district': 'Shillong'},
            '389': {'state': 'Tripura', 'district': 'Agartala'},
            '387': {'state': 'Manipur', 'district': 'Imphal'},
            '385': {'state': 'Nagaland', 'district': 'Kohima'},
            '364': {'state': 'Mizoram', 'district': 'Aizawl'},
            '364': {'state': 'Arunachal Pradesh', 'district': 'Itanagar'},
            '364': {'state': 'Sikkim', 'district': 'Gangtok'},
            '364': {'state': 'Goa', 'district': 'Panaji'},
            '364': {'state': 'Kerala', 'district': 'Thiruvananthapuram'},
            '484': {'state': 'Kerala', 'district': 'Kochi'},
            '495': {'state': 'Kerala', 'district': 'Kozhikode'},
            '487': {'state': 'Kerala', 'district': 'Thrissur'},
            '364': {'state': 'Karnataka', 'district': 'Bangalore'},
            '821': {'state': 'Karnataka', 'district': 'Mysore'},
            '836': {'state': 'Karnataka', 'district': 'Hubli'},
            '824': {'state': 'Karnataka', 'district': 'Mangalore'},
            '364': {'state': 'Tamil Nadu', 'district': 'Chennai'},
            '422': {'state': 'Tamil Nadu', 'district': 'Coimbatore'},
            '452': {'state': 'Tamil Nadu', 'district': 'Madurai'},
            '431': {'state': 'Tamil Nadu', 'district': 'Tiruchirapalli'},
            '364': {'state': 'Andhra Pradesh', 'district': 'Visakhapatnam'},
            '866': {'state': 'Andhra Pradesh', 'district': 'Vijayawada'},
            '863': {'state': 'Andhra Pradesh', 'district': 'Guntur'},
            '877': {'state': 'Andhra Pradesh', 'district': 'Tirupati'},
            '364': {'state': 'Telangana', 'district': 'Hyderabad'},
            '870': {'state': 'Telangana', 'district': 'Warangal'},
            '8462': {'state': 'Telangana', 'district': 'Nizamabad'},
            '8742': {'state': 'Telangana', 'district': 'Khammam'},
            '364': {'state': 'Odisha', 'district': 'Bhubaneswar'},
            '661': {'state': 'Odisha', 'district': 'Cuttack'},
            '661': {'state': 'Odisha', 'district': 'Rourkela'},
            '680': {'state': 'Odisha', 'district': 'Berhampur'},
            '364': {'state': 'Chhattisgarh', 'district': 'Raipur'},
            '775': {'state': 'Chhattisgarh', 'district': 'Bilaspur'},
            '788': {'state': 'Chhattisgarh', 'district': 'Durg'},
            '7744': {'state': 'Chhattisgarh', 'district': 'Rajnandgaon'},
            '364': {'state': 'Madhya Pradesh', 'district': 'Bhopal'},
            '731': {'state': 'Madhya Pradesh', 'district': 'Indore'},
            '751': {'state': 'Madhya Pradesh', 'district': 'Gwalior'},
            '761': {'state': 'Madhya Pradesh', 'district': 'Jabalpur'},
            '364': {'state': 'Maharashtra', 'district': 'Mumbai'},
            '20': {'state': 'Maharashtra', 'district': 'Pune'},
            '712': {'state': 'Maharashtra', 'district': 'Nagpur'},
            '253': {'state': 'Maharashtra', 'district': 'Nashik'},
            '364': {'state': 'Jharkhand', 'district': 'Ranchi'},
            '657': {'state': 'Jharkhand', 'district': 'Jamshedpur'},
            '326': {'state': 'Jharkhand', 'district': 'Dhanbad'},
            '6542': {'state': 'Jharkhand', 'district': 'Bokaro'},
            '364': {'state': 'Bihar', 'district': 'Patna'},
            '612': {'state': 'Bihar', 'district': 'Gaya'},
            '641': {'state': 'Bihar', 'district': 'Bhagalpur'},
            '621': {'state': 'Bihar', 'district': 'Muzaffarpur'},
            '364': {'state': 'Uttar Pradesh', 'district': 'Lucknow'},
            '512': {'state': 'Uttar Pradesh', 'district': 'Kanpur'},
            '562': {'state': 'Uttar Pradesh', 'district': 'Agra'},
            '542': {'state': 'Uttar Pradesh', 'district': 'Varanasi'},
            '120': {'state': 'Uttar Pradesh', 'district': 'Noida'},
            '364': {'state': 'Uttarakhand', 'district': 'Dehradun'},
            '135': {'state': 'Uttarakhand', 'district': 'Haridwar'},
            '1332': {'state': 'Uttarakhand', 'district': 'Roorkee'},
            '5946': {'state': 'Uttarakhand', 'district': 'Haldwani'},
            '364': {'state': 'Himachal Pradesh', 'district': 'Shimla'},
            '177': {'state': 'Himachal Pradesh', 'district': 'Dharamshala'},
            '1902': {'state': 'Himachal Pradesh', 'district': 'Manali'},
            '1792': {'state': 'Himachal Pradesh', 'district': 'Solan'},
            '364': {'state': 'Punjab', 'district': 'Chandigarh'},
            '161': {'state': 'Punjab', 'district': 'Ludhiana'},
            '183': {'state': 'Punjab', 'district': 'Amritsar'},
            '181': {'state': 'Punjab', 'district': 'Jalandhar'},
            '364': {'state': 'Haryana', 'district': 'Gurgaon'},
            '129': {'state': 'Haryana', 'district': 'Faridabad'},
            '180': {'state': 'Haryana', 'district': 'Panipat'},
            '184': {'state': 'Haryana', 'district': 'Karnal'},
            '364': {'state': 'Rajasthan', 'district': 'Jaipur'},
            '141': {'state': 'Rajasthan', 'district': 'Jodhpur'},
            '294': {'state': 'Rajasthan', 'district': 'Udaipur'},
            '744': {'state': 'Rajasthan', 'district': 'Kota'},
            '364': {'state': 'Delhi', 'district': 'New Delhi'},
            '11': {'state': 'Delhi', 'district': 'New Delhi'}
        }
        
        # Extract area code from phone number
        if clean_number.startswith('+91'):
            # Remove country code
            number = clean_number[3:]
        elif clean_number.startswith('91'):
            # Remove country code
            number = clean_number[2:]
        else:
            number = clean_number
        
        # Try to match area codes (from longest to shortest)
        for length in range(4, 0, -1):
            if len(number) >= length:
                area_code = number[:length]
                if area_code in area_codes:
                    return area_codes[area_code]
        
        return None
    
    @staticmethod
    def detect_location_from_address(address: str) -> Optional[Dict]:
        """
        Detect location from address text using keyword matching
        
        Args:
            address (str): Address text
            
        Returns:
            Dict: Location information or None
        """
        if not address:
            return None
        
        address_lower = address.lower()
        
        # Check for state names
        for state, districts in LocationService.INDIA_STATES.items():
            state_name = state.replace('_', ' ')
            if state_name in address_lower:
                # Try to find district
                for district in districts:
                    if district.replace('_', ' ') in address_lower:
                        return {
                            'state': state.replace('_', ' ').title(),
                            'district': district.replace('_', ' ').title()
                        }
                
                # Return state if found but no district
                return {
                    'state': state.replace('_', ' ').title(),
                    'district': 'Unknown'
                }
        
        return None
    
    @staticmethod
    def validate_coordinates(lat: float, lng: float) -> bool:
        """
        Validate if coordinates are within India bounds
        
        Args:
            lat (float): Latitude
            lng (float): Longitude
            
        Returns:
            bool: True if coordinates are valid
        """
        # India bounds (approximate)
        INDIA_BOUNDS = {
            'min_lat': 6.0,
            'max_lat': 37.0,
            'min_lng': 68.0,
            'max_lng': 97.0
        }
        
        return (INDIA_BOUNDS['min_lat'] <= lat <= INDIA_BOUNDS['max_lat'] and
                INDIA_BOUNDS['min_lng'] <= lng <= INDIA_BOUNDS['max_lng'])
    
    @staticmethod
    def get_location_from_coordinates(lat: float, lng: float) -> Optional[Dict]:
        """
        Get location information from coordinates using reverse geocoding
        
        Args:
            lat (float): Latitude
            lng (float): Longitude
            
        Returns:
            Dict: Location information or None
        """
        if not LocationService.validate_coordinates(lat, lng):
            return None
        
        try:
            # Using a free reverse geocoding service (you might want to use a paid service in production)
            url = f"https://api.bigdatacloud.net/data/reverse-geocode-client?latitude={lat}&longitude={lng}&localityLanguage=en"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'state': data.get('principalSubdivision', 'Unknown'),
                    'district': data.get('locality', 'Unknown'),
                    'address': data.get('localityInfo', {}).get('informative', [{}])[0].get('name', 'Unknown')
                }
        except Exception:
            pass
        
        return None
    
    @staticmethod
    def get_emergency_services_location(lat: float, lng: float) -> Dict:
        """
        Get nearest emergency services for a given location
        
        Args:
            lat (float): Latitude
            lng (float): Longitude
            
        Returns:
            Dict: Emergency services information
        """
        # This is a simplified implementation
        # In production, you'd want to integrate with actual emergency services databases
        
        location_info = LocationService.get_location_from_coordinates(lat, lng)
        
        return {
            'police_station': f"Nearest Police Station - {location_info.get('district', 'Unknown')}",
            'hospital': f"Nearest Hospital - {location_info.get('district', 'Unknown')}",
            'fire_station': f"Nearest Fire Station - {location_info.get('district', 'Unknown')}",
            'disaster_management': f"District Disaster Management Authority - {location_info.get('district', 'Unknown')}",
            'emergency_contact': '100 (Police), 101 (Fire), 102 (Ambulance), 108 (Emergency)'
        }
    
    @staticmethod
    def format_location_for_report(location_info: Dict) -> str:
        """
        Format location information for emergency reports
        
        Args:
            location_info (Dict): Location information
            
        Returns:
            str: Formatted location string
        """
        if not location_info:
            return "Location not specified"
        
        parts = []
        if location_info.get('district'):
            parts.append(location_info['district'])
        if location_info.get('state'):
            parts.append(location_info['state'])
        
        return ", ".join(parts) if parts else "Location not specified"
