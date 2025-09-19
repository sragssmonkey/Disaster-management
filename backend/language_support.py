"""
Multi-language support for emergency reporting system
Provides translations for emergency categories, severity levels, and system messages
"""

# Language translations for emergency categories
EMERGENCY_CATEGORIES = {
    'en': {
        'medical': 'Medical Emergency',
        'fire': 'Fire',
        'flood': 'Flood',
        'earthquake': 'Earthquake',
        'cyclone': 'Cyclone',
        'landslide': 'Landslide',
        'roadblock': 'Roadblock',
        'other': 'Other'
    },
    'hi': {
        'medical': 'चिकित्सा आपातकाल',
        'fire': 'आग',
        'flood': 'बाढ़',
        'earthquake': 'भूकंप',
        'cyclone': 'चक्रवात',
        'landslide': 'भूस्खलन',
        'roadblock': 'सड़क अवरोध',
        'other': 'अन्य'
    },
    'bn': {
        'medical': 'চিকিৎসা জরুরি',
        'fire': 'আগুন',
        'flood': 'বন্যা',
        'earthquake': 'ভূমিকম্প',
        'cyclone': 'ঘূর্ণিঝড়',
        'landslide': 'ভূমিধস',
        'roadblock': 'রাস্তা অবরোধ',
        'other': 'অন্যান্য'
    },
    'te': {
        'medical': 'వైద్య అత్యవసర',
        'fire': 'అగ్ని',
        'flood': 'వరద',
        'earthquake': 'భూకంపం',
        'cyclone': 'చక్రవాతం',
        'landslide': 'భూస్ఖలనం',
        'roadblock': 'రహదారి అడ్డంకి',
        'other': 'ఇతర'
    },
    'mr': {
        'medical': 'वैद्यकीय आणीबाणी',
        'fire': 'आग',
        'flood': 'पूर',
        'earthquake': 'भूकंप',
        'cyclone': 'चक्रीवादळ',
        'landslide': 'भूस्खलन',
        'roadblock': 'रस्ता अडथळा',
        'other': 'इतर'
    },
    'ta': {
        'medical': 'மருத்துவ அவசரம்',
        'fire': 'தீ',
        'flood': 'வெள்ளம்',
        'earthquake': 'நிலநடுக்கம்',
        'cyclone': 'சூறைக்காற்று',
        'landslide': 'நிலச்சரிவு',
        'roadblock': 'சாலை தடை',
        'other': 'மற்றவை'
    },
    'gu': {
        'medical': 'વૈદ્યકીય કટોકટી',
        'fire': 'આગ',
        'flood': 'પૂર',
        'earthquake': 'ભૂકંપ',
        'cyclone': 'ચક્રવાત',
        'landslide': 'ભૂસ્ખલન',
        'roadblock': 'રસ્તો અવરોધ',
        'other': 'અન્ય'
    },
    'kn': {
        'medical': 'ವೈದ್ಯಕೀಯ ತುರ್ತು',
        'fire': 'ಬೆಂಕಿ',
        'flood': 'ವೈಪತ್ತು',
        'earthquake': 'ಭೂಕಂಪ',
        'cyclone': 'ಚಂಡಮಾರುತ',
        'landslide': 'ಭೂಕುಸಿತ',
        'roadblock': 'ರಸ್ತೆ ಅಡಚಣೆ',
        'other': 'ಇತರೆ'
    },
    'ml': {
        'medical': 'വൈദ്യ അടിയന്തരം',
        'fire': 'തീ',
        'flood': 'വെള്ളപ്പൊക്കം',
        'earthquake': 'ഭൂകമ്പം',
        'cyclone': 'ചുഴലിക്കാറ്റ്',
        'landslide': 'ഭൂസ്ഖലനം',
        'roadblock': 'റോഡ് തടസ്സം',
        'other': 'മറ്റുള്ളവ'
    },
    'pa': {
        'medical': 'ਡਾਕਟਰੀ ਐਮਰਜੈਂਸੀ',
        'fire': 'ਅੱਗ',
        'flood': 'ਹੜ੍ਹ',
        'earthquake': 'ਭੂਚਾਲ',
        'cyclone': 'ਤੂਫਾਨ',
        'landslide': 'ਭੂਮੀ ਖਿਸਕਣ',
        'roadblock': 'ਸੜਕ ਰੁਕਾਵਟ',
        'other': 'ਹੋਰ'
    },
    'or': {
        'medical': 'ଚିକିତ୍ସା ଜରୁରୀ',
        'fire': 'ଅଗ୍ନି',
        'flood': 'ବନ୍ୟା',
        'earthquake': 'ଭୂକମ୍ପ',
        'cyclone': 'ବାତ୍ୟା',
        'landslide': 'ଭୂସ୍ଖଳନ',
        'roadblock': 'ରାସ୍ତା ଅବରୋଧ',
        'other': 'ଅନ୍ୟ'
    },
    'as': {
        'medical': 'চিকিৎসা জৰুৰী',
        'fire': 'জুই',
        'flood': 'বানপানী',
        'earthquake': 'ভূমিকম্প',
        'cyclone': 'ঘূৰ্ণীবতাহ',
        'landslide': 'ভূমিস্খলন',
        'roadblock': 'ৰাস্তা বাধা',
        'other': 'অন্যান্য'
    }
}

