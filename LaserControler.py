from PyQt4 import QtCore, QtGui
import sys  # list of comand line argus need to run Gui
# import serial             # will error if not connected to laser and motor
import fakeSerial as serial           # use this if not connected to serial
import LaserGUI
import time        # yep importing time that way we can go back to the future
import threading

# Setup Global stop variables
laser_on = ""    # 1 = stop laser
motor_on = 0    # 1 = stop motor
AllGuiVars = {}  # initialize All Vars dictionary


class APP(LaserGUI.gui):
    """"This Class is used to create the Gui for the laser and
    to controll it."""

# Creat a python signal that will be used to pass app history stuff
    apphistory = QtCore.pyqtSignal(str)

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)  # See Laser GUI
        # initialize the serial connections
        self.laser_ser = serial.Serial('COM4', 9600, timeout=0.1)
        self.laser_ser.close()
        self.motor_ser = serial.Serial('COM3', 9600, timeout=0.01)
        self.motor_ser.close()

    def run(self):
        global laser_on
        global motor_on
        global AllGuiVars
# Set up Button Click and change event refs (Slots)
        self.NRG.Button.clicked.connect(lambda: self.laser_click())
        # lambda is used to allow you to pass args,  not really needed here...
        self.Volt.Button.clicked.connect(lambda: self.laser_click())
        self.PLID.Button.clicked.connect(lambda: self.laser_click())
        self.motor_button.clicked.connect(lambda: self.motor_click())
        self.Setup.FillBt.clicked.connect(lambda: self.laser_click())
        self.Setup.FlushBt.clicked.connect(lambda: self.laser_click())
        self.Setup.PlinBt.clicked.connect(lambda: self.laser_click())
        self.Setup.PResBt.clicked.connect(lambda: self.laser_click())
        self.Setup.CalBt.clicked.connect(lambda: self.laser_click())
        self.Terminal.laser_send.clicked.connect(
                lambda: self.laser_cmd(self.Terminal.inpt.toPlainText()))
        self.Terminal.motor_send.clicked.connect(
                lambda: self.motor_cmd(self.Terminal.inpt.toPlainText()))
        self.REButton.clicked.connect(lambda: self.laser_check())
        self.Terminal.hist_clear.clicked.connect(self.Terminal.hist.clear)
        # On Value changes update the guiVars dictionary
        # (Not the most efficient way of passing Values but makes it clean)
        self.motor_spd.valueChanged.connect(self.up_motor)
        self.NRG.hz.valueChanged.connect(self.up_EGY)
        self.NRG.val.valueChanged.connect(self.up_EGY)
        self.Volt.hz.valueChanged.connect(self.up_HV)
        self.Volt.val.valueChanged.connect(self.up_HV)
        self.PLID.NRG1.valueChanged.connect(self.up_PLID)
        self.PLID.NRG2.valueChanged.connect(self.up_PLID)
        self.PLID.NRG3.valueChanged.connect(self.up_PLID)
        self.PLID.frq1.valueChanged.connect(self.up_PLID)
        self.PLID.frq2.valueChanged.connect(self.up_PLID)
        self.PLID.frq3.valueChanged.connect(self.up_PLID)
        self.PLID.sec1.valueChanged.connect(self.up_PLID)
        self.PLID.sec2.valueChanged.connect(self.up_PLID)
        self.PLID.sec3.valueChanged.connect(self.up_PLID)
        self.PLID.reps.valueChanged.connect(self.up_PLID)

        self.apphistory.connect(self.Terminal.hist.append)
        self.show()         # show the Gui
        self.update_guiVars()   # update the variables

# Check laser parameters (for refresh button only)
    def laser_check(self):
        # Send output of laser_cmd to displays
        self.laser_tpress.display(self.laser_cmd('PRESSURE?'))
        self.laser_act_nrg.display(self.laser_cmd('EGY?'))
        self.laser_act_volt.display(self.laser_cmd('HV?'))
        self.laser_act_frq.display(self.laser_cmd('REPRATE?'))
        out = self.laser_cmd('OPMODE?')
        self.laser_mess_con(out)

