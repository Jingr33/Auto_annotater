import cv2 as cv

from src.backend.config.selector_config import SelectorConfig as CFG

FONT = cv.FONT_HERSHEY_SIMPLEX
FONT_SCL = 0.6
TXT_CLR = (255, 255, 255)
THICK = 2

BARS = {
    'left': ((0, 0), (CFG.BAR_WIDTH, CFG.WIN_HEIGHT)),
    'right': ((CFG.WIN_WIDTH - CFG.BAR_WIDTH, 0), (CFG.WIN_WIDTH, CFG.WIN_HEIGHT)),
    'top': ((CFG.BAR_WIDTH, 0), (CFG.WIN_WIDTH - CFG.BAR_WIDTH, CFG.BAR_HEIGHT)),
    'bottom': ((CFG.BAR_WIDTH, CFG.WIN_HEIGHT - CFG.BAR_HEIGHT), (CFG.WIN_WIDTH - CFG.BAR_WIDTH, CFG.WIN_HEIGHT)),
}
