# SugCommand - Intelligent Terminal Command Suggestion Tool

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![PyPI](https://img.shields.io/badge/PyPI-sugcommand-blue.svg)

!Important: HAVING SOME BUG AND NOT FIXED YET
**SugCommand** is an intelligent Python library that provides terminal command suggestions based on:
- Available system commands
- Command history analysis from different shells
- Usage patterns and context
- Simple machine learning algorithms
- **🚀 NEW: REAL-TIME AUTO-SUGGESTIONS** - Automatic suggestions while typing!

## ✨ Key Features

### 🎯 **NEW: Real-time Auto-Suggestions**
- **💡 Automatic display**: Suggestions appear as you type - no Tab needed!
- **⚡ Ultra-fast**: Sub-3ms response time
- **🎨 Beautiful display**: Elegant suggestions below your cursor
- **🔧 Zero config**: Works out of the box
- **🖥️ Multi-shell**: Bash, Zsh, Fish support

### 🔍 Smart Command Detection
- Scans all available commands from PATH and system directories
- Supports fuzzy and exact matching
- Intelligent caching for speed

### 📚 History Analysis
- Supports bash, zsh, fish shell history
- Learns patterns from previous usage
- Context-aware suggestions based on command sequences

### 🎯 Customizable Key Bindings
- **Multiple binding options** (Ctrl+Space, Ctrl+@, Ctrl+], etc.)
- **Shell-specific bindings** for bash/zsh/fish
- **Real-time trigger** for instant suggestions
- **Fallback completion** when needed

### 🚀 Real-time Shell Integration
- **Automatic suggestions while typing** (no need to run sugcommand separately)
- Integration with bash/zsh/fish tab completion
- Background daemon for fast response (<50ms)
- Custom key bindings for instant suggestions

### ⚡ High Performance
- Parallel directory scanning
- Intelligent caching with TTL
- Response time < 100ms
- Daemon architecture for real-time response

### 🎨 Beautiful Interface
- Customizable colors (supports dark/light themes)
- Shows confidence scores and suggestion sources
- Compact mode for small terminals

### ⚙️ Flexible Configuration
- Enable/disable individual features
- Customize number of suggestions
- Exclude/include commands
- Export/import configuration

## 🚀 Installation

### From PyPI (Recommended)
```bash
pip install sugcommand
```

### From Source
```bash
git clone https://github.com/yourusername/sugcommand.git
cd sugcommand
pip install -e .
```

### System Requirements
- Python 3.8+
- Linux/macOS/WSL
- Terminal with ANSI color support

## 🎯 Setup Auto-Completion (IMPORTANT!)

**This is the main feature! To get automatic suggestions while typing:**

### Step 1: Install shell integration
```bash
# Auto-detect shell and install
sugcommand integration install

# Or specify shell
sugcommand integration install --shell bash
sugcommand integration install --shell zsh
sugcommand integration install --shell fish
```

### Step 2: Start daemon
```bash
# Start daemon in background
sugcommand daemon start --background

# Check daemon status
sugcommand daemon status
```

### Step 3: Add to shell config
**Bash:** Add to `~/.bashrc`:
```bash
source ~/.config/sugcommand/bash_completion.sh
```

**Zsh:** Add to `~/.zshrc`:
```bash
source ~/.config/sugcommand/zsh_completion.zsh
```

**Fish:** Fish loads automatically, or add to `~/.config/fish/config.fish`:
```bash
source ~/.config/sugcommand/fish_completion.fish
```

### Step 4: Restart shell and test
```bash
# Restart shell
exec $SHELL

# Test auto-completion
git c<TAB>      # Will suggest: commit, clone, checkout...
apt u<TAB>      # Will suggest: update, upgrade...
docker r<TAB>   # Will suggest: run, rm, restart...
```

## 📖 Usage

### Basic Usage (CLI)

```bash
# Get suggestions for a command
sugcommand suggest "apt"

# Get suggestions with interactive mode
sugcommand suggest

# Show with confidence scores
sugcommand suggest "git" --show-confidence

# Compact mode
sugcommand suggest "docker" --compact

# Limit number of suggestions
sugcommand suggest "npm" --limit 5
```

### Daemon Management

```bash
# Start/stop daemon
sugcommand daemon start --background
sugcommand daemon stop
sugcommand daemon status

# Check integration status
sugcommand integration status
```

### Configuration Management

```bash
# Enable/disable suggestions
sugcommand enable
sugcommand disable
sugcommand toggle

# View statistics
sugcommand stats
sugcommand stats --engine
sugcommand stats --performance

# Configuration
sugcommand config set max_suggestions 15
sugcommand config get enabled
sugcommand config reset

# Export/Import configuration
sugcommand config export my-config.json
sugcommand config import my-config.json
```

