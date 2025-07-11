# Windsurf Credit Claimer

An automation script to claim credits on Windsurf using promotion codes.

## Features

- Automatically navigates to Windsurf website
- Clicks "Purchase Credit" button
- Handles Stripe payment page
- Enters promotion code "OPEN-SF"
- Fills in name (kendall) if field is empty
- Enters address "1200 market street"
- Completes the purchase
- Can run multiple times in sequence

## Prerequisites

1. **Python 3.7+** - Make sure Python is installed on your system
2. **Google Chrome** - The script uses Chrome browser for automation
3. **Internet connection** - Required to access Windsurf and Stripe

## Quick Start

### Option 1: Automatic Setup (Recommended)
```bash
python setup_and_run.py
```

### Option 2: Manual Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the script:
   ```bash
   python windsurf_credit_claimer.py
   ```

## Usage

1. Run the script using one of the methods above
2. When prompted, enter how many times you want to claim credits (default: 1)
3. The browser will open and automatically perform the credit claiming process
4. Watch the console output for progress updates

## Configuration

You can modify the script behavior by editing `windsurf_credit_claimer.py`:

- **Headless mode**: Set `headless=True` in the `WindsurfCreditClaimer()` initialization to run without opening a browser window
- **Wait times**: Adjust `time.sleep()` values if the script runs too fast for the website
- **Selectors**: Update the XPath selectors if the website structure changes

## Troubleshooting

### Common Issues

1. **Chrome not found**
   - Install Google Chrome from https://www.google.com/chrome/
   - Make sure Chrome is in your system PATH

2. **Elements not found**
   - The website structure may have changed
   - Try running in non-headless mode to see what's happening
   - Update the XPath selectors in the script

3. **Slow internet connection**
   - Increase the wait times in the script
   - The default timeout is 10 seconds, you can increase it

### Debug Mode

To run in debug mode (see the browser actions):
- Set `headless=False` in the script (this is the default)
- Watch the browser window to see what the script is doing

## Safety Notes

- This script is for educational purposes
- Make sure you comply with Windsurf's terms of service
- Use responsibly and don't abuse the promotion system
- The script includes delays to avoid overwhelming the servers

## Files

- `windsurf_credit_claimer.py` - Main automation script
- `setup_and_run.py` - Setup and run helper script
- `requirements.txt` - Python dependencies
- `README.md` - This documentation

## Support

If you encounter issues:
1. Check that all prerequisites are installed
2. Try running in non-headless mode to see what's happening
3. Check the console output for error messages
4. Make sure your internet connection is stable
