from mmap import mmap, ACCESS_WRITE
import win32security
import win32con
import win32file

class ChuniIO:
    _buffer = None
    _accessor = None
    _init = False
    
    SENSOR_MAP = [1, 0, 3, 2, 5, 4]
    
    @classmethod
    def send(cls, sensors):
        if not cls._init:
            cls.initialize()
        
        data = bytearray(6)
        for i in range(6):
            data[cls.SENSOR_MAP[i]] = 0x80 if sensors[i].hand_detected else 0x00
        
        cls._accessor.seek(0)
        cls._accessor.write(bytes(data))
    
    @classmethod
    def initialize(cls):
        security_descriptor = win32security.SECURITY_DESCRIPTOR()
        security_descriptor.Initialize()
        
        world_sid = win32security.CreateWellKnownSid(win32security.WinWorldSid)
        
        sa = win32security.SECURITY_ATTRIBUTES()
        sa.SECURITY_DESCRIPTOR = security_descriptor
        
        dacl = win32security.ACL()
        dacl.AddAccessAllowedAce(
            win32security.ACL_REVISION,
            win32con.GENERIC_ALL,
            world_sid
        )
        security_descriptor.SetSecurityDescriptorDacl(1, dacl, 0)
        
        try:
            cls._buffer = mmap(
                -1,
                1024,
                tagname="Local\\BROKENITHM_SHARED_BUFFER",
                access=ACCESS_WRITE
            )
        except Exception:
            handle = win32file.CreateFileMapping(
                win32file.INVALID_HANDLE_VALUE,
                sa,
                win32con.PAGE_READWRITE,
                0,
                1024,
                "Local\\BROKENITHM_SHARED_BUFFER"
            )
            
            cls._buffer = mmap(
                handle.Detach(),
                1024,
                access=ACCESS_WRITE
            )
        
        cls._accessor = cls._buffer
        cls._init = True
    
    @classmethod
    def close(cls):
        if cls._init:
            cls._buffer.close()
            cls._init = False