import os
import platform
import sys

from PyQt5.Qt import PYQT_VERSION_STR, QSizePolicy
from PyQt5.QtCore import Qt, QT_VERSION_STR
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QWidget,
    QFileDialog,
    QStyle,
    QTreeWidgetItem,
    QHeaderView,
    QMainWindow,
    QAbstractItemView,
    QGridLayout,
    QAction,
    QMessageBox,
    QDesktopWidget,
    QPushButton,
    QFontDialog,
    QLineEdit,
    QLabel,
    QTreeWidget,
)

from PlaylistFormatter import PlaylistFormatter
from colorprint import print_color, Color


class PlaylistGui(QMainWindow):
    def __init__(self):
        super().__init__()

        self.formatter = PlaylistFormatter()
        self.platform = platform.system().lower()
        if self.platform == "darwin":  # MacOS
            self.defaultPath = os.path.expanduser("~/Dropbox")
        else:
            self.defaultPath = "D:/Dropbox"

        self.about_act = None
        self.basso_button = None
        self.exit_act = None
        self.export_button = None
        self.file_menu = None
        self.font_act = None
        self.help_menu = None
        self.list = None
        self.main_grid = None
        self.main_widget = None
        self.menubar = None
        self.open_button = None
        self.playlist_date_edit = None
        self.playlist_date_label = None
        self.playlist_file_edit = None
        self.playlist_file_label = None
        self.playlist_name_edit = None
        self.playlist_name_label = None
        self.statusbar = None
        self.view_menu = None

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Esgrove's Playlist Tool")
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.setAcceptDrops(True)

        # geometry
        self.setGeometry(0, 0, 1000, 800)
        self.setMinimumSize(500, 500)
        qt_rectangle = self.frameGeometry()
        qt_rectangle.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(qt_rectangle.topLeft())

        # menubar
        self.menubar = self.menuBar()
        self.file_menu = self.menubar.addMenu("&File")
        self.view_menu = self.menubar.addMenu("&View")
        self.help_menu = self.menubar.addMenu("&Help")
        self.statusbar = self.statusBar()

        # menu actions
        self.exit_act = QAction(
            self.style().standardIcon(QStyle.SP_MessageBoxCritical), "&Exit", self
        )
        self.exit_act.setShortcut("Escape")
        self.exit_act.setStatusTip("Exit application")
        self.exit_act.triggered.connect(self.closeEvent)
        self.file_menu.addAction(self.exit_act)

        self.about_act = QAction(
            self.style().standardIcon(QStyle.SP_MessageBoxQuestion), "&About", self
        )
        self.about_act.setShortcut("Ctrl+I")
        self.about_act.setStatusTip("About this application")
        self.about_act.triggered.connect(self.about_event)
        self.help_menu.addAction(self.about_act)

        self.font_act = QAction("&Choose Font", self)
        self.font_act.triggered.connect(self.choose_font)
        self.view_menu.addAction(self.font_act)

        # buttons
        self.open_button = QPushButton("Open playlist", self)
        self.open_button.setToolTip("Open playlist filedialog")
        self.open_button.clicked.connect(self.open_playlist)
        self.open_button.setStyleSheet("QPushButton { font: bold 16px; height: 50px; }")

        self.export_button = QPushButton("Save playlist", self)
        self.export_button.setToolTip("Export playlist to file")
        self.export_button.clicked.connect(self.export_playlist)
        self.export_button.setStyleSheet(
            "QPushButton { font: bold 16px; height: 50px; }"
        )

        self.basso_button = QPushButton("Upload to Basso", self)
        self.basso_button.setToolTip("Fill playlist to dj.Basso.fi")
        self.basso_button.clicked.connect(self.fill_basso)
        self.basso_button.setStyleSheet(
            "QPushButton { font: bold 16px; height: 50px; }"
        )

        # line edits
        self.playlist_name_label = QLabel("Playlist Name")
        self.playlist_date_label = QLabel("Playlist Date")
        self.playlist_file_label = QLabel("Playlist File")
        self.playlist_name_edit = QLineEdit()
        self.playlist_date_edit = QLineEdit()
        self.playlist_file_edit = QLineEdit()
        self.playlist_file_edit.setReadOnly(True)

        # list view
        self.list = QTreeWidget()
        self.list.setFont(QFont("Consolas", 9))
        self.list.setStyleSheet("QTreeView::item { margin: 2px; }")
        self.list.setAlternatingRowColors(True)
        self.list.setAcceptDrops(True)
        self.list.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.list.setDragDropMode(QAbstractItemView.InternalMove)
        self.list.setDropIndicatorShown(True)
        self.list.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.list.setColumnCount(4)
        self.list.setHeaderLabels(("index", "artist", "song", "playtime"))
        self.list.header().setStretchLastSection(False)
        self.list.header().setSectionResizeMode(2, QHeaderView.Stretch)
        self.list.setColumnWidth(0, 50)
        self.list.setColumnWidth(1, 500)
        self.list.setColumnWidth(3, 100)

        # grid
        self.main_grid = QGridLayout()
        self.main_grid.setSpacing(10)
        self.main_grid.addWidget(self.open_button, 0, 0, 1, 2, Qt.AlignTop)
        self.main_grid.addWidget(self.export_button, 0, 2, 1, 2, Qt.AlignTop)
        self.main_grid.addWidget(self.basso_button, 0, 4, 1, 2, Qt.AlignTop)
        self.main_grid.addWidget(self.playlist_file_label, 1, 0, 1, 1, Qt.AlignRight)
        self.main_grid.addWidget(self.playlist_file_edit, 1, 1, 1, 5, Qt.AlignTop)
        self.main_grid.addWidget(self.playlist_name_label, 2, 0, 1, 1, Qt.AlignRight)
        self.main_grid.addWidget(self.playlist_name_edit, 2, 1, 1, 2, Qt.AlignTop)
        self.main_grid.addWidget(self.playlist_date_label, 2, 3, 1, 1, Qt.AlignRight)
        self.main_grid.addWidget(self.playlist_date_edit, 2, 4, 1, 2, Qt.AlignTop)
        self.main_grid.addWidget(self.list, 3, 0, 1, 6)

        # main widget
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_grid)
        self.setCentralWidget(self.main_widget)

    def about_event(self, event):
        QMessageBox.about(
            self,
            "About",
            "Playlist Tools\nAkseli Lukkarila\n2018\n\n"
            + f"Python {sys.version.split(' ')[0]} QT {QT_VERSION_STR} PyQT {PYQT_VERSION_STR}",
        )

    def add_playlist(self, filename):
        self.formatter.read_playlist(filename)
        for index, row in enumerate(self.formatter.playlist):
            self.list.addTopLevelItem(
                QTreeWidgetItem(
                    (
                        str(index + 1),
                        row["artist"],
                        row["song"],
                        str(row["playtime"]).split(", ")[-1],
                    )
                )
            )

        self.playlist_file_edit.setText(str(self.formatter.playlist_file))
        self.playlist_name_edit.setText(str(self.formatter.playlist_name))
        self.playlist_date_edit.setText(str(self.formatter.playlist_date))
        self.statusbar.showMessage(f"Loaded playlist: {filename}", 5000)

    def choose_font(self, event):
        font, ok = QFontDialog.getFont()
        if ok:
            self.list.setFont(font)

    def export_playlist(self, event):
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save playlist",
            self.defaultPath + os.sep + self.playlist_name_edit.text(),
        )
        if filename:
            if filename.endswith(".csv"):
                self.formatter.export_csv(filename)

            elif filename.endswith(".txt"):
                print_color("txt export not implemented yet!", Color.red)
                return

            elif filename.endswith(".xlsx"):
                print_color("Excel export not implemented yet!", Color.red)
                return

            else:
                self.formatter.export_csv(filename)

            self.statusbar.showMessage(f"Saved playlist as: {filename}", 5000)

    def fill_basso(self, event):
        self.formatter.fill_basso("Ruff Cut", self.playlist_date_edit.text())

    def open_playlist(self, event):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Open playlist", self.defaultPath, "Files (*.csv *.txt *.xlsx *.xlsm)"
        )
        if filename:
            self.add_playlist(filename)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        filename = str(event.mimeData().urls()[0].toLocalFile())
        self.add_playlist(filename)

    def closeEvent(self, event):
        self.quit()
