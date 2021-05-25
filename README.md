# log-spiral-generator

Fusion 360 add-on for generating a logarithmic spiral as a sketch curve.

## Installation

Save the whole repository in `%AppData%\Autodesk\Autodesk Fusion 360\API\AddIns`

### Using git from the command line

```bash
git clone https://github.com/murar8/log-spiral-generator "$env:APPDATA\Autodesk\Autodesk Fusion 360\API\AddIns\Logarithmic Spiral Generator"
```

## Usage

1. ### Create a sketch

    - Go to `Solid` > `Create` > `Create Sketch`

2. ### Launch the script

    - Go to `Sketch` > `Create` > `Logarithmic Spiral`
    - Enter the desired parameters or play around with the handles if going by feel, noting that the number of points determines the dimensional accuracy of the spline.

3. Done!

## How it works

This extension just generates the desired number of points on the spiral, then interpolates them with a spline.

## Donations

[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=WW7VLKVE9YP8Q&source=url)
I do not expect to make any money from this extension but if you would like to buy me a coffee or something you are welcome to do so :)

## License

Copyright (c) 2021 Lorenzo Murarotto <lnzmrr@gmail.com>

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
