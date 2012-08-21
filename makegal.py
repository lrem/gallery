#!/usr/bin/env python
# vim: set fileencoding=utf8 :

import os
import glob
import time
import argparse

def get_args():
    parser = argparse.ArgumentParser(description = __doc__)
    add = parser.add_argument
    add('path', help="path to the images directory")
    add('--copy', help="copy the images and prepare gallery in this path")
    add('--title', help="Alternative title, default is `dirname`")
    return parser.parse_args()

def main(args):
    if args.copy:
        os.system("cp -a '%s' '%s'" % (args.path, args.copy))
        os.chdir(args.copy)
    else:
        os.chdir(args.path)
    images = glob.glob("*.jpg")
    make_thumbs(images)
    if args.title:
        title = args.title
    else:
        title = os.path.basename(os.path.abspath(os.path.curdir))
    make_index(images, title, 'index.html')

def make_thumbs(images):
    try:
        os.mkdir('thumbs')
    except OSError:
        print "Output already exist, press CTRL-C in 3 seconds to abort"
        time.sleep(3)
    for name in FORMATS:
        try:
            os.mkdir(name)
        except:
            pass # Let's assume that the user really meant not aborting :>
    for image in images:
        os.system("convert -resize 240x160 '%s' '%s'" % 
            (image, 'thumbs/' + image))
        for name in FORMATS:
            os.system("convert -resize %sx%s '%s' '%s'" % 
                (FORMATS[name][0], FORMATS[name][1], image, 
                    os.path.join(name, image)))


def make_index(images, title, fname):
    index = open(fname, 'w')
    print >>index, HEAD % {'title': title}
    for image in images:
        print >>index, IMAGE % {'file': image, 'caption': image}
    print >>index, TAIL

FORMATS = {
        '320p': (480, 320),
        '480p': (720, 480),
        '720p': (1280, 720),
        '1080p': (1920,1080),
        }

HEAD = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title> %(title)s </title>
    <link href="/gallery.css" type="text/css" rel="stylesheet">
    
    <!--
        <script src="/js/jquery-1.7.2.min.js"></script>
        <script src="/js/lightbox.js"></script>
        <link href="/css/lightbox.css" rel="stylesheet" />
    -->

    <script type="text/javascript" src="/jquery-1.8.0.min.js"></script>
    <script type="text/javascript" src="/gallery.js"></script>

    <script type="text/javascript" src="/js/prototype.js"></script>
    <script type="text/javascript" src="/js/scriptaculous.js?load=effects,builder"></script>
    <script type="text/javascript" src="/js/lightboxHTHcustCap2b.js"></script>
    <link rel="stylesheet" href="/css/lightboxHTHcustCap2b.css" type="text/css" />
<script language="JavaScript" type="text/javascript">
function popUp(URL) {
	day = new Date();
	id = day.getTime();
	eval("page" + id + " = window.open(URL, '" + id + "', 'toolbar=0,scrollbars=0,location=0,statusbar=0,copyhistory=no,menubar=0,resizable=1,width='+screen.availWidth*.8+',height='+screen.availHeight*.8+',top = 10');");
}
</script>

    
</head>
<body>
<header>
<h1> %(title)s </h1>
</header>
<p>
Sugeruję na dobry początek włączyć przeglądarkę na pełny ekran (klawisz F11 pod
Firefox, Commad+Shift+F pod Chrome, powinno być też w menu widok). Po
kliknięciu w dowolne zdjęcie włączy się podgląd skalowany do wielkości okna
przeglądarki. Przewijać można myszką albo strzałkami na klawiaturze.
</p>
<hr>
<p>
I suggest making your browser full screen (F11 under Firefox, Command+Shift+F
under Chrome, or search in view menu). After clicking a photo you'll see a
viewer scaled to the window size. Use mouse or arrow keys to scroll.
</p>
<div class="gallery">
'''

IMAGE = '''
<div class="thumb">
<a href="720p/%(file)s" rel="lightbox[gal]">
<img src="thumbs/%(file)s" alt="%(caption)s">
<p>%(caption)s</p>
</a>
</div>
'''

TAIL = '''
</div>
<footer>
&copy; Remigiusz
'<a href="http://lrem.net">lRem</a>'
Modrzejewski
</footer>
</body>
</html>
'''

if __name__ == '__main__':
    main(get_args())
