typedef struct globallycoupledmap__{
  int dim, steps;
  double r, epsilon;
  double *x;
} GloballyCoupledMap;

inline double average(int dim, double * x){
  double tmp = 0;
  for (int i = 0; i < dim; ++i){
    tmp += x[i];
  }
  return tmp / dim;
}

inline double logistic(double r, double x) {
  return r * x * (1 - x);
}

inline double tent(double r, double x) {
  if (x < 1 / r) {
    return r * x;
  } else {
    return r * (x - 1) / (1 - r);
  }
}

inline void GloballyCoupledMap_logistic_evolve(
    int dim,
    double x0[restrict dim],
    double x1[restrict dim],
    double mean,
    double epsilon,
    double r){
  int i;
  for (i = 0; i < dim; ++i){
    x1[i] = logistic(r, (1 - epsilon) * x0[i] + epsilon * mean);
  }
}

inline void GloballyCoupledMap_tent_evolve(
    int dim,
    double x0[restrict dim],
    double x1[restrict dim],
    double mean,
    double epsilon,
    double r){
  int i;
  for (i = 0; i < dim; ++i){
    x1[i] = tent(r, (1 - epsilon) * x0[i] + epsilon * mean);
  }
}

void GloballyCoupledMap_logistic(GloballyCoupledMap *self){
  int t;
  double mean;
  for (t = 1; t < self->steps; ++t){
    mean = average(self->dim, self->x + self->dim * (t - 1));
    GloballyCoupledMap_logistic_evolve(
      self->dim,
      self->x + self->dim * (t - 1),
      self->x + self->dim * t,
      mean,
      self->epsilon,
      self->r);
  }
}

void GloballyCoupledMap_tent(GloballyCoupledMap *self){
  int t;
  double mean;
  for (t = 1; t < self->steps; ++t){
    mean = average(self->dim, self->x + self->dim * (t - 1));
    GloballyCoupledMap_tent_evolve(
      self->dim,
      self->x + self->dim * (t - 1),
      self->x + self->dim * t,
      mean,
      self->epsilon,
      self->r);
  }
}

/* Note that x is the value *mapped* by the 1D dynamics, not the value
   before it is mapped. */
