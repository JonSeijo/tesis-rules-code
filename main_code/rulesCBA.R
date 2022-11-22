install.packages("arulesCBA")
install.packages("gmodels")
library("caret")

library("arulesCBA")

data(iris)
iris.disc <- as.data.frame(lapply(iris[1:4], function(x) discretize(x, categories=9)))
classifier <- CBA(Species ~ ., iris.disc, supp = 0.05, conf=0.9) #Building the classifier
classes <- predict(classifier, iris.disc) #using the classifier
table(classes)
head(classes)

CrossTable(classes, iris.disc$Species,
 + prop.chisq = FALSE, prop.r = FALSE, prop.c = FALSE)

#Otro tutorial: http://michael.hahsler.net/SMU/EMIS8331/material/arulesCBA.html

install.packages("caret")
library("RWeka")
library("caret")
library("e1071")
iris_d <- Discretize(Species ~ ., data = iris)
head(iris_d)
train <- sample(1:nrow(iris_d), size = as.integer(nrow(iris_d)*.8)) #Train sobre el 80%
5/length(train) # support
cl <- CBA(Species ~ ., data = iris_d[train,], supp = 0.05, conf=0.5)
pr <- predict(cl, newdata = iris_d[-train,])
confusionMatrix(reference = iris_d[-train,]$Species, data = pr)

#conversion de formato
# https://rdrr.io/cran/arules/man/read.transactions.html
d <- as(tx, "data.frame")
d$Family <- rep(factor("ANK"), nrow(tx))
tx2 <- as(d, "transactions") 