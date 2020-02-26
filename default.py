import os, sys, unicodedata, time
import xbmc, xbmcgui, xbmcaddon, xbmcvfs
import xml.etree.ElementTree as xmltree

__addon__        = xbmcaddon.Addon()
__addonid__      = __addon__.getAddonInfo('id')
__addonversion__ = __addon__.getAddonInfo('version')

def log(txt):
    if isinstance (txt,str):
        txt = txt.decode('utf-8')
    message = u'%s: %s' % (__addonid__, txt)
    xbmc.log(msg=message.encode('utf-8'), level=xbmc.LOGDEBUG)

class Main:
    def __init__( self ):
        self._init_vars()
        # self._parse_argv()
        self._fetch_playlists()
        self._write_playlists()
        self._fetch_icons()
        self._write_icons()

    def _init_vars( self ):
        self.playlists = []
        self.iconlists = []

    def _fetch_playlists( self ):
         # if self.type == 'makelist':  
            path = 'special://profile/playlists/music/'
            dirlist = os.listdir( xbmc.translatePath( path ).decode('utf-8') )

            # log('dirlist: %s' % dirlist)
            log('fetch playlist')
            for item in dirlist:
                playlist = os.path.join( path, item)
                playlistfile = xbmc.translatePath( playlist )
                if item.endswith('.xsp'):
                    contents = xbmcvfs.File(playlistfile, 'r')
                    contents_data = contents.read().decode('utf-8')
                    xmldata = xmltree.fromstring(contents_data.encode('utf-8'))
                    for line in xmldata.getiterator():
                        if line.tag == "name":
                            name = line.text
                            if not name:
                                name = item[:-4]
                            self.playlists.append( (name, playlist) )
                            break
                elif item.endswith('.m3u'):
                    name = item[:-4]
                    self.playlists.append( (name, playlist) )


    def _write_playlists( self ):

        includes_file = xbmc.translatePath("special://skin/720p/IncludePlaylistsList.xml")
                  
        plfile = open(includes_file, "w")
        
        plfile.write ("<?xml version=\"1.0\" encoding=\"UTF-8\"?> \n\n")
        plfile.write ("<includes> \n")
        plfile.write ("<include name=\"PlaylistList\">\n\n")
    
        for idcount, item in enumerate( self.playlists ):
            plfile.write ("<item id=\"%d\">\n"  % (idcount + 1))
            plfile.write ("<label>" + item[0] + "</label>\n")
            plfile.write ("<label2>" + item[0] + ".icon</label2>\n")
            plfile.write ("<icon>$INFO[Skin.String(" + item[0] + ".icon)]</icon>\n")
            plfile.write ("<onclick>ActivateWindow(1120)</onclick>\n")
            plfile.write ("<onclick>PlayMedia(" + item[1] +")</onclick> \n") 
            plfile.write ("<onclick>Skin.SetBool(NotAnAlbum)</onclick>\n")

            plfile.write ("<property name=\"listpath\">" + item[1] + "</property>\n")                        
            plfile.write ("</item> \n\n")
        plfile.write ("</include> \n")
        plfile.write ("</includes> \n")

    def _fetch_icons( self ):
        path = 'special://skin/media/playlist.icons/'
        dirlist = os.listdir( xbmc.translatePath( path ).decode('utf-8') )
        
        # log('dirlist: %s' % dirlist)'
        log('fetch icons')
        for item in dirlist:
            self.iconlists.append( (item[:-4], item) )
            iconlist = os.path.join( path, item)
            iconlistfile = xbmc.translatePath( iconlist )

        # log('playlists: %s' % self.iconlists)

    def _write_icons ( self ):

     includes_file = xbmc.translatePath("special://skin/720p/IncludePlaylistIcons.xml")
              
     plfile = open(includes_file, "w")
     plfile.write ("<?xml version=\"1.0\" encoding=\"UTF-8\"?> \n\n")
     plfile.write ("<includes> \n")
     plfile.write ("<include name=\"PlaylistIcons\">\n\n")
     for idcount, item in enumerate( self.iconlists ):
        plfile.write ("<item id=\"%d\">\n"  % (idcount + 1))
        plfile.write ("<label>" + item[0] + "</label>\n")
        plfile.write ("<label2>playlist.icons/" + item[1] + "</label2>\n")
        plfile.write ("<icon>playlist.icons/" + item[1] + "</icon>\n")
        # plfile.write ("<property name=\"foo\">$NUMBER[%d]</property>\n" % (idcount + 1))
        plfile.write ("</item> \n\n")
     plfile.write ("</include> \n")
     plfile.write ("</includes> \n")
     
     time.sleep(.05)
     # xbmc.executebuiltin('ReloadSkin()')


