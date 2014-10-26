# CAMRANGER APPLICATION
#
# Marshall Ehlinger, 10/24/14
####
# This is an aid to building a traditional climbing rack. There is no subsitute for proper safety instruction.
# Rock climbing is an inherently dangerous sport. The information in this app is not guaranteed to be correct.
# Use, and climb, wholly at your own risk. All measurements should be assumed false unless you physically check them.
# Don't sue me when you whip. Wear a helmet. All measurements are in inches. Join the AAC.
# Good luck, sucka.
####

from Tkinter import *


class CamRangerApp:
	def __init__(self, master, camList):
		master.wm_title('CamRanger')
		self.parentList = camList

		lframe = Frame(master)
		rframe = Frame(master)
		bframe = Frame(master)
		rframe.config(bg="grey")
		bframe.config(bg="grey")
		lframe.pack(side=LEFT)
		rframe.pack(side=RIGHT)
		bframe.pack(side=BOTTOM)

		scrollbar = Scrollbar(master, orient=VERTICAL)
		self.listbox = Listbox(master, selectmode=MULTIPLE, yscrollcommand=scrollbar.set, bg="white")
		scrollbar.config(command=self.listbox.yview)
		scrollbar.pack(side=RIGHT, fill=Y)
		self.listbox.pack(side=LEFT, fill=BOTH, expand=1)


		self.populateListbox(lframe, self.listbox)
		self.establishCanvas(rframe)
		self.establishDataBox(bframe)


		graphButton = Button(bframe, text='GRAPH', highlightbackground="grey", command=self.graphRack)
		graphButton.pack(side=TOP)

		clearButton = Button(bframe, text='CLEAR', highlightbackground="grey", command=self.clearGraph)
		clearButton.pack(side=TOP)

		quitButton = Button(bframe, text='EXIT', highlightbackground="grey", command=rframe.quit)
		quitButton.pack(side=BOTTOM)

		

	def populateListbox(self, master, emptylb):
		listbox = emptylb
		i = 0
		for item in self.parentList:
			listbox.insert(END, self.parentList[i][0])
			i +=1

	def clearGraph(self):
		self.graphField.delete(ALL)
		self.dataBox.delete(ALL)
		self.listbox.selection_clear(0, self.listbox.size()-1)


	def establishCanvas(self, master):
		self.canvas_width= 500
		self.canvas_height= 500
		self.graphField = Canvas(master, width=self.canvas_width, height=self.canvas_height, bg="grey")
		self.graphField.pack(side=RIGHT)

	def establishDataBox(self, master):
		self.dataBoxWidth = self.canvas_width/2
		self.dataBox = Canvas(master, width = self.dataBoxWidth, bg='gray')
		self.dataBox.pack(side=RIGHT)

	def graphRack(self):
		# Clear the data and visuals from previous rack
		self.graphField.delete(ALL)
		self.dataBox.delete(ALL)
		# Initialize variable for the new rack
		selectedRack = []
		# Add selections from cam listbox to the selectedRack variable
		for index in self.listbox.curselection():
			selectedRack.append(self.parentList[int(index)])
		# Sort by the max expansion ranges of each cam	
		selectedRack.sort(key=lambda x: x[2])
		# Define relevant data for databox and spacing of bars on graph
		minExpansion = selectedRack[0][1]
		maxExpansion = selectedRack[len(selectedRack)-1][2]
		# Create list (gapsInRack) of any gaps of width where no cam in list offers protection (to be used in the databox)
		gapsInRack = []
		prevCamMax = 0.00
		for cam in selectedRack:
			curCamMin = cam[1]
			if prevCamMax < curCamMin:
				gapsInRack.append(str(prevCamMax) + ' to ' + str(curCamMin))
			prevCamMax = cam[2]
		# Define variables used to position and size the graph bars
		heightInterval = self.canvas_height/len(selectedRack)
		yvalue = 0
		# Graph the rack
		for item in selectedRack:
			upperleftx= float(item[1])*float(self.canvas_width)/float(maxExpansion)
			upperlefty= yvalue
			lowerrightx= float(item[2])*float(self.canvas_width)/float(maxExpansion)
			yvalue += heightInterval
			lowerrighty= yvalue
			self.graphField.create_rectangle(upperleftx, upperlefty, lowerrightx, lowerrighty, fill=item[3])
			self.graphField.create_text(upperleftx, upperlefty, text=item[0], anchor=NW, fill='black')

		# Populate the databox with relevant data
		self.dataBox.create_text(5, 0, text='Widest Protectable Width: ' + maxExpansion + ' in', anchor=NW, width=self.dataBoxWidth)
		self.dataBox.create_text(5, 20, text='Smallest Protectable Width: ' + minExpansion + ' in', anchor=NW, width=self.dataBoxWidth)
		self.dataBox.create_text(5, 40, text='No Protection Between:\n' + '\n'.join(gapsInRack), anchor=NW, width=self.dataBoxWidth)


def getCamsFromFile(source):
	doc = open(source, 'r')
	camsLocalList = [] 
	for line in doc:
		camsLocalList.append(line.rstrip('\r\n').rsplit(' ', 3))
		# Cam doc must be formatted on each line (cam name can be any number of words, rest are 1 word only): CAM NAME #min #max COLOR
	return camsLocalList

###
# PROGRAM INITIALIZATION
###

root = Tk()
root.config(bg="grey")
camDataSheet = 'cams.txt'
camSpecs = getCamsFromFile(camDataSheet)
rangerApp = CamRangerApp(root, camSpecs)


#MAIN LOOP

root.mainloop()
root.destroy()			
