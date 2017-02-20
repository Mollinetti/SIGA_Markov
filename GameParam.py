
import Gene, Parameters, random

#GAME ENGINE, SHOULD HAVE BEEN CALLED LIKE THIS, BUT OH WELL...
class GameEngine:

	#game parameters, the letters represents the utility function received by playing:
	#
	#	R: reward
	#	T: temptation
	#	P: punishment
	#	S: sucker
	#
	def __init__(self):
		#starting payment matrix (original Dillema)
		self.R = 3
		self.T = 5
		self.S = 1
		self.P = 0

	#change game behavior according to chosen number (I used a number notation in order to leave an easier implementation for stochastic games)
	def change(self, type):

		#Prisoner's Dillema
		if type == 1:
			self.R = 3
			self.T = 5
			self.S = 1
			self.P = 0
		#Stag Hunt
		elif type == 2:
			self.R = 5
			self.T = 3
			self.S = 1
			self.P = 0
		#Hawk Dove
		elif type == 3:
			self.R = 3
			self.T = 5
			self.S = 0
			self.P = 1
		#Harmonic Games
		elif type == 4:
			self.R = 5
			self.T = 3
			self.S = 0
			self.P = 1

	#standard game without any sthocasticity
	def socialGame(self, p1 = Gene, p2 = Gene, param = Parameters):

		#initialize each player memory as if the opponent has cooperated (C: Cooperate | D: Defect)
		p1Memory ="C"
		p2Memory ="C"
		for i in range(0, param.numRounds):

			if p1.strategy == 'ALLC':
				if p2.strategy == "ALLC": 		
					p1.socialFitness+= self.R
					p2.socialFitness+= self.R
                    

				if p2.strategy== "ALLD":
					p1.socialFitness+= self.S
					p2.socialFitness+= self.T
					p2Memory = "D"

				if p2.strategy == "TFT":
					p1.socialFitness += self.R
					p2.socialFitness+= self.R 
                
			else :
				if p1.strategy == "ALLD":
					if p2.strategy == "ALLC":
						p1.socialFitness += self.T
						p2.socialFitness += self.S
						p1Memory = "D"

					if (p2.strategy == "ALLD") :
						p1.socialFitness += self.P
						p2.socialFitness += self.P
						p1Memory = "D"
						p2Memory = "D"

					if (p2.strategy == "TFT") :
						if p1Memory == "C":
                        
							p1.socialFitness += self.T
							p2.socialFitness+= self.S

						else :

							p1.socialFitness += self.P
							p2.socialFitness+= self.P
							p2Memory = "D"
                    
				else :
					if (p1.strategy == "TFT") :
						if (p2.strategy == "ALLC") :
                           
							p1.socialFitness += self.R
							p2.socialFitness+= self.R


						if (p2.strategy == "ALLD"):
							if  p1Memory == "C":
                             
								p1.socialFitness += self.S
								p2.socialFitness+= self.T
                                
							else:
								p1.socialFitness += self.P
								p2.socialFitness+= self.P
								p2Memory = "D"
                        

						if (p2.strategy == "TFT"):

							p1.socialFitness += self.R
							p2.socialFitness+= self.R

               
     #whole social interaction process
	def socialInteraction(self, population, param = Parameters):
    	
    	#initilize random list
		index = list(range(0, (int(param.popNum) - 1)))

		random.shuffle(index)

		for i in range(0, int(param.popNum)-2, 2):

			self.socialGame(population[index[i]], population[index[i+1]], param)
    	
