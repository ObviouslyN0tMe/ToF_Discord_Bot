from discord.ext import commands
import datetime

# emojis for reactions
emojis = ["1⃣", "2⃣", "3⃣", "4⃣", "5⃣"]


async def update_participants(message, bot):
    # check old message content
    msg_content = message.content.split("\n")
    msg_reactions = message.reactions
    # collect roles and roster ids
    surv_role = message.guild.get_role(1114665314362331156)
    killer_role = message.guild.get_role(1114665372919005265)
    surv_roster_ids = []
    for surv in surv_role.members:
        surv_roster_ids.append(surv.id)
    for reaction in msg_reactions:
        # create playerlists
        surv_list = []
        killer_list = []
        users = [user async for user in reaction.users()]
        users.remove(bot)
        for user in users:
            if user.id in surv_roster_ids:
                surv_list.append(user.display_name)
            else:
                killer_list.append(user.display_name)
        # make strings from lists
        surv_list_str = ""
        for surv in surv_list:
            surv_list_str += surv
            surv_list_str += ", "
        surv_list_str = " " + surv_list_str.strip(", ")
        killer_list_str = ""
        for killer in killer_list:
            killer_list_str += killer
            killer_list_str += ", "
        killer_list_str = " " + killer_list_str.strip(", ")
        # calc playercount
        surv_count = str(len(surv_list))
        killer_count = str(len(killer_list))
        # update lines in content
        surv_line_index = 3 * emojis.index(reaction.emoji) + 3
        killer_line_index = 3 * emojis.index(reaction.emoji) + 4
        msg_content[surv_line_index] = "(" + surv_count + ") " + surv_role.mention + surv_list_str
        msg_content[killer_line_index] = "(" + killer_count + ") " + killer_role.mention + killer_list_str
    # create new message
    new_msg_content = ""
    for line in msg_content:
        new_msg_content += line + "\n"
    # send message
    await message.edit(content=new_msg_content)


class Trainingdates(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        await ctx.send("läuft")

    @commands.command()
    async def neu(self, ctx, monday):
        # get monday date
        monday = monday.split(".")
        mon = datetime.date(int(monday[2]), int(monday[1]), int(monday[0]))
        # create all weekdates
        forward = datetime.timedelta(days=1)
        w = {"mon": mon.strftime("**%a (%d. %B)**"),
             "tue": (mon + 1*forward).strftime("**%a (%d. %B)**"),
             "wed": (mon + 2*forward).strftime("**%a (%d. %B)**"),
             "thu": (mon + 3*forward).strftime("**%a (%d. %B)**"),
             "fri": (mon + 4*forward).strftime("**%a (%d. %B)**"),
             "sat": (mon + 5*forward).strftime("**%a (%d. %B)**"),
             "sun": (mon + 6*forward).strftime("**%a (%d. %B)**")}
        # create message headers
        header_week = ":bar_chart:  **TRAINING DATES (8PM CET)**\n" + w["mon"] + " **-** " + w["fri"] + "\n"
        header_weekend = ":bar_chart:  **TRAINING DATES (CET)**\n" + w["sat"] + " **-** " + w["sun"] + "\n"
        # create timeslots
        dates_week = [emojis[0] + w["mon"] + "\n",
                      emojis[1] + w["tue"] + "\n",
                      emojis[2] + w["wed"] + "\n",
                      emojis[3] + w["thu"] + "\n",
                      emojis[4] + w["fri"] + "\n"]
        dates_weekend = [emojis[0] + w["sat"] + " **3PM **\n", emojis[1] + w["sat"] + " **8PM**\n",
                         emojis[2] + w["sun"] + " **3PM**\n", emojis[3] + w["sun"] + " **8PM**\n"]
        # get roles to ping
        surv_role = ctx.guild.get_role(1114665314362331156)
        killer_role = ctx.guild.get_role(1114665372919005265)
        # create message for week
        message_week = header_week
        for timeslot in dates_week:
            message_week += timeslot
            message_week += "(0) " + surv_role.mention + "\n"
            message_week += "(0) " + killer_role.mention + "\n"
        # create message for weekend
        message_weekend = header_weekend
        for timeslot in dates_weekend:
            message_weekend += timeslot
            message_weekend += "(0) " + surv_role.mention + "\n"
            message_weekend += "(0) " + killer_role.mention + "\n"
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
            await update_participants(message, self.bot.user)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        # check if reaction is from bot
        if payload.user_id == self.bot.user.id:
            return
        # check if message is from bot
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        if message.author.id == self.bot.user.id:
            await update_participants(message, self.bot.user)


async def setup(bot):
    await bot.add_cog(Trainingdates(bot))
