# Import PyQt5's widgets to be used throughout the program
from PyQt5.QtCore import Qt, QDateTime, pyqtSignal, QDate
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
        self.student_username = self.create_QLineEdit("login_widget_container", "login_screen_text_fields", False, 80, 160,
                                                      240, 30)
        self.student_password_label = self.create_QLabel("login_widget_container", "login_screen_labels", "Password",
                                                         80, 187, 200, 50)
        self.student_password = self.create_QLineEdit("login_widget_container", "login_screen_text_fields", False, 80, 225,
                                                      240, 30)
        self.student_forgot_password = self.create_QPushButton("login_widget_container", "login_screen_forgot_password",
                                                               "Forgot password?", "None", 65, 255, 140, 30)
        self.student_login_button = self.create_QPushButton("login_widget_container", "student_login_button", "Login", "None",
                                                            80, 290, 240, 30)
        self.student_login_button.clicked.connect(self.setup_portal)

        # Line divider between logins
        self.login_divider_line = self.create_QFrame("login_widget_container", "login_screen_elements", "VLine", 399,
                                                     40, 1, 410)

        # Administrator Login
        self.administrator_login_title = self.create_QLabel("login_widget_container", "login_titles",
                                                            "Administrator Login",
                                                            525, 80, 200, 50)
        self.administrator_username_label = self.create_QLabel("login_widget_container", "login_screen_labels", "Email ID",
                                                         480, 122, 200, 50)
        self.administrator_username = self.create_QLineEdit("login_widget_container", "login_screen_text_fields", False, 480, 160,
                                                      240, 30)
        self.administrator_password_label = self.create_QLabel("login_widget_container", "login_screen_labels", "Password",
                                                         480, 187, 200, 50)
        self.administrator_password = self.create_QLineEdit("login_widget_container", "login_screen_text_fields", False, 480, 225,
                                                      240, 30)
        self.administrator_forgot_password = self.create_QPushButton("login_widget_container", "login_screen_forgot_password",
                                                               "Forgot password?", "None", 465, 255, 140, 30)
        self.administrator_login_button = self.create_QPushButton("login_widget_container", "administrator_login_button", "Login", "None",
                                                            480, 290, 240, 30)
        self.administrator_login_button.clicked.connect(self.setup_portal)

    def setup_portal(self):
        sending_button = self.login_widget_container.sender().objectName()
        self.login_widget_container.hide()
        self.login_screen_background.clear()

        main_window.setFixedSize(1000, 800)
        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("central_widget")
        self.central_widget.resize(1000, 800)

        self.app_logo = QtWidgets.QLabel(self.central_widget)
        self.app_logo.setFixedSize(140, 140)
        self.app_logo.move(20, 10)
        self.app_logo.setPixmap(
            QtGui.QPixmap("Application Pictures and Icons/Time Track Icon.png"))
        self.app_logo.setScaledContents(True)
        self.app_logo.show()


        if sending_button == "student_login_button":
            self.setup_student_page()
        else:
            self.setup_admin_page()

        main_window.setCentralWidget(self.central_widget)

    def setup_student_page(self):
        self.intro_label = self.create_QLabel("central_widget", "intro_label", "Signed in as Wallace McCarthy",
                                              200, 10, 600, 50)

        self.tab_widget = VerticalTabWidget(self.central_widget)
        self.tab_widget.setObjectName("tab_widget")
        self.tab_widget.resize(1000, 710)
        self.tab_widget.move(0, 55)

        self.dashboard_tab = QtWidgets.QWidget()
        self.upcoming_events_tab = QtWidgets.QWidget()
        self.points_tab = QtWidgets.QWidget()
        self.rewards_tab = QtWidgets.QWidget()
        self.student_profile_tab = QtWidgets.QWidget()

        self.tab_widget.addTab(self.dashboard_tab, "Dashboard")
        self.tab_widget.addTab(self.upcoming_events_tab, "Upcoming Events")
        self.tab_widget.addTab(self.points_tab, "Points")
        self.tab_widget.addTab(self.rewards_tab, "Rewards")
        self.tab_widget.addTab(self.student_profile_tab, "My Student Profile")

        # Dashboard

        # Title
        self.dashboard_label = self.create_QLabel("dashboard_tab", "dashboard_label", "Dashboard",
                                                  20, 20, 600, 50)
        self.dashboard_title_line = self.create_QFrame("dashboard_tab", "dashboard_title_line", "HLine",
                                                       10, 65, 600, 6)
        self.dashboard_announcement_label = self.create_QLabel("dashboard_tab", "dashboard_announcement_label",
                                                               "  Announcements", 20, 80, 560, 30)
        self.dashboard_announcement_objects = self.create_QScrollArea("dashboard_tab",
                                                                         "dashboard_announcements_QScrollArea", 20,
                                                                         110, 560, 340)
        self.dashboard_announcement_events = self.dashboard_announcement_objects[0]
        self.dashboard_announcement_events_layout = self.dashboard_announcement_objects[1]
        self.dashboard_announcement_events_scrollArea = self.dashboard_announcement_objects[2]

        for i in range(6):
            self.event_object = QtWidgets.QGroupBox(self.dashboard_announcement_events)
            self.event_object.setFixedSize(750, 50)
            self.event_object.setLayout(QtWidgets.QVBoxLayout())
            self.label = self.create_QLabel("event", "test", "   Event Name",
                                            0, 0, 100, 30)
            self.dashboard_announcement_events_layout.addWidget(self.event_object)
        self.dashboard_announcement_events_scrollArea.setWidget(self.dashboard_announcement_events)
        self.dashboard_announcement_events_scrollArea.verticalScrollBar().setSliderPosition(0)

        self.dashboard_important_events = self.create_QLineEdit("dashboard_tab", "dashboard_upcoming_events", True,
                                                               600, 110, 200, 340)
        self.dashboard_important_events_label = self.create_QLabel("dashboard_tab",
                                                                  "dashboard_upcoming_events_label",
                                                                  "  Important Events", 600, 80, 200, 30)

        self.dashboard_upcoming_events_objects = self.create_QScrollArea("dashboard_tab", "dashboard_upcoming_events_QScrollArea", 20,
                                                               485, 780, 200)
        self.dashboard_upcoming_events = self.dashboard_upcoming_events_objects[0]
        self.dashboard_upcoming_events_layout = self.dashboard_upcoming_events_objects[1]
        self.dashboard_upcoming_events_scrollArea = self.dashboard_upcoming_events_objects[2]
        self.dashboard_upcoming_events_label = self.create_QLabel("dashboard_tab", "dashboard_important_events_label",
                                                                  "  Upcoming Events", 20, 470, 780, 30)

        for i in range(6):
            self.event_object = QtWidgets.QGroupBox(self.dashboard_upcoming_events)
            self.event_object.setFixedSize(750, 50)
            self.event_object.setLayout(QtWidgets.QVBoxLayout())
            self.label = self.create_QLabel("event", "test", "   Event Name",
                                                   0, 0, 100, 30)
            self.dashboard_upcoming_events_layout.addWidget(self.event_object)
        self.dashboard_upcoming_events_scrollArea.setWidget(self.dashboard_upcoming_events)
        self.dashboard_upcoming_events_scrollArea.verticalScrollBar().setSliderPosition(0)

        # Upcoming Events

        # Title
        self.upcoming_events_label = self.create_QLabel("upcoming_events_tab", "upcoming_events_label",
                                                        "Upcoming Events",
                                                        20, 20, 600, 50)
        self.upcoming_events_title_line = self.create_QFrame("upcoming_events_tab", "upcoming_events_title_line",
                                                             "HLine", 10, 65, 600, 6)

        # Body

        self.student_calendar = self.create_QCalendar("upcoming_events_tab", 20, 80, 350, 350)


        self.student_calendar.selectionChanged.connect(self.student_upcoming_events_calendar)

        self.day_events_label = self.create_QLabel("upcoming_events_tab", "day_events_label", "  Selected Event",
                                                   400, 80, 400, 30)
        self.day_events = self.create_QLineEdit("upcoming_events_tab", "day_events", True, 400, 110, 400, 320)
        current_day = self.student_calendar.selectedDate().toString()
        self.day_events.setText("Events on: " + current_day[4:] + ":")
        self.day_events.setAlignment(Qt.AlignTop)

        self.upcoming_events_objects = self.create_QScrollArea("upcoming_events_tab", "upcoming_events_QScrollArea", 20, 485, 780, 200)
        self.upcoming_events = self.upcoming_events_objects[0]
        self.upcoming_events_layout = self.upcoming_events_objects[1]
        self.upcoming_events_scrollArea = self.upcoming_events_objects[2]
        self.upcoming_events_page_label = self.create_QLabel("upcoming_events_tab", "upcoming_events_page_label",
                                                             "  Upcoming Events", 20, 455, 780, 30)

        # Example of upcoming events
        for i in range(6):
            self.event_object = QtWidgets.QGroupBox(self.upcoming_events)
            self.event_object.setFixedSize(750, 50)
            self.event_object.setLayout(QtWidgets.QVBoxLayout())
            self.label = self.create_QLabel("event", "test", "   Event Name",
                                                   0, 0, 100, 30)
            self.upcoming_events_layout.addWidget(self.event_object)
        self.upcoming_events_scrollArea.setWidget(self.upcoming_events)
        self.upcoming_events_scrollArea.verticalScrollBar().setSliderPosition(0)

        # Points Page

        # Title
        self.points_label = self.create_QLabel("points_tab", "points_label", "Points", 20, 20, 600, 50)
        self.points_title_line = self.create_QFrame("points_tab", "points_title_line",
                                                    "HLine",
                                                    10, 65, 600, 6)

        # Body
        self.personal_points_label = self.create_QLabel("points_tab", "personal_points_label", "  Personal Points", 20,
                                                        80, 300, 30)
        self.personal_points = self.create_QLineEdit("points_tab", "personal_points", True, 20, 110, 300, 300)

        self.points_leaderboard_label = self.create_QLabel("points_tab", "points_leaderboard_label", "  Leaderboard",
                                                           350, 80, 450, 30)
        self.points_leaderboard = self.create_QLineEdit("points_tab", "point_leaderboard", True, 350, 110, 450, 300)

        # Rewards Tab
        # Title

        self.rewards_label = self.create_QLabel("rewards_tab", "rewards_label", "Rewards",
                                                20, 20, 600, 50)
        self.rewards_title_line = self.create_QFrame("rewards_tab", "rewards_title_line", "HLine",
                                                     10, 65, 600, 6)

        # Body
        self.rewards_my_points_label = self.create_QLabel("rewards_tab", "rewards_my_points_label",
                                                             "  Test", 20, 80, 300, 30)
        self.rewards_my_points = self.create_QLineEdit("rewards_tab", "rewards_my_points", True,
                                                          20, 110, 300, 300)

        # Student Profile
        # Title
        self.student_profile_label = self.create_QLabel("student_profile_tab", "student_profile_label",
                                                        "My Profile",
                                                        20, 20, 600, 50)
        self.student_profile_title_line = self.create_QFrame("student_profile_tab", "student_profile_title_line",
                                                             "HLine",
                                                             10, 65, 600, 6)
        # Body
        self.student_profile_data = self.create_QLineEdit("student_profile_tab", "student_profile_data", True,
                                                          20, 110, 300, 300)
        self.student_profile_data_label = self.create_QLabel("student_profile_tab", "student_profile_data_label",
                                                             "  data", 20, 80, 300, 30)
        # Button
        self.student_profile_settings_button = self.create_QPushButton("main_window",
                                                                       "student_profile_settings_button", "Press me",
                                                                       "None", 700, 10, 100, 40)
        self.student_profile_settings_button.clicked.connect(self.admin_events_calendar)

        self.tab_widget.show()

    def setup_admin_page(self):
        self.intro_label = self.create_QLabel("central_widget", "intro_label", "Signed in as Dheeraj Vislawath",
                                              200, 10, 600, 50)

        self.tab_widget = VerticalTabWidget(self.central_widget)
        self.tab_widget.setObjectName("tab_widget")
        self.tab_widget.resize(1000, 650)
        self.tab_widget.move(0, 55)

        # Administrator Login
        self.admin_dashboard_tab = QtWidgets.QWidget()
        self.admin_events_tab = QtWidgets.QWidget()
        self.admin_statistics_tab = QtWidgets.QWidget()
        self.admin_student_view_tab = QtWidgets.QWidget()

        self.tab_widget.addTab(self.admin_dashboard_tab, "Dashboard")
        self.tab_widget.addTab(self.admin_events_tab, "Events")
        self.tab_widget.addTab(self.admin_statistics_tab, "Statistics")
        self.tab_widget.addTab(self.admin_student_view_tab, "Student View")

        self.count = 0

        self.admin_dashboard_label = self.create_QLabel("admin_dashboard_tab", "admin_dashboard_label", "Dashboard", 20,
                                                        20, 600, 50)
        self.admin_dashboard_line = self.create_QFrame("admin_dashboard_tab", "admin_dashboard_line", "HLine", 10, 65, 600, 6)

        self.admin_events_label = self.create_QLabel("admin_events_tab", "admin_events_label", "Events", 20, 20, 600, 50)
        self.admin_events_line = self.create_QFrame("admin_events_tab", "admin_events_line", "HLine", 10, 65, 600, 6)
        self.admin_calendar = self.create_QCalendar("admin_events_tab", 20, 80, 350, 350)
        self.admin_calendar.selectionChanged.connect(self.admin_events_calendar)

        # setting selected date
        # self.admin_calendar.clicked.connect(lambda: self.admin_current_events.setText(text + str(self.count)))
        self.admin_events_title = self.create_QLabel("admin_events_tab", "admin_events_text", "Current Events", 400, 80, 400,
                                                            30)
        self.admin_current_events = self.create_QLineEdit("admin_events_tab", "admin_current_events", True, 400, 110, 400, 320, )
        current_day = self.admin_calendar.selectedDate().toString()
        self.admin_current_events.setText("Events on " + current_day[4:] + ":")
        self.admin_current_events.setAlignment(Qt.AlignTop)

        self.admin_statistics_label = self.create_QLabel("admin_statistics_tab", "admin_statistics_label", "Statistics", 20, 20, 600, 50)
        self.admin_statistics_line = self.create_QFrame("admin_statistics_tab", "admin_statistics_line", "HLine", 10, 65, 600, 6)

        self.admin_student_view_label = self.create_QLabel("admin_student_view_tab", "admin_student_view_label", "Student View", 20, 20,
                                                           600, 50)
        self.admin_student_view_line = self.create_QFrame("admin_student_view_tab", "admin_student_view_line", "HLine", 10, 65, 600, 6)

        self.tab_widget.show()

    def get_count(self):
        self.count += 1
        return self.count

    def admin_events_calendar(self):
        selected_date = self.admin_events_tab.sender().selectedDate().toString()
        self.admin_current_events.setText("Events on " + selected_date[4:] + ":")
        self.admin_current_events.setAlignment(Qt.AlignTop)

    def student_upcoming_events_calendar(self):
        selected_date = self.upcoming_events_tab.sender().selectedDate().toString()
        self.day_events.setText("Events on " + selected_date[4:] + ":")
        self.day_events.setAlignment(Qt.AlignTop)

    def create_QCalendar(self, container, x_coordinate, y_coordinate, width, length):
        if container == "upcoming_events_tab":
            self.QCalender = QtWidgets.QCalendarWidget(self.upcoming_events_tab)
        elif container == "admin_events_tab":
            self.QCalender = QtWidgets.QCalendarWidget(self.admin_events_tab)
        self.QCalender.setGeometry(x_coordinate, y_coordinate, width, length)
        return self.QCalender

    def create_QLabel(self, container, object_name, text, x_coordinate, y_coordinate, width, length,):
        # Creates and associates QLabel to specified container
        if container == "login_widget_container":
            self.QLabel = QtWidgets.QLabel(self.login_widget_container)
        elif container == "central_widget":
            self.QLabel = QtWidgets.QLabel(self.central_widget)
        elif container == "dashboard_tab":
            self.QLabel = QtWidgets.QLabel(self.dashboard_tab)
        elif container == "upcoming_events_tab":
            self.QLabel = QtWidgets.QLabel(self.upcoming_events_tab)
        elif container == "points_tab":
            self.QLabel = QtWidgets.QLabel(self.points_tab)
        elif container == "rewards_tab":
            self.QLabel = QtWidgets.QLabel(self.rewards_tab)
        elif container == "student_profile_tab":
            self.QLabel = QtWidgets.QLabel(self.student_profile_tab)
        elif container == "event":
            self.QLabel = QtWidgets.QLabel(self.event_object)

        #Administrator
        elif container == "admin_dashboard_tab":
            self.QLabel = QtWidgets.QLabel(self.admin_dashboard_tab)
        elif container == "admin_events_tab":
            self.QLabel = QtWidgets.QLabel(self.admin_events_tab)
        elif container == "admin_statistics_tab":
            self.QLabel = QtWidgets.QLabel(self.admin_statistics_tab)
        elif container == "admin_student_view_tab":
            self.QLabel = QtWidgets.QLabel(self.admin_student_view_tab)
        self.QLabel.setObjectName(object_name)
        self.QLabel.setText(text)
        # Geometry of QLabel is specified by the passed function parameters
        self.QLabel.setGeometry(QtCore.QRect(x_coordinate, y_coordinate, width, length))
        return self.QLabel

    def create_QLineEdit(self, container, object_name, read_only, x_coordinate, y_coordinate, width, length):
        # Creates and associates QLabel to specified container
        if container == "login_widget_container":
            self.QLineEdit = QtWidgets.QLineEdit(self.login_widget_container)
        elif container == "dashboard_tab":
            self.QLineEdit = QtWidgets.QLineEdit(self.dashboard_tab)
        elif container == "admin_dashboard_tab":
            self.QLineEdit = QtWidgets.QLineEdit(self.admin_dashboard_tab)
        elif container == "upcoming_events_tab":
            self.QLineEdit = QtWidgets.QLineEdit(self.upcoming_events_tab)
        elif container == "points_tab":
            self.QLineEdit = QtWidgets.QLineEdit(self.points_tab)
        elif container == "rewards_tab":
            self.QLineEdit = QtWidgets.QLineEdit(self.rewards_tab)
        elif container == "student_profile_tab":
            self.QLineEdit = QtWidgets.QLineEdit(self.student_profile_tab)

            # Administrator
        elif container == "admin_dashboard_tab":
            self.QLineEdit = QtWidgets.QLineEdit(self.admin_dashboard_tab)
        elif container == "admin_events_tab":
            self.QLineEdit = QtWidgets.QLineEdit(self.admin_events_tab)
        elif container == "admin_statistics_tab":
            self.QLineEdit = QtWidgets.QLineEdit(self.admin_statistics_tab)
        elif container == "admin_student_view_tab":
            self.QLineEdit = QtWidgets.QLineEdit(self.admin_student_view_tab)
        self.QLineEdit.setObjectName(object_name)
        # user cannot type in the boxes
        self.QLineEdit.setReadOnly(read_only)
        # Geometry of QLineEdit is specified by the passed function parameters
        self.QLineEdit.setFixedSize(width, length)
        self.QLineEdit.move(x_coordinate, y_coordinate)
        return self.QLineEdit

    def create_QScrollArea(self, container, object_name, x_coordinate, y_coordinate, fixed_width, min_length):
        self.scrollArea_object_container = QtWidgets.QWidget()
        if container == "upcoming_events_tab":
            self.QScrollArea = QtWidgets.QScrollArea(self.upcoming_events_tab)
        elif container == "dashboard_tab":
            self.QScrollArea = QtWidgets.QScrollArea(self.dashboard_tab)
        self.QScrollArea.setFixedWidth(fixed_width)
        self.QScrollArea.setFixedHeight(min_length)
        self.QScrollArea.move(x_coordinate, y_coordinate)
        self.QScrollArea.setWidgetResizable(True)
        self.QScrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_vertical_layout = QtWidgets.QVBoxLayout(self.scrollArea_object_container)
        self.scrollArea_object_container.setLayout(self.scroll_vertical_layout)
        return [self.scrollArea_object_container, self.scroll_vertical_layout, self.QScrollArea]

    def create_QFrame(self, container, object_name, orientation, x_coordinate, y_coordinate, width, length):
        if container == "login_widget_container":
            self.QFrame = QtWidgets.QFrame(self.login_widget_container)
        elif container == "dashboard_tab":
            self.QFrame = QtWidgets.QFrame(self.dashboard_tab)
        elif container == "admin_dashboard_tab":
            self.QFrame = QtWidgets.QFrame(self.admin_dashboard_tab)
        elif container == "upcoming_events_tab":
            self.QFrame = QtWidgets.QFrame(self.upcoming_events_tab)
        elif container == "points_tab":
            self.QFrame = QtWidgets.QFrame(self.points_tab)
        elif container == "rewards_tab":
            self.QFrame = QtWidgets.QFrame(self.rewards_tab)
        elif container == "student_profile_tab":
            self.QFrame = QtWidgets.QFrame(self.student_profile_tab)
            # Administrator
        elif container == "admin_dashboard_tab":
            self.QFrame = QtWidgets.QFrame(self.admin_dashboard_tab)
        elif container == "admin_events_tab":
            self.QFrame = QtWidgets.QFrame(self.admin_events_tab)
        elif container == "admin_statistics_tab":
            self.QFrame = QtWidgets.QFrame(self.admin_statistics_tab)
        elif container == "admin_student_view_tab":
            self.QFrame = QtWidgets.QFrame(self.admin_student_view_tab)
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
        elif container == "main_window":
            self.QPushButton = QtWidgets.QPushButton(main_window)
        elif container == "student_profile_tab":
            self.QPushButton = QtWidgets.QPushButton(self.student_profile_tab)
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