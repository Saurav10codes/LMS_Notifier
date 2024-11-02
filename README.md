![Logo ](https://cdn.discordapp.com/attachments/1096831439972085852/1302162934855761931/icon.jpg?ex=67271d3c&is=6725cbbc&hm=561044744304f5f05f39f8d063b8f61d2b9d6eebeb6201ff6fdb3715b62890b5&)

# What Does it Do?
At [IIT Mandi](https://www.iitmandi.ac.in/), we have a [LMS](https://lms.iitmandi.ac.in) (Learning Management System). 
One of the main problem of this site (or mobile app) is that it does not sends notification properly whenever new upload or announcement is made in the course. To tackle this problem, I've built this python script that sends notification whenever something is uploaded in the LMS.

# Introduction
I have used plain python for this project along with the following libraries/modules :

 - [`requests`](https://pypi.org/project/requests/) - To perform `GET` and `POST` requests to the LMS Website.
 - [`bs4 (BeautifulSoup)`](https://pypi.org/project/beautifulsoup4/) - To scrape the webpages.
 - [`pwinput`](https://pypi.org/project/pwinput/) - To hide the password with asterisks(`*`) in the terminal.
 - [`plyer`](https://pypi.org/project/plyer/) - To send notifications

The script checks the site every one hour (provided that the script is kept running by the user) .

# How to use?

 1. Make sure you have python installed in your system (Don't use online compilers).
 2. Download the repository as `zip` .
 3. Extract the `zip` wherever you want.
 4. Open `terminal` and navigate to the required folder.
 5. Type `python main.py`  then hit enter, and the work is done. 
 6. This will consume negligible amount of CPU, memory and disk (you can see the same in task manager if you don't believe) so you can keep it running in the background and do your work.

# Limitations :

 - Will NOT give notifications instantly (You can manually change the code to constantly check the site in lesser intervals, but don't make it too small otherwise your IP Address may get blocked for too many requests).
 - Can happen that you may get logged out after a certain duration of inactivity (can't do anything about it, that's how the website works).