# Network Setup Diagram

## 🌐 Visual Guide for 3-PC Demo Setup

---

## **Network Topology**

```
                    SAME WiFi NETWORK
    ┌─────────────────────────────────────────────┐
    │                                             │
    │   ┌─────────────┐      ┌─────────────┐    │
    │   │   PC 1      │      │   PC 2      │    │
    │   │  (Sender)   │─────▶│ (Receiver)  │    │
    │   │ Soldier A   │      │  Soldier B  │    │
    │   └─────────────┘      └─────────────┘    │
    │         │                      ▲           │
    │         │                      │           │
    │         │    ┌─────────────┐   │           │
    │         └───▶│   PC 3      │───┘           │
    │              │ (Attacker)  │               │
    │              │   Hacker    │               │
    │              └─────────────┘               │
    │                                             │
    └─────────────────────────────────────────────┘
```

---

## **IP Address Configuration**

### **Example Setup:**

```
WiFi Network: "MyHomeWiFi" (192.168.1.x)

┌─────────────────────────────────────────────────┐
│ PC 1 (Sender)                                   │
│ IP: 192.168.1.100                               │
│ Role: Sends encrypted messages                  │
│ Config: receiver_ip = "192.168.1.105"           │
└─────────────────────────────────────────────────┘
                    │
                    │ Encrypted Message
                    ▼
┌─────────────────────────────────────────────────┐
│ PC 2 (Receiver)                                 │
│ IP: 192.168.1.105  ← THIS IS THE KEY IP!       │
│ Role: Receives and validates messages           │
│ Config: receiver_ip = "192.168.1.105"           │
│ Listens on: Port 5555                           │
└─────────────────────────────────────────────────┘
                    ▲
                    │ Replay Attack
                    │
┌─────────────────────────────────────────────────┐
│ PC 3 (Attacker)                                 │
│ IP: 192.168.1.110                               │
│ Role: Intercepts and replays messages           │
│ Config: receiver_ip = "192.168.1.105"           │
└─────────────────────────────────────────────────┘
```

---

## **Configuration File Setup**

### **On ALL 3 PCs, config.json should have:**

```json
{
  "network": {
    "receiver_ip": "192.168.1.105",  ← PC 2's IP address
    "receiver_port": 5555,
    "buffer_size": 4096,
    "timeout": 30
  },
  "security": {
    "encryption_key": "HkJ9hvRvrPFTRRClGPKEmoMd_TBIAzFLquGjDTP4gw8=",
    "auth_key": "+IM45nJIlTiM6irSJIZEb12n72nmj4jaDPpaOYieuO0=",
    "timestamp_window": 60,
    "replay_window": 300
  }
}
```

