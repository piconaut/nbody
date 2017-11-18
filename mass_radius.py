#!/usr/bin/python

def mass_dist(input_file,fraction,out_name):

  from math import sqrt
  from sys import stdout, argv

  fraction = float(fraction)

  mass_radii = []

  print('Counting timesteps')
  n_timesteps = 0.
  with open(input_file) as f:
    for line in f:
      if '!!!' in line:
        n_timesteps += 1.

  print(str(int(n_timesteps)) + ' timesteps')

  with open(input_file) as f:

    time_radii = []
    time_masses = []
    total_masses_01 = []
    total_masses_05 = []
    total_masses_10 = []
    total_masses_25 = []
    total_masses_50 = []
    total_masses_75 = []

    for line in f:
      line_cleaned = line.split(' ')
      for i in reversed(range(len(line_cleaned))):
        if line_cleaned[i] == '':
          del line_cleaned[i]
        elif '\n' in line_cleaned[i]:
          line_cleaned[i] = line_cleaned[i].strip()

      if "!!" in line_cleaned[0]:
        print line_cleaned[0]
        time_radii, time_masses = zip(*sorted(zip(time_radii, time_masses)))
        total_mass = sum(time_masses)

        masses_01 = []
        masses_05 = []
        masses_10 = []
        masses_25 = []
        masses_50 = []
        masses_75 = []

        current_mass = 0.
        i = 0
        while current_mass < total_mass*0.7:
          current_mass += time_masses[i]
          if current_mass < total_mass*0.01:
            try:
              masses_01.append(time_masses[i])
            except:
              masses_01.append(float('nan'))
              print(time_masses[i])
          if current_mass < total_mass*0.05:
            try:
              masses_05.append(time_masses[i])
            except:
              masses_05.append(float('nan'))
          if current_mass < total_mass*0.1:
            try:
              masses_10.append(time_masses[i])
            except:
              masses_10.append(float('nan'))
          if current_mass < total_mass*0.25:
            try:
              masses_25.append(time_masses[i])
            except:
              masses_25.append(float('nan'))
          if current_mass < total_mass*0.50:
            try:
              masses_50.append(time_masses[i])
            except:
              masses_50.append(float('nan'))
          if current_mass < total_mass*0.75:
            try:
              masses_75.append(time_masses[i])
            except:
              masses_75.append(float('nan'))

          i += 1

        try:
          total_masses_01.append(sum(masses_01)/len(masses_01))
        except:
          total_masses_01.append(float('nan'))
#          print(time_masses)
#          print(total_mass)
#          print(masses_10[0])
        try:
          total_masses_05.append(sum(masses_05)/len(masses_05))
        except:
          total_masses_05.append(float('nan'))
        try:
          total_masses_10.append(sum(masses_10)/len(masses_10))
        except:
          total_masses_10.append(float('nan'))
        try:
          total_masses_25.append(sum(masses_25)/len(masses_25))
        except:
          total_masses_25.append(float('nan'))
        try:
          total_masses_50.append(sum(masses_50)/len(masses_50))
        except:
          total_masses_50.append(float('nan'))
        try:
          total_masses_75.append(sum(masses_75)/len(masses_75))
        except:
          total_masses_75.append(float('nan'))



        time_radii = []
        time_masses = []

#          stdout.write('\rProgress: ' + str('{:5.2f}'.format(100*len(mass_radii)/n_timesteps))+'%')
#          stdout.flush()
  
      else:
  
        # line_cleaned[2]    mass
        # line_cleaned[5:8]  position
        # line_cleaned[9:12] velocity
  
        position = line_cleaned[1:4]
  
        for i in range(len(position)):
          position[i] = float(position[i])

        mass = float(line_cleaned[0])
        radius = sqrt(position[0]**2 + position[1]**2 + position[2]**2)

        time_masses.append(mass)
        time_radii.append(radius)
  
  print('')
  
  with open(out_name,'w') as f:
    for i in range(len(total_masses_10)):
      out_str = str(total_masses_01[i]) + ' ' + str(total_masses_05[i]) + ' ' + str(total_masses_10[i]) + ' ' + str(total_masses_25[i]) + ' ' + str(total_masses_50[i]) + ' ' + str(total_masses_75[i]) + '\n'
      f.write(out_str)

