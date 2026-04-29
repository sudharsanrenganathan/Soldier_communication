# Quick VS Code Steps (5 Minutes)

## 🚀 **FASTEST WAY TO RUN IN VS CODE**

---

### **STEP 1: Open Project (30 seconds)**
1. **Open VS Code**
2. **File** → **Open Folder**
3. Select `Soldier_communication` folder
4. Click **Select Folder**

---

### **STEP 2: Open Terminal (10 seconds)**
1. Press `Ctrl+Shift+`` (backtick)
2. Terminal opens at bottom

---

### **STEP 3: Navigate to Project (10 seconds)**
```bash
cd secure-communication
```

---

### **STEP 4: Install Dependencies (30 seconds)**
```bash
pip install -r requirements.txt
```

---

### **STEP 5: Open 3 Terminals (20 seconds)**
1. Click **"+"** button next to terminal tab (creates Terminal 2)
2. Click **"+"** button again (creates Terminal 3)
3. You now have 3 terminals!

---

### **STEP 6: Run All 3 Components (1 minute)**

#### **Terminal 1 (Receiver) - Click on "1" tab:**
```bash
cd secure-communication
python receiver.py
```
**Wait for:** `✓ Receiver listening on port 8080`

#### **Terminal 2 (Attacker) - Click on "2" tab:**
```bash
cd secure-communication  
python attacker.py
```
**Wait for:** Menu with 4 options

#### **Terminal 3 (Sender) - Click on "3" tab:**
```bash
cd secure-communication
python sender.py
```
**Wait for:** `✓ Connected successfully!`

---

### **STEP 7: Test It! (1 minute)**

#### **Send Message:**
1. **Click Terminal 3 (Sender)**
2. Type: `Hello World!`
3. Press Enter
4. **Check Terminal 1 (Receiver)** → Should show decrypted message!

#### **Perform Attack:**
1. **Click Terminal 2 (Attacker)**
2. Type: `1` (Capture message)
3. Enter dummy data
4. Type: `3` (Replay message)
5. **Check Terminal 1 (Receiver)** → Should show RED attack detection!

---

## 🎯 **WHAT YOU'LL SEE:**

### **VS Code Layout:**
```
┌─────────────────────────────────────────────────────────┐
│ File  Edit  View  Terminal  Help                        │
├─────────────────────────────────────────────────────────┤
│ 📁 Explorer    │                                        │
│ ├─ 📁 .kiro     │         CODE EDITOR                   │
│ ├─ 📁 secure-   │     (receiver.py, sender.py,          │
│ │  communication│      attacker.py, etc.)               │
│ │  ├─ receiver.py│                                       │
│ │  ├─ sender.py │                                        │
│ │  ├─ attacker.py│                                       │
│ │  └─ config.json│                                       │
├─────────────────────────────────────────────────────────┤
│ TERMINAL 1: Receiver │ TERMINAL 2: Attacker │ TERMINAL 3: Sender │
│ ✓ Receiver listening │ === ATTACKER MENU === │ ✓ Connected!       │
│ Threat Level: SAFE   │ 1. Capture message    │ Message >          │
│                      │ 2. View messages      │                    │
│                      │ 3. Replay message     │                    │
└─────────────────────────────────────────────────────────┘
```

---

## 🎬 **DEMO FLOW:**

### **1. Normal Communication (GREEN)**
- **Terminal 3**: Type message
- **Terminal 1**: Shows decrypted message + GREEN status

### **2. Attack Simulation (RED)**
- **Terminal 2**: Capture and replay message
- **Terminal 1**: Detects attack + RED status

### **3. System Resilience**
- **Terminal 3**: Send new message
- **Terminal 1**: Still works despite attacks!

---

## 💡 **PRO TIPS:**

### **Make Terminals Bigger:**
- Drag the divider between code and terminals up

### **Rename Terminals:**
- Right-click terminal tab → **Rename**
- Name them: "Receiver", "Attacker", "Sender"

### **Increase Font Size:**
- `Ctrl+Shift+P` → "Preferences: Open Settings"
- Search "font size" → Set to 16 for demos

### **Full Screen Terminal:**
- Click **↗️** icon in terminal to maximize

---

## ✅ **SUCCESS INDICATORS:**

### **Receiver Terminal:**
```
✓ Receiver listening on port 8080
╔══════════════════════════════════════╗
║  Threat Level: SAFE                 ║
║  Attacks Detected:  0                ║
╚══════════════════════════════════════╝
```

### **Sender Terminal:**
```
✓ Connected successfully!
Enter messages to send (Ctrl+C to exit):
Message >
```

### **Attacker Terminal:**
```
=== ATTACKER MENU ===
1. Capture message (manual entry)
2. View captured messages
3. Replay captured message
4. Exit
Select option:
```

---

## 🆘 **QUICK FIXES:**

### **If Terminal Doesn't Open:**
- Press `Ctrl+Shift+`` again
- Or **Terminal** → **New Terminal**

### **If Python Not Found:**
- `Ctrl+Shift+P` → "Python: Select Interpreter"
- Choose your Python installation

### **If Connection Fails:**
- Make sure Receiver (Terminal 1) started FIRST
- Check all terminals are in `secure-communication` folder

---

**That's it! You're ready to demo in VS Code!** 🚀

**Total setup time: ~5 minutes**
**Demo time: ~10 minutes**
**Wow factor: 100%** 🔐✨