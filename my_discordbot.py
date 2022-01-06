#-------------------------------------------------------------------------------
# Name:         My_DiscordBot
# Purpose:      個人用のDiscordBot
#
# Author:       Shaneron
#
# Created:      2021/12/27
# Copyright:    (c) Shaneron 2021
#-------------------------------------------------------------------------------

def main():
    JSON_PATH = "data_file.json"

    try:
        import discord
        from discord.ext import commands
        import datetime

        jsons = read_json(JSON_PATH)

        token = jsons[0]
        ROOM_ID = int(jsons[1])
        COMMAND_ROOM_ID = int(jsons[2])

        PREFIX = '&'

        bot = commands.Bot(command_prefix=PREFIX)

        #起動時の処理
        @bot.event
        async def on_ready():
            print("---Login Info---")
            print(bot.user.name)
            print(bot.user.id)
            print(discord.__version__)
            print("----------------")
            channel = bot.get_channel(ROOM_ID)

            now = datetime.datetime.now()
            embed = discord.Embed( # Embedを定義
                                  title= str(bot.user) + " Logged in!",
                                  color=0xff0000,
                                  description="Logged in to [" + str(now.strftime('%H:%M:%S')) + "]\n discord_version:" + str(discord.__version__) + "\n The current PREFIX is 「" + str(PREFIX) + "」.",
                                  url="https://github.com/Unigmos" # 指定URL
                                  )
            embed.set_author(name=bot.user, # Botのユーザー名
                             url="https://github.com/Unigmos",
                             icon_url=bot.user.avatar_url
                             )

            embed.set_footer(text="Made by Shaneron", # フッター情報
                     icon_url="https://avatars.githubusercontent.com/u/77985354?v=4")

            await channel.send(embed=embed)

        @bot.event
        async def on_message(message):
            global unk_flag
            channel = bot.get_channel(COMMAND_ROOM_ID)
            # メッセージ送信者がBotだった場合は無視する
            if message.author.bot:
                return

            # helpコマンド(コマンド一覧表示)
            if message.content == f"{PREFIX}help":
                embed = discord.Embed( # Embedを定義
                                  title= "コマンド一覧",
                                  color=0xff0000,
                                  description="コマンド一覧を表示します。",
                                  url=""
                                  )
                embed.set_author(name=bot.user, # Botのユーザー名
                                 url="https://github.com/Unigmos",
                                 icon_url=bot.user.avatar_url
                                 )
                embed.add_field(name=f"{PREFIX}help",value="今打ったであろうコマンド。コマンド一覧を表示します。", inline=False)
                embed.add_field(name=f"{PREFIX}team",value="チーム分けコマンド。チーム分けを行います。(現在開発中)", inline=False)
                embed.add_field(name=f"{PREFIX}unk",value="リアクションコマンド。何のリアクションかは打ってからのお楽しみ。\n ※オプション(true, false)", inline=False)
                embed.add_field(name=f"{PREFIX}del_log",value="ログ削除コマンド。トーク履歴の削除を行います。(管理者専用)", inline=False)
                embed.add_field(name=f"{PREFIX}set_prefix",value="PREFIXセットコマンド。(管理者専用)(現在開発中)", inline=False)
                embed.add_field(name=f"{PREFIX}end",value="プログラム終了コマンド。(管理者専用)", inline=False)

                await channel.send(embed=embed)

            # del_logコマンド(メッセージ削除)
            if message.content == f"{PREFIX}del_log":
                if message.author.guild_permissions.administrator:
                    embed = discord.Embed( # Embedを定義する
                                  title= "メッセージ削除",
                                  color=0xff0000,
                                  description="本当に削除するなら「OK」、やっぱりやめるなら「NG」を選択してください。2度は聞かんぞ？",
                                  url=""
                                  )
                    embed.set_author(name=bot.user, # Botのユーザー名
                                     url="https://github.com/Unigmos",
                                     icon_url=bot.user.avatar_url
                                     )

                    msg = await channel.send(embed=embed)
                    await msg.add_reaction("🆗")
                    await msg.add_reaction("🆖")

                    @bot.event
                    async def on_reaction_add(reaction, member):
                        # メッセージ送信者がBotだった場合は無視する
                        if message.author.bot:
                            return
                        if reaction.emoji == ("🆗"):
                            await message.channel.purge()
                            embed = discord.Embed( # Embedを定義する
                                  title= "",
                                  color=0xff0000,
                                  description= "きれいさっぱりさ！",
                                  url=""
                                  )
                            embed.set_author(name=bot.user, # Botのユーザー名
                                     url="https://github.com/Unigmos",
                                     icon_url=bot.user.avatar_url
                                     )
                            await channel.send(embed=embed)

                        else:
                            return
                else:
                    embed = discord.Embed( # Embedを定義する
                                  title= "",
                                  color=0xff0000,
                                  description="管理者のみ実行可能コマンドです。",
                                  url=""
                                  )
                    embed.set_author(name=bot.user, # Botのユーザー名
                                     url="https://github.com/Unigmos",
                                     icon_url=bot.user.avatar_url
                                     )

                    await channel.send(embed=embed)

            # unkコマンド
            if message.content == f"{PREFIX}unk":
                embed = discord.Embed( # Embedを定義する
                              title= "unkコマンド",
                              color=0xff0000,
                              description=f"オプションの設定を行ってください。例:unk true",
                              url=""
                              )
                embed.set_author(name=bot.user, # Botのユーザー名
                                 url="https://github.com/Unigmos",
                                 icon_url=bot.user.avatar_url
                                 )

                msg = await channel.send(embed=embed)

            # unkコマンド(True)
            if message.content == f"{PREFIX}unk true":
                unk_flag = True
                embed = discord.Embed( # Embedを定義する
                              title= "unkコマンド",
                              color=0xff0000,
                              description=f"unk_flagのbool値を{unk_flag}にしました。",
                              url=""
                              )
                embed.set_author(name=bot.user, # Botのユーザー名
                                 url="https://github.com/Unigmos",
                                 icon_url=bot.user.avatar_url
                                 )

                msg = await channel.send(embed=embed)

            # unkコマンド(False)
            if message.content == f"{PREFIX}unk false":
                unk_flag = False
                embed = discord.Embed( # Embedを定義する
                              title= "unkコマンド",
                              color=0xff0000,
                              description=f"unk_flagのbool値を{unk_flag}にしました。",
                              url=""
                              )
                embed.set_author(name=bot.user, # Botのユーザー名
                                 url="https://github.com/Unigmos",
                                 icon_url=bot.user.avatar_url
                                 )

                msg = await channel.send(embed=embed)

            # teamコマンド(チーム分け)
            if message.content == f"{PREFIX}team":
                try:
                    import random

                    members = [member.name for member in message.author.voice.channel.members]
                    random.shuffle(members)

                    party = 2
                    team = []

                    for member in range(party):
                        team.append("=====チーム"+str(member+1)+"=====")
                        team.extend(members[member:len(members):party])

                    contents = '\r\n'.join(team)

                    embed = discord.Embed( # Embedを定義
                                      title= "チーム分け",
                                      color=0xff0000,
                                      description="チーム分けを行います。",
                                      url=""
                                      )
                    embed.set_author(name=bot.user, # Botのユーザー名
                                     url="https://github.com/Unigmos",
                                     icon_url=bot.user.avatar_url
                                     )
                    embed.add_field(name="",value=contents, inline=False)

                    await channel.send(embed=embed)

                except ModuleNotFoundError as NO_MODULE_ERROR:
                    print("ModuleNotFoundError:", NO_MODULE_ERROR, "at main-team")
                except AttributeError:
                    embed = discord.Embed( # Embedを定義
                                      title= "AttributeError",
                                      color=0xff0000,
                                      description="誰もVCにいないねん。",
                                      url=""
                                      )
                    embed.set_author(name=bot.user, # Botのユーザー名
                                     url="https://github.com/Unigmos",
                                     icon_url=bot.user.avatar_url
                                     )

                    await channel.send(embed=embed)

            # endコマンド(プログラム終了)
            if message.content == f"{PREFIX}end":
                if message.author.guild_permissions.administrator:
                    try:
                        import sys

                        embed = discord.Embed( # Embedを定義する
                                          title= "Exit the program",
                                          color=0xff0000,
                                          description="プログラムを終了します。",
                                          url=""
                                          )
                        embed.set_author(name=bot.user, # Botのユーザー名
                                         url="https://github.com/Unigmos",
                                         icon_url=bot.user.avatar_url
                                         )

                        await channel.send(embed=embed)
                        sys.exit()

                    except ModuleNotFoundError as NO_MODULE_ERROR:
                        print("ModuleNotFoundError:", NO_MODULE_ERROR, "at main-team")
                else:
                    embed = discord.Embed( # Embedを定義する
                                  title= "",
                                  color=0xff0000,
                                  description="管理者のみ実行可能コマンドです。",
                                  url=""
                                  )
                    embed.set_author(name=bot.user, # Botのユーザー名
                                     url="https://github.com/Unigmos",
                                     icon_url=bot.user.avatar_url
                                     )

                    await channel.send(embed=embed)

            if unk_flag:
                await message.add_reaction("💩")

        #実行
        bot.run(token)

    except ModuleNotFoundError as NO_MODULE_ERROR:
        print("ModuleNotFoundError:", NO_MODULE_ERROR, "at main")
    except RuntimeError as RUN_TIME_ERROR:
        print("RuntimeError", RUN_TIME_ERROR, "at main")
    except NameError as NAME_ERROR:
        print("NameError", NAME_ERROR, "at main")

def read_json(path):
    try:
        import json
        json_values = []

        with open(path, 'r') as json_file:
            json_data = json.load(json_file)

            json_values.append(json_data.get('token'))
            json_values.append(json_data.get('login_room_id'))
            json_values.append(json_data.get('command_room_id'))

        return json_values

    except ModuleNotFoundError as NO_MODULE_ERROR:
        print("ModuleNotFoundError:", NO_MODULE_ERROR, "at read_json")
    except FileNotFoundError as NOT_FOUND_ERROR:
        print("FileNotFoundError:", NOT_FOUND_ERROR, "at read_json")

if __name__ == '__main__':
    main()
