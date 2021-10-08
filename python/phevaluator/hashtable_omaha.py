from struct import *
from pathlib import Path

DIR = Path(__file__).parent

FLUSH_OMAHA = unpack('<4099095h', open(DIR / 'omaha_flush.dat', 'rb').read())
NO_FLUSH_OMAHA = unpack('<11238500h', open(DIR / 'omaha_noflush.dat', 'rb').read())
