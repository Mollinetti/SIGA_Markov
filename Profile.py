import numpy, Parameters


class Profile(object):
	"""docstring for Profile"""
	def __init__(self, param = Parameters):
		super(Profile, self).__init__()
		#random sample [0,1)
		self.type = numpy.random.random_sample()
		#ALLC
		if (self.type >= 0  and self.type < param.allCRate):
			self.probC = 0.9
			self.probD = 0.1
		#ALLD
		elif (self.type >= param.allCRate  and  self.type < param.allCRate + param.allDRate):
			self.probC = 0.1
			self.probD = 0.9
		#TFT
		elif (self.type >= param.allCRate + param.allDRate   and  self.type < param.allCRate + param.allDRate + param.TFTRate):
			self.probC = 0.5
			self.probD = 0.5

		elif (self.type >= param.allCRate + param.allDRate + param.TFTRate and  self.type <= 1):
			self.probC = numpy.random.random_sample()
			self.probD = 1 - self.probC

		self.payoff = 0

	#model what kind of move will the player do
	def play(self):
		#flip a coin
		coin = numpy.random.random_sample()
		#C
		if (coin >= 0 and coin < self.probC):
			return "C"
		#D
		elif (coin >= self.probC and coin < 1):
			return "D"


	def calcDiscPayoff(self):
		pay = 0
		self.discountedpayoff+= pay

	def flush(self):
		self.payoff=0



