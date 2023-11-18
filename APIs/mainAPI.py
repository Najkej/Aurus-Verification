from fastapi import FastAPI
import uvicorn

app = FastAPI()

import mysql.connector


@app.get("/api/robloxwhitelist/{robloxid}")
def index(robloxid: str):
    connection = mysql.connector.connect(
    host="your-host",
    user="your-username",
    password="your-password",
    database="your-database"
    )

    cursor = connection.cursor()

    cursor.execute(f"SELECT DiscordID, NickDiscord, Zweryfikowany FROM Users WHERE RobloxID = '{robloxid}';")

    results = cursor.fetchall()


    print(results)
    if results:
      
      return {'DiscordID' : results[0][0] ,
              "DiscordNick" : results[0][1],
              "Verified" : results[0][2]}
    else:
        return {"Not found"}

    cursor.close()
    connection.close()


if __name__ == "__main__":
  uvicorn.run(app,host="0.0.0.0")
