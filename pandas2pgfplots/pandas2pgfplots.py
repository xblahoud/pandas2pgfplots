""" Pgfplots code for DataFrame objects

Currently, it supports scatter plots and cactus plots.

The generated code is not enclosed in the `tikzpicture` environment.
"""

def_opts_scatter = {
    "mark size" : "1.2pt",
    "axis x line*" : "bottom",
    "axis y line*" : "left",
    "width" : "7cm",
    "height" : "6.5cm",
    "xlabel near ticks" : True,
    "ylabel near ticks" : True,
    "xmin" : 0,
    "ymin" : 0,
    # colorbar
    "colorbar/width" : ".1cm",
    "colorbar style" : "{line width=.1pt}",
    "colorbar shift/.style" : r"{xshift=.1cm}",
}

# This is defaults for \addplot in the scatter plot, not \axis
def_opts_scatter_marks = {
    "scatter" : True,
    "scatter src" : "explicit",
    "only marks" : True,
    "mark options" : "{fill opacity=.3, draw opacity=0}",
}

def_opts_cactus = {
    "very thick" : True,
    "no markers" : True,
    "axis x line*" : "bottom",
    "axis y line*" : "left",
    "width" : "12cm",
    "height" : "7cm",
    "cycle list" : """{%
    {green, solid},
    {blue, densely dashed},
    {red, dashdotdotted},
    {black, densely dotted},
    {brown, loosely dashdotted}
}""",
    "xlabel near ticks" : True,
    "ylabel near ticks" : True,
    "xmin" : 0,
    # Legends
    "legend pos" : "north west",
    "every axis legend/.append style": "{cells={anchor=west}, draw=none}",
}

def_opts_pgfplots = {
    # general
    "compat" : "newest",
}


def scatter(df, log=None, tikz_hook="", marks_dict={}, pgfplotsset_dict={}, **kwargs):
    """Return pgfplots code of a scatter plot for `df`.

    The DataFrame `df` must have 2 or 3 columns.

    Parameters
    ==========
      df : DataFrame with at least 2 columns
      x : str
          The column name to be used as horizontal coordinates for each point.
      y : str
          The column name to be used as vertical coordinates for each point.
      c : str (default None)
          The column name to be used
      diagonal : Bool (default `True`)
          whether to draw the y=x line
      log : one of None (default), 'x', 'y', 'both'
          Make the given axis in logarithmic scale.
      tikz_hook : str
          Tikz code inserted just before `\end{axis}`. Can be used to draw or add
           nodes using the axis coordinates.
      pgfplotsset_dict : dict (str -> value)
          Dict of pgfplots keys to be set, after TikZification supplied to `\pgfplotsset`
      marks_dict : dict (str -> value)
          Dict of pgfplots keys given to `every mark/.append style` which is given
          to `\addplot`'s options insread of `axis`.
      **kwargs : will be supplied to axis options after "TikZification"


    Returns
    -------
    Multiline string with the pgfplots code for scatter plot. This needs to be placed
    inside `tikzpicture` environment.
    """
    x = kwargs.pop("x", df.columns.values[0])
    y = kwargs.pop("y", df.columns.values[1])
    c = kwargs.pop("c", None)
    diagonal = kwargs.pop("diagonal", True)

    args = def_opts_scatter.copy()
    args["xlabel"] = f"{{{x}}}"
    args["ylabel"] = f"{{{y}}}"
    args.update(kwargs)

    pgfplots_args = def_opts_pgfplots.copy()
    pgfplots_args.update(pgfplotsset_dict)

    marks_args = def_opts_scatter_marks.copy()
    marks_args["every mark/.append style"] = f"{{{tikzify_dict(marks_dict)}}}"

    # Check the valid content of `log`
    axis = 'axis'
    if log is not None:
        if log == 'both':
            axis = 'loglogaxis'
            args['xmin'] = 1
            args['ymin'] = 1
        elif log in ['x','y']:
            axis = f'semilog{log}axis'
            args[f'{log}min'] = 1
        else:
            raise ValueError("`log` should be one of None, 'x', 'y', 'both'")

    # Create the list of coordinates
    # The [1] allow us not to distinguish between `scatter` and `marks only` in
    # \addplot options.
    if c is None:
        coordinates = [f'({vx},{vy}) [1]%\n' for vx,vy in df.reindex(axis=1)[[x,y]].to_numpy()]
        marks_args["scatter"] = False
        if kwargs.get("colorbar"):
            raise ValueError("When colorbar requested, column for color has to be specified by `c`.")
    else:
        coordinates = [f'({vx},{vy}) [{vc}]%\n' for vx,vy,vc in df.reindex(axis=1)[[x,y,c]].to_numpy()]
        marks_args["scatter"] = True

    if diagonal:
        start_line = 0 if log is None else 1
        line = f'\\addplot[gray,domain={start_line}:{min(df.max(axis=0)[:2])+1}]{{x}};'
    else:
        line = ""

    res = f'''\\pgfplotsset{{
{tikzify_dict(pgfplots_args, 2)}}}
\\begin{{{axis}}}[
{tikzify_dict(args, 2)}%
]
\\addplot[
{tikzify_dict(marks_args, 2)}%
] coordinates
  {{{"  ".join(coordinates)}}};%
{line}%
{tikz_hook}%
\\end{{{axis}}}
'''
    return res