# On Laser Button click
    def laser_click(self):
        global laser_on
        global laser_on
        sending_button = self.sender()
        laser_on = sending_button.objectName()
        text = sending_button.text()
        if text[0:5] == "Stop!" or text[-4:] == "Stop":
            # name is stop as the button has already been changed by the Gui
            self.statusbar.showMessage("Laser Running....")
            self.laser_run()
        else:
            self.statusbar.showMessage("Laser Off")
            # we may want to add this if the laser stop is not fast enough
            # self.laser_cmd("OPMODE=OFF")
            laser_on = ""

# On Motor Button click
    def motor_click(self):
        global motor_on
        self.up_motor()
        sending_button = self.sender()
        text = sending_button.text()

        if text[0:5] == "Stop!":
            self.motor_init()
            # self.statusbar.showMessage("Motor Running....")
            thread1 = threading.Thread(target=self.motor_init)
            thread1.start
            motor_out = "for"
            self.motor_run(motor_out)
        else:
            self.statusbar.showMessage("Motor Off")
            motor_on = 1

# ###            Capture Close and do Stuff          ####
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(
                self, 'Message',
                "Are you sure to quit?", QtGui.QMessageBox.Yes |
                QtGui.QMessageBox.No, QtGui.QMessageBox.No
                )

        if reply == QtGui.QMessageBox.Yes:
            self.motor_cmd("MD")
            self.motor_cmd("QT")
            event.accept()
        else:
            event.ignore()

# ##             Update variables     #####
    def up_motor(self):
        global AllGuiVars
        AllGuiVars["spd"] = self.motor_spd.value()

    def up_EGY(self, val=1, send=True):  # val =place holder for val from box
        global AllGuiVars
        print "EGY"
        # populat AllGuiVars pydictionary
        AllGuiVars["EGY_frq"] = self.NRG.hz.value()
        AllGuiVars["EGY_NRG"] = self.NRG.val.value()
        if send:
            print "sent"
            self.laser_cmd('REPRATE=%d' % AllGuiVars["EGY_frq"])
            self.laser_cmd('EGY=%d' % AllGuiVars["EGY_NRG"])

    def up_HV(self, val=1, send=True):
        global AllGuiVars
        print "HV"
        AllGuiVars["Volt_frq"] = self.Volt.hz.value()
        AllGuiVars["Volt_HV"] = self.Volt.val.value()
        if send:
            print "HV sent"
            self.laser_cmd('REPRATE=%d' % AllGuiVars["Volt_frq"])
            self.laser_cmd('HV=%d' % AllGuiVars["Volt_HV"])

    def up_PLID(self):
        global AllGuiVars
        AllGuiVars["NRG1"] = self.PLID.NRG1.value()
        AllGuiVars["NRG2"] = self.PLID.NRG2.value()
        AllGuiVars["NRG3"] = self.PLID.NRG3.value()
        AllGuiVars["frq1"] = self.PLID.frq1.value()
        AllGuiVars["frq2"] = self.PLID.frq2.value()
        AllGuiVars["frq3"] = self.PLID.frq3.value()
        AllGuiVars["sec1"] = self.PLID.sec1.value()
        AllGuiVars["sec2"] = self.PLID.sec2.value()
        AllGuiVars["sec3"] = self.PLID.sec3.value()
        AllGuiVars["reps"] = self.PLID.reps.value()

    def update_guiVars(self):
        self.up_motor()
        self.up_EGY(1, False)
        self.up_HV(1, False)
        self.up_PLID()

