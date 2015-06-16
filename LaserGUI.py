# -*- coding: utf-8 -*-

# 'LogOnGui.py'
#
# Created: Sat Feb 28 21:00:21 2015
#      by: Austin Fox#
# GPL




from PyQt4 import QtCore, QtGui
import sys  #list of comand line argus need to run Gui
#####################################################
# Try Encoding (Error prevention)
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
#####################################################

#Set Up Fonts
 #Normal font
font_N = QtGui.QFont()
font_N.setFamily(_fromUtf8("Georgia"))
font_N.setPointSize(14)
#Lable Font
font_L = QtGui.QFont()
font_L.setFamily(_fromUtf8("Georgia"))
font_L.setPointSize(18)
#Bold Font
font_B = QtGui.QFont()
font_B.setFamily(_fromUtf8("Georgia"))
font_B.setPointSize(18)
#Title Font
font_T = QtGui.QFont()
font_T.setFamily(_fromUtf8("Georgia"))
font_T.setPointSize(24)

QtGui.QToolTip.setFont(QtGui.QFont('Georgia', 12)) # set the font

#Set up Styles
ButtonStyle = "QPushButton{ \
        background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 :1, stop : 0.0 lightgrey, stop : 1 white ); \
        padding: 6px; \
        border-style: outset; \
        border-width: 1px; border-color: grey; } \
        QPushButton:pressed { \
        background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 grey, stop : 1 lightgrey ); }"
ButtonStopStyle = "QPushButton{ \
        background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 hsv(0, 255, 210), stop : 1 hsv(0, 255, 255) ); \
        padding: 6px; \
        border-style: outset; \
        border-width: 1px; \
        border-color: grey; } \
        QPushButton:pressed { \
        background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 hsv(0, 255, 160), stop : 1 hsv(0, 255, 210) ); }"
#style for lcd display boxes
styl = "Background-color: transparent; color: black; border-style: ridge; border-width: 1px; border-color: grey;"

