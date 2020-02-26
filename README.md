Credit to ronie for the Playlists Script - https://kodi.wiki/view/Add-on:Playlists_Script, which I used as the starting point for all this.  I'm not sure how much of the original code is recognizable, but it's important to say thanks.

Many thanks to the users on the kodi forums.

INFO FOR USE

This script generates a multitude of results to help with skin.hammernail 

RunScript(script.listhammer,makelist)

    This will generate two include files that provide content to lists.   
    1. IncludePlaylistsList.xml, Include name=PlaylistList
    For each *.xsp playlist, a static list item is created -
        <item id="1">
            <label>theplaylist</label>
            <label2>theplaylist.icon</label2>
            <icon>$INFO[Skin.String(theplaylist.icon)]</icon>
            <onclick>ActivateWindow(1120)</onclick>
            <onclick>PlayMedia(special://profile/playlists/music/theplaylistfile.xsp)</onclick> 
            <onclick>Skin.SetBool(NotAnAlbum)</onclick>
            <property name="listpath">special://profile/playlists/music/theplaylistfile.xsp</property>
        </item> 

    2. IncludePlaylistIcon, include name=PlaylistIcon
    Reads the directory of \media\playlist.icons and creates a static list item
        <item id="1">
            <label>filename</label>
            <label2>playlist.icons/filename.png</label2>
            <icon>playlist.icons/filename.png</icon>
        </item> 

RunScript(script.listhammer,seticon)
Supports changing the assigned playlist icon

RunScript(script.listhammer,editlist)
Supports editing a smartplaylist by passing the right path to smartplaylisteditor.xml
Also keeps icon assignment correct for edited lists

RunScript(script.listhammer,newlist)
Supports creating a new smartplaylist by creating a placeholder file than can be passed to smartplaylisteditor.xml

RunScript(script.listhammer,deletelist)
Deletes the selected playlist

RunScript(script.listhammer,showlist)
Pulls up a list of the songs in the current playlist when on the media player window

RunScript(script.listhammer,hidelist)
hides the list from showlist, above.


