import requests
from bs4 import BeautifulSoup
from pwinput import pwinput
from plyer import notification

import time

username = input('Enter your username : ')
password = pwinput('Enter your password : ')

loginUrl = 'https://lms.iitmandi.ac.in/login/index.php'
homePageUrl = 'https://lms.iitmandi.ac.in/'


class Courses:
    def __init__(self, name, mainLink, announcementLink, maxId, maxD):
        self.name = name
        self.mainLink = mainLink
        self.announcementLink = announcementLink
        self.maxId = maxId
        self.maxD = maxD

    def setMaxId(self, id):
        self.maxId = id
    
    def setMaxD(self, d):
        self.maxD = d



courseList = [] # It will contain the objects of the 'Courses' class

def notify(title, body):

    notification.notify(
        title=title,
        message=body,
        app_name="LMS Notifier",
        app_icon="./icon.ico"
    )


with requests.Session() as session:
    # using session to be logged in in the website

    loginGet = session.get(loginUrl)
    loginToken = BeautifulSoup(loginGet.text, 'html.parser').find_all('input')[1].get('value')
    # logintoken is the 2nd input field (hidden)
    

    payload = {
        'username':username,
        'password':password,
        'anchor' : '',
        'logintoken' : loginToken
    }
    # login requires 2 more input fields other than username and password
    # anchor is empty string('')
    # logintoken (string of len 32) is randomly generated on every session


    headers = {
        "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
    }
    # IMP : Content-Type is NOT json. It's urlencoded
    # User-Agent is usually needed to mimic browser


    loginPost = session.post(loginUrl,data=payload, headers=headers)

    homeGet = session.get(homePageUrl)

    if "You are not logged in" in homeGet.text:
        print('Login Unsuccessful')
        notify('Login Unsuccessful','Please Try Again')
        exit()

    print(f'Logged in as {username}')
    notify(f'Logged in as {username}','Please keep the python session running to get the notifications')


    # Course home page has links of increasing ?id= (on basis on date of upload)
        # eg : https://lms.iitmandi.ac.in/mod/resource/view.php?id=55986

    # Announcements page has links of increasing ?d= (on basis on date of upload)
        # eg : https://lms.iitmandi.ac.in/mod/forum/discuss.php?d=9561



    homePageSoup = BeautifulSoup(homeGet.text, 'html.parser')
    courseAnchors = homePageSoup.find_all('div', class_='coursebox') # contains the links to courses's main pages


    # 1. Creating array of objects for each course
    # 2. Filling in course name, course link, AA link, max ID, max D
    for box in courseAnchors:
        courseLink = box.a['href']

        coursePageSoup = BeautifulSoup(session.get(courseLink).text,'html.parser')
        probablyAALink = coursePageSoup.find_all('a',class_='aalink')[0].get('href')

        maxId = 0
        for i in coursePageSoup.find_all('a',class_='aalink'):
            s = i.get('href')
            id = int(s[s.find('?id=')+4:])
            if id > maxId:
                maxId = id
        

        if 'forum' in probablyAALink:
            annPageSoup = BeautifulSoup(session.get(probablyAALink).text, 'html.parser')
            maxD = 0
            for i in annPageSoup.find_all('a',class_='d-block'):
                s = i.get('href')
                d = int(s[s.find('?d=')+3:])
                if d > maxD:
                    maxD = d

            courseList.append(Courses(box.a.text.strip(), courseLink, probablyAALink, maxId, maxD))
        else:
            courseList.append(Courses(box.a.text.strip(), courseLink, None, maxId, None))



    # Main implementation starts (checking the site every 1 hour) :

    while True:

        time.sleep(3600) # 3600 seconds = 1 hour

        for course in courseList:
            # Sending request to course main page :
            newCoursePageSoup = BeautifulSoup(session.get(course.mainLink).text, 'html.parser')
            newMaxId = 0
            for i in newCoursePageSoup.find_all('a',class_='aalink'):
                s = i.get('href')
                id = int(s[s.find('?id=')+4:])
                if id > newMaxId:
                    newMaxId = id
            
            if newMaxId > course.maxId :
                print(f'You have a new notification from {course.name}')
                notify(course.name, f'You have a new notification from {course.name}')
                course.setMaxId(newMaxId)
            else:
                print(f'No new notifications in {course.name}')

            
            # Sending request to announcement page :
            if course.announcementLink != None:
                newAnnPageSoup = BeautifulSoup(session.get(course.announcementLink).text, 'html.parser')
                newMaxD = 0
                for i in newAnnPageSoup.find_all('a',class_='d-block'):
                    s = i.get('href')
                    d = int(s[s.find('?d=')+3:])
                    if d > newMaxD:
                        newMaxD = d

                if newMaxD > course.maxD:
                    print(f'You have a new announcement from {course.name}')
                    notify(course.name, f'You have a new announcement from {course.name}')
                    course.setMaxD(newMaxD)
                else:
                    print(f'No new annoucements in {course.name}')



# Courses Class structure :
# ------Courses
#   ├───name
#   ├───mainLink
#   ├───announcementLink
#   ├───maxId
#   ├───maxD
#   ├───mainPageCL
#   ├───annPageCL
#   ├───setMaxId(id)
#   ├───setMaxD(d)