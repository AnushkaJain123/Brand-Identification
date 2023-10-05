from tkinter import ttk, Tk, PhotoImage, SUNKEN, END
import random
from PIL import ImageTk, Image
from indexdb import DbOperations



class Brand:

    def __init__(self, master):
        self.master = master

        self.createDefaultFrames()
        self.home()

    def createDefaultFrames(self):
        #For Window Geometry with offset(where will it happen to open)
        self.master.geometry('640x500+250+150')

        #For Title of the Window
        self.master.title('Brand Identification Game')

        #Creating the Header which contains the Logo and Description of the App
        self.frame_header = ttk.Frame(self.master)
        self.frame_header.pack(pady = 15)
        self.logo= PhotoImage(file='images.gif').subsample(2,2)
        ttk.Label(self.frame_header, image=self.logo).grid(row=0, column=0, rowspan=4, padx = 10)
        ttk.Label(self.frame_header, text='Welcome to Brand Identification Game' ).grid(row=0, column=1, columnspan=1 )
        ttk.Label(self.frame_header, text='Test Your Knowledge on Brands').grid(row=1, column=1, columnspan=1 )


        #Creating a Frame Menu which contains Options  such as Info
        self.frame_menu = ttk.Frame(self.master)
        self.frame_menu.pack()

        #Adding Widget Buttons
        ttk.Button(self.frame_menu, text = "Home", command=self.home).grid(row=0,column=0)

        ttk.Button(self.frame_menu, text = "Info", command=self.info).grid(row=0,column=1)

        ttk.Button(self.frame_menu, text = "Settings", command=self.settings).grid(row=0,column=2)

        ttk.Button(self.frame_menu, text = "High Scores", command=self.high_scores).grid(row=0,column=3)

    #For Frame Body to call it. Frame Body varies with each menu. So Labels and other widgets will be created on that menu
    def create_frame_body(self):
        try:
            self.frame_body.forget()
        except:
            pass
        self.frame_body = ttk.Frame(self.master)
        self.frame_body.pack(pady=30)
        self.frame_body.config(relief=SUNKEN, padding=(100,15))


#**********Frame Menu Buttons Functions***************************************

    #Home Button Function
    def home(self):
        self.create_frame_body()
        self.score = 0
        self.db_obj = DbOperations()
        #As Database is in the form of List where different rows(question) reside. First have to convert into Dictionary
        self.questions = {}

        for i in self.db_obj.select_question():
            self.questions[i[1]] = tuple([i[2], i[3]])
        print(self.questions)
        ttk.Label(self.frame_body, wraplength = 300, text=""" Welcome to this Brand Identification Game.Score points according to your guesses.\n Click on Clues to Reveal few Clues at the cost of half of a point. Click on Play Button to start scoring. Info Button For More Information """).grid(row=0, columnspan=4)

        ttk.Button(self.frame_body, text="Start", command=self.play_start).grid(row=1, column=0, rowspan=1, columnspan=2, padx=10, pady=10)
        ttk.Button(self.frame_body, text="How to Play", command=self.info).grid(row=2, column=0, rowspan=1, columnspan=2, padx=10, pady=10)

    #Home Button Sub-Functionality
    def play_start(self):
        self.create_frame_body()
        ttk.Label(self.frame_body, text="Enter your name").grid(row=0,column=0, pady=5)
        self.player = ttk.Entry(self.frame_body)
        self.player.grid(row=1, column=0, pady=5)
        ttk.Button(self.frame_body, text="Enter", command=self.play).grid(row=2, column=0, pady=3)

    #Sub Button of the Start Button
    def play(self):
        self.create_frame_body()
        if self.questions:
            #Getting the Question from the Dictionary Keys and converting those keys into List and then choose it randomly
            question = random.choice(list(self.questions.keys()))

            ttk.Label(self.frame_body, text = question).grid(row=0, column=0, pady=5)

            self.answer_object = ttk.Entry(self.frame_body)
            self.answer_object.grid(row=1, column=0, pady=5)

            self.clue_button = ttk.Button(self.frame_body, text = "Clue", command = lambda: self.clue(question)) #passing the argument so lambda function is provided
            self.clue_button.grid(row=3, column=0, pady=5)

            ttk.Button(self.frame_body, text="Next", command=lambda: self.next_action(question)).grid(row=4, column=0, pady=5)

        else:
            if self.score < 0:
                self.score = 0

            self.player_name = self.player.get()
            ttk.Label(self.frame_body, text=f"You have reached the end of the game, {self.player_name}'s score is {self.score}").grid(row=0, column=0, pady = 5)
            self.db_obj.create_score(self.player_name, self.score)
            self.db_obj.select_score()
            self.score = 0
            ttk.Button(self.frame_body, text="Play Again", command=self.home).grid(row=2, column=0, pady=5)

    #For Clue and Next Action Button
    def next_action(self, question):
        self.answer = self.answer_object.get()
        self.answer_object.delete(0, END) #to deleting the entry of the answer object

        if self.answer.strip().lower() == self.questions[question][1]:
            self.score+=10

        #Deleting the old question
        self.questions.pop(question)
        self.play()

    def clue(self, question):
        self.score -= 5
        image = Image.open(self.questions[question][0])
        image = image.resize((80,80))

        self.image = ImageTk.PhotoImage(image)
        self.clue_button['state'] = 'disabled'

        ttk.Label(self.frame_body, image=self.image).grid(row=2, column=0, pady = 5)

    def info(self):
        self.create_frame_body()
        ttk.Label(self.frame_body, text="This is the information page").pack()

    def settings(self):
        self.create_frame_body()
        ttk.Label(self.frame_body, text="You can add or remove questions according to your needs.\n To Add a question, click on Add button below. \n Provide a question, and a clue to be an image, and comma seperated correct answer").grid(row=0, column=0, pady=5)
        ttk.Button(self.frame_body, text = "Add a question",  command= self.add_questions).grid(row=1, column=0, pady=5)

    #Settings Sub Functions

    #Add questions
    def add_questions(self):
        self.create_frame_body()

        ttk.Label(self.frame_body, text="Enter the question").grid(row=0,column=0, pady=5)
        self.question_field = ttk.Entry(self.frame_body)
        self.question_field.grid(row=0, column=1, pady=5)

        ttk.Label(self.frame_body, text="Enter the path to image for clue").grid(row=1,column=0, pady=5)
        self.path_to_image_field = ttk.Entry(self.frame_body)
        self.path_to_image_field.grid(row=1, column=1, pady=5)

        ttk.Label(self.frame_body, text="Enter the correct answer seperated by comma").grid(row=2,column=0, pady=5)
        self.add_answer_field = ttk.Entry(self.frame_body)
        self.add_answer_field.grid(row=2, column=1, pady=5)

        ttk.Button(self.frame_body, text="Add", command=self.save_questions).grid(row=3, column=0, pady=5)
    #Save Questions
    def save_questions(self):
        #global user_questions
        self.question = self.question_field.get()
        self.path_to_image = self.path_to_image_field.get()
        self.add_answer = set([self.add_answer_field.get()])
        self.db_obj.insert_questions(self.question, self.path_to_image, self.add_answer)
        #user_questions[self.question] = (self.path_to_image, self.add_answer)
        self.settings()


    def high_scores(self):
        self.create_frame_body()
        for i in self.db_obj.select_score():
            ttk.Label(self.frame_body, text= i).pack()



root = Tk()
Brand(root)
root.mainloop()
