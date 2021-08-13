import numpy as np 
from PIL import Image, ImageDraw
import os

# this probably should have been a class, I know it looks silly constantly opening the image, converting to RGB ect 
# below is what actually takes a picture. I convert the pdfs to pngs, then I use the code below to crop the questions. 

white = (255,255,255)
black = (0,0,0)
gray = (209,209,209)
positions = []

img_dir1 = r"C:\Users\moham\Desktop\python projects\satmath\work\out-1.png"
img_dir2 = r"C:\Users\moham\Desktop\python projects\satmath\work\out-2.png"
img_dir3 = r"C:\Users\moham\Desktop\python projects\satmath\work\out-3.png"
img_dir4 = r"C:\Users\moham\Desktop\python projects\satmath\work\out-4.png"
def black_count(filename):
	# counts the number of black pixels and returns the ratio of black pixels to all pixels 
	crop_whiten(filename)
	image = Image.open("temp.png")
	image = image.convert("RGB")
	image_load = image.load()
	width = image.size[0]
	height = image.size[1]

	all_pixels = width * height
	black = 0

	for i in range(width):
		for j in range(height):

			if image_load[i,j] == (0,0,0):
				black += 1

	return(black / all_pixels)

def white_line_count(filename):
	counter = []
	image = Image.open(filename)
	image = image.convert("RGB")
	width = image.size[0]
	height = image.size[1]
	image_load = image.load()


	for j in range(height):
		white_line = True
		for i in range(width):
			if image_load[i,j] != (255,255,255):
				white_line = False
		if white_line == True:
			counter.append(1)
		else:
			counter.append(0)
	bottom_crop = 0
	for i in range(len(counter)-70):
		white = True
		for j in range(70):
			if counter[i+j] != 1:
				white = False
		if white == True:
			bottom_crop = i
			break
	top_crop = 0
	for i in range(len(counter)):
		if counter[i] == 0:
			top_crop = i
			break

	return(top_crop, bottom_crop)


def crop_whiten(filename,name="temp.png"):
	# crops the top of the image, replaces all grays for white 
	# makes it easier to find the question positions 

	white = (255,255,255)
	black = (0,0,0)

	image = Image.open(filename)
	image = image.convert("RGB")
	width = image.size[0]
	height = image.size[1]
	image = image.crop((0,230,width,height))
	width = image.size[0]
	height = image.size[1]
	image_load = image.load()

	for i in range(width):
		for j in range(height):
			if image_load[i,j][0] > 50:
				image_load[i,j] = white
			else: 
				image_load[i,j] = black
	image.save(name)

def top_left(filename):
	crop_whiten(filename)
	# crop whitten will crop the page image such that a question always begins on the first line, so loop through the first line's
	# pixel looking for the first black pixel. When I find it, I append the x-coor to the rulers list, then I skip 50 pixels and start
	# looking for the next question on the first line, there is usually two.
	# once I find the x-coor for the first two questions, I know that all other question on the page will be directly below them, so
	# I loop down through the pixels with same x-positions. once I find a black pixel, I have an x-coor, and a y-coor, and I append 
	# that to toppositions. Once I get all the x-coors and y-coors for all questions, I return toppositions. the function's called 
	# top_left because once I crop the image, the coors I get back will represent (drumroll please) the top-most and left-most positions   
	image = Image.open("temp.png")
	image = image.convert("RGB")
	width = image.size[0]
	height = image.size[1]
	image_load = image.load()
	rulers = []
	toppositions = []
	i = 0
	while i < width:
		if image_load[i,0] == black:
			# looping through the first line, I have to use a while loop so I can skip some pixels.
			rulers.append(i)
			i+= 50
		#print(i)
		i+= 1
	for i in range(2):
		j = 0
		while j < height:
			if image_load[rulers[i],j] == black:
				# looping down
				toppositions.append([rulers[i],j])
				j += 50
			j+= 1 

	return toppositions