######################################################
# Setup Main Window
class gui(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QWidget.__init__(self) # could also use 'super(gui, self).__init__()' which calls the parent of our class
      
        self.setupUi(self) # make the UI  See Bellow

    def setupUi(self, MainWindow):
        
#System Checks.  Avoid errors!!
        if sys.platform=="darwin":  #check if you are on a mac 
            QtGui.qt_mac_set_native_menubar(False)      #if on mac disable native menues

#Set Up Widget(Form) 
    #set up size policy (Currently no using a size policy but left the below in incase I decide to add it)
        #sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        #sizePolicy.setHorizontalStretch(0)
        #sizePolicy.setVerticalStretch(0)
        #sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        
    #Setup Main Window
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        #MainWindow.setMaximumSize(100,100) #height, width
        #MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setWindowTitle("PLD Controller") 

        #central widget (widget "gui" of the main window)
        self.centralwidget = QtGui.QWidget(MainWindow)
        #self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
#bring in other class widgets (See below for classes)
        self.stack = StackedWidget()
        self.NRG = NRG()
        self.Volt = Volt()
        self.PLID= PLID()
        self.Setup = Setup()
        self.Terminal = Terminal()

##############
    #Laser Status Bar
        #Tube Pressure
        self.laser_tpress = QtGui.QLCDNumber()
        self.laser_tpress.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.laser_tpress.setStyleSheet(styl)
        self.laser_tpress.setMinimumSize(60,30) #Width, height
        self.laser_tpress.setDigitCount(4)
        self.laser_tpress.display(1234)
        self.LB1 = QtGui.QLabel()
        self.LB1.setText(_fromUtf8("Tube Pressure:"))
        self.LB1.setFont(font_L)
        #Actual NRG
        self.laser_act_nrg = QtGui.QLCDNumber()
        self.laser_act_nrg.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.laser_act_nrg.setStyleSheet(styl)
        self.laser_act_nrg.setMinimumSize(46,30) #Width, height
        self.laser_act_nrg.setDigitCount(3)
        self.laser_act_nrg.display(123)
        self.LB2 = QtGui.QLabel()
        self.LB2.setText(_fromUtf8("Actual Energy [mJ]:"))
        self.LB2.setFont(font_L)
        #Actual Voltage
        self.laser_act_volt = QtGui.QLCDNumber()
        self.laser_act_volt.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.laser_act_volt.setStyleSheet(styl)
        self.laser_act_volt.setMinimumSize(60,30) #Width, height
        self.laser_act_volt.setDigitCount(4)
        self.laser_act_volt.display("12.0")
        self.LB3 = QtGui.QLabel()
        self.LB3.setText(_fromUtf8("Actual Voltage [kV]:"))
        self.LB3.setFont(font_L)

        #Actual Frq
        self.laser_act_frq = QtGui.QLCDNumber()
        self.laser_act_frq.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.laser_act_frq.setStyleSheet(styl)
        self.laser_act_frq.setMinimumSize(30,30) #Width, height
        self.laser_act_frq.setDigitCount(2)
        self.laser_act_frq.display(12)
        self.LB5 = QtGui.QLabel()
        self.LB5.setText(_fromUtf8("Rep. Rate [Hz]:"))
        self.LB5.setFont(font_L)
        #Refresh Button
        self.REButton = QtGui.QPushButton(_fromUtf8("Refresh"))
        self.REButton.setFont(font_B)
        self.REButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.REButton.setStyleSheet(ButtonStyle)
        #Messages
        self.laser_messages = QtGui.QTextEdit()
        self.laser_messages.setReadOnly(True)
        self.laser_messages.setFont(font_N)
        self.laser_messages.setMaximumHeight(30)
        self.laser_messages.setStyleSheet(styl)
        self.LB6 = QtGui.QLabel()
        self.LB6.setText(_fromUtf8("Messages:"))
        self.LB6.setFont(font_L)

    #setup status bar layout (align in grid)
        self.grid = QtGui.QGridLayout()
        self.grid.addWidget(self.LB1,1,1)
        self.grid.addWidget(self.laser_tpress,1,2)
        self.grid.addWidget(self.LB2,1,3)
        self.grid.addWidget(self.laser_act_nrg,1,4)
        self.grid.addWidget(self.LB3,2,1)
        self.grid.addWidget(self.laser_act_volt,2,2)
        self.grid.addWidget(self.LB5,2,3)
        self.grid.addWidget(self.laser_act_frq,2,4)
        self.grid.addWidget(self.REButton,1,5,QtCore.Qt.AlignTop)        
        self.grid.addWidget(self.LB6,3,1)
        self.grid.addWidget(self.laser_messages,3,2,3,5) #row, col[,end row, end col(for multi grid)]

###############
    #Notes Box
        #Box
        self.Note = QtGui.QTextEdit()
        self.Note.setFont(font_N)
        self.Note.setMaximumHeight(70)
        self.Note.setToolTip(_fromUtf8("Please Add/Delete Notes for other users here."))
        #Label
        self.NoteLabel = QtGui.QLabel()
        self.NoteLabel.setText(_fromUtf8("Notes:"))
        self.NoteLabel.setFont(font_L)
################
    #Motor Control stuff
        self.motor_spd = QtGui.QDoubleSpinBox()
        self.motor_spd.setRange(0,5)
        self.motor_spd.setSingleStep(0.25)
        self.motor_spd.setValue(0.25)
        self.motor_spd.setObjectName("spd")
        self.spdLb= QtGui.QLabel()
        self.spdLb.setText(_fromUtf8("Motor Speed [AU]:"))
        self.motor_spd.setToolTip('Motor is setup to jog back and forth at the desired speed.')
        self.spdLb.setFont(font_L)
        #Button
        self.motor_button = QtGui.QPushButton("Start Motor")
        self.motor_button.resize(100, 60)
        self.motor_button.setFont(font_B)
        self.motor_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) 
        self.motor_button.setObjectName(_fromUtf8("Motor"))
        self.motor_button.setStyleSheet(ButtonStyle)

        #motorcontroll Horizontal Box Layout
        self.motorbox = QtGui.QHBoxLayout()
        self.motorbox.addWidget(self.spdLb)
        self.motorbox.addWidget(self.motor_spd)
        self.motorbox.addWidget(self.motor_button)
