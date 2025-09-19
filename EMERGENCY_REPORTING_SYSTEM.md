# Emergency Reporting System Documentation

## Overview

The Emergency Reporting System allows citizens to report emergencies through multiple channels (SMS, IVR, USSD) in their local language, ensuring accessibility even in areas with poor or no internet connectivity.

## Features

### 1. Multi-Channel Reporting
- **SMS**: Text-based emergency reporting
- **IVR**: Voice-based emergency reporting through phone calls
- **USSD**: Menu-based emergency reporting for basic phones
- **Web Interface**: Traditional web-based reporting

### 2. Multi-Language Support
- English, Hindi, Bengali, Telugu, Marathi, Tamil, Gujarati, Kannada, Malayalam, Punjabi, Odia, Assamese
- Automatic language detection based on phone number
- Localized emergency categories and responses

### 3. Location Detection
- Automatic location detection from phone numbers
- Address parsing and validation
- Coordinate-based location services

### 4. Priority Scoring
- Intelligent priority calculation based on:
  - Emergency category
  - Severity level
  - Location proximity to emergency services
  - Historical data

## API Endpoints

### Emergency Reporting

#### SMS Emergency Report
```
POST /emergency/sms/
```
**Request Body:**
```json
{
    "phone_number": "+919876543210",
    "message": "EMERGENCY flood 3 water level rising fast near main road"
}
```

**SMS Format:**
```
EMERGENCY <category> <severity> <description>
```

**Categories:** medical, fire, flood, earthquake, cyclone, landslide, roadblock, other
**Severity:** 1 (Low), 2 (Medium), 3 (High), 4 (Critical)

#### IVR Emergency Report
```
POST /emergency/ivr/
```
**Request Body:**
```json
{
    "phone_number": "+919876543210",
    "call_id": "CA1234567890",
    "transcript": "There's a fire in my building",
    "category": "fire",
    "severity": 3,
    "location": "123 Main Street, Mumbai"
}
```

#### USSD Emergency Report
```
POST /emergency/ussd/
```
**Request Body:**
```json
{
    "phone_number": "+919876543210",
    "session_id": "USS1234567890",
    "menu_level": 1,
    "selected_option": "1",
    "user_input": "",
    "session_data": {}
}
```

### Emergency Report Management

#### List Emergency Reports
```
GET /emergency/reports/
```
**Query Parameters:**
- `status`: Filter by status (pending, acknowledged, in_progress, resolved, false_alarm)
- `category`: Filter by category
- `severity`: Filter by severity (1-4)
- `channel`: Filter by channel (sms, ivr, ussd, web)

#### Get Emergency Report Details
```
GET /emergency/reports/{report_id}/
```

#### Acknowledge Emergency Report
```
POST /emergency/reports/{report_id}/acknowledge/
```

#### Update Emergency Report Status
```
POST /emergency/reports/{report_id}/status/
```
**Request Body:**
```json
{
    "status": "in_progress",
    "message": "Emergency services dispatched"
}
```

### Webhook Endpoints

#### SMS Webhook
```
POST /webhooks/sms/
```
Handles incoming SMS from SMS gateway providers.

#### IVR Webhook
```
POST /webhooks/ivr/
```
Handles IVR call events and recordings.

#### USSD Webhook
```
POST /webhooks/ussd/
```
Handles USSD session events.

### TwiML Endpoints (for Twilio IVR)

#### Welcome Message
```
GET /ivr/twiml/welcome/
```

#### Category Selection
```
GET /ivr/twiml/category/
```

#### Severity Selection
```
GET /ivr/twiml/severity/
```

#### Description Prompt
```
GET /ivr/twiml/description/
```

#### Location Prompt
```
GET /ivr/twiml/location/
```

#### Confirmation
```
GET /ivr/twiml/confirmation/?report_id=EMR-12345678
```

## Database Models

### EmergencyReport
- `report_id`: Unique report identifier
- `channel`: Reporting channel (sms, ivr, ussd, web)
- `language`: Language code
- `phone_number`: Reporter's phone number
- `caller_name`: Reporter's name (optional)
- `category`: Emergency category
- `severity`: Severity level (1-4)
- `description`: Emergency description
- `lat`, `lng`: Coordinates
- `address`: Location address
- `district`, `state`: Administrative divisions
- `status`: Report status
- `assigned_to`: Assigned responder
- `priority_score`: Calculated priority score
- `raw_data`: Original channel data
- `created_at`, `updated_at`: Timestamps

