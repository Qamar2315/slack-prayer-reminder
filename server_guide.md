## Server Deployment & Management Guide

This guide details how to manage the bot on the production Ubuntu server where it runs as a `systemd` service named `prayerbot.service`.

### Checking the Bot's Status

To check if the bot is running and see its most recent activity, use the following command:

```bash
sudo systemctl status prayerbot.service
```

-   Look for a green `active (running)` message.
-   This command also shows the last few log entries from the script.

### Viewing Live Logs

To see a real-time, continuous stream of the bot's log output (e.g., to see it fetch times or send a message), use:

```bash
sudo journalctl -u prayerbot.service -f
```

Press `Ctrl + C` to exit the live log view.

### Starting, Stopping, and Restarting the Bot

You will need to use these commands whenever you update the code or need to manually manage the service.

-   **To Stop the bot:**
    ```bash
    sudo systemctl stop prayerbot.service
    ```

-   **To Start the bot (if it was stopped):**
    ```bash
    sudo systemctl start prayerbot.service
    ```

-   **To Restart the bot (the most common command):**
    *You must run this after every code update to apply the changes.*
    ```bash
    sudo systemctl restart prayerbot.service
    ```

### How to Update the Bot's Code

Follow this workflow to safely update the bot with new code from the GitHub repository.

1.  **Log in to the server** via SSH.

2.  **Navigate to the project directory:**
    ```bash
    cd /opt/prayer_bot/slack-prayer-reminder
    ```

3.  **Pull the latest code** from GitHub:
    ```bash
    git pull
    ```

4.  **(If needed) Update dependencies:** If you added new packages to `requirements.txt`, you must activate the virtual environment and install them.
    ```bash
    source venv/bin/activate
    pip install -r requirements.txt
    deactivate
    ```

5.  **Restart the service** to make the new code active:
    ```bash
    sudo systemctl restart prayerbot.service
    ```

6.  **Verify the update:** Check the status to ensure the bot restarted without errors.
    ```bash
    sudo systemctl status prayerbot.service
    ```

### Initial Setup on a New Server (For future reference)

1.  **Clone the repository:**
    `git clone https://github.com/Qamar2315/slack-prayer-reminder.git /opt/prayer_bot/slack-prayer-reminder`
2.  **Create Python virtual environment:**
    `cd /opt/prayer_bot/slack-prayer-reminder`
    `python3 -m venv venv`
3.  **Install dependencies:**
    `source venv/bin/activate`
    `pip install -r requirements.txt`
    `deactivate`
4.  **Create the environment file:**
    `nano .env`
    And add your keys:
    ```env
    GEMINI_API_KEY="YOUR_GEMINI_KEY"
    SLACK_BOT_TOKEN="YOUR_SLACK_TOKEN"
    ```
5.  **Create and enable the systemd service:**
    `sudo nano /etc/systemd/system/prayerbot.service`
    (Paste the service file content from our setup)
    `sudo systemctl daemon-reload`
    `sudo systemctl start prayerbot.service`
    `sudo systemctl enable prayerbot.service`