###############
# Set up buttion actions and changes (Button Click is defined below)
        self.motor_button.clicked.connect(lambda: self.ButtonClick())          
        self.NRG.Button.clicked.connect(lambda: self.ButtonClick())
        self.Volt.Button.clicked.connect(lambda: self.ButtonClick())  
        self.PLID.Button.clicked.connect(lambda: self.ButtonClick())  
        self.Setup.FillBt.clicked.connect(lambda: self.ButtonClick())  
        self.Setup.CalBt.clicked.connect(lambda: self.ButtonClick())  
        self.Setup.PResBt.clicked.connect(lambda: self.ButtonClick())  
        self.Setup.PlinBt.clicked.connect(lambda: self.ButtonClick())  
        self.Setup.FlushBt.clicked.connect(lambda: self.ButtonClick())  
            


################
#Setup Main Layout

    #Set up stack (this allows for the switching between pages egy cont, volt cont, etc.)
        self.stack.addWidget(self.NRG)  
        self.stack.addWidget(self.Volt) 
        self.stack.addWidget(self.PLID) 
        self.stack.addWidget(self.Setup) 
        self.stack.addWidget(self.Terminal) 

    #create vertical layout
        self.layoutV = QtGui.QVBoxLayout(self.centralwidget)
        self.layoutV.addLayout(self.grid)       #laser status bar
        self.layoutV.addWidget(self.stack)      #stack of pages
        self.layoutV.addLayout(self.motorbox)   #motor controlls
        self.layoutV.addWidget(self.NoteLabel)
        self.layoutV.addWidget(self.Note)
    #add to main window to display 
        MainWindow.setCentralWidget(self.centralwidget)
        
#Add program Status Bar at bottom
        self.statusbar = QtGui.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
        self.statusbar.showMessage(_fromUtf8("Program On"))

#Menu Bar
    #Set up Menu items
        self.page0 = QtGui.QAction(QtGui.QIcon('img/NRG.png'), '  Energy', self)  # set up the action
        self.page0.triggered.connect(lambda: self.stack.setPage(0))         #On click do...
        self.page0.setShortcut('Ctrl+1')    #give it a shortcut
       
       
        self.page1 = QtGui.QAction(QtGui.QIcon('img/Volt.png'), '  Voltage', self)  # set up the action
        self.page1.triggered.connect(lambda: self.stack.setPage(1))         #On click do...
        self.page1.setShortcut('Ctrl+2')    #give it a shortcut

        self.page2 = QtGui.QAction(QtGui.QIcon('img/PLID.png'), '  PLID', self)  # set up the action
        self.page2.triggered.connect(lambda: self.stack.setPage(2))         #On click do...
        self.page2.setShortcut('Ctrl+3')    #give it a shortcut

        self.page3 = QtGui.QAction(QtGui.QIcon('img/Setup.png'), '  Setup', self)  # set up the action
        self.page3.triggered.connect(lambda: self.stack.setPage(3))         #On click do...
        self.page3.setShortcut('Ctrl+4')    #give it a shortcut
        
        self.page4 = QtGui.QAction(QtGui.QIcon('img/Terminal.png'), '  Terminal', self)  # set up the action
        self.page4.triggered.connect(lambda: self.stack.setPage(4))         #On click do...
        self.page4.setShortcut('Ctrl+5')    #give it a shortcut

    #Add the Menu Bar
        self.menu = self.menuBar()
        self.fileMenu = self.menu.addMenu('&Mode')
        #Add Items
        self.fileMenu.addAction(self.page0)
        self.fileMenu.addAction(self.page1)
        self.fileMenu.addAction(self.page2)
        self.fileMenu.addAction(self.page3)
        self.fileMenu.addAction(self.page4)
