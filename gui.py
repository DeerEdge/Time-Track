# Import PyQt5's widgets to be used throughout the program
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore, QtWidgets

# A class is created that holds all functions of the program
class ui_main_window(object):
    # This function setups up a basic window where widgets can be added
    def setup_window(self, main_window):
        main_window.setWindowTitle("Time Track")
        main_window.setObjectName("main_window")
        # The size of the window is specified using "resize()"
        main_window.setFixedSize(800, 500)

        self.setup_login_screen(main_window)

    def setup_login_screen(self, main_window):
        self.login_central_widget = QtWidgets.QWidget(main_window)
        self.login_central_widget.resize(800, 500)
        self.login_screen_background = QtWidgets.QLabel(self.login_central_widget)
        self.login_screen_background.setFixedSize(800, 500)
        self.login_screen_background.setPixmap(QtGui.QPixmap("Application Pictures and Icons/Login Screen Background.png"))
        self.login_screen_background.setScaledContents(True)
        self.login_screen_background.show()
        self.login_widget_container = QtWidgets.QGroupBox(self.login_central_widget)
        self.login_widget_container.resize(800, 500)

        # Application Logo
        self.login_screen_logo = QtWidgets.QLabel(self.login_widget_container)
        self.login_screen_logo.setFixedSize(200, 200)
        self.login_screen_logo.move(-20, -75)
        self.login_screen_logo.setPixmap(
            QtGui.QPixmap("Application Pictures and Icons/Time Track Logo.png"))
        self.login_screen_logo.setScaledContents(True)
        self.login_screen_logo.show()

        # Student Login
        self.student_login_title = self.create_QLabel("login_widget_container", "login_titles", "Student Login", 145,
                                                      80, 200, 50)
        self.student_username_label = self.create_QLabel("login_widget_container", "login_screen_labels", "Email ID",
                                                         80, 122, 200, 50)
        self.student_username = self.create_QLineEdit("login_widget_container", "login_screen_text_fields", 80, 160,
                                                      240, 30)
        self.student_password_label = self.create_QLabel("login_widget_container", "login_screen_labels", "Password",
                                                         80, 187, 200, 50)
        self.student_password = self.create_QLineEdit("login_widget_container", "login_screen_text_fields", 80, 225,
                                                      240, 30)
        self.student_forgot_password = self.create_QPushButton("login_widget_container", "login_screen_forgot_password",
                                                               "Forgot password?", "None", 65, 255, 140, 30)
        self.student_login_button = self.create_QPushButton("login_widget_container", "student_login_button", "Login", "None",
                                                            80, 290, 240, 30)
        self.student_login_button.clicked.connect(self.setup_home_page)

        # Line divider between logins
        self.login_divider_line = self.create_QFrame("login_widget_container", "login_screen_elements", "VLine", 399,
                                                     40, 1, 410)

        # Administrator Login
        self.administrator_login_title = self.create_QLabel("login_widget_container", "login_titles",
                                                            "Administrator Login",
                                                            525, 80, 200, 50)
        self.administrator_username_label = self.create_QLabel("login_widget_container", "login_screen_labels", "Email ID",
                                                         480, 122, 200, 50)
        self.administrator_username = self.create_QLineEdit("login_widget_container", "login_screen_text_fields", 480, 160,
                                                      240, 30)
        self.administrator_password_label = self.create_QLabel("login_widget_container", "login_screen_labels", "Password",
                                                         480, 187, 200, 50)
        self.administrator_password = self.create_QLineEdit("login_widget_container", "login_screen_text_fields", 480, 225,
                                                      240, 30)
        self.administrator_forgot_password = self.create_QPushButton("login_widget_container", "login_screen_forgot_password",
                                                               "Forgot password?", "None", 465, 255, 140, 30)
        self.administrator_login_button = self.create_QPushButton("login_widget_container", "administrator_login_button", "Login", "None",
                                                            480, 290, 240, 30)

    def setup_home_page(self):
        sending_button = self.login_widget_container.sender().objectName()
        self.login_widget_container.hide()
        self.login_screen_background.clear()

        main_window.setFixedSize(1000, 700)
        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("central_widget")
        self.central_widget.resize(1000, 700)

        self.app_logo = QtWidgets.QLabel(self.central_widget)
        self.app_logo.setFixedSize(140, 140)
        self.app_logo.move(20, 10)
        self.app_logo.setPixmap(
            QtGui.QPixmap("Application Pictures and Icons/Time Track Icon.png"))
        self.app_logo.setScaledContents(True)
        self.app_logo.show()

        self.intro_label = self.create_QLabel("central_widget", "intro_label", "Signed in as Wallace McCarthy",
                                              200, 10, 600, 50)

        self.tab_widget = VerticalTabWidget(self.central_widget)
        self.tab_widget.setObjectName("tab_widget")
        self.tab_widget.resize(1000, 650)
        self.tab_widget.move(0, 55)

        if sending_button == "student_login_button":
            self.dashboard_tab = QtWidgets.QWidget()
            self.upcoming_events_tab = QtWidgets.QWidget()
            self.points_tab = QtWidgets.QWidget()
            self.profile_tab = QtWidgets.QWidget()

            self.tab_widget.addTab(self.dashboard_tab, "Dashboard")
            self.tab_widget.addTab(self.upcoming_events_tab, "Upcoming Events")
            self.tab_widget.addTab(self.points_tab, "Points")
            self.tab_widget.addTab(self.profile_tab, "My Student Profile")

            self.dashboard_widget = QtWidgets.QWidget(self.dashboard_tab)
            self.upcoming_events_widget = QtWidgets.QWidget(self.upcoming_events_tab)
            self.points_widget = QtWidgets.QWidget(self.points_tab)
            self.profile_widget = QtWidgets.QWidget(self.profile_tab)

            self.dashboard_label = self.create_QLabel("dashboard_widget", "dashboard_label", "Dashboard",
                                              20, 20, 600, 50)
            self.dashboard_title_line = self.create_QFrame("dashboard_widget", "dashboard_title_line", "HLine",
                                                         10, 65, 600, 6)
            # upcomming events page
            #Title
            self.upcoming_events_label = self.create_QLabel("upcoming_events_widget", "upcoming_events_label",
                                                            "Upcoming",
                                                            20, 20, 600, 50)
            self.upcoming_events_title_line = self.create_QFrame("upcoming_events_widget", "upcoming_events_title_line",
                                                                 "HLine",
                                                                 10, 65, 600, 6)

            #body
            self.calender = QtWidgets.QCalendarWidget(self.upcoming_events_tab)
            self.calender.setGeometry(20, 50, 350, 350)
            self.day_events = self.create_QLineEdit("upcoming_events_tab", "day_events", 400, 50, 400, 350)
            self.upcoming_events = self.create_QLineEdit("upcoming_events_tab", "upcoming_events", 20, 425, 780, 200)

            # points page
            self.personal_points = self.create_QLineEdit("points_tab", "personal_points", 20, 50, 300, 300)
            self.points_leaderboard = self.create_QLineEdit("points_tab", "point_leaderboard", 350, 50, 450, 300)





            #self.incompeted_tasks_tab = QtWidgets.QTabWidget(self.points_tab)
            #self.incompeted_tasks_tab.addTab(self.points_tab, self.incompleted_tasks_tab, "hello")

            #self.tab_point_widget = QTabWidget()
            #self.tab_point_widget.setObjectName("tab_widget")
            #self.tab_point_widget.resize(500, 650)
            #self.tab_point_widget.move(100, 200)

            #self.incompleted_events_tab = QtWidgets.QWidget()
            #self.prevous_events_tab = QtWidgets.QWidget()
            #self.tab_point_widget.addTab(self.incompleted_events_tab, "Incompleted Events")
            #self.tab_point_widget.addTab(self.prevous_events_tab, "Prevous Events")


        self.tab_widget.show()
        main_window.setCentralWidget(self.central_widget)



    def create_QLabel(self, container, object_name, text, x_coordinate, y_coordinate, width, length):
        # Creates and associates QLabel to specified container
        if container == "login_widget_container":
            self.QLabel = QtWidgets.QLabel(self.login_widget_container)
        elif container == "central_widget":
            self.QLabel = QtWidgets.QLabel(self.central_widget)
        elif container == "dashboard_widget":
            self.QLabel = QtWidgets.QLabel(self.dashboard_widget)
        self.QLabel.setObjectName(object_name)
        self.QLabel.setText(text)
        # Geometry of QLabel is specified by the passed function parameters
        self.QLabel.setGeometry(QtCore.QRect(x_coordinate, y_coordinate, width, length))
        return self.QLabel

    def create_QLineEdit(self, container, object_name, x_coordinate, y_coordinate, width, length):
        # Creates and associates QLabel to specified container
        if container == "login_widget_container":
            self.QLineEdit = QtWidgets.QLineEdit(self.login_widget_container)
        elif container == "upcoming_events_tab":
            self.QLineEdit = QtWidgets.QLineEdit(self.upcoming_events_tab)
        elif container == "points_tab":
            self.QLineEdit = QtWidgets.QLineEdit(self.points_tab)
        elif container == "upcoming_events_tab":
            self.QLineEdit = QtWidgets.QLineEdit(self.upcoming_events_tab)
        self.QLineEdit.setObjectName(object_name)

        # Geometry of QLineEdit is specified by the passed function parameters
        self.QLineEdit.setFixedSize(width, length)
        self.QLineEdit.move(x_coordinate, y_coordinate)
        return self.QLineEdit

    def create_QFrame(self, container, object_name, orientation, x_coordinate, y_coordinate, width, length):
        if container == "login_widget_container":
            self.QFrame = QtWidgets.QFrame(self.login_widget_container)
        elif container == "dashboard_widget":
            self.QFrame = QtWidgets.QFrame(self.dashboard_widget)
        self.QFrame.setObjectName(object_name)
        self.QFrame.setGeometry(QtCore.QRect(x_coordinate, y_coordinate, width, length))
        if orientation == "VLine":
            self.QFrame.setFrameShape(QtWidgets.QFrame.VLine)
        else:
            self.QFrame.setFrameShape(QtWidgets.QFrame.HLine)

    def create_QPushButton(self, container, object_name, text, icon, x_coordinate, y_coordinate, width, length):
        # Creates and associates QLabel to specified container
        if container == "login_widget_container":
            self.QPushButton = QtWidgets.QPushButton(self.login_widget_container)
        self.QPushButton.setObjectName(object_name)
        self.QPushButton.setText(text)
        if icon != "None":
            self.QPushButton.setIcon(QIcon(icon))
        # Geometry of QLineEdit is specified by the passed function parameters
        self.QPushButton.setFixedSize(width, length)
        self.QPushButton.move(x_coordinate, y_coordinate)
        return self.QPushButton

