# VS Code Guide: Secure Communication Project

## 🎯 **Complete Guide to Open and Run in VS Code**

This guide will teach you how to open, navigate, and run the Secure Soldier-to-Soldier Communication project in Visual Studio Code.

---

## 📂 **STEP 1: Opening the Project in VS Code**

### **Method 1: Open from File Explorer**
1. **Open VS Code**
2. **File** → **Open Folder**
3. Navigate to your project folder: `Soldier_communication`
4. Click **Select Folder**

### **Method 2: Open from Command Line**
1. Open **Command Prompt** or **PowerShell**
2. Navigate to your project:
   ```bash
   cd C:\Users\[YourName]\Desktop\Soldier_communication
   ```
3. Open in VS Code:
   ```bash
   code .
   ```

### **Method 3: Drag and Drop**
1. Open **File Explorer**
2. Navigate to `Soldier_communication` folder
3. **Drag the folder** into VS Code window

---

## 🗂️ **STEP 2: Understanding the Project Structure**

Once opened, you'll see this structure in the **Explorer Panel** (left side):

```
Soldier_communication/
├── 📁 .kiro/                    # Kiro workspace files
├── 📁 secure-communication/     # Main project folder
│   ├── 📄 receiver.py          # Receiver role (Soldier B)
│   ├── 📄 sender.py            # Sender role (Soldier A)  
│   ├── 📄 attacker.py          # Attacker role (Hacker)
│   ├── 📄 config.py            # Configuration management
│   ├── 📄 crypto_utils.py      # AES-256-GCM encryption
│   ├── 📄 network_utils.py     # TCP communication
│   ├── 📄 logger.py            # Attack logging
│   ├── 📄 setup.py             # Key generation
│   ├── 📄 config.json          # Configuration file
│   ├── 📄 requirements.txt     # Dependencies
│   └── 📄 README.md            # Documentation
├── 📄 .gitignore               # Git ignore rules
└── 📄 VS_CODE_GUIDE.md         # This guide
```

---

## ⚙️ **STEP 3: Setting Up VS Code for Python**

### **Install Python Extension**
1. Click **Extensions** icon (left sidebar) or press `Ctrl+Shift+X`
2. Search for **"Python"**
3. Install **Python extension by Microsoft**
4. Restart VS Code if prompted

### **Select Python Interpreter**
1. Press `Ctrl+Shift+P` to open Command Palette
2. Type **"Python: Select Interpreter"**
3. Choose your Python installation (e.g., `Python 3.11.x`)

---

## 🖥️ **STEP 4: Opening and Using the Terminal**

