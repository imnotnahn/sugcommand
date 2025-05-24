#!/usr/bin/env python3
"""
Demo script for SugCommand library.

This script demonstrates the main features of the sugcommand library
including command suggestions, configuration, and performance monitoring.
"""

import time
import sys
from pathlib import Path

# Add src to path for demo
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sugcommand import SuggestionEngine, ConfigManager
from sugcommand.utils.display import SuggestionFormatter, ColorScheme
from sugcommand.utils.performance import get_performance_summary, timer


def demo_basic_suggestions():
    """Demo basic command suggestions."""
    print("🔍 Demo: Basic Command Suggestions")
    print("=" * 50)
    
    # Initialize components
    config = ConfigManager()
    engine = SuggestionEngine(config)
    formatter = SuggestionFormatter(
        color_enabled=True,
        show_confidence=True,
        show_source=True
    )
    
    # Demo queries
    queries = ["git", "apt", "docker", "npm", "py"]
    
    for query in queries:
        print(f"\nQuery: '{query}'")
        print("-" * 30)
        
        with timer(f"suggestion_{query}"):
            suggestions = engine.get_suggestions(query)
        
        if suggestions:
            output = formatter.format_suggestions(
                suggestions[:5],  # Limit to 5 for demo
                title=f"Top suggestions for '{query}'",
                highlight_text=query
            )
            print(output)
        else:
            print(formatter.format_warning(f"No suggestions found for '{query}'"))
        
        print()


def demo_configuration():
    """Demo configuration management."""
    print("⚙️ Demo: Configuration Management")
    print("=" * 50)
    
    config = ConfigManager()
    formatter = SuggestionFormatter()
    
    # Show current config
    print("Current configuration:")
    summary = config.get_config_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    print("\n" + formatter.format_success("Configuration loaded successfully!"))
    
    # Demo config changes
    print(f"\nOriginal max_suggestions: {config.get_max_suggestions()}")
    
    config.set_max_suggestions(15)
    print(f"Updated max_suggestions: {config.get_max_suggestions()}")
    
    # Reset to original
    config.set_max_suggestions(10)
    print(f"Reset max_suggestions: {config.get_max_suggestions()}")


def demo_performance():
    """Demo performance monitoring."""
    print("📊 Demo: Performance Monitoring")
    print("=" * 50)
    
    config = ConfigManager()
    engine = SuggestionEngine(config)
    
    # Warm up the engine
    print("Warming up engine...")
    engine.warm_up()
    
    # Run some queries to generate metrics
    queries = ["ls", "cd", "grep", "find", "vim"]
    
    print(f"\nRunning {len(queries)} queries for performance testing...")
    start_time = time.time()
    
    for query in queries:
        suggestions = engine.get_suggestions(query)
        print(f"  {query}: {len(suggestions)} suggestions")
    
    total_time = time.time() - start_time
    print(f"\nTotal time: {total_time:.3f}s")
    print(f"Average per query: {total_time/len(queries):.3f}s")
    
    # Show performance summary
    print("\nPerformance Summary:")
    perf_summary = get_performance_summary()
    for key, value in perf_summary.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.3f}")
        else:
            print(f"  {key}: {value}")


def demo_color_schemes():
    """Demo different color schemes."""
    print("🎨 Demo: Color Schemes")
    print("=" * 50)
    
    config = ConfigManager()
    engine = SuggestionEngine(config)
    
    suggestions = engine.get_suggestions("git")[:3]
    
    if not suggestions:
        print("No suggestions available for color demo")
        return
    
    schemes = [
        (ColorScheme.DEFAULT, "Default Theme"),
        (ColorScheme.DARK, "Dark Theme"),
        (ColorScheme.LIGHT, "Light Theme"),
        (ColorScheme.MINIMAL, "Minimal Theme"),
    ]
    
    for scheme, name in schemes:
        print(f"\n{name}:")
        print("-" * 20)
        
        formatter = SuggestionFormatter(
            color_scheme=scheme,
            show_confidence=True,
            show_source=True
        )
        
        output = formatter.format_suggestions(
            suggestions,
            title=f"Git suggestions ({name.lower()})",
            highlight_text="git"
        )
        print(output)


def demo_engine_stats():
    """Demo engine statistics."""
    print("📈 Demo: Engine Statistics")
    print("=" * 50)
    
    config = ConfigManager()
    engine = SuggestionEngine(config)
    formatter = SuggestionFormatter()
    
    # Get engine stats
    stats = engine.get_engine_stats()
    
    # Format and display
    output = formatter.format_stats(stats)
    print(output)


def main():
    """Run all demos."""
    print("🚀 SugCommand Library Demo")
    print("=" * 60)
    print()
    
    demos = [
        demo_basic_suggestions,
        demo_configuration,
        demo_performance,
        demo_color_schemes,
        demo_engine_stats,
    ]
    
    for i, demo_func in enumerate(demos, 1):
        try:
            demo_func()
            
            if i < len(demos):
                print("\n" + "="*60 + "\n")
                input("Press Enter to continue to next demo...")
                print()
                
        except KeyboardInterrupt:
            print("\n\nDemo interrupted by user.")
            break
        except Exception as e:
            print(f"\nError in demo: {e}")
            continue
    
    print("\n🎉 Demo completed! Thank you for trying SugCommand!")


if __name__ == "__main__":
    main() 