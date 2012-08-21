JQ = jQuery.noConflict()

resolutions = [[480, 320], [720, 480], [1280, 720], [1920,1080]]

adapt_resolution = () ->
    # I find it weird, but this returns the last one, what is what I want
    ok = res for res in resolutions when (
        res[0] <= JQ(window).width() and res[1] <= JQ(window).height())
    format = "#{ok[1]}p"
    JQ("div.thumb a").attr("href", (index, oldv) -> 
        "#{format}/#{oldv.split(/\//)[1]}")

JQ -> 
    adapt_resolution()
    JQ(window).resize(adapt_resolution)
