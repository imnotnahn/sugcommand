#!/usr/bin/env python3

import sys
import time
import threading
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from sugcommand.integrations.auto_suggest import (
    AutoSuggestionServer, 
    AutoSuggestionClient, 
    AutoSuggestionHandler,
    create_shell_integration
)

def test_server_client():
    """Test the server-client communication"""
    print("Testing server-client communication...")
    
    # Start server in background
    server = AutoSuggestionServer()
    server_thread = threading.Thread(target=server.start, daemon=True)
    server_thread.start()
    
    # Wait for server to start
    time.sleep(1)
    
    # Test client
    client = AutoSuggestionClient()
    
    test_commands = ["git", "docker", "ls", "npm", "python"]
    
    for cmd in test_commands:
        print(f"\nTesting command: '{cmd}'")
        suggestions = client.get_suggestions(cmd)
        if suggestions:
            print(f"  Suggestions: {suggestions}")
        else:
            print("  No suggestions found")
    
    server.stop()
    print("\nServer-client test completed!")

def test_display():
    """Test the terminal display"""
    print("Testing terminal display...")
    
    from sugcommand.integrations.auto_suggest import TerminalSuggestionDisplay
    
    display = TerminalSuggestionDisplay()
    
    # Test showing suggestions
    print("Showing test suggestions in 3 seconds...")
    time.sleep(3)
    
    suggestions = [
        "git commit -m 'message'",
        "git push origin main", 
        "git pull origin main",
        "git status",
        "git add ."
    ]
    
    display.show_suggestions(suggestions, "git")
    
    print("Suggestions displayed above. Press Enter to hide them...")
    input()
    
    display.hide_suggestions()
    print("Suggestions hidden!")

def test_shell_integration():
    """Test creating shell integration files"""
    print("Testing shell integration creation...")
    
    config_dir = create_shell_integration()
    
    print(f"Integration files created in: {config_dir}")
    
    # Check if files exist
    bash_file = config_dir / "bash_auto_suggest.sh"
    zsh_file = config_dir / "zsh_auto_suggest.zsh"
    
    if bash_file.exists():
        print(f"✓ Bash integration: {bash_file}")
    else:
        print("✗ Bash integration not created")
        
    if zsh_file.exists():
        print(f"✓ Zsh integration: {zsh_file}")
    else:
        print("✗ Zsh integration not created")

def main():
    print("SugCommand Auto-Suggestion Test")
    print("================================")
    
    while True:
        print("\nSelect test to run:")
        print("1. Test server-client communication")
        print("2. Test terminal display")
        print("3. Test shell integration creation")
        print("4. Run all tests")
        print("5. Exit")
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == "1":
            test_server_client()
        elif choice == "2":
            test_display()
        elif choice == "3":
            test_shell_integration()
        elif choice == "4":
            test_shell_integration()
            test_server_client()
            test_display()
        elif choice == "5":
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main() 