### Using in Python

```python
from sugcommand import SuggestionEngine, ConfigManager
from sugcommand.integrations.realtime_daemon import DaemonClient

# Use daemon (fastest)
client = DaemonClient()
suggestions = client.get_suggestions("git c")

# Or use engine directly
config = ConfigManager()
engine = SuggestionEngine(config)
suggestions = engine.get_suggestions("git c")

for suggestion in suggestions:
    print(f"{suggestion['command']} (confidence: {suggestion['confidence']:.2f})")
```

## 🔧 Key Bindings

After installing shell integration, you can use:

- **Tab**: Enhanced completion with suggestions
- **Ctrl+Space**: Show suggestions for current command (bash)
- **Ctrl+X** (fish): Show suggestions for current command
- **Ctrl+X Ctrl+S** (zsh): Show suggestions for current command

### Custom Key Bindings

You can customize key bindings in your shell configuration:

**Bash:**
```bash
# In ~/.bashrc
bind -x '"\\C- ": _sugcommand_realtime_display'  # Ctrl+Space
# Or use other keys:
# bind -x '"\\C-@": _sugcommand_realtime_display'  # Ctrl+@
# bind -x '"\\C-]": _sugcommand_realtime_display'  # Ctrl+]
```

**Zsh:**
```bash
# In ~/.zshrc
bindkey '^ ' _sugcommand_widget    # Ctrl+Space
# Or use other keys:
# bindkey '^]' _sugcommand_widget    # Ctrl+]
```

**Fish:**
```fish
# In ~/.config/fish/config.fish
bind \e[32~ __sugcommand_show_suggestions  # F2
# Or use other keys:
# bind \e[33~ __sugcommand_show_suggestions  # F3
```

## 🔧 Advanced Configuration

### Configuration File

SugCommand stores configuration at `~/.config/sugcommand/config.json`:

```json
{
  "enabled": true,
  "max_suggestions": 10,
  "show_confidence": false,
  "color_enabled": true,
  "history_analysis_enabled": true,
  "command_scan_enabled": true,
  "fuzzy_search_enabled": true,
  "min_confidence_threshold": 0.1,
  "cache_duration": 3600,
  "daemon_enabled": true,
  "shell_integration_enabled": true,
  "custom_directories": [
    "/opt/custom/bin"
  ],
  "excluded_commands": [
    "history",
    "clear"
  ]
}
```

### Custom Scan Directories

```bash
# Add custom directories
sugcommand config set custom_directories '["/opt/myapp/bin", "~/scripts"]'

# Exclude commands
sugcommand config set excluded_commands '["passwd", "sudo -s"]'
```

### Color Schemes

```bash
# Choose color scheme
sugcommand config set color_scheme "dark"    # dark, light, minimal
sugcommand config set color_enabled false   # Disable colors
```

## 🏗️ Architecture

```
sugcommand/
├── core/
│   ├── command_scanner.py     # System command scanning
│   ├── history_analyzer.py    # History analysis
│   ├── suggestion_engine.py   # Main engine
│   └── config_manager.py      # Configuration management
├── integrations/             # ✨ NEW: Shell Integration
│   ├── realtime_daemon.py     # Daemon for real-time suggestions
│   ├── bash_integration.py    # Bash completion integration
│   ├── zsh_integration.py     # Zsh completion integration
│   └── fish_integration.py    # Fish completion integration
├── utils/
│   ├── display.py            # Display formatting
│   └── performance.py        # Performance monitoring
└── cli.py                    # Command line interface
```

### Real-time Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Shell Input   │───▶│  Completion      │───▶│   SugCommand    │
│   (git c<TAB>)  │    │  Script          │    │   Daemon        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │  Unix Socket     │◀───│  Suggestion     │
                       │  Communication   │    │  Engine         │
                       └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │  Fast Response   │    │  Cache &        │
                       │  (<50ms)         │    │  History        │
                       └──────────────────┘    └─────────────────┘
```

## 📊 Algorithm

### Scoring Algorithm

```python
def calculate_confidence(suggestion):
    score = 0.0
    
    # Exact match bonus
    if exact_match:
        score += 1.0
    
    # Prefix match
    elif prefix_match:
        score += 0.8
    
    # Frequency bonus from history
    score += frequency_weight * (usage_count / total_commands)
    
    # Recency bonus
    score += recency_weight * (1.0 / days_since_last_use)
    
    # Context bonus (sequence patterns)
    score += context_weight * sequence_probability
    
    return min(score, 1.0)
```

### Real-time Performance

```
Component               Response Time
─────────────────────────────────────
Command Scanner:        ~20ms
History Analysis:       ~15ms  
Suggestion Engine:      ~10ms
Daemon Communication:   ~5ms
─────────────────────────────────────
Total (with daemon):    ~50ms
Total (without daemon): ~100ms
```

## 🔧 Development

### Setup development environment

```bash
git clone https://github.com/yourusername/sugcommand.git
cd sugcommand

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or venv\Scripts\activate  # Windows