### **Open Terminal in VS Code**
1. **Terminal** → **New Terminal** (or press `Ctrl+Shift+``)
2. The terminal opens at the bottom of VS Code
3. Make sure you're in the project directory

### **Navigate to Project Folder**
```bash
cd secure-communication
```

### **Install Dependencies**
```bash
pip install -r requirements.txt
```

---

## 🚀 **STEP 5: Running the Project (3 Methods)**

---

### **METHOD 1: Using Multiple Terminals (Recommended)**

#### **Step 5.1: Open Multiple Terminals**
1. Click **Terminal** → **New Terminal** (creates Terminal 1)
2. Click the **"+"** button next to terminal tabs (creates Terminal 2)
3. Click the **"+"** button again (creates Terminal 3)

You now have 3 terminals at the bottom!

#### **Step 5.2: Run Each Component**

**Terminal 1 - Receiver (Start FIRST):**
```bash
cd secure-communication
python receiver.py
```
**Wait for:** `✓ Receiver listening on port 8080`

**Terminal 2 - Attacker (Start SECOND):**
```bash
cd secure-communication
python attacker.py
```
**Wait for:** Menu with 4 options

**Terminal 3 - Sender (Start THIRD):**
```bash
cd secure-communication
python sender.py
```
**Wait for:** `✓ Connected successfully!`

---

### **METHOD 2: Using VS Code's Run Feature**

#### **Step 5.1: Create Launch Configuration**
1. Click **Run and Debug** icon (left sidebar) or press `Ctrl+Shift+D`
2. Click **"create a launch.json file"**
3. Select **Python**
4. Replace the content with:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Receiver",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/secure-communication/receiver.py",
            "cwd": "${workspaceFolder}/secure-communication",
            "console": "integratedTerminal"
        },
        {
            "name": "Sender", 
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/secure-communication/sender.py",
            "cwd": "${workspaceFolder}/secure-communication",
            "console": "integratedTerminal"
        },
        {
            "name": "Attacker",
            "type": "python",
            "request": "launch", 
            "program": "${workspaceFolder}/secure-communication/attacker.py",
            "cwd": "${workspaceFolder}/secure-communication",
            "console": "integratedTerminal"
        }
    ]
}
```

#### **Step 5.2: Run Each Component**
1. Select **"Receiver"** from dropdown
2. Press `F5` or click **▶️ Start Debugging**
3. Repeat for **"Attacker"** and **"Sender"**

---

### **METHOD 3: Using Code Runner Extension**

#### **Step 5.1: Install Code Runner**
1. **Extensions** → Search **"Code Runner"**
2. Install **Code Runner by Jun Han**

#### **Step 5.2: Run Files**
1. Open `receiver.py`
2. Press `Ctrl+F5` or click **▶️** button (top right)
3. Repeat for other files

---

## 📝 **STEP 6: Editing and Viewing Code**

### **Opening Files**
- **Single-click** file in Explorer → Preview (italic name)
- **Double-click** file in Explorer → Open permanently

### **Key Files to Explore**

#### **🔐 crypto_utils.py - Encryption Engine**
```python
def encrypt_message(plaintext: str, key: bytes) -> bytes:
    """Encrypt message using AES-256-GCM encryption."""
    # Military-grade encryption implementation
```

#### **🌐 network_utils.py - Communication**
```python
def send_message(sock, message_dict):
    """Send JSON message with length prefix."""
    # TCP socket communication
```

#### **🚨 logger.py - Attack Detection**
```python
def log_attack(attack_type, details):
    """Log security violations."""
    # Real-time threat monitoring
```

#### **⚙️ config.json - Configuration**
```json
{
  "network": {
    "receiver_ip": "127.0.0.1",
    "receiver_port": 8080
  },
  "security": {
    "encryption_key": "...",
    "auth_key": "..."
  }
}
```

---

## 🎬 **STEP 7: Running the Demo**

### **Demo Flow in VS Code**

#### **Phase 1: Normal Communication**
1. **Terminal 3 (Sender)**: Type `Hello World!`
2. **Terminal 1 (Receiver)**: Shows decrypted message + GREEN status

#### **Phase 2: Capture Message**
1. **Terminal 2 (Attacker)**: Select option `1`
2. Enter dummy encrypted data
3. Shows captured message (encrypted gibberish)

#### **Phase 3: Replay Attack**
1. **Terminal 2 (Attacker)**: Select option `3`
2. **Terminal 1 (Receiver)**: Detects attack, turns RED!

#### **Phase 4: System Recovery**
1. **Terminal 3 (Sender)**: Send new message
2. **Terminal 1 (Receiver)**: Still works despite attacks!

---

## 🔧 **STEP 8: Useful VS Code Features**

### **Split Editor**
- **View** → **Editor Layout** → **Split Right**
- View multiple files side-by-side

### **Integrated Git**
- **Source Control** icon (left sidebar)
- See changes, commit, push to GitHub

### **Search Across Files**
- Press `Ctrl+Shift+F`
- Search for functions, variables across entire project

### **Go to Definition**
- `Ctrl+Click` on function name
- Jump to where it's defined

### **IntelliSense (Auto-complete)**
- Start typing → VS Code suggests completions
- Press `Tab` to accept

---

## 📊 **STEP 9: Monitoring and Debugging**

### **Terminal Management**
- **Rename terminals**: Right-click tab → Rename
- **Split terminal**: Click split icon
- **Kill terminal**: Click trash icon

### **Output Monitoring**
Watch these terminals for:

**Receiver Terminal:**
```
✓ Message received (seq #1): Hello World!
Threat Level: SAFE
```

**Sender Terminal:**
```
Message > Hello World!
✓ Message sent (seq #1): Hello World!
```

**Attacker Terminal:**
```
✓ REPLAY ATTACK EXECUTED!
```

### **Debug Mode**
- Set breakpoints: Click left margin of code
- Press `F5` to start debugging
- Step through code line by line

---

## 🎯 **STEP 10: Customizing VS Code**

### **Themes**
- **File** → **Preferences** → **Color Theme**
- Try: Dark+ (default), Monokai, Solarized Dark

### **Font Size**
- **File** → **Preferences** → **Settings**
- Search "font size"
- Increase for better visibility during demos

### **Terminal Font**
- **File** → **Preferences** → **Settings**
- Search "terminal font"
- Use "Consolas" or "Courier New" for clarity

---

## 📋 **QUICK REFERENCE COMMANDS**

### **Essential VS Code Shortcuts**
| Action | Shortcut |
|--------|----------|
| Open Command Palette | `Ctrl+Shift+P` |
| New Terminal | `Ctrl+Shift+`` |
| Run Python File | `Ctrl+F5` |
| Open File | `Ctrl+O` |
| Save File | `Ctrl+S` |
| Find in File | `Ctrl+F` |
| Find in Project | `Ctrl+Shift+F` |
| Go to Line | `Ctrl+G` |
| Comment/Uncomment | `Ctrl+/` |

### **Terminal Commands**
| Action | Command |
|--------|---------|
| Navigate to project | `cd secure-communication` |
| Install dependencies | `pip install -r requirements.txt` |
| Run receiver | `python receiver.py` |
| Run sender | `python sender.py` |
| Run attacker | `python attacker.py` |
| Generate keys | `python setup.py` |
| Check Python version | `python --version` |

---

## 🆘 **Troubleshooting in VS Code**

### **Problem: Python not found**
**Solution:**
1. `Ctrl+Shift+P` → "Python: Select Interpreter"
2. Choose correct Python installation

### **Problem: Module not found**
**Solution:**
1. Open terminal in VS Code
2. `cd secure-communication`
3. `pip install -r requirements.txt`

### **Problem: Can't see terminals**
**Solution:**
1. **View** → **Terminal**
2. Or press `Ctrl+Shift+``

### **Problem: Code not running**
**Solution:**
1. Make sure you're in `secure-communication` folder
2. Check Python interpreter is selected
3. Install Python extension

---

## 🎓 **VS Code Tips for Demos**

### **Presentation Mode**
1. **View** → **Appearance** → **Zen Mode** (`Ctrl+K Z`)
2. Hides all panels except editor
3. Press `Escape` twice to exit

### **Increase Font for Audience**
1. `Ctrl+Shift+P` → "Preferences: Open Settings"
2. Search "font size"
3. Set to 16-18 for demos

### **Terminal Visibility**
1. **View** → **Appearance** → **Panel Position** → **Right**
2. Moves terminal to right side for better visibility

### **Color Coding**
- **Green text**: Successful operations
- **Red text**: Errors or attacks
- **Blue text**: Information
- **Magenta text**: Attacker actions

---

## 📚 **Learning Resources**

### **VS Code Documentation**
- [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial)
- [VS Code Terminal Guide](https://code.visualstudio.com/docs/terminal/basics)

### **Project Documentation**
- `README.md` - Complete project overview
- `SECURITY_UPGRADE.md` - AES-256-GCM details
- `COMPLETE_3PC_GUIDE.md` - Multi-PC setup

---

## ✅ **Checklist: Ready for Demo**

### **Setup Checklist**
- [ ] VS Code installed with Python extension
- [ ] Project opened in VS Code
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Python interpreter selected
- [ ] 3 terminals opened and labeled

### **Demo Checklist**
- [ ] Receiver started first (Terminal 1)
- [ ] Attacker started second (Terminal 2)  
- [ ] Sender started third (Terminal 3)
- [ ] All showing "ready" status
- [ ] Font size increased for audience visibility

### **Presentation Checklist**
- [ ] Zen mode enabled for clean view
- [ ] Terminal positioned for visibility
- [ ] Color theme suitable for projector
- [ ] Demo script prepared

---

## 🎉 **You're Ready!**

You now know how to:
- ✅ Open the project in VS Code
- ✅ Navigate the code structure
- ✅ Run all 3 components in separate terminals
- ✅ Monitor real-time communication
- ✅ Demonstrate attacks and detection
- ✅ Customize VS Code for presentations

**Your secure communication system is ready for demonstration in VS Code!** 🚀🔐

---

## 📞 **Quick Help**

**If you get stuck:**
1. Check this guide
2. Use `Ctrl+Shift+P` → "Help: Welcome"
3. **Terminal** → **New Terminal** if terminals disappear
4. **File** → **Reload Window** if VS Code acts strange

**Happy coding and demonstrating!** 🎯