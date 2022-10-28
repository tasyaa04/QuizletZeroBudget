# QuizletZeroBudget
The idea of the project is to create a program like AnkiApp or Quizlet, in which the user can access flashcards with different themes, create them, and study them. When the user selects a set, they are given a number of cards. When the user clicks on a card, the definition of the term appears on it and vice versa. 

The idea was implemented using various forms created in Qt Designer and a database created in SQLiteStudio. For each form, a separate class was created. The main window that appears when the app is started is the MyWidget(QMainWindow) class. This form uses  various Qt widgets to display sets of flashcards and a search bar, apply filters, and access other forms. The user can search for the sets by entering the desired name and pressing the 'Search' button or Enter. The user can also apply filters to find required sets or choose between free/premium sets.

The set creation form is a SecondForm(QWidget) class, in which the user can create their own sets that thay can later find on the main page. 

The last form for learning is the ThirdForm(QWidget) class. This is the page for learning the terms themselves. 

The program is written in Python. QtDesigner and SQLiteStudio were used during the creation of the app. 

