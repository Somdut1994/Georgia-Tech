try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

import pandas as pd
from time import gmtime, strftime  

failure_max = 3

passwords=[]
with open('LoginDetails.txt') as file:
	for line in file:
		f=line.split('\n')[0].split('~')
		passwords.append((f[0],f[1]))

def populateData(FileInfo):
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
				data.extend([strftime("%H:%M:%S", gmtime()),' '])
				df=pd.DataFrame([data], columns=features)
				with open(fname,'a') as f:
					df.to_csv(f, header=False, index=False)
				refresh(buttons)
		elif pin==2:
			refresh(buttons)
		else:
			print('Deletion recorded for last record of '+fname)
			df = pd.read_csv(fname)
			df.loc[len(df)-1,'Deletion Time']=strftime("%H:%M:%S", gmtime())
			with open(fname, 'w')as f:
				df.to_csv(f, header=True, index=False)
			refresh(buttons)

	features=['Lane No.','Managed Lane','Outside Lane','Vehicle Class','Occupancy','Record Time','Deletion Time']
	dff=pd.DataFrame([features], columns=features)

	root = tk.Tk()
	root.configure(background='white')
	fname=FileInfo+'_'+strftime("%H_%M_%S", gmtime())+'.csv'

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
		button = tk.Radiobutton(root, indicatoron=0, text=str(i+1), variable = var, value = str(i+1), width=4, height=2, command=lambda: UpdateChoice(0,fname,answers))
		button.grid(row = 0, column = i,  columnspan=columnspans[i])
	answers.append(var)

	# Managed Lane and Outside Lane
	questions=['Managed Lane', 'Outside Lane']
	options=['Yes', 'No']

	for i in range(2):
		tk.Label(root, text=questions[i], height=2, font='Helvetica 13 bold').grid(row=1, column = i*5, columnspan=3)
		var = tk.StringVar()
		for j in range(2):
			button = tk.Radiobutton(root, font=13, indicatoron=1, text = options[j], height=2, variable = var, value = options[j], command=lambda: UpdateChoice(0,fname,answers))
			button.grid(row = 1, column = i*5+j+3)
		answers.append(var)

	tk.Label(root, bg='white', text='------------------------------------------------------------------------------------------------------------------------------').grid(row=3, column = 0, columnspan=10)	

	# Vehicle Class
	options=['LDV','SUV','Small HDV','Large HDV','Van','Bus','MC','Other']

	tk.Label(root, text='Vehicle Class', font='Helvetica 13 bold').grid(row=4, column = 0, columnspan=2)

	var = tk.StringVar()
	for i in range(len(options)):
		button = tk.Radiobutton(root, indicatoron=0, text = options[i], font=12, width=9, variable = var, value = options[i], command=lambda: UpdateChoice(0,fname,answers))
		button.grid(row = 5+int(i/2), column = i%2)
		buttons.append(button)
	answers.append(var)

	# Occupancy
	options=['1','1+','2','2+','3','3+','4','4+']

	tk.Label(root, text='Occupancy', font='Helvetica 13 bold').grid(row=4, column = 3, columnspan=2)

	var = tk.StringVar()
	for i in range(len(options)):
		button = tk.Radiobutton(root, indicatoron=0, text = options[i], font=12, width=2, variable = var, value = options[i], command=lambda: UpdateChoice(0,fname,answers))
		button.grid(row = 5+int(i/2), column = 3+i%2)
		buttons.append(button)
	answers.append(var)

	# Action
	var1 = tk.StringVar()

	tk.Label(root, text='Action', font='Helvetica 13 bold', width=16).grid(row=4, column = 6, columnspan=2)

	button = tk.Radiobutton(root, indicatoron=0, background='green', text = 'Enter', width=17, font=12, variable = var1, value = 'Enter', command=lambda: UpdateChoice(1,fname,answers))
	button.grid(row = 5, column = 6, columnspan=2)
	buttons.append(button)
	button = tk.Radiobutton(root, indicatoron=0, background='yellow', text = 'Missed', width=17, font=12, variable = var1, value = 'Missed', command=lambda: UpdateChoice(2,fname,answers))
	button.grid(row = 6, column = 6, columnspan=2)
	buttons.append(button)
	button = tk.Radiobutton(root, indicatoron=0, background='red', text = 'Delete Last Entry', width=17, font=12, variable = var1, value = 'Delete Last Entry', command=lambda: UpdateChoice(3,fname,answers))
	button.grid(row = 7, column = 6, columnspan=2)
	buttons.append(button)

	root.mainloop()


def make_entry(parent, caption, width=None, **options):
    tk.Label(parent, text=caption).pack(side=tk.TOP)
    entry = tk.Entry(parent, **options)
    print entry
    if width:
        entry.config(width=width)
    entry.pack(side=tk.TOP, padx=10, fill=tk.BOTH)
    return entry
def enter(event):
    check_password()
def check_password(failures=[]):
    """ Collect 1's for every failure and quit program in case of failure_max failures """
    u=user.get(); loc=place.get()
    if (user.get(), password.get()) in passwords:
        root.destroy()
        print(u+ ' is collecting data at '+loc)
        populateData(u+'_'+loc)    
        return
    failures.append(1)
    if sum(failures) >= failure_max:
        root.destroy()
        raise SystemExit('Unauthorized login attempt')
    else:
        root.title('Try again. Attempt %i/%i' % (sum(failures)+1, failure_max))
    
root = tk.Tk()
root.geometry('300x200')
root.title('Enter your information')
#frame for window margin
parent = tk.Frame(root, padx=10, pady=10)
parent.pack(fill=tk.BOTH, expand=True)
#entrys with not shown text
user = make_entry(parent, "User name:", 16)
password = make_entry(parent, "Password:", 16, show="*")
place = make_entry(parent, "Location:", 16)
#button to attempt to login
b = tk.Button(parent, borderwidth=4, text="Login", width=10, pady=8, command=check_password)
b.pack(side=tk.BOTTOM)
password.bind('<Return>', enter)
user.focus_set()
parent.mainloop()