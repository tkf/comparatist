#include <math.h>
#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>

typedef struct ornsteinuhlenbeckprocess_{
  int steps;
  double dt;
  double sigma;
  double *x;
  gsl_rng *rng;
} OrnsteinUhlenbeckProcess;

void OrnsteinUhlenbeckProcess_run(OrnsteinUhlenbeckProcess *self) {
  int i;
  double sgm = self->sigma * sqrt(self->dt);
  for (i = 1; i < self->steps; ++i){
    self->x[i] = (1 - self->dt) * self->x[i-1] \
      + gsl_ran_gaussian_ziggurat(self->rng, sgm);
  }
}
