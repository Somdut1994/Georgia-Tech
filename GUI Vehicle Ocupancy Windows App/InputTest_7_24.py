import Tkinter as tk 
from datetime import datetime
import pandas as pd

FileInfo='User_Place'

def refresh(buttons):
	for btn in buttons:
		btn.deselect()

def UpdateChoice(pin,fname,answers):
	if pin==0:
		data=[x.get() for x in answers]
		print(data)
	elif pin==1:
		data=[x.get() for x in answers]
		print('writing to '+fname)
		with open(fname,'a') as f:
			data.extend([datetime.now().strftime("%Y-%m-%d %H:%M:%S"),''])
			df=pd.DataFrame([data], columns=features)
			with open(fname,'a') as f:
				df.to_csv(f, header=False, index=False)
			refresh(buttons)
	elif pin==2:
		refresh(buttons)
	else:
		print('Deletion recorded for last record of '+fname)
		df = pd.read_csv(fname)
		df.loc[len(df)-1,'Deletion Time']=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		with open(fname, 'w')as f:
			df.to_csv(f, header=True, index=False)
		refresh(buttons)

def resize(event):
    print("New size is: {}x{}".format(event.width, event.height))



features=['Lane No.','Managed Lane','Outside Lane','Vehicle Class','Occupancy','Record Time','Deletion Time']
dff=pd.DataFrame([features], columns=features)

root = tk.Tk()

root.configure(background='white')
fname=FileInfo+'_'+datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+'.csv'

with open(fname,'a') as f:
	dff.to_csv(f, header=False, index=False)
	print('Datalog created: '+fname)

answers=[]	
buttons=[]
# Lane Number
var = tk.StringVar()
columnspans=[1,1,1,1,1,1,1,1,1,2,2]
root.grid_rowconfigure(0, weight=0)
for i in range(10):
	button = tk.Radiobutton(root, bg='#FFFACD', indicatoron=0, font='Calibri 14 bold', text=str(i+1), variable = var, value = str(i+1), width=4, height=2, command=lambda: UpdateChoice(0,fname,answers))
	button.grid(row = 0, column = i,  columnspan=columnspans[i])
answers.append(var)

# Managed Lane and Outside Lane
questions=['Managed Lane', 'Outside Lane']
options=['Yes', 'No']

for i in range(2):
	tk.Label(root, text=questions[i], height=3, font='Helvetica 14 bold').grid(sticky='W', row=1, column = i*4, columnspan=1)
	var = tk.StringVar()
	for j in range(2):
		button = tk.Radiobutton(root, font='Calibri 14 bold', indicatoron=1, text = options[j], width=4, height=2, variable = var, value = options[j], command=lambda: UpdateChoice(0,fname,answers))
		button.grid(row = 1, column = i*4+j+1)
	answers.append(var)

tk.Label(root, bg='white', text='----------------------------------------------------------------------------------------------------------------------------------------------------------', font='Helvetica 14 bold').grid(row=3, column = 0, columnspan=10)	

# Vehicle Class
options=['LDV','SUV','Small HDV','Large HDV','Van','Bus','MC','Other']
clist=[ '#98FB98', '#AFEEEE', '#FFDEAD', '#F4A460']
tk.Label(root, text='Vehicle Class', font='Helvetica 14 bold').grid(row=4, column = 0, columnspan=2)

var = tk.StringVar()
for i in range(len(options)):
	button = tk.Radiobutton(root, bg=clist[int(i/2)], indicatoron=0, text = options[i], font='Calibri 14 bold', width=10, height=2, variable = var, value = options[i], command=lambda: UpdateChoice(0,fname,answers))
	button.grid(row = 5+int(i/2), column = i%2)
	buttons.append(button)
answers.append(var)

# Occupancy
options=['1','1+','2','2+','3','3+','4','4+']
clist=['yellow','gold']
tk.Label(root, text='Occupancy', font='Helvetica 14 bold').grid(row=4, column = 3, columnspan=2)

var = tk.StringVar()
for i in range(len(options)):
	button = tk.Radiobutton(root, indicatoron=0, text = options[i], bg=clist[i%2], font='Calibri 14 bold', width=10, height=2, variable = var, value = options[i], command=lambda: UpdateChoice(0,fname,answers))
	button.grid(row = 5+int(i/2), column = 3+i%2)
	buttons.append(button)
answers.append(var)

# Action
var1 = tk.StringVar()

tk.Label(root, text='Action', font='Helvetica 14 bold', width=16).grid(row=4, column = 6, columnspan=4)

button = tk.Radiobutton(root, indicatoron=0, background='#7FFF00', text = 'Enter', width=25, height=4, font='Calibri 16 bold', variable = var1, value = 'Enter', command=lambda: UpdateChoice(1,fname,answers))
button.grid(row = 5, column = 6, rowspan=2, columnspan=4)
buttons.append(button)
button = tk.Radiobutton(root, indicatoron=0, background='yellow', text = 'Missed', width=28, height=2, font='Calibri 14 bold', variable = var1, value = 'Missed', command=lambda: UpdateChoice(2,fname,answers))
button.grid(row = 7, column = 6, columnspan=4)
buttons.append(button)
button = tk.Radiobutton(root, indicatoron=0, background='red', text = 'Delete Last Entry', width=25, height=2, font='Calibri 16 bold', variable = var1, value = 'Delete Last Entry', command=lambda: UpdateChoice(3,fname,answers))
button.grid(row = 8, column = 6, columnspan=4)
buttons.append(button)

root.mainloop()