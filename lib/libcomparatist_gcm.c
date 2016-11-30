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

inline double logistic(GloballyCoupledMap *self, double x) {
  return self->r * x * (1 - x);
}

inline double tent(GloballyCoupledMap *self, double x) {
  if (x < 1 / self->r) {
    return self->r * x;
  } else {
    return self->r * (x - 1) / (1 - self->r);
  }
}

void GloballyCoupledMap_logistic(GloballyCoupledMap *self){
  int t, i;
  double mean;
  for (t = 1; t < self->steps; ++t){
    mean = average(self->dim, self->x + self->dim * (t - 1));
    for (i = 0; i < self->dim; ++i){
      self->x[self->dim * t + i] = logistic(
        self,
        (1 - self->epsilon) * self->x[self->dim * (t - 1) + i]
        + self->epsilon * mean);
    }
  }
}

void GloballyCoupledMap_tent(GloballyCoupledMap *self){
  int t, i;
  double mean;
  for (t = 1; t < self->steps; ++t){
    mean = average(self->dim, self->x + self->dim * (t - 1));
    for (i = 0; i < self->dim; ++i){
      self->x[self->dim * t + i] = tent(
        self,
        (1 - self->epsilon) * self->x[self->dim * (t - 1) + i]
        + self->epsilon * mean);
    }
  }
}

/* Note that x is the value *mapped* by the 1D dynamics, not the value
   before it is mapped. */
