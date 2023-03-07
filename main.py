# Import PyQt5's widgets to be used throughout the program
import io
import os
import sqlite3
from datetime import time
import time

# folium v0.12.1 - Used to display geographical data
import folium
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt, QRunnable, pyqtSlot, QThreadPool
from PyQt5.QtGui import QIcon, QPixmap, QTextCursor, QFont
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import *
from folium.plugins import MarkerCluster

# import class functions
import create_widget_functions
import user_details
from create_widget_functions import VerticalTabWidget

sqliteConnection = sqlite3.connect('identifier.sqlite')
cursor = sqliteConnection.cursor()
sqlite_select_query = """SELECT * from events"""
cursor.execute(sqlite_select_query)
events = cursor.fetchall()

cursor.execute("SELECT * from students")
students = cursor.fetchall()

cursor.execute("SELECT email_address, first_name, last_name, points, RANK() OVER(ORDER BY points DESC) 'Rank' from students")
students_leaderboard = cursor.fetchall()

cursor.execute("SELECT FIRST_NAME, LAST_NAME, POINTS FROM students")
student_rows = cursor.fetchall()

cursor.execute("SELECT FIRST_NAME, LAST_NAME, POINTS, EVENT, RATING, DESCRIPTION FROM approval")
admin_approval_rows = cursor.fetchall()

first_name = ""
last_name = ""

def sort_key(student_rows):
    return student_rows[2]

student_rows.sort(key=sort_key, reverse=True)
cursor.close()

event_combobox_selection = ""
rating_combobox_selection = ""
description_box = ""

name_annoucement_text_stuff = ""
details_annoucement_text_stuff = ""




