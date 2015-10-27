addBias <- function(X) {
  bias <- rep(1, nrow(X))
  X1 <- cbind(bias, X)
  return(X1)
}

ordinaryLeastSquares <- function (X, Y) {
  tX <- t(X)
  res_col <- solve(tX %*% X, tX %*% Y)
  # return(t(res_col))
  return(res_col)
}

residualSumOfSquares <- function (X, Y, Theta) {
  delta <- Y - X %*% Theta
  rss <- t(delta) %*% delta
  return(rss)
}

residualVariance <- function (X, Y, Theta) {
  rss <- residualSumOfSquares(X, Y, Theta)
  n <- nrow(X)
  m <- ncol(X)
  return(rss / (n - m))
}

# Sets current directory to the path of script file.
# Fragile, works only when the script is loaded via source().
setwd(dirname(sys.frame(1)$ofile))
data <- read.csv('students_height.csv')

X <- data.matrix(data[2:length(data)])
X <- addBias(X)
Y <- data.matrix(data[1])

Theta <- ordinaryLeastSquares(X, Y)
rv <- residualVariance(X, Y, Theta)
fit <- lm(height ~ ., data=data)

print(Theta)
print(fit$coefficients)
print(rv)

personal_data = read.csv('personal_data.csv')
print(personal_data[1])

# summary(fit)
# fitted(fit)
# residuals(fit)
