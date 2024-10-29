import disnake
from disnake.ext import commands
import config

intents = disnake.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Бот запущен!")

@bot.event
async def on_member_join(member: disnake.Member):
    if getattr(config, "auto_role_enabled", False):
        auto_role = member.guild.get_role(config.auto_role_id)
        if auto_role:
            await member.add_roles(auto_role)

@bot.slash_command(name="action", guild_ids=[config.guild_id])
async def action(interaction: disnake.AppCmdInter, user: disnake.Member):
    command_role = interaction.guild.get_role(config.command_role_id)

    if command_role in interaction.author.roles:
        member = interaction.guild.get_member(user.id)
        unverified_role = interaction.guild.get_role(config.unverified_role_id)

        male_role = interaction.guild.get_role(config.male_role_id)
        female_role = interaction.guild.get_role(config.female_role_id)
        denied_role = interaction.guild.get_role(config.denied_role_id)

        if male_role in member.roles or female_role in member.roles or denied_role in member.roles:
            await interaction.response.send_message(embed=disnake.Embed(
                title="Ошибка",
                description=f"Пользователь {member.mention} уже верифицирован или недопущен!",
                color=disnake.Color.red()
            ), ephemeral=True)
            return

        if unverified_role in member.roles:
            embed = disnake.Embed(
                title="Выберите пол",
                description="",
                color=disnake.Color.blue()
            )
            buttons = [
                disnake.ui.Button(label="Мужской", style=disnake.ButtonStyle.secondary, emoji="♂️"),
                disnake.ui.Button(label="Женский", style=disnake.ButtonStyle.secondary, emoji="♀️"),
                disnake.ui.Button(label="Недопуск", style=disnake.ButtonStyle.red)
            ]

            action_row = disnake.ui.ActionRow(*buttons)
            await interaction.response.send_message(embed=embed, components=[action_row], ephemeral=True)

            button_interaction = await bot.wait_for("button_click", check=lambda i: i.user == interaction.user)

            if button_interaction.component.label == "Мужской":
                role = interaction.guild.get_role(config.male_role_id)
                await member.add_roles(role)
                await member.remove_roles(unverified_role)

                log_channel = interaction.guild.get_channel(config.log_channel_id)
                log_embed = disnake.Embed(
                    title="Верификация пользователя",
                    description=f"{button_interaction.user.mention} верифицировал {member.mention} как '♂️'.",
                    color=disnake.Color.blue()
                )
                await log_channel.send(embed=log_embed)

                await button_interaction.send("Пользователь успешно верифицирован!", ephemeral=True)

            elif button_interaction.component.label == "Женский":
                role = interaction.guild.get_role(config.female_role_id)
                await member.add_roles(role)
                await member.remove_roles(unverified_role)

                log_channel = interaction.guild.get_channel(config.log_channel_id)
                log_embed = disnake.Embed(
                    title="Верификация пользователя",
                    description=f"{button_interaction.user.mention} верифицировал {member.mention} как '♀️'.",
                    color=disnake.Color.from_rgb(255, 105, 180)
                )
                await log_channel.send(embed=log_embed)

                await button_interaction.send("Пользователь успешно верифицирован!", ephemeral=True)

            elif button_interaction.component.label == "Недопуск":
                modal = disnake.ui.Modal(
                    title="Причина недопуска",
                    custom_id="denial_reason",
                    components=[
                        disnake.ui.TextInput(
                            label="Введите причину",
                            placeholder="Причина недопуска...",
                            custom_id="reason_input",
                            style=disnake.TextInputStyle.paragraph
                        )
                    ]
                )

                await button_interaction.response.send_modal(modal)

                modal_interaction = await bot.wait_for("modal_submit", check=lambda
                    i: i.user == interaction.user and i.custom_id == modal.custom_id)

                reason = modal_interaction.text_values["reason_input"]
                await member.add_roles(denied_role)
                await modal_interaction.response.send_message("Пользователь был не допущен", ephemeral=True)

                log_channel = interaction.guild.get_channel(config.log_channel_id)
                log_embed = disnake.Embed(
                    title="Недопуск пользователя",
                    description=f"{button_interaction.user.mention} не допустил {member.mention}. Причина: {reason}",
                    color=disnake.Color.red()
                )
                await log_channel.send(embed=log_embed)

        else:
            await interaction.response.send_message(embed=disnake.Embed(
                title="Ошибка",
                description=f"У этого пользователя нет роли <@&{config.unverified_role_id}>!",
                color=disnake.Color.red()
            ), ephemeral=True)
    else:
        await interaction.response.send_message(embed=disnake.Embed(
            title="Ошибка",
            description="У вас нет прав на выполнение этой команды!",
            color=disnake.Color.red()
        ), ephemeral=True)

bot.run(config.token)
