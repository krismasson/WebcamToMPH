import mss
import mss.tools


monitor = {"left": 5, "top": 750, "width": 1380, "height": 330}
with mss.mss() as sct:
    img = sct.grab(monitor)
    mss.tools.to_png(img.rgb, img.size, output="captured_frame.png")