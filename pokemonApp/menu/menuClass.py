# -*- coding: utf-8 -*-
from PyInquirer import style_from_dict, Token, Separator
from mytools.formCheck import userValidator
import os

class menu:
	def __init__(self):

		self.style = style_from_dict({
			Token.QuestionMark: '#E91E63 bold',
			Token.Selected: '#673AB7 bold',
			Token.Instruction: '',	# default
			Token.Answer: '#2196f3 bold',
			Token.Question: '',
		})



	def questions_formater(self, questions):
		for i in range(len(questions)):
			if 'validate' in questions[i].keys():
				questions[i]['validate'] = eval(questions[i]['validate'])
			if 'when' in questions[i].keys():
				questions[i]['when'] = eval(questions[i]['when'])
			if 'choices' in questions[i].keys():
				if type(questions[i]['choices'])!=list:
					questions[i]['choices'] = eval(questions[i]['choices'])
				if "Separator()" in questions[i]['choices']:
					questions[i]['choices'][questions[i]['choices'].index("Separator()")] = Separator()
		return questions


	def getMenus(self):
		questions_ = []
		with open(os.getcwd()+"/menu/menu_questions.txt", "r") as f:
			f_data = eval(f.read())
		for i in f_data.keys():
			f_data[i] = self.questions_formater(f_data[i])
		return f_data

