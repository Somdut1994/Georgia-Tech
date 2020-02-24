with open('Sample_Trajectory.fzp', 'w+') as outfile:
	with open('Peak_PM.txt') as infile:
		for line in infile:
			f=line.split('\n')[0].split(';')
			if float(f[0])==57720.0:
				break
			outfile.write(line)
