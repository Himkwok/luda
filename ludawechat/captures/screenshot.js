var page = new WebPage(),
    address, outfile, width, height, clip_height;

address = require('system').args[1];
outfile = require('system').args[2];
/*
console.debug(address)
console.debug(outfile)*/

/*width = 1024;
 clip_height = height = 800;

 page.clipRect = {width: width, height: clip_height};*/
page.viewportSize = {width: 900, height: 800};
/*console.debug(page.clipRect.height)
console.debug(page.clipRect.width)*/
page.open(address, function (status) {
    if (status !== 'success') {
        phantom.exit(1);
    } else {
        page.render(outfile);
        phantom.exit();
    }
});