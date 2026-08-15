import numpy as np
import cv2 as cv

from backend.enums.annotation_type import AnnotationType
from backend.config.selector_config import SelectorConfig as CFG
from backend.core.prediction import Prediction
from frontend.opencv.config import BARS, FONT, FONT_SCL, TXT_CLR, THICK


class OpenCVFrontend:
    def __init__(self, manager):
        self.manager = manager
        self.active_bars = {k: False for k in BARS}

    def _to_prediction(self, obj):
        if obj is None:
            return None
        if isinstance(obj, Prediction):
            return obj
        return Prediction(obj.item_id, obj.workspace)

    def run(self) -> None:
        while True:
            canvas = np.full((CFG.WIN_HEIGHT, CFG.WIN_WIDTH, 3), CFG.BG_COLOR, dtype=np.uint8)

            waiting = getattr(self.manager, "is_waiting", lambda: False)()
            if waiting:
                self._draw_waiting(canvas)
            else:
                self._draw_bars(canvas)
                self._draw_current_prediction(canvas)

            cv.imshow("canvas", canvas)
            self._reset_bars()
            key = cv.waitKey(35)
            if key != -1:
                self._handle_key(key)
            if key == 27:
                self.manager.finalize()
                break

    def _draw_waiting(self, canvas: np.ndarray) -> None:
        msg = "Waiting for annotation..."
        size = cv.getTextSize(msg, FONT, 1.0, 2)[0]
        x = (CFG.WIN_WIDTH - size[0]) // 2
        y = CFG.WIN_HEIGHT // 2
        cv.putText(canvas, msg, (x, y), FONT, 1.0, (180, 180, 180), 2, cv.LINE_AA)
        total = getattr(self.manager, "get_total", lambda: 0)()
        if total:
            sub = f"Done: {total}"
            cx = (CFG.WIN_WIDTH - cv.getTextSize(sub, FONT, 0.6, 1)[0][0]) // 2
            cv.putText(canvas, sub, (cx, y + 40), FONT, 0.6, (120, 120, 120), 1, cv.LINE_AA)

    def _draw_bars(self, canvas: np.ndarray) -> None:
        for side, ((x1, y1), (x2, y2)) in BARS.items():
            color = CFG.BAR_COLORS[side] if self.active_bars[side] else CFG.BG_COLOR
            cv.rectangle(canvas, (x1, y1), (x2, y2), color, -1)
        cv.putText(canvas, "REJECT", (15, CFG.WIN_HEIGHT // 2), FONT, FONT_SCL, TXT_CLR, THICK, cv.LINE_AA)
        cv.putText(canvas, "ACCEPT", (CFG.WIN_WIDTH - 80, CFG.WIN_HEIGHT // 2), FONT, FONT_SCL, TXT_CLR, THICK, cv.LINE_AA)
        cv.putText(canvas, "BACK", (CFG.WIN_WIDTH // 2, 30), FONT, FONT_SCL, TXT_CLR, THICK, cv.LINE_AA)
        cv.putText(canvas, "SKIP", (CFG.WIN_WIDTH // 2, CFG.WIN_HEIGHT - 30), FONT, FONT_SCL, TXT_CLR, THICK, cv.LINE_AA)

    def _draw_current_prediction(self, canvas: np.ndarray) -> None:
        raw = self.manager.get_current()
        pred = self._to_prediction(raw)
        if pred is None or pred.image is None:
            return
        orig_h, orig_w = pred.image.shape[:2]
        img_w = CFG.WIN_WIDTH - 2 * CFG.BAR_WIDTH
        ratio = img_w / orig_w
        img_h = int(orig_h * ratio)
        image = cv.resize(pred.image, (img_w, img_h), interpolation=cv.INTER_AREA)
        canvas[CFG.BAR_HEIGHT:CFG.BAR_HEIGHT + img_h,
               CFG.BAR_WIDTH:CFG.BAR_WIDTH + img_w] = image
        for annot in pred.annotations:
            class_color = CFG.CLASS_COLORS.get(annot.class_index, (255, 255, 255))
            if annot.annotation_type == AnnotationType.BBOX:
                self._draw_bbox(canvas, annot, img_w, img_h, class_color)
            elif annot.annotation_type == AnnotationType.POLYGON:
                self._draw_polygon(canvas, annot, img_w, img_h, class_color)

    def _draw_bbox(self, canvas, annot, img_w, img_h, color):
        x1 = int(CFG.BAR_WIDTH + img_w * (annot.x - annot.width / 2))
        y1 = int(CFG.BAR_HEIGHT + img_h * (annot.y - annot.height / 2))
        x2 = int(CFG.BAR_WIDTH + img_w * (annot.x + annot.width / 2))
        y2 = int(CFG.BAR_HEIGHT + img_h * (annot.y + annot.height / 2))
        cv.rectangle(canvas, (x1, y1), (x2, y2), color, 1)

    def _draw_polygon(self, canvas, annot, img_w, img_h, color):
        pts = np.array(
            [[int(CFG.BAR_WIDTH + img_w * x), int(CFG.BAR_HEIGHT + img_h * y)] for x, y in annot.points],
            dtype=np.int32,
        )
        if len(pts) >= 3:
            cv.polylines(canvas, [pts], isClosed=True, color=color, thickness=1)

    def _handle_key(self, key: int) -> None:
        if key == ord("a"):
            self.manager.reject()
            self.active_bars["left"] = True
            print("Reject")
        elif key == ord("d"):
            self.manager.accept()
            self.active_bars["right"] = True
            print("Accept")
        elif key == ord("w"):
            self.manager.back()
            self.active_bars["top"] = True
            print("Back")
        elif key == ord("s"):
            self.manager.skip()
            self.active_bars["bottom"] = True
            print("Skip")

    def _reset_bars(self) -> None:
        for k in self.active_bars:
            self.active_bars[k] = False
