from os import listdir
from os.path import abspath, isdir, join, getmtime
from time import strftime, localtime

from PIL import Image, UnidentifiedImageError
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QGraphicsPixmapItem, QGraphicsScene
from PyQt5.uic import loadUi
from numpy import array


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi(abspath(r'src\Qt\GPM_AI_training.ui'), self)
        self.file_path = QFileDialog()

        self.training_data_path = None
        self.testing_data_path = None
        self.training_image_list = None
        self.testing_image_list = None
        self.all_image_list = None

        self.display_type_list = ['Training', 'Testing', 'All']
        self.display_type = 'Training'
        self.sort_type_list = ['Image Type', 'Alphabetical', 'Time']
        self.sort_type = 'Image Type'
        self.label_type_list = ['Without Mark', 'Mark']
        self.label_type = 'Without Mark'

        self.listWidget_ImageName.itemDoubleClicked.connect(self.on_listWidget_ImageName_itemDoubleClicked)

        self.image = QImage()
        self.pix = None
        self.pix_item = None
        self.scene = QGraphicsScene()
        self.image_width = self.graphicsView.width() - 10
        self.image_height = self.graphicsView.height() - 10

    @pyqtSlot()
    def on_pushButton_AIModelPath_3_clicked(self):
        self.training_data_path = self.file_path.getExistingDirectory(self)
        self.plainTextEdit_TrainingDataPath.setPlainText(self.training_data_path)
        self.training_image_list = self.get_image_name(self.training_data_path)
        self.listWidget_ImageName_display()

    @pyqtSlot()
    def on_pushButton_AIModelPath_4_clicked(self):
        self.testing_data_path = self.file_path.getExistingDirectory(self)
        self.plainTextEdit_TestingDataPath.setPlainText(self.testing_data_path)
        self.testing_image_list = self.get_image_name(self.testing_data_path)
        self.listWidget_ImageName_display()

    @pyqtSlot()
    def on_listWidget_ImageName_itemDoubleClicked(self):
        if self.display_type == 'Training':
            self.image_display(self.training_image_list[self.listWidget_ImageName.currentRow()])
        elif self.display_type == 'Testing':
            self.image_display(self.testing_image_list[self.listWidget_ImageName.currentRow()])
        elif self.display_type == 'All':
            self.image_display(self.all_image_list[self.listWidget_ImageName.currentRow()])

    @pyqtSlot()
    def on_pushButton_clicked(self):
        self.image_zoom_in()
        self.image_handler()

    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        self.image_zoom_out()
        self.image_handler()

    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        self.image_fit()
        self.image_handler()

    @staticmethod
    def get_image_name(data_path):
        image_list = []
        if isdir(data_path):
            for item in listdir(data_path):
                full_path = join(data_path, item)
                try:
                    Image.open(full_path)
                    image_list.append(full_path)
                except UnidentifiedImageError:
                    pass

            return image_list
        else:
            return []

    def listWidget_ImageName_display(self):


    def display_determine(self):
        if self.display_type == 'Training':


    def sort_determine(self):
        if self.sort_type == 'Image Type':


    def label_determine(self):
        if self.label_type == 'Without Mark':


    def image_data_sort_by_time(self, image_list):
        buf = []
        self.listWidget_ImageName.clear()
        if image_list is not None:
            for each in image_list:
                buf.append([each, strftime('%Y-%m-%d %H:%M:%S', localtime(getmtime(each)))])
            buf.sort(key=lambda x: x[1])
            return list(array(buf)[:, 0])
        else:
            return []

    def image_display(self, img):
        self.image.load(img)
        self.image_handler()

    def image_handler(self):
        image_copy = self.image
        self.pix = QPixmap.fromImage(image_copy)
        self.pix = self.pix.scaled(self.image_width, self.image_height)
        self.pix_item = QGraphicsPixmapItem(self.pix)
        self.scene.clear()
        self.scene.addItem(self.pix_item)
        self.graphicsView.setSceneRect(0, 0, self.image_width, self.image_height)
        self.graphicsView.setScene(self.scene)

    def image_zoom_in(self):
        self.image_width = self.image_width + 10
        self.image_height = self.image_height + 10

    def image_zoom_out(self):
        self.image_width = self.image_width - 10
        self.image_height = self.image_height - 10

    def image_fit(self):
        self.image_width = self.graphicsView.width() - 10
        self.image_height = self.graphicsView.height() - 10
