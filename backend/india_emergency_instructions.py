"""
India-specific emergency instructions and contact information
Provides localized emergency guidance for Indian citizens
"""

# India Emergency Contact Numbers
INDIA_EMERGENCY_CONTACTS = {
    'police': '100',
    'fire': '101', 
    'ambulance': '102',
    'disaster_management': '108',
    'women_helpline': '1091',
    'child_helpline': '1098',
    'mental_health': '1800-599-0019',
    'flood_helpline': '1800-180-5522',
    'earthquake_helpline': '1800-180-5522',
    'cyclone_helpline': '1800-180-5522'
}

# India-specific emergency instructions in multiple languages
INDIA_EMERGENCY_INSTRUCTIONS = {
    'hi': {
        'medical': "चिकित्सा आपातकाल: शांत रहें। एम्बुलेंस के लिए 102 पर कॉल करें। स्पष्ट स्थान बताएं। रोगी को हिलाएं नहीं।",
        'fire': "आग का आपातकाल: तुरंत निकलें। फायर डिपार्टमेंट के लिए 101 पर कॉल करें। लिफ्ट का उपयोग न करें।",
        'flood': "बाढ़ का आपातकाल: ऊंची जगह पर जाएं। बाढ़ के पानी से बचें। बचाव के लिए 100 पर कॉल करें।",
        'earthquake': "भूकंप: बैठ जाएं, ढकें, पकड़ें। सुरक्षित हो तो घर के अंदर रहें। खिड़कियों से बचें।",
        'cyclone': "चक्रवात: घर के अंदर रहें। खिड़कियां बंद रखें। बिजली काट दें। 108 पर कॉल करें।",
        'landslide': "भूस्खलन: तुरंत सुरक्षित जगह पर जाएं। पहाड़ी क्षेत्र से दूर रहें। 100 पर कॉल करें।"
    },
    'en': {
        'medical': "MEDICAL EMERGENCY: Stay calm. Call 102 for ambulance. Provide clear location. Do not move patient if injured.",
        'fire': "FIRE EMERGENCY: Evacuate immediately. Call 101 for fire department. Do not use elevators. Stay low if smoke present.",
        'flood': "FLOOD EMERGENCY: Move to higher ground. Avoid walking through floodwater. Call 100 for rescue. Stay informed.",
        'earthquake': "EARTHQUAKE: Drop, Cover, Hold. Stay indoors if safe. Avoid windows. Call 100 if trapped.",
        'cyclone': "CYCLONE: Stay indoors. Close windows. Turn off electricity. Call 108 for help.",
        'landslide': "LANDSLIDE: Move to safe area immediately. Stay away from hilly areas. Call 100 for rescue."
    },
    'te': {
        'medical': "వైద్య అత్యవసర: ప్రశాంతంగా ఉండండి. అంబులెన్స్ కోసం 102 కాల్ చేయండి. స్పష్టమైన స్థానాన్ని అందించండి.",
        'fire': "అగ్ని అత్యవసర: వెంటనే బయటకు వెళ్లండి. అగ్నిమాపక దళానికి 101 కాల్ చేయండి. లిఫ్ట్ ఉపయోగించవద్దు.",
        'flood': "వరద అత్యవసర: ఎత్తైన ప్రదేశానికి వెళ్లండి. వరద నీటిలో నడవవద్దు. రక్షణ కోసం 100 కాల్ చేయండి.",
        'earthquake': "భూకంపం: కూర్చోండి, కప్పుకోండి, పట్టుకోండి. సురక్షితంగా ఉంటే ఇంటి లోపల ఉండండి.",
        'cyclone': "చక్రవాతం: ఇంటి లోపల ఉండండి. కిటికీలు మూసేయండి. విద్యుత్ కత్తిరించండి. 108 కాల్ చేయండి.",
        'landslide': "భూస్ఖలనం: వెంటనే సురక్షిత ప్రదేశానికి వెళ్లండి. కొండ ప్రాంతాలకు దూరంగా ఉండండి."
    },
    'ta': {
        'medical': "மருத்துவ அவசரம்: அமைதியாக இருங்கள். ஆம்புலன்ஸுக்கு 102 அழைக்கவும். தெளிவான இடத்தை வழங்கவும்.",
        'fire': "தீ அவசரம்: உடனடியாக வெளியேறவும். தீயணைப்பு படைக்கு 101 அழைக்கவும். உயர்த்தி பயன்படுத்த வேண்டாம்.",
        'flood': "வெள்ள அவசரம்: உயரமான இடத்திற்கு செல்லவும். வெள்ள நீரில் நடக்க வேண்டாம். மீட்புக்கு 100 அழைக்கவும்.",
        'earthquake': "நிலநடுக்கம்: உட்காருங்கள், மறைக்கவும், பிடிக்கவும். பாதுகாப்பாக இருந்தால் வீட்டிற்குள் இருங்கள்.",
        'cyclone': "சூறைக்காற்று: வீட்டிற்குள் இருங்கள். ஜன்னல்களை மூடுங்கள். மின்சாரத்தை அணைக்கவும். 108 அழைக்கவும்.",
        'landslide': "நிலச்சரிவு: உடனடியாக பாதுகாப்பான இடத்திற்கு செல்லவும். மலைப்பகுதிகளிலிருந்து விலகி இருங்கள்."
    },
    'bn': {
        'medical': "চিকিৎসা জরুরি: শান্ত থাকুন। অ্যাম্বুলেন্সের জন্য ১০২ ডাকুন। স্পষ্ট অবস্থান দিন।",
        'fire': "আগুনের জরুরি: সঙ্গে সঙ্গে বেরিয়ে আসুন। ফায়ার ডিপার্টমেন্টের জন্য ১০১ ডাকুন।",
        'flood': "বন্যার জরুরি: উঁচু জায়গায় যান। বন্যার পানিতে হাঁটবেন না। উদ্ধারের জন্য ১০০ ডাকুন।",
        'earthquake': "ভূমিকম্প: বসুন, ঢাকুন, ধরে রাখুন। নিরাপদ হলে ঘরের ভিতরে থাকুন। জানালা এড়িয়ে চলুন।",
        'cyclone': "ঘূর্ণিঝড়: ঘরের ভিতরে থাকুন। জানালা বন্ধ রাখুন। বিদ্যুৎ বন্ধ করুন। ১০৮ ডাকুন।",
        'landslide': "ভূমিধস: সঙ্গে সঙ্গে নিরাপদ জায়গায় যান। পাহাড়ি এলাকা এড়িয়ে চলুন। ১০০ ডাকুন।"
    }
}

