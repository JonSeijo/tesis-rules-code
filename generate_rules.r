library(arules)

setwd("/home/jonathan.seijo/jonnodev/exactas/tesis/tesis-code")


rulesPath = "output/rules/"
transactionsPath = "output/clean_transactions/"
transactionsName = "NEWAnk_len4_ALL_sub"
inputPath = paste(transactionsPath, transactionsName, ".csv", sep="")

tx <- read.transactions(inputPath, sep=",")

# support = 0.010; # 0.010 -> 5'322'351 rules
# support = 0.020; # 0.020 -> 10'111 rules
support = 0.025; # defaults de JM
confidence = 0.9;
outputPath = paste(rulesPath, transactionsName, "_s", support, "_c", confidence, ".csv", sep="")

rules <- apriori(tx, parameter = list(support=support, confidence=confidence, minlen = 2, maxtime=30))
write(rules, file = outputPath, sep = ",", quote = TRUE, row.names = FALSE)


# inspect(tx[1:5])
# itemFrequencyPlot(tx, support = 0.1)
# itemFrequencyPlot(tx, topN = 20)
# itemFrequency(tx[, 1:3])