#######################
#function to change button from a start to a stop (change styl and text)
    def ButtonClick(self):
    #what button sent the command??
        sending_button = self.sender()
        name = sending_button.objectName()
        self.ChangeButton(name)
    
    def ChangeButton(self, name, chk=""):
    #what button sent the command??
        sending_button = self.findChild(QtGui.QPushButton, name)
        text = sending_button.text()
    #Was it a start button?
        if text[0:5] == "Start" and chk != "Stop":    #Start button to Stop
            text = "Stop!%s" %text[5:]
            sending_button.setText(text)
            sending_button.setStyleSheet(ButtonStopStyle)
            self.ablebt(name,False)
        elif text[0:5] == "Stop!":  #Stop button to Start
            text = "Start%s" %text[5:]
            sending_button.setText(text)
            sending_button.setStyleSheet(ButtonStyle)
            self.ablebt(name,True)

        elif text[-4:] == "Stop":   #Setup Stop  button
            text = text[0:-5]
            sending_button.setText(text)
            sending_button.setStyleSheet(ButtonStyle)
            self.ablebt(name,True)
        elif chk != "Stop":                       #Setup start Button
            text = "%s Stop" %text
            sending_button.setText(text)
            sending_button.setStyleSheet(ButtonStopStyle)
            self.ablebt(name,False)

# disable/enable all other Lasr buttons (that way you can't try to start more then one thing)
    def ablebt(self,name,TF):
        if name != "Motor":
            Selection=['NRG','Volt', 'PLID', 'Fill', 'Flush', 'Pline', 'PRes', 'Cal']
            for button in Selection:
                if button != name:
                    Obj = self.findChild(QtGui.QPushButton, button)
                    Obj.setEnabled(TF)


#####################################################
#####################################################	
#Setup Basic Gui Page that will be inherited by others (Lowers amount of code)
class Basic(QtGui.QWidget):
    def __init__(self):
        super(Basic, self).__init__()
        self.setupUi() # make the UI  See Bellow
    def  setupUi(self):
        #Setup Title
        self.Title = QtGui.QLabel()
        self.Title.setFont(font_T)
        self.Title.setAlignment(QtCore.Qt.AlignCenter)
	#Value input
        self.val= QtGui.QSpinBox()
        #self.val.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.Label1 = QtGui.QLabel()
        self.Label1.setFont(font_L)
	#Frequency
        self.hz = QtGui.QSpinBox()
        self.hz.setRange(0,30)
        self.hz.setSingleStep(1)
        self.hz.setValue(10)
        #self.hz.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))     
        self.Label2 = QtGui.QLabel()
        self.Label2.setText(_fromUtf8("Frequency [Hz]:"))
        self.hz.setToolTip(_fromUtf8('Please input an integer between 0 and 20'))
        self.Label2.setFont(font_L)
        #Button
        self.Button = QtGui.QPushButton(_fromUtf8("Start Laser"))
        self.Button.resize(100, 60)
        self.Button.setFont(font_B)
        self.Button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Button.setStyleSheet(ButtonStyle)
        
#####################################################
#Setup Energy Controlled Page
class NRG(Basic): # inherit from basic class above
    def __init__(self):
        super(NRG, self).__init__()
        self.setupUiedits()
        self.initUi()

    def  setupUiedits(self): #change things about the basic gui
        self.Title.setText(_fromUtf8("Laser Energy Controller"))
        self.val.setRange(0,400)
        self.val.setSingleStep(25)
        self.val.setValue(200)
        self.Button.setObjectName(_fromUtf8("NRG"))
        self.val.setToolTip(_fromUtf8('Please input an integer between 0 and 350'))
        self.Label1.setText(_fromUtf8("Energy [mJ]:"))

        self.val.setObjectName("NRG.val")
        self.hz.setObjectName("NRG.hz")

    def  initUi(self):
        #Setup Form
        self.FormLayout = QtGui.QFormLayout()
        self.FormLayout.addRow(self.Label1, self.val)
        self.FormLayout.addRow(self.Label2, self.hz)
        #Setup Vertical Box Layout
        self.vbox = QtGui.QVBoxLayout()
        #add Layouts
        self.vbox.addWidget(self.Title)
        self.vbox.addLayout(self.FormLayout)
        self.vbox.addWidget(self.Button)
    #Finish Page Setup
        self.setLayout(self.vbox)
