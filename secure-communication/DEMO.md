# Demonstration Guide: Secure Soldier-to-Soldier Communication Network

## Overview

This guide provides a complete script for demonstrating the Secure Soldier-to-Soldier Communication Network in a college setting. Follow this script to showcase encryption, authentication, replay attack prevention, and threat monitoring.

---

## Pre-Demonstration Checklist

Before starting the demonstration, ensure:

- [ ] All 3 laptops are set up (see SETUP.md)
- [ ] All laptops are connected to the same WiFi network
- [ ] Dependencies are installed on all laptops
- [ ] Keys have been generated using `setup.py`
- [ ] `config.json` is configured with correct IP addresses
- [ ] Network connectivity has been verified (ping test)
- [ ] All terminals are visible to the audience (use projector or screen sharing)

---

## Demonstration Script

### Introduction (2 minutes)

**Presenter**: 
> "Today we're demonstrating a secure military communication system that shows how encryption, authentication, and attack detection work in real-time. We have three laptops representing:
> - **Laptop A**: Sender (Soldier A) - sends encrypted messages
> - **Laptop B**: Receiver (Soldier B) - receives and validates messages
> - **Laptop C**: Attacker (Hacker) - attempts to compromise the system
>
> All three laptops are running the same codebase but in different roles. Let's see how the system protects against attacks."

---

### Part 1: System Startup (3 minutes)

#### Step 1: Start Receiver (Laptop B)

**Action**: On Laptop B, run:
```bash
python receiver.py
```

**Expected Output**:
```
==================================================
  SECURE SOLDIER-TO-SOLDIER COMMUNICATION
  Role: RECEIVER (Soldier B)
==================================================

✓ Receiver listening on port 5555

╔══════════════════════════════════════╗
║  Threat Level: SAFE                  ║
║  Attacks Detected:  0                ║
╚══════════════════════════════════════╝

Waiting for connections...
```

**Presenter**:
> "The receiver is now listening for incoming connections. Notice the threat level is **GREEN (SAFE)** with zero attacks detected."

---

#### Step 2: Start Attacker (Laptop C)

**Action**: On Laptop C, run:
```bash
python attacker.py
```

**Expected Output**:
```
==================================================
  SECURE SOLDIER-TO-SOLDIER COMMUNICATION
  Role: ATTACKER (Hacker)
==================================================

Target: 192.168.1.100:5555
⚠ Attacker has NO encryption or authentication keys
⚠ Can only see encrypted data and replay captured messages

=== ATTACKER MENU ===
1. Capture message (manual entry)
2. View captured messages
3. Replay captured message
4. Exit

Select option:
```

**Presenter**:
> "The attacker is now active. Notice that the attacker does NOT have the encryption or authentication keys. This simulates an unauthorized party on the network who can intercept traffic but cannot decrypt it."

---

#### Step 3: Start Sender (Laptop A)

**Action**: On Laptop A, run:
```bash
python sender.py
```

**Expected Output**:
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

**Presenter**:
> "The sender has successfully connected to the receiver. The system is now ready for secure communication."

---

### Part 2: Normal Secure Communication (3 minutes)

#### Step 4: Send First Message

**Action**: On Laptop A (Sender), type:
```
Message > Mission briefing at 0800 hours
```

**Expected Output on Laptop A**:
```
✓ Message sent (seq #1): Mission briefing at 0800 hours
```

**Expected Output on Laptop B (Receiver)**:
```
Connection from 192.168.1.XXX:XXXXX

✓ Message received (seq #1): Mission briefing at 0800 hours

╔══════════════════════════════════════╗
║  Threat Level: SAFE                  ║
║  Attacks Detected:  0                ║
╚══════════════════════════════════════╝
```

**Presenter**:
> "The message was successfully encrypted by the sender, transmitted over the network, and decrypted by the receiver. The threat level remains **GREEN (SAFE)** because no attacks were detected. Let's send another message."

---

#### Step 5: Send Second Message

**Action**: On Laptop A (Sender), type:
```
Message > Rendezvous at checkpoint Alpha
```

**Expected Output on Laptop B (Receiver)**:
```
✓ Message received (seq #2): Rendezvous at checkpoint Alpha

╔══════════════════════════════════════╗
║  Threat Level: SAFE                  ║
║  Attacks Detected:  0                ║
╚══════════════════════════════════════╝
```

