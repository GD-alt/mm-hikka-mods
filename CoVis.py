from .. import loader, utils
import io
import logging
import asyncio
import requests
from textwrap import wrap
from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)

# meta developer: @minimaxno
# meta pic: https://img.icons8.com/fluency/344/color-palette.png


class CoVisMod(loader.Module):
    """Visualise colors by those formules."""
    strings = {"name": "CoVis", "noargs": "📪 <b>And where's args?</b>", "inargs": "😵 <b>Incorrect args format!</b>"}
    strings_ru = {"name": "CoVis", "noargs": "📪 <b>Где аргументы?</b>", "inargs": "😵 <b>Неверный формат аргумента!</b>"}
    strings_de = {"name": "CoVis", "noargs": "📪 <b>Wo ist Argumenten?</b>", "inargs": "😵 <b>Falsches Argumenten-Format!</b>"}

    async def _dl_font(self, font_name, short_name, size):
        font_name = font_name.replace(" ", "%20")
        setattr(
            self,
            short_name,
            ImageFont.truetype(
                io.BytesIO(
                    (
                        await utils.run_sync(
                            requests.get,
                            f"https://github.com/GD-alt/fonts/blob/main/{font_name}.ttf?raw=true",
                        )
                    ).content
                ),
            size),
        )
        getattr(self, f"{short_name}_ready").set()

    async def client_ready(self, client, db):
        self.tnrb_ready = asyncio.Event()
        asyncio.ensure_future(self._dl_font('Times New Roman Bold', 'tnrb', 64))
        self.fptb_ready = asyncio.Event()
        asyncio.ensure_future(self._dl_font('FuturaPT-Bold', 'fptb', 80))
        self.cpsb_ready = asyncio.Event()
        asyncio.ensure_future(self._dl_font('SourceCodePro-SemiBold', 'cpsb', 45))
        self.client = client

    async def hpiccmd(self, message):
        """Visualise HEX-coded color.
		.hpic <HEX-color>"""
        text = utils.get_args_raw(message)
        if not text:
            await utils.answer(message, self.strings("noargs"))
            return
        color = text
        if color.startswith("#") and len(color) == 7:
            for ch in color.lower()[1:]:
                if ch not in "0123456789abcdef":
                    await utils.answer(message, self.strings("inargs"))
                    break
        else:
            color = "#FFFFFF"
        txt = []
        for line in text.split("\n"):
            txt.append("\n".join(wrap(line, 30)))
        text = "\n".join(txt)
        image = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((0, 0, 512, 512), 50, outline="#000000", fill=color, width=8)
        output = io.BytesIO()
        output.name = color + ".webp"
        image.save(output, "WEBP")
        output.seek(0)
        await message.delete()
        await self.client.send_file(message.chat_id, output)
        
    async def rpiccmd(self, message):
        """Visualise RGB-coded color.
        .rpic <RGB-color>"""
        text = utils.get_args_raw(message)
        if not text:
            await utils.answer(message, self.strings("noargs"))
            return
        color = text
        if color.startswith("(") and color.endswith(")") and color.count(",") == 2:
            color = color.replace('(', '')
            color = color.replace(')', '')
            r, g, b = color.split(',')
            if (not r.isnumeric()) or (not g.isnumeric()) or (not b.isnumeric()):
                await utils.answer(message, self.strings("inargs"))
                return
            color = eval(f"[{int(r)}, {int(g)}, {int(b)}]")
            for i in range(0, 2):
                if (color[i] > 255) or (color[i] < 0):
                    await utils.answer(message, self.strings("inargs"))
                    break
            color = f'rgb({color[0]},{color[1]},{color[2]})'
        else:
            color = "rgb(0,0,0)"
        txt = []
        for line in text.split("\n"):
            txt.append("\n".join(wrap(line, 30)))
        text = "\n".join(txt)
        image = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((0, 0, 512, 512), 50, outline="#000000", fill=color, width=8)
        output = io.BytesIO()
        output.name = color + ".webp"
        image.save(output, "WEBP")
        output.seek(0)
        await message.delete()
        await self.client.send_file(message.chat_id, output)
        
    async def spiccmd(self, message):
        """Visualise HSB-coded color.
        .spic <HSB-color>"""
        text = utils.get_args_raw(message)
        if not text:
            await utils.answer(message, self.strings("noargs"))
            return
        color = text
        if color.startswith("(") and color.endswith(")") and color.count(",") == 2:
            color = color.replace('(', '')
            color = color.replace(')', '')
            h, s, b = color.split(',')
            if (not h.isnumeric()) or (not s.isnumeric()) or (not b.isnumeric()):
                await utils.answer(message, self.strings("inargs"))
                return
            h = int(h)
            s = int(s)
            b = int(b)
            if (h < 0) or (h > 360):
                await utils.answer(message, self.strings("inargs"))
                return
            if (s < 0) or (s > 100):
                await utils.answer(message, self.strings("inargs"))
                return
            if (b < 0) or (b > 100):
                await utils.answer(message, self.strings("inargs"))
                return
            color = f'hsv({h},{s}%,{b}%)'
        else:
            color = "hsv(0,0%,0%)"
        txt = []
        for line in text.split("\n"):
            txt.append("\n".join(wrap(line, 30)))
        text = "\n".join(txt)
        image = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((0, 0, 512, 512), 50, outline="#000000", fill=color, width=8)
        output = io.BytesIO()
        output.name = color + ".webp"
        image.save(output, "WEBP")
        output.seek(0)
        await message.delete()
        await self.client.send_file(message.chat_id, output)

    async def hdpiccmd(self, message):
        """Visualise HEX-coded color with color code on it.
		.hdpic <HEX-color>"""
        text = utils.get_args_raw(message)
        if not text:
            await utils.answer(message, self.strings("noargs"))
            return
        color = text
        if color.startswith("#") and len(color) == 7:
            for ch in color.lower()[1:]:
                if ch not in "0123456789abcdef":
                    await utils.answer(message, self.strings("inargs"))
                    break
        else:
            color = "#FFFFFF"
        txt = []
        for line in text.split("\n"):
            txt.append("\n".join(wrap(line, 30)))
        text = "\n".join(txt)
        await self.fptb_ready.wait()
        image = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((0, 0, 512, 512), 50, outline="#000000", fill=color, width=8)
        draw.text((256, 256), text=color, anchor="mm", font=self.fptb, fill="#FFFFFF", align="center", stroke_width=8,
                  stroke_fill="#000000")
        output = io.BytesIO()
        output.name = color + ".webp"
        image.save(output, "WEBP")
        output.seek(0)
        await message.delete()
        await self.client.send_file(message.chat_id, output)

    async def rdpiccmd(self, message):
        """Visualise RGB-coded color with color code on it.
        .rdpic <RGB-color>"""
        text = utils.get_args_raw(message)
        if not text:
            await utils.answer(message, self.strings("noargs"))
            return
        color = text
        if color.startswith("(") and color.endswith(")") and color.count(",") == 2:
            color = color.replace('(', '')
            color = color.replace(')', '')
            r, g, b = color.split(',')
            if (not r.isnumeric()) or (not g.isnumeric()) or (not b.isnumeric()):
                await utils.answer(message, self.strings("inargs"))
                return
            color = eval(f"[{int(r)}, {int(g)}, {int(b)}]")
            for i in range(0, 2):
                if (color[i] > 255) or (color[i] < 0):
                    await utils.answer(message, self.strings("inargs"))
                    break
            color = f'rgb({color[0]},{color[1]},{color[2]})'
        else:
            color = "rgb(0,0,0)"
        txt = []
        for line in text.split("\n"):
            txt.append("\n".join(wrap(line, 30)))
        text = "\n".join(txt)
        image = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
        await self.tnrb_ready.wait()
        font = io.BytesIO(self.tnrb)
        font = ImageFont.truetype(font, 64)
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((0, 0, 512, 512), 50, outline="#000000", fill=color, width=8)
        draw.text((256, 256), text=color, anchor="mm", font=self.tnrb, fill="#FFFFFF", align="center", stroke_width=8,
                  stroke_fill="#000000")
        output = io.BytesIO()
        output.name = color + ".webp"
        image.save(output, "WEBP")
        output.seek(0)
        await message.delete()
        await self.client.send_file(message.chat_id, output)

    async def sdpiccmd(self, message):
        """Visualise HSB-coded color with color code on it.
        .sdpic <HSB-color>"""
        text = utils.get_args_raw(message)
        if not text:
            await utils.answer(message, self.strings("noargs"))
            return
        color = text
        if color.startswith("(") and color.endswith(")") and color.count(",") == 2:
            color = color.replace('(', '')
            color = color.replace(')', '')
            h, s, b = color.split(',')
            if (not h.isnumeric()) or (not s.isnumeric()) or (not b.isnumeric()):
                await utils.answer(message, self.strings("inargs"))
                return
            h = int(h)
            s = int(s)
            b = int(b)
            if (h < 0) or (h > 360):
                await utils.answer(message, self.strings("inargs"))
                return
            if (s < 0) or (s > 100):
                await utils.answer(message, self.strings("inargs"))
                return
            if (b < 0) or (b > 100):
                await utils.answer(message, self.strings("inargs"))
                return
            color = f'hsv({h},{s}%,{b}%)'
        else:
            color = "hsv(0,0%,0%)"
        txt = []
        for line in text.split("\n"):
            txt.append("\n".join(wrap(line, 30)))
        text = "\n".join(txt)
        image = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((0, 0, 512, 512), 50, outline="#000000", fill=color, width=8)
        await self.cpsb_ready.wait()
        draw.text((256, 256), text=color, anchor="mm", font=self.cpsb, fill="#FFFFFF", align="center", stroke_width=8,
                  stroke_fill="#000000")

        output = io.BytesIO()
        output.name = color + ".webp"
        image.save(output, "WEBP")
        output.seek(0)
        await message.delete()
        await self.client.send_file(message.chat_id, output)