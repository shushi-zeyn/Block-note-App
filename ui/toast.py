from PyQt6.QtWidgets import QLabel, QGraphicsOpacityEffect
from PyQt6.QtCore import QTimer, Qt, QPropertyAnimation, QEasingCurve

class Toast(QLabel):
    def __init__(self, parent, text, is_dark=True):
        super().__init__(parent)
        self.setText(text)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        bg = "#333333" if not is_dark else "#F0F0F0"
        color = "#FFFFFF" if not is_dark else "#000000"
        
        # Padding important pour que le texte respire
        self.setStyleSheet(f"""
            background-color: {bg};
            color: {color};
            border-radius: 20px;
            padding: 10px 25px; 
            font-weight: bold;
            font-size: 14px;
        """)
        
        # Ajuster la taille au contenu automatiquement
        self.adjustSize()

        self.move(30, parent.height() - 80)
        self.show()

        # Animation
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        
        self.anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.anim.setDuration(400)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.anim.start()

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.fade_out)
        self.timer.start(2500)

    def fade_out(self):
        self.anim.setDirection(QPropertyAnimation.Direction.Backward)
        self.anim.finished.connect(self.close)
        self.anim.start()
