# Setup Instructions for Secure Soldier-to-Soldier Communication Network

## Overview

This guide provides step-by-step instructions for setting up the Secure Soldier-to-Soldier Communication Network on 3 laptops for a live demonstration.

## Requirements

- **3 Laptops** (Windows, macOS, or Linux)
- **Same WiFi Network** - All laptops must be connected to the same WiFi
- **Python 3.8+** installed on all laptops
- **pip** (Python package manager)

## Laptop Roles

- **Laptop A**: Sender (Soldier A)
- **Laptop B**: Receiver (Soldier B)
- **Laptop C**: Attacker (Hacker)

---

## Step 1: Install Python Dependencies

On **ALL 3 laptops**, navigate to the `secure-communication` directory and install dependencies:

```bash
cd secure-communication
pip install -r requirements.txt
```

This will install:
- `cryptography` - For Fernet encryption and HMAC
- `hypothesis` - For property-based testing (optional)
- `pytest` - For running tests (optional)

---

## Step 2: Generate Cryptographic Keys

On **ONE laptop** (any of the 3), run the setup script to generate encryption and authentication keys:

```bash
python setup.py
```

This will:
- Generate a Fernet encryption key
- Generate an HMAC authentication key
- Save both keys to `config.json`
- Display the keys for reference

**IMPORTANT**: The keys are now stored in `config.json`. You'll copy this entire folder to all laptops in the next step.

---

## Step 3: Find IP Addresses

You need to find the IP address of **Laptop B (Receiver)**.

### On Windows:
```cmd
ipconfig
```
Look for "IPv4 Address" under your WiFi adapter (e.g., `192.168.1.100`)

### On macOS/Linux:
```bash
ifconfig
```
or
```bash
ip addr show
```
Look for the IP address of your WiFi interface (e.g., `192.168.1.100`)

**Write down Laptop B's IP address** - you'll need it for configuration.

---

## Step 4: Configure Network Settings

Edit `config.json` on **ALL 3 laptops** and update the `receiver_ip` field:

```json
{
  "network": {
    "receiver_ip": "192.168.1.100",  ← Change this to Laptop B's IP address
    "receiver_port": 5555,
    "buffer_size": 4096,
    "timeout": 30
  },
  ...
}
```

### Configuration for Each Laptop:

- **Laptop A (Sender)**: Set `receiver_ip` to Laptop B's IP address
- **Laptop B (Receiver)**: Set `receiver_ip` to its own IP address (or leave as is)
- **Laptop C (Attacker)**: Set `receiver_ip` to Laptop B's IP address

**Note**: The `receiver_port` (5555) can be changed if needed, but must be the same on all laptops.

---

## Step 5: Copy Files to All Laptops

Copy the **entire `secure-communication` folder** to all 3 laptops. This ensures:
- All laptops have the same codebase
- All laptops have the same encryption/authentication keys
- Configuration is consistent

You can use:
- USB drive
- Cloud storage (Google Drive, Dropbox)
- Network file sharing
- Email (zip the folder)

---

## Step 6: Verify Network Connectivity

Before running the demonstration, verify that all laptops can communicate:

### On Laptop B (Receiver):
Find your IP address (from Step 3)

### On Laptops A and C:
Ping Laptop B to verify connectivity:

```bash
ping 192.168.1.100
```
(Replace with Laptop B's actual IP address)

You should see replies. If not:
- Verify all laptops are on the same WiFi network
- Check firewall settings (may need to allow Python or port 5555)
- Try a different port in `config.json`

---

## Step 7: Run the Demonstration

Start the applications in this order:

### 1. On Laptop B (Receiver):
```bash
python receiver.py
```

You should see:
```
==================================================
  SECURE SOLDIER-TO-SOLDIER COMMUNICATION
  Role: RECEIVER (Soldier B)
==================================================

✓ Receiver listening on port 5555
Waiting for connections...
```

### 2. On Laptop C (Attacker):
```bash
python attacker.py
```

You should see the attacker menu:
```
==================================================
  SECURE SOLDIER-TO-SOLDIER COMMUNICATION
  Role: ATTACKER (Hacker)
==================================================

=== ATTACKER MENU ===
1. Capture message (manual entry)
2. View captured messages
3. Replay captured message
4. Exit
```

### 3. On Laptop A (Sender):
```bash
python sender.py
```

You should see:
```
==================================================
  SECURE SOLDIER-TO-SOLDIER COMMUNICATION
  Role: SENDER (Soldier A)
==================================================

Connecting to receiver at 192.168.1.100:5555...
✓ Connected successfully!

Enter messages to send (Ctrl+C to exit):

Message >
```

---

## Step 8: Test Normal Communication

On **Laptop A (Sender)**, type a message and press Enter:

```
Message > Hello from Soldier A
```

On **Laptop B (Receiver)**, you should see:
```
✓ Message received (seq #1): Hello from Soldier A

╔══════════════════════════════════════╗
║  Threat Level: SAFE                  ║
║  Attacks Detected:  0                ║
╚══════════════════════════════════════╝
```

The threat level should be **GREEN (SAFE)**.

---

## Step 9: Perform Replay Attack

### On Laptop C (Attacker):

1. Select option `1` to capture a message
2. You'll need to manually enter the message details. To get these:
   - On Laptop A, send another message
   - The encrypted payload, HMAC, timestamp, and sequence number are in the message
   - For demo purposes, you can use dummy values or copy from network logs

3. After capturing, select option `3` to replay the message
4. Select the message number to replay

### On Laptop B (Receiver):

You should see:
```
✗ ATTACK DETECTED: REPLAY_ATTACK: Sequence number 1 not greater than 1

╔══════════════════════════════════════╗
║  Threat Level: ATTACK                ║
║  Attacks Detected:  1                ║
╚══════════════════════════════════════╝
```

The threat level should change to **RED (ATTACK)**.

---

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues and solutions.

---

## Summary

You now have a working demonstration of:
- ✓ Encrypted communication between Sender and Receiver
- ✓ Authentication using HMAC
- ✓ Replay attack detection
- ✓ Threat level monitoring
- ✓ Attack logging

The system demonstrates fundamental cybersecurity concepts in a beginner-friendly way!
