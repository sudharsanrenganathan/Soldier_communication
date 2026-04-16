# System Architecture

## Overview

The Secure Soldier-to-Soldier Communication Network uses a client-server architecture with three distinct roles running the same codebase.

---

## System Topology

```
┌─────────────────────────────────────────────────────────────┐
│                    WiFi Network (LAN)                       │
│                                                             │
│  ┌──────────────┐         ┌──────────────┐                │
│  │   Sender     │────────▶│   Receiver   │                │
│  │ (Soldier A)  │  TCP    │ (Soldier B)  │                │
│  │ Laptop A     │  5555   │ Laptop B     │                │
│  └──────────────┘         └──────────────┘                │
│         │                         ▲                         │
│         │                         │                         │
│         │    ┌──────────────┐    │                         │
│         └───▶│   Attacker   │────┘                         │
│              │  (Hacker)    │  Replay                      │
│              │  Laptop C    │  Attack                      │
│              └──────────────┘                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Sender Role                          │
├─────────────────────────────────────────────────────────────┤
│  sender.py                                                  │
│    ├─ User Input Loop                                      │
│    ├─ Message Encryption (crypto_utils)                    │
│    ├─ HMAC Generation (crypto_utils)                       │
│    ├─ Timestamp & Sequence Number                          │
│    └─ TCP Send (network_utils)                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                       Receiver Role                         │
├─────────────────────────────────────────────────────────────┤
│  receiver.py                                                │
│    ├─ TCP Server (network_utils)                           │
│    ├─ Message Reception (network_utils)                    │
│    ├─ HMAC Verification (crypto_utils)                     │
│    ├─ Timestamp Validation                                 │
│    ├─ Sequence Number Validation                           │
│    ├─ Message Decryption (crypto_utils)                    │
│    ├─ Attack Logging (logger)                              │
│    └─ Threat Level Display (logger)                        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                       Attacker Role                         │
├─────────────────────────────────────────────────────────────┤
│  attacker.py                                                │
│    ├─ Message Capture (manual entry)                       │
│    ├─ Captured Message Storage                             │
│    ├─ Message Display (encrypted)                          │
│    └─ Replay Attack (network_utils)                        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                      Shared Modules                         │
├─────────────────────────────────────────────────────────────┤
│  config.py          - Configuration & Key Generation       │
│  crypto_utils.py    - Fernet Encryption & HMAC             │
│  network_utils.py   - TCP Socket Communication             │
│  logger.py          - Attack Logging & Threat Monitoring   │
└─────────────────────────────────────────────────────────────┘
```

---

## Message Flow

### Normal Message Flow (Successful)

```
Sender                    Network                    Receiver
  │                          │                          │
  │ 1. User Input           │                          │
  │    "Hello World"        │                          │
  │                          │                          │
  │ 2. Encrypt Message      │                          │
  │    Fernet(plaintext)    │                          │
  │                          │                          │
  │ 3. Generate HMAC        │                          │
  │    HMAC(encrypted)      │                          │
  │                          │                          │
  │ 4. Add Metadata         │                          │
  │    timestamp, seq#      │                          │
  │                          │                          │
  │ 5. Send JSON ──────────▶│                          │
  │                          │                          │
  │                          │ 6. Receive JSON ───────▶│
  │                          │                          │
  │                          │    7. Verify HMAC       │
  │                          │       ✓ Valid           │
  │                          │                          │
  │                          │    8. Check Timestamp   │
  │                          │       ✓ Fresh           │
  │                          │                          │
  │                          │    9. Check Sequence#   │
  │                          │       ✓ Greater         │
  │                          │                          │
  │                          │    10. Decrypt Message  │
  │                          │        "Hello World"    │
  │                          │                          │
  │                          │    11. Display Message  │
  │                          │        ✓ SAFE (Green)   │
```

### Replay Attack Flow (Detected)

```
Sender      Attacker              Network              Receiver
  │            │                      │                    │
  │ 1. Send    │                      │                    │
  │   Message ─┼─────────────────────▶│───────────────────▶│
  │            │                      │                    │
  │            │ 2. Intercept         │                    │
  │            │    (Capture)         │                    │
  │            │    Store Message     │                    │
  │            │                      │                    │
  │            │ 3. Replay Attack     │                    │
  │            │    Send Captured ───▶│                    │
  │            │    Message           │                    │
  │            │                      │ 4. Receive ───────▶│
  │            │                      │                    │
  │            │                      │    5. Verify HMAC  │
  │            │                      │       ✓ Valid      │
  │            │                      │                    │
  │            │                      │    6. Check Time   │
  │            │                      │       ✗ Too Old    │
  │            │                      │                    │
  │            │                      │    7. Check Seq#   │
  │            │                      │       ✗ Duplicate  │
  │            │                      │                    │
  │            │                      │    8. Log Attack   │
  │            │                      │       REPLAY_ATTACK│
  │            │                      │                    │
  │            │                      │    9. Reject Msg   │
  │            │                      │       ✗ ATTACK (Red)│
```

