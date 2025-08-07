# GTD-5

A Python-based project for data processing.

## Setup Instructions

After cloning the repository, follow these steps to set up the project:

```bash
# Navigate to the project directory
cd GTD-5/

# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install required dependencies
pip install -r requirements.txt

# Deactivate the virtual environment when done with setup
deactivate
```

## Manual Execution

To run the project manually:

```bash
# Activate the virtual environment
source /home/net/x249581/GTD-5/.venv/bin/activate

# Navigate to the project directory
cd /home/net/x249581/GTD-5

# Run the main script
python main.py
```

### Command-line Arguments

The `main.py` script accepts the following command-line arguments:

1. `mode` - Execution mode:

   - `0` (default): Cron-triggered mode. Only runs on Sunday or Monday and processes files from the previous day.
   - `1`: Manual mode. Bypasses day-of-week restrictions and processes the specified group.

2. `group` - Site group to process (e.g., "w1_d7", "w2_d1", etc.):
   - Format: "w{week_number}\_d{day_number}" where day 7 = Saturday, day 1 = Sunday
   - Example groups: "w1_d7", "w1_d1", "w2_d7", "w2_d1", etc.

Examples:

```bash
# Run in manual mode to process week 1, Saturday sites
python main.py 1 w1_d7

# Run in manual mode to process week 2, Sunday sites
python main.py 1 w2_d1
```

When running in manual mode (mode=1), the script will process the specified group regardless of the current day of the week.

## Automated Execution via Cron Job

The project can be automatically executed using a cron job that runs the `gtd5.sh` script. This script:

1. Activates the virtual environment
2. Changes to the project directory
3. Runs the main Python script
4. Moves the output files to a designated directory

Here's the content of the `gtd5.sh` script:

```bash
# Activate the virtual environment
source /home/net/x249581/GTD-5/.venv/bin/activate

# Navigate to the project directory
cd /home/net/x249581/GTD-5

# Run the main script
python main.py

# Move output files to the destination directory
mv output/* /devops/projects/Customer_Count/Voice/GTD5
```

To set up a cron job to run this script automatically, you can use the `crontab -e` command and add an entry specifying when to run the script. For example, to run it daily at midnight:

```
0 0 * * * /path/to/gtd5.sh
```
