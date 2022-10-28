# QuizletZeroBudget
The idea of the project is to create a program like AnkiApp or Quizlet, in which the user can access flashcards with different themes, create them, and study them. When the user selects a set, they are given a number of cards. When the user clicks on a card, the definition of the term appears on it and vice versa. 

The idea was implemented using various forms created in Qt Designer and a database created in SQLiteStudio. For each form, a separate class was created. The main window that appears when the app is started is the MyWidget(QMainWindow) class. This form uses  various Qt widgets to display sets of flashcards and a search bar, apply filters, and access other forms. The user can search for the sets by entering the desired name and pressing the 'Search' button or Enter. The user can also apply filters to only display their sets or choose between free/premium sets.

The set creation form is a SecondForm(QWidget) class, in which the user can create their own sets that thay can later find on the main page. 

The last form for learning is the ThirdForm(QWidget) class. This is the page for learning the terms themselves. 

The program is written in Python. QtDesigner and SQLiteStudio were used during the creation of the app. 

Operating Language: Russian


![image](https://user-images.githubusercontent.com/74925466/198718224-05da467d-f515-417e-92f5-a9843760c0db.png)

![image](https://user-images.githubusercontent.com/74925466/198718262-6c9b8a51-1741-4db0-90a9-7d0ed657f5c7.png)

![image](https://user-images.githubusercontent.com/74925466/198718305-aed788d9-edef-4a5c-9d6e-5491d14b4e84.png)