if ( sys.argv[1] == "makelist" ):
        log('sys.argv makelist')
        Main()
        # xbmc.executebuiltin('ReloadSkin()')
        
if ( sys.argv[1] == "seticon" ):
       log('sys.argv seticon')
       # line1 = "placeholder"
       # line2 = "Showing this message using"
       # line3 = sys.argv[1]
       # xbmcgui.Dialog().ok(line1, line2, line3)
       time.sleep(.2)
    
       iconstring = xbmc.getInfoLabel("Container(50000).ListItem(0).Label2")
       texture = xbmc.getInfoLabel("Container(50000).ListItem(0).Icon")
       xbmc.executebuiltin('ActivateWindow(1170)')
       xbmc.executebuiltin(('Skin.SetString(currentplaylist,%s)') % iconstring)
       xbmc.executebuiltin(('Skin.SetString(currenticon,%s)') % texture)
       # xbmcgui.Dialog().ok(iconstring, texture, texture) 
       log('seticon done')


if ( sys.argv[1] == "editlist" ):
       log('sys.argv editlist')
       line1 = "Status Check"
       line2 = "Showing this message using"
       line3 = sys.argv[1]
       
       stringnameforicon = xbmc.getInfoLabel("Container(50000).ListItem(0).Label2")
       texture = xbmc.getInfoLabel("Container(50000).ListItem(0).Icon")
       editingthelist = xbmc.getInfoLabel("ListItem.Property(listpath)")

       time.sleep(.05)     
       # xbmcgui.Dialog().ok(texture, editingthelist, filestamp, filestamp2)
	   
       xbmc.executebuiltin('ActivateWindow(10136,%s,music)' % editingthelist)
       time.sleep(.05)	   
   
       # time.sleep(3)

       editinglist = "yes"
       # xbmcgui.Dialog().ok(texture, editinglist,editinglist)
       
       while (editinglist == "yes"):
           editinglist = xbmc.getInfoLabel("Skin.String(editinglist)")
           # log("still sleeping")
           time.sleep(.01)
 

       time.sleep(.01) 
       
       playlistfile = xbmc.translatePath( editingthelist )
       contents = xbmcvfs.File(playlistfile, 'r')
       contents_data = contents.read().decode('utf-8')
       xmldata = xmltree.fromstring(contents_data.encode('utf-8'))
       for line in xmldata.getiterator():
        if line.tag == "name":
         newiconname = line.text + ".icon"
         # log("found name")
       
       time.sleep(.01)        
       # newtexture = xbmc.getInfoLabel("Container(50000).ListItem(0).Icon")
       # stringnameforicon2 = xbmc.getInfoLabel("Container(50000).ListItem(0).Label2")
       # log("getting new texture")	   

       # heading = texture + " old texture"  
       # line1 = "new texture"
       # line2 = stringnameforicon + "  old"
       # line3 = newiconname + "  new"

       # xbmcgui.Dialog().ok(heading, line1, line2, line3)
 
       stuff = (newiconname, texture)
       xbmc.executebuiltin(('Skin.SetString(%s,%s)') % stuff)
       time.sleep(.1) 
       log('end editlist')

       xbmc.executebuiltin('ReloadSkin()')