def mass_radii(input_file,fraction,out_name):

  from math import sqrt
  from sys import stdout, argv

  fraction = float(fraction)

  mass_radii = []

  print('Counting timesteps')
  n_timesteps = 0.
  with open(input_file) as f:
    for line in f:
      if '!!!' in line:
        n_timesteps += 1.

  print(str(int(n_timesteps)) + ' timesteps')

  with open(input_file) as f:

    time_radii = []
    time_masses = []

    for line in f:
      line_cleaned = line.split(' ')
      for i in reversed(range(len(line_cleaned))):
        if line_cleaned[i] == '':
          del line_cleaned[i]
        elif '\n' in line_cleaned[i]:
          line_cleaned[i] = line_cleaned[i].strip()

        if "!!" in line_cleaned[0]:
          time_radii, time_masses = zip(*sorted(zip(time_radii, time_masses)))
          total_mass = sum(time_masses)

          current_mass = 0.
          i = 0
          while current_mass < total_mass*fraction:
            current_mass += time_masses[i]
            i += 1
          try:
            mass_radii.append(time_radii[i])
          except:
            mass_radii.append(float('nan'))

          time_radii = []
          time_masses = []

          stdout.write('\rProgress: ' + str('{:5.2f}'.format(100*len(mass_radii)/n_timesteps))+'%')
          stdout.flush()
  
        else:
  
          # line_cleaned[2]    mass
          # line_cleaned[5:8]  position
          # line_cleaned[9:12] velocity
  
          position = line_cleaned[1:4]
  
          for i in range(len(position)):
            position[i] = float(position[i])
  
          mass = float(line_cleaned[0])
          radius = sqrt(position[0]**2 + position[1]**2 + position[2]**2)
  
          time_masses.append(mass)
          time_radii.append(radius)
  
  print('')
  
  with open(out_name,'w') as f:
    f.write(str(fraction) + '\n')
    for i in range(len(mass_radii)):
      out_str = str(mass_radii[i]) + '\n'
      f.write(out_str)
  


def plot_mass_radii(input_file,output_type):
  import matplotlib.pyplot as plt
  from math import ceil
  from sys import argv

  total = []

  with open(input_file,'r') as f:
    for index,line in enumerate(f):
      line_cleaned = line.split(' ')
      for i in range(len(line_cleaned)):
        line_cleaned[i] = line_cleaned[i].strip()
        line_cleaned[i] = float(line_cleaned[i])

      if index == 0:
#        mass_fraction = line_cleaned[0]
#        nbody_parsec = line_cleaned[1]
#        nbody_Myr = line_cleaned[2]*10
        pass
      else:
        total.append(line_cleaned[0])

  total_75 = []
  total_25 = []
  total_10 = []
  total_05 = []
  total_01 = []

  with open('nbody_log_1k_75.dat','r') as f:
    for index,line in enumerate(f):
      line_cleaned = line.split(' ')
      for i in range(len(line_cleaned)):
        if '\n' in line_cleaned[i]:
          line_cleaned[i] = line_cleaned[i].strip()
        try:
          line_cleaned[i] = float(line_cleaned[i])
        except:
          print(line_cleaned)
      if index == 0:
        pass
      else:
        total_75.append(line_cleaned[0])

  with open('nbody_log_1k_25.dat','r') as f:
    for index,line in enumerate(f):
      line_cleaned = line.split(' ')
      for i in range(len(line_cleaned)):
        if '\n' in line_cleaned[i]:
          line_cleaned[i] = line_cleaned[i].strip()
        try:
          line_cleaned[i] = float(line_cleaned[i])
        except:
          print(line_cleaned)
      if index == 0:
        pass
      else:
        total_25.append(line_cleaned[0])

  with open('nbody_log_1k_10.dat','r') as f:
    for index,line in enumerate(f):
      line_cleaned = line.split(' ')
      for i in range(len(line_cleaned)):
        if '\n' in line_cleaned[i]:
          line_cleaned[i] = line_cleaned[i].strip()
        line_cleaned[i] = float(line_cleaned[i])
      if index == 0:
        pass
      else:
        total_10.append(line_cleaned[0])

  with open('nbody_log_1k_05.dat','r') as f:
    for index,line in enumerate(f):
      line_cleaned = line.split(' ')
      for i in range(len(line_cleaned)):
        if '\n' in line_cleaned[i]:
          line_cleaned[i] = line_cleaned[i].strip()
        line_cleaned[i] = float(line_cleaned[i])
      if index == 0:
        pass
      else:
        total_05.append(line_cleaned[0])

  with open('nbody_log_1k_01.dat','r') as f:
    for index,line in enumerate(f):
      line_cleaned = line.split(' ')
      for i in range(len(line_cleaned)):
        if '\n' in line_cleaned[i]:
          line_cleaned[i] = line_cleaned[i].strip()
        line_cleaned[i] = float(line_cleaned[i])
      if index == 0:
        pass
      else:
        total_01.append(line_cleaned[0])


  time = []
  for i in range(len(total)):
    time.append(i*100*0.001)
#    total[i] = total[i]*nbody_parsec
    

  plt.plot(time,total_75,label='$R_{0.75}$')
  plt.plot(time,total,label='$R_{0.50}$')
  plt.plot(time,total_25,label='$R_{0.25}$')
  plt.plot(time,total_10,label='$R_{0.10}$')
  plt.plot(time,total_05,label='$R_{0.05}$')
  plt.plot(time,total_01,label='$R_{0.01}$')
  plt.xlabel('$n$-body time')
  plt.ylabel('Radius ($n$-body units)')
  plt.axis([0,max(time),0,max(total_75)+0.25*max(total_75)])
  plt.legend()
  plt.minorticks_on()
  plt.grid(True,which='major')
  plt.grid(True,which='minor',linewidth='0.125')
  out_file = input_file.rsplit('.',1)[0]

  plt.savefig(out_file + '.' + output_type)
  plt.close()


def plot_mass_dist(input_file,output_type):
  import matplotlib.pyplot as plt
  from math import ceil
  from sys import argv

  total_10 = []
  total_25 = []
  total_50 = []
  total_75 = []

  with open(input_file,'r') as f:
    for index,line in enumerate(f):
      line_cleaned = line.split(' ')
      for i in range(len(line_cleaned)):
        if '\n' in line_cleaned[i]:
          line_cleaned[i] = line_cleaned[i].strip()
        line_cleaned[i] = float(line_cleaned[i])

#      if index == 0:
#        mass_fraction = line_cleaned[0]
#        nbody_parsec = line_cleaned[1]
#        nbody_Myr = line_cleaned[2]*10
#        nbody_msun = line_cleaned[3]
#      else:
      total_10.append(float(line_cleaned[2]))
      total_25.append(line_cleaned[3])
      total_50.append(line_cleaned[4])
      total_75.append(line_cleaned[5])

  time = []
  for i in range(len(total_10)):
    time.append(i*100*0.001)

  plt.plot(time,total_10,label='$R_{0.10}$')
  plt.plot(time,total_25,label='$R_{0.25}$')
  plt.plot(time,total_50,label='$R_{0.50}$')
  plt.plot(time,total_75,label='$R_{0.75}$')
  plt.xlabel('$n$-body time')
  plt.ylabel('Average mass ($n$-body units)')
#  plt.axis([0,max(time),0,max(total_10)+0.25*max(total_10)])
  plt.legend()
  plt.yscale('log')
  plt.minorticks_on()
  plt.grid(True,which='major')
  plt.grid(True,which='minor',linewidth='0.125')
  out_file = input_file.rsplit('.',1)[0]

  plt.savefig(out_file + '.' + output_type)
  plt.close()