#####################################################	
#Setup Voltage Controlled Page
class Volt(Basic): # inherit from basic class above
    def __init__(self):
        super(Volt, self).__init__()
        self.setupUiedits()
        self.initUi()

    def  setupUiedits(self):  #change things about the basic gui
        self.Title.setText(_fromUtf8("Laser Voltage Controller"))
        self.val.setRange(0,35)
        self.val.setSingleStep(1)
        self.val.setValue(30)
        self.Button.setObjectName(_fromUtf8("Volt"))
        self.val.setToolTip(_fromUtf8('Please input an integer between 0 and ???'))
        self.Label1.setText(_fromUtf8("Voltage [kV]:"))

    def  initUi(self):
        #Setup Form
        self.FormLayout = QtGui.QFormLayout()
        self.FormLayout.addRow(self.Label1, self.val)
        self.FormLayout.addRow(self.Label2, self.hz)
        #Setup Vertical Box Layout
        self.vbox = QtGui.QVBoxLayout()
        #add Layouts
        self.vbox.addWidget(self.Title)
        self.vbox.addLayout(self.FormLayout)
        self.vbox.addWidget(self.Button)
    #Finish Page Setup
        self.setLayout(self.vbox)
#####################################################
#Setup PLID Controlled Page
class PLID(QtGui.QWidget): #inherit from regular widget
    def __init__(self):
        super(PLID, self).__init__()
        self.setupUi() # make the UI  See Bellow
        self.initUi()
  
    def  setupUi(self):
        #Setup Title
        self.Title = QtGui.QLabel()
        self.Title.setFont(font_T)
        self.Title.setAlignment(QtCore.Qt.AlignCenter)
        self.Title.setText(_fromUtf8("Laser PLID Controller"))
        #vertical lables
        self.VLab1 = QtGui.QLabel()
        self.VLab1.setFont(font_L)
        self.VLab1.setText(_fromUtf8(""))

        self.VLab2 = QtGui.QLabel()
        self.VLab2.setFont(font_L)
        self.VLab2.setText(_fromUtf8("NRG [mJ]:"))

        self.VLab3 = QtGui.QLabel()
        self.VLab3.setFont(font_L)
        self.VLab3.setText(_fromUtf8("Freq [Hz]:"))

        self.VLab4 = QtGui.QLabel()
        self.VLab4.setFont(font_L)
        self.VLab4.setText(_fromUtf8("Time [s]:"))

                
        #horizontal lables    
        self.Lab1 = QtGui.QLabel()
        self.Lab1.setFont(font_L)
        self.Lab1.setText(_fromUtf8("Iteration 1:"))

        self.Lab2 = QtGui.QLabel()
        self.Lab2.setFont(font_L)
        self.Lab2.setText(_fromUtf8("Iteration 2:"))

        self.Lab3 = QtGui.QLabel()
        self.Lab3.setFont(font_L)
        self.Lab3.setText(_fromUtf8("Iteration 3:"))

	#NRG1 input
        self.NRG1 = QtGui.QSpinBox()
        self.NRG1.setRange(0,400)
        self.NRG1.setSingleStep(25)
        self.NRG1.setValue(200)
        #NRG2 input
        self.NRG2 = QtGui.QSpinBox()
        self.NRG2.setRange(0,400)
        self.NRG2.setSingleStep(25)
        self.NRG2.setToolTip(_fromUtf8('Please input an integer between 0 and ???'))
        self.NRG2.setValue(200)
        #NRG3 input
        self.NRG3 = QtGui.QSpinBox()
        self.NRG3.setRange(0,400)
        self.NRG3.setSingleStep(25)
 	
        #hz1 input
        self.frq1 = QtGui.QSpinBox()
        self.frq1.setRange(0,30)
        self.frq1.setSingleStep(1)
        self.frq1.setValue(10)
        self.frq1.valueChanged.connect(lambda: self.reps_and_time("Reps")) 

        #hz3 input
        self.frq2 = QtGui.QSpinBox()
        self.frq2.setRange(0,30)
        self.frq2.setSingleStep(1)
        self.frq2.setValue(10)
        self.frq2.valueChanged.connect(lambda: self.reps_and_time("Reps"))  #see below

        #hz3 input
        self.frq3 = QtGui.QSpinBox()
        self.frq3.setRange(0, 30)
        self.frq3.setSingleStep(1)
        self.frq3.valueChanged.connect(lambda: self.reps_and_time("Reps")) 

        #time1 input
        self.sec1 = QtGui.QDoubleSpinBox()
        self.sec1.setRange(0,300)
        self.sec1.setSingleStep(0.5)
        self.sec1.setValue(2)
        self.sec1.valueChanged.connect(lambda: self.reps_and_time("Reps")) 

        #time3 input
        self.sec2 = QtGui.QDoubleSpinBox()
        self.sec2.setRange(0,300)
        self.sec2.setSingleStep(0.5)
        self.sec2.setValue(3)
        self.sec2.valueChanged.connect(lambda: self.reps_and_time("Reps"))

        #time3 input
        self.sec3 = QtGui.QDoubleSpinBox()
        self.sec3.setRange(0,300)
        self.sec3.setSingleStep(0.5)
        self.sec3.valueChanged.connect(lambda: self.reps_and_time("Reps")) 

        #Time total input
        self.Time = QtGui.QDoubleSpinBox()
        self.Time.setRange(0,240)
        self.Time.setSingleStep(5)
        #self.Time.setValue(10)
        self.TimeLb = QtGui.QLabel()
        self.TimeLb.setFont(font_L)
        self.TimeLb.setText(_fromUtf8("Total Run Time [min]:"))
        self.Time.setObjectName(_fromUtf8("Time"))
        self.Time.valueChanged.connect(lambda:self.reps_and_time("Time")) 

        #Total Reps input
        self.reps = QtGui.QSpinBox()
        self.reps.setRange(1,1000)
        self.reps.setSingleStep(5)
        self.repsLb = QtGui.QLabel()
        self.repsLb.setFont(font_L)
        self.repsLb.setText(_fromUtf8("Total Repititions:"))
        self.reps.setObjectName(_fromUtf8("Reps"))
        self.reps.valueChanged.connect(lambda: self.reps_and_time("Reps")) 
        
        #Calculated Total Pulses
        self.pulses = QtGui.QLCDNumber()
        self.pulses.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.pulses.setStyleSheet(styl)
        self.pulses.setMinimumSize(46,30) #Width, height
        self.pulses.setDigitCount(3)
        self.pulses.display(123)
        self.pulsesLB = QtGui.QLabel()
        self.pulsesLB.setText(_fromUtf8("Total Pulses:"))
        self.pulsesLB.setFont(font_L)

        #Button
        self.Button = QtGui.QPushButton("Start Laser")
        self.Button.resize(100, 60)
        self.Button.setFont(font_B)
        self.Button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Button.setObjectName(_fromUtf8("PLID"))
        self.Button.setStyleSheet(ButtonStyle)


        self.reps.setValue(10)
        self.setStatusTip(_fromUtf8("Set to time to 0 if itteration is unneeded."))

    def  initUi(self):
    #Setup Grid Layout
        self.grid = QtGui.QGridLayout()  #row, col[,end row, end col(for multi grid)]
        #add Layouts column1
        self.grid.addWidget(self.VLab1,1,1)
        self.grid.addWidget(self.VLab2,2,1)
        self.grid.addWidget(self.VLab3,3,1)
        self.grid.addWidget(self.VLab4,4,1)

        #add Layouts column2
        self.grid.addWidget(self.Lab1,1,2)
        self.grid.addWidget(self.NRG1,2,2)
        self.grid.addWidget(self.frq1,3,2)
        self.grid.addWidget(self.sec1,4,2)

        #add Layouts column3
        self.grid.addWidget(self.Lab2,1,3)
        self.grid.addWidget(self.NRG2,2,3)
        self.grid.addWidget(self.frq2,3,3)
        self.grid.addWidget(self.sec2,4,3)

        #add Layouts column4
        self.grid.addWidget(self.Lab3,1,4)
        self.grid.addWidget(self.NRG3,2,4)
        self.grid.addWidget(self.frq3,3,4)
        self.grid.addWidget(self.sec3,4,4)
        #add Layouts Bottom Row1
        self.hbox1 = QtGui.QHBoxLayout()
        self.hbox1.addWidget(self.pulsesLB)
        self.hbox1.addWidget(self.pulses)
        #add Layouts Bottom Row2
        self.hbox2 = QtGui.QHBoxLayout()
        self.hbox2.addWidget(self.TimeLb)
        self.hbox2.addWidget(self.Time)
        self.hbox2.addWidget(self.repsLb)
        self.hbox2.addWidget(self.reps)

    #Setup Vertical box of all
        self.vbox = QtGui.QVBoxLayout()
        self.vbox.addWidget(self.Title)
        self.vbox.addLayout(self.grid)
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        self.vbox.addWidget(self.Button)
    #Finish Page Setup
        self.setLayout(self.vbox)
    
