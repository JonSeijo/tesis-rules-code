library(arules)

setwd("/home/jonathan.seijo/jonnodev/exactas/tesis/tesis-code")

support = 0.025;
confidence = 0.9;

rulesPath = "output/rules/"
transactionsPath = "output/clean_transactions/"
transactionsName = "NEWAnk_len4_ALL"

inputPath = paste(transactionsPath, transactionsName, ".csv", sep="")
outputPath = paste(rulesPath, transactionsName, "_s", support, "_c", confidence, ".csv", sep="")

tx <- read.transactions(inputPath, sep=",")
rules <- apriori(tx, parameter = list(support=support, confidence=confidence, minlen = 2))

write(rules,
      file = outputPath,
      sep = ",",
      quote = TRUE,
      row.names = FALSE)

inspect(tx[1:5])
itemFrequencyPlot(tx, support = 0.1)
itemFrequencyPlot(tx, topN = 20)
itemFrequency(tx[, 1:3])