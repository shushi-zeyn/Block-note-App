import random
import math
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QTimer, Qt, QPointF, QRectF
from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QPainterPath

class FloatingElement:
    def __init__(self, width, height):
        self.reset(width, height)
        self.y = random.randint(0, height)
        self.opacity = random.randint(0, 100)

    def reset(self, width, height):
        self.x = random.randint(0, width)
        self.y = height + 100
        self.speed = random.uniform(0.5, 1.5)
        self.opacity = 0
        self.fading_in = True
        self.rotation = random.randint(0, 360)
        self.rot_speed = random.uniform(-1, 1)
        
        self.type = random.choice(['text', 'atom', 'cube', 'dna', 'gear'])
        
        if self.type == 'text':
            self.content = random.choice([
                "E=mc²", "φ = 1.618", "0xDEADBEEF", "SYSTEM_READY", 
                "ANALYSIS", "BLUEPRINT", "V.1.0.4", "LOADING..."
            ])
            self.size = random.randint(10, 18)
        else:
            self.size = random.randint(30, 80)

    def update(self, width, height):
        self.y -= self.speed
        self.rotation += self.rot_speed
        
        if self.y < -150:
            self.reset(width, height)

        if self.fading_in:
            self.opacity += 1.5
            if self.opacity >= 120:
                self.fading_in = False
        else:
            if random.random() < 0.005:
                self.opacity -= 1
        
        self.opacity = max(0, min(255, self.opacity))

class AnimatedBackground(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.elements = []
        self.is_static = False # Mode sans animation
        
        for _ in range(25):
            self.elements.append(FloatingElement(1920, 1080))
            
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(30)
        
        self.bg_color = QColor(0, 0, 0)
        self.pen_color = QColor(255, 255, 255)

    def set_theme(self, is_dark):
        if is_dark:
            self.bg_color = QColor(18, 18, 18) # Noir doux
            self.pen_color = QColor(255, 255, 255)
        else:
            self.bg_color = QColor(240, 242, 245) # Gris très clair
            self.pen_color = QColor(20, 20, 20)

    def set_static_mode(self, enabled):
        self.is_static = enabled
        if enabled:
            self.timer.stop()
            self.update() # Redessiner une dernière fois (juste le fond)
        else:
            if not self.timer.isActive():
                self.timer.start(30)

    def update_animation(self):
        if self.is_static: return
        
        w = self.width()
        h = self.height()
        if w <= 0: return
        for el in self.elements:
            el.update(w, h)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Fond
        painter.fillRect(self.rect(), self.bg_color)
        

        if self.is_static:
            return
        
        for el in self.elements:
            if el.opacity <= 0: continue
            
            c = QColor(self.pen_color)
            c.setAlpha(int(el.opacity))
            pen = QPen(c, 1.5)
            pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            
            painter.save()
            painter.translate(el.x, el.y)
            painter.rotate(el.rotation)
            
            if el.type == 'text':
                painter.rotate(-el.rotation)
                font = QFont("Courier New", el.size)
                font.setBold(True)
                painter.setFont(font)
                painter.drawText(0, 0, el.content)
            elif el.type == 'atom':
                painter.drawEllipse(-5, -5, 10, 10)
                painter.drawEllipse(-el.size//2, -el.size//4, el.size, el.size//2)
                painter.rotate(60)
                painter.drawEllipse(-el.size//2, -el.size//4, el.size, el.size//2)
                painter.rotate(60)
                painter.drawEllipse(-el.size//2, -el.size//4, el.size, el.size//2)
            elif el.type == 'cube':
                s = el.size // 2
                painter.drawRect(-s, -s, s*2, s*2)
                offset = s // 2
                painter.drawRect(-s+offset, -s-offset, s*2, s*2)
                painter.drawLine(-s, -s, -s+offset, -s-offset)
                painter.drawLine(s, -s, s+offset, -s-offset)
                painter.drawLine(s, s, s+offset, s-offset)
                painter.drawLine(-s, s, -s+offset, s-offset)
            elif el.type == 'dna':
                path = QPainterPath()
                h = el.size
                w = el.size // 3
                path.moveTo(0, -h//2)
                path.cubicTo(w, -h//4, -w, h//4, 0, h//2)
                painter.drawPath(path)
                for i in range(-h//2, h//2, 10):
                    painter.drawLine(-5, i, 5, i)
            elif el.type == 'gear':
                painter.drawEllipse(-el.size//2, -el.size//2, el.size, el.size)
                painter.drawEllipse(-el.size//4, -el.size//4, el.size//2, el.size//2)
                for i in range(0, 360, 45):
                    painter.rotate(45)
                    painter.drawLine(0, -el.size//2, 0, -el.size//2 - 10)

            painter.restore()
