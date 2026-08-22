from frontend_open.pyqt.config import MIN_HEIGHT, MIN_WIDTH, WINDOW_TITLE
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction, QColor, QImage, QKeySequence, QPainter, QPen, QPixmap
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from backend.config.selector_config import SelectorConfig as CFG
from backend.pipeline_engine.prediction import Prediction
from backend.enums.annotation_type import AnnotationType


class PyQtFrontend(QMainWindow):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self._build_ui()
        self._setup_timer()
        self._prediction = None

    def _build_ui(self) -> None:
        self.setWindowTitle(WINDOW_TITLE)
        self.setMinimumSize(MIN_WIDTH, MIN_HEIGHT)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet('background-color: #333;')
        self.image_label.setFixedSize(CFG.WIN_WIDTH - 2 * CFG.BAR_WIDTH, CFG.WIN_HEIGHT - CFG.BAR_HEIGHT)

        side = QVBoxLayout()
        self.stats_label = QLabel('Total: 0\nAccepted: 0\nRejected: 0')
        self.stats_label.setStyleSheet('font-size: 14px; padding: 10px;')

        self.waiting_label = QLabel('')
        self.waiting_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.waiting_label.setStyleSheet('font-size: 18px; color: #666;')

        btn_accept = QPushButton('Accept  (D)')
        btn_accept.clicked.connect(self._accept)
        btn_reject = QPushButton('Reject  (A)')
        btn_reject.clicked.connect(self._reject)
        btn_skip = QPushButton('Skip  (S)')
        btn_skip.clicked.connect(self._skip)
        btn_back = QPushButton('Back  (W)')
        btn_back.clicked.connect(self._back)

        side.addWidget(self.stats_label)
        side.addStretch()
        side.addWidget(self.waiting_label)
        side.addWidget(btn_accept)
        side.addWidget(btn_reject)
        side.addWidget(btn_skip)
        side.addWidget(btn_back)

        layout.addWidget(self.image_label, 1)
        layout.addLayout(side)

        for key, slot in [
            (Qt.Key.Key_D, self._accept),
            (Qt.Key.Key_A, self._reject),
            (Qt.Key.Key_S, self._skip),
            (Qt.Key.Key_W, self._back),
            (Qt.Key.Key_Escape, self.close),
        ]:
            act = QAction(self)
            act.setShortcut(QKeySequence(key))
            act.triggered.connect(slot)
            self.addAction(act)

    def _setup_timer(self) -> None:
        self.timer = QTimer()
        self.timer.timeout.connect(self._update)
        self.timer.start(100)

    def _accept(self) -> None:
        self.manager.accept()
        self._prediction = None

    def _reject(self) -> None:
        self.manager.reject()
        self._prediction = None

    def _skip(self) -> None:
        self.manager.skip()
        self._prediction = None

    def _back(self) -> None:
        if self.manager.back():
            self._prediction = None

    def _to_prediction(self, obj):
        if obj is None:
            return None
        if isinstance(obj, Prediction):
            return obj
        return Prediction(obj.item_id, obj.workspace)

    def _update(self) -> None:
        waiting = getattr(self.manager, 'is_waiting', lambda: False)()
        self.waiting_label.setText('Waiting for annotation...' if waiting else '')

        if self._prediction is None:
            raw = self.manager.get_current()
            self._prediction = self._to_prediction(raw) if raw is not None else None

        self._update_stats()
        self._render()

    def _update_stats(self) -> None:
        total = getattr(self.manager, 'get_total', lambda: 0)()
        self.stats_label.setText(f'Total: {total}\nAccepted: -\nRejected: -')

    def _render(self) -> None:
        pred = self._prediction
        if pred is None or pred.image is None:
            self.image_label.clear()
            return

        h, w, ch = pred.image.shape
        bytes_per_line = ch * w
        qimage = QImage(pred.image.data, w, h, bytes_per_line, QImage.Format.Format_BGR888)

        label_w = self.image_label.width()
        label_h = self.image_label.height()
        scaled = qimage.scaled(
            label_w, label_h, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.FastTransformation
        )

        pixmap = QPixmap.fromImage(scaled)
        painter = QPainter(pixmap)

        scale_x = scaled.width() / w
        scale_y = scaled.height() / h

        for annot in pred.annotations:
            b, g, r = CFG.CLASS_COLORS.get(annot.class_index, (255, 255, 255))
            pen = QPen(QColor(r, g, b))
            pen.setWidth(2)
            painter.setPen(pen)

            if annot.annotation_type == AnnotationType.BBOX:
                x1 = int((annot.x - annot.width / 2) * w * scale_x)
                y1 = int((annot.y - annot.height / 2) * h * scale_y)
                x2 = int((annot.x + annot.width / 2) * w * scale_x)
                y2 = int((annot.y + annot.height / 2) * h * scale_y)
                painter.drawRect(x1, y1, x2 - x1, y2 - y1)

            elif annot.annotation_type == AnnotationType.POLYGON:
                pts = [(int(x * w * scale_x), int(y * h * scale_y)) for x, y in annot.points]
                if len(pts) >= 2:
                    for i in range(len(pts)):
                        painter.drawLine(pts[i][0], pts[i][1], pts[(i + 1) % len(pts)][0], pts[(i + 1) % len(pts)][1])

        painter.end()
        self.image_label.setPixmap(pixmap)