# Severity level translations
SEVERITY_LEVELS = {
    'en': {
        1: 'Low',
        2: 'Medium', 
        3: 'High',
        4: 'Critical'
    },
    'hi': {
        1: 'कम',
        2: 'मध्यम',
        3: 'उच्च',
        4: 'गंभीर'
    },
    'bn': {
        1: 'কম',
        2: 'মাঝারি',
        3: 'উচ্চ',
        4: 'গুরুতর'
    },
    'te': {
        1: 'తక్కువ',
        2: 'మధ్యమ',
        3: 'ఎక్కువ',
        4: 'క్లిష్టమైన'
    },
    'mr': {
        1: 'कमी',
        2: 'मध्यम',
        3: 'उच्च',
        4: 'गंभीर'
    },
    'ta': {
        1: 'குறைவு',
        2: 'நடுத்தரம்',
        3: 'அதிகம்',
        4: 'முக்கியமான'
    },
    'gu': {
        1: 'ઓછું',
        2: 'મધ્યમ',
        3: 'વધુ',
        4: 'ગંભીર'
    },
    'kn': {
        1: 'ಕಡಿಮೆ',
        2: 'ಮಧ್ಯಮ',
        3: 'ಹೆಚ್ಚು',
        4: 'ಗಂಭೀರ'
    },
    'ml': {
        1: 'കുറവ്',
        2: 'ഇടത്തരം',
        3: 'കൂടുതൽ',
        4: 'ഗുരുതരം'
    },
    'pa': {
        1: 'ਘੱਟ',
        2: 'ਮੱਧਮ',
        3: 'ਵੱਧ',
        4: 'ਗੰਭੀਰ'
    },
    'or': {
        1: 'କମ୍',
        2: 'ମଧ୍ୟମ',
        3: 'ଅଧିକ',
        4: 'ଗୁରୁତର'
    },
    'as': {
        1: 'কম',
        2: 'মধ্যম',
        3: 'বেছি',
        4: 'গুৰুতৰ'
    }
}

# System messages in different languages
SYSTEM_MESSAGES = {
    'en': {
        'emergency_received': 'Emergency report received. Help is on the way.',
        'invalid_format': 'Invalid format. Please try again.',
        'select_category': 'Select emergency type:',
        'select_severity': 'Enter severity (1-4):',
        'enter_description': 'Describe the emergency:',
        'report_acknowledged': 'Emergency report acknowledged.',
        'report_resolved': 'Emergency report resolved.',
        'thank_you': 'Thank you for reporting. Emergency services have been notified.'
    },
    'hi': {
        'emergency_received': 'आपातकाल रिपोर्ट प्राप्त हुई। सहायता रास्ते में है।',
        'invalid_format': 'अमान्य प्रारूप। कृपया पुनः प्रयास करें।',
        'select_category': 'आपातकाल प्रकार चुनें:',
        'select_severity': 'गंभीरता दर्ज करें (1-4):',
        'enter_description': 'आपातकाल का वर्णन करें:',
        'report_acknowledged': 'आपातकाल रिपोर्ट स्वीकृत।',
        'report_resolved': 'आपातकाल रिपोर्ट हल।',
        'thank_you': 'रिपोर्ट करने के लिए धन्यवाद। आपातकाल सेवाओं को सूचित किया गया है।'
    },
    'bn': {
        'emergency_received': 'জরুরি রিপোর্ট পেয়েছি। সাহায্য আসছে।',
        'invalid_format': 'ভুল ফরম্যাট। আবার চেষ্টা করুন।',
        'select_category': 'জরুরি ধরন নির্বাচন করুন:',
        'select_severity': 'গুরুত্ব লিখুন (1-4):',
        'enter_description': 'জরুরি বর্ণনা করুন:',
        'report_acknowledged': 'জরুরি রিপোর্ট স্বীকৃত।',
        'report_resolved': 'জরুরি রিপোর্ট সমাধান।',
        'thank_you': 'রিপোর্ট করার জন্য ধন্যবাদ। জরুরি সেবাকে জানানো হয়েছে।'
    },
    'te': {
        'emergency_received': 'అత్యవసర నివేదిక అందింది। సహాయం వస్తోంది।',
        'invalid_format': 'తప్పు ఫార్మాట్। మళ్లీ ప్రయత్నించండి।',
        'select_category': 'అత్యవసర రకాన్ని ఎంచుకోండి:',
        'select_severity': 'తీవ్రతను నమోదు చేయండి (1-4):',
        'enter_description': 'అత్యవసరాన్ని వివరించండి:',
        'report_acknowledged': 'అత్యవసర నివేదిక అంగీకరించబడింది।',
        'report_resolved': 'అత్యవసర నివేదిక పరిష్కరించబడింది।',
        'thank_you': 'నివేదించినందుకు ధన్యవాదాలు। అత్యవసర సేవలకు తెలియజేయబడింది।'
    }
}

