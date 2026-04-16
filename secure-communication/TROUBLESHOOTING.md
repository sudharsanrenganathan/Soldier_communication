# Troubleshooting Guide

## Common Errors and Solutions

### 1. Connection Refused Error

**Error Message**:
```
Error: Cannot connect to receiver at 192.168.1.100:5555
Ensure receiver is running and network is configured correctly
```

**Causes**:
- Receiver is not running
- Wrong IP address in config.json
- Firewall blocking the connection
- Laptops on different networks

**Solutions**:
1. **Start receiver first**: Always start `receiver.py` before `sender.py` or `attacker.py`
2. **Verify IP address**: 
   - On receiver laptop, run `ipconfig` (Windows) or `ifconfig` (Mac/Linux)
   - Update `receiver_ip` in `config.json` on all laptops
3. **Check firewall**:
   - Windows: Allow Python through Windows Firewall
   - Mac: System Preferences → Security & Privacy → Firewall → Allow Python
   - Linux: `sudo ufw allow 5555/tcp`
4. **Verify same network**: All laptops must be on the same WiFi network

---

### 2. Port Already in Use

**Error Message**:
```
Error: Port 5555 is already in use
Change the port in config.json or stop the process using this port
```

**Causes**:
- Receiver is already running
- Another application is using port 5555
- Previous receiver process didn't close properly

**Solutions**:
1. **Stop existing receiver**: Press Ctrl+C to stop the receiver, then restart
2. **Change port**: Edit `config.json` and change `receiver_port` to a different value (e.g., 5556)
   - **Important**: Change on ALL 3 laptops
