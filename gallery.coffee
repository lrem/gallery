JQ = jQuery.noConflict()

resolutions = [[480, 320], [720, 480], [1280, 720], [1920,1080]]

set_format = (format) ->
    if format is "Full"
        format = "."
    JQ("div.thumb a").attr("href", (index, oldv) -> 
        "#{format}/#{oldv.split(/\//)[1]}")
    JQ("nav li.active").removeClass("active")
    JQ("nav li:contains('#{format}')").addClass("active")

adapt_resolution = () ->
    # I find it weird, but this returns the last one, what is what I want
    ok = res for res in resolutions when (
        res[0] <= JQ(window).width() and res[1] <= JQ(window).height())
    set_format "#{ok[1]}p"

selector_clicked = () ->
    set_format JQ(this).html()

arm_selector = () ->
    JQ("nav a").click(selector_clicked)

JQ -> 
    adapt_resolution()
    arm_selector()
    JQ(window).resize(adapt_resolution)