# ######### Laser run commands ##################
    def laser_run(self):
        global laser_on
        global AllGuiVars
        # print "before check: %s" %AllGuiVars       # for testing
        self.update_guiVars()
    # Laser PLID Controlled
        if laser_on == "PLID":
            self.laser_cmd('MODE=EGY NGR')
            iterations = 0
            i = 0
            self.chck_on()  # start laser continue ifs on
    # Laser NRG Controlled
        elif laser_on == "NRG":
            self.laser_cmd('MODE=EGY NGR')
            self.laser_cmd('REPRATE=%d' % AllGuiVars["EGY_frq"])
            self.laser_cmd('EGY=%d' % AllGuiVars["EGY_NRG"])
            self.chck_on()
    # Laser Volt Controlled
        elif laser_on == "Volt":
            self.laser_cmd('MODE=HV')
            self.laser_cmd('REPRATE=%d' % AllGuiVars["Volt_frq"])
            self.laser_cmd('HV=%d' % AllGuiVars["Volt_HV"])
            self.chck_on()
            # run the laser loop (Keeps it running / does plid)
    # New Fill
        elif laser_on == 'Fill':
            reply = QtGui.QMessageBox.question(
                    self, 'Message',
                    "Tank is open, Buffer line is flushed, \
                    and you are ready for a new fill?",
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                    QtGui.QMessageBox.No
                    )
            if reply != QtGui.QMessageBox.Yes:
                super(APP, self).ChangeButton(laser_on, "Stop")
                laser_on = ""
                return
            # print "new ok"
            self.laser_cmd('OPMODE=NEW FILL')
            # Laser does not need polling here
            # but this allows the button to be used as a kill button
            self.laser_run_check()
    # Flush Line
        elif laser_on == 'Flush':
            items = ("BUFFER", "HALOGEN", "INERT", "RARE")
            out, ok = QtGui.QInputDialog.getItem(
                    self, "Purge line",
                    "Before clicking 'ok' make sure gas tank is closed. \
                    <br> Please select line to flush: ", items, 0, False
                    )
            if ok:
                # print "Flush ok %s" %out
                self.laser_cmd('OPMODE=FLUSH %s LINE' % out)
                self.laser_run_check()
            else:
                super(APP, self).ChangeButton(laser_on, "Stop")
                laser_on = ""
    # Purge Line
        elif laser_on == 'Pline':
            items = ("BUFFER", "HALOGEN", "INERT", "RARE")
            out, ok = QtGui.QInputDialog.getItem(
                    self, "Purge line", "Before clicking 'ok' make sure gas \
                    tank is closed. <br> Please select line to purge:",
                    items, 0, False
                    )
            if ok:
                # print "purgeline ok %s" %out
                self.laser_cmd('OPMODE=PURGE %s LINE' % out)
                self.laser_run_check()
            else:
                super(APP, self).ChangeButton(laser_on, "Stop")
                laser_on = ""
    # Purge Resivior
        elif laser_on == 'PRes':
            reply = QtGui.QMessageBox.question(
                    self, 'Message', "Please \
                    ensure the tank is closed! <br> Begin \
                    Purge?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                    QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                self.laser_cmd('OPMODE=PURGE RESERVOIR')
                self.laser_run_check()
            else:
                super(APP, self).ChangeButton(laser_on, "Stop")
                laser_on = ""
    # Energy Calibration Confirm these values with Ashley
        elif laser_on == 'Cal':
            self.laser_cmd('MODE=HV')
            self.laser_cmd('REPRATE=10')
            self.laser_cmd('HV=27')

            reply = QtGui.QMessageBox.question(
                    self, 'Message', "Please \
                    ensure the shutter is closed! <br> Laser will begin \
                    warm up.", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                    QtGui.QMessageBox.No
                    )
            if reply != QtGui.QMessageBox.Yes:
                super(APP, self).ChangeButton(laser_on, "Stop")
                laser_on = ""
                return
            self.laser_cmd('OPMODE=ON')
            self.laser_run_check()  # start loop to keep laser on to warm up

            # start a message box that counts down
            # allow the laser to warm up for 100 sec
            self.CountDownMsg("Pressing Abort will cancel the warm up. \
                              <br> Warming Up For: ", 100)

            # start the energy cal (Laser is still running)
            self.laser_cmd('OPMODE=OFF')
            laser_on = ""
            QtCore.QTimer.singleShot(5000, self.EGY_CAL_CON)

    def EGY_CAL_CON(self):
        global laser_on
        self.laser_cmd('OPMODE=ENERGY CAL')
        laser_on = 'Cal'
        self.laser_run_check([2, 5])
        # QtCore.QTimer.singleShot(250, self.laser_run_check)
        out, ok = QtGui.QInputDialog.getInt(
                    self, "Energy Calibration",
                    "Please enter measured energy:", 300, 1, 400)
        if ok:
                self.laser_cmd('EGY=%d' % out)
        super(APP, self).ChangeButton(laser_on, "Stop")
        laser_on = ""

# make message box that runs a count down
    def CountDownMsg(self, Msg, duration=10):
        global laser_on
        msgBox = QtGui.QMessageBox(self)
        button = msgBox.addButton(QtGui.QMessageBox.Abort)
        Time = time.time()
        stop = Time + duration  # figure out when to stop
        while time.time() < stop:
            timer = int(duration - (time.time() - Time))
            msgBox.setText(Msg + str(timer))
            msgBox.show()
            QtGui.QApplication.processEvents()
            ret = msgBox.clickedButton()
            if ret == button:
                msgBox.close()
                break
            elif time.time() >= stop:
                msgBox.close()
                break
            else:
                QtGui.QApplication.processEvents()

# laser Loop
    def PLID_loop(self, iterations, i):
        global laser_on
        global AllGuiVars
        if i < 3:
            i += 1
        elif i == 3:
            i = 1
            iterations += 1
            print "it: %d" % iterations
        # print "Start: %s" %str(time.time())
        print i
        print AllGuiVars["sec" + str(i)]
        stop = time.time() + int(AllGuiVars["sec" + str(i)])
        # print "Stop: %s" %str(stop)
        while True:
            self.laser_cmd('REPRATE=%d' % AllGuiVars["frq" + str(i)])
            self.laser_cmd('EGY=%d' % AllGuiVars["NRG" + str(i)])
            QtGui.QApplication.processEvents()
            if time.time() >= stop:      # break and continue to next it
                break
            elif laser_on == "":       # stop on button press
                break
            else:
                QtGui.QApplication.processEvents()
                time.sleep(0.01)  # this plus below sets the iteration acuracy
                # print "PLID inner" + str(time.time())  # learn how long take

        # if max itts reached of stop has been issued (laser_on changed to "")
        if iterations == AllGuiVars["reps"] or laser_on == "":
            self.laser_stop()
            return
        else:
            print "Main Laser " + str(time.time())  # learn how long this take
            QtCore.QTimer.singleShot(
                    10, lambda: self.laser_loop(iterations, i))

# Turn the laser on and check the on status of the laser
    def chck_on(self):
        global laser_on
        out = self.laser_cmd('OPMODE=ON')
        self.laser_mess_con(out)  # convert message recieved cmd and display
        # print out[0:4]
        if out[0:4] == "OFF:" or laser_on == "":
            self.laser_stop()
            return "off"
        else:
            self.laser_run_check()      # start polling to keep laser on
            return "on"

# Method to stop the laser
    def laser_stop(self, kill=True):
        global laser_on
        if laser_on != "":
            if kill:
                # print "laser stopping"  #for debug
                self.laser_cmd('OPMODE=OFF')   # turn off the Laser
            self.statusbar.showMessage("Laser Off")
            super(APP, self).ChangeButton(laser_on, "Stop")
            if laser_on == "Fill":
                QtGui.QMessageBox.question(
                        self, 'Message',
                        "Did you close the poisen?", QtGui.QMessageBox.Yes
                        )
            laser_on = ""        # set the laser_on to ""  to stop all loops

# Send Commands to Laser
    def laser_cmd(self, cmd):
        self.emit(QtCore.SIGNAL('apphistory(QString)'),
                  time.strftime('%y-%m-%d %H:%M:%S'))
        run_cmd = str(cmd).strip() + "\r"
        self.emit(QtCore.SIGNAL('apphistory(QString)'),
                  "Laser SEND: %s" % str(cmd).strip())
        # print "Laser SEND: %s" % cmd.strip()       #for debug
        self.laser_ser.open()       # open the serial port
        self.laser_ser.write(run_cmd)
        result = self.laser_ser.read(40)
        self.laser_ser.close()      # close the serial port
        self.emit(QtCore.SIGNAL('apphistory(QString)'),
                  "Laser RECV: %s" % str(result).strip())
        # print "Laser RECV: %s" % result.strip()    #for debug
        return str(result).strip()

# Check laser parameters
    def laser_run_check(self, use=[0, 1, 2, 3, 4], speed=500, num=1):
        # stop if laser is not on or button is pressed
        # if laser returns off turn off the loop (but lets run for OFF, Wait)
        # Laser Polling Commands
        cmd = {0: 'PRESSURE?',
               1: 'REPRATE?',
               2: 'EGY?',
               3: 'HV?',
               4: 'OPMODE?',
               5: 'OPMODE?'}

        # Display's
        func = {0: self.laser_tpress.display,
                1: self.laser_act_frq.display,
                2: self.laser_act_nrg.display,
                3: self.laser_act_volt.display,
                4: self.laser_OP_check,
                5: self.laser_messages.setPlainText}
        if laser_on != "":
            num = use[0]
            use.append(use.pop(0))
            # print use   # for debug
            # Send output of laser_cmd to displays
            func[num](self.laser_cmd(cmd[num]))
            # restart this funct after 'speed'
            QtCore.QTimer.singleShot(
                    speed, lambda:
                    self.laser_run_check(use, speed, num))
        else:
            self.laser_stop()

    def laser_OP_check(self, out):
        # if laser returns off turn off the loop (but lets run for OFF, Wait)
        if out[0:4] == "OFF:":
            self.laser_stop(False)      # no need to kill it's already dead
        # if the code is new check the message meaning and print to the display
        txt = str(self.laser_messages.toPlainText())
        if txt.find(out) == -1:
            # print "True"
            self.laser_mess_con(out)
        else:
            self.laser_messages.setPlainText(out)
            # stop if laser is not on or button is pressed

# Laser messages - convet to real meaning
    def laser_mess_con(self, code):
        if code == "":
            return ""
        message = ["", ""]
        txt = ""
        with open("Laser_Codes.csv") as data_file:
            for row in data_file:
                if code in row:
                    message = row.split("\t")
                    message.append("")          # fix error??
        txt = code + " - " + message[1]
        self.laser_messages.setPlainText(txt)
        return txt

# run The Motor
    def motor_run(self, motor_out):
        global motor_on
        global AllGuiVars
        half_turn = 5236  # =1600/11*36  total in 360 / smallsprk * largesprok
        self.motor_ser.close()     # make sure the serial connection is closed
        self.motor_cmd("VE%s" % AllGuiVars["spd"])
        QtGui.QApplication.processEvents
        # print motor_out
        if motor_out == "for":
            self.motor_cmd("FL-%d" % half_turn)
            QtGui.QApplication.processEvents
            self.motor_cmd('SSbac')
        elif motor_out == "bac":
            self.motor_cmd("FL%d" % half_turn)
            QtGui.QApplication.processEvents
            self.motor_cmd('SSfor')
        self.motor_ser.open()
        # repeat in 1 sec motor is spinning so it should be fine
        QtCore.QTimer.singleShot(1000, self.ms_loop)

    def ms_loop(self):
        global motor_on
        motor_out = self.motor_ser.readline()
        # QtGui.QApplication.processEvents()      #allow other stuff to happen
        # print 'out: %s' %motor_out     #for debug
        motor_out = motor_out.strip()
        if motor_on == 1:
            self.motor_ser.close()
            # stop kill add if we want to stop the motor instantly
            # self.motor_cmd("SK")
            motor_on = 0
            self.motor_cmd("MD")  # set motor to free spin
        elif motor_out != "":
            QtCore.QTimer.singleShot(10, lambda: self.motor_run(motor_out))
            # print motor_out  + "-" + str(time.time())
        else:
            QtCore.QTimer.singleShot(10, self.ms_loop)

    def motor_cmd(self, cmd):
        # print the time and date to the terminal
        self.emit(QtCore.SIGNAL('apphistory(QString)'),
                  time.strftime('%y-%m-%d %H:%M:%S'))
        run_cmd = str(cmd).strip() + "\r"
        # send signal to writ to app history
        self.emit(QtCore.SIGNAL('apphistory(QString)'),
                  "Motor SEND: %s" % str(cmd).strip())
        # print "Motor SEND: %s" % cmd.strip()       #for debug
        self.motor_ser.open()           # open the serial port
        self.motor_ser.write(run_cmd)
        result = self.motor_ser.readline()
        self.motor_ser.close()          # close the serial port
        # send signal to writ to app history
        self.emit(QtCore.SIGNAL('apphistory(QString)'),
                  "Motor RECV: %s" % str(result).strip())
        # print "Motor RECV: %s" % result.strip()    #for debug
        return result.strip()

# Initialize Motor
    def motor_init(self):
        self.motor_ser.open()           # open the serial port
        cmds = ["HR", "ME", "AR", "SC", "CM21", "AC25","DE25", "EG1600"]
        for cm in cmds:
            print cm
            self.motor_ser.write(cm)
            result = self.motor_ser.readline()
        self.motor_ser.close()          # close the serial port

# start it all up
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ex = APP()
    # ex.show()
    QtCore.QTimer.singleShot(10, ex.run)
    sys.exit(app.exec_())
