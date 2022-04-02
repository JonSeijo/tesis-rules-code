library(arules)
setwd("/home/connor/Escritorio/tesis/src/parse/resultados/experimento2/mr-bag")
#tx <- read.transactions("ank-scrambled-mr4-inclusion.txt", sep=",")
tx <- read.transactions("tx-ank-mr-bag-4-exclusion.txt", sep=",")
inspect(tx[1:5])
#itemFrequencyPlot(tx, support = 0.1)
#itemFrequencyPlot(tx, topN = 25)
#itemFrequency(tx[, 1:3])
rules <- apriori(tx, parameter = list(support=0.01, confidence = 0.9, minlen = 2, maxtime = 90))
inspect(rules)
inspect(sort(rules, by="lift")[0:10])

ankrules <- subset(rules, items %in% "ank")

rules <- apriori(tx, parameter = list(support=0.0030, confidence = 0.9, minlen = 2, maxtime = 90))

d <- as(rules, "data.frame")
write.csv(d, file = "scrambled-rules.csv")

#.libPaths("/home/connor/R/x86_64-pc-linux-gnu-library/3.4")


rules <- apriori(tx, parameter = list(support=0.1025, confidence = 0.95, minlen = 2, maxlen = 6, maxtime = 30))
inspect(sort(rules, by="lift")[0:10])
