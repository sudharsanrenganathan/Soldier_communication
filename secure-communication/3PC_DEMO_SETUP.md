# 3-PC Demo Setup Guide

## 🎯 Complete Step-by-Step Guide for Multi-PC Demo

This guide will help you set up the Secure Soldier-to-Soldier Communication Network on 3 different PCs for your demonstration.

---

## 📋 **Prerequisites**

- 3 laptops/PCs (Windows, Mac, or Linux)
- All 3 PCs connected to the **SAME WiFi network**
- Python 3.8 or higher installed on all PCs
- Internet connection (for initial setup)

---

## 🔧 **STEP 1: Setup on PC 1 (Master Setup)**

### **1.1 Clone the Repository**

Open terminal/command prompt and run:

```bash
git clone https://github.com/sudharsanrenganathan/Soldier_communication.git
cd Soldier_communication/secure-communication
```

### **1.2 Install Dependencies**

```bash
pip install -r requirements.txt
```

### **1.3 Generate Encryption Keys**

```bash
python setup.py
```

**Expected Output:**
```
============================================================
  SECURE SOLDIER-TO-SOLDIER COMMUNICATION - SETUP
============================================================

Generating cryptographic keys...
✓ Keys generated and saved to config.json

============================================================
GENERATED KEYS (for reference)
============================================================

Encryption Key (Fernet):
  HkJ9hvRvrPFTRRClGPKEmoMd_TBIAzFLquGjDTP4gw8=

Authentication Key (HMAC):
  +IM45nJIlTiM6irSJIZEb12n72nmj4jaDPpaOYieuO0=
```

✅ **IMPORTANT**: This creates a `config.json` file with encryption keys. You'll copy this entire folder to other PCs.

---

## 🌐 **STEP 2: Find IP Addresses**

### **On PC 2 (Receiver - Laptop B):**

#### **Windows:**
```bash
ipconfig
```
Look for: `IPv4 Address. . . . . . . . . . . : 192.168.1.XXX`

#### **Mac/Linux:**
```bash
ifconfig
```
Look for: `inet 192.168.1.XXX`

#### **Alternative (All OS):**
```bash
python -c "import socket; print(socket.gethostbyname(socket.gethostname()))"
```

**Example Output:** `192.168.1.105`

✅ **Write down this IP address** - this is your **Receiver IP**

---

## 📁 **STEP 3: Copy Project to All PCs**

### **Option A: Using USB Drive (Recommended)**

1. On PC 1, copy the entire `Soldier_communication` folder to USB drive
2. Plug USB into PC 2, copy folder to Desktop
3. Plug USB into PC 3, copy folder to Desktop

### **Option B: Using Git Clone (Requires Internet)**

On PC 2 and PC 3:
```bash
git clone https://github.com/sudharsanrenganathan/Soldier_communication.git
cd Soldier_communication/secure-communication
pip install -r requirements.txt
```

⚠️ **IMPORTANT**: If using Git Clone, you need to copy the `config.json` file from PC 1 to PC 2 and PC 3 (it contains the encryption keys and is not in the repository for security reasons).

---

## ⚙️ **STEP 4: Configure IP Addresses**

### **On ALL 3 PCs:**

1. Navigate to the `secure-communication` folder
2. Open `config.json` in a text editor
3. Find the line: `"receiver_ip": "127.0.0.1"`
4. Replace `127.0.0.1` with the **Receiver's IP address** from Step 2

**Example:**
```json
{
  "network": {
    "receiver_ip": "192.168.1.105",  ← Change this to Receiver's IP
    "receiver_port": 5555,
    "buffer_size": 4096,
    "timeout": 30
  },
  ...
}
```

✅ **Save the file on all 3 PCs**

---

## 🔍 **STEP 5: Verify Network Connectivity**

### **Test Connection Between PCs:**

On PC 1 (Sender) and PC 3 (Attacker), test connection to PC 2 (Receiver):

#### **Windows:**
```bash
ping 192.168.1.105
```

#### **Mac/Linux:**
```bash
ping -c 4 192.168.1.105
```

**Expected Output:**
```
Reply from 192.168.1.105: bytes=32 time=2ms TTL=64
Reply from 192.168.1.105: bytes=32 time=1ms TTL=64
```

✅ If you see replies, network is working!
❌ If you see "Request timed out", check:
- All PCs are on the same WiFi network
- Firewall is not blocking connections
- IP address is correct

---

## 🚀 **STEP 6: Run the Demo**

### **PC Assignment:**
- **PC 1**: Sender (Soldier A)
- **PC 2**: Receiver (Soldier B)
- **PC 3**: Attacker (Hacker)

### **6.1 Start Receiver (PC 2) FIRST**

On PC 2:
```bash
cd Soldier_communication/secure-communication
python receiver.py
```

**Expected Output:**
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

✅ **Receiver is ready!**

---

### **6.2 Start Attacker (PC 3) SECOND**

On PC 3:
```bash
cd Soldier_communication/secure-communication
python attacker.py
```

**Expected Output:**
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

✅ **Attacker is ready!**

---

### **6.3 Start Sender (PC 1) THIRD**

On PC 1:
```bash
cd Soldier_communication/secure-communication
python sender.py
```

**Expected Output:**
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

**On PC 2 (Receiver), you should see:**
```
Connection from 192.168.1.XXX:XXXXX
```

---

## 🎬 **STEP 7: Perform the Demo**

### **Phase 1: Normal Communication**

**On PC 1 (Sender):**
```
Message > Hello from Soldier A
```

**On PC 2 (Receiver):**
```
✓ Message received (seq #1): Hello from Soldier A

╔══════════════════════════════════════╗
║  Threat Level: SAFE                 ║
║  Attacks Detected:  0                ║
╚══════════════════════════════════════╝
```

