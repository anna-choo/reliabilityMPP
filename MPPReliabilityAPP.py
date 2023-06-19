import pandas as pd
import os, collections, csv, random, sys
import numpy as np
from sympy import Point3D, Line3D
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.pyplot import figure
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5.QtChart import *
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import matplotlib.patches as mpatches

class MplCanvas(FigureCanvasQTAgg):
    
    def __init__(self, parent=None, width=5, height=8, dpi=100):
        fig = figure(figsize=(width, height), dpi=dpi)
        # plt.rcParams.update({
        #     "lines.color": "black",
        #     "patch.edgecolor": "white",
        #     "text.color": "black",
        #     "axes.facecolor": "black",
        #     "axes.edgecolor": "gray",
        #     "axes.labelcolor": "black",
        #     "xtick.color": "black",
        #     "ytick.color": "black",
        #     "grid.color": "gray",
        #     "figure.facecolor": "white",
        #     "figure.edgecolor": "white",
        #     "savefig.facecolor": "white",
        #     "savefig.edgecolor": "white",
        #     "figure.figsize": (20,20),
        #     "font.size": 9})
        # plt.grid()
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class graphPopUp(QDialog):
    def __init__(self, Xaxis, Yaxis, color_list, segment,  parent = None):
        super().__init__()
        self.parent = parent
        self.setFixedSize(1000, 1000)

        self.setWindowTitle('MPP Graph')

        sc = MplCanvas(self, width=10, height=30, dpi=90)
        sc.axes.barh(Yaxis, Xaxis, color = color_list,height = 0.7, align='center',)
        sc.axes.grid(color = 'lightgray', linestyle = "-.")
        sc.axes.set_ylabel("Markers")
        sc.axes.set_xlabel("Distance(mm)")
        # color_legend = []
        # for i in range(len(color_list)):
        #     blue_patch = mpatches.Patch(color=color_list[i], label=segment[i])
        # sc.legend(handles=color_legend)
        # sc.axes.set_y
        # y_labels = []
        # for i in range(0, len(Xaxis), 2):
        #     for i%%2 == 0:
        #         y_labels
        #     y_labels
        # sc.axes.set_yticks([i for i in range(0, len(Xaxis), 2)])
        # sc.axes.set_yscale()
        # sc.axes.set_ylabel([i for i in range(0, len(Xaxis), 2)])
        # sc.axes.set_yticks([i for i in range(len(Yaxis), 1)])


        self.toolbar = NavigationToolbar2QT(sc, self)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(sc)
        # Create a placeholder widget to hold our toolbar and canvas.
        self.setLayout(self.layout)
        self.exec()
            



        # self.show()


