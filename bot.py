import discord
from data_manager import DataManager

class Bot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.data_manager = DataManager("data")

    def read_token(self):
        with open("token.txt", "r") as file:
            return file.read().strip()

    async def on_ready(self):
        print(f'Logged in as {self.user.name}')

    def run_bot(self):
        token = self.read_token()
        super().run(token)

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('!get_birthday'):
            server_id = str(message.guild.id)

            if len(message.mentions) == 1:
                user_id = str(message.mentions[0].id)
            else:
                user_id = str(message.author.id)
            
            server_data = self.data_manager.get_server_data(server_id)
            if server_data and user_id in server_data:
                birthday = server_data[user_id]
                await message.channel.send(f"<@{user_id}>'s birthday is: {birthday}")
            else:
                await message.channel.send(f"No birthday data found for <@{user_id}>.")            

        elif message.content.startswith('!set_birthday'):
            server_id = str(message.guild.id)

            if len(message.mentions) == 1:
                user_id = str(message.mentions[0].id)  
                user_input = message.content.split(' ', 2)[2] 
            else:
                user_id = str(message.author.id)
                user_input = message.content.split(' ', 1)[1]

            server_data = self.data_manager.get_server_data(server_id)
            if not server_data:
                self.data_manager.create_server_data(server_id, {user_id: user_input})
            else:
                server_data[user_id] = user_input
                self.data_manager.update_server_data(server_id, server_data)

            await message.channel.send(f"Data updated for <@{user_id}>: {user_input}")

        elif message.content.startswith('!delete_birthday'):
            server_id = str(message.guild.id)

            if len(message.mentions) == 1:
                user_id = str(message.mentions[0].id) 
            else:
                user_id = str(message.author.id)
            
            server_data = self.data_manager.get_server_data(server_id)
            if server_data and user_id in server_data:
                del server_data[user_id]
                self.data_manager.update_server_data(server_id, server_data)
                await message.channel.send(f"Data deleted successfully for <@{user_id}>.")
            else:
                await message.channel.send(f"No data found to delete for <@{user_id}>.")


if __name__ == "__main__":
    bot = Bot()
    bot.run_bot()