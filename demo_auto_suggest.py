#!/usr/bin/env python3

import sys
import time
import threading
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from sugcommand.integrations.auto_suggest import (
    AutoSuggestionServer, 
    AutoSuggestionClient, 
    TerminalSuggestionDisplay,
    AutoSuggestionHandler,
    create_shell_integration
)

def simulate_typing_with_suggestions():
    """Simulate typing with auto-suggestions"""
    print("\n🎯 Auto-Suggestion Demo")
    print("========================")
    print("This demo simulates typing commands and showing auto-suggestions")
    print("in real-time, just like it would work in your terminal.\n")
    
    # Start suggestion server
    server = AutoSuggestionServer()
    server_thread = threading.Thread(target=server.start, daemon=True)
    server_thread.start()
    time.sleep(1)
    
    # Create handler
    handler = AutoSuggestionHandler()
    
    # Simulate typing different commands
    test_commands = [
        ("g", "git"),
        ("gi", "git"),
        ("git", "git"),
        ("git c", "git c"),
        ("git co", "git co"),
        ("git com", "git com"),
        ("docker", "docker"),
        ("docker r", "docker r"),
        ("npm", "npm"),
        ("npm i", "npm i"),
        ("python", "python"),
        ("ls", "ls"),
        ("cd", "cd")
    ]
    
    for partial, full in test_commands:
        print(f"\n💻 Typing: '{partial}'")
        print("─" * 40)
        
        # Simulate user typing
        handler.handle_command_input(partial)
        
        # Wait for suggestions to appear
        time.sleep(1)
        
        # Hide suggestions after a moment
        if partial != full:
            handler.hide_suggestions()
            time.sleep(0.5)
    
    # Final cleanup
    handler.hide_suggestions()
    server.stop()
    
    print("\n✅ Demo completed!")

def interactive_suggestion_test():
    """Interactive test where user can type commands"""
    print("\n🔧 Interactive Auto-Suggestion Test")
    print("===================================")
    print("Start typing commands to see suggestions appear automatically!")
    print("Type 'quit' to exit.\n")
    
    # Start suggestion server
    server = AutoSuggestionServer()
    server_thread = threading.Thread(target=server.start, daemon=True)
    server_thread.start()
    time.sleep(1)
    
    # Create handler
    handler = AutoSuggestionHandler()
    
    try:
        while True:
            command = input("Command> ").strip()
            
            if command.lower() == 'quit':
                break
            
            if command:
                print(f"Showing suggestions for: '{command}'")
                handler.handle_command_input(command)
                
                # Keep suggestions visible for a moment
                time.sleep(2)
                handler.hide_suggestions()
            
    except KeyboardInterrupt:
        pass
    
    handler.hide_suggestions()
    server.stop()
    print("\n👋 Goodbye!")

def setup_shell_integration():
    """Setup shell integration with instructions"""
    print("\n⚙️ Setting up Shell Integration")
    print("===============================")
    
    try:
        config_dir = create_shell_integration()
        
        print(f"✅ Shell integration files created in: {config_dir}")
        print("\n📝 Setup Instructions:")
        print("======================")
        
        print("\n1. For Bash users, add this line to ~/.bashrc:")
        print(f"   source {config_dir}/bash_auto_suggest.sh")
        
        print("\n2. For Zsh users, add this line to ~/.zshrc:")
        print(f"   source {config_dir}/zsh_auto_suggest.zsh")
        
        print("\n3. Restart your shell:")
        print("   exec $SHELL")
        
        print("\n4. Start the auto-suggestion daemon:")
        print("   sugcommand auto start --background")
        
        print("\n5. Now try typing commands in your terminal!")
        print("   🎉 Suggestions will appear automatically as you type!")
        
        print("\n📋 Command Reference:")
        print("   sugcommand auto start --background   # Start daemon")
        print("   sugcommand auto stop                 # Stop daemon")
        print("   sugcommand auto status               # Check status")
        print("   sugcommand auto install              # Install integration")
        
        return True
        
    except Exception as e:
        print(f"❌ Error setting up shell integration: {e}")
        return False

def performance_test():
    """Test suggestion performance"""
    print("\n⚡ Performance Test")
    print("==================")
    
    # Start server
    server = AutoSuggestionServer()
    server_thread = threading.Thread(target=server.start, daemon=True)
    server_thread.start()
    time.sleep(1)
    
    client = AutoSuggestionClient()
    
    test_commands = ["git", "docker", "npm", "python", "ls", "cd", "vim", "grep", "find", "curl"]
    total_time = 0
    successful_requests = 0
    
    print("Testing suggestion response times...")
    
    for cmd in test_commands:
        start_time = time.time()
        suggestions = client.get_suggestions(cmd)
        elapsed = time.time() - start_time
        
        if suggestions:
            successful_requests += 1
            total_time += elapsed
            print(f"  {cmd:10} -> {len(suggestions)} suggestions in {elapsed*1000:.1f}ms")
        else:
            print(f"  {cmd:10} -> No suggestions")
    
    if successful_requests > 0:
        avg_time = total_time / successful_requests
        print(f"\n📊 Results:")
        print(f"  Successful requests: {successful_requests}/{len(test_commands)}")
        print(f"  Average response time: {avg_time*1000:.1f}ms")
        print(f"  Total time: {total_time*1000:.1f}ms")
        
        if avg_time < 0.1:  # Less than 100ms
            print("  ✅ Performance: Excellent!")
        elif avg_time < 0.2:
            print("  ✅ Performance: Good")
        else:
            print("  ⚠️  Performance: Could be better")
    
    server.stop()

def main():
    print("🚀 SugCommand Auto-Suggestion Demo & Setup")
    print("==========================================")
    print("Welcome to the enhanced SugCommand with auto-suggestions!")
    print("This tool provides real-time command suggestions as you type.")
    
    while True:
        print("\n📋 Available options:")
        print("1. 🎯 Watch Auto-Suggestion Demo")
        print("2. 🔧 Interactive Test")
        print("3. ⚙️ Setup Shell Integration") 
        print("4. ⚡ Performance Test")
        print("5. 📖 View Integration Files")
        print("6. 🚪 Exit")
        
        try:
            choice = input("\nSelect option (1-6): ").strip()
            
            if choice == "1":
                simulate_typing_with_suggestions()
            elif choice == "2":
                interactive_suggestion_test()
            elif choice == "3":
                setup_shell_integration()
            elif choice == "4":
                performance_test()
            elif choice == "5":
                config_dir = Path.home() / ".config" / "sugcommand"
                bash_file = config_dir / "bash_auto_suggest.sh"
                zsh_file = config_dir / "zsh_auto_suggest.zsh"
                
                print(f"\n📁 Integration files location: {config_dir}")
                if bash_file.exists():
                    print(f"  ✅ Bash: {bash_file}")
                else:
                    print("  ❌ Bash integration not found")
                    
                if zsh_file.exists():
                    print(f"  ✅ Zsh:  {zsh_file}")
                else:
                    print("  ❌ Zsh integration not found")
                    
            elif choice == "6":
                print("\n👋 Thank you for trying SugCommand!")
                print("Don't forget to set up shell integration for the best experience!")
                break
            else:
                print("❌ Invalid option. Please choose 1-6.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except EOFError:
            print("\n\n👋 Goodbye!")
            break

if __name__ == "__main__":
    main() 