3. **Kill process** (if receiver won't stop):
   - Windows: `taskkill /F /IM python.exe`
   - Mac/Linux: `pkill -9 python` or `lsof -ti:5555 | xargs kill -9`

---

### 3. Key Errors

**Error Message**:
```
Error loading keys: Invalid base64-encoded string
Run setup.py to generate keys
```

**Causes**:
- Keys not generated
- config.json corrupted
- Keys not properly copied to all laptops

**Solutions**:
1. **Regenerate keys**: Run `python setup.py` on one laptop
2. **Copy config.json**: Copy the updated `config.json` to all 3 laptops
3. **Verify keys**: Open `config.json` and check that `encryption_key` and `auth_key` are not empty

---

### 4. Module Not Found Error

**Error Message**:
```
ModuleNotFoundError: No module named 'cryptography'
```

**Causes**:
- Dependencies not installed
- Wrong Python environment

**Solutions**:
1. **Install dependencies**: Run `pip install -r requirements.txt`
2. **Check Python version**: Run `python --version` (must be 3.8+)
3. **Use pip3**: If `pip` doesn't work, try `pip3 install -r requirements.txt`
4. **Virtual environment**: If using venv, ensure it's activated

---

### 5. Configuration File Not Found

**Error Message**:
```
Error: Configuration file 'config.json' not found
Run setup.py to generate keys and configuration
```

**Causes**:
- Running from wrong directory
- config.json deleted or not copied

**Solutions**:
1. **Navigate to correct directory**: `cd secure-communication`
2. **Verify file exists**: Run `ls` (Mac/Linux) or `dir` (Windows) to see if `config.json` is present
3. **Copy from template**: If missing, copy `config.json.template` to `config.json` and run `setup.py`

---

### 6. Network Timeout

**Error Message**:
```
Error: Connection timeout after 30 seconds
Check if receiver at 192.168.1.100:5555 is reachable
```

**Causes**:
- Receiver not responding
- Network congestion
- Firewall blocking connection
- Wrong IP address

**Solutions**:
1. **Ping test**: Run `ping 192.168.1.100` to verify network connectivity
2. **Check receiver**: Ensure receiver is running and showing "Waiting for connections..."
3. **Increase timeout**: Edit `config.json` and increase `timeout` value (e.g., 60)
4. **Try localhost**: For testing on single laptop, use `127.0.0.1` as `receiver_ip`

---

### 7. Decryption Failed Error

**Error Message**:
```
Error: Decryption failed - message may be corrupted or tampered
```

**Causes**:
- Different keys on sender and receiver
- Message corrupted during transmission
- Attacker modified the message

**Solutions**:
1. **Verify same keys**: Ensure all laptops have the same `config.json` with same keys
2. **Regenerate keys**: Run `setup.py` and copy `config.json` to all laptops
3. **Check network**: Verify stable network connection

---

### 8. JSON Decode Error

**Error Message**:
```
Error: Received malformed message: Expecting value: line 1 column 1 (char 0)
```

**Causes**:
- Network interruption during transmission
- Incompatible sender/receiver versions
- Buffer size too small

**Solutions**:
1. **Increase buffer size**: Edit `config.json` and increase `buffer_size` (e.g., 8192)
2. **Verify same codebase**: Ensure all laptops have the same version of the code
3. **Restart receiver**: Stop and restart `receiver.py`

---

### 9. No Color Output in Terminal

**Issue**: Terminal shows escape codes like `\033[92m` instead of colors

**Causes**:
- Terminal doesn't support ANSI colors
- Windows Command Prompt (older versions)

**Solutions**:
1. **Use different terminal**:
   - Windows: Use Windows Terminal, PowerShell, or Git Bash
   - Mac: Use Terminal.app or iTerm2
   - Linux: Most terminals support colors by default
2. **Enable ANSI support** (Windows 10+):
   - Run: `reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1`
3. **Ignore colors**: The system works fine without colors - they're just visual indicators

---

### 10. Permission Denied Error

**Error Message**:
```
PermissionError: [Errno 13] Permission denied: 'config.json'
```

**Causes**:
- File is read-only
- Insufficient permissions
- File is open in another program

**Solutions**:
1. **Close other programs**: Close any text editors that have `config.json` open
2. **Check permissions**: 
   - Windows: Right-click → Properties → Uncheck "Read-only"
   - Mac/Linux: `chmod 644 config.json`
3. **Run as administrator** (last resort):
   - Windows: Right-click → Run as administrator
   - Mac/Linux: `sudo python receiver.py` (not recommended)

---

### 11. Replay Attack Not Detected

**Issue**: Receiver accepts replayed message instead of rejecting it

**Causes**:
- Sequence number was incremented
- Timestamp is still fresh (within 60 seconds)
- Different receiver instance (sequence number reset)

**Solutions**:
1. **Use same sequence number**: When capturing message, use the exact same sequence number
2. **Replay quickly**: Replay within 60 seconds of capture
3. **Don't restart receiver**: Restarting receiver resets sequence number tracking
4. **Check validation logic**: Verify `validate_message()` function is working correctly

---

### 12. Attacker Can't Connect

**Error Message** (on attacker laptop):
```
Error: Cannot connect to receiver at 192.168.1.100:5555
```

**Causes**:
- Same as "Connection Refused Error" above
- Receiver only accepts one connection at a time

**Solutions**:
1. **Wait for sender to disconnect**: The receiver accepts one connection at a time
2. **Use separate receiver instances**: For demo purposes, you can run multiple receivers on different ports
3. **Verify IP address**: Ensure attacker has correct receiver IP in `config.json`

---

## Testing on Single Laptop

If you don't have 3 laptops, you can test on a single laptop:

1. **Edit config.json**: Set `receiver_ip` to `127.0.0.1` (localhost)
2. **Open 3 terminals**: One for each role
3. **Run in order**:
   - Terminal 1: `python receiver.py`
   - Terminal 2: `python attacker.py`
   - Terminal 3: `python sender.py`

This works exactly the same but all communication stays on your local machine.

---

## Network Debugging Commands

### Check if port is open:
```bash
# Windows
netstat -an | findstr 5555

# Mac/Linux
netstat -an | grep 5555
lsof -i :5555
```

### Find your IP address:
```bash
# Windows
ipconfig

# Mac/Linux
ifconfig
ip addr show
```

### Test connectivity:
```bash
# Ping receiver
ping 192.168.1.100

# Test port (requires telnet)
telnet 192.168.1.100 5555
```

---

## Still Having Issues?

If none of the above solutions work:

1. **Check Python version**: Must be 3.8 or higher
   ```bash
   python --version
   ```

2. **Reinstall dependencies**:
   ```bash
   pip uninstall cryptography hypothesis pytest
   pip install -r requirements.txt
   ```

3. **Try localhost test**: Test on single laptop using `127.0.0.1`

4. **Check system logs**: Look for error messages in terminal output

5. **Simplify setup**: Start with just sender and receiver (skip attacker initially)

6. **Review code**: Check for any modifications that might have broken functionality

---

## Getting Help

If you're still stuck:
- Review the SETUP.md and DEMO.md guides
- Check that all steps were followed in order
- Verify all 3 laptops have identical code and configuration
- Try the single-laptop test to isolate network issues

---

**Remember**: Most issues are related to network configuration or missing dependencies. Double-check IP addresses and ensure all dependencies are installed!
