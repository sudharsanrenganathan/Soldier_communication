# Complete 3-PC Demo Guide

## 🎯 **SIMPLE STEP-BY-STEP GUIDE FOR 3 LAPTOPS**

This guide will help you run the Secure Soldier-to-Soldier Communication Network on 3 different PCs.

---

## 📋 **What You Need:**

- ✅ 3 Laptops/PCs (Windows, Mac, or Linux)
- ✅ All 3 PCs on the **SAME WiFi network**
- ✅ Python 3.8+ installed on all PCs
- ✅ 15 minutes of setup time

---

## 🖥️ **PC ROLES:**

| PC | Role | What It Does |
|----|------|--------------|
| **PC 1** | **RECEIVER** (Soldier B) | Receives and decrypts messages, detects attacks |
| **PC 2** | **SENDER** (Soldier A) | Encrypts and sends messages |
| **PC 3** | **ATTACKER** (Hacker) | Intercepts and replays messages (gets detected!) |

---

## 🚀 **SETUP PROCESS**

---

### **PART 1: Setup on ONE PC First (PC 1)**

#### **Step 1.1: Clone the Project**

Open terminal and run:

```bash
git clone https://github.com/sudharsanrenganathan/Soldier_communication.git
cd Soldier_communication/secure-communication
```

#### **Step 1.2: Install Dependencies**

```bash
pip install -r requirements.txt
```

#### **Step 1.3: Generate Encryption Keys**

```bash
python setup.py
```

**You'll see:**
```
============================================================
  SECURE SOLDIER-TO-SOLDIER COMMUNICATION - SETUP
============================================================

Generating cryptographic keys...
✓ Keys generated and saved to config.json

Encryption Key (Fernet):
  HkJ9hvRvrPFTRRClGPKEmoMd_TBIAzFLquGjDTP4gw8=

Authentication Key (HMAC):
  +IM45nJIlTiM6irSJIZEb12n72nmj4jaDPpaOYieuO0=
```

✅ **Keys are now saved in `config.json`**

---

### **PART 2: Find the Receiver's IP Address**

#### **Step 2.1: On PC 1 (Receiver), Find IP Address**

**Windows:**
```bash
ipconfig
```
Look for: `IPv4 Address. . . . . . . . . . . : 192.168.1.XXX`

**Mac/Linux:**
```bash
ifconfig
```
Look for: `inet 192.168.1.XXX`

**Example:** `192.168.1.105`

📝 **Write this IP address down!** This is your **Receiver IP**.

---

### **PART 3: Copy Project to All 3 PCs**

#### **Option A: Using USB Drive (Easiest)**

1. Copy the entire `Soldier_communication` folder to USB drive
2. Plug USB into PC 2, copy folder to Desktop
3. Plug USB into PC 3, copy folder to Desktop

#### **Option B: Using Git Clone (Requires copying config.json)**

On PC 2 and PC 3:
```bash
git clone https://github.com/sudharsanrenganathan/Soldier_communication.git
cd Soldier_communication/secure-communication
pip install -r requirements.txt
```

**IMPORTANT:** Copy the `config.json` file from PC 1 to PC 2 and PC 3 (it contains the encryption keys).

---

### **PART 4: Update config.json on ALL 3 PCs**

#### **Step 4.1: Open config.json**

On **ALL 3 PCs**, open `config.json` in a text editor.

#### **Step 4.2: Update receiver_ip**

Find this line:
```json
"receiver_ip": "127.0.0.1",
```

Change it to the Receiver's IP from Step 2.1:
```json
"receiver_ip": "192.168.1.105",
```
(Replace `192.168.1.105` with your actual Receiver IP)

#### **Step 4.3: Save the file**

Save `config.json` on **ALL 3 PCs**.

---

### **PART 5: Test Network Connection**

#### **Step 5.1: On PC 2 and PC 3, Test Connection**

```bash
ping 192.168.1.105
```
(Replace with your Receiver IP)

**You should see:**
```
Reply from 192.168.1.105: bytes=32 time=2ms TTL=64
Reply from 192.168.1.105: bytes=32 time=1ms TTL=64
```

✅ If you see replies → **Network is working!**
❌ If you see "Request timed out" → Check:
- All PCs on same WiFi?
- Correct IP address?
- Firewall blocking?

---

## 🎬 **RUNNING THE DEMO**

---

### **STEP 1: Start RECEIVER (PC 1) FIRST**

**On PC 1:**

```bash
cd Soldier_communication/secure-communication
python receiver.py
```

**You should see:**
```
==================================================
  SECURE SOLDIER-TO-SOLDIER COMMUNICATION
  Role: RECEIVER (Soldier B)
==================================================

Starting receiver on port 5555...
✓ Receiver listening on port 5555

╔══════════════════════════════════════╗
║  Threat Level: SAFE                 ║
║  Attacks Detected:  0                ║
╚══════════════════════════════════════╝

Waiting for connections...
```

✅ **Receiver is ready!** Leave this terminal open.

---

### **STEP 2: Start ATTACKER (PC 3) SECOND**

