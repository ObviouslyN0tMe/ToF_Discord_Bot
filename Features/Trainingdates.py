from discord.ext import commands
import datetime

# emojis for reactions
emojis = ["1⃣", "2⃣", "3⃣", "4⃣", "5⃣"]


class Trainingdates(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def neueWoche(self, ctx, monday):
        # get monday date
        monday = monday.split(".")
        mon = datetime.date(int(monday[2]), int(monday[1]), int(monday[0]))
        # create all weekdates
        forward = datetime.timedelta(days=1)
        w = {"mon": mon.strftime("%a %d.%m"),
             "tue": (mon + 1*forward).strftime("%a %d.%m"),
             "wed": (mon + 2*forward).strftime("%a %d.%m"),
             "thu": (mon + 3*forward).strftime("%a %d.%m"),
             "fri": (mon + 4*forward).strftime("%a %d.%m"),
             "sat": (mon + 5*forward).strftime("%a %d.%m"),
             "sun": (mon + 6*forward).strftime("%a %d.%m")}
        # create message headers
        header_week = ":bar_chart:  TRAINING DATES  " + w["mon"] + " - " + w["fri"] + "\n"
        header_weekend = ":bar_chart:  TRAINING DATES  " + w["sat"] + " - " + w["sun"] + "\n"
        # create timeslots
        dates_week = [emojis[0] + w["mon"] + " 8PM\n",
                      emojis[1] + w["tue"] + " 8PM\n",
                      emojis[2] + w["wed"] + " 8PM\n",
                      emojis[3] + w["thu"] + " 8PM\n",
                      emojis[4] + w["fri"] + " 8PM\n"]
        dates_weekend = [emojis[0] + w["sat"] + " 3PM\n", emojis[1] + w["sat"] + " 8PM\n",
                         emojis[2] + w["sun"] + " 3PM\n", emojis[3] + w["sun"] + " 8PM\n"]
        # create message for week
        message_week = header_week
        for timeslot in dates_week:
            message_week += timeslot
            message_week += "(0)\n"
        # create message for weekend
        message_weekend = header_weekend
        for timeslot in dates_weekend:
            message_weekend += timeslot
            message_weekend += "(0)\n"
        # send messages and add reactions
        await ctx.send(message_week)
        msg_id = ctx.channel.last_message_id
        msg = ctx.channel.get_partial_message(msg_id)
        for i in range(len(dates_week)):
            await msg.add_reaction(emojis[i])
        await ctx.send(message_weekend)
        msg_id = ctx.channel.last_message_id
        msg = ctx.channel.get_partial_message(msg_id)
        for i in range(len(dates_weekend)):
            await msg.add_reaction(emojis[i])

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # check if reaction is from bot
        if payload.user_id == self.bot.user.id:
            return
        # check if message is from bot
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        if message.author.id == self.bot.user.id:
            # check old message content
            message_content = message.content.split("\n")
            line_to_edit_index = 2*emojis.index(payload.emoji.name) + 2
            line_to_edit = message_content[line_to_edit_index]
            line_to_edit = line_to_edit.split(")")
            # update playercount and player list
            playercount = str(int(line_to_edit[0].strip("(")) + 1)
            line_to_edit[1] = line_to_edit[1].strip(" ")
            player_list = line_to_edit[1].split(", ")
            player_to_add = self.bot.get_user(payload.user_id)
            player_list.append(player_to_add.display_name)
            # create new strings
            player_list_str = ""
            for player in player_list:
                player_list_str += player
                player_list_str += ", "
            player_list_str = player_list_str.strip(", ")
            line_edited = "(" + playercount + ") " + str(player_list_str)
            message_content[line_to_edit_index] = line_edited
            new_msg_content = ""
            for line in message_content:
                new_msg_content += line
                new_msg_content += "\n"
            # send message
            await message.edit(content=new_msg_content)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        # check if reaction is from bot
        if payload.user_id == self.bot.user.id:
            return
        # check if message is from bot
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        if message.author.id == self.bot.user.id:
            # check old message content
            message_content = message.content.split("\n")
            line_to_edit_index = 2 * emojis.index(payload.emoji.name) + 2
            line_to_edit = message_content[line_to_edit_index]
            line_to_edit = line_to_edit.split(")")
            # update playercount and player list
            playercount = str(int(line_to_edit[0].strip("(")) + -1)
            line_to_edit[1] = line_to_edit[1].strip(" ")
            player_list = line_to_edit[1].split(", ")
            player_to_remove = self.bot.get_user(payload.user_id)
            player_list.remove(player_to_remove.display_name)
            # create new strings
            player_list_str = ""
            for player in player_list:
                player_list_str += player
                player_list_str += ", "
            player_list_str = player_list_str.strip(", ")
            line_edited = "(" + playercount + ") " + str(player_list_str)
            message_content[line_to_edit_index] = line_edited
            new_msg_content = ""
            for line in message_content:
                new_msg_content += line
                new_msg_content += "\n"
            # send message
            await message.edit(content=new_msg_content)


async def setup(bot):
    await bot.add_cog(Trainingdates(bot))