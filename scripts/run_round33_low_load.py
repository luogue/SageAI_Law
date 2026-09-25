"""Run one acceptance task on one logical CPU at idle priority on Windows."""
import ctypes
import os
import runpy
import sys

if os.name == 'nt':
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    kernel.SetPriorityClass.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
    handle = kernel.GetCurrentProcess()
    if not kernel.SetProcessAffinityMask(handle, 1):
        raise ctypes.WinError(ctypes.get_last_error())
    if not kernel.SetPriorityClass(handle, 0x40):
        raise ctypes.WinError(ctypes.get_last_error())

target = sys.argv[1]
sys.argv = sys.argv[1:]
if target == '--module':
    module = sys.argv[1]
    sys.argv = sys.argv[1:]
    runpy.run_module(module, run_name='__main__', alter_sys=True)
else:
    runpy.run_path(target, run_name='__main__')