class TabBar(QTabBar):
    def tabSizeHint(self, index):
        self.setGeometry(0, 120, 180, 300)
        s = QTabBar.tabSizeHint(self, index)
        s.transpose()
        return s

    def paintEvent(self, event):
        painter = QStylePainter(self)
        opt = QStyleOptionTab()

        for i in range(self.count()):
            self.initStyleOption(opt, i)
            painter.drawControl(QStyle.CE_TabBarTabShape, opt)
            painter.save()

            s = opt.rect.size()
            s.transpose()
            r = QtCore.QRect(QtCore.QPoint(), s)
            r.moveCenter(opt.rect.center())
            opt.rect = r

            c = self.tabRect(i).center()
            painter.translate(c)
            painter.rotate(90)
            painter.translate(-c)
            painter.drawControl(QStyle.CE_TabBarTabLabel, opt)
            painter.restore()

class VerticalTabWidget(QTabWidget):
    def __init__(self, *args, **kwargs):
        QTabWidget.__init__(self, *args, **kwargs)
        self.setTabBar(TabBar())
        self.setTabPosition(QtWidgets.QTabWidget.West)
        self.setStyleSheet("QTabBar::tab { height: 180px; width: 50px;}")


if __name__ == "__main__":
    import sys
    # An application is created
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    # Read the css file and apply the stylesheet
    with open("styling.css", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)
    # A main window is created for the application
    main_window = QtWidgets.QMainWindow()
    # The user interface sets up the main window class
    ui = ui_main_window()
    ui.setup_window(main_window)
    main_window.show()
    sys.exit(app.exec_())