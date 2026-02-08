import win32gui, win32con, win32api
import random
import time
import threading
import os

os.system("pip install pywin32")

icons = [win32con.IDI_WARNING, win32con.IDI_INFORMATION, win32con.IDI_ERROR]

def wnd_proc(hwnd, msg, wparam, lparam):
    if msg == win32con.WM_DESTROY:
        win32gui.PostQuitMessage(0)
        return 0
    return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

def crash_thread():
    try:
        wc = win32gui.WNDCLASS()
        wc.lpfnWndProc = wnd_proc
        wc.lpszClassName = "IconSpamWindow"
        wc.hInstance = win32api.GetModuleHandle(None)
        wc.hbrBackground = win32gui.GetStockObject(win32con.NULL_BRUSH)
        win32gui.RegisterClass(wc)
        
        sw, sh = win32api.GetSystemMetrics(win32con.SM_CXSCREEN), win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        hwnd = win32gui.CreateWindowEx(win32con.WS_EX_TRANSPARENT, "IconSpamWindow", "", win32con.WS_POPUP, 0, 0, sw, sh, 0, 0, wc.hInstance, None)
        print(f"Window handle: {hwnd}")
        if hwnd == 0:
            print("Window creation failed")
            return
        
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, sw, sh, win32con.SWP_SHOWWINDOW)
        hdc = win32gui.GetDC(hwnd)
        loaded_icons = [win32gui.LoadIcon(None, i) for i in icons]
        
        while True:
            w, h = win32gui.GetClientRect(hwnd)[2], win32gui.GetClientRect(hwnd)[3]
            for _ in range(10):
                win32gui.DrawIconEx(hdc, random.randint(0, max(0, w-32)), random.randint(0, max(0, h-32)), random.choice(loaded_icons), 32, 32, 0, None, win32con.DI_NORMAL)
            win32gui.PumpWaitingMessages()
            time.sleep(0.1) 
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Starting icon spam thread...")
    threading.Thread(target=crash_thread, daemon=True).start()
    input("Press Enter to stop...")
