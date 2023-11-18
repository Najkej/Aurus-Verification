How to Configure AurusVerification Bot
This guide is tailored for individuals who are not familiar with databases, server hosting, and related topics. Setting up requires knowledge of Python, Lua, and MySQL databases.

![image](https://github.com/Najkej/Aurus-Verification/assets/74835186/8ca76796-71f1-4e1a-bcff-4a33705a2e56)

Configuration Steps:

MySQL Database: Find your database hosting service; for budget projects, we recommend https://www.db4free.net/. Keep in mind that this is a free hosting service, so the database may not be entirely stable. Create 5 columns in the database: RobloxID (string), DiscordID (string), NickRoblox (string), NickDiscord (string), Verified (bool/boolean). Fill in this table; it will be useful later.
python
Copy code
host = "your-host"  # your host's domain address, e.g., db4free.net
user = "your-username"  # your database username
password = "your-password"  # your database user password
database = "your-database"  # your database name, e.g., "Users"
Discord Bot: Create a new bot on the Discord Developer Portal (https://discord.com/developers/applications). Make sure to include a mention of the original bot creator in the bot's description or provide a link to the project's GitHub! Copy your bot token and paste it into the last line of DiscordBot->main.py, replacing "Your_bot_token". Also, replace the table in lines 10-13 with the one you created during database hosting. In line 82, there is a command to add a verified role to the user; fill in the line with your role ID or remove it if you don't want to add a role. Hosting the bot can be done on various platforms, but there is no universal free hosting for it; I recommend paid alternatives.

API: Complete the database table in APIs->mainAPI.py, in lines 12-15. The API is designed to handle game queries on Roblox. A budget-friendly hosting option for the API could be Repl.it, but for a larger number of queries, I recommend other hosting services. Save the address where you host the API, as it will be needed for completing the setup in the Roblox game.

Roblox: The easiest part of the puzzle; fill in the API address in LuaScripts->CheckWhitelistByAPI.lua, on line 5. Upon successful verification, the player object should have attributes "DiscordNick" and "DiscordID."

If you encounter any issues with bot setup, feel free to contact us.