⚠️ **CRITICAL**: All 3 PCs must have:
1. **Same encryption keys** (copy config.json from PC 1)
2. **Same receiver_ip** (PC 2's IP address)
3. **Same receiver_port** (5555)

---

## **Message Flow Diagram**

### **Normal Communication:**

```
PC 1 (Sender)                    PC 2 (Receiver)
─────────────                    ───────────────

1. User types:
   "Hello World"
        │
        ▼
2. Encrypt message
   (AES-128-CBC)
        │
        ▼
3. Generate HMAC
   (SHA-256)
        │
        ▼
4. Add timestamp
   & sequence #
        │
        ▼
5. Send over TCP ──────────────▶ 6. Receive message
   Port 5555                         │
                                     ▼
                                7. Verify HMAC
                                   (Authentic?)
                                     │
                                     ▼
                                8. Check timestamp
                                   (Fresh?)
                                     │
                                     ▼
                                9. Check sequence
                                   (Not replay?)
                                     │
                                     ▼
                               10. Decrypt message
                                     │
                                     ▼
                               11. Display:
                                   "Hello World"
                                   Status: SAFE ✓
```

---

### **Replay Attack Flow:**

```
PC 3 (Attacker)                  PC 2 (Receiver)
───────────────                  ───────────────

1. Capture message
   (from network)
        │
        ▼
2. Store:
   - Encrypted payload
   - HMAC
   - Timestamp
   - Sequence #2
        │
        ▼
3. Wait...
        │
        ▼
4. Replay message ──────────────▶ 5. Receive message
   (Send again)                       │
                                      ▼
                                 6. Verify HMAC
                                    ✓ Valid
                                      │
                                      ▼
                                 7. Check timestamp
                                    ✓ Fresh
                                      │
                                      ▼
                                 8. Check sequence
                                    ✗ Seq #2 already used!
                                      │
                                      ▼
                                 9. REJECT MESSAGE
                                    Log: REPLAY_ATTACK
                                      │
                                      ▼
                                10. Display:
                                    Status: ATTACK ✗
                                    Threat: RED
```

---

## **Port and Protocol Details**

```
┌─────────────────────────────────────────────────┐
│ Protocol: TCP                                   │
│ Port: 5555                                      │
│ Direction: Client → Server                      │
│                                                 │
│ Sender (Client)  ──────────▶  Receiver (Server) │
│ Attacker (Client) ─────────▶  Receiver (Server) │
│                                                 │
│ Message Format: JSON                            │
│ Encoding: UTF-8                                 │
│ Encryption: Fernet (AES-128-CBC + HMAC-SHA256)  │
└─────────────────────────────────────────────────┘
```

---

## **Firewall Configuration**

### **PC 2 (Receiver) MUST allow incoming connections:**

```
┌─────────────────────────────────────────────────┐
│ Windows Firewall:                               │
│ - Allow Python.exe                              │
│ - Allow incoming on port 5555                   │
│                                                 │
│ Mac Firewall:                                   │
│ - Add Python to allowed apps                    │
│                                                 │
│ Linux (ufw):                                    │
│ - sudo ufw allow 5555/tcp                       │
└─────────────────────────────────────────────────┘
```

---

## **Step-by-Step Connection Process**

```
Step 1: Find Receiver IP
┌─────────────────────────────────────────────────┐
│ On PC 2 (Receiver):                             │
│                                                 │
│ Windows: ipconfig                               │
│ Mac/Linux: ifconfig                             │
│                                                 │
│ Look for: IPv4 Address: 192.168.1.105          │
│                          ^^^^^^^^^^^^^^^^       │
│                          This is the IP!        │
└─────────────────────────────────────────────────┘

Step 2: Update config.json on ALL PCs
┌─────────────────────────────────────────────────┐
│ Edit config.json:                               │
│                                                 │
│ "receiver_ip": "192.168.1.105"  ← Change this   │
│                                                 │
│ Save on PC 1, PC 2, and PC 3                    │
└─────────────────────────────────────────────────┘

Step 3: Test Connectivity
┌─────────────────────────────────────────────────┐
│ On PC 1 and PC 3:                               │
│                                                 │
│ ping 192.168.1.105                              │
│                                                 │
│ Should see: Reply from 192.168.1.105            │
└─────────────────────────────────────────────────┘

Step 4: Start Programs in Order
┌─────────────────────────────────────────────────┐
│ 1st: PC 2 → python receiver.py                  │
│      (Must start first - it's the server!)      │
│                                                 │
│ 2nd: PC 3 → python attacker.py                  │
│      (Can start anytime)                        │
│                                                 │
│ 3rd: PC 1 → python sender.py                    │
│      (Connects to receiver)                     │
└─────────────────────────────────────────────────┘
```

---

## **Common Network Issues**

### **Issue 1: Different Subnets**

```
❌ WRONG:
PC 1: 192.168.1.100  ← Subnet: 192.168.1.x
PC 2: 192.168.0.105  ← Subnet: 192.168.0.x (Different!)
PC 3: 192.168.1.110  ← Subnet: 192.168.1.x

✓ CORRECT:
PC 1: 192.168.1.100  ← All same subnet
PC 2: 192.168.1.105  ← All same subnet
PC 3: 192.168.1.110  ← All same subnet
```

### **Issue 2: Guest Network Isolation**

```
❌ WRONG:
PC 1: Connected to "MyWiFi"
PC 2: Connected to "MyWiFi-Guest"  ← Guest networks block device communication
PC 3: Connected to "MyWiFi"

✓ CORRECT:
PC 1: Connected to "MyWiFi"
PC 2: Connected to "MyWiFi"  ← All on same network
PC 3: Connected to "MyWiFi"
```

---

## **Quick Troubleshooting Flowchart**

```
Connection Failed?
       │
       ▼
   Can ping?
       │
   ┌───┴───┐
   │       │
  YES     NO
   │       │
   │       └──▶ Check WiFi network
   │            Same network?
   │            Not guest network?
   │
   ▼
Firewall blocking?
   │
   └──▶ Allow Python
        Allow port 5555
        
Still failing?
   │
   └──▶ Check config.json
        Correct receiver_ip?
        Same keys on all PCs?
```

---

## **Demo Day Checklist**

```
□ All 3 PCs on same WiFi network
□ Receiver IP address identified (ipconfig/ifconfig)
□ config.json updated on all 3 PCs with correct receiver_ip
□ Dependencies installed on all PCs (pip install -r requirements.txt)
□ Same config.json (with keys) copied to all PCs
□ Firewall configured to allow connections
□ Network connectivity tested (ping successful)
□ Practice run completed successfully
□ Backup plan ready (single PC demo or video)
```

---

**Ready for your demo! 🚀**
