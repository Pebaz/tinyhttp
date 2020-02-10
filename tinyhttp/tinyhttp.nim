#[
The MIT License (MIT)

Copyright (c) 2015 Fabio Cevasco

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
]#

import 
    asynchttpserver, 
    asyncdispatch, 
    os, strutils, 
    mimetypes, 
    times, 
    strutils,
    uri,
    nimpy

from httpcore import HttpMethod, HttpHeaders

const style = "style.css".slurp

type 
    NimHttpResponse* = tuple[
        code: HttpCode,
        content: string,
        headers: HttpHeaders]
    NimHttpSettings* = object
        logging*: bool
        directory*: string
        mimes*: MimeDb
        port*: Port
        address*: string
        name: string
        version*: string

proc h_page(settings:NimHttpSettings, content: string, title=""): string =
    var footer = """<div id="footer">$1 v$2</div>""" % [settings.name, settings.version]
    result = """
<!DOCTYPE html>
<html>
    <head>
        <title>$1</title>
        <style type="text/css">$2</style>
        <meta charset="UTF-8">
    </head>
    <body>
        <h1>$1</h1>
        $3
        $4
    </body>
</html>
    """ % [title, style, content, footer]

proc relativePath(path, cwd: string): string =
    var path2 = path
    if cwd == "/":
        return path
    else:
        path2.delete(0, cwd.len-1)
    var relpath = path2.replace("\\", "/")
    if (not relpath.endsWith("/")) and (not path.existsFile):
        relpath = relpath&"/"
    if not relpath.startsWith("/"):
        relpath = "/"&relpath
    return relpath

proc relativeParent(path, cwd: string): string =
    var relparent = path.parentDir.relativePath(cwd)
    if relparent == "":
        return "/"
    else: 
        return relparent

proc sendNotFound(settings: NimHttpSettings, path: string): NimHttpResponse = 
    var content = "<p>The page you requested cannot be found.<p>"
    return (code: Http404, content: h_page(settings, content, $Http404), headers: newHttpHeaders())

proc sendNotImplemented(settings: NimHttpSettings, path: string): NimHttpResponse =
    var content = "<p>This server does not support the functionality required to fulfill the request.</p>"
    return (code: Http501, content: h_page(settings, content, $Http501), headers: newHttpHeaders())

proc sendStaticFile(settings: NimHttpSettings, path: string): NimHttpResponse =
    let mimes = settings.mimes
    var ext = path.splitFile.ext
    if ext == "":
        ext = ".txt"

    var file = path.readFile
    if ext == ".md":
        file = "<meta charset=utf-8><link rel=stylesheet href=https://casual-effects.com/markdeep/latest/apidoc.css?>" & file & "<script src=https://casual-effects.com/markdeep/latest/markdeep.min.js? charset=utf-8></script>"

    ext = ext[1 .. ^1]
    let mimetype = mimes.getMimetype(ext.toLowerAscii)
    return (code: Http200, content: file, headers: {"Content-Type": mimetype}.newHttpHeaders)

proc sendDirContents(settings: NimHttpSettings, path: string): NimHttpResponse = 
    let cwd = settings.directory
    var res: NimHttpResponse
    var files = newSeq[string](0)
    if path != cwd and path != cwd&"/" and path != cwd&"\\":
        files.add """<li class="i-back entypo"><a href="$1">..</a></li>""" % [path.relativeParent(cwd)]
    var title = "Index of " & path.relativePath(cwd)
    for i in walkDir(path):
        let name = i.path.extractFilename
        let relpath = i.path.relativePath(cwd)
        if name == "index.html" or name == "index.htm":
            return sendStaticFile(settings, i.path)
        if i.path.existsDir:
            files.add """<li class="i-folder entypo"><a href="$1">$2</a></li>""" % [relpath, name]
        else:
            files.add """<li class="i-file entypo"><a href="$1">$2</a></li>""" % [relpath, name]
    let ul = """
<ul>
    $1
</ul>
""" % [files.join("\n")]
    res = (code: Http200, content: h_page(settings, ul, title), headers: newHttpHeaders())
    return res

proc printReqInfo(settings: NimHttpSettings, req: Request) =
    if not settings.logging:
        return
    echo getTime().local, " - ", req.hostname, " ", req.reqMethod, " ", req.url.path

proc handleCtrlC() {.noconv.} =
    echo "\nExiting..."
    quit()

setControlCHook(handleCtrlC)

proc serve(settings: NimHttpSettings) =
    var server = newAsyncHttpServer()
    proc handleHttpRequest(req: Request): Future[void] {.async.} =
        printReqInfo(settings, req)
        let path = settings.directory/req.url.path.replace("%20", " ").decodeUrl()
        var res: NimHttpResponse 
        if req.reqMethod != HttpGet:
            res = sendNotImplemented(settings, path)
        elif path.existsDir:
            res = sendDirContents(settings, path)
        elif path.existsFile:
            res = sendStaticFile(settings, path)
        else:
            res = sendNotFound(settings, path)
        await req.respond(res.code, res.content, res.headers)
    echo settings.name, " v", settings.version, " started on port ", int(settings.port)
    echo "Serving directory ", settings.directory
    asyncCheck server.serve(settings.port, handleHttpRequest, settings.address)


proc serve_static_files*(
    host: string, port: int, dir: string, log: bool=false
) {.exportpy.} =
    const version = staticRead(currentSourcePath() / "../../VERSION.txt")
    var settings: NimHttpSettings
    settings.name = "tinyhttp"
    settings.version = version
    settings.directory = getCurrentDir() / dir
    settings.logging = log
    settings.mimes = newMimeTypes()
    settings.mimes.register("html", "text/html")
    settings.mimes.register("md", "text/html")

    var text_files = @[
        "txt", "py", "c", "cpp", "hpp", "css", "nim", "html", "js", "java",
        "sh", "rs", "cs", "lc", "json", "csv"
    ]
    for ext in text_files:
        settings.mimes.register(ext, "text/plain")
    
    settings.address = host
    settings.port = Port(port)
    serve(settings)

    asyncdispatch.runForever()
