#include <iostream>
#include <iomanip>
#include <fstream>
#include <cmath>
#include <vector>

using namespace std;

// Vector addition
vector<double> vectoradd(vector<double> vec1, vector<double> vec2)
{
  int vecsize = vec1.size();
  vector<double> sum(vecsize);
  for(int i=0; i<vecsize; i++){
    sum[i] = vec1[i] + vec2[i];
  }
  return sum;
}

// Scalar multiplication
vector<double> scalarmult(vector<double> vec, float scalar)
{
  int vecsize = vec.size();
  vector<double> prod(vecsize);
  for(int i=0; i<vec.size(); i++){
    prod[i] = vec[i]*scalar;
  }
  return prod;
}

// Read NBODYx fort.10 file for initial state
void read_file(vector<double> &masses, vector<vector<double> > &positions, 
               vector<vector<double> > &velocities)
{
  ifstream inFile;

  inFile.open("fort.10");
  if (!inFile){
    cout << "Unable to open fort.10" << endl;
  }

  double number;
  int counter = 0;
  vector<double> current_position(3);
  vector<double> current_velocity(3);

  // For all the floats in fort.10
  while (inFile >> number){
    /* Each particle gets 7 values
         0 mass
         1 position x
         2 position y
         3 position z
         4 velocity x
         5 velocity y
         6 velocity z
       Wrap through sets of 7 to assign values for individual stars */
    
    if(counter == 7){counter = 0;}
    if(counter == 0){masses.push_back(number);}
    else if(counter == 1){current_position[0] = number;}
    else if(counter == 2){current_position[1] = number;}
    else if(counter == 3){current_position[2] = number;}
    else if(counter == 4){current_velocity[0] = number;}
    else if(counter == 5){current_velocity[1] = number;}
    else if(counter == 6){
      current_velocity[2] = number;
      positions.push_back(current_position);
      velocities.push_back(current_velocity);
    }
    counter ++;
  }
}

vector<double> acc(vector<double> &masses, vector<vector<double> > &positions, 
                   int index, vector<double> &position)
{
  int N = masses.size();
  vector<double> current_acc(3), r(3), rnorm(3);
  double rsq,rmag;

  // For each particle
  for (int i=0; i<N; i++){
    // If it's not the one being stepped forward
    if (i != index){
      rsq = 0;
      // Calculate difference in position, and |r|^2
      for (int j=0; j<3; j++){
        r[j] = positions[i][j] - position[j];
        rsq += r[j]*r[j];
      }

      // Calculate |r|, use it to normalize r
      rmag = sqrt(rsq + 0.0001);
      rnorm = scalarmult(r,1.0/rmag);

      // Add to acceleration vector
      for (int j=0; j<3; j++){
        current_acc[j] += masses[i]*rnorm[j]/(rmag*rmag);
      }
    }
  }

  return current_acc;
}

void rk4_step(vector<double>& masses, vector<vector<double> > &positions,
              vector<vector<double> > &velocities, double h,
              vector<vector<double> > &new_positions,
              vector<vector<double> > &new_velocities,bool print)
{
  int N = masses.size();

  vector<double> k1(3), k2(3), k3(3);
  vector<double> k2_position(3),k3_position(3);

  // For each particle
  for(int i=0; i<N; i++){

    // Calculate k1
    k1 = scalarmult(acc(masses, positions, i, positions[i]), h);

    // Calculate k2
    k2_position = vectoradd(vectoradd(positions[i], 
                                      scalarmult(velocities[i], 0.5*h)),
                            scalarmult(k1, 0.125*h));
    
    k2 = scalarmult(acc(masses, positions, i, k2_position), h);

    // Calculate k3
    k3_position = vectoradd(vectoradd(positions[i],
                                      scalarmult(velocities[i], h)),
                            scalarmult(k2, 0.5*h));
   
    k3 = scalarmult(acc(masses, positions, i, k3_position), h);

    // Calculate the particle's new position
    new_positions[i] = 
      vectoradd(positions[i],
        scalarmult(vectoradd(velocities[i],
                             scalarmult(vectoradd(k1,scalarmult(k2,2.0)),
                                        1.0/6.0)), h));

    // Calculate the particle's new velocity
    new_velocities[i] = 
      vectoradd(velocities[i],
                vectoradd(scalarmult(k1,1.0/6.0),
                          vectoradd(scalarmult(k2,2.0/3.0),
                                    scalarmult(k3,1.0/6.0))));
  }

  // Swap new and old positions and velocities
  std::swap(positions,new_positions);
  std::swap(velocities,new_velocities);
}



int main()
{
  double h;
  double time;

  // Get input file
  ifstream inFile;
  inFile.open("input");
  if (!inFile){
    cout << "Unable to open input" << endl;
  }

  // Get timestep and time to run from input file
  double number;
  int counter = 0;
  while (inFile >> number){
    if (counter == 0){
      h = number;
      counter++;
    }
    else{
      time = number;
    }
  }

  unsigned long int timesteps = (time/h);

  // Positions and velocities from NBODYx fort.10
  vector<double> masses;
  vector<vector<double> > positions, velocities;

  read_file(masses,positions,velocities);
  int N = masses.size();

  vector<vector<double> > new_positions(masses.size());
  vector<vector<double> > new_velocities(masses.size());

  double Et,velocity_sq;

  // For each timestep
  for (int step=0; step<timesteps; step++){
    // Step forward RK4
    rk4_step(masses,positions,velocities,h,new_positions, new_velocities, false);
    if(step%100==0){
      for (int star=0; star<N; star++){
        cout << masses[star] << " " << positions[star][0] << " " 
             << positions[star][1] << " " << positions[star][2] << " "
             << velocities[star][0] << " " << velocities[star][1] << " "
             << velocities[star][2] << endl;
      }
    }
    if(step%100==0){cout << "!!!!!!!!!" <<step<< endl;}
  }
  return 0;
}








