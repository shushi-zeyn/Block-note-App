from PyQt6.QtWidgets import QTextEdit, QMenu, QColorDialog, QFontDialog
from PyQt6.QtGui import QAction, QTextCursor, QTextListFormat, QColor, QTextCharFormat, QFont
from PyQt6.QtCore import Qt

class RichTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptRichText(True)
        self.setTabChangesFocus(False) # Important pour gérer la tabulation nous-mêmes

    def keyPressEvent(self, event):
        cursor = self.textCursor()
        

        if event.key() == Qt.Key.Key_Tab:
            if cursor.currentList():

                list_fmt = cursor.currentList().format()
                list_fmt.setIndent(list_fmt.indent() + 1)
                cursor.createList(list_fmt)
                return
        
        # Shift+Tab pour désindenter
        if event.key() == Qt.Key.Key_Backtab:
            if cursor.currentList():
                list_fmt = cursor.currentList().format()
                indent = list_fmt.indent()
                if indent > 1:
                    list_fmt.setIndent(indent - 1)
                    cursor.createList(list_fmt)
                else:

                    block_fmt = cursor.blockFormat()
                    block_fmt.setObjectIndex(-1)
                    cursor.setBlockFormat(block_fmt)
                return

        super().keyPressEvent(event)

    def contextMenuEvent(self, event):
        # Menu contextuel personnalisé (Clic Droit)
        menu = self.createStandardContextMenu()
        menu.addSeparator()
        
        # --- Formatage ---
        format_menu = menu.addMenu("Formatage")
        
        action_bold = QAction("Gras", self)
        action_bold.setCheckable(True)
        action_bold.setChecked(self.fontWeight() == QFont.Weight.Bold)
        action_bold.triggered.connect(lambda: self.setFontWeight(QFont.Weight.Bold if action_bold.isChecked() else QFont.Weight.Normal))
        format_menu.addAction(action_bold)
        
        action_italic = QAction("Italique", self)
        action_italic.setCheckable(True)
        action_italic.setChecked(self.fontItalic())
        action_italic.triggered.connect(lambda: self.setFontItalic(action_italic.isChecked()))
        format_menu.addAction(action_italic)
        
        action_underline = QAction("Souligné", self)
        action_underline.setCheckable(True)
        action_underline.setChecked(self.fontUnderline())
        action_underline.triggered.connect(lambda: self.setFontUnderline(action_underline.isChecked()))
        format_menu.addAction(action_underline)

        # --- Couleur & Surlignage ---
        color_menu = menu.addMenu("Couleurs")
        
        action_text_color = QAction("Couleur du texte...", self)
        action_text_color.triggered.connect(self.choose_text_color)
        color_menu.addAction(action_text_color)
        
        action_highlight = QAction("Surligner (Jaune)", self)
        action_highlight.triggered.connect(lambda: self.setTextBackgroundColor(QColor("yellow")))
        color_menu.addAction(action_highlight)
        
        action_no_highlight = QAction("Effacer surlignage", self)
        action_no_highlight.triggered.connect(lambda: self.setTextBackgroundColor(QColor("transparent")))
        color_menu.addAction(action_no_highlight)

        # --- Listes ---
        list_menu = menu.addMenu("Listes")
        
        action_bullet = QAction("• Puces", self)
        action_bullet.triggered.connect(lambda: self.create_list(QTextListFormat.Style.ListDisc))
        list_menu.addAction(action_bullet)
        
        action_number = QAction("1. Numérotée", self)
        action_number.triggered.connect(lambda: self.create_list(QTextListFormat.Style.ListDecimal))
        list_menu.addAction(action_number)

        menu.exec(event.globalPos())

    def choose_text_color(self):
        color = QColorDialog.getColor(self.textColor(), self)
        if color.isValid():
            self.setTextColor(color)

    def create_list(self, style):
        cursor = self.textCursor()
        cursor.createList(style)
