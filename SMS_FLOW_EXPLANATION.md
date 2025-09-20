# 📱 SMS Emergency Reporting Flow - Complete Guide

## 🔄 **How SMS Emergency Reporting Works**

### **Step 1: Citizen Sends Emergency SMS**
```
📱 Citizen's Phone (Any Indian Network)
    ↓
📡 Mobile Network (Airtel/Vodafone/Jio/BSNL)
    ↓
🌐 SMS Gateway (MSG91)
    ↓
🔗 Your ResQMap System (https://disaster-management-z940.onrender.com)
    ↓
📊 Emergency Report Created in Database
    ↓
👮 Emergency Response Team Notified
```

## 📍 **Where Messages Go - 3 Options**

### **Option 1: Direct SMS to Your MSG91 Number (Easiest)**
```
Citizen sends SMS to: +91-XXXX-XXXXXX (Your MSG91 number)
Message: "EMERGENCY flood 3 water level rising fast"
```

**How it works:**
1. Citizen sends SMS to your MSG91 number
2. MSG91 receives the SMS
3. MSG91 sends webhook to your system
4. Your system processes the emergency
5. Response sent back to citizen

### **Option 2: SMS to Short Code (Professional)**
```
Citizen sends SMS to: 12345 (Short Code)
Message: "EMERGENCY flood 3 water level rising fast"
```

**How it works:**
1. Citizen sends SMS to short code
2. Short code provider forwards to MSG91
3. MSG91 processes and sends to your system
4. Your system creates emergency report
5. Response sent back to citizen

### **Option 3: USSD Menu (Advanced)**
```
Citizen dials: *123#
Menu appears:
1. Medical Emergency
2. Fire
3. Flood
4. Earthquake
5. Other
```

**How it works:**
1. Citizen dials USSD code
2. USSD gateway shows menu
3. Citizen selects emergency type
4. System collects details
5. Emergency report created

## 🔧 **Technical Implementation**

### **SMS Webhook Flow:**
```
1. Citizen SMS → MSG91 → Your System
2. Your System → Parse Emergency → Create Report
3. Your System → Send Confirmation → Citizen
4. Your System → Notify Emergency Team
```

### **API Endpoints:**
```
POST /emergency/sms/          # Receive SMS
POST /webhooks/sms/           # MSG91 webhook
GET  /emergency/reports/      # View reports
POST /emergency/reports/{id}/acknowledge/  # Acknowledge
```

## 📱 **Where Citizens Can Send Messages**

### **1. Your MSG91 Number (Primary)**
```
Number: +91-XXXX-XXXXXX
Format: EMERGENCY <category> <severity> <description>
Example: EMERGENCY flood 3 water level rising fast
```

### **2. Short Code (Professional)**
```
Number: 12345 (or your chosen short code)
Format: EMERGENCY <category> <severity> <description>
Example: EMERGENCY fire 4 building on fire
```

### **3. USSD Menu (Advanced)**
```
Code: *123#
Process: Interactive menu system
Example: Select 1 for Medical, 2 for Fire, etc.
```

## 🌐 **Webhook Configuration**

### **MSG91 Webhook Setup:**
```
Webhook URL: https://disaster-management-z940.onrender.com/webhooks/sms/
Method: POST
Content-Type: application/json
```

### **Webhook Data Format:**
```json
{
  "From": "+919876543210",
  "Body": "EMERGENCY flood 3 water level rising fast",
  "To": "+91-XXXX-XXXXXX",
  "MessageId": "MSG123456789"
}
```

## 🔄 **Complete SMS Flow Example**

### **Step 1: Citizen Sends SMS**
```
From: +919876543210
To: +91-XXXX-XXXXXX
Message: "EMERGENCY flood 3 water level rising fast"
```

### **Step 2: MSG91 Processes**
```
MSG91 receives SMS
↓
MSG91 sends webhook to your system
↓
Your system parses emergency data
↓
Emergency report created with ID: EMR-ABC123
```

### **Step 3: System Response**
```
Your system sends confirmation SMS:
"Emergency report EMR-ABC123 received. Help is on the way."
```

### **Step 4: Emergency Team Notification**
```
Emergency team receives notification:
- Report ID: EMR-ABC123
- Category: Flood
- Severity: 3 (High)
- Description: Water level rising fast
- Location: Auto-detected from phone number
- Citizen: +919876543210
```

## 📊 **Message Routing**

### **Incoming Messages:**
```
Citizen SMS → MSG91 → Your System → Database → Emergency Team
```

### **Outgoing Messages:**
```
Your System → MSG91 → Citizen Phone
```

## 🔧 **Setup Requirements**

### **1. MSG91 Account**
- Sign up at [msg91.com](https://msg91.com)
- Get Auth Key and Sender ID
- Configure webhook URL

### **2. Phone Number**
- Get Indian phone number from MSG91
- Configure webhook for incoming SMS
- Set up sender ID

### **3. System Configuration**
```bash
MSG91_AUTH_KEY=your_auth_key_here
MSG91_SENDER_ID=DISASTER
MSG91_ROUTE=4
MSG91_COUNTRY=91
```

## 📱 **Testing Your System**

### **Test SMS Sending:**
```bash
curl -X POST https://disaster-management-z940.onrender.com/emergency/sms/ \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+919876543210",
    "message": "EMERGENCY flood 3 water level rising fast"
  }'
```

### **Test Webhook:**
```bash
curl -X POST https://disaster-management-z940.onrender.com/webhooks/sms/ \
  -H "Content-Type: application/json" \
  -d '{
    "From": "+919876543210",
    "Body": "EMERGENCY fire 4 building on fire",
    "To": "+91-XXXX-XXXXXX"
  }'
```

## 🎯 **Summary**

**Where messages go:**
1. **Citizen SMS** → **MSG91** → **Your System** → **Emergency Team**
2. **Your System** → **MSG91** → **Citizen Phone** (confirmations)

**Where citizens can send:**
1. **Your MSG91 number** (primary method)
2. **Short code** (professional method)
3. **USSD menu** (advanced method)

**Your system is live at:**
**https://disaster-management-z940.onrender.com**

The SMS flow is completely automated - citizens just send SMS and your system handles everything! 🚀