**Presenter**:
> "Another successful transmission. The sequence number has incremented to #2, which helps prevent replay attacks. Now let's see what happens when an attacker tries to compromise the system."

---

### Part 3: Replay Attack Demonstration (5 minutes)

#### Step 6: Capture Message (Attacker)

**Action**: On Laptop C (Attacker), select option `1` (Capture message)

**Presenter**:
> "In a real attack, the hacker would use packet sniffing tools to intercept network traffic. For this demonstration, we'll manually enter the captured message details."

**Action**: When prompted, enter the details from the last message sent:
- **Encrypted payload**: (copy from sender output or use a sample)
- **HMAC**: (copy from sender output or use a sample)
- **Timestamp**: (use the timestamp from the message, e.g., `1705329135.234`)
- **Sequence number**: `2` (the last sequence number used)

**Note**: For a simplified demo, you can use these sample values:
```
Encrypted payload: gAAAAABl1234abcd...
HMAC: a1b2c3d4e5f6...
Timestamp: 1705329135.234
Sequence number: 2
```

**Expected Output on Laptop C**:
```
✓ Message captured!
Total captured: 1
```

**Presenter**:
> "The attacker has successfully intercepted the encrypted message. However, notice that the attacker can only see the encrypted data - they cannot read the actual message content because they don't have the decryption key."

---

#### Step 7: View Captured Messages

**Action**: On Laptop C (Attacker), select option `2` (View captured messages)

**Expected Output**:
```
=== CAPTURED MESSAGES ===
[1] Seq #2 | Time: 14:32:15
    Encrypted: gAAAAABl1234abcd...
```

**Presenter**:
> "Here's the captured message. The encrypted payload is unreadable without the decryption key. Now let's see what happens when the attacker tries to replay this message."

---

#### Step 8: Replay Attack

**Action**: On Laptop C (Attacker), select option `3` (Replay captured message)

**Action**: When prompted, enter `1` to select the first captured message

**Expected Output on Laptop C**:
```
Connecting to receiver at 192.168.1.100:5555...
Replaying captured message...
✓ REPLAY ATTACK EXECUTED!
Message sent to receiver (should be detected as replay)
```

**Expected Output on Laptop B (Receiver)**:
```
✗ ATTACK DETECTED: REPLAY_ATTACK: Sequence number 2 not greater than 2

╔══════════════════════════════════════╗
║  Threat Level: ATTACK                ║
║  Attacks Detected:  1                ║
╚══════════════════════════════════════╝
```

**Presenter**:
> "**CRITICAL MOMENT**: The receiver has detected the replay attack! Notice:
> 1. The threat level changed from **GREEN (SAFE)** to **RED (ATTACK)**
> 2. The attack counter increased to 1
> 3. The system rejected the message because the sequence number (2) was not greater than the last valid sequence number (2)
>
> This demonstrates how sequence numbers prevent replay attacks. Even though the attacker captured a valid message, they cannot reuse it because the receiver tracks sequence numbers."

---

#### Step 9: Attempt Multiple Replays

**Action**: On Laptop C (Attacker), replay the same message 2 more times (repeat Step 8)

