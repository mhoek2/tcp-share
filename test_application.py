# app core modules
from modules.app.gui import Gui
from modules.app.read_write import ReadWrite
from modules.app.settings import Settings


# import GUI modules
from modules.gui.create_files import *
from modules.gui.share_files import *
from modules.gui.view_files import *
from modules.gui.encrypt_files import *
from modules.gui.decrypt_files import *

# testing
import pytest
from main import Application
from modules.tcp import TCP

@pytest.fixture
def app_instance():
    return Application( pytest=True )

def test_module_instances( app_instance ):
    """Test if modules are set and match the correct class data type"""
    assert isinstance( app_instance.settings,     Settings )

    # app specific modules
    assert isinstance( app_instance.tcp,          TCP )
    assert isinstance( app_instance.read_write,   ReadWrite )
    assert isinstance( app_instance.tk_root,      Gui )

    app_instance.tk_root.destroy()

def test_gui_frames( app_instance ):
    """Test if gui frames/pages class match the required order"""
    num_frames = len(app_instance.tk_root.frames)

    print( f"Num frames: {num_frames}" )

    frames_class = [ GUI_CreateFiles ,
                     GUI_ShareFiles,
                     GUI_ViewFiles,
                     GUI_EncryptFiles,
                     GUI_DecryptFiles ]
    
    for i in range(0, num_frames):
        assert isinstance( app_instance.tk_root.frames[i], frames_class[i] )
    
def test_tcp_pint( app_instance ):
    """Test basic ping and verify type"""
    ping = app_instance.tcp.ping_device( '127.0.0.1' )
    print(f"Able to ping myself: {ping}")
    assert isinstance( ping, bool )

# read-write
def test_read_write_hasShareableFiles( app_instance ):
    """Verify output type"""
    output = app_instance.read_write.hasShareableFiles()
    assert isinstance( output, bool )

def test_read_write_getShareableFiles( app_instance ):
    """Verify output type"""
    output = app_instance.read_write.getShareableFiles()
    assert isinstance( output, list )

def test_read_write_numShareableFiles( app_instance ):
    """Verify output type"""
    output = app_instance.read_write.numShareableFiles
    assert isinstance( output, int )