def pos(filename):
	# I crop the image but I dont use the crop_whitten function, meaning the image looks normal. I look for where the gray bar
	# changes to white, I know the question will always be directly below the gray bar. Like with the top_left function, once I know
	# where the two gray bars at the top are, I know the others are directly below them, so again I loop down from there and get 
	top_pos = top_left(filename)
	image = Image.open(filename)
	image = image.convert("RGB")
	width = image.size[0]
	height = image.size[1]
	image = image.crop((0,230,width,height))
	image_load = image.load()
	height = image.size[1]
	gray_ruler = []
	for i in range(width):
		if image_load[i,0] == gray and image_load[i+1,0] == white:
			gray_ruler.append(i)



	mini = top_pos[0][0]
	maxi = top_pos[-1][0]
	final_pos = []

	for i in range(len(top_pos)):
		coor = []
		#left top right bottom 
		if top_pos[i][0] == mini: 
			final_pos.append([top_pos[i][0],top_pos[i][1],gray_ruler[0],top_pos[i][1]+500])
		else: 
			final_pos.append([top_pos[i][0],top_pos[i][1],gray_ruler[1],top_pos[i][1]+500])
	return final_pos 

def show_questions(filename):
	final_pos = pos(filename)
	# print(final_pos)
	white = (255,255,255)
	black = (0,0,0)

	image = Image.open(filename)
	image = image.convert("RGB")
	image_load = image.load()
	width = image.size[0]
	height = image.size[1]

	page_question_list = []

	for i in range(len(final_pos)):
		temping = image.copy()
		temping = temping.crop((final_pos[i][0],final_pos[i][1]+233,final_pos[i][2],height))
		temping.save("goddamnme.png")

		temping2 = Image.open("goddamnme.png")
		width = temping2.size[0] 
		top_crop, bottom_crop = white_line_count("goddamnme.png")
		temping2 = temping2.crop((0,top_crop,width,bottom_crop+10))

		page_question_list.append(temping2)
	return page_question_list


temp_tot_question_list = []
directory = r'C:\Users\moham\Desktop\python projects\satmath\work'
for filename in os.listdir(directory):
    if  filename.endswith(".png"):
    	if black_count(os.path.join(directory, filename)) <= 0.025:
        	# print(os.path.join(directory, filename))
        		page_question_list = show_questions(os.path.join(directory, filename))
        		temp_tot_question_list.append(page_question_list)        	

    else:
        continue
tot_question_list = []
for i in range(len(temp_tot_question_list)):
	for j in range(len(temp_tot_question_list[i])):
		tot_question_list.append(temp_tot_question_list[i][j])
for i in range(len(tot_question_list)):
	tot_question_list[i].save("question%i.png"%(i+1))









# copy_pixels = np.zeros((width,height))
# copy = Image.new('RGB',(width,height), color=white)
# copy_load = copy.load()

# for i in range(height):
# 	for j in range(width): 

# 		r,g,b = image.getpixel((j,i))

# 		if (r,g,b) != white:
# 			copy_pixels[j,i] = 255


# 		if copy_pixels[j,i] == 255:
# 			copy_load[j,i] = black



# for i in range(height):
# 	for j in range(width):

# 		if copy_pixels[j,i] == 255:
# 			copy_load[j,i] = black
# copy.save("copy.png")































# img = Image.open("sat5.png")
# img = img.convert("RGB")

# red_pixels = []

# for i in range(img.size[0]):
# 	column = []
# 	for j in range(img.size[1]):

# 		r,g,b = img.getpixel((i,j))

# 		if r != 255:
# 			column.append([r,g,b])
# 		else:
# 			column.append([255,0,0])
# 	red_pixels.append(column)

# red_img = Image.new("RGB",(img.size[0],img.size[1]),"black")
# print(red_img.size)

# red_img_pixels = red_img.load()

# for i in range(red_img.size[0]):
# 	for j in range(red_img.size[1]):

# 		red_img_pixels[i,j] = tuple(red_pixels[i][j])

# red_img.show()

