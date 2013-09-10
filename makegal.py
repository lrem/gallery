#!/usr/bin/env python
# vim: set fileencoding=utf8 :

import os
import glob
import time
import argparse


def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    add = parser.add_argument
    add('path', help="path to the images directory")
    add('--copy', help="copy the images and prepare gallery in this path")
    add('--title', help="Alternative title, default is `dirname`")
    add('--html', help="HTML only (don't scale images)", action='store_true')
    add('--desc', help="gallery description file", default="desc.txt")
    return parser.parse_args()


def main(args):
    if args.copy:
        os.system("cp -a '%s' '%s'" % (args.path, args.copy))
        os.chdir(args.copy)
    else:
        os.chdir(args.path)
    images = glob.glob("*.jpg")
    if not args.html:
        make_thumbs(images)
    if args.title:
        title = args.title
    else:
        title = os.path.basename(os.path.abspath(os.path.curdir))
    desc = ''
    if os.path.exists(args.desc):
        desc = '<div id="desc">' + open(args.desc).read() + '</div>'
    make_index(images, title, desc, 'index.html')


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
            pass  # Let's assume that the user really meant not aborting :>
    for image in images:
        os.system("convert -resize 240x160 '%s' '%s'" %
                  (image, 'thumbs/' + image))
        for name in FORMATS:
            os.system("convert -resize %sx%s '%s' '%s'" %
                      (FORMATS[name][0], FORMATS[name][1], image,
                       os.path.join(name, image)))


def make_index(images, title, desc, fname):
    index = open(fname, 'w')
    print >>index, HEAD % {'title': title, 'desc': desc}
    for image in images:
        print >>index, IMAGE % {'file': image, 'caption': image}
    print >>index, TAIL

FORMATS = {
    '320p': (480, 320),
    '480p': (720, 480),
    '720p': (1280, 720),
    '1080p': (1920, 1080)
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
    <nav>
        <ul>
            <li>Format:</li>
            <li><a href="#">320p</a></li>
            <li><a href="#">480p</a></li>
            <li class="active"><a href="#">720p</a></li>
            <li><a href="#">1080p</a></li>
            <li><a href="#">Full</a></li>
        </ul>
    </nav>

    <h1> %(title)s </h1>
</header>
%(desc)s
<div id="help">
<p>
Sugeruję na dobry początek włączyć przeglądarkę na pełny ekran (klawisz F11 pod
Firefox, Commad+Shift+F pod Chrome, powinno być też w menu widok). Po
kliknięciu w dowolne zdjęcie włączy się podgląd skalowany do wielkości okna
przeglądarki. Przewijać można myszką albo strzałkami na klawiaturze.
</p>
<p>
Menu u góry pozwala wybrać format zdjęć. Im bardziej w prawo, tym większa
jakość, ale też tym większy plik do ściągnięcia. Domyślnie, automatycznie
wybrany jest największy format jaki w całości zmieści się w oknie. Po
wyborze większego, będzie on pokazywany przeskalowany do wielkości okna.
</p>
<hr>
<p>
I suggest making your browser full screen (F11 under Firefox, Command+Shift+F
under Chrome, or search in view menu). After clicking a photo you'll see a
viewer scaled to the window size. Use mouse or arrow keys to scroll.
</p>
<p>
Menu on the top allows you to choose image format. The more right, the bigger
format and bigger file to download. By default, it is automatically set to the
biggest one that fully fits in the window. If you choose a bigger one, it will
be scaled down to fill the window.
</p>
</div>
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