class MPP_Reliability_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cluster_list = {
            'RSK':['RSK1', 'RSK2', 'RSK3', 'RSK4'],
            'LSK':['LSK1', 'LSK2', 'LSK3', 'LSK4'],
            'RTH':['RTH1', 'RTH2', 'RTH3', 'RTH4'],
            'LTH':['LTH1', 'LTH2', 'LTH3', 'LTH4'],
            'RFT':['RFMB1', 'RFMB2', 'RFMB3'],
            'LFT':['LFMB1', 'LFMB2', 'LFMB3'],
            'RUA':['RUA1', 'RUA2', 'RUA3', 'RUA4'],
            'LUA':['LUA1', 'LUA2', 'LUA3', 'LUA4'],
            'RFA':['RFA1', 'RFA2', 'RFA3'],
            'LFA':['LFA1', 'LFA2', 'LFA3'],
            'TS':['T6_1', 'T6_2', 'T6_3'],
            'SAC':['SACRAL1', 'SACRAL2', 'SACRAL3'],
            'LHMC':['LHMC1', 'LHMC2', 'LHMC3'],
            'RHMC':['RHMC1', 'RHMC2', 'RHMC3'],
            'ST':['ST1', 'ST2','ST3']
            }

        self.marker_list = {
            ###ankle####
            'RSK':['RFAL', 'RTAM'],
            'LSK':['LFAL', 'LTAM'],
            ########knee##############
            'RTH':['RFLE', 'RFME'],
            'LTH':['LFLE', 'LFME'],
            ###########Foot##############
            'RFT':['RFMT1', 'RFMT2', 'RFMT5', 'RFCC', 'RCUN'],
            'LFT':['LFMT1', 'LFMT2', 'LFMT5', 'LFCC', 'LCUN'],
            #########elbow###########
            'RUA':['RHME', 'RHLE', 'RACR'],
            'LUA':['LHME', 'LHLE', 'LACR'],
            #wrist####
            'RFA':['RUSP', 'RRSP'],
            'LFA':['LUSP', 'LRSP'],
            ############hand########
            'LHMC':['LCAP'],
            'RHMC':['RCAP'],
            ####T spine####### 
            'TS':['T4', 'T8', 'T10', 'C7'],
            'ST':['STER', 'XPRO'],
            #########pelvis############
            'SAC':['RASIS', 'RPSIS', 'RICR', 'LASIS', 'LPSIS', 'LICR']

            }

        self.grouping_list = {
            ###ankle####
            'RSK':['ankle', 'green'],
            'LSK':['ankle', 'green'],
            ########knee##############
            'RTH':['knee', 'blue'],
            'LTH':['knee', 'blue'],
            ###########Foot##############
            'RFT':['foot', 'red'],
            'LFT':['foot', 'red'],
            #########elbow###########
            'RUA':['elbow', 'yellow'],
            'LUA':['elbow', 'yellow'],
            ###wrist####
            'RFA':['wrist', 'pink'],
            'LFA':['wrist', 'pink'],
            ############hand########
            'LHMC':['hand', 'purple'],
            'RHMC':['hand', 'purple'],
            #######T spine####### 
            'TS':['T_spine', 'grey'],
            #########pelvis############
            'SAC':['pelvis', 'cyan']
        }


        self.selected_file1 = None
        self.selected_file2 = None


        # self.setFixedSize(660, 180)
        self.setFixedSize(750, 260)

        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)
        self.setWindowTitle('MPP Reliability')

        self.LABEL_MPP1 = QLabel(self.widget)
        self.LABEL_MPP1.setText("<b> MPP 1 </b>")
        # self.LABEL_MPP1.setText("Select MPP1 \t\t File 1: ")
        self.LABEL_MPP1.setGeometry(QRect(40,55,50,20))
        # self.LABEL_MPP1.setAlignment(Qt.AlignRight)


        self.LABEL_file1 = QLabel(self.widget)
        self.LABEL_file1.setText("File 1:")
        # self.LABEL_file1.setText("Select MPP1 \t\t File 1: ")
        self.LABEL_file1.setGeometry(QRect(90,40,50,20))
        self.LABEL_file1.setAlignment(Qt.AlignRight)

        self.file1_path = QLineEdit(" Please Select", self.widget)
        self.file1_path.setStyleSheet("background-color: White;")
        self.file1_path.setGeometry(QRect(150, 30, 450, 30))

        self.BUTTON_browse1 = QPushButton("Browse", self.widget)
        self.BUTTON_browse1.setGeometry(QRect(630, 30, 80, 30))
        self.BUTTON_browse1.clicked.connect(self.browse_files1)


        self.LABEL_file2 = QLabel(self.widget)
        self.LABEL_file2.setText("File 2:")
        self.LABEL_file2.setGeometry(QRect(90,80,50,20))
        self.LABEL_file2.setAlignment(Qt.AlignRight)


        self.file2_path = QLineEdit(" Please Select", self.widget)
        self.file2_path.setStyleSheet("background-color: White;")
        self.file2_path.setGeometry(QRect(150, 70, 450, 30))

        self.BUTTON_browse2 = QPushButton("Browse", self.widget)
        self.BUTTON_browse2.setGeometry(QRect(630, 70, 80, 30))
        self.BUTTON_browse2.clicked.connect(self.browse_files2)

        self.LABEL_MPP2 = QLabel(self.widget)
        self.LABEL_MPP2.setText("<b> MPP 2 </b>")
        # self.LABEL_MPP2.setText("Select MPP1 \t\t File 1: ")
        self.LABEL_MPP2.setGeometry(QRect(40,135,50,20))
        # self.LABEL_MPP2.setAlignment(Qt.AlignRight)


        self.LABEL_file3 = QLabel(self.widget)
        self.LABEL_file3.setText("File 1:")
        self.LABEL_file3.setGeometry(QRect(90,120,50,20))
        self.LABEL_file3.setAlignment(Qt.AlignRight)

        # self.LABEL_file3.show()

        self.file3_path = QLineEdit(" Please Select", self.widget)
        self.file3_path.setStyleSheet("background-color: White;")
        self.file3_path.setGeometry(QRect(150, 110, 450, 30))
        # self.file3_path.show()

        self.BUTTON_browse3 = QPushButton("Browse", self.widget)
        self.BUTTON_browse3.setGeometry(QRect(630, 110, 80, 30))
        self.BUTTON_browse3.clicked.connect(self.browse_files3)
        # self.BUTTON_browse3.show()

        self.LABEL_file4 = QLabel(self.widget)
        self.LABEL_file4.setText("File 2:")
        self.LABEL_file4.setGeometry(QRect(90,160,50,20))
        self.LABEL_file4.setAlignment(Qt.AlignRight)

        # self.LABEL_file4.show()

        self.file4_path = QLineEdit(" Please Select", self.widget)
        self.file4_path.setStyleSheet("background-color: White;")
        self.file4_path.setGeometry(QRect(150, 150, 450, 30))
        # self.file4_path.show()


        self.BUTTON_browse4 = QPushButton("Browse", self.widget)
        self.BUTTON_browse4.setGeometry(QRect(630, 150, 80, 30))
        self.BUTTON_browse4.clicked.connect(self.browse_files4)
        # self.BUTTON_browse4.show()

        self.intraRater = QCheckBox("Intra-rater Reliability", self.widget)
        # self.intraRater.setGeometry(QRect(540, 120, 100, 30))
        self.intraRater.setGeometry(QRect(540, 200, 150, 30))

        # self.intraRater.clicked.connect(self.expandSelection)
        # self.intraRater.clicked

        self.generateGraphButton = QPushButton("Graph", self.widget)
        # self.generateGraphButton.setGeometry(QRect(440, 120, 90, 30))
        self.generateGraphButton.setGeometry(QRect(440, 200, 90, 30))

        self.generateGraphButton.clicked.connect(self.plot_graph)


        
    # def expandSelection(self):
    #     # if self.intraRater.isChecked() == False:
    #     #     self.setFixedSize(660, 180)
    #     #     self.LABEL_file3.hide()
    #     #     self.file3_path.hide()
    #     #     self.BUTTON_browse3.hide()
    #     #     self.LABEL_file4.hide()
    #     #     self.file4_path.hide()
    #     #     self.BUTTON_browse4.hide()
    #     #     self.intraRater.setGeometry(QRect(540, 120, 100, 30))
    #     #     self.generateGraphButton.setGeometry(QRect(440, 120, 90, 30))



    #     # else:
    #     self.setFixedSize(660, 260)

    #     self.LABEL_file3 = QLabel(self.widget)
    #     self.LABEL_file3.setText("Select MPP1 file2: ")
    #     self.LABEL_file3.setGeometry(QRect(40,120,100,10))
    #     self.LABEL_file3.show()

    #     self.file3_path = QLineEdit(" Please Select", self.widget)
    #     self.file3_path.setStyleSheet("background-color: White;")
    #     self.file3_path.setGeometry(QRect(130, 110, 400, 30))
    #     self.file3_path.show()

    #     self.BUTTON_browse3 = QPushButton("Browse", self.widget)
    #     self.BUTTON_browse3.setGeometry(QRect(540, 110, 80, 30))
    #     self.BUTTON_browse3.clicked.connect(self.browse_files3)
    #     self.BUTTON_browse3.show()

    #     self.LABEL_file4 = QLabel(self.widget)
    #     self.LABEL_file4.setText("Select MPP2 file2: ")
    #     self.LABEL_file4.setGeometry(QRect(40,160,100,10))
    #     self.LABEL_file4.show()

    #     self.file4_path = QLineEdit(" Please Select", self.widget)
    #     self.file4_path.setStyleSheet("background-color: White;")
    #     self.file4_path.setGeometry(QRect(130, 150, 400, 30))
    #     self.file4_path.show()


    #     self.BUTTON_browse4 = QPushButton("Browse", self.widget)
    #     self.BUTTON_browse4.setGeometry(QRect(540, 150, 80, 30))
    #     self.BUTTON_browse4.clicked.connect(self.browse_files4)
    #     self.BUTTON_browse4.show()


    #     self.intraRater.setGeometry(QRect(540, 200, 100, 30))
    #     self.generateGraphButton.setGeometry(QRect(440, 200, 90, 30))




    def browse_files1(self):
        self.selected_file1 = QFileDialog.getOpenFileName(self.widget)
        self.savedPath1 = self.selected_file1[0]
        self.file1_path.setText(self.savedPath1)

    def browse_files2(self):
        self.selected_file2 = QFileDialog.getOpenFileName(self.widget)
        self.savedPath2 = self.selected_file2[0]
        self.file2_path.setText(self.savedPath2)
        
    def browse_files3(self):
        self.selected_file3 = QFileDialog.getOpenFileName(self.widget)
        self.savedPath3 = self.selected_file3[0]
        self.file3_path.setText(self.savedPath3)

    def browse_files4(self):
        self.selected_file4 = QFileDialog.getOpenFileName(self.widget)
        self.savedPath4 = self.selected_file4[0]
        self.file4_path.setText(self.savedPath4)



    def manipulate_data(self, file_dir):
        with open(file_dir) as tsvfile:
            tsvreader = csv.reader(tsvfile, delimiter="\t")
            event_list = []

            # calculate the number of rows to skip to get to markers data
            number_of_rows_to_skip = -1

            # record all event first before skipping these lines
            for line in tsvreader:
                # once found data, stop collecting event and break the loop
                if line[0] == "MARKER_NAMES":
                    break
                number_of_rows_to_skip += 1

            df = pd.read_csv(tsvfile, delimiter="\t")
            # remove unamed column
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

        return df


    def unit_vector(self, vector):
        dist = np.sqrt(sum(vector**2))
        return (vector/dist)

    def dist(self, data1, data2):
        df = pd.DataFrame(columns=['markers', 'distance'])
        missing_marker = []
        for cluster, anatomical_list in self.marker_list.items():
            try:
                target_cluster1 = np.array(np.mean(data1.loc[:, data1.columns[(data1.columns.str.contains('|'.join(self.cluster_list[cluster])))]])).reshape(-1,3)
                Xaxis1 = self.unit_vector(target_cluster1[1] - target_cluster1[0])
                Zaxis1 = self.unit_vector(np.cross(Xaxis1, self.unit_vector(target_cluster1[2] - target_cluster1[1])))
                Yaxis1 = self.unit_vector(np.cross(Xaxis1, Zaxis1))
                trans_matrix1 = np.array([Xaxis1, Yaxis1, Zaxis1, target_cluster1[0]])
                trans_matrix1 = np.concatenate([trans_matrix1, np.array([0, 0, 0, 1]).reshape(4,1)], axis = 1).T
                i_trans_matrix1 = np.linalg.inv(trans_matrix1)
                
                target_cluster2 = np.array(np.mean(data2.loc[:, data2.columns[(data2.columns.str.contains('|'.join(self.cluster_list[cluster])))]])).reshape(-1,3)
                Xaxis2 = self.unit_vector(target_cluster2[1] - target_cluster2[0])
                Zaxis2 = self.unit_vector(np.cross(Xaxis2, self.unit_vector(target_cluster2[2] - target_cluster2[1])))
                Yaxis2 = self.unit_vector(np.cross(Xaxis2, Zaxis2))
                trans_matrix2 = np.array([Xaxis2, Yaxis2, Zaxis2, target_cluster2[0]])
                trans_matrix2 = np.concatenate([trans_matrix2, np.array([0, 0, 0, 1]).reshape(4,1)], axis = 1).T
                i_trans_matrix2 = np.linalg.inv(trans_matrix2)


                for anatomical in anatomical_list:
                    try:
                        target_anatomical1 = np.array(np.mean(data1.loc[:, data1.columns[(data1.columns.str.contains(anatomical))]]))
                        target_anatomical1 = np.concatenate([target_anatomical1, np.array([1])], axis = 0)
                        target_anatomical2 = np.array(np.mean(data2.loc[:, data2.columns[(data2.columns.str.contains(anatomical))]]))
                        target_anatomical2 = np.concatenate([target_anatomical2, np.array([1])], axis = 0)

                        # target_anatomical2 = np.array(np.mean(data2.loc[:, data2.columns[(data2.columns.str.contains(anatomical))]])).reshape(-1,3)
                        tester1 = np.matmul(i_trans_matrix1, target_anatomical1)
                        tester2 = np.matmul(i_trans_matrix2, target_anatomical2)

                        d_matrix = tester1 - tester2
                        dist = round(np.sqrt(sum(d_matrix**2)),2)
                        new_row = {'markers': anatomical, 'distance': dist, 'grouping': self.grouping_list[cluster][0], 'color': self.grouping_list[cluster][1]}
                        df = df.append(new_row, ignore_index = True)
                    except:
                        missing_marker.append(anatomical)
            except:
                missing_marker.append(cluster)
        df = df.sort_values(by = ['distance'], ascending=False)

        return df


    # def plot_graph(self, df):
    #     plt.rcParams.update({
    #         "lines.color": "white",
    #         "patch.edgecolor": "white",
    #         "text.color": "black",
    #         "axes.facecolor": "white",
    #         "axes.edgecolor": "lightgray",
    #         "axes.labelcolor": "white",
    #         "xtick.color": "white",
    #         "ytick.color": "white",
    #         "grid.color": "lightgray",
    #         "figure.facecolor": "black",
    #         "figure.edgecolor": "black",
    #         "savefig.facecolor": "black",
    #         "savefig.edgecolor": "black",
    #         "figure.figsize": (20,20),
    #         "font.size": 20})
    #     ax = MplCanvas(self, width=5, height=4, dpi=100)
    #     markers = df["markers"]
    #     y_pos = df["distance"]

    #     ax.barh(markers, y_pos)
    #     for i, v in enumerate(y_pos):
    #         ax.text(v, i, str(round(v,2)))
    #     ax.set_xlabel('Distance(mm)')
    #     ax.set_title('MPP Reliability')
    #     self.setCentralWidget(ax)
    #     self.show()
        # plt.grid()
        # plt.show()

    def plot_graph(self):
        if self.intraRater.isChecked() == False:
            # self.openfile1 = self.file1_path.text()
            # self.openfile2 = self.file2_path.text()

            # if os.path.exists(self.openfile1) and os.path.exists(self.openfile2):
            #     self.data1 = self.manipulate_data(self.openfile1)
            #     self.data2 = self.manipulate_data(self.openfile2)

            #     self.results = self.dist(self.data1, self.data2)
            #     # graphPopUp(list(self.results["distance"]), list(self.results["markers"]))
            #     graphPopUp(list(self.results["distance"]), list(self.results["markers"]), list(self.results["color"]), list(self.results["grouping"]))
            self.openfile1 = self.file1_path.text()
            self.openfile2 = self.file2_path.text()
            self.openfile3 = self.file3_path.text()
            self.openfile4 = self.file4_path.text()

            if os.path.exists(self.openfile1) and os.path.exists(self.openfile2) and os.path.exists(self.openfile3) and os.path.exists(self.openfile4):
                self.data1 = self.manipulate_data(self.openfile1)
                self.data2 = self.manipulate_data(self.openfile2)
                self.data3 = self.manipulate_data(self.openfile3)
                self.data4 = self.manipulate_data(self.openfile4)

                self.results1 = self.dist(self.data1, self.data3)
                self.results2 = self.dist(self.data1, self.data4)
                
                self.results3 = self.dist(self.data2, self.data3)
                self.results4 = self.dist(self.data2, self.data4)
                self.finalResult = self.results1.append(self.results2)
                self.finalResult = pd.DataFrame(columns=["markers", "grouping", "color", "distance"])
                for i in range(len(self.results1)):
                    average_distance = (self.results1["distance"][i] + self.results2["distance"][i] + self.results3["distance"][i] + self.results4["distance"][i])/4
                    new_row = {"markers": self.results1["markers"][i], "grouping": self.results1["grouping"][i], "color":self.results1["color"][i], "distance": average_distance}
                    self.finalResult = self.finalResult.append(new_row, ignore_index = True)
                self.finalResult = self.finalResult.sort_values(by =['grouping', "markers"])
                # self.finalResult['display_name'] = self.finalResult['markers'] + "_" + self.finalResult["MPP"]

                graphPopUp(list(self.finalResult["distance"]), list(self.finalResult["markers"]), list(self.finalResult["color"]), list(self.finalResult["grouping"]))

            else:
                warning_message = QMessageBox.warning(self, "Path not found!", "Please select 2 existing file path.")
        else:
            self.openfile1 = self.file1_path.text()
            self.openfile2 = self.file2_path.text()
            self.openfile3 = self.file3_path.text()
            self.openfile4 = self.file4_path.text()

            if os.path.exists(self.openfile1) and os.path.exists(self.openfile2) and os.path.exists(self.openfile3) and os.path.exists(self.openfile4):
                self.data1 = self.manipulate_data(self.openfile1)
                self.data2 = self.manipulate_data(self.openfile2)
                self.data3 = self.manipulate_data(self.openfile3)
                self.data4 = self.manipulate_data(self.openfile4)

                self.results1 = self.dist(self.data1, self.data2)
                self.results1["MPP"] = "MPP1"
                self.results2 = self.dist(self.data3, self.data4)
                self.results2["MPP"] = "MPP2"
                self.finalResult = self.results1.append(self.results2)
                self.finalResult = self.finalResult.sort_values(by =['grouping', "markers", "MPP"])
                self.finalResult['display_name'] = self.finalResult['markers'] + "_" + self.finalResult["MPP"]

                graphPopUp(list(self.finalResult["distance"]), list(self.finalResult["display_name"]), list(self.finalResult["color"]), list(self.finalResult["grouping"]))
            else:
                warning_message = QMessageBox.warning(self, "Path not found!", "Please select 4 existing file path.")
    


app = QApplication(sys.argv)

window = MPP_Reliability_MainWindow()


window.show()

app.exec()