class Main(object):
    def setup_window(self, main_window):
        main_window.setWindowTitle("Time Track")
        main_window.setObjectName("main_window")
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
        self.login_screen_logo.setPixmap(QtGui.QPixmap("Application Pictures and Icons/Time Track Logo.png"))
        self.login_screen_logo.setScaledContents(True)
        self.login_screen_logo.show()

        # Student Login
        self.student_login_title = self.create_QLabel("login_widget_container", "login_titles", "Student Login", 145,80, 200, 50)
        self.student_username_label = self.create_QLabel("login_widget_container", "login_screen_labels", "Email ID", 80, 122, 200, 50)
        self.student_username = self.create_QLineEdit("login_widget_container", "login_screen_text_fields", False, 80,160, 240, 30)
        self.student_password_label = self.create_QLabel("login_widget_container", "login_screen_labels", "Password",80, 187, 200, 50)
        self.student_password = self.create_QLineEdit("login_widget_container", "login_screen_text_fields", False, 80,225, 240, 30)

        self.student_forgot_password = self.create_QPushButton("login_widget_container", "login_screen_forgot_password","Forgot password?", "None", 65, 255, 140, 30)
        self.student_incorrect_login = self.create_QLabel("login_widget_container", "incorrect_login", "Email ID and/or Password Icorrect. Please enter correct credentials.", 82, 275, 240, 50)
        self.student_incorrect_login.setWordWrap(True)
        self.student_incorrect_login.hide()
        self.student_login_button = self.create_QPushButton("login_widget_container", "student_login_button", "Login", "None", 80, 290, 240, 30)
        self.student_login_button.clicked.connect(self.setup_portal)
        self.student_or_label = self.create_QLabel("login_widget_container", "login_screen_labels", "or", 190, 310, 40,50)
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
        main_window.setStatusBar(None)

    def setup_portal(self):
        global username
        global password
        global user

        sending_button = self.login_widget_container.sender().objectName()

        if sending_button == "student_login_button":
            sqliteConnection = sqlite3.connect('identifier.sqlite')
            cursor = sqliteConnection.cursor()

            cursor.execute("SELECT EMAIL_ADDRESS, PASSWORD, FIRST_NAME, LAST_NAME FROM students")
            student_rows = cursor.fetchall()
            cursor.close()

            for user in student_rows:
                if self.student_username.text() == user[0] and self.student_password.text() == user[1]:
                    self.initialize_student_page()
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
                if self.administrator_username.text() == user[0] and self.administrator_password.text() == user[1]:
                    self.initialize_administrator_page()
                    break
            self.administrator_login_button.move(480, 320)
            self.administrator_or_label.move(590, 340)
            self.administrator_create_account.move(480, 380)
            self.administrator_incorrect_login.show()

    def initialize_student_page(self):
        self.login_central_widget.deleteLater()

        main_window.setFixedSize(1400, 800)
        qtRectangle = main_window.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        main_window.move(qtRectangle.topLeft())
        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("central_widget")
        self.central_widget.resize(1400, 800)

        self.app_logo = QtWidgets.QLabel(self.central_widget)
        self.app_logo.setFixedSize(140, 140)
        self.app_logo.move(20, 10)
        self.app_logo.setPixmap(QtGui.QPixmap("Application Pictures and Icons/Time Track Icon.png"))
        self.app_logo.setScaledContents(True)
        self.app_logo.show()

        self.log_out_button = self.create_QPushButton("central_widget", "log_out", "None",
                                                      "Application Pictures and Icons/Log Out.png", 1240, -50, 160, 160)
        self.log_out_button.setIconSize(QtCore.QSize(150, 150))
        self.log_out_button.setFlat(True)
        self.log_out_button.clicked.connect(self.return_to_login_screen)

        sqliteConnection = sqlite3.connect('identifier.sqlite')
        cursor = sqliteConnection.cursor()
        username = user[0]
        password = user[1]
        first_name = user[2]
        last_name = user[3]
        cursor.execute(
            "SELECT * FROM students WHERE EMAIL_ADDRESS = ? AND PASSWORD = ? AND FIRST_NAME = ? AND LAST_NAME = ?",
            (username, password, first_name, last_name))
        self.logged_in_user_details = cursor.fetchall()
        cursor.close()

        self.setup_student_page(first_name, last_name)
        main_window.setCentralWidget(self.central_widget)
        self.status_bar = QtWidgets.QStatusBar(main_window)
        main_window.setStatusBar(self.status_bar)

    def initialize_administrator_page(self):
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

        self.log_out_button = self.create_QPushButton("central_widget", "log_out", "None",
                                                      "Application Pictures and Icons/Log Out.png", 1240, -50, 160, 160)
        self.log_out_button.setIconSize(QtCore.QSize(150, 150))
        self.log_out_button.setFlat(True)
        self.log_out_button.clicked.connect(self.return_to_login_screen)

        self.setup_admin_page()
        main_window.setCentralWidget(self.central_widget)
        self.status_bar = QtWidgets.QStatusBar(main_window)
        main_window.setStatusBar(self.status_bar)

    def setup_student_page(self, first_name, last_name):
        global dashboard_slideshow
        global slideshow_title
        global slideshow_description
        global kill_thread_boolean
        global threadpool
        global map

        user_details.get_user_details.__init__(self)

        self.tab_widget = VerticalTabWidget(self.central_widget)
        self.tab_widget.setObjectName("tab_widget")
        self.tab_widget.resize(1405, 700)
        self.tab_widget.move(0, 55)

        self.dashboard_tab = QtWidgets.QWidget()
        self.upcoming_events_tab = QtWidgets.QWidget()
        self.maps_tab = QtWidgets.QWidget()
        self.points_tab = QtWidgets.QWidget()
        self.rewards_tab = QtWidgets.QWidget()
        self.community_tab = QtWidgets.QWidget()
        self.student_profile_tab = QtWidgets.QWidget()

        self.tab_widget.addTab(self.dashboard_tab, "Dashboard")
        self.tab_widget.addTab(self.upcoming_events_tab, "Upcoming Events")
        self.tab_widget.addTab(self.maps_tab, "Maps")
        self.tab_widget.addTab(self.points_tab, "Points")
        self.tab_widget.addTab(self.rewards_tab, "Rewards")
        self.tab_widget.addTab(self.student_profile_tab, "My Student Profile")

        # Dashboard Tab
        self.intro_label = self.create_QLabel("central_widget", "intro_label", "Signed in as " + first_name + " " + last_name, 200, 10, 600, 50)
        self.dashboard_label = self.create_QLabel("dashboard_tab", "dashboard_label", "Dashboard", 20, 20, 600, 50)
        self.dashboard_title_line = self.create_QFrame("dashboard_tab", "dashboard_title_line", "HLine", 10, 65, 600, 6)
        dashboard_slideshow = self.create_QLabel("dashboard_tab", "dashboard_slider_label", "filler", 20, 90, 840, 480)
        dashboard_slideshow.setScaledContents(True)
        self.slideshow_description_groupbox = QtWidgets.QGroupBox(self.dashboard_tab)
        self.slideshow_description_groupbox.setGeometry(20, 580, 840, 100)
        slideshow_title = self.create_QLabel("slideshow_description_groupbox", "slideshow_title", "", 10, 10, 830, 20)
        slideshow_title.setWordWrap(True)
        slideshow_description = self.create_QLabel("slideshow_description_groupbox", "slideshow_description", "", 10, 35, 830, 100)
        slideshow_description.setWordWrap(True)
        slideshow_description.setAlignment(QtCore.Qt.AlignTop)
        kill_thread_boolean = False
        threadpool = QThreadPool()
        slideshow = Slideshow()
        threadpool.start(slideshow)

        sqliteConnection = sqlite3.connect('identifier.sqlite')
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT * FROM Announcement")
        announcements = cursor.fetchall()

        self.side_announcement1 = QtWidgets.QGroupBox(self.dashboard_tab)
        self.side_announcement1.setGeometry(880, 88, 320, 290)
        self.sa1_picture = QLabel(self.side_announcement1)
        self.sa1_picture.setGeometry(10, 15, 300, 200)
        self.sa1_picture.setPixmap(QPixmap(announcements[0][6]))
        self.sa1_picture.setScaledContents(True)
        self.sa1_title = QtWidgets.QLabel(self.side_announcement1)
        self.sa1_title.setWordWrap(True)
        self.sa1_title.setGeometry(10, 220, 300, 50)
        self.sa1_title.setText(announcements[0][1] + announcements[0][2])


        self.side_announcement2 = QtWidgets.QGroupBox(self.dashboard_tab)
        self.side_announcement2.setGeometry(880, 388, 320, 290)
        self.sa2_picture = QLabel(self.side_announcement2)
        self.sa2_picture.setGeometry(10, 15, 300, 200)
        self.sa2_picture.setPixmap(QPixmap(announcements[1][6]))
        self.sa2_picture.setScaledContents(True)
        self.sa2_title = QtWidgets.QLabel(self.side_announcement2)
        self.sa2_title.setWordWrap(True)
        self.sa2_title.setGeometry(10, 220, 300, 50)
        self.sa2_title.setText(announcements[1][1] + announcements[1][2])

        # Upcoming Events Tab
        self.upcoming_events_label = self.create_QLabel("upcoming_events_tab", "upcoming_events_label", "Upcoming Events", 20, 20, 600, 50)
        self.upcoming_events_title_line = self.create_QFrame("upcoming_events_tab", "upcoming_events_title_line", "HLine", 10, 65, 600, 6)
        self.student_calendar = self.create_QCalendar("upcoming_events_tab", 20, 80, 600, 600)
        self.student_calendar.selectionChanged.connect(self.student_upcoming_events_calendar)
        self.day_events_label = self.create_QLabel("upcoming_events_tab", "day_events_label", "  Selected Event", 765, 80, 430, 30)
        self.day_events = self.create_QTextEdit("upcoming_events_tab", "day_events", True, 765, 110, 430, 560)
        self.current_day = self.student_calendar.selectedDate().toString()
        self.day_events_label.setText("Events on: " + self.current_day[4:] + ":") #changed to self
        self.day_events.setAlignment(Qt.AlignTop)

        # Maps Tab
        self.maps_label = self.create_QLabel("maps_tab", "maps_label", "Maps", 20, 20, 600, 50)
        self.maps_line = self.create_QFrame("maps_tab", "maps_line", "HLine", 10, 65, 600, 6)
        self.map_container = QtWidgets.QGroupBox(self.maps_tab)
        self.map_container.setGeometry(QtCore.QRect(20, 80, 800, 600))
        self.maps_objects = self.create_QScrollArea("maps_tab", "maps_QScrollArea", "vertical_layout", 835, 85, 360, 595)
        self.maps = self.maps_objects[0]
        self.maps_layout = self.maps_objects[1]
        self.maps_scrollArea = self.maps_objects[2]

        # The created QGroupBox container's layout is set to hold the web widget
        self.map_frame = QtWidgets.QVBoxLayout(self.map_container)
        coordinate = (40.617847198627, -111.86923371648)
        map = folium.Map(zoom_start=12, location=coordinate, control_scale=True)
        folium.Marker(location=coordinate, icon=folium.Icon(color="darkgreen", icon='user'),).add_to(map)
        self.show_event_locations("student")
        data = io.BytesIO()
        map.save(data, close_file=False)
        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())
        self.map_frame.addWidget(webView)

        self.maps_scrollArea.setWidget(self.maps)
        self.maps_scrollArea.verticalScrollBar().setSliderPosition(0)

        # Points Tab
        self.points_label = self.create_QLabel("points_tab", "points_label", "Points", 20, 20, 600, 50)
        self.points_title_line = self.create_QFrame("points_tab", "points_title_line", "HLine", 10, 65, 600, 6)

    # combo boxes and stars

        self.event_combobox = QComboBox(self.points_tab)
        self.event_combobox.setGeometry(QtCore.QRect(60, 170, 200, 50))
        self.event_combobox.addItem("Select Event")
        self.event_combobox.addItem("Football Game")
        self.event_combobox.addItem("Volleyball Game")
        self.event_combobox.addItem("Basketball Game")
        self.event_combobox.addItem("Swim Meet")
        self.event_combobox.addItem("Wrestling Competition")


