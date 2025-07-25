## 🌍 **Postman Environment Files Created!**

I've created **3 environment files** for your PerfBurger API testing:

### **📂 Files Created:**

#### **1. Main Environment** - `PerfBurger_Environment.postman_environment.json`
- **Purpose**: General testing environment
- **Variables**: All essential variables for API testing

#### **2. Development Environment** - `PerfBurger_Development.postman_environment.json`  
- **Purpose**: Local development testing
- **URL**: `http://localhost:5000`
- **Features**: Debug mode enabled, dev-specific test users

#### **3. Production Environment** - `PerfBurger_Production.postman_environment.json`
- **Purpose**: Production API testing (when deployed)
- **URL**: `https://api.perfburger.com` (placeholder)
- **Features**: SSL verification, production settings

---

## 🚀 **How to Import and Use:**

### **Step 1: Import Environments**
1. Open Postman
2. Click **"Import"** button
3. Select all 3 environment files:
   - `PerfBurger_Environment.postman_environment.json`
   - `PerfBurger_Development.postman_environment.json` 
   - `PerfBurger_Production.postman_environment.json`
4. Click **"Import"**

### **Step 2: Select Environment**
- In Postman, look for the **environment dropdown** (top right)
- Select **"PerfBurger - Development"** for local testing
- Select **"PerfBurger - Production"** when testing deployed API

### **Step 3: Use Variables**
All requests in your collection now use variables like:
- `{{baseUrl}}` - Automatically switches between dev/prod URLs
- `{{testUserEmail}}` - Default test user email
- `{{accessToken}}` - Auto-populated after login
- `{{sampleOrderId}}` - Sample order for testing

---

## 📋 **Environment Variables Included:**

### **🔧 Core Variables:**
- `baseUrl` - API server URL
- `accessToken` - JWT authentication token
- `contentType` - Default: application/json

### **👤 Test User Variables:**
- `testUserEmail` - Default test user email
- `testUserPassword` - Default test user password  
- `testUserFirstName` - Test user first name
- `testUserLastName` - Test user last name

### **📦 Testing Variables:**
- `sampleOrderId` - Sample order ID (PB001234)
- `sessionId` - Chat session ID
- `environment` - Current environment name
- `debugMode` - Enable/disable debug features

### **⚙️ Configuration Variables:**
- `apiVersion` - API version (v1)
- `timeout` - Request timeout (30000ms)
- `sslVerify` - SSL verification setting

---

## 💡 **Benefits of Using Environments:**

### **🔄 Easy Switching:**
- Switch between dev/prod with one click
- No need to manually change URLs in requests

### **🔐 Security:**
- Sensitive variables marked as "secret"
- Tokens auto-managed after login

### **🧪 Consistent Testing:**
- Same test data across environments
- Standardized variable names

### **⚡ Efficiency:**
- Pre-filled test data
- Automatic token management
- Environment-specific settings

---

## 🎯 **Quick Start Guide:**

1. **Import** all 3 environment files
2. **Select** "PerfBurger - Development" environment
3. **Import** the collection file
4. **Run** "Register User" (saves token automatically)
5. **Test** any chat or order endpoint

Your Postman setup is now complete and professional! 🚀🍔
