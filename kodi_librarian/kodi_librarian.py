from kodijson import Kodi
kodi = Kodi("http://<the android box's IP>:8080/jsonrpc")

# This returns a complex Python dict, but all I needed her was the `tvshowid`
tv_show = kodi.VideoLibrary.GetTVShows(
    filter={"field": "title", "operator": "contains", "value": "adventure"}
)
tv_show_id = tv_show["result"]["tvshows"][0]["tvshowid"]

# Now that I have the tv show id, I can get a list of episodes, filtering for `playcount < 1`
# The filtration syntax is very powerful, but not at all obvious from the machine-generated docs.
# I figured it out by looking at code samples for an old version of the API and hoped things
# hadn't changed too much:
# https://www.programcreek.com/python/exam...uteJSONRPC
kodi.VideoLibrary.GetEpisodes(
    tvshowid=tv_show_id,
    properties=[
        "season",
        "episode",
        "playcount",
        "file"
    ],
    filter={
        "field": "playcount",
        "operator": "lessthan",
        "value": "1"
    }
)