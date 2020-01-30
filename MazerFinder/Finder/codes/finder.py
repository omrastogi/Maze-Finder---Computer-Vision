
'''
*****************************************************************************************
*
*        		===============================================
*           		Rapid Rescuer (RR) Theme (eYRC 2019-20)
*        		===============================================
*
*  This script is to implement Task 1A of Rapid Rescuer (RR) Theme (eYRC 2019-20).
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
# Filename:			finder.py
# Functions:		readImage, solveMaze, blockwork
# Global variables:	CELL_SIZE


# Import necessary modules
# Do not import any other modules
import cv2
import numpy as np
import os


# To enhance the maze image
import image_enhancer


# Maze images in mazes folder have cell size of 20 pixels
CELL_SIZE = 20


#def blockwork(img,coordinate)

def readImage(img_file_path):

	"""
	Purpose:
	---
	the function takes file path of original image as argument and returns it's binary form

	Input Arguments:
	---
	`img_file_path` :		[ str ]
		file path of image

	Returns:
	---
	`original_binary_img` :	[ numpy array ]
		binary form of the original image at img_file_path

	Example call:
	---
	original_binary_img = readImage(img_file_path)

	"""
	binary_img = None

	#############	Add your Code here	###############
	
	img = cv2.imread(img_file_path,0)
	ret,img = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
	binary_img = img
	###################################################

	return binary_img


def solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width):

	"""
	Purpose:
	---
	the function takes binary form of original image, start and end point coordinates and solves the maze
	to return the list of coordinates of shortest path from initial_point to final_point

	Input Arguments:
	---
	`original_binary_img` :	[ numpy array ]
		binary form of the original image at img_file_path
	`initial_point` :		[ tuple ]
		start point coordinates
	`final_point` :			[ tuple ]
		end point coordinates
	`no_cells_height` :		[ int ]
		number of cells in height of maze image
	`no_cells_width` :		[ int ]
		number of cells in width of maze image

	Returns:
	---
	`shortestPath` :		[ list ]
		list of coordinates of shortest path from initial_point to final_point

	Example call:
	---
	shortestPath = solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width)

	"""
	
	shortestPath = []

	#############	Add your Code here	###############
	img = original_binary_img
	sp = []
	rec = [0]
	p = 0
	sp.append(list(initial_point))
	edgearray = []
	for i in range (no_cells_height):
		edgearray.append([])
		for j in range(no_cells_width):
			sz = [i,j]
			edge, block = blockwork(img, sz)
			edgearray[i].append(edge)	

	edge= edgearray 


	while True:
		h,w = sp[p][0],sp[p][1]
		if sp[-1]==list(final_point):
			break

		if edge[h][w] > 0:
			rec.append(len(sp))

		if edge[h][w]>999:
			edge[h][w] = edge[h][w]-1000
			h = h-1
			sp.append([h,w])
			edge[h][w] =edge[h][w]-100

			p = p+1
			continue

		if edge[h][w]>99:
			edge[h][w] =edge[h][w]-100
			h = h+1
			sp.append([h,w])
			edge[h][w] =edge[h][w]-1000
			p=p+1
			continue

	
		if edge[h][w]>9:
			edge[h][w] = edge[h][w]-10
			w = w-1
			sp.append([h,w])
			edge[h][w] = edge[h][w]-1
			p = p+1
			continue


		if edge[h][w]==1:
			edge[h][w] = edge[h][w]-1
			w = w+1
			sp.append([h,w])
			edge[h][w] = edge[h][w]-10
			p=p+1
			continue

		else: 
			sp.pop()
			rec.pop()
			p = rec[-1]
			
			
	for i in sp:
		shortestPath.append(tuple(i))
	




	###################################################
	
	return shortestPath


#############	You can add other helper functions here		#############

def blockwork(img,coordinate):
#coordinate is a list consisting for dimension of block to be processesd
#coordinate = [y-axis, x-axis]
#the first block is coordinate = [0,0]
	size = CELL_SIZE
	h = CELL_SIZE*(coordinate[0]+1)
	w = CELL_SIZE*(coordinate[1]+1)
	h0= CELL_SIZE*coordinate[0]
	w0= CELL_SIZE*coordinate[1]

	block = img[h0:h,w0:w]

	up    = bool(block[0,int(size/2)]) *1000
	down  = bool(block[int(size-1),int(size/2)])*100
	left  = bool(block[int(size/2),0]) *10
	right = bool(block[int(size/2),int(size-1)])*1

	

#	edge = [up, down, left, right]
	edge = up+down+left+right
	
	# cv2.imshow('image',block)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()
	return edge, block

#########################################################################


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
# 
# Function Name:	main
# Inputs:			None
# Outputs: 			None
# Purpose: 			the function first takes 'maze00.jpg' as input and solves the maze by calling readImage
# 					and solveMaze functions, it then asks the user whether to repeat the same on all maze images
# 					present in 'mazes' folder or not

if __name__ == '__main__':

	curr_dir_path = os.getcwd()
	img_dir_path = curr_dir_path + '/../mazes/'				# path to directory of 'mazes'
	
	file_num = 0
	img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'		# path to 'maze00.jpg' image file

	print('\n============================================')

	print('\nFor maze0' + str(file_num) + '.jpg')

	try:
		
		original_binary_img = readImage(img_file_path)
		height, width = original_binary_img.shape

	except AttributeError as attr_error:
		
		print('\n[ERROR] readImage function is not returning binary form of original image in expected format !\n')
		exit()
	
	no_cells_height = int(height/CELL_SIZE)							# number of cells in height of maze image
	no_cells_width = int(width/CELL_SIZE)							# number of cells in width of maze image
	initial_point = (0, 0)											# start point coordinates of maze
	final_point = ((no_cells_height-1),(no_cells_width-1))			# end point coordinates of maze

	try:

		shortestPath = solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width)

		if len(shortestPath) > 2:

			img = image_enhancer.highlightPath(original_binary_img, initial_point, final_point, shortestPath)
			
		else:

			print('\n[ERROR] shortestPath returned by solveMaze function is not complete !\n')
			exit()
	
	except TypeError as type_err:
		
		print('\n[ERROR] solveMaze function is not returning shortest path in maze image in expected format !\n')
		exit()

	print('\nShortest Path = %s \n\nLength of Path = %d' % (shortestPath, len(shortestPath)))
	
	print('\n============================================')
	
	cv2.imshow('canvas0' + str(file_num), img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	choice = input('\nWant to run your script on all maze images ? ==>> "y" or "n": ')

	if choice == 'y':

		file_count = len(os.listdir(img_dir_path))

		for file_num in range(file_count):

			img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'

			print('\n============================================')

			print('\nFor maze0' + str(file_num) + '.jpg')

			try:
				
				original_binary_img = readImage(img_file_path)
				height, width = original_binary_img.shape

			except AttributeError as attr_error:
				
				print('\n[ERROR] readImage function is not returning binary form of original image in expected format !\n')
				exit()
			
			no_cells_height = int(height/CELL_SIZE)							# number of cells in height of maze image
			no_cells_width = int(width/CELL_SIZE)							# number of cells in width of maze image
			initial_point = (0, 0)											# start point coordinates of maze
			final_point = ((no_cells_height-1),(no_cells_width-1))			# end point coordinates of maze

			try:

				shortestPath = solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width)

				if len(shortestPath) > 2:

					img = image_enhancer.highlightPath(original_binary_img, initial_point, final_point, shortestPath)
					
				else:

					print('\n[ERROR] shortestPath returned by solveMaze function is not complete !\n')
					exit()
			
			except TypeError as type_err:
				
				print('\n[ERROR] solveMaze function is not returning shortest path in maze image in expected format !\n')
				exit()

			print('\nShortest Path = %s \n\nLength of Path = %d' % (shortestPath, len(shortestPath)))
			
			print('\n============================================')

			cv2.imshow('canvas0' + str(file_num), img)
			cv2.waitKey(0)
			cv2.destroyAllWindows()
	
	else:

		print('')