### EmergencyResponse
- `emergency_report`: Related emergency report
- `responder`: Responding user
- `response_type`: Type of response
- `message`: Response message
- `created_at`: Timestamp

## Configuration

### Environment Variables

```bash
# Twilio Configuration (for SMS and IVR)
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890

# SMS Gateway Configuration (alternative to Twilio)
SMS_GATEWAY_URL=https://api.smsgateway.com/send
SMS_GATEWAY_API_KEY=your_api_key

# Base URL for webhooks
BASE_URL=https://yourdomain.com
```

### Django Settings

Add to `settings.py`:
```python
# Emergency Reporting System
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
SMS_GATEWAY_URL = os.getenv('SMS_GATEWAY_URL')
SMS_GATEWAY_API_KEY = os.getenv('SMS_GATEWAY_API_KEY')
BASE_URL = os.getenv('BASE_URL', 'http://localhost:8000')
```

## Usage Examples

### SMS Reporting

1. **Send SMS to emergency number:**
   ```
   EMERGENCY flood 3 water level rising fast near main road
   ```

2. **System Response:**
   ```
   Emergency report EMR-12345678 received. Help is on the way.
   ```

### IVR Reporting

1. **Call emergency number**
2. **Follow voice prompts:**
   - Select emergency type (1-5)
   - Rate severity (1-4)
   - Describe emergency
   - Provide location

### USSD Reporting

1. **Dial USSD code** (e.g., *123#)
2. **Follow menu prompts:**
   - Select emergency type
   - Rate severity
   - Enter description
   - Confirm report

## Multi-Language Support

### Supported Languages
- English (en)
- Hindi (hi)
- Bengali (bn)
- Telugu (te)
- Marathi (mr)
- Tamil (ta)
- Gujarati (gu)
- Kannada (kn)
- Malayalam (ml)
- Punjabi (pa)
- Odia (or)
- Assamese (as)

### Language Detection
The system automatically detects language based on:
- Phone number area codes
- User preferences (if available)
- Default fallback to English

## Location Services

### Automatic Location Detection
- **Phone Number**: Area code mapping to states/districts
- **Address Parsing**: Text-based location extraction
- **Coordinates**: GPS-based location services

### Location Validation
- India boundary validation
- Administrative division mapping
- Emergency services proximity

## Priority Scoring Algorithm

### Base Score Calculation
```
base_score = severity * 25
```

### Category Multipliers
- Medical: 1.5x
- Fire: 1.4x
- Earthquake: 1.3x
- Flood: 1.2x
- Cyclone: 1.2x
- Landslide: 1.1x
- Roadblock: 1.0x
- Other: 0.9x

### Final Priority Score
```
priority_score = base_score * category_multiplier
```

## Security Considerations

### Input Validation
- Phone number format validation
- Message content sanitization
- Coordinate boundary checking

### Rate Limiting
- SMS rate limiting per phone number
- IVR call frequency limits
- USSD session timeout

### Data Privacy
- Phone number encryption
- Personal information protection
- Audit trail maintenance

## Monitoring and Analytics

### Key Metrics
- Reports per channel
- Response times
- Resolution rates
- Language distribution
- Geographic distribution

### Alerts
- High-priority reports
- System failures
- Unusual patterns
- Capacity thresholds

## Deployment

### Prerequisites
- Django 5.2.6+
- Python 3.8+
- PostgreSQL/MySQL
- Redis (for caching)
- SMS Gateway (Twilio or custom)

### Installation
```bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
```

### Production Setup
1. Configure environment variables
2. Set up SMS gateway
3. Configure webhook URLs
4. Set up monitoring
5. Test all channels

## Testing

### Unit Tests
```bash
python manage.py test backend.tests
```

### Integration Tests
- SMS gateway integration
- IVR call flow testing
- USSD menu testing
- Webhook handling

### Load Testing
- Concurrent report processing
- Database performance
- API response times

## Troubleshooting

### Common Issues

1. **SMS not received**
   - Check phone number format
   - Verify SMS gateway configuration
   - Check rate limits

2. **IVR not working**
   - Verify Twilio configuration
   - Check TwiML endpoints
   - Test webhook URLs

3. **USSD menu issues**
   - Check session management
   - Verify menu level logic
   - Test input validation

### Debug Mode
Enable debug logging:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'emergency_reports.log',
        },
    },
    'loggers': {
        'backend': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

## Support

For technical support or questions about the Emergency Reporting System, please contact the development team or refer to the API documentation.

## License

This system is part of the Disaster Management Platform and follows the same licensing terms.