**On PC 3:**

```bash
cd Soldier_communication/secure-communication
python attacker.py
```

**You should see:**
```
==================================================
  SECURE SOLDIER-TO-SOLDIER COMMUNICATION
  Role: ATTACKER (Hacker)
==================================================

Target: 192.168.1.105:5555
⚠ Attacker has NO encryption or authentication keys
⚠ Can only see encrypted data and replay captured messages

=== ATTACKER MENU ===
1. Capture message (manual entry)
2. View captured messages
3. Replay captured message
4. Exit

Select option:
```

✅ **Attacker is ready!** Leave this terminal open.

---

### **STEP 3: Start SENDER (PC 2) THIRD**

**On PC 2:**

```bash
cd Soldier_communication/secure-communication
python sender.py
```

**You should see:**
```
==================================================
  SECURE SOLDIER-TO-SOLDIER COMMUNICATION
  Role: SENDER (Soldier A)
==================================================

Connecting to receiver at 192.168.1.105:5555...
✓ Connected successfully!

Enter messages to send (Ctrl+C to exit):

Message >
```

✅ **Sender is connected!**

**On PC 1 (Receiver), you should also see:**
```
Connection from 192.168.X.X:XXXXX
```

---

## 📤 **DEMO SCRIPT**

---

### **PHASE 1: Normal Secure Communication**

#### **On PC 2 (Sender):**

Type and press Enter:
```
Message > Mission briefing at 0800 hours
```

#### **On PC 1 (Receiver):**

You should see:
```
✓ Message received (seq #1): Mission briefing at 0800 hours

╔══════════════════════════════════════╗
║  Threat Level: SAFE                 ║
║  Attacks Detected:  0                ║
╚══════════════════════════════════════╝
```

✅ **Message encrypted, transmitted, and decrypted successfully!**

#### **Send another message:**

**On PC 2 (Sender):**
```
Message > Rendezvous at checkpoint Alpha
```

**On PC 1 (Receiver):**
```
✓ Message received (seq #2): Rendezvous at checkpoint Alpha
Threat Level: SAFE
```

---

### **PHASE 2: Capture Message (Attacker)**

#### **On PC 3 (Attacker):**

1. Select option `1` (Capture message)
2. Enter these values (you can use dummy values for demo):

```
Encrypted payload: gAAAAABl1234abcdefghijklmnopqrstuvwxyz
HMAC: a1b2c3d4e5f6g7h8i9j0
Timestamp: 1705329135.234
Sequence number: 2
```

**You'll see:**
```
✓ Message captured!
Total captured: 1
```

---

### **PHASE 3: View Captured Messages**

#### **On PC 3 (Attacker):**

Select option `2` (View captured messages)

**You'll see:**
```
=== CAPTURED MESSAGES ===
[1] Seq #2 | Time: 14:32:15
    Encrypted: gAAAAABl1234abcdefghijklmnopqrstuvwxyz...
```

**👉 Point out to audience:** "See? The attacker can only see encrypted gibberish! They cannot read the actual message because they don't have the decryption key."

---

### **PHASE 4: Replay Attack**

#### **On PC 3 (Attacker):**

1. Select option `3` (Replay captured message)
2. Enter `1` to select the first message

**You'll see:**
```
Connecting to receiver at 192.168.1.105:5555...
Replaying captured message...
✓ REPLAY ATTACK EXECUTED!
Message sent to receiver (should be detected as replay)
```

#### **On PC 1 (Receiver):**

**🚨 ATTACK DETECTED! 🚨**

```
✗ ATTACK DETECTED: REPLAY_ATTACK: Sequence number 2 not greater than 2

╔══════════════════════════════════════╗
║  Threat Level: ATTACK                ║
║  Attacks Detected:  1                ║
╚══════════════════════════════════════╝
```

**👉 Point out to audience:** "The receiver detected the replay attack! The threat level changed from GREEN (SAFE) to RED (ATTACK). The system rejected the message because the sequence number was already used."

---

### **PHASE 5: Multiple Replay Attempts**

#### **On PC 3 (Attacker):**

Repeat the replay attack 2 more times (Option 3, select message 1)

#### **On PC 1 (Receiver):**

After 3 attacks:
```
✗ ATTACK DETECTED: REPLAY_ATTACK: Sequence number 2 not greater than 2
✗ ATTACK DETECTED: REPLAY_ATTACK: Sequence number 2 not greater than 2
✗ ATTACK DETECTED: REPLAY_ATTACK: Sequence number 2 not greater than 2

╔══════════════════════════════════════╗
║  Threat Level: ATTACK                ║
║  Attacks Detected:  3                ║
╚══════════════════════════════════════╝

=== ATTACK LOG ===
[2025-01-15 14:35:10] REPLAY_ATTACK: Sequence number 2 not greater than 2
[2025-01-15 14:35:15] REPLAY_ATTACK: Sequence number 2 not greater than 2
[2025-01-15 14:35:20] REPLAY_ATTACK: Sequence number 2 not greater than 2
```

**👉 Point out to audience:** "All 3 replay attempts were detected and logged. The system maintains a complete audit trail of all attacks."

