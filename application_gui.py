# Import PyQt5's widgets to be used throughout the program
import threading

from PyQt5.QtCore import Qt, pyqtSignal, QDate, QRunnable, pyqtSlot, QThreadPool
from PyQt5.QtGui import QIcon, QPixmap, QTextCursor
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from datetime import time

# folium v0.12.1 - Used to display geographical data
import folium
import time
import io
import os
import sqlite3

sqliteConnection = sqlite3.connect('identifier.sqlite')
cursor = sqliteConnection.cursor()
sqlite_select_query = """SELECT * from events"""
cursor.execute(sqlite_select_query)
events = cursor.fetchall()
for event in events:
    print(event)
cursor.close()

# A class is created that holds all functions of the program
class ui_main_window(object):
    # Window Setup Functions
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
        self.student_login_title = self.create_QLabel("login_widget_container", "login_titles", "Student Login", 145, 80, 200, 50)
        self.student_username_label = self.create_QLabel("login_widget_container", "login_screen_labels", "Email ID", 80, 122, 200, 50)
        self.student_username = self.create_QLineEdit("login_widget_container", "login_screen_text_fields", False, 80, 160, 240, 30)
        self.student_password_label = self.create_QLabel("login_widget_container", "login_screen_labels", "Password", 80, 187, 200, 50)
        self.student_password = self.create_QLineEdit("login_widget_container", "login_screen_text_fields", False, 80, 225, 240, 30)
        self.student_forgot_password = self.create_QPushButton("login_widget_container", "login_screen_forgot_password", "Forgot password?", "None", 65, 255, 140, 30)
        self.student_incorrect_login = self.create_QLabel("login_widget_container", "incorrect_login", "Email ID and/or Password Icorrect. Please enter correct credentials.", 82, 275, 240, 50)
        self.student_incorrect_login.setWordWrap(True)
        self.student_incorrect_login.hide()
        self.student_login_button = self.create_QPushButton("login_widget_container", "student_login_button", "Login", "None", 80, 290, 240, 30)
        self.student_login_button.clicked.connect(self.setup_portal)
        self.student_or_label = self.create_QLabel("login_widget_container", "login_screen_labels", "or", 190, 310, 40, 50)
        self.student_create_account = self.create_QPushButton("login_widget_container", "student_login_button", "Create a Student Account", "None", 80, 350, 240, 30)

        # Line divider between logins
        self.login_divider_line = self.create_QFrame("login_widget_container", "login_screen_elements", "VLine", 399, 40, 1, 410)

        # Administrator Login
        self.administrator_login_title = self.create_QLabel("login_widget_container", "login_titles", "Administrator Login", 525, 80, 200, 50)
        self.administrator_username_label = self.create_QLabel("login_widget_container", "login_screen_labels", "Email ID", 480, 122, 200, 50)
        self.administrator_username = self.create_QLineEdit("login_widget_container", "login_screen_text_fields", False, 480, 160, 240, 30)
        self.administrator_password_label = self.create_QLabel("login_widget_container", "login_screen_labels", "Password", 480, 187, 200, 50)
        self.administrator_password = self.create_QLineEdit("login_widget_container", "login_screen_text_fields", False, 480, 225, 240, 30)
        self.administrator_forgot_password = self.create_QPushButton("login_widget_container", "login_screen_forgot_password", "Forgot password?", "None", 465, 255, 140, 30)
        self.administrator_incorrect_login = self.create_QLabel("login_widget_container", "incorrect_login", "Email ID and/or Password Icorrect. Please enter correct credentials.", 482, 275, 240, 50)
        self.administrator_incorrect_login.setWordWrap(True)
        self.administrator_incorrect_login.hide()
        self.administrator_login_button = self.create_QPushButton("login_widget_container", "administrator_login_button", "Login", "None", 480, 290, 240, 30)
        self.administrator_login_button.clicked.connect(self.setup_portal)
        self.administrator_or_label = self.create_QLabel("login_widget_container", "login_screen_labels", "or", 590, 310, 40, 50)
        self.administrator_create_account = self.create_QPushButton("login_widget_container", "administrator_login_button", "Create an Administrator Account", "None", 480, 350, 240, 30)

    def setup_portal(self):
        sending_button = self.login_widget_container.sender().objectName()
        if sending_button == "student_login_button":
            sqliteConnection = sqlite3.connect('identifier.sqlite')
            cursor = sqliteConnection.cursor()

            cursor.execute("SELECT EMAIL_ADDRESS, PASSWORD FROM students")
            student_rows = cursor.fetchall()
            cursor.close()

            for user in student_rows:
                if self.student_username.text() == user[0] and self.student_password.text() == user[1]:
                    self.login_central_widget.deleteLater()

                    main_window.setFixedSize(1400, 800)
                    self.central_widget = QtWidgets.QWidget(main_window)
                    self.central_widget.setObjectName("central_widget")
                    self.central_widget.resize(1400, 800)

                    self.app_logo = QtWidgets.QLabel(self.central_widget)
                    self.app_logo.setFixedSize(140, 140)
                    self.app_logo.move(20, 10)
                    self.app_logo.setPixmap(QtGui.QPixmap("Application Pictures and Icons/Time Track Icon.png"))
                    self.app_logo.setScaledContents(True)
                    self.app_logo.show()

                    self.log_out_button = self.create_QPushButton("central_widget", "log_out", "None", "Application Pictures and Icons/Log Out.png", 1240, -50, 160, 160)
                    self.log_out_button.setIconSize(QtCore.QSize(150, 150))
                    self.log_out_button.setFlat(True)
                    self.log_out_button.clicked.connect(self.return_to_login_screen)

                    self.setup_student_page()
                    main_window.setCentralWidget(self.central_widget)
                    break
            self.student_login_button.move(80, 320)
            self.student_or_label.move(190, 340)
            self.student_create_account.move(80, 380)
            self.student_incorrect_login.show()


        elif sending_button == "administrator_login_button":
            sqliteConnection = sqlite3.connect('identifier.sqlite')
            cursor = sqliteConnection.cursor()

            cursor.execute("SELECT EMAIL_ADDRESS, PASSWORD FROM administrators")
            admin_rows = cursor.fetchall()
            cursor.close()

            for user in admin_rows:
                if self.student_username.text() == user[0][0] and self.student_password.text() == user[0][1]:
                    self.login_central_widget.deleteLater()

                    main_window.setFixedSize(1400, 800)
                    self.central_widget = QtWidgets.QWidget(main_window)
                    self.central_widget.setObjectName("central_widget")
                    self.central_widget.resize(1400, 800)

                    self.app_logo = QtWidgets.QLabel(self.central_widget)
                    self.app_logo.setFixedSize(140, 140)
                    self.app_logo.move(20, 10)
                    self.app_logo.setPixmap(QtGui.QPixmap("Application Pictures and Icons/Time Track Icon.png"))
                    self.app_logo.setScaledContents(True)
                    self.app_logo.show()

                    self.log_out_button = self.create_QPushButton("central_widget", "log_out", "None", "Application Pictures and Icons/Log Out.png", 1240, -50, 160, 160)
                    self.log_out_button.setIconSize(QtCore.QSize(150, 150))
                    self.log_out_button.setFlat(True)
                    self.log_out_button.clicked.connect(self.return_to_login_screen)

                    self.setup_student_page()
                    main_window.setCentralWidget(self.central_widget)
                    break
            self.administrator_login_button.move(480, 320)
            self.administrator_or_label.move(590, 340)
            self.administrator_create_account.move(480, 380)
            self.administrator_incorrect_login.show()

    def setup_student_page(self):
        global dashboard_slideshow
        global slideshow_title
        global slideshow_description
        global kill_thread_boolean
        global threadpool

        self.tab_widget = VerticalTabWidget(self.central_widget)
        self.tab_widget.setObjectName("tab_widget")
        self.tab_widget.resize(1400, 710)
        self.tab_widget.move(0, 55)

        self.dashboard_tab = QtWidgets.QWidget()
        self.upcoming_events_tab = QtWidgets.QWidget()
        self.maps_tab = QtWidgets.QWidget()
        self.points_tab = QtWidgets.QWidget()
        self.rewards_tab = QtWidgets.QWidget()
        self.student_profile_tab = QtWidgets.QWidget()

        self.tab_widget.addTab(self.dashboard_tab, "Dashboard")
        self.tab_widget.addTab(self.upcoming_events_tab, "Upcoming Events")
        self.tab_widget.addTab(self.maps_tab, "Maps")
        self.tab_widget.addTab(self.points_tab, "Points")
        self.tab_widget.addTab(self.rewards_tab, "Rewards")
        self.tab_widget.addTab(self.student_profile_tab, "My Student Profile")

        # Dashboard Tab
        self.intro_label = self.create_QLabel("central_widget", "intro_label", "Signed in as Wallace McCarthy", 200, 10, 600, 50)
        self.dashboard_label = self.create_QLabel("dashboard_tab", "dashboard_label", "Dashboard", 20, 20, 600, 50)
        self.dashboard_title_line = self.create_QFrame("dashboard_tab", "dashboard_title_line", "HLine", 10, 65, 600, 6)
        dashboard_slideshow = self.create_QLabel("dashboard_tab", "dashboard_slider_label", "filler", 20, 90, 840, 480)
        dashboard_slideshow.setScaledContents(True)
        slideshow_title = self.create_QLabel("dashboard_tab", "slideshow_title", "", 20, 580, 840, 20)
        slideshow_title.setWordWrap(True)
        slideshow_description = self.create_QLabel("dashboard_tab", "slideshow_description", "", 20, 600, 840, 100)
        slideshow_description.setWordWrap(True)
        slideshow_description.setAlignment(QtCore.Qt.AlignTop)
        kill_thread_boolean = False
        threadpool = QThreadPool()
        slideshow = Slideshow()
        threadpool.start(slideshow)
        self.dashboard_separator_line = self.create_QFrame("dashboard_tab", "dashboard_separator_line", "VLine", 875, 40, 6, 630)

        # Upcoming Events Tab
        self.upcoming_events_label = self.create_QLabel("upcoming_events_tab", "upcoming_events_label", "Upcoming Events", 20, 20, 600, 50)
        self.upcoming_events_title_line = self.create_QFrame("upcoming_events_tab", "upcoming_events_title_line", "HLine", 10, 65, 600, 6)
        self.student_calendar = self.create_QCalendar("upcoming_events_tab", 20, 80, 350, 350)
        self.student_calendar.selectionChanged.connect(self.student_upcoming_events_calendar)
        self.day_events_label = self.create_QLabel("upcoming_events_tab", "day_events_label", "  Selected Event", 400, 80, 400, 30)
        self.day_events = self.create_QTextEdit("upcoming_events_tab", "day_events", True, 400, 110, 400, 320)
        current_day = self.student_calendar.selectedDate().toString()
        self.day_events_label.setText("Events on: " + current_day[4:] + ":")
        self.day_events.setAlignment(Qt.AlignTop)

        self.upcoming_events_objects = self.create_QScrollArea("upcoming_events_tab", "upcoming_events_QScrollArea", "vertical_layout", 20, 485, 780, 200)
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
            self.check_box = self.create_QCheckBox("event", 725, 12, 30, 30)
            self.upcoming_events_layout.addWidget(self.event_object)
        self.upcoming_events_scrollArea.setWidget(self.upcoming_events)
        self.upcoming_events_scrollArea.verticalScrollBar().setSliderPosition(0)

        # Maps Tab
        self.maps_label = self.create_QLabel("maps_tab", "maps_label", "Maps", 20, 20, 600, 50)
        self.maps_line = self.create_QFrame("maps_tab", "maps_line", "HLine", 10, 65, 600, 6)
        self.map_container = QtWidgets.QGroupBox(self.maps_tab)
        self.map_container.setGeometry(QtCore.QRect(20, 80, 800, 600))
        # self.map_container.setEnabled(True)
        # self.map_container.setFlat(True)
        self.maps_objects = self.create_QScrollArea("maps_tab", "maps_QScrollArea", "vertical_layout", 850, 85, 350, 600)
        self.maps = self.maps_objects[0]
        self.maps_layout = self.maps_objects[1]
        self.maps_scrollArea = self.maps_objects[2]

        # The created QGroupBox container's layout is set to hold the web widget
        self.map_frame = QtWidgets.QVBoxLayout(self.map_container)
        coordinate = (40.617847198627, -111.86923371648)
        global map
        map = folium.Map(zoom_start=15, location=coordinate)

        folium.Marker(
            location=coordinate,
            icon=folium.Icon(color="darkgreen", icon='user'),
        ).add_to(map)

        self.show_event_locations("student")
        # Save map data to data object
        data = io.BytesIO()
        map.save(data, close_file=False)
        webView = QWebEngineView()
        # Sets the web widget to the map data
        webView.setHtml(data.getvalue().decode())
        # Adds the map data to the QGroupBox layout
        self.map_frame.addWidget(webView)

        self.maps_scrollArea.setWidget(self.maps)
        self.maps_scrollArea.verticalScrollBar().setSliderPosition(0)

        # Points Tab
        self.points_label = self.create_QLabel("points_tab", "points_label", "Points", 20, 20, 600, 50)
        self.points_title_line = self.create_QFrame("points_tab", "points_title_line", "HLine", 10, 65, 600, 6)
        self.personal_points_label = self.create_QLabel("points_tab", "personal_points_label", "  Personal Points", 20, 80, 300, 30)
        self.personal_points = self.create_QLineEdit("points_tab", "personal_points", True, 20, 110, 300, 300)
        self.points_leaderboard_label = self.create_QLabel("points_tab", "points_leaderboard_label", "  Leaderboard", 350, 80, 450, 30)
        self.points_leaderboard = self.create_QLineEdit("points_tab", "point_leaderboard", True, 350, 110, 450, 300)

        # Rewards Tab
        self.rewards_label = self.create_QLabel("rewards_tab", "rewards_label", "Rewards", 20, 20, 600, 50)
        self.rewards_title_line = self.create_QFrame("rewards_tab", "rewards_title_line", "HLine", 10, 65, 600, 6)
        self.rewards_my_points_label = self.create_QLabel("rewards_tab", "rewards_my_points_label", "  Your Points", 20, 80, 300, 30)
        self.rewards_my_points = self.create_QLineEdit("rewards_tab", "rewards_my_points", True, 50, 110, 100, 25)
        self.rewards_tab_objects = self.create_QScrollArea("rewards_tab", "rewards_QScrollArea", "grid_layout", 20, 150, 1180, 540)
        self.rewards = self.rewards_tab_objects[0]
        self.rewards_layout = self.rewards_tab_objects[1]
        self.rewards_events_scrollArea = self.rewards_tab_objects[2]

        for i in range(4):
            for j in range(3):
                self.event_object = QtWidgets.QGroupBox(self.rewards)
                self.event_object.setFixedSize(367, 350)
                self.event_object.setLayout(QtWidgets.QGridLayout())
                self.label = self.create_QLabel("event", "test", "   Event Name",0, 0, 100, 30)
                self.check_box = self.create_QCheckBox("event", 305, 12, 30, 30)
                self.rewards_layout.addWidget(self.event_object, i, j)
        self.rewards_events_scrollArea.setWidget(self.rewards)
        self.rewards_events_scrollArea.verticalScrollBar().setSliderPosition(0)

        # Profile Tab
        self.student_profile_label = self.create_QLabel("student_profile_tab", "student_profile_label", "My Profile", 20, 20, 600, 50)
        self.student_profile_title_line = self.create_QFrame("student_profile_tab", "student_profile_title_line", "HLine", 10, 65, 600, 6)
        self.student_profile_data = self.create_QLineEdit("student_profile_tab", "student_profile_data", True,20, 110, 300, 300)
        self.student_profile_data_label = self.create_QLabel("student_profile_tab", "student_profile_data_label", "  data", 20, 80, 300, 30)
        self.student_profile_settings_button = self.create_QPushButton("main_window", "student_profile_settings_button", "Press me", "None", 700, 10, 100, 40)
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

    def student_upcoming_events_calendar(self):
        selected_date = self.upcoming_events_tab.sender().selectedDate().toString()
        new_date = selected_date.split()
        self.check_events_on_day()
        # self.day_events.setText("Events on " + selected_date[4:] + ":")
        # self.day_events.setAlignment(Qt.AlignTop)

    def admin_events_calendar(self):
        selected_date = self.admin_events_tab.sender().selectedDate().toString()
        new_date = selected_date.split()
        self.admin_current_events.setText("Events on " + selected_date[4:] + ":")
        self.admin_current_events.setAlignment(Qt.AlignTop)
        event_year = new_date[3]
        event_month = new_date[1]
        event_day = new_date[2]
        new_month = 1
        if event_month == "Jan":
            new_month = 1
        elif event_month == "Feb":
            new_month = 2
        elif event_month == "Mar":
            new_month = 3
        elif event_month == "Apr":
            new_month = 4
        elif event_month == "May":
            new_month = 5
        elif event_month == "Jun":
            new_month = 6
        elif event_month == "Jul":
            new_month = 7
        elif event_month == "Aug":
            new_month = 8
        elif event_month == "Sep":
            new_month = 9
        elif event_month == "Oct":
            new_month = 10
        elif event_month == "Nov":
            new_month = 11
        elif event_month == "Dec":
            new_month = 12
        for event in events:
            events_day = event[8]
            events_month = event[7]
            events_year = event[6]
            if str(event_year) == str(events_year):
                if str(new_month) == str(events_month):
                    if str(event_day) == str(events_day):
                        self.admin_current_events.setText("Events on " + selected_date[4:] + ": " + event[2])

    # Logic Functions
    # def check_if_user_exists(self):

    def return_to_login_screen(self):
        global kill_thread_boolean
        kill_thread_boolean = True
        self.central_widget.deleteLater()
        main_window.setFixedSize(800, 500)
        self.setup_login_screen(main_window)
        main_window.setCentralWidget(self.login_central_widget)

    def show_event_locations(self, user):
        if user == "student":
            for event in events:
                event_coordinate = (event[9], event[10])
                folium.Marker(location=event_coordinate,
                              icon=folium.Icon(color="red", icon='circle', prefix='fa'),
                              popup=(folium.Popup(f'<h6><b>{event[1]}</b></h6>' + "\n" + f'<h6><b>{event[2]}</b></h6>', show=True, min_width=20)),).add_to(map)
                self.event_object = QtWidgets.QGroupBox(self.maps)
                self.event_object.setFixedSize(250, 100)
                self.event_object.setLayout(QtWidgets.QVBoxLayout())
                self.label = self.create_QLabel("event", str(event[0]), ("   " + event[1] + ", " + event[2]), 0, 0, 250, 70)
                self.label.setWordWrap(True)
                self.maps_layout.addWidget(self.event_object)

    def check_events_on_day(self):
        selected_date = self.upcoming_events_tab.sender().selectedDate().toString()
        numerical_data_list = selected_date.split()
        numerical_data_list[2] = int(numerical_data_list[2])
        numerical_data_list[3] = int(numerical_data_list[3])

        if numerical_data_list[1] == "Jan":
            numerical_data_list[1] = 1
        elif numerical_data_list[1] == "Feb":
            numerical_data_list[1] = 2
        elif numerical_data_list[1] == "Mar":
            numerical_data_list[1] = 3
        elif numerical_data_list[1] == "Apr":
            numerical_data_list[1] = 4
        elif numerical_data_list[1] == "May":
            numerical_data_list[1] = 5
        elif numerical_data_list[1] == "Jun":
            numerical_data_list[1] = 6
        elif numerical_data_list[1] == "Jul":
            numerical_data_list[1] = 7
        elif numerical_data_list[1] == "Aug":
            numerical_data_list[1] = 8
        elif numerical_data_list[1] == "Sep":
            numerical_data_list[1] = 9
        elif numerical_data_list[1] == "Oct":
            numerical_data_list[1] = 10
        elif numerical_data_list[1] == "Nov":
            numerical_data_list[1] = 11
        elif numerical_data_list[1] == "Dec":
            numerical_data_list[1] = 12
        self.day_events.clear()
        current_text = self.day_events.toPlainText()
        for event in events:
            if ((event[7] == numerical_data_list[1]) and (event[8] == numerical_data_list[2]) and (event[6] == numerical_data_list[3])):
                self.day_events.clear()
                self.day_events.setText(current_text + "\n" + "Event: " + event[2] + "\n" + "Address: " + event[3] + "\n"
                                        +  "Type: " + event[4] + "\n" + "Points: " + str(event[5]) + "\n" + "Coordinates: " + str(event[9]) + ", " + str(event[10]))

                # self.day_events_picture = self.create_QLabel("upcoming_events_tab", "day_events_picture", "",
                #                                              400, 210, 300, 320)
                # self.day_events_picture.setPixmap(QPixmap(picture))
                picture = event[11]
                document = self.day_events.document()
                cursor = QTextCursor(document)
                cursor.insertImage(picture)

    # Widget Creation Functions
    def create_QCheckBox(self, container, x_coordinate, y_coordinate, width, length):
        if container == "dashboard_tab":
            self.QCheckBox = QtWidgets.QCheckBox(self.dashboard_tab)
        elif container == "upcoming_events_tab":
            self.QCheckBox = QtWidgets.QCheckBox(self.upcoming_events_tab)
        elif container == "event":
            self.QCheckBox = QtWidgets.QCheckBox(self.event_object)
        self.QCheckBox.resize(width, length)
        self.QCheckBox.move(x_coordinate, y_coordinate)
        return QCheckBox

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
        elif container == "maps_tab":
            self.QLabel = QtWidgets.QLabel(self.maps_tab)
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
        elif container == "maps_tab":
            self.QLineEdit = QtWidgets.QLineEdit(self.maps_tab)
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

    def create_QTextEdit(self, container, object_name, read_only, x_coordinate, y_coordinate, width, length):
        # Creates and associates QLabel to specified container
        if container == "login_widget_container":
            self.QTextEdit = QtWidgets.QTextEdit(self.login_widget_container)
        elif container == "dashboard_tab":
            self.QTextEdit = QtWidgets.QTextEdit(self.dashboard_tab)
        elif container == "admin_dashboard_tab":
            self.QTextEdit = QtWidgets.QTextEdit(self.admin_dashboard_tab)
        elif container == "upcoming_events_tab":
            self.QTextEdit = QtWidgets.QTextEdit(self.upcoming_events_tab)
        elif container == "points_tab":
            self.QTextEdit = QtWidgets.QTextEdit(self.points_tab)
        elif container == "rewards_tab":
            self.QTextEdit = QtWidgets.QTextEdit(self.rewards_tab)
        elif container == "student_profile_tab":
            self.QTextEdit = QtWidgets.QTextEdit(self.student_profile_tab)

            # Administrator
        elif container == "admin_dashboard_tab":
            self.QTextEdit = QtWidgets.QTextEdit(self.admin_dashboard_tab)
        elif container == "admin_events_tab":
            self.QTextEdit = QtWidgets.QTextEdit(self.admin_events_tab)
        elif container == "maps_tab":
            self.QTextEdit = QtWidgets.QTextEdit(self.maps_tab)
        elif container == "admin_statistics_tab":
            self.QTextEdit = QtWidgets.QTextEdit(self.admin_statistics_tab)
        elif container == "admin_student_view_tab":
            self.QTextEdit = QtWidgets.QTextEdit(self.admin_student_view_tab)
        self.QTextEdit.setObjectName(object_name)
        # user cannot type in the boxes
        self.QTextEdit.setReadOnly(read_only)
        # Geometry of QLineEdit is specified by the passed function parameters
        self.QTextEdit.setFixedSize(width, length)
        self.QTextEdit.move(x_coordinate, y_coordinate)
        self.QTextEdit.setWordWrapMode(True)

        return self.QTextEdit

    def create_QScrollArea(self, container, object_name, layout, x_coordinate, y_coordinate, fixed_width, min_length):
        self.scrollArea_object_container = QtWidgets.QWidget()
        if container == "upcoming_events_tab":
            self.QScrollArea = QtWidgets.QScrollArea(self.upcoming_events_tab)
        elif container == "dashboard_tab":
            self.QScrollArea = QtWidgets.QScrollArea(self.dashboard_tab)
        elif container == "maps_tab":
            self.QScrollArea = QtWidgets.QScrollArea(self.maps_tab)
        elif container == "rewards_tab":
            self.QScrollArea = QtWidgets.QScrollArea(self.rewards_tab)
        self.QScrollArea.setFixedWidth(fixed_width)
        self.QScrollArea.setFixedHeight(min_length)
        self.QScrollArea.move(x_coordinate, y_coordinate)
        self.QScrollArea.setWidgetResizable(True)
        self.QScrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        if layout == "vertical_layout":
            self.scroll_vertical_layout = QtWidgets.QVBoxLayout(self.scrollArea_object_container)
            self.scrollArea_object_container.setLayout(self.scroll_vertical_layout)
            return [self.scrollArea_object_container, self.scroll_vertical_layout, self.QScrollArea]
        elif layout == "grid_layout":
            self.scroll_grid_layout = QtWidgets.QGridLayout(self.scrollArea_object_container)
            self.scrollArea_object_container.setLayout(self.scroll_grid_layout)
            self.QScrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
            return [self.scrollArea_object_container, self.scroll_grid_layout, self.QScrollArea]

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
        elif container == "maps_tab":
            self.QFrame = QtWidgets.QFrame(self.maps_tab)
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
        elif container == "central_widget":
            self.QPushButton = QtWidgets.QPushButton(self.central_widget)
        elif container == "main_window":
            self.QPushButton = QtWidgets.QPushButton(main_window)
        elif container == "student_profile_tab":
            self.QPushButton = QtWidgets.QPushButton(self.student_profile_tab)

        elif container == "rewards_tab":
            self.QPushButton = QtWidgets.QPushButton(self.rewards_tab)
        self.QPushButton.setObjectName(object_name)
        if text != "None":
            self.QPushButton.setText(text)
        if icon != "None":
            self.QPushButton.setIcon(QIcon(icon))
        # Geometry of QLineEdit is specified by the passed function parameters
        self.QPushButton.setFixedSize(width, length)
        self.QPushButton.move(x_coordinate, y_coordinate)
        return self.QPushButton

    def create_horizontal_QSlider(self, container, x_coordinate, y_coordinate, width, length):
        if container == "dashboard_tab":
            self.QSlider = QtWidgets.QSlider(Qt.Horizontal, self.dashboard_tab)
        self.QSlider.setGeometry(x_coordinate, y_coordinate, width, length)
        return self.QSlider

