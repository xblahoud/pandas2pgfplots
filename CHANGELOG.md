# Changelog
This is Changelog for the pandas2pgfplots project developed by Fanda Blahoudek.
The project provides a basic functionality to produce [pgfplots] code from 
[pandas] DataFrames. 

## [Unreleased]
### Added
 * `display` module that can display plots as SVG in Jupyter
 * wrapper class `Plot` that renders plots in Jupyter as SVG and pgfplots code
     as string in Python console.

### Changed
 * `tikzify` changed to `tikzify_dict`
 * `tikzify_dict` now works on nested dicts
 * functions producing plots return a `Plot` object instead of string

### Requirements
 * Requires now [itikz] and working installation of TeX

## [0.1.0] — 2020-05-08
### Added
 * `tikzify` function that converts a dictionary of key-value pairs into a string
   that can be passed as tikz options 
 * scatter plot (function `scatter`)
 * cactus plot (function `cactus`)

[Unreleased]: https://github.com/xblahoud/pandas2pgfplots/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/xblahoud/pandas2pgfplots/tree/v0.1.0

[itikz]: https://github.com/jbn/itikz/
[pgfplots]: http://pgfplots.sourceforge.net/
[pandas]: https://pandas.pydata.org/