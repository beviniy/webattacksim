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
    """主窗体类"""

    def __init__(self, parent=None):
        """构造函数"""
        super(Attacker, self).__init__(parent)
        
        self.initUI()   #初始化UI
        self.initInfo()     #初始化attackPackageInfo的显示信息
        
    def initUI(self):

        # 设置窗体属性
        self.setWindowTitle("web 攻击模拟")
        self.resize(800, 400)

        # 初始化控件
        targetInfoLabel = QLabel("设置靶机信息：")
        self.targetInfo = QLineEdit("tcp://localhost:5299")
        
        attackPackageInfoLabel = QLabel("攻击包信息：")
        self.attackPackageInfo = QListWidget()
        okBtn = QPushButton("解析并发送")
        self.statusLabel = QLabel("status:")

        # 布局控件
        gridLayout = QGridLayout()
        gridLayout.addWidget(targetInfoLabel, 0, 0, 1, 1)
        gridLayout.addWidget(attackPackageInfoLabel, 1, 0, 1, 1)
        gridLayout.addWidget(self.targetInfo, 0, 1, 1, 3);
        gridLayout.addWidget(self.attackPackageInfo, 1, 1, 1, 3);

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

        # 绑定按钮到方法
        okBtn.clicked.connect(self.send)
        
        
    def initInfo(self):
        """利用dbmodel查询数据库，并将数据库Packet信息显示到控件"""

        session = dbmodel.get_session()
        for pt in session.query(dbmodel.Packet):
            info = "\t".join([pt.uname, str(pt.utype), pt.upath])
            self.attackPackageInfo.addItem(info)

    def send(self):
        """按钮事件"""

        # 如果没有包被选中，则警告
        if not self.attackPackageInfo.currentItem():
            QMessageBox.warning(self, "warn", "请先选择攻击包", QMessageBox.Yes)
            return
        
        # 获取被选中包的内容
        packet = self.attackPackageInfo.currentItem().text()
        # 解析字符串获取文件名
        pcapfile = packet.split("\t")[-1]
        # 从控件获取远程机器配置
        target = str(self.targetInfo.displayText())
        # 连接
        zmq_sender.connect(target)

        # 打开选中的pcap包，发送
        f = open("./pcaps/%s" % pcapfile, "rb")
        zmq_sender.send(f.read())
        f.close()
        
        # 发送完成，设置status
        self.statusLabel.setText("status: send %s"% pcapfile)

app = QApplication(sys.argv)
dlg = Attacker()
dlg.show()
dlg.exec_()
app.exit()