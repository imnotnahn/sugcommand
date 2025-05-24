#!/usr/bin/env python3
"""
Demo script for SugCommand shell integration features.

This script demonstrates the new real-time shell integration capabilities
including daemon management and auto-completion setup.
"""

import time
import sys
from pathlib import Path

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sugcommand.integrations.realtime_daemon import RealtimeDaemon, DaemonClient
from sugcommand.integrations.bash_integration import BashIntegration
from sugcommand.integrations.zsh_integration import ZshIntegration
from sugcommand.integrations.fish_integration import FishIntegration
from sugcommand.core import ConfigManager
from sugcommand.utils.display import SuggestionFormatter


def print_header(title: str):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"🚀 {title}")
    print(f"{'='*60}")


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'─'*40}")
    print(f"📋 {title}")
    print(f"{'─'*40}")


def demo_daemon():
    """Demo daemon functionality."""
    print_header("DAEMON MANAGEMENT DEMO")
    
    client = DaemonClient()
    
    print_section("Checking Daemon Status")
    if client.is_daemon_running():
        print("✅ Daemon is already running")
    else:
        print("❌ Daemon is not running")
        print("Starting daemon...")
        
        # Start daemon in background (simplified for demo)
        daemon = RealtimeDaemon()
        import threading
        daemon_thread = threading.Thread(target=daemon.start, daemon=True)
        daemon_thread.start()
        
        # Wait for daemon to start
        time.sleep(2)
        
        if client.is_daemon_running():
            print("✅ Daemon started successfully")
        else:
            print("❌ Failed to start daemon")
            return False
    
    print_section("Testing Daemon Communication")
    test_commands = ["git c", "apt u", "docker r", "npm i", "python -m"]
    
    for cmd in test_commands:
        print(f"\n🔍 Testing: '{cmd}'")
        start_time = time.time()
        suggestions = client.get_suggestions(cmd, timeout=1.0)
        response_time = time.time() - start_time
        
        if suggestions:
            print(f"   ⚡ Response time: {response_time*1000:.1f}ms")
            print(f"   📝 Found {len(suggestions)} suggestions:")
            for i, suggestion in enumerate(suggestions[:3], 1):
                confidence = suggestion.get('confidence', 0) * 100
                print(f"      {i}. {suggestion['command']} ({confidence:.0f}%)")
        else:
            print(f"   ⚠️  No suggestions found ({response_time*1000:.1f}ms)")
    
    return True


def demo_shell_integrations():
    """Demo shell integration features."""
    print_header("SHELL INTEGRATION DEMO")
    
    integrations = [
        ("Bash", BashIntegration()),
        ("Zsh", ZshIntegration()),
        ("Fish", FishIntegration()),
    ]
    
    for shell_name, integration in integrations:
        print_section(f"{shell_name} Integration")
        
        status = integration.get_status()
        print(f"Shell: {status['shell']}")
        print(f"Installed: {'✅' if status['installed'] else '❌'}")
        print(f"Daemon Running: {'✅' if status['daemon_running'] else '❌'}")
        print(f"Script Path: {status['completion_script']}")
        
        if not status['installed']:
            print(f"\n💡 To install {shell_name} integration:")
            print(f"   sugcommand integration install --shell {shell_name.lower()}")
        else:
            print(f"\n✅ {shell_name} integration is ready!")
            
            # Test completion for bash if available
            if hasattr(integration, 'get_suggestions_for_completion'):
                print(f"\n🧪 Testing completion suggestions:")
                test_cmds = ["git c", "apt u"]
                for cmd in test_cmds:
                    suggestions = integration.get_suggestions_for_completion(cmd, limit=3)
                    if suggestions:
                        print(f"   '{cmd}' → {', '.join(suggestions)}")
                    else:
                        print(f"   '{cmd}' → No suggestions")


