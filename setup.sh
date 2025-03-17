#!/bin/bash
# filepath: setup.sh

echo "🚀 Setting up Records Management Documentation System"
echo "======================================================"

# Check for Python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Python is required but not installed. Please install Python 3 and try again."
    exit 1
fi

# Check for pip
if ! $PYTHON_CMD -m pip --version &> /dev/null; then
    echo "❌ pip is required but not installed. Please install pip and try again."
    echo "   You can install it with: sudo apt install python3-pip"
    exit 1
fi

# Create virtual environment properly
echo "📦 Creating Python virtual environment..."
if [ -d ".venv" ]; then
    echo "   Virtual environment directory exists but may be incomplete. Recreating..."
    rm -rf .venv
fi

$PYTHON_CMD -m venv .venv
if [ ! -f ".venv/bin/activate" ]; then
    echo "❌ Failed to create virtual environment. Please ensure you have the 'venv' module installed."
    echo "   You can install it with: sudo apt install python3-venv"
    exit 1
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source .venv/bin/activate
if [ $? -ne 0 ]; then
    echo "❌ Failed to activate virtual environment."
    exit 1
fi

# Verify we're using the virtual environment Python
VENV_PYTHON=$(which python)
echo "   Using Python at: $VENV_PYTHON"

# Fix requirements.txt if needed
echo "   Fixing requirements.txt format..."
if grep -q "^//" requirements.txt; then
    # Remove the filepath line and keep the rest
    sed -i '/^\/\//d' requirements.txt
fi

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies."
    exit 1
fi

# Generate config file
echo "⚙️ Generating configuration file..."
python document_processor.py --config

# Ask for key configuration values
if [ -f "config.yaml" ]; then
    echo "🔧 Would you like to update the configuration values now? (y/n)"
    read -r update_config
    
    if [[ $update_config == "y" || $update_config == "Y" ]]; then
        echo "Organization name (e.g., City of Springfield) [Your Organization]:"
        read -r org_name
        org_name=${org_name:-"Your Organization"}
        
        echo "State name (e.g., Washington) [Your State]:"
        read -r state_name
        state_name=${state_name:-"Your State"}
        
        echo "Department name (e.g., Records Management) [Records Management]:"
        read -r dept_name
        dept_name=${dept_name:-"Records Management"}
        
        echo "Contact email [records@example.gov]:"
        read -r email
        email=${email:-"records@example.gov"}
        
        # Use sed to update config values
        sed -i "s/organization_name: .*/organization_name: \"$org_name\"/" config.yaml
        sed -i "s/state_name: .*/state_name: \"$state_name\"/" config.yaml
        sed -i "s/department: .*/department: \"$dept_name\"/" config.yaml
        sed -i "s/contact_email: .*/contact_email: \"$email\"/" config.yaml
        echo "✅ Configuration updated."
    fi
fi

# Process documentation
echo "🔄 Processing documentation with your configurations..."
python document_processor.py

# Ask about HTML generation
echo "📄 Would you like to generate HTML files for SharePoint? (y/n)"
read -r generate_html
if [[ $generate_html == "y" || $generate_html == "Y" ]]; then
    python document_processor.py --html
fi

echo ""
echo "✅ Setup complete! Your documentation is now ready."
echo ""
echo "📝 Usage Tips:"
echo "---------------"
echo "1. Run 'source .venv/bin/activate' to activate the virtual environment"
echo "2. Run 'python document_processor.py' anytime you add new files"
echo "3. Run 'python document_processor.py --html' to generate SharePoint-ready HTML"
echo "4. Edit config.yaml to update your organization's information"

echo ""
echo "🌟 Happy documenting! 🌟"