if ( sys.argv[1] == "newlist" ):
       log('sys.argv newlist')
       line1 = "Status Check"
       line2 = "Showing this message using"
       line3 = sys.argv[1]

       
       stringnameforicon = xbmc.getInfoLabel("Container(50000).ListItem(0).Label2")
       texture = xbmc.getInfoLabel("Container(50000).ListItem(0).Icon")

       filestamp1 = str(int(time.time()*100))
       filestamp = str(int(time.time()*100) - (int(time.time()*100)/1000000)*1000000+1000000)
       # log (filestamp1)
       # log (filestamp)
 
       newlist = 'special://profile/playlists/music/'+filestamp+'.xsp'
       translatenewlist = xbmc.translatePath(newlist)

       # xbmcgui.Dialog().ok(texture, filestamp2, newlist, translatenewlist)
 
       plfile = open(translatenewlist, "w+")
       plfile.write ("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\" ?>\n")
       plfile.write ("<smartplaylist type=\"songs\">\n")
       plfile.write ("    <name>new playlist</name>\n")       
       plfile.write ("        <match>all</match>\n")  
       plfile.write ("</smartplaylist>\n")
       plfile.close()
 
       # xbmcgui.Dialog().ok(texture, editingthelist, filestamp, filestamp2)
      
       xbmc.executebuiltin('ActivateWindow(10136,%s,music)' % newlist)

       header = "opened playlist editor"
       line1 = "continue"
       # xbmcgui.Dialog().ok(header, line1)

       # log("sleeping")   
       # log(sys.argv[1])
       time.sleep(.05)	   
       # log("is active")	   
       # time.sleep(3)


       editinglist = "yes"
       # xbmcgui.Dialog().ok(texture, editinglist,editinglist)
       
       while (editinglist == "yes"):
           editinglist = xbmc.getInfoLabel("Skin.String(editinglist)")
           # log("still sleeping")
           time.sleep(.01)

       canceledit = xbmc.getInfoLabel("Skin.String(canceledit)")
       time.sleep(.1)
       log('did we cancel edit?')
       log(canceledit)
       
       if canceledit == "no":
           log('setting icon')


           playlistfile = xbmc.translatePath( newlist )
           contents = xbmcvfs.File(playlistfile, 'r')
           contents_data = contents.read().decode('utf-8')
           xmldata = xmltree.fromstring(contents_data.encode('utf-8'))
           for line in xmldata.getiterator():
            if line.tag == "name":
             newiconname = line.text + ".icon"
             # log("found name")
           
           iconstring = filestamp +".icon"
           texture = "iconmonstr-playlist.png"

           xbmc.executebuiltin('ActivateWindow(1170)')
           xbmc.executebuiltin(('Skin.SetString(currentplaylist,%s)') % newiconname)
           xbmc.executebuiltin(('Skin.SetString(currenticon,%s)') % texture)

 

           
           setnewicon = "yes"
           log('are we setting the new icon?')
           log(setnewicon)
           # xbmcgui.Dialog().ok(texture, newiconname)  
           time.sleep(.2)
           while (setnewicon == "yes"):
             setnewicon = xbmc.getInfoLabel("Skin.String(setnewicon)")
             log(newiconname)
             log("sleeping while setting new icon")
             time.sleep(.01)
             
           time.sleep(.02)        
           # newtexture = xbmc.getInfoLabel("Container(50000).ListItem(0).Icon")
           # stringnameforicon2 = xbmc.getInfoLabel("Container(50000).ListItem(0).Label2")
           # log("getting new texture")	   
        
           log('endedit')

           xbmc.executebuiltin('ReloadSkin()')

       elif canceledit == "yes":
           log ("delete dummy playlistfile")
           log (translatenewlist)
           os.remove(translatenewlist) 

if ( sys.argv[1] == "deletelist" ):
       log('sys.argv editlist')
       line1 = "Status Check"
       line2 = "Showing this message using"
       line3 = sys.argv[1]
       time.sleep(.2)
       
       deletemessage = xbmc.getInfoLabel("Container(50000).ListItem(0).Label")
       texture = xbmc.getInfoLabel("Container(50000).ListItem(0).Icon")
       selectedlist = xbmc.getInfoLabel("ListItem.Property(listpath)")
       deletethelist = xbmc.translatePath( selectedlist )
       
       # xbmcgui.Dialog().ok(selectedlist, deletethelist)
       
       dialog = xbmcgui.Dialog()
       confirmdelete = dialog.yesno('Confirm', 'Do you want to delete playlist?',' ',deletemessage)

       time.sleep(.1)     
       # xbmcgui.Dialog().ok(texture, editingthelist, filestamp, filestamp2)
	   
       log("dialog says!")
       log(confirmdelete)
 
       if confirmdelete == 1:
        log("confirm delete")
        os.remove(deletethelist)
       time.sleep(.1) 
       
       log('endedit')
       Main()
       xbmc.executebuiltin('ReloadSkin()')
       log ('reloadskin')
       # time.sleep(3)

