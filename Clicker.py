import discord
import sqlite3
import datetime
import os
import random

from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

con = sqlite3.connect("clicker.db")
cur = con.cursor()

click = 1
clicks_per_click = 1

# Create table if doesn't exist
cur.execute(f"""
            SELECT name 
            FROM sqlite_master 
            WHERE type='table' AND name= 'clicker'
            """)

if cur.fetchone():
    print(f"the table clicker already exist")

else:
    print(f"creating table clicker")

    cur.execute("CREATE TABLE clicker(user_id INTEGER, user_name TEXT, clicks INTEGER, date DATE, clicks_per_click INTEGER, PRIMARY KEY(user_id))")
        
    print(f"table clicker created")

class ClickerGame(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=0)
        self.cliques = 0

    def create_user(self, user_id, user_name, click, date, clicks_per_click):
        print(f"user: {user_name} | date: {date}")

        cur.execute(f"""
                    INSERT INTO clicker (user_id, user_name, clicks, date, clicks_per_click)
                    VALUES ({user_id}, '{user_name}', {click}, '{date}', {clicks_per_click})""")
        con.commit()

    def check_user(self, user_id):
        cur.execute(f"""
                    SELECT *
                    FROM clicker
                    WHERE user_id = '{user_id}'
                    """)
        return cur.fetchone()
    
    def update_clicks(self, user_id, click, date):
        cur.execute(f"""
                    UPDATE clicker
                    SET clicks = clicks + {click}, date = '{date}'
                    WHERE user_id = '{user_id}'
                    RETURNING clicks
                    """)
        
        resultado = cur.fetchone()
        
        con.commit()

        return resultado[0]
    
    def check_user_clicks(self, user_id):
        cur.execute(f"""
                    SELECT clicks_per_click
                    FROM clicker
                    WHERE user_id = '{user_id}'
                    """)
        return cur.fetchone()
    
    @discord.ui.button(label="Click", style=discord.ButtonStyle.blurple)
    async def click_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        user_name = interaction.user.display_name
        date = datetime.datetime.now().strftime("%d/%m/%Y %X")
        clicks_per_click = 1
        
        bonus = False

        achou = self.check_user(user_id)

        if achou:
            clicks_per_click = self.check_user_clicks(user_id)[0]
            click = clicks_per_click
            
            if random.random() < 0.05:
                bonus = True
                click = clicks_per_click + random.randint(1, 10)

                await interaction.response.send_message(f"{user_name}, You got blessed with {click} clicks", ephemeral=True)

            print(f"updating user record")

            resultado = self.update_clicks(user_id, click, date)

            print(f"user: {user_name} | clicks: {resultado} | date: {date}")

        else:
            print(f"creating user record")

            self.create_user(user_id, user_name, click, date, clicks_per_click)

            print(f"user record created")

        if not bonus:
            await interaction.response.defer()

@bot.command()
async def clicker(ctx):
    view = ClickerGame()
    await ctx.send(" ", view=view)


@bot.command()
async def board(ctx):
    cur.execute(f"""
                SELECT user_name, clicks
                FROM clicker
                ORDER BY clicks DESC
                """)
    
    resultado = cur.fetchall()

    if resultado:
        board_message = "Leaderboard:\n"

        for index, (user_name, clicks) in enumerate(resultado, start=1):
            board_message += f"{index}. {user_name} - {clicks} clicks\n"

    else:
        board_message = "No clicks recorded"

    await ctx.send(board_message)

bot.run(os.getenv("TOKEN"))