def get_india_emergency_instructions(language, category):
    """
    Get India-specific emergency instructions
    
    Args:
        language (str): Language code
        category (str): Emergency category
    
    Returns:
        str: Emergency instructions
    """
    return INDIA_EMERGENCY_INSTRUCTIONS.get(language, INDIA_EMERGENCY_INSTRUCTIONS['en']).get(category, "Follow emergency procedures.")

def get_india_emergency_contacts():
    """
    Get India emergency contact numbers
    
    Returns:
        dict: Emergency contact numbers
    """
    return INDIA_EMERGENCY_CONTACTS

def format_india_emergency_message(language, report_id, category, severity, description):
    """
    Format emergency message for India with local contacts
    
    Args:
        language (str): Language code
        report_id (str): Report ID
        category (str): Emergency category
        severity (int): Severity level
        description (str): Description
    
    Returns:
        str: Formatted message
    """
    from .language_support import get_translation
    
    # Get emergency instructions
    instructions = get_india_emergency_instructions(language, category)
    
    # Get emergency contacts
    contacts = get_india_emergency_contacts()
    
    # Format message
    message = f"🚨 EMERGENCY REPORT {report_id} 🚨\n"
    message += f"Type: {get_translation(language, category, category=True)}\n"
    message += f"Severity: {get_translation(language, severity)}\n"
    message += f"Description: {description}\n\n"
    message += f"Instructions: {instructions}\n\n"
    message += f"Emergency Contacts:\n"
    message += f"Police: {contacts['police']}\n"
    message += f"Fire: {contacts['fire']}\n"
    message += f"Ambulance: {contacts['ambulance']}\n"
    message += f"Disaster Management: {contacts['disaster_management']}\n\n"
    message += f"Help is on the way! Stay safe."
    
    return message