# A custom-built widget that creates a slideshow
class Slideshow(QRunnable):
    @pyqtSlot()
    def run(self) -> None:
        sqliteConnection = sqlite3.connect('identifier.sqlite')
        cursor = sqliteConnection.cursor()

        dir_path = r'Announcement Pictures'
        picture_list = []

        for path in os.listdir(dir_path):
            if os.path.isfile(os.path.join(dir_path, path)):
                picture_list.append(path)

        index = 0
        while True:
            dashboard_slideshow.setPixmap(QPixmap("Announcement Pictures/" + picture_list[index]))
            rowidnum = picture_list[index][0:1]
            cursor.execute("SELECT rowid, * FROM slideshow WHERE id = " + rowidnum)
            row = cursor.fetchall()

            slideshow_title.setText(row[0][2])
            slideshow_description.setText(row[0][3])
            time.sleep(3)
            index += 1
            if index == len(picture_list):
                index = 0
            if kill_thread_boolean == True:
                break
        cursor.close()

class TabBar(QTabBar):
    def tabSizeHint(self, index):
        self.setGeometry(0, 120, 180, 380)
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
    with open("styling.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)
    # A main window is created for the application
    main_window = QtWidgets.QMainWindow()
    # The user interface sets up the main window class
    ui = ui_main_window()
    ui.setup_window(main_window)
    main_window.show()
    sys.exit(app.exec_())