def demo_performance():
    """Demo performance metrics."""
    print_header("PERFORMANCE DEMO")
    
    client = DaemonClient()
    if not client.is_daemon_running():
        print("❌ Daemon not running. Start daemon first.")
        return
    
    print_section("Performance Benchmarks")
    
    test_commands = ["git", "ls", "cd", "python", "docker", "npm", "apt", "sudo"]
    total_time = 0
    total_requests = 0
    
    print("Running performance tests...")
    
    for cmd in test_commands:
        times = []
        for _ in range(5):  # 5 requests per command
            start_time = time.time()
            suggestions = client.get_suggestions(cmd, timeout=1.0)
            response_time = time.time() - start_time
            times.append(response_time)
            total_time += response_time
            total_requests += 1
        
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        print(f"📊 '{cmd}': avg={avg_time*1000:.1f}ms, min={min_time*1000:.1f}ms, max={max_time*1000:.1f}ms")
    
    avg_response_time = total_time / total_requests
    print(f"\n🎯 Overall Performance:")
    print(f"   Total requests: {total_requests}")
    print(f"   Average response time: {avg_response_time*1000:.1f}ms")
    print(f"   Requests per second: {1/avg_response_time:.1f}")


def demo_configuration():
    """Demo configuration features."""
    print_header("CONFIGURATION DEMO")
    
    config = ConfigManager()
    formatter = SuggestionFormatter(color_enabled=True)
    
    print_section("Current Configuration")
    summary = config.get_config_summary()
    
    config_items = [
        ("Status", "✅ ENABLED" if summary['enabled'] else "❌ DISABLED"),
        ("Max suggestions", summary['max_suggestions']),
        ("History analysis", "✅" if summary['history_analysis_enabled'] else "❌"),
        ("Command scanning", "✅" if summary['command_scan_enabled'] else "❌"),
        ("Fuzzy search", "✅" if summary['fuzzy_search_enabled'] else "❌"),
        ("Colors", "✅" if summary['color_enabled'] else "❌"),
        ("Custom directories", summary['custom_directories_count']),
        ("Excluded commands", summary['excluded_commands_count']),
    ]
    
    for key, value in config_items:
        print(f"   {key}: {value}")
    
    print(f"\n📁 Config file: {summary['config_file']}")


def demo_usage_examples():
    """Demo practical usage examples."""
    print_header("USAGE EXAMPLES")
    
    examples = [
        ("Developer Workflow", [
            "git status → git s<TAB>",
            "npm install → npm i<TAB>", 
            "docker run → docker r<TAB>",
            "python -m pip → python -m<TAB>",
        ]),
        ("System Administration", [
            "systemctl start → systemctl s<TAB>",
            "apt update → apt u<TAB>",
            "sudo service → sudo s<TAB>",
            "find . -name → find<TAB>",
        ]),
        ("File Operations", [
            "ls -la → ls<TAB>",
            "chmod +x → chmod<TAB>",
            "cp file.txt → cp<TAB>",
            "mkdir new_dir → mkdir<TAB>",
        ]),
    ]
    
    for category, cmds in examples:
        print_section(category)
        for cmd in cmds:
            print(f"   💡 {cmd}")


def main():
    """Run the complete demo."""
    print("🎉 Welcome to SugCommand Shell Integration Demo!")
    print("This demo showcases the real-time auto-completion features.")
    
    try:
        # Demo daemon functionality
        daemon_ok = demo_daemon()
        
        if daemon_ok:
            # Demo shell integrations
            demo_shell_integrations()
            
            # Demo performance
            demo_performance()
        
        # Demo configuration (works without daemon)
        demo_configuration()
        
        # Demo usage examples
        demo_usage_examples()
        
        print_header("SETUP INSTRUCTIONS")
        print("""
🚀 To enable real-time auto-completion:

1. Install shell integration:
   sugcommand integration install

2. Start daemon:
   sugcommand daemon start --background

3. Add to your shell config:
   # For Bash (~/.bashrc):
   source ~/.config/sugcommand/bash_completion.sh
   
   # For Zsh (~/.zshrc):
   source ~/.config/sugcommand/zsh_completion.zsh
   
   # For Fish (~/.config/fish/config.fish):
   source ~/.config/sugcommand/fish_completion.fish

4. Restart your shell:
   exec $SHELL

5. Enjoy auto-completion:
   git c<TAB>  # 🎉 Suggestions appear!

📚 For more info: sugcommand --help
        """)
        
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 