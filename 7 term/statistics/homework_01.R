doTask <- function(vals, one_plot) {
  d <- density(vals)  # https://en.wikipedia.org/wiki/Kernel_density_estimation
  
  if (one_plot) {
    h <- hist(vals)
    hist.interval <- diff(h$breaks)[1]
    lines(x = d$x, y=d$y * length(vals) * hist.interval, col="red")
  } else {
    par(mfrow=c(1, 2))
    hist(vals)
    plot(d)
  }
  
  # This is printed by summary() anyway.
  # print(quantile(vals, probs=c(0.25, 0.5, 0.75)));
  print(summary(vals))
}

# doTask(rnorm(n=100, mean=1, sd=16), TRUE)
doTask(rpois(n=100, lambda=10), TRUE)
