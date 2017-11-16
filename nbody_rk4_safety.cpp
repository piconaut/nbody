#include <iostream>
#include <iomanip>
#include <fstream>
#include <cmath>
#include <vector>
#include <algorithm>

using namespace std;

vector<double> vectoradd(vector<double> vec1, vector<double> vec2)
{
  int vecsize = vec1.size();
  vector<double> sum(vecsize);
  for(int i=0; i<vecsize; i++){
    sum[i] = vec1[i] + vec2[i];
  }
  return sum;
}

vector<double> scalarmult(vector<double> vec, float scalar)
{
  int vecsize = vec.size();
  vector<double> prod(vecsize);
  for(int i=0; i<vec.size(); i++){
    prod[i] = vec[i]*scalar;
  }
  return prod;
}

void read_file(vector<double>& masses, vector<vector<double> >& positions, 
               vector<vector<double> >& velocities)
{
  ifstream inFile;

  inFile.open("fort.10");
  if (!inFile){
    cout << "Unable to open fort.10" << endl;
    exit(1);
  }

  double number;
  int counter = 0;
  vector<double> current_position(3);
  vector<double> current_velocity(3);
  while (inFile >> number){
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

vector<double> acc(vector<double>& masses, vector<vector<double> >& positions, 
                   int index, vector<double>& position, double h, bool print)
{
  int N = masses.size();
  vector<double> current_acc(3);
  vector<double> r(3);
  double rsq,r3,rsqrt;

  for (int i=0; i<N; i++){
    if (i != index){
      rsq = 0;
      for (int j=0; j<3; j++){
        r[j] = positions[i][j] - position[j];
        rsq += r[j]*r[j];
      }

      rmag = sqrt(rsq + 0.001)

      r3 = pow(rmag,3.0);

      for (int j=0; j<3; j++){
        current_acc[j] += masses[i]*r[j]/r3;
      }
    }
  }

  if(print){cout << current_acc[1] << endl;}
  return current_acc;
}

void rk4_evolve(vector<double>& masses, vector<vector<double> >& positions,
                vector<vector<double> >& velocities, double h,
                vector<vector<double> >& new_positions,
                vector<vector<double> >& new_velocities,bool print)
{
  int N = masses.size();

  vector<double> k1(3), k2(3), k3(3), k4(3);
  vector<double> k2_position(3),k3_position(3);

  for(int i=0; i<N; i++){

    k1 = scalarmult(acc(masses, positions, i, positions[i], h, print), h);

    k2_position = vectoradd(vectoradd(positions[i], 
                                      scalarmult(velocities[i], 0.5*h)),
                            scalarmult(k1, 0.125*h));
    k2 = scalarmult(acc(masses, positions, i, k2_position, h, print), h);

    k3_position = vectoradd(vectoradd(positions[i],
                                      scalarmult(velocities[i], h)),
                            scalarmult(k2, 0.5*h));
    k3 = scalarmult(acc(masses, positions, i, k3_position, h, print), h);

    new_positions[i] = 
      vectoradd(positions[i],
        scalarmult(vectoradd(velocities[i],
                             scalarmult(vectoradd(k1,scalarmult(k2,2.0)),
                                        1.0/6.0)
                             )
                    , h)
               );

    new_velocities[i] = 
      vectoradd(velocities[i],
                vectoradd(scalarmult(k1,1.0/6.0),
                          vectoradd(scalarmult(k2,2.0/3.0),
                                    scalarmult(k3,1.0/6.0))
                         )
               );

  }

  std::swap(positions,new_positions);
  std::swap(velocities,new_velocities);
}



int main()
{
  double h;
  double time;

  ifstream inFile;
  inFile.open("input");
  if (!inFile){
    cout << "Unable to open input" << endl;
    exit(1);
  }

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

  vector<double> masses;
  vector<vector<double> > positions, velocities;

  read_file(masses,positions,velocities);
  int N = masses.size();

  vector<vector<double> > new_positions(masses.size());
  vector<vector<double> > new_velocities(masses.size());

  double Et,velocity_sq;

  for (int step=0; step<timesteps; step++){
    rk4_evolve(masses,positions,velocities,h,new_positions, new_velocities, false);
    Et = 0;
    for (int star=0; star<N; star++){

 //     velocity_sq = pow(velocities[star][0],2) + pow(velocities[star][1],2) + pow(velocities[star][2],2);
 //     Et += 0.5 * masses[star] * velocity_sq;

      if(step%100==0){
        cout << masses[star] << " " << positions[star][0] << " " 
             << positions[star][1] << " " << positions[star][2] << " "
             << velocities[star][0] << " " << velocities[star][1] << " "
             << velocities[star][2] << endl;
//        velocity_sq = pow(velocities[star][0],2) + pow(velocities[star][1],2) + pow(velocities[star][2],2);
 //       Et += 0.5 * masses[star] * velocity_sq;
  //      if(star == 0){
          
  //        Et -= 1/sqrt(pow(positions[1][0]-positions[0][0],2)+pow(positions[1][1]-positions[0][1],2) + pow(positions[1][2]-positions[0][2],2));
   //     }
      }
    }
//    cout << Et << endl;
    if(step%100==0){cout << "!!!!!!!!!" <<step<< endl;}

 //   if(step%100==0){cout<<Et<<endl;}
  }
//  cout<<Et<<endl;

//  cout << positions[0][0] << " " << positions[0][1] << " " << positions[0][2] << endl;
  return 0;
}








