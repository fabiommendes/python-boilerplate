from functools import partial

import ezio

fancy_print = partial(ezio.print, format=True, max_width=70)