def cactus(df, exclude_treshold=None, log=None, pgfplotsset_dict={}, **kwargs):
    """Create pgfplots code for cactus plots for a DataFrame.

    In a cactus plot, the values in each column are sorted separately, yielding an
    order of values for each column. These values are then ploted, one line for each
    column. The value $v$ that is on position $i$ in this order for column `col`
    results in a point of the `col` line at $(i,v)$.

    The parameter `exclude_treshold`, if given, controls which data are plotted.
    The points for values `v >= exclude_treshold` are not added to the line for
    col. This can cause that each line has different length (and x-domain).

    Parameters
    ----------
    df : DataFrame
    exclude_treshold : int
        Values greater or equal to `exclude_treshold` are not added to the plot
    log : one of None (default), 'x', 'y', 'both'
        Make the given axis in logarithmic scale.
    pgfplotsset_dict : dict (str -> value)
        Dict of pgfplots keys to be set, after TikZification supplied to `\pgfplotsset`
    **kwargs : will be supplied to axis options after "TikZification"

    Returns
    -------
    Multiline string with the pgfplots code for cactus plot. This needs to be placed
    inside `tikzpicture` environment.
    """
    args = def_opts_cactus.copy()
    args.update(kwargs)

    pgfplots_args = def_opts_pgfplots.copy()
    pgfplots_args.update(pgfplotsset_dict)

    # Check the valid content of `log`
    axis = 'axis'
    if log is not None:
        if log == 'both':
            axis = 'loglogaxis'
        elif log in ['x', 'y']:
            axis = f'semilog{log}axis'
            args[f'{log}min'] = 1
        else:
            raise ValueError("`log` should be one of None, 'x', 'y', 'both'")

    args["xmax"] = len(df)
    args["ymax"] = exclude_treshold if exclude_treshold is not None else df.max().max()

    def col_plot(col):
        values = sorted(list(df[col]))
        if exclude_treshold is not None:
            coords = [f'({i},{values[i]})' for i in range(len(values)) if values[i] < exclude_treshold]
        else:
            coords = [f'({i},{values[i]})' for i in range(len(values))]
        return f'''\\addplot coordinates {{{' '.join(coords)}}};%
\\addlegendentry{{{col}}}%'''

    plots = "\n".join([col_plot(col) for col in df.columns])

    res = f'''
\\pgfplotsset{{
{tikzify_dict(pgfplots_args, 2)}}}
\\begin{{{axis}}}[
{tikzify_dict(args,2)}%
]
{plots}
\\end{{{axis}}}
'''
    return res


def tikzify_dict(args, padding=0):
    """Translates Python dict of args into string to be passed to TikZ code.

    For a pair `k` : `v` we will get `k=v,%\n`, these values are TikZified
    (see further) and merged into a single string.

    TikZification means that we substiture True for "true", False for "false",
    and None for "none".

    Returns a string with TikZ options
    """
    #TODO expand to dicts recursively
    res = ""
    pad = " "*padding
    for k, v in args.items():
        res += pad
        if v is False:
            res += f"{k}=false"
        elif v is True:
            res += f"{k}=true"
        elif v is None:
            res += f"{k}=none"
        else:
            res += f"{k}={v}"
        res += ",%\n"
    return res