def get_translation(language, key, category=None):
    """
    Get translation for a given language and key
    
    Args:
        language (str): Language code (en, hi, bn, etc.)
        key (str): Translation key
        category (str): Category for emergency types
    
    Returns:
        str: Translated text or fallback to English
    """
    if language not in SYSTEM_MESSAGES:
        language = 'en'  # Fallback to English
    
    if category and key in EMERGENCY_CATEGORIES.get(language, {}):
        return EMERGENCY_CATEGORIES[language][key]
    elif key in SEVERITY_LEVELS.get(language, {}):
        return SEVERITY_LEVELS[language][key]
    elif key in SYSTEM_MESSAGES.get(language, {}):
        return SYSTEM_MESSAGES[language][key]
    else:
        # Fallback to English
        return SYSTEM_MESSAGES.get('en', {}).get(key, key)

def get_ussd_menu(language='en', menu_level=1):
    """
    Get USSD menu text for different languages and menu levels
    
    Args:
        language (str): Language code
        menu_level (int): Menu level (1-4)
    
    Returns:
        str: Formatted menu text
    """
    if language not in SYSTEM_MESSAGES:
        language = 'en'
    
    if menu_level == 1:
        categories = EMERGENCY_CATEGORIES.get(language, EMERGENCY_CATEGORIES['en'])
        menu_text = f"{get_translation(language, 'select_category')}\n"
        menu_text += f"1. {categories['medical']}\n"
        menu_text += f"2. {categories['fire']}\n"
        menu_text += f"3. {categories['flood']}\n"
        menu_text += f"4. {categories['earthquake']}\n"
        menu_text += f"5. {categories['other']}"
        return menu_text
    
    elif menu_level == 2:
        severities = SEVERITY_LEVELS.get(language, SEVERITY_LEVELS['en'])
        menu_text = f"{get_translation(language, 'select_severity')}\n"
        menu_text += f"1. {severities[1]}\n"
        menu_text += f"2. {severities[2]}\n"
        menu_text += f"3. {severities[3]}\n"
        menu_text += f"4. {severities[4]}"
        return menu_text
    
    elif menu_level == 3:
        return get_translation(language, 'enter_description')
    
    else:
        return get_translation(language, 'invalid_format')

def detect_language_from_phone_number(phone_number):
    """
    Detect language based on phone number prefix (simplified approach)
    This is a basic implementation - in production, you might want to use
    more sophisticated language detection or user preferences
    
    Args:
        phone_number (str): Phone number
    
    Returns:
        str: Detected language code
    """
    # This is a simplified approach - in reality, you'd need more sophisticated detection
    # or maintain user language preferences in the database
    
    # Basic mapping based on common prefixes (this is just an example)
    if phone_number.startswith('+91'):
        # India - could be any Indian language
        return 'en'  # Default to English for now
    elif phone_number.startswith('+880'):
        # Bangladesh
        return 'bn'
    else:
        return 'en'  # Default fallback

def format_emergency_message(language, report_id, category, severity, description):
    """
    Format emergency report message in the specified language
    
    Args:
        language (str): Language code
        report_id (str): Report ID
        category (str): Emergency category
        severity (int): Severity level
        description (str): Description
    
    Returns:
        str: Formatted message
    """
    category_name = get_translation(language, category, category=True)
    severity_name = get_translation(language, severity)
    
    message = f"Report ID: {report_id}\n"
    message += f"Type: {category_name}\n"
    message += f"Severity: {severity_name}\n"
    message += f"Description: {description}\n"
    message += get_translation(language, 'thank_you')
    
    return message
