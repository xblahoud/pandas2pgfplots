"""Display tikzcode in Jupyter notebook"""
import os
import tempfile

import itikz


def get_tempdir():
    cwd = os.path.join(tempfile.gettempdir(), 'itikz')
    os.makedirs(cwd, exist_ok=True)
    return cwd


def display_tikz(tikzcode, scale=2.0):
    preamble = r"""\usepackage{pgfplots}
\usepackage{xcolor}
\pgfplotsset{compat=newest}
"""
    d = {"src": tikzcode,
         "extras": preamble,
         "scale": float(scale)
         }

    src = itikz.IMPLICIT_PIC_TMPL.substitute(d)
    return itikz.fetch_or_compile_svg(src, prefix='pandas2pgfplots-', working_dir=get_tempdir())