if ( sys.argv[1] == "showlist" ):
        log ('showlist')

        title = "show list"
        HideList = "True"
        # xbmcgui.Dialog().ok(title, HideList, clickdo)  

        if(xbmc.getCondVisibility('Skin.HasSetting(HideList)') == False):
            clickdo = xbmc.getInfoLabel('ListItem.Property(play_song)')
            # positionlabel = xbmc.getInfoLabel('ListItem.Label2')
            # positioninfo = positionlabel.split(",")
            # absolute = positioninfo[0]
            # relative = positioninfo[1]
            # offset = str(21+int(positioninfo[1]))
            # log ('positionlabel')
            # log ('positioninfo')
            # log (positionlabel)
            # log (positioninfo)
            # xbmc.executebuiltin('SetFocus(950)')

            # time.sleep(.05)
            # focuscommand='SetFocus(9900,'+offset+'20,absolute)'
            # xbmc.executebuiltin('focuscommand')
            # line1 = "playsong"
            # xbmcgui.Dialog().ok(title, absolute, relative, offset) 
            xbmc.executebuiltin(clickdo)
        
        time.sleep(.05)
        
        if (xbmc.getCondVisibility('MusicPlayer.offset(-20).Exists')):
            xbmc.executebuiltin('SetFocus(9900,20,absolute)')
            log('-20 exists')
        elif (xbmc.getCondVisibility('MusicPlayer.offset(-19).Exists')):
            xbmc.executebuiltin('SetFocus(9900,19,absolute)')
            log('-19 exists')
        elif (xbmc.getCondVisibility('MusicPlayer.offset(-18).Exists')):
            xbmc.executebuiltin('SetFocus(9900,18,absolute)')
            log('-18 exists')
        elif (xbmc.getCondVisibility('MusicPlayer.offset(-17).Exists')):
            xbmc.executebuiltin('SetFocus(9900,17,absolute)')
            log('-17 exists')
        elif (xbmc.getCondVisibility('MusicPlayer.offset(-16).Exists')):
            xbmc.executebuiltin('SetFocus(9900,16,absolute)')
            log('-16 exists')
        elif (xbmc.getCondVisibility('MusicPlayer.offset(-15).Exists')):
            xbmc.executebuiltin('SetFocus(9900,15,absolute)')
            log('-15 exists')
        elif (xbmc.getCondVisibility('MusicPlayer.offset(-14).Exists')):
            xbmc.executebuiltin('SetFocus(9900,14,absolute)')
            log('-14 exists')
        elif (xbmc.getCondVisibility('MusicPlayer.offset(-13).Exists')):
            xbmc.executebuiltin('SetFocus(9900,13,absolute)')
            log('-13 exists')
        elif (xbmc.getCondVisibility('MusicPlayer.offset(-12).Exists')):
            xbmc.executebuiltin('SetFocus(9900,12,absolute)')
            log('-12 exists')
        elif (xbmc.getCondVisibility('MusicPlayer.offset(-11).Exists')):
            xbmc.executebuiltin('SetFocus(9900,11,absolute)')
            log('-11 exists')
        elif (xbmc.getCondVisibility('MusicPlayer.offset(-10).Exists')):
            xbmc.executebuiltin('SetFocus(9900,10,absolute)')
            log('-10 exists')
        elif (xbmc.getCondVisibility('MusicPlayer.offset(-9).Exists')):
            xbmc.executebuiltin('SetFocus(9900,9,absolute)')
            log('-9 exists')
        elif (xbmc.getCondVisibility('MusicPlayer.offset(-8).Exists')):
            xbmc.executebuiltin('SetFocus(9900,8,absolute)')
            log('-8 exists')
        elif (xbmc.getCondVisibility('MusicPlayer.offset(-7).Exists')):
            xbmc.executebuiltin('SetFocus(9900,7,absolute)')
            log('-7 exists')
        elif (xbmc.getCondVisibility('MusicPlayer.offset(-6).Exists')):
            xbmc.executebuiltin('SetFocus(9900,6,absolute)')
            log('-6 exists')
        elif (xbmc.getCondVisibility('MusicPlayer.offset(-5).Exists')):
            xbmc.executebuiltin('SetFocus(9900,5,absolute)')
            log('-5 exists')
        elif (xbmc.getCondVisibility('MusicPlayer.offset(-4).Exists')):
            xbmc.executebuiltin('SetFocus(9900,4,absolute)')
            log('-4 exists')
        elif (xbmc.getCondVisibility('MusicPlayer.offset(-3).Exists')):
            xbmc.executebuiltin('SetFocus(9900,3,absolute)')
            log('-3 exists')
        elif (xbmc.getCondVisibility('MusicPlayer.offset(-2).Exists')):
            xbmc.executebuiltin('SetFocus(9900,2,absolute)')
            log('-2 exists')
        elif (xbmc.getCondVisibility('MusicPlayer.offset(-1).Exists')):
            xbmc.executebuiltin('SetFocus(9900,1,absolute)')
            log('-1 exists')
        elif (xbmc.getCondVisibility('MusicPlayer.offset(0).Exists')):
            xbmc.executebuiltin('SetFocus(9900,0,absolute)')
            log('0 exists')
   

            
        # xbmcgui.Dialog().ok(title, HideList, clickdo)           
            
       
        xbmc.executebuiltin('Skin.Reset(HideList)')
 
        # ListStatus = xbmc.getCondVisibility("HideList")

        # xbmc.executebuiltin('Skin.SetBool(HideList,False)')
        xbmc.executebuiltin('SetFocus(9900)')        

