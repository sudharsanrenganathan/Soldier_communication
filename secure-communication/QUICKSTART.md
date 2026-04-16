# Quick Start Guide

## For Impatient Users 🚀

Want to see it work RIGHT NOW? Here's the fastest way:

### Single Laptop Test (5 minutes)

1. **Install dependencies**:
   ```bash
   pip install cryptography
   ```

2. **Generate keys**:
   ```bash
   python setup.py
   ```

3. **Edit config.json** - Change `receiver_ip` to `127.0.0.1`

4. **Open 3 terminals** and run:
   - Terminal 1: `python receiver.py`
   - Terminal 2: `python attacker.py`
   - Terminal 3: `python sender.py`

5. **Send a message** in Terminal 3 (sender):
   ```
   Message > Hello World
   ```

6. **See it work** in Terminal 1 (receiver):
   ```
   ✓ Message received (seq #1): Hello World
   Threat Level: SAFE (green)
   ```

7. **Perform replay attack** in Terminal 2 (attacker):
   - Select option 1 (Capture message)
   - Enter dummy values or copy from sender
   - Select option 3 (Replay message)
   - Select message 1

8. **See attack detected** in Terminal 1 (receiver):
   ```
   ✗ ATTACK DETECTED: REPLAY_ATTACK
   Threat Level: ATTACK (red)
   ```

**Done!** You've just demonstrated encryption, authentication, and replay attack prevention.

---

### 3 Laptop Demo (15 minutes)

1. **On ONE laptop**, run:
   ```bash
   pip install cryptography
   python setup.py
   ```

2. **Copy entire folder** to all 3 laptops (USB, cloud, etc.)

3. **Find Laptop B's IP**:
   - Windows: `ipconfig`
   - Mac/Linux: `ifconfig`
   - Look for something like `192.168.1.100`

4. **Edit config.json** on ALL laptops:
   - Change `receiver_ip` to Laptop B's IP

5. **Run in order**:
   - Laptop B: `python receiver.py`
   - Laptop C: `python attacker.py`
   - Laptop A: `python sender.py`

6. **Follow the demo** in [DEMO.md](DEMO.md)

---

## What You'll See

### Sender (Green text):
```
✓ Message sent (seq #1): Hello World
```

### Receiver (Green → Red):
```
✓ Message received (seq #1): Hello World
Threat Level: SAFE

✗ ATTACK DETECTED: REPLAY_ATTACK
Threat Level: ATTACK
```

### Attacker (Magenta text):
```
✓ Message captured!
✓ REPLAY ATTACK EXECUTED!
```

---

## Troubleshooting

- **Connection refused**: Start receiver first
- **Module not found**: Run `pip install cryptography`
- **Port in use**: Change port in config.json
- **No colors**: Use Windows Terminal or PowerShell

For more help, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## Next Steps

- Read [README.md](README.md) for full documentation
- Follow [DEMO.md](DEMO.md) for complete demonstration script
- Check [SETUP.md](SETUP.md) for detailed setup instructions

**Have fun demonstrating cybersecurity! 🔐**
