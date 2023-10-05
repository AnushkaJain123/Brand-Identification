#Implementing the database into the python program

import sqlite3


class DbOperations:
    def __init__(self):
        #connecting the database
        self.conn = sqlite3.connect('Branddb.db')
        #Cursor which is used to execute the command
        self.curs = self.conn.cursor()

    #To Select questions from the table
    def select_question(self):
        self.curs.execute('SELECT * fROM question')
        self.questions = self.curs.fetchall()
        return self.questions

    #Inserting the questions
    def insert_questions(self, question,path, answer):
        try:
            self.curs.execute(f'INSERT INTO question (question, path, answer) VALUES("{question}","{path}","{answer}")')
            self.conn.commit()
        except Exception as e:
            print(e)

    #Deleting questions
    def delete_questions(self,id):
        try:
            self.curs.execute(f'DELETE FROM question WHERE serial = {id}')
            self.conn.commit()
        except Exception as e:
            print(e)



    #Printing the scores
    def select_score(self):
        try:
            self.curs.execute(f'SELECT * FROM score_table')
            self.scores = self.curs.fetchall()
            return self.scores
        except Exception as e:
            print(e)

    #Selecting Highest Score
    def highest_score(self):
        try:
            self.curs.execute(f'SELECT MAX(score), name FROM score_table')
            print(self.curs.fetchall())
        except Exception as e:
            print(e)

    #Creating score
    def create_score(self, player, score):
        try:
            self.curs.execute(f'INSERT INTO score_table (name, score) VALUES("{player}",{score})')

        except Exception as e:
            self.curs.execute(f'SELECT score FROM score_table WHERE name="{player}"')
            self.player_score = self.curs.fetchone()
            if self.player_score[0]< score :
                self.curs.execute(f'UPDATE score_table SET score=? WHERE name=?', [score, player])
        self.conn.commit()

questions = DbOperations()
#questions.insert_questions("This is my first question","path to image","the answer is this")
questions.create_score("Anu", 10)