---

## Data Flow

### Message Structure

```
┌─────────────────────────────────────────────────────────────┐
│                      JSON Message                           │
├─────────────────────────────────────────────────────────────┤
│  {                                                          │
│    "encrypted_payload": "gAAAAABl...",  ← Fernet encrypted │
│    "hmac": "a1b2c3d4e5f6...",           ← HMAC-SHA256      │
│    "timestamp": 1705329135.234,         ← Unix timestamp   │
│    "sequence_number": 42                ← Monotonic counter│
│  }                                                          │
└─────────────────────────────────────────────────────────────┘
```

### Encryption Process

```
Plaintext Message
      │
      ▼
┌─────────────┐
│   UTF-8     │  "Hello World" → bytes
│  Encoding   │
└─────────────┘
      │
      ▼
┌─────────────┐
│   Fernet    │  AES-128-CBC + HMAC-SHA256
│ Encryption  │  Key: 32 bytes (base64)
└─────────────┘
      │
      ▼
┌─────────────┐
│   Base64    │  Binary → ASCII string
│  Encoding   │
└─────────────┘
      │
      ▼
Encrypted Payload
"gAAAAABl1234abcd..."
```

### Authentication Process

```
Encrypted Payload
      │
      ▼
┌─────────────┐
│   UTF-8     │  String → bytes
│  Encoding   │
└─────────────┘
      │
      ▼
┌─────────────┐
│ HMAC-SHA256 │  Hash with secret key
│ Generation  │  Key: 32 bytes
└─────────────┘
      │
      ▼
┌─────────────┐
│     Hex     │  Binary → hex string
│  Encoding   │
└─────────────┘
      │
      ▼
HMAC Digest
"a1b2c3d4e5f6..."
```

### Validation Process

```
Received Message
      │
      ▼
┌─────────────────┐
│ Check Required  │  encrypted_payload, hmac,
│     Fields      │  timestamp, sequence_number
└─────────────────┘
      │
      ▼
┌─────────────────┐
│ Verify HMAC     │  Compare with computed HMAC
│                 │  ✓ Valid / ✗ FAKE_SENDER
└─────────────────┘
      │
      ▼
┌─────────────────┐
│ Check Timestamp │  current_time - msg_time <= 60s
│                 │  ✓ Fresh / ✗ REPLAY_ATTACK
└─────────────────┘
      │
      ▼
┌─────────────────┐
│ Check Sequence# │  msg_seq > last_seq
│                 │  ✓ Greater / ✗ REPLAY_ATTACK
└─────────────────┘
      │
      ▼
┌─────────────────┐
│ Decrypt Message │  Fernet decryption
│                 │  ✓ Success / ✗ Error
└─────────────────┘
      │
      ▼
Plaintext Message
"Hello World"
```

---

## Network Protocol

### TCP Connection Flow

```
Receiver                                    Sender
   │                                           │
   │ 1. socket()                               │
   │    Create socket                          │
   │                                           │
   │ 2. bind(0.0.0.0:5555)                    │
   │    Bind to port                           │
   │                                           │
   │ 3. listen(5)                              │
   │    Listen for connections                 │
   │                                           │
   │                                           │ 4. socket()
   │                                           │    Create socket
   │                                           │
   │                                           │ 5. connect(IP:5555)
   │ ◀─────────────────────────────────────────│    Connect to receiver
   │                                           │
   │ 6. accept()                               │
   │    Accept connection                      │
   │                                           │
   │ ◀────────────────────────────────────────▶│ 7. Connected
   │                                           │
   │ ◀────────────────────────────────────────▶│ 8. Exchange messages
   │                                           │
   │                                           │ 9. close()
   │ ◀─────────────────────────────────────────│    Close connection
   │                                           │
   │ 10. Back to accept()                      │
   │     Wait for new connection               │
```

### Message Framing

```
┌────────────────────────────────────────────────────────┐
│                    TCP Stream                          │
├────────────────────────────────────────────────────────┤
│  ┌──────────┬──────────────────────────────────────┐  │
│  │  Length  │         JSON Message                 │  │
│  │ (4 bytes)│         (Variable)                   │  │
│  └──────────┴──────────────────────────────────────┘  │
│                                                        │
│  Length: Network byte order (big-endian)              │
│  Message: UTF-8 encoded JSON                          │
└────────────────────────────────────────────────────────┘
```

---

## Security Architecture

### Key Management