---

### **PHASE 6: System Recovery**

#### **On PC 2 (Sender):**

Send a new message:
```
Message > All clear, mission complete
```

#### **On PC 1 (Receiver):**

```
✓ Message received (seq #3): All clear, mission complete

╔══════════════════════════════════════╗
║  Threat Level: ATTACK                ║
║  Attacks Detected:  3                ║
╚══════════════════════════════════════╝
```

**👉 Point out to audience:** "Despite the attacks, the system continues to operate normally. Valid messages with new sequence numbers are still accepted. The threat level remains RED as a warning, but the system is fully functional."

---

## 🎓 **WHAT TO TELL YOUR AUDIENCE**

### **Security Features Demonstrated:**

1. **🔐 Military-Grade Encryption (AES-256-GCM)**
   - Same encryption used by U.S. Military for TOP SECRET data
   - 256-bit keys = 2^256 possible combinations
   - Would take longer than the age of the universe to brute-force

2. **✅ Authentication**
   - Built-in authentication with AES-GCM
   - HMAC-SHA256 for message verification
   - Prevents message forgery

3. **🛡️ Replay Attack Prevention**
   - Sequence numbers prevent message reuse
   - Timestamps reject old messages (>60 seconds)
   - All replay attempts detected and logged

4. **🚨 Real-Time Threat Monitoring**
   - Dynamic threat levels (SAFE/WARNING/ATTACK)
   - Complete attack audit trail
   - Color-coded visual indicators

5. **💪 System Resilience**
   - Continues operating despite attacks
   - Accepts valid messages
   - Maintains security posture

---

## 🆘 **TROUBLESHOOTING**

### **Problem: "Connection refused"**

**Solution:**
1. Make sure Receiver (PC 1) is running FIRST
2. Check IP address in config.json is correct
3. Test with `ping` command
4. Check firewall settings

### **Problem: "No route to host"**

**Solution:**
1. Verify all PCs on same WiFi network
2. Check IP address with `ipconfig` or `ifconfig`
3. Ensure not on guest network

### **Problem: Firewall Blocking**

**Windows:**
1. Open Windows Defender Firewall
2. Click "Allow an app through firewall"
3. Find Python and check both Private and Public
4. Click OK

**Mac:**
1. System Preferences → Security & Privacy → Firewall
2. Click "Firewall Options"
3. Add Python to allowed apps

**Linux:**
```bash
sudo ufw allow 5555/tcp
```

---

## 📊 **DEMO CHECKLIST**

### **Before Demo:**
- [ ] All 3 PCs have project folder
- [ ] All 3 PCs have same config.json (with keys)
- [ ] All 3 PCs have correct receiver_ip in config.json
- [ ] All 3 PCs on same WiFi network
- [ ] Ping test successful from PC 2 and PC 3 to PC 1
- [ ] Dependencies installed on all PCs
- [ ] Firewall configured to allow connections
- [ ] Practice run completed successfully

### **During Demo:**
- [ ] Start Receiver (PC 1) FIRST
- [ ] Start Attacker (PC 3) SECOND
- [ ] Start Sender (PC 2) THIRD
- [ ] Send normal messages (show GREEN status)
- [ ] Capture message on Attacker (show encrypted data)
- [ ] Replay attack (show RED status and detection)
- [ ] Send new message (show system still works)

---

## 🎯 **STARTUP ORDER (CRITICAL!)**

```
1st: PC 1 (Receiver) → python receiver.py
     ↓
     Wait for "Receiver listening on port 5555"
     ↓
2nd: PC 3 (Attacker) → python attacker.py
     ↓
     Wait for menu to appear
     ↓
3rd: PC 2 (Sender) → python sender.py
     ↓
     Wait for "Connected successfully!"
     ↓
READY FOR DEMO!
```

---

## 📝 **QUICK REFERENCE**

### **Commands:**

| PC | Command | Purpose |
|----|---------|---------|
| PC 1 | `python receiver.py` | Start receiver |
| PC 2 | `python sender.py` | Start sender |
| PC 3 | `python attacker.py` | Start attacker |

### **Config:**

| Setting | Value | Notes |
|---------|-------|-------|
| `receiver_ip` | PC 1's IP | Same on all 3 PCs |
| `receiver_port` | 5555 | Default port |
| `encryption_key` | Generated | Same on all 3 PCs |
| `auth_key` | Generated | Same on all 3 PCs |

---

## 🎉 **SUCCESS INDICATORS**

✅ **Receiver:** Shows "Receiver listening on port 5555" and GREEN status
✅ **Sender:** Shows "Connected successfully!" and accepts input
✅ **Attacker:** Shows menu with 4 options
✅ **Communication:** Messages appear on receiver with GREEN status
✅ **Attack Detection:** Replay attacks show RED status and are logged

---

**Your 3-PC demo is ready! Good luck! 🚀**

For more details, see:
- `README.md` - Complete documentation
- `SECURITY_UPGRADE.md` - Security features
- `TROUBLESHOOTING.md` - Common issues
