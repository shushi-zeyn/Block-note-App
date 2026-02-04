from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QStackedWidget, QMessageBox, 
                             QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView, 
                             QMenu, QFrame, QGraphicsDropShadowEffect, QColorDialog)
from PyQt6.QtCore import Qt, QSize, QSettings, QTimer
from PyQt6.QtGui import QIcon, QAction, QColor, QFont, QTextListFormat
from ui.background import AnimatedBackground
from ui.editor_widget import RichTextEdit
from ui.toast import Toast
from ui.content_container import ContentContainer
from database import NoteManager
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NoteBlock")
        
        self.settings = QSettings("MyCompany", "FuturisticNotes")
        
        self.db = NoteManager()
        self.current_note_id = None
        

        self.autosave_timer = QTimer(self)
        self.autosave_timer.setInterval(30000)
        self.autosave_timer.timeout.connect(self.auto_save)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.background = AnimatedBackground(self.central_widget)
        self.background.lower() 
        
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        self.create_header()
        
        self.stack = QStackedWidget()
        self.main_layout.addWidget(self.stack)
        
        self.home_page = self.create_home_page()
        self.list_page = self.create_list_page()
        self.editor_page = self.create_editor_page()
        self.about_page = self.create_about_page()
        
        self.stack.addWidget(self.home_page)
        self.stack.addWidget(self.list_page)
        self.stack.addWidget(self.editor_page)
        self.stack.addWidget(self.about_page)
        
        self.load_settings()
        self.apply_theme()

    def load_settings(self):
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)
        else:
            self.resize(1200, 800)
            
        self.is_dark_theme = self.settings.value("dark_theme", False, type=bool)
        self.auto_save_enabled = self.settings.value("auto_save", False, type=bool)
        self.static_mode_enabled = self.settings.value("static_mode", False, type=bool)
        
        if hasattr(self, 'action_autosave'):
            self.action_autosave.setChecked(self.auto_save_enabled)
        if hasattr(self, 'action_static'):
            self.action_static.setChecked(self.static_mode_enabled)
            
        self.update_static_mode()
        self.update_autosave()

    def closeEvent(self, event):
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("dark_theme", self.is_dark_theme)
        self.settings.setValue("auto_save", self.auto_save_enabled)
        self.settings.setValue("static_mode", self.static_mode_enabled)
        super().closeEvent(event)

    def resizeEvent(self, event):
        if hasattr(self, 'background'):
            self.background.resize(self.central_widget.size())
        super().resizeEvent(event)

    def get_icon_path(self, icon_name):
        return os.path.join("Asset", "ICON", icon_name)

    def create_header(self):
        header_widget = QWidget()
        header_widget.setFixedHeight(70)
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(30, 0, 30, 0)
        
        lbl_logo = QLabel("✨ NoteBlock") # Changement du logo texte
        lbl_logo.setStyleSheet("font-size: 22px; font-weight: 800; font-family: 'Segoe UI';")
        header_layout.addWidget(lbl_logo)
        
        header_layout.addStretch()
        
        # Bouton Paramètres
        self.settings_btn = QPushButton()
        self.settings_btn.setFixedSize(45, 45)
        self.settings_btn.setObjectName("IconBtn")
        self.settings_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.settings_btn.setIconSize(QSize(24, 24))
        
        self.settings_menu = QMenu(self)
        self.action_autosave = QAction("Sauvegarde Auto (30s)", self)
        self.action_autosave.setCheckable(True)
        self.action_autosave.triggered.connect(self.toggle_autosave)
        self.settings_menu.addAction(self.action_autosave)
        
        self.action_static = QAction("Mode Statique", self)
        self.action_static.setCheckable(True)
        self.action_static.triggered.connect(self.toggle_static_mode)
        self.settings_menu.addAction(self.action_static)
        
        self.settings_btn.setMenu(self.settings_menu)
        header_layout.addWidget(self.settings_btn)
        
        # Bouton Thème
        self.theme_btn = QPushButton()
        self.theme_btn.setFixedSize(45, 45)
        self.theme_btn.setObjectName("IconBtn")
        self.theme_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.theme_btn.setIconSize(QSize(24, 24))
        self.theme_btn.clicked.connect(self.toggle_theme)
        header_layout.addWidget(self.theme_btn)
        
        self.main_layout.addWidget(header_widget)
        self.header_widget = header_widget

    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        self.apply_theme()
        mode = "Sombre" if self.is_dark_theme else "Clair"
        Toast(self, f"Thème : {mode}", self.is_dark_theme)

    def toggle_autosave(self):
        self.auto_save_enabled = self.action_autosave.isChecked()
        self.update_autosave()
        state = "Activée" if self.auto_save_enabled else "Désactivée"
        Toast(self, f"Auto-save : {state}", self.is_dark_theme)

    def update_autosave(self):
        if self.auto_save_enabled:
            if not self.autosave_timer.isActive():
                self.autosave_timer.start()
        else:
            self.autosave_timer.stop()

    def auto_save(self):
        if self.stack.currentWidget() == self.editor_page:
            title = self.title_edit.text()
            if title:
                content = self.text_edit.toHtml()
                if self.current_note_id is None:
                    self.db.add_note(title, content, self.current_status)
                else:
                    self.db.update_note(self.current_note_id, title, content, self.current_status)
                print("Auto-save effectué")

    def toggle_static_mode(self):
        self.static_mode_enabled = self.action_static.isChecked()
        self.update_static_mode()
        self.apply_theme()

    def update_static_mode(self):
        self.background.set_static_mode(self.static_mode_enabled)

    def apply_theme(self):
        if self.is_dark_theme:
            self.theme_btn.setIcon(QIcon(self.get_icon_path("wht_sun.png")))
            self.settings_btn.setIcon(QIcon(self.get_icon_path("wht_setting.png")))
            
            text_color = "#E3E3E3"
            header_bg = "#121212"
            
            container_bg = "#1E1E1E"
            
            self.btn_bg_color = "#2D2D2D"
            self.btn_hover_color = "#3D3D3D"
            self.toolbar_checked_color = "#5A5A5A"
            
            btn_checked = "#0D47A1"
            menu_bg = "#2D2D2D"
            shadow_color = QColor(0, 0, 0, 150)
        else:
            self.theme_btn.setIcon(QIcon(self.get_icon_path("BLK_moon.png")))
            self.settings_btn.setIcon(QIcon(self.get_icon_path("blk_setting.png")))
            
            text_color = "#1F1F1F"
            header_bg = "#F5F7FA"
            
            container_bg = "#E8F0FE" 
            
            self.btn_bg_color = "#FFFFFF"
            self.btn_hover_color = "#D2E3FC"
            self.toolbar_checked_color = "#AECBFA"
            
            btn_checked = "#AECBFA"
            menu_bg = "#FFFFFF"
            shadow_color = QColor(0, 0, 0, 40)

        self.background.set_theme(self.is_dark_theme)
        self.header_widget.setStyleSheet(f"background-color: {header_bg}; border-bottom: none;")

        for widget in [self.home_container, self.list_container, self.about_container, self.editor_container]:
            self.add_shadow(widget)
            widget.set_shadow_color(shadow_color)
            widget.setStyleSheet(f"background-color: {container_bg}; border-radius: 24px;")

        style = f"""
            QWidget {{ color: {text_color}; }}
            QLabel {{ color: {text_color}; }}
            
            QPushButton {{
                background-color: {self.btn_bg_color};
                color: {text_color};
                border: none;
            }}
            QPushButton:hover {{
                background-color: {self.btn_hover_color};
            }}
            
            QPushButton#IconBtn {{
                background-color: transparent;
                border: none;
            }}
            QPushButton#IconBtn:hover {{
                background-color: {self.btn_hover_color};
                border-radius: 22px;
            }}
            
            QPushButton:checked {{
                background-color: {btn_checked};
            }}
            
            QPushButton#PrimaryBtn {{
                background-color: {self.btn_bg_color};
                color: {text_color};
                border: 2px solid {text_color};
                font-weight: bold;
            }}
            QPushButton#PrimaryBtn:hover {{
                background-color: {self.btn_hover_color};
                border: 2px solid {text_color};
            }}
            
            #ContentContainer {{
                background-color: {container_bg};
                border: none;
            }}
            
            QTextEdit, QLineEdit {{
                background-color: transparent;
                color: {text_color};
                selection-background-color: #1A73E8;
                selection-color: white;
            }}
            
            QMenu {{
                background-color: {menu_bg};
                color: {text_color};
                border: 1px solid {self.btn_hover_color};
            }}
            QMenu::item:selected {{
                background-color: {self.btn_hover_color};
            }}
            
            QPushButton#ToolBtn {{
                border-radius: 8px;
                padding: 5px;
                min-width: 32px;
                font-weight: bold;
            }}
        """
        self.setStyleSheet(style)
        self.update_toolbar_state()

    def add_shadow(self, widget):
        if widget.graphicsEffect() is None:
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(30)
            shadow.setOffset(0, 8)
            shadow.setColor(QColor(0, 0, 0, 50))
            widget.setGraphicsEffect(shadow)

    # --- PAGES ---

    def create_home_page(self):
        page = QWidget()
        page.setStyleSheet("background-color: transparent;") 
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        content_widget = QWidget()
        box_layout = QVBoxLayout(content_widget)
        box_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        box_layout.setSpacing(25)
        
        title = QLabel("Bonjour Shushi")
        title.setStyleSheet("font-size: 36px; font-weight: 800; background: transparent;")
        box_layout.addWidget(title)
        
        subtitle = QLabel("Prêt à créer quelque chose de génial ?")
        subtitle.setStyleSheet("font-size: 16px; opacity: 0.7; background: transparent;")
        box_layout.addWidget(subtitle)
        
        box_layout.addSpacing(10)
        
        btn_add = QPushButton("+ Nouvelle Note")
        btn_add.setObjectName("PrimaryBtn")
        btn_add.setFixedSize(220, 55)
        btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add.clicked.connect(self.start_new_note)
        
        btn_list = QPushButton("Mes Notes")
        btn_list.setFixedSize(220, 55)
        btn_list.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_list.clicked.connect(self.show_notes_list)
        
        btn_about = QPushButton("À propos")
        btn_about.setFixedSize(220, 55)
        btn_about.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_about.clicked.connect(lambda: self.stack.setCurrentWidget(self.about_page))
        
        box_layout.addWidget(btn_add)
        box_layout.addWidget(btn_list)
        box_layout.addWidget(btn_about)
        
        self.home_container = ContentContainer(content_widget)
        self.home_container.setFixedSize(500, 500)
        self.add_shadow(self.home_container)
        
        layout.addWidget(self.home_container)
        return page

    def create_list_page(self):
        page = QWidget()
        page.setStyleSheet("background-color: transparent;")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(50, 20, 50, 20)
        
        content_widget = QWidget()
        box_layout = QVBoxLayout(content_widget)
        
        top_layout = QHBoxLayout()
        title = QLabel("Mes Notes")
        title.setStyleSheet("font-size: 28px; font-weight: bold; background: transparent;")
        top_layout.addWidget(title)
        top_layout.addStretch()
        
        btn_back = QPushButton()
        btn_back.setIcon(QIcon(self.get_icon_path("left-arrow.png")))
        btn_back.setFixedSize(45, 45)
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_back.clicked.connect(self.go_back_home)
        top_layout.addWidget(btn_back)
        box_layout.addLayout(top_layout)
        
        self.notes_table = QTableWidget()
        self.notes_table.setColumnCount(4)
        self.notes_table.setHorizontalHeaderLabels(["Titre", "Date", "Statut", "ID"])
        self.notes_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.notes_table.setColumnHidden(3, True)
        self.notes_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.notes_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.notes_table.setShowGrid(False)
        self.notes_table.verticalHeader().setVisible(False)
        self.notes_table.doubleClicked.connect(self.open_selected_note)
        box_layout.addWidget(self.notes_table)
        
        action_layout = QHBoxLayout()
        btn_del = QPushButton("Supprimer")
        btn_del.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_del.clicked.connect(self.delete_selected_note)
        action_layout.addStretch()
        action_layout.addWidget(btn_del)
        box_layout.addLayout(action_layout)
        
        self.list_container = ContentContainer(content_widget)
        self.add_shadow(self.list_container)
        
        layout.addWidget(self.list_container)
        return page

    def create_editor_page(self):
        page = QWidget()
        page.setStyleSheet("background-color: transparent;")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(50, 20, 50, 20)
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(15)
        
        header_layout = QHBoxLayout()
        
        btn_back = QPushButton()
        btn_back.setIcon(QIcon(self.get_icon_path("left-arrow.png")))
        btn_back.setFixedSize(45, 45)
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_back.clicked.connect(self.go_back_home)
        header_layout.addWidget(btn_back)
        
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Titre de la note")
        self.title_edit.setStyleSheet("font-size: 24px; font-weight: bold; background: transparent; border: none;")
        header_layout.addWidget(self.title_edit)
        
        self.btn_status = QPushButton("En cours")
        self.btn_status.setFixedSize(130, 40)
        self.btn_status.setCursor(Qt.CursorShape.PointingHandCursor)
        self.status_menu = QMenu(self)
        self.status_menu.addAction("En cours", lambda: self.set_status("En cours"))
        self.status_menu.addAction("Terminé", lambda: self.set_status("Terminé"))
        self.btn_status.setMenu(self.status_menu)
        header_layout.addWidget(self.btn_status)
        
        btn_save = QPushButton("Sauvegarder")
        btn_save.setObjectName("PrimaryBtn")
        btn_save.setFixedSize(130, 40)
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save.clicked.connect(self.save_note)
        header_layout.addWidget(btn_save)
        
        content_layout.addLayout(header_layout)
        
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setSpacing(8)
        
        self.btn_bold = QPushButton("B")
        self.btn_bold.setObjectName("ToolBtn")
        self.btn_bold.setCheckable(True)
        self.btn_bold.setFixedSize(36, 36)
        self.btn_bold.toggled.connect(self.toggle_bold)
        
        self.btn_italic = QPushButton("I")
        self.btn_italic.setObjectName("ToolBtn")
        self.btn_italic.setCheckable(True)
        self.btn_italic.setFixedSize(36, 36)
        self.btn_italic.toggled.connect(self.toggle_italic)
        
        self.btn_underline = QPushButton("U")
        self.btn_underline.setObjectName("ToolBtn")
        self.btn_underline.setCheckable(True)
        self.btn_underline.setFixedSize(36, 36)
        self.btn_underline.toggled.connect(self.toggle_underline)
        
        btn_color = QPushButton("🎨")
        btn_color.setObjectName("ToolBtn")
        btn_color.setFixedSize(36, 36)
        btn_color.clicked.connect(self.choose_text_color)
        
        toolbar_layout.addWidget(self.btn_bold)
        toolbar_layout.addWidget(self.btn_italic)
        toolbar_layout.addWidget(self.btn_underline)
        toolbar_layout.addWidget(btn_color)
        
        toolbar_layout.addSpacing(15)
        
        btn_list_menu = QPushButton("Liste ▾")
        btn_list_menu.setObjectName("ToolBtn")
        btn_list_menu.setFixedSize(80, 36)
        
        list_menu = QMenu(self)
        list_menu.addAction("• Puces", lambda: self.text_edit.create_list(QTextListFormat.Style.ListDisc))
        list_menu.addAction("1. Chiffres", lambda: self.text_edit.create_list(QTextListFormat.Style.ListDecimal))
        list_menu.addAction("A. Lettres", lambda: self.text_edit.create_list(QTextListFormat.Style.ListUpperAlpha))
        list_menu.addAction("I. Romains", lambda: self.text_edit.create_list(QTextListFormat.Style.ListUpperRoman))
        
        btn_list_menu.setMenu(list_menu)
        toolbar_layout.addWidget(btn_list_menu)
        
        toolbar_layout.addStretch()
        content_layout.addLayout(toolbar_layout)
        
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Plain)
        line.setStyleSheet("background-color: rgba(128, 128, 128, 0.2);")
        line.setFixedHeight(1)
        content_layout.addWidget(line)
        
        self.text_edit = RichTextEdit()
        self.text_edit.cursorPositionChanged.connect(self.update_toolbar_state)
        content_layout.addWidget(self.text_edit)
        
        self.editor_container = ContentContainer(content_widget)
        self.add_shadow(self.editor_container)
        
        layout.addWidget(self.editor_container)
        return page

    def create_about_page(self):
        page = QWidget()
        page.setStyleSheet("background-color: transparent;")
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        content_widget = QWidget()
        box_layout = QVBoxLayout(content_widget)
        box_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title = QLabel("À PROPOS")
        title.setStyleSheet("font-size: 32px; font-weight: bold; background: transparent;")
        content = QLabel("NoteBlock Beta\n\nMade by Shushi")
        content.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content.setStyleSheet("background: transparent;")
        
        btn_back = QPushButton("Retour")
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_back.clicked.connect(self.go_back_home)
        
        box_layout.addWidget(title)
        box_layout.addWidget(content)
        box_layout.addSpacing(20)
        box_layout.addWidget(btn_back)
        
        self.about_container = ContentContainer(content_widget)
        self.about_container.setFixedSize(500, 300)
        self.add_shadow(self.about_container)
        
        layout.addWidget(self.about_container)
        return page

    def update_button_style(self, button, is_checked):
        if is_checked:
            button.setStyleSheet(f"background-color: {self.toolbar_checked_color};")
        else:
            button.setStyleSheet(f"background-color: {self.btn_bg_color};")

    def toggle_bold(self, checked):
        self.text_edit.setFontWeight(QFont.Weight.Bold if checked else QFont.Weight.Normal)
        self.update_button_style(self.btn_bold, checked)
        self.text_edit.setFocus()

    def toggle_italic(self, checked):
        self.text_edit.setFontItalic(checked)
        self.update_button_style(self.btn_italic, checked)
        self.text_edit.setFocus()

    def toggle_underline(self, checked):
        self.text_edit.setFontUnderline(checked)
        self.update_button_style(self.btn_underline, checked)
        self.text_edit.setFocus()

    def update_toolbar_state(self):
        fmt = self.text_edit.currentCharFormat()
        
        is_bold = fmt.fontWeight() == QFont.Weight.Bold
        self.btn_bold.setChecked(is_bold)
        self.update_button_style(self.btn_bold, is_bold)
        
        is_italic = fmt.fontItalic()
        self.btn_italic.setChecked(is_italic)
        self.update_button_style(self.btn_italic, is_italic)
        
        is_underline = fmt.fontUnderline()
        self.btn_underline.setChecked(is_underline)
        self.update_button_style(self.btn_underline, is_underline)

    def go_back_home(self):
        self.stack.setCurrentWidget(self.home_page)

    def start_new_note(self):
        self.current_note_id = None
        self.title_edit.clear()
        self.text_edit.clear()
        self.set_status("En cours")
        self.stack.setCurrentWidget(self.editor_page)

    def show_notes_list(self):
        self.refresh_notes_list()
        self.stack.setCurrentWidget(self.list_page)

    def refresh_notes_list(self):
        self.notes_table.setRowCount(0)
        notes = self.db.get_all_notes()
        for row_idx, (note_id, title, date, status) in enumerate(notes):
            self.notes_table.insertRow(row_idx)
            self.notes_table.setItem(row_idx, 0, QTableWidgetItem(title))
            self.notes_table.setItem(row_idx, 1, QTableWidgetItem(date))
            self.notes_table.setItem(row_idx, 2, QTableWidgetItem(status))
            self.notes_table.setItem(row_idx, 3, QTableWidgetItem(str(note_id)))

    def open_selected_note(self):
        selected = self.notes_table.selectedItems()
        if not selected: return
        row = selected[0].row()
        note_id = int(self.notes_table.item(row, 3).text())
        
        note = self.db.get_note_content(note_id)
        if note:
            title, content, status = note
            self.current_note_id = note_id
            self.title_edit.setText(title)
            self.text_edit.setHtml(content)
            self.set_status(status)
            self.stack.setCurrentWidget(self.editor_page)

    def delete_selected_note(self):
        selected = self.notes_table.selectedItems()
        if not selected: return
        row = selected[0].row()
        note_id = int(self.notes_table.item(row, 3).text())
        
        confirm = QMessageBox.question(self, "Confirmer", "Supprimer ?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            self.db.delete_note(note_id)
            self.refresh_notes_list()
            Toast(self, "Note supprimée", self.is_dark_theme)

    def save_note(self):
        title = self.title_edit.text()
        content = self.text_edit.toHtml()
        if not title:
            QMessageBox.warning(self, "Erreur", "Titre requis")
            return
        if self.current_note_id is None:
            self.db.add_note(title, content, self.current_status)
            Toast(self, "Note créée !", self.is_dark_theme)
        else:
            self.db.update_note(self.current_note_id, title, content, self.current_status)
            Toast(self, "Note sauvegardée", self.is_dark_theme)
        self.show_notes_list()

    def set_status(self, status):
        self.current_status = status
        self.btn_status.setText(status)
        if status == "Terminé":
            self.btn_status.setStyleSheet("background-color: #E6F4EA; color: #137333; border: none; border-radius: 18px;")
        else:
            self.btn_status.setStyleSheet("background-color: #FEF7E0; color: #B06000; border: none; border-radius: 18px;")

    def choose_text_color(self):
        color = QColorDialog.getColor(self.text_edit.textColor(), self)
        if color.isValid():
            self.text_edit.setTextColor(color)
