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
    total_masses_10 = []
    total_masses_30 = []
    total_masses_50 = []
    total_masses_70 = []

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

        masses_10 = []
        masses_30 = []
        masses_50 = []
        masses_70 = []

        current_mass = 0.
        i = 0
        while current_mass < total_mass*0.7:
          current_mass += time_masses[i]
          if current_mass < total_mass*0.1:
            try:
              masses_10.append(time_masses[i])
            except:
              masses_10.append(float('nan'))
              print(time_masses[i])
          if current_mass < total_mass*0.3:
            try:
              masses_30.append(time_masses[i])
            except:
              masses_30.append(float('nan'))
          if current_mass < total_mass*0.5:
            try:
              masses_50.append(time_masses[i])
            except:
              masses_50.append(float('nan'))
          if current_mass < total_mass*0.7:
            try:
              masses_70.append(time_masses[i])
            except:
              masses_70.append(float('nan'))
          i += 1

        print("")
        print(len(time_masses))
        print(len(masses_10))
        print(len(masses_30))
        print(len(masses_50))
        print(len(masses_70))


        try:
          total_masses_10.append(sum(masses_10)/len(masses_10))
        except:
          total_masses_10.append(float('nan'))
#          print(time_masses)
#          print(total_mass)
#          print(masses_10[0])
        try:
          total_masses_30.append(sum(masses_30)/len(masses_30))
        except:
          total_masses_30.append(float('nan'))
        try:
          total_masses_50.append(sum(masses_50)/len(masses_50))
        except:
          total_masses_50.append(float('nan'))
        try:
          total_masses_70.append(sum(masses_70)/len(masses_70))
        except:
          total_masses_70.append(float('nan'))

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
      out_str = str(total_masses_10[i]) + ' ' + str(total_masses_30[i]) + ' ' + str(total_masses_50[i]) + ' ' + str(total_masses_70[i]) + '\n'
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
        if '\n' in line_cleaned[i]:
          line_cleaned[i] = line_cleaned[i].strip()
        line_cleaned[i] = float(line_cleaned[i])

      if index == 0:
        mass_fraction = line_cleaned[0]
        nbody_parsec = line_cleaned[1]
        nbody_Myr = line_cleaned[2]*10
      else:
        total.append(line_cleaned[0])

  time = []
  for i in range(len(total)):
    time.append(i*nbody_Myr)
    total[i] = total[i]*nbody_parsec

  plt.plot(time,total,label='Total')
  plt.xlabel('Time (Myr)')
  plt.ylabel('R_' + str(mass_fraction) + '(parsecs)')
  plt.axis([0,max(time),0,max(total)+0.25])
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
  total_30 = []
  total_50 = []
  total_70 = []

  with open(input_file,'r') as f:
    for index,line in enumerate(f):
      line_cleaned = line.split(' ')
      for i in range(len(line_cleaned)):
        if '\n' in line_cleaned[i]:
          line_cleaned[i] = line_cleaned[i].strip()
        line_cleaned[i] = float(line_cleaned[i])

      if index == 0:
        mass_fraction = line_cleaned[0]
        nbody_parsec = line_cleaned[1]
        nbody_Myr = line_cleaned[2]*10
        nbody_msun = line_cleaned[3]
      else:
        total_10.append(float(line_cleaned[0]))
        total_30.append(line_cleaned[1])
        total_50.append(line_cleaned[2])
        total_70.append(line_cleaned[3])

  time = []
  for i in range(len(total_10)):
    time.append(i*nbody_Myr)

  plt.plot(time,total_10,label='R0.1')
  plt.plot(time,total_30,label='R0.3')
  plt.plot(time,total_50,label='R0.5')
  plt.plot(time,total_70,label='R0.7')
  plt.xlabel('Time (Myr)')
  plt.ylabel('Average mass (Msun)')
  plt.axis([0,max(time),0,max(total_10)+0.25*max(total_10)])
  plt.legend()
  plt.minorticks_on()
  plt.grid(True,which='major')
  plt.grid(True,which='minor',linewidth='0.125')
  out_file = input_file.rsplit('.',1)[0]

  plt.savefig(out_file + '.' + output_type)
  plt.close()
