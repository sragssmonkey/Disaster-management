# 🚀 MSG91 Setup Guide for India Emergency Reporting System

## 📱 **Why MSG91 for India?**

MSG91 is the **#1 SMS provider in India** with:
- ✅ **Excellent India coverage** (all networks)
- ✅ **Low cost** (₹0.15 per SMS)
- ✅ **High delivery rates** (99%+)
- ✅ **Unicode support** for Indian languages
- ✅ **Transactional SMS** support
- ✅ **Easy integration** with Django

## 🔧 **Step 1: Sign up for MSG91**

### **1.1 Create MSG91 Account**
1. Go to [msg91.com](https://msg91.com/)
2. **Click "Sign Up"**
3. **Enter your details:**
   - Name: Your Name
   - Email: your-email@example.com
   - Phone: Your Indian mobile number
   - Company: Disaster Management System
4. **Verify your email and phone**

### **1.2 Get Your Credentials**
1. **Login to MSG91 Dashboard**
2. **Go to API → API Details**
3. **Copy your credentials:**
   - **Auth Key**: `your_auth_key_here`
   - **Sender ID**: `DISASTER` (or your preferred name)
   - **Route**: `4` (Transactional)

## 🔧 **Step 2: Configure Your System**

### **2.1 Update Environment Variables**

Add these to your **Render.com Environment Variables**:

```bash
# MSG91 Configuration (Primary)
MSG91_AUTH_KEY=your_auth_key_here
MSG91_SENDER_ID=DISASTER
MSG91_ROUTE=4
MSG91_COUNTRY=91

# Base URL
BASE_URL=https://disaster-management-z940.onrender.com
```

### **2.2 Test Your Configuration**

```bash
# Test SMS sending
curl -X POST https://disaster-management-z940.onrender.com/emergency/sms/ \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+919876543210",
    "message": "EMERGENCY flood 3 water level rising fast near main road"
  }'
```

## 📱 **Step 3: MSG91 Features for India**

### **3.1 Indian Language Support**
MSG91 supports **all Indian languages**:
- Hindi (हिंदी)
- Bengali (বাংলা)
- Telugu (తెలుగు)
- Tamil (தமிழ்)
- Marathi (मराठी)
- Gujarati (ગુજરાતી)
- Kannada (ಕನ್ನಡ)
- Malayalam (മലയാളം)
- Punjabi (ਪੰਜਾਬੀ)
- Odia (ଓଡ଼ିଆ)
- Assamese (অসমীয়া)

### **3.2 SMS Formats Supported**
```
# Emergency SMS Format
EMERGENCY <category> <severity> <description>

# Examples:
EMERGENCY flood 3 water level rising fast
EMERGENCY fire 4 building on fire
EMERGENCY medical 2 person injured
EMERGENCY earthquake 4 building collapsed
```

### **3.3 Automatic Language Detection**
The system automatically detects language based on phone number area code:
- **Delhi (11)**: Hindi
- **Mumbai (22)**: Marathi
- **Chennai (44)**: Tamil
- **Bangalore (80)**: Kannada
- **Hyderabad (40)**: Telugu
- **Kolkata (33)**: Bengali

## 🚀 **Step 4: Deploy and Test**

### **4.1 Deploy to Render.com**
```bash
# Your system is already deployed at:
https://disaster-management-z940.onrender.com
```

### **4.2 Test Emergency Reporting**

#### **SMS Emergency Reporting:**
```
Send SMS to your MSG91 number:
EMERGENCY flood 3 water level rising fast near main road

Response:
Emergency report EMR-XXXXXX received. Help is on the way.
```

#### **Multi-Language SMS:**
```
Hindi: आपातकालीन रिपोर्ट EMR-XXXXXX प्राप्त हुई। सहायता रास्ते में है।
Tamil: அவசரகால அறிக்கை EMR-XXXXXX பெறப்பட்டது। உதவி வருகிறது।
Bengali: জরুরি রিপোর্ট EMR-XXXXXX পাওয়া গেছে। সাহায্য আসছে।
```

## 💰 **Step 5: MSG91 Pricing for India**

### **5.1 SMS Pricing**
- **Transactional SMS**: ₹0.15 per SMS
- **Promotional SMS**: ₹0.12 per SMS
- **International SMS**: ₹2.50 per SMS

### **5.2 Free Credits**
- **New accounts**: ₹100 free credits
- **Referral bonus**: ₹50 per referral
- **Monthly bonus**: ₹25 for active accounts

### **5.3 Cost Calculation**
```
1000 SMS = ₹150
5000 SMS = ₹750
10000 SMS = ₹1500
```

## 🔧 **Step 6: Advanced Configuration**

### **6.1 Custom Sender ID**
```python
# In your Django settings
MSG91_SENDER_ID = 'DISASTER'  # Your custom sender ID
```

### **6.2 Route Configuration**
```python
# Route 4 = Transactional (recommended for emergency)
MSG91_ROUTE = '4'

# Route 1 = Promotional (cheaper but lower priority)
MSG91_ROUTE = '1'
```

### **6.3 Unicode Support**
```python
# For Indian languages
unicode = '1' if language != 'en' else '0'
```

## 📊 **Step 7: Monitoring and Analytics**

### **7.1 MSG91 Dashboard**
- **Real-time delivery reports**
- **SMS delivery status**
- **Cost tracking**
- **Performance analytics**

### **7.2 API Monitoring**
```bash
# Check SMS delivery status
curl https://disaster-management-z940.onrender.com/emergency/reports/
```

## 🚨 **Step 8: Emergency Contacts Integration**

### **8.1 India Emergency Numbers**
- **Police**: 100
- **Fire**: 101
- **Ambulance**: 102
- **Disaster Management**: 108

### **8.2 Automatic Emergency Instructions**
The system automatically sends:
- **Category-specific instructions**
- **Emergency contact numbers**
- **Safety guidelines**
- **Follow-up instructions**

## ✅ **Step 9: Testing Checklist**

### **9.1 Basic Testing**
- [ ] SMS sending works
- [ ] Emergency parsing works
- [ ] Multi-language support works
- [ ] Location detection works
- [ ] Report creation works

### **9.2 Advanced Testing**
- [ ] Unicode SMS works
- [ ] Emergency instructions sent
- [ ] Status updates work
- [ ] Webhook integration works
- [ ] Cost tracking works

## 🎯 **Step 10: Go Live**

### **10.1 Production Checklist**
- [ ] MSG91 account verified
- [ ] Environment variables set
- [ ] SMS testing completed
- [ ] Emergency contacts configured
- [ ] Monitoring setup
- [ ] Cost tracking enabled

### **10.2 Launch Your System**
Your **ResQMap Emergency Reporting System** is now ready for India! 🇮🇳

**Features:**
- ✅ **Multi-channel reporting** (SMS, IVR, USSD, Web)
- ✅ **12 Indian languages** supported
- ✅ **Smart location detection**
- ✅ **Priority scoring system**
- ✅ **India emergency contacts**
- ✅ **Real-time monitoring**

**Your system is now live at:**
**https://disaster-management-z940.onrender.com**

## 📞 **Support**

- **MSG91 Support**: [support.msg91.com](https://support.msg91.com)
- **Documentation**: [docs.msg91.com](https://docs.msg91.com)
- **API Reference**: [api.msg91.com](https://api.msg91.com)

---

**🎉 Congratulations! Your India-specific Emergency Reporting System is ready!**
