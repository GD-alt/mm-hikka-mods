# `7MMM.     ,MMF'`7MMM.     ,MMF'   `7MMM.     ,MMF'              `7MM
# MMMb    dPMM    MMMb    dPMM       MMMb    dPMM                  MM
# M YM   ,M MM    M YM   ,M MM       M YM   ,M MM  ,pW"Wq.    ,M""bMM  ,pP"Ybd
# M  Mb  M' MM    M  Mb  M' MM       M  Mb  M' MM 6W'   `Wb ,AP    MM  8I   `"
# M  YM.P'  MM    M  YM.P'  MM mmmmm M  YM.P'  MM 8M     M8 8MI    MM  `YMMMa.
# M  `YM'   MM    M  `YM'   MM       M  `YM'   MM YA.   ,A9 `Mb    MM  L.   I8
# .JML. `'  .JMML..JML. `'  .JMML.   .JML. `'  .JMML.`Ybmd9'   `Wbmd"MML.M9mmmP'
#
# (c) 2022 — licensed under Apache 2.0 — https://www.apache.org/licenses/LICENSE-2.0

# meta pic: https://img.icons8.com/stickers/344/calendar.png
# meta developer: @mm_mods
# requires: deep-translator

__version__ = "1.0.0"

import re
from .. import loader, utils
import deep_translator
import requests
import random

from telethon.tl.types import Message
import logging

logger = logging.getLogger(__name__)


@loader.tds
class ShittytextMod(loader.Module):
    """Makes your text shitty. Be very, very careful."""
    
    strings = {'name': 'Shittytext'}
    
    async def watcher(self, m):
        if not m.out:
            return
        tet = deep_translator.GoogleTranslator(source='auto', target='zh-CN').translate(m.raw_text)
        res = ''.join(random.sample(tet, len(tet)))
        res = deep_translator.GoogleTranslator(source='auto', target='ru').translate(res)
        await utils.answer(m, res)