```
┌─────────────────────────────────────────────────────────────┐
│                    Key Generation                           │
│                     (setup.py)                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Encryption Key          Authentication Key                │
│  ┌──────────────┐        ┌──────────────┐                 │
│  │   Fernet     │        │   secrets    │                 │
│  │ generate_key │        │ token_bytes  │                 │
│  └──────────────┘        └──────────────┘                 │
│         │                        │                         │
│         ▼                        ▼                         │
│    32 bytes                 32 bytes                       │
│   (base64)                  (raw)                          │
│         │                        │                         │
│         └────────┬───────────────┘                         │
│                  ▼                                         │
│           config.json                                      │
│                  │                                         │
│         ┌────────┼────────┐                               │
│         ▼        ▼        ▼                               │
│     Sender  Receiver  Attacker                            │
│      (✓)      (✓)       (✗)                               │
└─────────────────────────────────────────────────────────────┘
```

### Threat Detection

```
┌─────────────────────────────────────────────────────────────┐
│                   Threat Level System                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Attack Count          Threat Level         Color          │
│  ─────────────────────────────────────────────────────     │
│       0                  SAFE              Green           │
│      1-2               WARNING             Yellow          │
│      3+                ATTACK              Red             │
│                                                             │
│  Attack Types:                                             │
│  • FAKE_SENDER      - Invalid HMAC                        │
│  • REPLAY_ATTACK    - Old timestamp or duplicate seq#     │
│                                                             │
│  Attack Log Entry:                                         │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ [2025-01-15 14:32:15] REPLAY_ATTACK:               │  │
│  │ Sequence number 2 not greater than 2                │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Deployment Architecture

### Single Laptop (Testing)

```
┌─────────────────────────────────────────────────────────────┐
│                      Laptop                                 │
│                   (127.0.0.1)                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐            │
│  │ Terminal │    │ Terminal │    │ Terminal │            │
│  │    1     │    │    2     │    │    3     │            │
│  ├──────────┤    ├──────────┤    ├──────────┤            │
│  │ Receiver │    │ Attacker │    │  Sender  │            │
│  └──────────┘    └──────────┘    └──────────┘            │
│       │               │                │                   │
│       └───────────────┼────────────────┘                   │
│                       │                                    │
│                  Localhost                                 │
│                 (127.0.0.1)                                │
└─────────────────────────────────────────────────────────────┘
```

### Three Laptops (Demonstration)

```
┌─────────────────────────────────────────────────────────────┐
│                    WiFi Network                             │
│                  (192.168.1.0/24)                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐│
│  │  Laptop A    │    │  Laptop B    │    │  Laptop C    ││
│  │ 192.168.1.10 │    │192.168.1.100 │    │192.168.1.20  ││
│  ├──────────────┤    ├──────────────┤    ├──────────────┤│
│  │   Sender     │───▶│   Receiver   │◀───│  Attacker    ││
│  │ (Soldier A)  │    │ (Soldier B)  │    │  (Hacker)    ││
│  └──────────────┘    └──────────────┘    └──────────────┘│
│                                                             │
│  Same Codebase       Same Codebase       Same Codebase    │
│  Same Keys           Same Keys           NO Keys          │
└─────────────────────────────────────────────────────────────┘
```

---

## Performance Characteristics

### Latency
- **Encryption**: < 1ms (Fernet is fast)
- **HMAC Generation**: < 1ms
- **Network Transmission**: 1-10ms (LAN)
- **Validation**: < 1ms
- **Decryption**: < 1ms
- **Total Round-Trip**: 5-15ms typical

### Throughput
- **Message Size**: Typically < 1KB
- **Network Bandwidth**: Minimal (< 10 KB/s for normal use)
- **CPU Usage**: Low (< 5% per role)
- **Memory Usage**: < 50MB per role

### Scalability
- **Current**: 1 sender, 1 receiver, 1 attacker
- **Limitation**: Receiver accepts one connection at a time
- **Extension**: Could support multiple senders with threading

---

## Security Considerations

### Strengths
✅ Strong encryption (AES-128)
✅ Message authentication (HMAC-SHA256)
✅ Replay attack prevention
✅ Real-time threat monitoring
✅ Constant-time HMAC comparison

### Limitations
⚠️ Pre-shared keys (no key exchange protocol)
⚠️ No forward secrecy
⚠️ Single connection at a time
⚠️ No certificate-based authentication
⚠️ Simplified attacker simulation

### Educational Focus
This is a **demonstration project** designed for learning. Production systems would need:
- Key exchange protocol (e.g., Diffie-Hellman)
- Certificate-based authentication (e.g., X.509)
- Forward secrecy (e.g., ephemeral keys)
- More sophisticated attack detection
- Proper key rotation

---

## Extension Possibilities

### Easy Extensions
- Add more attack types (man-in-the-middle, timing attacks)
- Implement GUI interface
- Add file transfer capability
- Support multiple simultaneous connections
- Add message history/logging

### Advanced Extensions
- Implement Diffie-Hellman key exchange
- Add certificate-based authentication
- Implement forward secrecy
- Add end-to-end encryption for group chat
- Implement intrusion detection system

---

**This architecture provides a solid foundation for understanding secure communication systems!**