#PLID reps buttons (make time and reps connected)    
    def reps_and_time(self,name):
        sec1 = self.sec1.value()
        sec2 = self.sec2.value()
        sec3 = self.sec3.value()
        total = sec1 + sec2 + sec3
        hz1 = self.frq1.value()
        hz2 = self.frq2.value()
        hz3 = self.frq2.value()
        reps = self.reps.value() 

        if name == "Reps":
            self.Time.setValue((reps * total) / 60)
            self.pulses.display(reps * (sec1 * hz1 + sec2 * hz2 + sec3 * hz3))

        elif name == "Time":
            self.reps.setValue(int(round((self.Time.value() * 60) / total)))

#####################################################
#Setup Setup Laser Page
class Setup(QtGui.QWidget): #inherit from regular widget
    def __init__(self):
        super(Setup, self).__init__()
        self.setupUi() # make the UI  See Bellow
        self.initUi()
  
    def  setupUi(self):
        #Setup Title
        self.Title = QtGui.QLabel()
        self.Title.setFont(font_T)
        self.Title.setText(_fromUtf8("Laser Setup"))
        self.Title.setAlignment(QtCore.Qt.AlignCenter)
        #Fill Button
        self.FillBt = QtGui.QPushButton("New Fill")
        self.FillBt.resize(100, 60)
        self.FillBt.setFont(font_B)
        self.FillBt.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.FillBt.setObjectName("Fill")
        self.FillBt.setStyleSheet(ButtonStyle)
        #Flush Button
        self.FlushBt = QtGui.QPushButton("Flush Line (Evacuate Line for 2 sec)")
        self.FlushBt.resize(100, 60)
        self.FlushBt.setFont(font_B)
        self.FlushBt.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) 
        self.FlushBt.setObjectName('Flush')
        self.FlushBt.setStyleSheet(ButtonStyle)
        #Purge Line Button
        self.PlinBt = QtGui.QPushButton("Purge Line (Flush and Fill Line With Inert Gas)")
        self.PlinBt.resize(100, 60)
        self.PlinBt.setFont(font_B)
        self.PlinBt.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) 
        self.PlinBt.setObjectName('Pline')
        self.PlinBt.setStyleSheet(ButtonStyle)
        #Purge Resevoir Button
        self.PResBt = QtGui.QPushButton("Purge Reservoir")
        self.PResBt.resize(100, 60)
        self.PResBt.setFont(font_B)
        self.PResBt.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) 
        self.PResBt.setObjectName('PRes')
        self.PResBt.setStyleSheet(ButtonStyle)  
        #Calibration Button
        self.CalBt = QtGui.QPushButton("Energy Calibration")
        self.CalBt.resize(100, 60)
        self.CalBt.setFont(font_B)
        self.CalBt.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) 
        self.CalBt.setObjectName('Cal')
        self.CalBt.setStyleSheet(ButtonStyle)
        
    def  initUi(self):
        #Setup Vertical Box Layout<F3>
        self.vbox = QtGui.QVBoxLayout()
        #add Layouts
        self.vbox.addWidget(self.Title)
        self.vbox.addWidget(self.FillBt)
        self.vbox.addWidget(self.FlushBt)
        self.vbox.addWidget(self.PlinBt)
        self.vbox.addWidget(self.PResBt)
        self.vbox.addWidget(self.CalBt)

    #Finish Page Setup
        self.setLayout(self.vbox)
