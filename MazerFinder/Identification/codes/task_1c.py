
'''
*****************************************************************************************
*
*        		===============================================
*           		Rapid Rescuer (RR) Theme (eYRC 2019-20)
*        		===============================================
*
*  This script is to implement Task 1C of Rapid Rescuer (RR) Theme (eYRC 2019-20).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD project under National Mission on Education using ICT (NMEICT)
*
*****************************************************************************************
'''


# Author List:		Om Rastogi
# Functions:		computeSum, checkNum, train, show, getNum 					
# Global variables:	None



# Import necessary modules
import cv2
import numpy as np
import os
import sys

#############	You can import other modules here	#############



#################################################################


# Function Name:	computeSum
# Inputs: 			img_file_path [ file path of image ]
# 					shortestPath [ list of coordinates of shortest path from initial_point to final_point ]
# Outputs:			digits_list [ list of digits present in the maze image ]
# 					digits_on_path [ list of digits present on the shortest path in the maze image ]
# 					sum_of_digits_on_path [ sum of digits present on the shortest path in the maze image ]
# Purpose: 			the function takes file path of original image and shortest path in the maze image
# 					to return the list of digits present in the image, list of digits present on the shortest
# 					path in the image and sum of digits present on the shortest	path in the image
# Logic:			[ write the logic in short of how this function solves the purpose ]
# Example call: 	digits_list, digits_on_path, sum_of_digits_on_path = computeSum(img_file_path, shortestPath)

def computeSum(img_file_path, shortestPath):

	"""
	Purpose:
	---
	the function takes file path of original image and shortest path as argument and returns list of digits, digits on path and sum of digits on path

	Input Arguments:
	---
	`img_file_path` :		[ str ]
		file path of image
	`shortestPath` :		[ list ]
		list of coordinates of shortest path from initial_point to final_point

	Returns:
	---
	`digits_list` :	[ list ]
		list of all digits on image
	`digits_on_path` :	[ list ]
		list of digits adjacent to the path from initial_point to final_point
	`sum_of_digits_on_path` :	[ int ]
		sum of digits on path

	Example call:
	---
	original_binary_img = readImage(img_file_path)

	"""

	digits_list = []
	digits_on_path = []
	sum_of_digits_on_path = 0

	#############  Add your Code here   ###############
	img = finder.readImage(img_file_path)
	knn = train()
	numberPosition = []
	for i in range (0,10):
		for j in range(0,10):
			edge, block = finder.blockwork(img,[i,j])
			block = block[4:36,4:36]
			if np.mean(block)< 250:
				numberPosition.append([i,j])
				num = getNum(block,knn)
				digits_list.append(num) 



	values = []
	for sc in shortestPath:
		sq = list(sc)

		edge, block = finder.blockwork(img,sq)
		getval = []
		if edge>999:
			checkpos = sq
			# print ("up",edge)
			edge = edge - 1000
			checkpos = [sq[0]-1,sq[1]]
			getval.append(checkNum(img,checkpos))

			
		if edge>99:
			# print ("down",edge)
			edge = edge - 100
			checkpos = [sq[0]+1,sq[1]]
			getval.append(checkNum(img,checkpos))

		if edge>9:
			# print ("left",edge)				
			edge = edge - 10
			checkpos = [sq[0],sq[1]-1]
			getval.append(checkNum(img,checkpos))

		if edge>0:
			# print ("right",edge)
			edge = edge - 1
			checkpos = [sq[0],sq[1]+1]
			getval.append(checkNum(img,checkpos))
		#print (getval)

		for val in getval:
			if val == None:
				continue
			for i in range(0,len(numberPosition)):
				if val == numberPosition[i]:
					digits_on_path.append(digits_list[i]) 
	


	for digit in digits_on_path:
		sum_of_digits_on_path+=digit


	
	###################################################

	return digits_list, digits_on_path, sum_of_digits_on_path


#############	You can add other helper functions here		#############
def checkNum(img,pos):
	edge, block = finder.blockwork(img,pos)
	block = block[4:36,4:36]
	if np.mean(block)< 250:
		return pos
	else:
		return None



def train():
	number = [0,1,2,3,4,5,6,7,8,9]
	cells=[]
	for label in number:
		directory = "DataSet/"+str(label)  
		for i in range(0,11):
			file = directory+"/"+"num"+str(i)+".png"
			digit = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
			# print ("train size",np.shape(digit))
			cell = digit.flatten()
			# print ("train size",np.size(cell))
			cells.append(cell)
	cells = np.array(cells, dtype=np.float32)        
	k = np.arange(len(number))
	cells_labels = np.repeat(k, 11)
	# print (cells_labels)
	knn = cv2.ml.KNearest_create()
	knn.train(cells, cv2.ml.ROW_SAMPLE, cells_labels)
	return knn


def show(cells):
	cv2.imshow('img',cells)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def getNum(img,knn):
	# show(img)
	img = img.flatten()
	test_cells = []
	test_cells.append(img)
	test_cells = np.array(test_cells, dtype=np.float32)
	# print ("test size",np.shape(img))
	ret, result, neighbours, dist = knn.findNearest(test_cells, k=1) 
	return int(result[0][0])

# def readImage(img_file_path):

# 	binary_img = None

