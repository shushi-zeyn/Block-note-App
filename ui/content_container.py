from PyQt6.QtWidgets import QFrame, QVBoxLayout, QWidget, QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt

class ContentContainer(QFrame):

    def __init__(self, content_widget: QWidget, parent=None):
        super().__init__(parent)
        self.setObjectName("ContentContainer")
        
        # Layout interne du conteneur
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30) # Marges internes
        

        layout.addWidget(content_widget)
        

        self._setup_shadow()

    def _setup_shadow(self):
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(40)
        self.shadow.setOffset(0, 10)
        self.setGraphicsEffect(self.shadow)

    def set_shadow_color(self, color):

        if self.graphicsEffect() is None:
            self._setup_shadow()

        if self.shadow:
            try:
                self.shadow.setColor(color)
            except RuntimeError:

                self._setup_shadow()
                self.shadow.setColor(color)