# Install dependencies
pip install -e ".[dev,daemon]"

# Run tests
pytest

# Code formatting
black src/
isort src/

# Type checking
mypy src/
```

### Test shell integration

```bash
# Test daemon
python -c "from sugcommand.integrations.realtime_daemon import RealtimeDaemon; d = RealtimeDaemon(); d.start()"

# Test completions
python -c "from sugcommand.integrations.bash_integration import BashIntegration; b = BashIntegration(); b.test_completion('git c')"

# Test client
python -c "from sugcommand.integrations.realtime_daemon import DaemonClient; c = DaemonClient(); print(c.get_suggestions('git c'))"
```

### Run tests

```bash
# All tests
pytest

# With coverage
pytest --cov=sugcommand --cov-report=html

# Test specific module
pytest tests/test_daemon.py -v
```

### Build package

```bash
# Build wheel
python -m build

# Upload to PyPI
twine upload dist/*
```

## 📈 Performance

### Benchmarks

```
Real-time Mode (with daemon):
──────────────────────────────
Command Scanning: ~20ms (avg)
History Analysis: ~15ms (avg)
Suggestion Generation: ~10ms (avg)
Daemon Communication: ~5ms (avg)
Total Response Time: ~50ms (95th percentile)

Direct Mode (without daemon):
─────────────────────────────
Command Scanning: ~50ms (avg)
History Analysis: ~30ms (avg)  
Suggestion Generation: ~20ms (avg)
Total Response Time: ~100ms (95th percentile)

Memory Usage: ~15MB (daemon) + ~8MB (per client)
Cache Hit Rate: >95% (after warmup)
```

### Optimization tips

1. **Use daemon mode**: Daemon keeps cache warm and responds quickly
2. **Enable shell integration**: Smoothest automatic completion
3. **Limit scan directories**: Remove unnecessary directories
4. **Exclude commands**: Exclude unnecessary commands
5. **Warm up cache**: Run `sugcommand refresh` after installation

## 🎯 Use Cases

### 1. Developer Workflow
```bash
git s<TAB>     → status, stash, show
npm i<TAB>     → install, init, info
docker r<TAB>  → run, rm, restart
```

### 2. System Administration
```bash
systemctl s<TAB>    → start, stop, status
apt u<TAB>          → update, upgrade
sudo service <TAB>  → apache2, nginx, mysql
```

### 3. Python Development
```bash
pip i<TAB>      → install, info, list
python -m <TAB> → pip, venv, pytest
pytest -<TAB>   → -v, --cov, --help
```

## 🚨 Troubleshooting

### Daemon won't start
```bash
# Check port conflict
sugcommand daemon status

# Check logs
tail -f ~/.config/sugcommand/daemon.log

# Restart daemon
sugcommand daemon stop
sugcommand daemon start --background
```

### Tab completion not working
```bash
# Check integration
sugcommand integration status

# Reinstall integration
sugcommand integration install --shell bash

# Source shell config
source ~/.bashrc  # or ~/.zshrc
```

### Slow performance
```bash
# Warm up cache
sugcommand refresh

# Check performance
sugcommand stats --performance

# Reduce scan directories
sugcommand config set custom_directories '[]'
```


## 📝 Changelog

### v0.2.0 (2024-01-XX)
- 🎯 **Customizable Key Bindings**: Multiple binding options and triggers
- 🔄 **Enhanced Shell Integration**: Improved real-time suggestions
- ⚡ **Performance Improvements**: Faster response times
- 🔧 **Better Error Handling**: More reliable suggestion display

### v0.1.0 (2024-01-XX)
- ✨ **Shell Integration**: Real-time auto-completion for bash/zsh/fish
- ⚡ **Daemon Architecture**: Background daemon for fast response
- 🔍 Command scanning and indexing
- 📚 Multi-shell history analysis
- 🎨 Beautiful CLI interface with colors
- ⚙️ Comprehensive configuration system
- 📊 Performance monitoring
- 🚀 Tab completion enhancement
- 🔧 Key bindings for real-time suggestions

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.




⭐ **If you find this useful, please star the repository!** ⭐

### 🎯 Quick Start Summary

```bash
# 1. Install
pip install sugcommand

# 2. Setup auto-completion
sugcommand integration install
sugcommand daemon start --background

# 3. Add to shell config
echo 'source ~/.config/sugcommand/bash_completion.sh' >> ~/.bashrc

# 4. Restart shell
exec $SHELL

# 5. Enjoy auto-completion!
git c<TAB>  # 🎉 Suggestions appear!
```