# 	#############	Add your Code here	###############
	
# 	img = cv2.imread(img_file_path,0)
# 	ret,img = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
# 	binary_img = img
# 	###################################################

# 	return binary_img

#########################################################################


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
# 
# Function Name:	main
# Inputs:			None
# Outputs: 			None
# Purpose: 			the function first takes 'maze00.jpg' as input and solves the maze by calling computeSum
# 					function, it then asks the user whether to repeat the same on all maze images
# 					present in 'mazes' folder or not

if __name__ != '__main__':
	
	curr_dir_path = os.getcwd()

	# Importing finder and image_enhancer script
	try:

		finder_dir_path = curr_dir_path + '/../../Finder/codes'
		sys.path.append(finder_dir_path)

		import finder
		import image_enhancer

	except Exception as e:

		print('\nfinder.py or image_enhancer.pyc file is missing from Finder folder !\n')
		exit()

if __name__ == '__main__':
	
	curr_dir_path = os.getcwd()
	img_dir_path = curr_dir_path + '/../mazes/'				# path to directory of 'mazes'
	
	file_num = 4
	img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'		# path to 'maze00.jpg' image file

	# Importing finder and image_enhancer script
	try:

		finder_dir_path = curr_dir_path + '/../../Finder/codes'
		sys.path.append(finder_dir_path)

		import finder
		import image_enhancer

	except Exception as e:

		print('\n[ERROR] finder.py or image_enhancer.pyc file is missing from Finder folder !\n')
		exit()

	# modify the finder.CELL_SIZE to 40 since maze images
	# in mazes folder have cell size of 40 pixels
	finder.CELL_SIZE = 40

	print('\n============================================')

	print('\nFor maze0' + str(file_num) + '.jpg')

	try:
		
		original_binary_img = finder.readImage(img_file_path)
		height, width = original_binary_img.shape

	except AttributeError as attr_error:
		
		print('\n[ERROR] readImage function is not returning binary form of original image in expected format !\n')
		exit()

	
	no_cells_height = int(height/finder.CELL_SIZE)					# number of cells in height of maze image
	no_cells_width = int(width/finder.CELL_SIZE)					# number of cells in width of maze image
	initial_point = (0, 0)											# start point coordinates of maze
	final_point = ((no_cells_height-1),(no_cells_width-1))			# end point coordinates of maze

	try:

		shortestPath = finder.solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width)

		if len(shortestPath) > 2:

			img = image_enhancer.highlightPath(original_binary_img, initial_point, final_point, shortestPath)
			
		else:

			print('\n[ERROR] shortestPath returned by solveMaze function is not complete !\n')
			exit()
	
	except TypeError as type_err:
		
		print('\n[ERROR] solveMaze function is not returning shortest path in maze image in expected format !\n')
		exit()

	print('\nShortest Path = %s \n\nLength of Path = %d' % (shortestPath, len(shortestPath)))

	digits_list, digits_on_path, sum_of_digits_on_path = computeSum(img_file_path, shortestPath)

	print('\nDigits in the image = ', digits_list)
	print('\nDigits on shortest path in the image = ', digits_on_path)
	print('\nSum of digits on shortest path in the image = ', sum_of_digits_on_path)

	print('\n============================================')

	# cv2.imshow('canvas0' + str(file_num), img)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()

	choice = input('\nWant to run your script on all maze images ? ==>> "y" or "n": ')

	if choice == 'y':

		file_count = len(os.listdir(img_dir_path))

		for file_num in range(file_count):

			img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'		# path to 'maze00.jpg' image file

			print('\n============================================')

			print('\nFor maze0' + str(file_num) + '.jpg')

			try:
				
				original_binary_img = finder.readImage(img_file_path)
				height, width = original_binary_img.shape

			except AttributeError as attr_error:
				
				print('\n[ERROR] readImage function is not returning binary form of original image in expected format !\n')
				exit()

			
			no_cells_height = int(height/finder.CELL_SIZE)					# number of cells in height of maze image
			no_cells_width = int(width/finder.CELL_SIZE)					# number of cells in width of maze image
			initial_point = (0, 0)											# start point coordinates of maze
			final_point = ((no_cells_height-1),(no_cells_width-1))			# end point coordinates of maze

			try:

				shortestPath = finder.solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width)

				if len(shortestPath) > 2:

					img = image_enhancer.highlightPath(original_binary_img, initial_point, final_point, shortestPath)
					
				else:

					print('\n[ERROR] shortestPath returned by solveMaze function is not complete !\n')
					exit()
			
			except TypeError as type_err:
				
				print('\n[ERROR] solveMaze function is not returning shortest path in maze image in expected format !\n')
				exit()

			print('\nShortest Path = %s \n\nLength of Path = %d' % (shortestPath, len(shortestPath)))

			digits_list, digits_on_path, sum_of_digits_on_path = computeSum(img_file_path, shortestPath)

			print('\nDigits in the image = ', digits_list)
			print('\nDigits on shortest path in the image = ', digits_on_path)
			print('\nSum of digits on shortest path in the image = ', sum_of_digits_on_path)

			print('\n============================================')

			cv2.imshow('canvas0' + str(file_num), img)
			cv2.waitKey(0)
			cv2.destroyAllWindows()

	else:

		print('')


