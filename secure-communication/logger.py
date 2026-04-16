# Attack logging and threat level monitoring system
# Tracks security violations and calculates threat levels

from datetime import datetime
from enum import Enum
from dataclasses import dataclass
from typing import Optional


class ThreatLevel(Enum):
    """Threat level enumeration based on attack count."""
    SAFE = "SAFE"          # 0 attacks
    WARNING = "WARNING"    # 1-2 attacks
    ATTACK = "ATTACK"      # 3+ attacks


@dataclass
class AttackLog:
    """Attack log entry data structure."""
    timestamp: datetime
    attack_type: str  # "FAKE_SENDER" or "REPLAY_ATTACK"
    details: str
    message_data: Optional[dict] = None


# Global attack log storage
_attack_logs = []


def log_attack(attack_type: str, details: str, message_data: Optional[dict] = None) -> None:
    """Log a security violation.
    
    Args:
        attack_type: Type of attack detected ("FAKE_SENDER" or "REPLAY_ATTACK")
        details: Additional information about the attack
        message_data: Optional captured message for analysis
    """
    entry = AttackLog(
        timestamp=datetime.now(),
        attack_type=attack_type,
        details=details,
        message_data=message_data
    )
    _attack_logs.append(entry)


def get_attack_count() -> int:
    """Get total number of detected attacks.
    
    Returns:
        int: Number of attacks logged
    """
    return len(_attack_logs)


def clear_attack_log() -> None:
    """Clear all attack logs (useful for testing)."""
    global _attack_logs
    _attack_logs = []



def get_threat_level() -> ThreatLevel:
    """Calculate current threat level based on attack count.
    
    Returns:
        ThreatLevel: SAFE (0 attacks), WARNING (1-2 attacks), or ATTACK (3+ attacks)
    """
    attack_count = get_attack_count()
    
    if attack_count == 0:
        return ThreatLevel.SAFE
    elif attack_count <= 2:
        return ThreatLevel.WARNING
    else:
        return ThreatLevel.ATTACK



def display_attack_log(colors: Optional[dict] = None) -> None:
    """Display all logged attacks with timestamps and color coding.
    
    Args:
        colors: Optional dictionary of ANSI color codes
    """
    # Default colors if not provided
    if colors is None:
        colors = {
            'attack': '\033[91m',  # Red
            'reset': '\033[0m'
        }
    
    if not _attack_logs:
        print(f"{colors.get('info', '')}No attacks detected{colors.get('reset', '')}")
        return
    
    print(f"\n{colors.get('attack', '')}=== ATTACK LOG ==={colors.get('reset', '')}")
    for entry in _attack_logs:
        timestamp_str = entry.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        print(f"{colors.get('attack', '')}[{timestamp_str}] {entry.attack_type}: {entry.details}{colors.get('reset', '')}")
    print()


def display_threat_level(colors: Optional[dict] = None) -> None:
    """Display current threat level with ANSI color coding.
    
    Args:
        colors: Optional dictionary of ANSI color codes with keys:
            - safe: Green color code
            - warning: Yellow color code
            - attack: Red color code
            - reset: Reset color code
    """
    # Default colors if not provided
    if colors is None:
        colors = {
            'safe': '\033[92m',      # Green
            'warning': '\033[93m',   # Yellow
            'attack': '\033[91m',    # Red
            'reset': '\033[0m'
        }
    
    threat_level = get_threat_level()
    attack_count = get_attack_count()
    
    # Select color based on threat level
    if threat_level == ThreatLevel.SAFE:
        color = colors.get('safe', '')
    elif threat_level == ThreatLevel.WARNING:
        color = colors.get('warning', '')
    else:  # ATTACK
        color = colors.get('attack', '')
    
    reset = colors.get('reset', '')
    
    # Display threat level with color
    print(f"\n{color}╔══════════════════════════════════════╗{reset}")
    print(f"{color}║  Threat Level: {threat_level.value:20s} ║{reset}")
    print(f"{color}║  Attacks Detected: {attack_count:2d}                ║{reset}")
    print(f"{color}╚══════════════════════════════════════╝{reset}\n")
