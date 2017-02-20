import numpy, Profile, Parameters

class Game(object):
	"""Social interaction between two individuals. Does not deal with rounds with other players, just
	with one player"""
	def __init__(self, param = Parameters, p1 = Profile, p2 = Profile):
		super(Game, self).__init__()
		self.param = param

		self.p1 = p1
		self.p2 = p2

		#initial payment matrix (original Dillema)
		self.R = 0
		self.T = 0
		self.S = 0
		self.P = 0

		#discount factor
		self.beta = 0.9

		#state matrixes
		self.state = []
		#initialize state S0 with equal chance for all 4 games [1x4]
		self.state.append(numpy.array([0.25, 0.25, 0.25, 0.25]))
		#initialize probability matrix P (4x4) with same chance for everyone
		#	 PD		 HD		 SH		 H
		#  [.25		.25		.25		.25]
		self.pmat = numpy.full((4,4),0.25, dtype=float)

	def doGame(self):
		for i in range(0,self.param.numRounds):
		#flip a coin to decide which game will be chosen according to the state array
			coin = numpy.random.random_sample()
			#configuration tuple
			#			0	 1  2   3  4      5               6             
			#config = (name, R, T , P, S, player1 reward, player2reward)
			config = None
			#PRISONER DILLEMA
			if(coin >= 0 and coin < self.state[i][0]):
				config=self.interaction(i+1,config = "PD")
			#HAWK DOVE
			elif(coin >= self.state[i][0] and coin < self.state[i][0] + self.state[i][1]):
				config=self.interaction(i+1,config = "HD")
			#STAG HUNT
			elif(coin >=  self.state[i][0] + self.state[i][1] and coin < self.state[i][0] + self.state[i][1] + self.state[i][2]):
				config=self.interaction(i+1,config = "SH")
			#HARMONICS
			elif(coin >=  self.state[i][0] + self.state[i][1] + self.state[i][2] and coin < 1):
				config=self.interaction(i+1,config = "H")

			#model the probability matrix according to the outcome of the game
			#both play C, receive R and R > T
			if(config[5] == "R" and config[6] == "R" and config[1] > config[2]):
				self.pmat = numpy.array([[0.25, 0.25, 0.25, 0.25],[0.25, 0.25, 0.25, 0.25],[0.05, 0.05, 0.45, 0.45],[0.05, 0.05, 0.45, 0.45]])
			#both play C, receive R and T > R
			elif(config[5] == "R" and config[6] == "R" and config[1] < config[2]):
				self.pmat = numpy.array([[0.05, 0.05, 0.45, 0.45],[0.05, 0.05, 0.45, 0.45],[0.25, 0.25, 0.25, 0.25],[0.25, 0.25, 0.25, 0.25]])
			#both play D, receive P and P > S
			elif(config[5] == "P" and config[6] == "P" and config[3] > config[4]):
				self.pmat = numpy.array([[0.25, 0.25, 0.25, 0.25],[0.45, 0.05, 0.45, 0.05],[0.25, 0.25, 0.25, 0.25],[0.45, 0.05, 0.45, 0.05]])
			#both play D, receive P and S > P
			elif(config[5] == "P" and config[6] == "P" and config[3] < config[4]):
				self.pmat = numpy.array([[0.45, 0.45, 0.05, 0.05],[0.25, 0.25, 0.25, 0.25],[0.45, 0.45, 0.05, 0.05],[0.25, 0.25, 0.25, 0.25]])
			#anything else
			else:
				self.pmat = numpy.array([[0.25, 0.25, 0.25, 0.25],[0.25, 0.25, 0.25, 0.25],[0.25, 0.25, 0.25, 0.25],[0.25, 0.25, 0.25, 0.25]])

			#update state matrix
			self.state.append(numpy.dot(self.state[i],self.pmat))
			#print(config[5], config[6])

		return self.p1, self.p2



	def interaction(self, turn, config = None):
		p1reward = None
		p2reward = None
		#Prisoner's Dillema
		if config == "PD":
			self.R = 3
			self.T = 5
			self.S = 1
			self.P = 0
		#Stag Hunt
		elif config == "HD":
			self.R = 5
			self.T = 3
			self.S = 1
			self.P = 0
		#Hawk Dove
		elif config == "SH":
			self.R = 3
			self.T = 5
			self.S = 0
			self.P = 1
		#Harmonic Games
		elif config == "H":
			self.R = 5
			self.T = 3
			self.S = 0
			self.P = 1

		#both player make their move
		p1move = self.p1.play()
		p2move = self.p2.play()

		#model all possible moves (both C, both D, one D and one C)
		#both cooperate
		if(p1move == "C" and p2move == "C"):
			p1reward = p2reward = "R"
			self.p1.payoff+= numpy.power(self.beta,turn) * self.R
			self.p2.payoff+= numpy.power(self.beta,turn) * self.R
		#player1 cooperate and player 2 defect
		elif(p1move == "C" and p2move == "D"):
			p1reward = "S"
			p2reward = "T"
			self.p1.payoff+= numpy.power(self.beta,turn) * self.S
			self.p2.payoff+= numpy.power(self.beta,turn) * self.T
		#player 1 defect and player 2 cooperate
		elif(p1move == "D" and p2move == "C"):
			p1reward = "T"
			p2reward = "S"
			self.p1.payoff+= numpy.power(self.beta,turn) * self.T
			self.p2.payoff+= numpy.power(self.beta,turn) * self.S
		#both defect
		elif(p1move == "D" and p2move == "D"):
			p1reward = p2reward = "P"
			self.p1.payoff+= numpy.power(self.beta,turn) * self.P
			self.p2.payoff+= numpy.power(self.beta,turn) * self.P

		return config, self.R, self.T, self.P, self.S, p1reward, p2reward




