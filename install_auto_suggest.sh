#!/bin/bash

echo "🚀 SugCommand Auto-Suggestion Installer"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check Python version
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
if [[ $(echo "$python_version < 3.8" | bc -l) -eq 1 ]]; then
    echo "❌ Python $python_version detected. Python 3.8+ is required."
    exit 1
fi

echo "✅ Python $python_version detected"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed"

# Install the package
echo ""
echo "📦 Installing SugCommand..."
pip3 install -e .

if [ $? -ne 0 ]; then
    echo "❌ Failed to install SugCommand"
    exit 1
fi

echo "✅ SugCommand installed"

# Create shell integration files
echo ""
echo "⚙️ Setting up shell integration..."
python3 -c "
import sys
sys.path.insert(0, 'src')
from sugcommand.integrations.auto_suggest import create_shell_integration
config_dir = create_shell_integration()
print(f'✅ Shell integration files created in: {config_dir}')
"

# Detect current shell
current_shell=$(basename "$SHELL")
echo ""
echo "🔍 Detected shell: $current_shell"

# Add to shell config based on detected shell
if [[ "$current_shell" == "bash" ]]; then
    config_file="$HOME/.bashrc"
    source_line="source ~/.config/sugcommand/bash_auto_suggest.sh"
    
    if ! grep -q "bash_auto_suggest.sh" "$config_file" 2>/dev/null; then
        echo "" >> "$config_file"
        echo "# SugCommand Auto-Suggestion" >> "$config_file"
        echo "$source_line" >> "$config_file"
        echo "✅ Added to $config_file"
    else
        echo "⚠️  Already configured in $config_file"
    fi
    
elif [[ "$current_shell" == "zsh" ]]; then
    config_file="$HOME/.zshrc"
    source_line="source ~/.config/sugcommand/zsh_auto_suggest.zsh"
    
    if ! grep -q "zsh_auto_suggest.zsh" "$config_file" 2>/dev/null; then
        echo "" >> "$config_file"
        echo "# SugCommand Auto-Suggestion" >> "$config_file"
        echo "$source_line" >> "$config_file"
        echo "✅ Added to $config_file"
    else
        echo "⚠️  Already configured in $config_file"
    fi
    
else
    echo "⚠️  Unsupported shell: $current_shell"
    echo "    Please manually add the source line to your shell config:"
    echo "    For Bash: source ~/.config/sugcommand/bash_auto_suggest.sh"
    echo "    For Zsh:  source ~/.config/sugcommand/zsh_auto_suggest.zsh"
fi

# Start the daemon
echo ""
echo "🚀 Starting auto-suggestion daemon..."
python3 -c "
import sys
import threading
import time
sys.path.insert(0, 'src')
from sugcommand.integrations.auto_suggest import AutoSuggestionServer

server = AutoSuggestionServer()
server_thread = threading.Thread(target=server.start, daemon=True)
server_thread.start()

print('✅ Auto-suggestion daemon started')
print('   Socket: ~/.config/sugcommand/auto_suggest.sock')

# Keep daemon running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print('\\n🛑 Daemon stopped')
    server.stop()
" &

daemon_pid=$!
echo "✅ Daemon started with PID: $daemon_pid"

# Save PID for later management
mkdir -p ~/.config/sugcommand
echo $daemon_pid > ~/.config/sugcommand/auto_suggest.pid

echo ""
echo "🎉 Installation Complete!"
echo "========================"
echo ""
echo "Next steps:"
echo "1. Restart your shell: exec \$SHELL"
echo "2. Start typing commands and see suggestions appear!"
echo ""
echo "Examples:"
echo "  git c    → git commit, git config, git checkout..."
echo "  docker r → docker run, docker restart, docker rm..."
echo "  npm i    → npm install, npm init, npm info..."
echo ""
echo "🔧 Management commands:"
echo "  python demo_auto_suggest.py  # Run demo and tests"
echo "  kill $daemon_pid             # Stop daemon"
echo "  ps aux | grep auto_suggest   # Check daemon status"
echo ""
echo "📖 For more info, see: SETUP_AUTO_SUGGEST.md" 