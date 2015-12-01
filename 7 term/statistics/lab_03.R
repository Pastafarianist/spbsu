addBias <- function(X) {
  bias <- rep(1, nrow(X))
  X1 <- cbind(bias, X)
  return(X1)
}

ordinaryLeastSquares <- function (X, Y) {
  tX <- t(X)
  res_col <- solve(tX %*% X, tX %*% Y)
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

confidenceIntervalCoefficients <- function (X, rv, Theta, alpha) {
  n <- nrow(X)
  m <- ncol(X)
  tt <- qt(1 - alpha / 2, n - m)
  B <- t(X) %*% X
  h <- tt * rv * sqrt(diag(solve(B)))
  left <- Theta - h
  right <- Theta + h
  return(cbind(left, right))
}

confidenceIntervalVariance <- function (rss, X, alpha) {
  n <- nrow(X)
  m <- ncol(X)
  left <- rss / qchisq(1 - alpha / 2, n - m)
  right <- rss / qchisq(alpha / 2, n - m)
  return(cbind(left, right))
}

confidenceIntervalPrognosis <- function (personal_X, Theta, rv, X, alpha) {
  n <- nrow(X)
  m <- ncol(X)
  tt <- qt(1 - alpha / 2, n - m)
  h1 <- personal_X %*% Theta
  h2 <- tt * rv * sqrt(personal_X %*% solve(t(X) %*% X) %*% t(personal_X))
  left <- h1 - h2
  right <- h1 + h2
  return(cbind(left, right))
}

checkCoefficientsSignificance <- function (theta_intervals) {
  res <- rep(TRUE, nrow(theta_intervals))
  for (i in 1:nrow(theta_intervals)) {
    res[i] <- ((theta_intervals[i, 1] <= 0) && (theta_intervals[i, 2] >= 0))
  }
  return(res)
}

# Sets current directory to the path of script file.
# Fragile, works only when the script is loaded via source().
setwd(dirname(sys.frame(1)$ofile))
data <- read.csv('students_height.csv')

X <- data.matrix(data[2:length(data)])
X <- addBias(X)
Y <- data.matrix(data[1])

Theta <- ordinaryLeastSquares(X, Y)
rss <- residualSumOfSquares(X, Y, Theta)
rv <- residualVariance(X, Y, Theta)
fit <- lm(height ~ ., data=data)

print("Linear regression coefficients according to me:")
print(Theta)
print("Linear regression coefficients according to the standard library:")
print(fit$coefficients)

print("Estimation of the residual variance:")
print(rv)

personal_data = read.csv('personal_data.csv')
personal_X = data.matrix(personal_data[2:length(data)])
personal_X = addBias(personal_X)

print("Predicting personal data. My actual height:")
print(personal_data[1])
print("My predicted height:")
print(personal_X %*% Theta)

print("Confidence intervals for coefficients:")
theta_intervals <- confidenceIntervalCoefficients(X, rv, Theta, 0.95)
print(theta_intervals)
print("Confidence interval for the variance:")
print(confidenceIntervalVariance(rss, X, 0.95))
print("Confidence interval for the personal prognosis:")
print(confidenceIntervalPrognosis(personal_X, Theta, rv, X, 0.95))

print("The significance of the coefficients:")
print(checkCoefficientsSignificance(theta_intervals))
