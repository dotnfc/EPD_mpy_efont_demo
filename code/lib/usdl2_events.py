#
# SDL_EventType from SDL_events.h
#

SDL_FIRSTEVENT     = const(0)

# Application events
SDL_QUIT           = const(0x100) # User-requested quit

# These application events have special meaning on iOS) see README-ios.md for details 
SDL_APP_TERMINATING= const(0x101)        # The application is being terminated by the OS
                            #     Called on iOS in applicationWillTerminate()
                            #     Called on Android in onDestroy()
                            
SDL_APP_LOWMEMORY = const(0x102) # The application is low on memory) free memory if possible.
                            #     Called on iOS in applicationDidReceiveMemoryWarning()
                            #     Called on Android in onLowMemory()
                            
SDL_APP_WILLENTERBACKGROUND= const(0x103) # The application is about to enter the background
                             #    Called on iOS in applicationWillResignActive()
                             #    Called on Android in onPause()
                            
SDL_APP_DIDENTERBACKGROUND= const(0x104) # The application did enter the background and may not get CPU for some time
                            #     Called on iOS in applicationDidEnterBackground()
                            #     Called on Android in onPause()
                            
SDL_APP_WILLENTERFOREGROUND= const(0x105) # The application is about to enter the foreground
                             #   Called on iOS in applicationWillEnterForeground()
                             #   Called on Android in onResume()
                            
SDL_APP_DIDENTERFOREGROUND= const(0x106) # The application is now interactive
                            #    Called on iOS in applicationDidBecomeActive()
                            #    Called on Android in onResume()
                            

# Window events 
SDL_WINDOWEVENT    = const(0x200) # Window state change 
SDL_SYSWMEVENT     = const(0x202) # System specific event 

# Keyboard events 
SDL_KEYDOWN        = const(0x300) # Key pressed 
SDL_KEYUP          = const(0x301) # Key released 
SDL_TEXTEDITING    = const(0x302) # Keyboard text editing (composition) 
SDL_TEXTINPUT      = const(0x303) # Keyboard text input 
SDL_KEYMAPCHANGED  = const(0x304) # Keymap changed due to a system event such as an
                                  # input language or keyboard layout change.
                            

# Mouse events 
SDL_MOUSEMOTION    = const(0x400) # Mouse moved 
SDL_MOUSEBUTTONDOWN= const(0x401) # Mouse button pressed 
SDL_MOUSEBUTTONUP  = const(0x402) # Mouse button released 
SDL_MOUSEWHEEL     = const(0x403) # Mouse wheel motion 

# Joystick events 
SDL_JOYAXISMOTION    = const(0x600) # Joystick axis motion 
SDL_JOYBALLMOTION    = const(0x601) # Joystick trackball motion 
SDL_JOYHATMOTION     = const(0x602) # Joystick hat position change 
SDL_JOYBUTTONDOWN    = const(0x603) # Joystick button pressed 
SDL_JOYBUTTONUP      = const(0x604) # Joystick button released 
SDL_JOYDEVICEADDED   = const(0x605) # A new joystick has been inserted into the system 
SDL_JOYDEVICEREMOVED = const(0x606) # An opened joystick has been removed 

# Game controller events 
SDL_CONTROLLERAXISMOTION  = const(0x650)    # Game controller axis motion 
SDL_CONTROLLERBUTTONDOWN  = const(0x651)    # Game controller button pressed 
SDL_CONTROLLERBUTTONUP    = const(0x652)    # Game controller button released 
SDL_CONTROLLERDEVICEADDED = const(0x653)    # A new Game controller has been inserted into the system 
SDL_CONTROLLERDEVICEREMOVED  = const(0x654) # An opened Game controller has been removed 
SDL_CONTROLLERDEVICEREMAPPED = const(0x655) # The controller mapping was updated 

# Touch events 
SDL_FINGERDOWN      = const(0x700)
SDL_FINGERUP        = const(0x701)
SDL_FINGERMOTION    = const(0x702)

# Gesture events 
SDL_DOLLARGESTURE   = const(0x800)
SDL_DOLLARRECORD    = const(0x801)
SDL_MULTIGESTURE    = const(0x802)

# Clipboard events 
SDL_CLIPBOARDUPDATE = const(0x900) # The clipboard changed 

# Drag and drop events 
SDL_DROPFILE        = const(0x1000) # The system requests a file open 
SDL_DROPTEXT        = const(0x1001) # text/plain drag-and-drop event 
SDL_DROPBEGIN       = const(0x1002) # A new set of drops is beginning (NULL filename) 
SDL_DROPCOMPLETE    = const(0x1003) # Current set of drops is now complete (NULL filename) 

# Audio hotplug events 
SDL_AUDIODEVICEADDED = const(0x1100)  # A new audio device is available 
SDL_AUDIODEVICEREMOVED= const(0x1101) # An audio device has been removed. 

# Render events 
SDL_RENDER_TARGETS_RESET = const(0x2000) # The render targets have been reset and their contents need to be updated 
SDL_RENDER_DEVICE_RESET = const(0x2001) # The device has been reset and all textures need to be recreated

# Events ::SDL_USEREVENT through ::SDL_LASTEVENT are for your use) and should be allocated with SDL_RegisterEvents()
SDL_USEREVENT    = const(0x8000)

# This last event is only for bounding internal arrays
SDL_LASTEVENT    = const(0xFFFF)
