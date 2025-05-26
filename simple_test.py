#!/usr/bin/env python3

import sys
import time
import threading
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_basic_imports():
    """Test basic imports"""
    print("Testing basic imports...")
    try:
        from sugcommand.integrations.auto_suggest import (
            AutoSuggestionServer, 
            AutoSuggestionClient, 
            TerminalSuggestionDisplay,
            create_shell_integration
        )
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False

def test_shell_integration():
    """Test creating shell integration files"""
    print("Testing shell integration creation...")
    try:
        from sugcommand.integrations.auto_suggest import create_shell_integration
        config_dir = create_shell_integration()
        print(f"✓ Integration files created in: {config_dir}")
        return True
    except Exception as e:
        print(f"✗ Shell integration error: {e}")
        return False

def test_display():
    """Test terminal display"""
    print("Testing terminal display...")
    try:
        from sugcommand.integrations.auto_suggest import TerminalSuggestionDisplay
        
        display = TerminalSuggestionDisplay()
        
        # Test showing suggestions
        suggestions = [
            "git commit -m 'message'",
            "git push origin main", 
            "git status"
        ]
        
        print("Showing suggestions now...")
        display.show_suggestions(suggestions, "git")
        
        time.sleep(2)
        
        print("Hiding suggestions...")
        display.hide_suggestions()
        
        print("✓ Display test completed")
        return True
    except Exception as e:
        print(f"✗ Display error: {e}")
        return False

def test_simple_server():
    """Test simple server without engine"""
    print("Testing simple server...")
    try:
        from sugcommand.integrations.auto_suggest import AutoSuggestionServer, AutoSuggestionClient
        
        # Start server in background
        server = AutoSuggestionServer()
        server_thread = threading.Thread(target=server.start, daemon=True)
        server_thread.start()
        
        # Wait for server to start
        time.sleep(2)
        
        # Test client
        client = AutoSuggestionClient()
        suggestions = client.get_suggestions("git")
        
        if suggestions:
            print(f"✓ Server responded with suggestions: {suggestions}")
        else:
            print("⚠ Server responded but no suggestions")
        
        server.stop()
        print("✓ Server test completed")
        return True
    except Exception as e:
        print(f"✗ Server error: {e}")
        return False

def main():
    print("Simple SugCommand Auto-Suggestion Test")
    print("======================================")
    
    tests = [
        ("Basic Imports", test_basic_imports),
        ("Shell Integration", test_shell_integration),
        ("Terminal Display", test_display),
        ("Simple Server", test_simple_server)
    ]
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        success = test_func()
        if not success:
            print(f"❌ {test_name} failed, stopping here")
            break
        print(f"✅ {test_name} passed")
    
    print("\nTest completed!")

if __name__ == "__main__":
    main() 