#####################################################
#Setup Setup Terminal Page
class Terminal(QtGui.QWidget): # inherit from basic class above
    def __init__(self):
        super(Terminal, self).__init__()
        self.setupUi() # make the UI  See Bellow
        self.initUi()
  
    def  setupUi(self):
        #Setup Title
        self.Title = QtGui.QLabel()
        self.Title.setFont(font_T)
        self.Title.setText(_fromUtf8("Control Terminal"))
        self.Title.setAlignment(QtCore.Qt.AlignCenter)
       #input
        self.inpt = QtGui.QTextEdit()
        self.inpt.setFont(font_N)
        self.inpt.setMaximumHeight(30)
        self.inptlb = QtGui.QLabel()
        self.inptlb.setFont(font_L)
        self.inptlb.setText(_fromUtf8("Input:"))
        self.inptlb.setAlignment(QtCore.Qt.AlignCenter)
        self.inpt.setToolTip(_fromUtf8('Check manuals for commands. \
            <br> Only send command (return is atomated).'))
       #Laser Button
        self.laser_send = QtGui.QPushButton("Send to Laser")
        #self.laser_send.resize(10, 60)
        self.laser_send.setFont(font_B)
        self.laser_send.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.laser_send.setStyleSheet(ButtonStyle) 
        #Motor Button
        self.motor_send = QtGui.QPushButton("Send to Motor")
        #self.motor_send.resize(100, 60)
        self.motor_send.setFont(font_B)
        self.motor_send.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) 
        self.motor_send.setStyleSheet(ButtonStyle)
        #Clear History Button
        self.hist_clear = QtGui.QPushButton("Clear History")
        #self.motor_send.resize(100, 60)
        self.hist_clear.setFont(font_B)
        self.hist_clear.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.hist_clear.setStyleSheet(ButtonStyle)
        
        #history text box
        self.hist = QtGui.QTextEdit()
        self.hist.setReadOnly(True)
        self.hist.setFont(font_N)
        self.histlb = QtGui.QLabel()
        self.histlb.setFont(font_L)
        self.histlb.setText(_fromUtf8("Sent and Recieved Codes:"))
        self.histlb.setAlignment(QtCore.Qt.AlignCenter)

    def  initUi(self):