**Expected Output on Laptop B (Receiver)** (after 3rd replay):
```
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

**Presenter**:
> "After multiple replay attempts, the system has logged all attacks. The threat level remains **RED (ATTACK)** with 3 attacks detected. The attack log shows timestamps and details for each attempt. This demonstrates real-time threat monitoring."

---

### Part 4: System Recovery (2 minutes)

#### Step 10: Send New Valid Message

**Action**: On Laptop A (Sender), send a new message:
```
Message > All clear, mission complete
```

**Expected Output on Laptop B (Receiver)**:
```
✓ Message received (seq #3): All clear, mission complete

╔══════════════════════════════════════╗
║  Threat Level: ATTACK                ║
║  Attacks Detected:  3                ║
╚══════════════════════════════════════╝
```

**Presenter**:
> "The system continues to operate normally despite the attacks. Valid messages with new sequence numbers are still accepted. The threat level remains **RED** because attacks were detected, but the system is fully functional. This demonstrates resilience against attacks."

---

### Part 5: Conclusion (2 minutes)

**Presenter**:
> "Let's summarize what we've demonstrated:
>
> **1. Encryption**: All messages are encrypted using Fernet (AES-128-CBC + HMAC-SHA256). The attacker could intercept messages but couldn't read them.
>
> **2. Authentication**: HMAC authentication ensures messages come from legitimate senders. Any tampering would be detected.
>
> **3. Replay Attack Prevention**: Sequence numbers and timestamps prevent attackers from reusing captured messages. The system detected and rejected all replay attempts.
>
> **4. Threat Monitoring**: The system provides real-time threat level indicators (SAFE, WARNING, ATTACK) and maintains detailed attack logs.
>
> **5. Resilience**: Despite multiple attacks, the system continued to operate and accept valid messages.
>
> This demonstrates fundamental cybersecurity concepts in a practical, visual way. The same principles are used in real-world secure communication systems like HTTPS, VPNs, and military communications."

---

## Expected Terminal Outputs Summary

### Laptop A (Sender) - Final State:
```
Message > Mission briefing at 0800 hours
✓ Message sent (seq #1): Mission briefing at 0800 hours

Message > Rendezvous at checkpoint Alpha
✓ Message sent (seq #2): Rendezvous at checkpoint Alpha

Message > All clear, mission complete
✓ Message sent (seq #3): All clear, mission complete
```

### Laptop B (Receiver) - Final State:
```
✓ Message received (seq #1): Mission briefing at 0800 hours
✓ Message received (seq #2): Rendezvous at checkpoint Alpha
✗ ATTACK DETECTED: REPLAY_ATTACK: Sequence number 2 not greater than 2
✗ ATTACK DETECTED: REPLAY_ATTACK: Sequence number 2 not greater than 2
✗ ATTACK DETECTED: REPLAY_ATTACK: Sequence number 2 not greater than 2
✓ Message received (seq #3): All clear, mission complete

╔══════════════════════════════════════╗
║  Threat Level: ATTACK                ║
║  Attacks Detected:  3                ║
╚══════════════════════════════════════╝

=== ATTACK LOG ===
[timestamp] REPLAY_ATTACK: Sequence number 2 not greater than 2
[timestamp] REPLAY_ATTACK: Sequence number 2 not greater than 2
[timestamp] REPLAY_ATTACK: Sequence number 2 not greater than 2
```

### Laptop C (Attacker) - Final State:
```
=== CAPTURED MESSAGES ===
[1] Seq #2 | Time: 14:32:15
    Encrypted: gAAAAABl1234abcd...

✓ REPLAY ATTACK EXECUTED! (x3)
```

---

## Tips for a Successful Demonstration

1. **Practice beforehand**: Run through the entire demo at least once before presenting
2. **Use large fonts**: Increase terminal font size so the audience can read output
3. **Explain as you go**: Don't just show - explain what's happening at each step
4. **Highlight color changes**: Point out when the threat level changes from green to red
5. **Pause for questions**: Allow time for questions after each major section
6. **Have backup**: Keep a video recording of a successful demo in case of technical issues
7. **Timing**: The full demo takes about 15-20 minutes including explanations

---

## Troubleshooting During Demo

If something goes wrong during the demonstration:

- **Connection refused**: Ensure receiver is running first, check IP addresses in config.json
- **No output**: Check that all terminals are visible and not minimized
- **Wrong colors**: Some terminals may not support ANSI colors - this is cosmetic only
- **Network issues**: Have a backup plan to run all three roles on a single laptop using localhost (127.0.0.1)

---

## Q&A Preparation

Common questions and answers:

**Q: Can the attacker decrypt the messages?**
A: No, the attacker doesn't have the encryption key. They can only see encrypted data.

**Q: What if the attacker guesses the key?**
A: The keys are 256-bit (32 bytes), making brute-force attacks computationally infeasible.

**Q: How does the system know it's a replay attack?**
A: The receiver tracks sequence numbers. Any message with a sequence number less than or equal to the last valid one is rejected.

**Q: What about timestamp-based replay attacks?**
A: The system also validates timestamps. Messages older than 60 seconds are rejected.

**Q: Is this used in real systems?**
A: Yes! Similar techniques are used in HTTPS, VPNs, SSH, and military communication systems.

**Q: What if messages arrive out of order?**
A: The current implementation requires strict ordering. Production systems often use sliding windows to handle out-of-order delivery.

---

## Post-Demonstration

After the demo, you can:
- Show the source code and explain key functions
- Discuss how to extend the system (e.g., add more attack types)
- Explain the cryptographic libraries used (Fernet, HMAC)
- Discuss real-world applications and limitations
- Encourage students to modify and experiment with the code

---

**Good luck with your demonstration!**
