#-*- coding:utf-8 -*-

"""
@created on 2017-06-06
@auther:Ziv Xiao
"""

import sys

from PyQt5.QtWidgets import *

import dbmodel
import zmq_sender

class Attacker(QDialog):
    
    def __init__(self, parent=None):
        super(Attacker, self).__init__(parent)
        
        self.initUI()
        self.initInfo()
        
    def initUI(self):
        targetInfoLabel = QLabel("设置靶机信息：")
        self.targetInfo = QLineEdit("tcp://localhost:5299")
        
        attackPackageInfoLabel = QLabel("攻击包信息：")
        self.attackPackageInfo = QListWidget()
       
        gridLayout = QGridLayout()
        gridLayout.addWidget(targetInfoLabel, 0, 0, 1, 1)
        gridLayout.addWidget(attackPackageInfoLabel, 1, 0, 1, 1)
        gridLayout.addWidget(self.targetInfo, 0, 1, 1, 3);
        gridLayout.addWidget(self.attackPackageInfo, 1, 1, 1, 3);

        okBtn = QPushButton("解析并发送")
        self.statusLabel = QLabel("status:")
        btnLayout = QHBoxLayout()

        btnLayout.setSpacing(60)
        btnLayout.addWidget(okBtn)
        btnLayout.addWidget(self.statusLabel)

        dlgLayout = QVBoxLayout()
        dlgLayout.setContentsMargins(40, 40, 40, 40)
        dlgLayout.addLayout(gridLayout)
        dlgLayout.addStretch(40)
        dlgLayout.addLayout(btnLayout)

        self.setLayout(dlgLayout)
        okBtn.clicked.connect(self.accept)
        self.setWindowTitle("web 攻击模拟")
        self.resize(800, 400)
        
    def initInfo(self):
        session = dbmodel.get_session()
        for pt in session.query(dbmodel.Packet):
            info = "\t".join([pt.uname, str(pt.utype), pt.upath])
            self.attackPackageInfo.addItem(info)

    def accept(self):
        if not self.attackPackageInfo.currentItem():
            QMessageBox.warning(self, "warn", "请先选择攻击包", QMessageBox.Yes)
            return
        packet = self.attackPackageInfo.currentItem().text()
        pcapfile = packet.split("\t")[-1]
        target = str(self.targetInfo.displayText())

        zmq_sender.connect(target)
        f = open("./pcaps/%s" % pcapfile, "rb")
        zmq_sender.send(f.read())
        f.close()
        
        self.statusLabel.setText("status: send %s"% pcapfile)

app = QApplication(sys.argv)
dlg = Attacker()
dlg.show()
dlg.exec_()
app.exit()