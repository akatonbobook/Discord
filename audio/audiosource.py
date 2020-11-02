import subprocess

import discord
import radiko
from discord.opus import Encoder as OpusEncoder


class RadiSource(discord.FFmpegAudio):

    def __init__(self, identifier):
        self.client = radiko.Client()
        source = self.client.get_stream(identifier)
        args = ['-i', source, '-f', 's16le', '-ac', '2', '-loglevel', 'warning', 'pipe:1']
        subprocess_kwargs = {
            'stdin': subprocess.DEVNULL
        }
        super().__init__(source, args=args, **subprocess_kwargs)
        print(source)

    def read(self):
        ret = self._stdout.read(OpusEncoder.FRAME_SIZE)
        if len(ret) != OpusEncoder.FRAME_SIZE:
            return b''
        return ret

    def is_opus(self):
        return False

    def select(self, identifier):
        """局を選択する関数
        """
        self.client.select_station(identifier)


class MyPCMVolumeTransformer(discord.PCMVolumeTransformer):

    def __init__(self, original, volume=1.0):
        super().__init__(original, volume)
        self.original = original