if ( sys.argv[1] == "hidelist" ):
        # xbmc.executebuiltin('Skin.SetBool(HideList)')
        # ListShow = xbmc.getInfoLabel("Skin.String(ListStatus)")
        title = "hide list"
        # xbmcgui.Dialog().ok(title, ListStatus)
        # xbmc.executebuiltin('SetFocus(9900,20,absolute)')
        
        xbmc.executebuiltin('Skin.SetBool(HideList,True)')
        xbmc.executebuiltin('SetFocus(50000)')  
        

if ( sys.argv[1] == "NeedleUp" ):

        # NeedleFrom = xbmc.getInfoLabel('skin.string(NeedleTo)')
        # xbmc.executebuiltin(('Skin.SetString(NeedleFrom2,%s)') % NeedleFrom)
        # NeedleToInt = int(NeedleFrom)+30 
        # NeedleTo = str(int(NeedleFrom)+30)
        
        # xbmc.executebuiltin(('Skin.SetString(NeedleFrom,%s)') % NeedleFrom)
        # xbmc.executebuiltin(('Skin.SetString(NeedleTo,%s)') % NeedleTo)
        
        # time.sleep(.5)
        # xbmc.executebuiltin('Skin.Reset(RotateNeedle)')
        # time.sleep(.5)
        # xbmc.executebuiltin('Skin.SetBool(RotateNeedle)')

    log ("moving up!!!") 
 
    for angle in range(0, 15):
        
        xbmc.executebuiltin(('Skin.SetString(needleangle,%d)') % angle)
        time.sleep(0.2)
        log(angle) 

        
        
        # log(NeedleFrom) 
        # log(NeedleTo) 

if ( sys.argv[1] == "NeedleDown" ):

        NeedleFrom = xbmc.getInfoLabel('skin.string(NeedleTo)')
        # xbmc.executebuiltin(('Skin.SetString(NeedleFrom2,%s)') % NeedleFrom)
        # NeedleToInt = int(NeedleFrom)-30 
        NeedleTo = str(int(NeedleFrom)-30)
        
        xbmc.executebuiltin(('Skin.SetString(NeedleFrom,%s)') % NeedleFrom)
        xbmc.executebuiltin(('Skin.SetString(NeedleTo,%s)') % NeedleTo)
        
        # time.sleep(.5)
        # xbmc.executebuiltin('Skin.Reset(RotateNeedle)')
        # time.sleep(.5)
        # xbmc.executebuiltin('Skin.SetBool(RotateNeedle)')
        
        log('Needle Down !!!!') 
        log(NeedleFrom) 
        log(NeedleTo) 
# log('script stopped')