**Send another message:**
```
Message > Mission briefing at 0800 hours
```

---

### **Phase 2: Capture Message (Attacker)**

**On PC 3 (Attacker):**
1. Select option `1` (Capture message)
2. Enter the following (you can use dummy values for demo):

```
Encrypted payload: gAAAAABl1234abcdefghijklmnopqrstuvwxyz
HMAC: a1b2c3d4e5f6g7h8i9j0
Timestamp: 1705329135.234
Sequence number: 2
```

**Output:**
```
✓ Message captured!
Total captured: 1
```

---

### **Phase 3: Replay Attack**

**On PC 3 (Attacker):**
1. Select option `3` (Replay captured message)
2. Enter `1` to select the first message

**Output on PC 3:**
```
Connecting to receiver at 192.168.1.105:5555...
Replaying captured message...
✓ REPLAY ATTACK EXECUTED!
```

**Output on PC 2 (Receiver):**
```
✗ ATTACK DETECTED: REPLAY_ATTACK: Sequence number 2 not greater than 2

╔══════════════════════════════════════╗
║  Threat Level: ATTACK                ║
║  Attacks Detected:  1                ║
╚══════════════════════════════════════╝
```

🎉 **Attack detected! Threat level changed to RED!**

---

## 🔥 **Troubleshooting**

### **Problem: "Connection refused"**

**Solution:**
1. Ensure receiver (PC 2) is running FIRST
2. Check IP address in `config.json` is correct
3. Verify all PCs are on the same WiFi network
4. Check firewall settings (see below)

---

### **Problem: "No route to host"**

**Solution:**
1. Verify IP address with `ipconfig` or `ifconfig`
2. Test with `ping` command
3. Ensure all PCs are on the same network (not guest network)

---

### **Problem: Firewall Blocking Connection**

#### **Windows Firewall:**
1. Open Windows Defender Firewall
2. Click "Allow an app through firewall"
3. Click "Change settings"
4. Find "Python" and check both "Private" and "Public"
5. Click OK

#### **Mac Firewall:**
1. System Preferences → Security & Privacy → Firewall
2. Click "Firewall Options"
3. Add Python to allowed apps

#### **Linux Firewall (ufw):**
```bash
sudo ufw allow 5555/tcp
```

---

### **Problem: Port 5555 already in use**

**Solution:**
1. Change port in `config.json` on ALL 3 PCs:
```json
"receiver_port": 5556,  ← Change to different port
```
2. Restart receiver

---

### **Problem: Different WiFi Networks**

**Solution:**
- Ensure all 3 PCs are connected to the SAME WiFi network
- Check network name (SSID) on all PCs
- Avoid connecting to "Guest" networks (they often block device-to-device communication)

---

## 📊 **Quick Reference Card**

### **PC Roles:**
| PC | Role | Command | Port |
|----|------|---------|------|
| PC 1 | Sender | `python sender.py` | Connects to 5555 |
| PC 2 | Receiver | `python receiver.py` | Listens on 5555 |
| PC 3 | Attacker | `python attacker.py` | Connects to 5555 |

### **Startup Order:**
1. **PC 2 (Receiver)** - Start FIRST
2. **PC 3 (Attacker)** - Start SECOND
3. **PC 1 (Sender)** - Start THIRD

### **IP Configuration:**
- Find Receiver IP: `ipconfig` (Windows) or `ifconfig` (Mac/Linux)
- Update `config.json` on ALL PCs with Receiver's IP
- Test connectivity: `ping <receiver_ip>`

---

## 🎓 **Demo Script Summary**

1. ✅ Start Receiver (PC 2) - Shows GREEN (SAFE)
2. ✅ Start Attacker (PC 3) - Shows "NO keys" warning
3. ✅ Start Sender (PC 1) - Connects to receiver
4. 📤 Send message from Sender - Receiver decrypts and shows GREEN
5. 🎯 Capture message on Attacker - Shows encrypted data (unreadable)
6. ⚠️ Replay attack from Attacker - Receiver detects and shows RED (ATTACK)
7. 📊 View attack log on Receiver - Shows all detected attacks

---

## 💡 **Tips for Successful Demo**

1. **Practice beforehand** - Run through the entire demo once before presenting
2. **Use large fonts** - Increase terminal font size for audience visibility
3. **Label PCs clearly** - Put signs: "Sender", "Receiver", "Attacker"
4. **Prepare backup** - Have video recording in case of technical issues
5. **Test network** - Verify connectivity 30 minutes before demo
6. **Have hotspot ready** - Use phone hotspot if WiFi fails
7. **Print this guide** - Keep physical copy during demo

---

## 🆘 **Emergency Backup: Single PC Demo**

If multi-PC setup fails, you can run all 3 roles on ONE PC:

1. Keep `receiver_ip` as `127.0.0.1` in `config.json`
2. Open 3 separate terminals
3. Run each role in different terminal:
   - Terminal 1: `python receiver.py`
   - Terminal 2: `python attacker.py`
   - Terminal 3: `python sender.py`

---

## 📞 **Support Checklist**

Before demo, verify:
- [ ] All 3 PCs have Python installed
- [ ] All 3 PCs have dependencies installed (`pip install -r requirements.txt`)
- [ ] All 3 PCs have same `config.json` with correct Receiver IP
- [ ] All 3 PCs are on same WiFi network
- [ ] Firewall allows Python connections
- [ ] Port 5555 is not blocked
- [ ] Network connectivity tested with `ping`
- [ ] Demo script practiced at least once

---

**Good luck with your demonstration! 🚀**

For questions or issues, refer to TROUBLESHOOTING.md or README.md
