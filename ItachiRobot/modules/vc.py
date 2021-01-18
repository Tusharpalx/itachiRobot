from __future__ import unicode_literals
import youtube_dl
import asyncio
import aiohttp
import aiofiles
import time
import json
import os
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from youtube_search import YoutubeSearch
from ItachiRobot import owner_id, bot_token, radio_link

@app.on_message(
    filters.command(["jiosaavn"])

async def jiosaavn(_, message: Message):
    global blacks
        return
    global s
    global m
    if len(message.command) < 2:
        await message.reply_text("/jiosaavn requires an argument")
        return
    try:
        os.system("killall -9 mpv")
    except:
        pass
    try:
        await m.delete()
    except:
        pass
    try:
        await message.delete()
    except:
        pass

    query = kwairi(message)

    m = await message.reply_text(f"Searching for `{query}` on JioSaavn")
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://jiosaavnapi.bhadoo.uk/result/?query={query}"
        ) as resp:
            r = json.loads(await resp.text())

    sname = r[0]["song"]
    slink = r[0]["media_url"]
    ssingers = r[0]["singers"]
    sthumb = r[0]["image"]
    sduration = r[0]["duration"]
    sduration_converted = convert_seconds(int(sduration)) 
    await m.edit("Processing Thumbnail.")
    async with aiohttp.ClientSession() as session:
        async with session.get(sthumb) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    def changeImageSize(maxWidth, maxHeight, image):
        widthRatio = maxWidth / image.size[0]
        heightRatio = maxHeight / image.size[1]
        newWidth = int(widthRatio * image.size[0])
        newHeight = int(heightRatio * image.size[1])
        newImage = image.resize((newWidth, newHeight))
        return newImage

    image1 = Image.open("./background.png")
    image2 = Image.open("etc/foreground.png")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save("temp.png")
    img = Image.open("temp.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("etc/JetBrainsMonoNL-Regular.ttf", 32)
    draw.text(
        (190, 550), f"Title: {sname}", (255, 255, 255), font=font
    )
    draw.text(
        (190, 590), f"Artist: {ssingers}", (255, 255, 255), font=font
    )
    draw.text(
        (190, 630),
        f"Duration: {sduration_converted} Seconds",
        (255, 255, 255),
        font=font,
    )
    draw.text(
        (190, 670),
        f"Played By: {message.from_user.first_name}",
        (255, 255, 255),
        font=font,
    )
    img.save("final.png")
    os.system("rm temp.png")
    os.system("rm background.png")
    await m.delete()
    m = await message.reply_photo(
        caption=f"Playing `{sname}` Via Jiosaavn #music",
        photo="final.png",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        f"STOP", callback_data="end"
                    )
                ]
            ]
        ),
        parse_mode="markdown",
    )

    s = await asyncio.create_subprocess_shell(
        f"mpv {slink} --no-video",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    await s.wait()
    await m.delete()


# Youtube Play

@app.on_message(
    filters.command(["youtube"])
async def ytplay(_, message: Message):
    global blacks
    if message.from_user.id in blacks:
        await message.reply_text("You're Blacklisted, So Stop Spamming.")
        return
    global m
    global s

    if len(message.command) < 2:
        await message.reply_text("/youtube requires one argument")
        return
    try:
        await message.delete()
    except:
        pass
    try:
        await m.delete()
    except:
        pass
    try:
        os.system("killall -9 mpv")
    except:
        pass
    try:
        os.remove("audio.mp3")
    except:
        pass
    ydl_opts = {"format": "bestaudio"}
    query = kwairi(message)
    m = await message.reply_text(f"Searching for `{query}` on YouTube")
    results = YoutubeSearch(query, max_results=1).to_dict()
    link = f"https://youtube.com{results[0]['url_suffix']}"
    title = results[0]["title"]
    thumbnail = results[0]["thumbnails"][0]
    duration = results[0]["duration"]
    views = results[0]["views"]
    await m.edit("Processing Thumbnail.")
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    def changeImageSize(maxWidth, maxHeight, image):
        widthRatio = maxWidth / image.size[0]
        heightRatio = maxHeight / image.size[1]
        newWidth = int(widthRatio * image.size[0])
        newHeight = int(heightRatio * image.size[1])
        newImage = image.resize((newWidth, newHeight))
        return newImage

    image1 = Image.open("./background.png")
    image2 = Image.open("etc/foreground.png")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save("temp.png")
    img = Image.open("temp.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("etc/JetBrainsMonoNL-Regular.ttf", 32)
    draw.text((190, 550), f"Title: {title}", (255, 255, 255), font=font)
    draw.text(
        (190, 590), f"Duration: {duration}", (255, 255, 255), font=font
    )
    draw.text((190, 630), f"Views: {views}", (255, 255, 255), font=font)
    draw.text(
        (190, 670),
        f"Played By: {message.from_user.first_name}",
        (255, 255, 255),
        font=font,
    )
    img.save("final.png")
    os.system("rm temp.png")
    os.system("rm background.png")
    await m.edit("Downloading Music.")
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(link, download=False)
        audio_file = ydl.prepare_filename(info_dict)
        ydl.process_info(info_dict)
        os.rename(audio_file, "audio.webm")
    await m.delete()
    m = await message.reply_photo(
        caption=f"Playing [{title}]({link}) Via YouTube #music",
        photo="final.png",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        f"STOP", callback_data="end"
                    )
                ]
            ]
        ),
        parse_mode="markdown",
    )
    os.system("rm final.png")
    s = await asyncio.create_subprocess_shell(
        "mpv audio.webm --no-video",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    await s.wait()
    await m.delete()


# youtube playlist


@app.on_message(
    filters.command(["playlist"])
)
async def playlist(_, message: Message):
        return
    global m
    global s

    if len(message.command) != 2:
        await message.reply_text(
            "/playlist requires one youtube playlist link"
        )
        return
    try:
        await message.delete()
    except:
        pass
    try:
        await m.delete()
    except:
        pass
    try:
        os.system("killall -9 mpv")
    except:
        pass
    try:
        os.remove("audio.mp3")
    except:
        pass

    link = message.command[1]
    ydl_opts = {"format": "bestaudio"}

    m = await message.reply_text("Processing Playlist...")
    with youtube_dl.YoutubeDL():
        result = youtube_dl.YoutubeDL().extract_info(link, download=False)

        if "entries" in result:
            video = result["entries"]
            await m.edit(
                f"Found {len(result['entries'])} Videos In Playlist, Playing Them All."
            )
            ii = 1
            for i, item in enumerate(video):
                video = result["entries"][i]["webpage_url"]
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(video, download=False)
                    audio_file = ydl.prepare_filename(info_dict)
                    ydl.process_info(info_dict)
                    os.rename(audio_file, "audio.webm")
                await m.edit(
                    f"Playing `{result['entries'][i]['title']}`, Song Number `{ii}` In Playlist, `{len(result['entries']) - ii}` In Queue. \nRequested by - {message.from_user.mention}"
                )
                s = await asyncio.create_subprocess_shell(
                    "mpv audio.webm --no-video",
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                await s.wait()
                ii += 1
                os.system("rm audio.webm")


# Telegram Audio


@app.on_message(
    filters.command(["telegram"])
async def tgplay(_, message: Message):
        return
    global m
    global s
    if not message.reply_to_message:
        await message.reply_text("Reply To A Telegram Audio To Play It.")
        return
    try:
        await message.delete()
    except:
        pass
    try:
        await m.delete()
    except:
        pass
    try:
        os.system("killall -9 mpv")
    except:
        pass
    try:
        os.remove("audio.mp3")
    except:
        pass
    try:
        os.remove("downloads/audio.mp3")
    except:
        pass
    m = await message.reply_text("Downloading")
    j = await app.download_media(message.reply_to_message, file_name="audio.mp3")
    await m.edit(f"Playing `{message.reply_to_message.link}` via Telegram.")
    s = await asyncio.create_subprocess_shell(
        "mpv downloads/audio.mp3 --no-video",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    await s.wait()
    await m.delete()
    os.system("rm downloads/audio.mp3")


# Radio


@app.on_message(
    filters.command(["radio"]) & filters.chat(sudo_chat_id) & ~filters.edited
)
async def radio(_, message: Message):
    global blacks
    if message.from_user.id in blacks:
        await message.reply_text("You're Blacklisted, So Stop Spamming.")
        return
    global m
    global s

    try:
        os.system("killall -9 mpv")
    except:
        pass
    try:
        await m.delete()
    except:
        pass
    try:
        await message.delete()
    except:
        pass

    try:
        os.remove("audio.mp3")
    except:
        pass
    m = await message.reply_text(
        f"Playing Radio\nRequested by - {message.from_user.mention}"
    )
    s = await asyncio.create_subprocess_shell(
        f"mpv {radio_link} --no-video",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    await s.wait()
    await m.delete()


# End Music


@app.on_message(
    filters.command(["end"]) & filters.chat(sudo_chat_id) & ~filters.edited
)
async def end(_, message: Message):
    global blacks
    global m
    global s
    if message.from_user.id in blacks:
        await message.reply_text("You're Blacklisted, So Stop Spamming.")
        return
    try:
        os.remove("audio.mp3")
    except:
        pass

    try:
        await message.delete()
    except:
        pass
    try:
        os.system("killall -9 mpv")
    except:
        pass
    try:
        s.terminate()
    except:
        pass
    try:
        await m.delete()
    except:
        pass

    await message.reply_text(
        f"{message.from_user.mention} Stopped The Music."
    )


@app.on_callback_query(filters.regex("end"))
async def end_callback(_, CallbackQuery):
    global blacks
    global m
    global s
    chat_id = int(CallbackQuery.message.chat.id)
    if CallbackQuery.from_user.id in blacks:
        return
    try:
        os.remove("audio.mp3")
    except:
        pass
    try:
        os.system("killall -9 mpv")
    except:
        pass
    try:
        s.terminate()
    except:
        pass
    try:
        await m.delete()
    except:
        pass
    await app.send_message(
        chat_id,
        f"{CallbackQuery.from_user.mention} - {CallbackQuery.from_user.id} Stopped The Music.",
    )

@app.on_message(
    filters.command(["users"]) & filters.chat(sudo_chat_id) & ~filters.edited
)
async def users(client, message: Message):
    global blacks
    if message.from_user.id in blacks:
        await message.reply_text("You're Blacklisted, So Stop Spamming.")
        return
    output = "Blacklisted Users:\n"
    n = 1
    for i in blacks:
        usern = (await client.get_users(i)).mention
        output += f"{n}. {usern}\n"
        n += 1
    if len(blacks) == 0:
        await message.reply_text("No Users Are Blacklisted")
        return
    await message.reply_text(output)