#set up grid layout
        self.vbox = QtGui.QVBoxLayout()
        self.vbox1 = QtGui.QVBoxLayout()
        self.vbox2 = QtGui.QVBoxLayout()
        self.hbox1 = QtGui.QHBoxLayout()
        self.hbox = QtGui.QHBoxLayout()
        #add Layouts
        self.vbox1.addWidget(self.inptlb)
        self.vbox1.addWidget(self.inpt)
        self.hbox1.addWidget(self.laser_send)
        self.hbox1.addWidget(self.motor_send)
        self.vbox1.addLayout(self.hbox1)
        self.vbox1.addWidget(self.hist_clear)
        self.vbox2.addWidget(self.histlb)
        self.vbox2.addWidget(self.hist)
        self.hbox.addLayout(self.vbox1)
        self.hbox.addLayout(self.vbox2)
        self.vbox.addWidget(self.Title)
        self.vbox.addLayout(self.hbox)
    #Finish Page Setup
        self.setLayout(self.vbox)
#####################################################
#Setup for fading between 'stacked' widgets. 
#(advanced and totally extra - not really needed but fun - I could comment/explain if wanted)
class FaderWidget(QtGui.QWidget):

    def __init__(self, old_widget, new_widget):
        #print old_widget, new_widget #for debug
        QtGui.QWidget.__init__(self, new_widget)
        
        self.old_pixmap = QtGui.QPixmap(new_widget.size())
        old_widget.render(self.old_pixmap)
        self.pixmap_opacity = 1.0
        
        self.timeline = QtCore.QTimeLine()
        self.timeline.valueChanged.connect(self.animate)
        self.timeline.finished.connect(self.close)
        self.timeline.setDuration(333)
        self.timeline.start()
        
        self.resize(new_widget.size())
        self.show()
    
    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setOpacity(self.pixmap_opacity)
        painter.drawPixmap(0, 0, self.old_pixmap)
        painter.end()
    
    def animate(self, value):
        self.pixmap_opacity = 1.0 - value
        self.repaint()

class StackedWidget(QtGui.QStackedWidget):

    def __init__(self, parent = None):
        QtGui.QStackedWidget.__init__(self, parent)

    def setCurrentIndex(self, index):
        self.fader_widget = FaderWidget(self.currentWidget(), self.widget(index))
        QtGui.QStackedWidget.setCurrentIndex(self, index)
    
    def setPage(self, index=0): 
        self.setCurrentIndex(index)    

#############################################
## Start up the Gui
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ex =  gui()
    ex.show()
    sys.exit(app.exec_())





