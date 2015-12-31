genes = {
			"0000":"0", "0001":"1", "0010":"2", 
			"0011":"3", "0100":"4", "0101":"5", 
			"0110":"6", "0111":"7", "1000":"8", 
			"1001":"9", "1010":"+", "1011":"-",
			"1100":"*", "1101":"/", "1110":"X",
			"1111":"X"
		 }

class Chromosone:
	def __init__(self,encoding,target):
		self.encoding = encoding		
		chromosone = self.encoding # calculates value of encoding expression
		splitted = [chromosone[i:i+4] for i in range(0,len(chromosone),4)] # Split chromosone into list of 4 bits
		accStr = "" 
		for byte in splitted:  # Combine chromosone bytes into string
			accStr += genes[byte]
		numAvailble = False
		opr = ""
		result = 0
		for char in accStr:
			if char in "+-*/" and numAvailble==False and opr == "":
				continue
			elif char in "0123456789" and numAvailble==False and opr == "":
				result = int(char)
				numAvailble = True
			# find another number and perform calculation
			elif char in "0123456789" and numAvailble==True and opr != "":
				# perform calculation, discard operator after use.
				# special case: avoid division by 0 by setting fitness score to 0
				try:
					result = eval(str(result)+opr+char)
				except ZeroDivisionError:
					self.fitnessScore = 0
					return
				opr = ""
			elif char in "+-*/" and numAvailble==True and opr == "":
				opr = char		

		tolerance = 0.01 # can be adjusted
		self.result = result
		error = float(result)-float(target)
		if (abs(error) < tolerance): 
			self.fitnessScore = -1 # given chromosone is a solution.
		else:
			score = 1/abs(error)
			self.fitnessScore = score

	# Returns the string expression used to calculate the fitness score
	def getEncoding(self):	
		chromosone = self.encoding
		splitted = [chromosone[i:i+4] for i in range(0,len(chromosone),4)]
		accStr = ""
		for byte in splitted:
			accStr += genes[byte]
		
		numAvailble = False
		opr = ""
		calcStr = ""
		for char in accStr:
			if char in "+-*/" and numAvailble==False and opr == "":
				continue
			elif char in "0123456789" and numAvailble==False and opr == "":
				calcStr = char
				numAvailble = True
			# find another number and perform calculation
			elif char in "0123456789" and numAvailble==True and opr != "":
				calcStr = calcStr+opr+char
				opr = ""
			elif char in "+-*/" and numAvailble==True and opr == "":
				opr = char
		return calcStr



invGenes = {
			"0":"0000", "1":"0001", "2":"0010", 
			"3":"0011", "4":"0100", "5":"0101", 
			"6":"0110", "7":"0111", "8":"1000", 
			"9":"1001", "+":"1010", "-":"1011",
			"*":"1100", "/":"1101", "X":"1110",
			"X":"1111"
		 }

# extra function for testing 
def convertExpr(expr):
	result = ""
	for char in expr:
		if char in "+-*/0123456789":
			result += invGenes[char]
	return(result)