# stars/ rating

        self.rating_combobox = QComboBox(self.points_tab)
        self.rating_combobox.setGeometry(QtCore.QRect(440, 170, 200, 50))
        self.rating_combobox.addItem("Rate Event")
        self.rating_combobox.addItem("⭐⭐⭐⭐⭐" + " --> Amazing")
        self.rating_combobox.addItem("⭐⭐⭐⭐" + " --> Good")
        self.rating_combobox.addItem("⭐⭐⭐"+ " --> Average")
        self.rating_combobox.addItem("⭐⭐"  + " -->Bad")
        self.rating_combobox.addItem("⭐" + " -->Horrible")


# describe field
        self.info = QTextEdit(self.points_tab)
        self.info.setGeometry(50, 260, 600, 300)
        self.info.setAlignment(Qt.AlignTop)
        self.info.setWordWrapMode(True)


# send button

        self.QPushButton = QtWidgets.QPushButton(self.points_tab)
        self.QPushButton.setText("Send For Approval")
        self.QPushButton.setAccessibleName("push_button")
        self.QPushButton.clicked.connect(self.update_points)
        self.QPushButton.clicked.connect(self.send_approval)
        self.QPushButton.setGeometry(160, 600, 350, 50)


        self.points_leaderboard_objects = self.create_QScrollArea("points_tab", "points_leaderboard_QScrollArea",
                                                                  "vertical_layout", 750, 80, 450, 300)
        self.points_leaderboard = self.points_leaderboard_objects[0]
        self.points_leaderboard_layout = self.points_leaderboard_objects[1]
        self.points_leaderboard_scrollArea = self.points_leaderboard_objects[2]
        self.points_leaderboard_label = self.create_QLabel("points_tab", "points_leaderboard_label", "  Leaderboard: ", 750, 40, 450, 30)
        self.points_leaderboard_label  = self.create_QLabel("points_tab", " ", "Personal Points : " + str(self.user_points), 900, 40, 300, 30)


        # Leaderboard
        for student in students_leaderboard:
            self.event_object = QtWidgets.QGroupBox(self.points_leaderboard)
            self.event_object.setFixedSize(400, 50)
            self.event_object.setLayout(QtWidgets.QVBoxLayout())
            self.label = self.create_QLabel("event", "test", "   " + str(student[1]) + ", " + str(student[2]) +
                                            " Points: " + str(student[3]), 0, 0, 400, 30)
            self.points_leaderboard_layout.addWidget(self.event_object)
        self.points_leaderboard_scrollArea.setWidget(self.points_leaderboard)
        self.points_leaderboard_scrollArea.verticalScrollBar().setSliderPosition(0)

        # Rewards Tab
        sqliteConnection = sqlite3.connect('identifier.sqlite')
        cursor = sqliteConnection.cursor()

        cursor.execute("SELECT IMAGE_LINK_SRC FROM rewards")
        pictures = cursor.fetchall()
        cursor.execute("SELECT NAME FROM rewards")
        names = cursor.fetchall()
        cursor.execute("SELECT DESCRIPTION  FROM rewards")
        descriptions = cursor.fetchall()
        cursor.execute("SELECT POINTS  FROM rewards")
        points = cursor.fetchall()
        cursor.execute("SELECT EMAIL_ADDRESS, PASSWORD, POINTS FROM students")
        student_rows = cursor.fetchall()
        cursor.execute("SELECT intpoints  FROM rewards")
        intpoints = cursor.fetchall()


        cursor.close()
        picture_list = []
        name_list = []
        description_list = []
        points_list = []
        int_points_list = []
        for picture in pictures:
            picture_list.append(picture)
        for name in names:
            name_list.append(name)
        for description in descriptions:
            description_list.append(description)
        for point in points:
            points_list.append(point)
        for points in intpoints:
            int_points_list.append(points)


        self.rewards_label = self.create_QLabel("rewards_tab", "rewards_label", "Rewards", 20, 20, 600, 50)
        self.rewards_title_line = self.create_QFrame("rewards_tab", "rewards_title_line", "HLine", 10, 65, 600, 6)
        self.rewards_my_points_label = self.create_QLabel("rewards_tab", "rewards_my_points_label", "  Your Points: " + str(self.user_points), 950, 40, 300, 30)
        self.rewards_tab_objects = self.create_QScrollArea("rewards_tab", "rewards_QScrollArea", "grid_layout", 20, 120, 1180, 570)
        self.rewards_tab_objects = self.create_QScrollArea("rewards_tab", "rewards_QScrollArea", "grid_layout", 20, 120, 1180, 570)
        self.rewards = self.rewards_tab_objects[0]
        self.rewards_layout = self.rewards_tab_objects[1]
        self.rewards_events_scrollArea = self.rewards_tab_objects[2]

        index = 0

        for i in range(3):
            for j in range(3):
                self.event_object = QtWidgets.QGroupBox(self.rewards)
                self.event_object.setFixedSize(340, 300)
                self.event_object.setLayout(QtWidgets.QGridLayout())
                self.label = self.create_QLabel("event", "test", "  " + name_list[index][0], 10, 10, 100, 30)
                self.cost_label = self.create_QLabel("event", "point_cost", "Cost: " + points_list[index][0] + " points", 220, 10, 100, 30)
                self.text = QTextEdit(self.event_object)
                self.text.setGeometry(230, 40, 100, 200)
                self.text.setText(description_list[index][0])
                self.text.setAlignment(Qt.AlignTop)
                self.text.setWordWrapMode(True)
                self.picture = QLabel(self.event_object)
                self.picture.setGeometry(10, 40, 200, 200)
                self.picture.setPixmap(QPixmap(picture_list[index][0]))
                self.button = QPushButton(self.event_object)
                self.button.setText("Redeem " + name_list[index][0])
                self.button.setGeometry(10, 250, 320, 40)
                self.button.clicked.connect(self.deduct_points)

                # self.check_box = self.create_QCheckBox("event", 305, 12, 30, 30)
                self.rewards_layout.addWidget(self.event_object, i, j)
                index += 1
                if index == len(picture_list):
                    index = 0
        self.rewards_events_scrollArea.setWidget(self.rewards)
        self.rewards_events_scrollArea.verticalScrollBar().setSliderPosition(0)

        # Student Profile Tab
        self.student_profile_label = self.create_QLabel("student_profile_tab", "student_profile_label", "My Profile", 20, 20, 600, 50)
        self.student_profile_title_line = self.create_QFrame("student_profile_tab", "student_profile_title_line", "HLine", 10, 65, 600, 6)
        self.student_profile_data = self.create_QTextEdit("student_profile_tab", "student_profile_data", True, 900, 50, 300, 300)
        self.student_profile_data_label = self.create_QLabel("student_profile_tab", "student_profile_data_label", "  User Data", 900, 20, 300, 30)
        self.user_picture = self.create_QLabel("student_profile_tab", "user_picture", " Tester ", 20, 110, 300, 300) # for chips pic
        self.student_purchases_label = self.create_QLabel("student_profile_tab", "student_purchases_label", "Past Purchases ", 20, 80, 300, 50)

        self.user_picture.setPixmap(QPixmap(self.user_profile_picture))
        self.student_profile_data.setText("Name: " + first_name + " " + last_name + '\n\n Grade: ' + str(self.grade) + '\n\n Gender: ' + self.user_gender + '\n\n Date of Birth: ' + self.date_of_birth + '\n\n Events Attended: ' + str(self.events_attended) + '\n\n Points: ' + str(self.user_points))
        # self.student_profile_settings_button = self.create_QPushButton("main_window", "student_profile_settings_button", "Press me", "None", 700, 10, 100, 40)
        # self.student_profile_settings_button.clicked.connect(self.admin_events_calendar)

        self.tab_widget.show()

    def send_approval(self):
        sqliteConnection = sqlite3.connect('identifier.sqlite')
        cursor = sqliteConnection.cursor()

        first_name = user[2]
        last_name = user[3]

        event_combobox_selection = self.event_combobox.currentText()
        rating_combobox_selection = self.rating_combobox.currentText()
        description_box = self.info.toPlainText()



        cursor.execute(
            "INSERT INTO approval (FIRST_NAME, LAST_NAME, POINTS, EVENT, RATING, DESCRIPTION) VALUES ('" + first_name + "', '" + last_name + "', '" + str(
                self.user_points) + "', '" + event_combobox_selection + "', '" + rating_combobox_selection + "', '" + description_box + "')")
        sqliteConnection.commit()
        cursor.close()



    def approved_points(self):
        approved_message = QMessageBox()
        approved_message.setText("Approved hours")
        approved_message.setIcon(QMessageBox.Information)
        approved_message.exec_()

    def update_points(self):
        message = QMessageBox()
        message.setText("Sent to Administrator")
        message.setIcon(QMessageBox.Information)
        message.exec_()

        sqliteConnection = sqlite3.connect('identifier.sqlite')
        cursor = sqliteConnection.cursor()
        updated_user_points = self.logged_in_user_details[0][11] + 20
        cursor.execute("UPDATE students SET POINTS = ? WHERE FIRST_NAME = ?", (updated_user_points, self.first_name))
        sqliteConnection.commit()

        self.user_points = updated_user_points

        username = user[0]
        password = user[1]
        first_name = user[2]
        last_name = user[3]

        cursor.execute("SELECT * FROM students WHERE EMAIL_ADDRESS = ? AND PASSWORD = ? AND FIRST_NAME = ? AND LAST_NAME = ?",
                       (username, password, first_name, last_name))
        self.logged_in_user_details = cursor.fetchall()

        cursor.close()

        # self.rewards_my_points_label.setText("  Your Points: " + str(self.user_points))
        # self.points_leaderboard_label.setText("Personal Points : " + str(self.user_points))
        # self.student_profile_data.setText("Name: " + first_name + " " + last_name + '\n\n Grade: ' + str(
        #     self.grade) + '\n\n Gender: ' + self.user_gender + '\n\n Date of Birth: ' + self.date_of_birth + '\n\n Events Attended: ' + str(
        #     self.events_attended) + '\n\n Points: ' + str(self.user_points))
        #
        #
        # user_details.get_user_details.__init__(self)



    def setup_admin_page(self):
        self.intro_label = self.create_QLabel("central_widget", "intro_label", "Signed in as Dheeraj Vislawath", 200, 10, 600, 50)

        self.tab_widget = VerticalTabWidget(self.central_widget)
        self.tab_widget.setObjectName("tab_widget")
        self.tab_widget.resize(1405, 750)
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

        self.admin_dashboard_label = self.create_QLabel("admin_dashboard_tab", "admin_dashboard_label", "Dashboard", 20, 20, 600, 50)
        self.admin_dashboard_line = self.create_QFrame("admin_dashboard_tab", "admin_dashboard_line", "HLine", 10, 65, 600, 6)

        self.admin_events_label = self.create_QLabel("admin_events_tab", "admin_events_label", "Events", 20, 20, 600, 50)
        self.admin_events_line = self.create_QFrame("admin_events_tab", "admin_events_line", "HLine", 10, 65, 600, 6)
        self.admin_calendar = self.create_QCalendar("admin_events_tab", 20, 80, 350, 350)
        self.admin_calendar.selectionChanged.connect(self.admin_events_calendar)

        # setting selected date
        # self.admin_calendar.clicked.connect(lambda: self.admin_current_events.setText(text + str(self.count)))
        self.admin_events_title = self.create_QLabel("admin_events_tab", "admin_events_text", "Current Events", 400, 80, 400, 30)
        self.admin_current_events = self.create_QLineEdit("admin_events_tab", "admin_current_events", True, 400, 110, 400, 320)
        current_day = self.admin_calendar.selectedDate().toString()
        self.admin_current_events.setText("Events on " + current_day[4:] + ":")
        self.admin_current_events.setAlignment(Qt.AlignTop)

        self.admin_statistics_label = self.create_QLabel("admin_statistics_tab", "admin_statistics_label", "Statistics", 20, 20, 600, 50)
        self.admin_statistics_line = self.create_QFrame("admin_statistics_tab", "admin_statistics_line", "HLine", 10, 65, 600, 6)

        self.admin_student_view_label = self.create_QLabel("admin_student_view_tab", "admin_student_view_label", "Student View", 20, 20,600, 50)
        self.admin_student_view_line = self.create_QFrame("admin_student_view_tab", "admin_student_view_line", "HLine", 10, 65, 600, 6)


        self.send_annoucements_label = self.create_QLabel("admin_dashboard_tab", "adminApprovalBlue", " Send Announcements", 10, 100, 500, 55)
        self.send_annoucements_label.setFont(QFont('Open Sans', 19, QFont.Bold))

        self.name_of_annoucement_label = self.create_QLabel("admin_dashboard_tab", "adminApprovalBlue", " Name of Announcement", 10, 175, 500, 55)
        self.name_of_annoucement_label.setFont(QFont('Calibri', 12))

        self.name_annoucement_text = QTextEdit(self.admin_dashboard_tab)
        self.name_annoucement_text.setGeometry(10, 220, 300, 30)
        self.name_annoucement_text.setAlignment(Qt.AlignTop)
        self.name_annoucement_text.setWordWrapMode(True)

        self.name_of_annoucement_label = self.create_QLabel("admin_dashboard_tab", "adminApprovalBlue", " Announcement Details", 10, 300, 500, 55)
        self.name_of_annoucement_label.setFont(QFont('Calibri', 12))

        self.annoucement_detail = QTextEdit(self.admin_dashboard_tab)
        self.annoucement_detail.setGeometry(10, 350, 450, 200)
        self.annoucement_detail.setAlignment(Qt.AlignTop)
        self.annoucement_detail.setWordWrapMode(True)

        self.QPushButton = QtWidgets.QPushButton(self.admin_dashboard_tab)
        self.QPushButton.setText("Send Announcement")
        self.QPushButton.clicked.connect(self.send_annoucement)
        self.QPushButton.setGeometry(10, 600, 450, 50)

     #  self.adminApprovalLable = self.create_QLabel("admin_dashboard_tab", "adminApprovalLable", "My Profil", 20, 20, 600, 50)
        self.adminApprovalLine = self.create_QFrame("admin_dashboard_tab", "adminApprovalLine", "HLine", 10, 65, 600, 6)
        self.adminApprovalData = self.create_QTextEdit("admin_dashboard_tab", "adminApprovalData", True, 900, 50, 300, 300)
        self.adminApprovalBlue = self.create_QLabel("admin_dashboard_tab", "adminApprovalBlue", " Requests Pending Approval", 900, 20, 300, 30)
        self.tab_widget.show()

        approval_text = ""
        self.adminApprovalData.clear()  # clear the widget before adding new values
        layout = QVBoxLayout()  # create a vertical layout for the new widgets
        for approval in admin_approval_rows:
            widget = QWidget()  # create a new widget for each row
            hbox = QHBoxLayout()  # create a horizontal layout for the new widget
            label = QLabel()  # create a label to display the data for the row
            label.setText("Name: " + str(approval[0]) + " " + str(approval[1]) + "\nPoints: " + str(
                approval[2]) + "\nEvent: " + str(approval[3]) + "\nRating: " + str(
                approval[4]) + "\nDescription: " + str(approval[5]))
            button = QPushButton("Approve")  # create an "Approved" button for the row
            button.setFixedSize(100, 30)  # set the size of the button
            button.setProperty("row", approval)  # set the "row" property of the button to the current approval row
            button.clicked.connect(self.approved_points)
            hbox.addWidget(label)  # add the label and button to the horizontal layout
            hbox.addWidget(button)
            widget.setLayout(hbox)  # set the horizontal layout as the widget's layout
            layout.addWidget(widget)  # add the widget to the vertical layout
        self.adminApprovalData.setLayout(layout)  # set the vertical layout as the adminApprovalData widget's layout

        self.adminApprovalData.setText(approval_text)


    def send_annoucement(self):
        try:
            sqliteConnection = sqlite3.connect('identifier.sqlite')
            cursor = sqliteConnection.cursor()

            name_annoucement_text_stuff = self.name_annoucement_text.toPlainText()
            details_annoucement_text_stuff = self.annoucement_detail.toPlainText()

            cursor.execute(
                "INSERT INTO Announcement (NAME, DETAILS, ADDRESS, LONGITUDE, LATITUDE, IMAGE_LINK_SOURCE) VALUES ('" + str(name_annoucement_text_stuff) + "', '" + str(details_annoucement_text_stuff) + "', '" + "N/A" + "', '" + "N/A" + "', '" + "N/A" + "', '" + "N/A" + "')")
            sqliteConnection.commit()
            cursor.close()
        except Exception as e:
            print(e)
            
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
        month_dict = {"Jan" : 1, "Feb" : 2, "Mar" : 3, "Apr" : 4, "May" : 5, "Jun" : 6, "Jul" : 7, "Aug" : 8, "Sep" : 9, "Oct" : 10, "Nov" : 11, "Dec" : 12}
        new_month = month_dict[event_month]
        for event in events:
            events_day = event[8]
            events_month = event[7]
            events_year = event[6]
            if str(event_year) == str(events_year):
                if str(new_month) == str(events_month):
                    if str(event_day) == str(events_day):
                        self.admin_current_events.setText("Events on " + selected_date[4:] + ": " + event[2])

    # Logic Functions
    def deduct_points(self):
        global username
        global password
        global user
        point_cost = int(self.rewards_tab.sender().parent().findChild(QtWidgets.QLabel, "point_cost").text()[6:9])

        if self.user_points >= point_cost:

            # print(new_user_points)
            sqliteConnection = sqlite3.connect('identifier.sqlite')
            cursor = sqliteConnection.cursor()
            new_user_points = self.logged_in_user_details[0][11] - point_cost
            cursor.execute("UPDATE students SET POINTS = ? WHERE FIRST_NAME = ?", (new_user_points, self.first_name))
            sqliteConnection.commit()

            self.user_points = new_user_points
            username = user[0]
            password = user[1]
            cursor.execute("SELECT * FROM students WHERE EMAIL_ADDRESS = ? AND PASSWORD = ?",
                           (username, password))
            self.logged_in_user_details = cursor.fetchall()
            cursor.close()
            self.rewards_my_points_label.setText("  Your Points: " + str(self.user_points))

            user_details.get_user_details.__init__(self)


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
                marker_cluster = MarkerCluster().add_to(map)
                folium.Marker(location=event_coordinate,
                              icon=folium.Icon(color="red", icon='circle', prefix='fa'),
                              popup=(folium.Popup(f'<h6><b>{event[1]}</b></h6>' + "\n" + f'<h6><b>{event[2]}</b></h6>', show=True, min_width=20)),).add_to(marker_cluster)
                self.event_object = QtWidgets.QGroupBox(self.maps)
                self.event_object.setFixedSize(325, 100)
                self.event_object.setLayout(QtWidgets.QVBoxLayout())
                self.title = self.create_QLabel("event", "title", (event[1] + "\n" + event[2]), 10, 10, 305, 60)
                self.title.setWordWrap(True)
                self.date = self.create_QLabel("event", "date", (str(event[7]) + "/" + str(event[8]) + "/" + str(event[6])), 240, 0, 80, 60)
                self.description = self.create_QLabel("event", "description", (event[3]), 10, 60, 305, 40)
                self.description.setWordWrap(True)
                self.maps_layout.addWidget(self.event_object)

    def check_events_on_day(self):
        selected_date = self.upcoming_events_tab.sender().selectedDate().toString()
        numerical_data_list = selected_date.split()
        numerical_data_list[2] = int(numerical_data_list[2])
        numerical_data_list[3] = int(numerical_data_list[3])

        month_dict = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
        numerical_data_list[1] = month_dict[numerical_data_list[1]]
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
        return create_widget_functions.create_QCheckBox.__init__(self, container, x_coordinate, y_coordinate, width, length)

    def create_QCalendar(self, container, x_coordinate, y_coordinate, width, length):
        return create_widget_functions.create_QCalendar.__init__(self, container, x_coordinate, y_coordinate, width, length)

    def create_QLabel(self, container, object_name, text, x_coordinate, y_coordinate, width, length):
        return create_widget_functions.create_QLabel.__init__(self, container, object_name, text, x_coordinate, y_coordinate, width, length)

    def create_QLineEdit(self, container, object_name, read_only, x_coordinate, y_coordinate, width, length):
        return create_widget_functions.create_QLineEdit.__init__(self, container, object_name, read_only, x_coordinate, y_coordinate, width, length)

    def create_QTextEdit(self, container, object_name, read_only, x_coordinate, y_coordinate, width, length):
        return create_widget_functions.create_QTextEdit.__init__(self, container, object_name, read_only, x_coordinate, y_coordinate, width, length)

    def create_QScrollArea(self, container, object_name, layout, x_coordinate, y_coordinate, fixed_width, min_length):
        return create_widget_functions.create_QScrollArea.__init__(self, container, object_name, layout, x_coordinate, y_coordinate, fixed_width, min_length)

    def create_QFrame(self, container, object_name, orientation, x_coordinate, y_coordinate, width, length):
        return create_widget_functions.create_QFrame.__init__(self, container, object_name, orientation, x_coordinate, y_coordinate, width, length)

    def create_QPushButton(self, container, object_name, text, icon, x_coordinate, y_coordinate, width, length):
        if container == "main_window":
            self.QPushButton = QtWidgets.QPushButton(main_window)
            if text != "None":
                self.QPushButton.setText(text)
            if icon != "None":
                self.QPushButton.setIcon(QIcon(icon))
            self.QPushButton.setFixedSize(width, length)
            self.QPushButton.move(x_coordinate, y_coordinate)

            return self.QPushButton
        else: return create_widget_functions.create_QPushButton.__init__(self, container, object_name, text, icon, x_coordinate, y_coordinate, width, length)

    def create_horizontal_QSlider(self, container, x_coordinate, y_coordinate, width, length):
        return create_widget_functions.create_horizontal_QSlider.__init__(self, container, x_coordinate, y_coordinate, width, length)

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

            cursor.execute("SELECT rowid, * FROM slideshow WHERE id = " + str(index))
            row = cursor.fetchall()

            if index == len(picture_list)-1:
                index = 0
            else:
                slideshow_title.setText(row[0][2])
                slideshow_description.setText(row[0][3])
                time.sleep(5)
                index += 1
            if kill_thread_boolean == True:
                break
        cursor.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    with open("styling.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)
    main_window = QtWidgets.QMainWindow()
    ui = Main()
    ui.setup_window(main_window)
    main_window.show()
    sys.exit(app.exec_())