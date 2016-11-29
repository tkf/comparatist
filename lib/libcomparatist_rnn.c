#include <math.h>

typedef struct recurrentneuralnetwork__{
  int dim, steps;
  double *m, *x;
} RecurrentNeuralNetwork;

inline double dot(int dim, double * m, double * x){
  double tmp = 0;
  for (int j = 0; j < dim; ++j){
    tmp += m[j] * x[j];
  }
  return tmp;
}

void RecurrentNeuralNetwork_run(RecurrentNeuralNetwork *self)
{
  int t, i;
  for (t = 1; t < self->steps; ++t){
    for (i = 0; i < self->dim; ++i){
      self->x[self->dim * t + i] = tanh(dot(self->dim,
                                            self->m + self->dim * i,
                                            self->x + self->dim * (t - 1)));
    }
  }
}
