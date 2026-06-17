import sys, os

from PySide6.QtCore import Slot, QMimeData
from PySide6.QtGui import QIcon, QAction, QFont, QTextDocument
from PySide6.QtPrintSupport import QPrinter, QPrintDialog
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QTextEdit,
    QLabel,
    QMessageBox,
    QFontDialog,
    QInputDialog,
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Untitled - Notepad")
        self.resize(1000, 600)

        # I inserted added this class to paste only the text, because by default it pastes also the foreground/background colors which is not what I want, it breaks the minimalist layout I'm trying to achieve
        class PlainTextEdit(QTextEdit):
            def insertFromMimeData(self, source: QMimeData):
                self.insertPlainText(source.text())

        self.text_editor = PlainTextEdit()
        font = QFont("Consolas", 12)
        self.text_editor.setFont(font)
        self.text_editor.setStyleSheet("border-style: none")
        self.default_font_size = 12
        self.current_font_size = 12
        self.current_file = None
        self.find_text = ""

        self.setCentralWidget(self.text_editor)
        self.text_editor.selectionChanged.connect(self.selection_changed)
        self.default_font_size = self.text_editor.font().pointSize()
        self.text_editor.cursorPositionChanged.connect(self.cursor_position)

        # defining some actions :

        # new file action
        self.new_file_action = QAction(QIcon("icons/new.png"), "&New file", self)
        self.new_file_action.setShortcut("Ctrl+N")
        self.new_file_action.setStatusTip("New file")
        self.new_file_action.triggered.connect(self.new_file)

        # new window action
        self.new_window_action = QAction(QIcon("icons/copy.png"), "&New window", self)
        self.new_window_action.setShortcut("Ctrl+Shift+N")
        self.new_window_action.setStatusTip("New window")
        self.new_window_action.triggered.connect(self.new_window)

        # open file action
        self.open_file_action = QAction(QIcon("icons/open.png"), "&Open file", self)
        self.open_file_action.setShortcut("Ctrl+O")
        self.open_file_action.setStatusTip("Open file")
        self.open_file_action.triggered.connect(self.open_file)

        # save file action
        self.save_file_action = QAction(QIcon("icons/save.png"), "&Save file", self)
        self.save_file_action.setShortcut("Ctrl+S")
        self.save_file_action.setStatusTip("Save file")
        self.save_file_action.triggered.connect(self.save_file)

        # save file as action
        self.save_file_as_action = QAction(
            QIcon("icons/save_as.png"), "&Save file as...", self
        )
        self.save_file_as_action.setShortcut("Ctrl+Shift+S")
        self.save_file_as_action.setStatusTip("Save file as")
        self.save_file_as_action.triggered.connect(self.save_file_as)

        # print file action
        self.print_file_action = QAction(QIcon("icons/print.png"), "&Print file", self)
        self.print_file_action.setShortcut("Ctrl+P")
        self.print_file_action.setStatusTip("Print file")
        self.print_file_action.triggered.connect(self.print_file)

        # close window action
        self.close_window_action = QAction(QIcon("icons/no.png"), "&Close window", self)
        self.close_window_action.setShortcut("Ctrl+W")
        self.close_window_action.setStatusTip("Close window")
        self.close_window_action.triggered.connect(self.close)

        # exit action
        self.exit_action = QAction(QIcon("icons/exit.png"), "&Exit", self)
        self.exit_action.setShortcut("Ctrl+Q")
        self.exit_action.setStatusTip("Exit")
        self.exit_action.triggered.connect(self.close_all_windows)

        # undo action
        self.undo_action = QAction(QIcon("icons/undo.png"), "&Undo", self)
        self.undo_action.setShortcut("Ctrl+Z")
        self.undo_action.setStatusTip("Undo")
        self.undo_action.setEnabled(False)
        self.undo_action.triggered.connect(self.text_editor.undo)

        # redo action
        self.redo_action = QAction(QIcon("icons/redo.png"), "&Redo", self)
        self.redo_action.setShortcut("Ctrl+Y")
        self.redo_action.setStatusTip("Redo")
        self.redo_action.setEnabled(False)
        self.redo_action.triggered.connect(self.text_editor.redo)

        self.text_editor.undoAvailable.connect(self.undo_action.setEnabled)
        self.text_editor.redoAvailable.connect(self.redo_action.setEnabled)

        # copy action
        self.copy_action = QAction(QIcon("icons/copy.png"), "&Copy", self)
        self.copy_action.setShortcut("Ctrl+C")
        self.copy_action.setStatusTip("Copy text")
        self.copy_action.setEnabled(False)
        self.copy_action.triggered.connect(self.text_editor.copy)

        # cut action
        self.cut_action = QAction(QIcon("icons/cut.png"), "&Cut", self)
        self.cut_action.setShortcut("Ctrl+X")
        self.cut_action.setStatusTip("Cut text")
        self.cut_action.setEnabled(False)
        self.cut_action.triggered.connect(self.text_editor.cut)

        # paste action
        self.paste_action = QAction(QIcon("icons/paste.png"), "&Paste", self)
        self.paste_action.setShortcut("Ctrl+V")
        self.paste_action.setStatusTip("Paste text")
        self.paste_action.triggered.connect(self.text_editor.paste)

        # delete action
        self.delete_action = QAction(QIcon("icons/remove.png"), "&Delete", self)
        self.delete_action.setShortcut("Del")
        self.delete_action.setStatusTip("Delete text")
        self.delete_action.setEnabled(False)
        self.delete_action.triggered.connect(self.delete_text)

        # find action
        self.find_action = QAction(QIcon("icons/find.png"),"&Find...", self)
        self.find_action.setShortcut("Ctrl+F")
        self.find_action.setStatusTip("Find text")
        self.find_action.triggered.connect(self.find)

        # select all action
        self.select_all_action = QAction("&Select all", self)
        self.select_all_action.setShortcut("Ctrl+A")
        self.select_all_action.setStatusTip("Select all")
        self.select_all_action.triggered.connect(self.text_editor.selectAll)

        # font action
        self.choose_font_action = QAction("&Font...", self)
        self.choose_font_action.setStatusTip("Change font")
        self.choose_font_action.triggered.connect(self.choose_font)

        # Zoom in action
        self.zoom_in_action = QAction(QIcon("icons/zoom_in.png"), "&Zoom in\tCtrl+", self)
        self.zoom_in_action.setShortcut("Ctrl+=")
        self.zoom_in_action.setStatusTip("Zoom in")
        self.zoom_in_action.triggered.connect(self.zoom_in)

        # zoom out action
        self.zoom_out_action = QAction(QIcon("icons/zoom_out.png"), "&Zoom out", self)
        self.zoom_out_action.setShortcut("Ctrl+-")
        self.zoom_out_action.setStatusTip("Zoom out")
        self.zoom_out_action.triggered.connect(self.zoom_out)

        # reset zoom action
        self.reset_zoom_action = QAction("&Reset zoom", self)
        self.reset_zoom_action.setShortcut("Ctrl+0")
        self.reset_zoom_action.setStatusTip("Reset zoom")
        self.reset_zoom_action.triggered.connect(self.reset_zoom)

        # status bar action
        self.toggle_status_bar_action = QAction("&Status bar", self)
        self.toggle_status_bar_action.setStatusTip("Toggle status bar")
        self.toggle_status_bar_action.setCheckable(True)
        self.toggle_status_bar_action.setChecked(True)
        self.toggle_status_bar_action.triggered.connect(self.toggle_status_bar)

        # word wrap action
        self.toggle_word_wrap_action = QAction("&Word wrap", self)
        self.toggle_word_wrap_action.setStatusTip("Toggle word wrap")
        self.toggle_word_wrap_action.setCheckable(True)
        self.toggle_word_wrap_action.setChecked(True)
        self.toggle_word_wrap_action.triggered.connect(self.toggle_word_wrap)

        menu_bar = self.menuBar()

        # File menu
        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction(self.new_file_action)
        file_menu.addAction(self.new_window_action)
        file_menu.addAction(self.open_file_action)
        file_menu.addAction(self.save_file_action)
        file_menu.addAction(self.save_file_as_action)
        file_menu.addSeparator()
        file_menu.addAction(self.print_file_action)
        file_menu.addSeparator()
        file_menu.addAction(self.close_window_action)
        file_menu.addAction(self.exit_action)

        # Edit menu
        edit_menu = menu_bar.addMenu("&Edit")
        edit_menu.addAction(self.undo_action)
        edit_menu.addAction(self.redo_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.copy_action)
        edit_menu.addAction(self.cut_action)
        edit_menu.addAction(self.paste_action)
        edit_menu.addAction(self.delete_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.select_all_action)
        edit_menu.addAction(self.find_action)
        # edit_menu.addAction(self.find_next_action)
        # edit_menu.addAction(self.find_previous_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.choose_font_action)

        # view menu
        view_menu = menu_bar.addMenu("&View")
        zoom_menu = view_menu.addMenu("&Zoom")
        zoom_menu.addAction(self.zoom_in_action)
        zoom_menu.addAction(self.zoom_out_action)
        zoom_menu.addAction(self.reset_zoom_action)
        view_menu.addAction(self.toggle_word_wrap_action)
        view_menu.addAction(self.toggle_status_bar_action)

        # status bar
        status_bar = self.statusBar()
        status_bar.setStyleSheet("background-color: #cccccc;")
        self.zoom_label = QLabel("Zoom : 100%")
        self.cursor_label = QLabel("Ln 0 col 0")

        separator_1 = QLabel("        ")
        separator_2 = QLabel("        ")

        status_bar.addPermanentWidget(self.cursor_label)
        status_bar.addPermanentWidget(separator_1)
        status_bar.addPermanentWidget(self.zoom_label)
        status_bar.addPermanentWidget(separator_2)
        status_bar.addPermanentWidget(QLabel("UTF-8"))

    @Slot()
    def new_file(self):
        if self.text_editor.document().isModified():
            ret = QMessageBox.question(
                self,
                "Unsaved changes",
                "You have unsaved changes. Create a file anyway ?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if ret == QMessageBox.StandardButton.No:
                return
        self.text_editor.clear()
        self.current_file = None
        self.setWindowTitle("Untitled - Notepad")
        self.statusBar().showMessage("New file created")

    @Slot()
    def new_window(self):
        window = MainWindow()
        window.show()
        QApplication.instance().windows.append(window)

    @Slot()
    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open file", ".", "Text Files (*.txt);;All Files (*)"
        )
        if not file_path:
            return
        try:
            with open(file_path, "r", encoding="UTF-8") as file:
                self.text_editor.setPlainText(file.read())
            self.setWindowTitle(f"{os.path.basename(file_path)} - Notepad")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not open file: {e}")

    @Slot()
    def save_file(self):
        if not self.current_file:
            return self.save_file_as()
        else:
            try:
                with open(self.current_file, "w", encoding="UTF-8") as file:
                    file.write(self.text_editor.toPlainText())
                self.text_editor.document().setModified(False)
                self.setWindowTitle(f"{os.path.basename(self.current_file)} - Notepad")
                self.statusBar().showMessage(
                    f"Saved: {os.path.basename(self.current_file)}"
                )
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save file: {e}")

    @Slot()
    def save_file_as(self):
        file_path, selected_filter = QFileDialog.getSaveFileName(
            self, "Save File As", "", "Text Files (*.txt);;All Files (*)"
        )
        if not file_path:
            return
        self.current_file = file_path
        self.save_file()

    @Slot()
    def print_file(self):
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        if dialog.exec() == QPrintDialog.DialogCode.Accepted:
            self.text_editor.print_(printer)

    @Slot()
    def close_all_windows(self):
        QApplication.closeAllWindows()

    def closeEvent(self, event):
        if self.text_editor.document().isModified():
            ret = QMessageBox.question(
                self,
                "Unsaved changes",
                "You have unsaved changes. Close anyway?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if ret == QMessageBox.StandardButton.No:
                event.ignore()
                return
        event.accept()

    @Slot()
    def delete_text(self):
        cursor = self.text_editor.textCursor()
        if cursor.hasSelection():
            cursor.removeSelectedText()

    @Slot()
    def find(self):
        text, ok = QInputDialog.getText(self, "Find", "Find:", text=self.find_text)
        if ok and text:
            self.find_text = text
            self.text_editor.find(text)

    @Slot()
    def selection_changed(self):
        has_selection = self.text_editor.textCursor().hasSelection()
        self.copy_action.setEnabled(has_selection)
        self.cut_action.setEnabled(has_selection)
        self.delete_action.setEnabled(has_selection)

    @Slot()
    def choose_font(self):
        current_font = self.text_editor.font()
        ok, font = QFontDialog.getFont(current_font, self, "Select font")
        if ok:
            self.text_editor.setFont(font)
            self.default_font_size = font.pointSize()
            self.current_font_size = font.pointSize()
            self.update_zoom_label()

    @Slot()
    def zoom_in(self):
        self.text_editor.zoomIn()
        self.current_font_size += 1
        self.update_zoom_label()

    @Slot()
    def zoom_out(self):
        self.text_editor.zoomOut()
        self.current_font_size -= 1
        self.update_zoom_label()

    @Slot()
    def reset_zoom(self):
        font = self.text_editor.font()
        font.setPointSize(self.default_font_size)
        self.text_editor.setFont(font)
        self.current_font_size = self.default_font_size
        self.update_zoom_label()

    @Slot()
    def cursor_position(self):
        cursor = self.text_editor.textCursor()
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber() + 1
        self.cursor_label.setText(f"Ln {line} col {col}")

    @Slot()
    def update_zoom_label(self):
        percentage = round((self.current_font_size / self.default_font_size) * 100)
        self.zoom_label.setText(f"Zoom : {percentage}%")

    @Slot()
    def toggle_status_bar(self):
        if self.toggle_status_bar_action.isChecked():
            self.statusBar().show()
        else:
            self.statusBar().hide()

    @Slot()
    def toggle_word_wrap(self):
        if self.toggle_word_wrap_action.isChecked():
            self.text_editor.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        else:
            self.text_editor.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.windows = []
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
