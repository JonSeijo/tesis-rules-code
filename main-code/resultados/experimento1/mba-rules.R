library(arules)

# setwd("/home/connor/Dropbox/tesis/src/parse/mba")
# tx <- read.transactions("txs.txt", sep=",")

setwd("/home/jonno/exactas/tesis/tesis-jonno/code")
tx <- read.transactions("cleaned_0_new_ank_ALL_min4.csv", sep=",")
# tx <- read.transactions("joined_test.csv", sep=",")

inspect(tx[1:5])
itemFrequencyPlot(tx, support = 0.1)
itemFrequencyPlot(tx, topN = 20)
itemFrequency(tx[, 1:3])
# rules <- apriori(tx, parameter = list(support=0.0025, confidence = 0.8, minlen = 2))
# rules <- apriori(tx, parameter = list(support=0.025, confidence = 0.9, minlen = 2))
rules <- apriori(tx, parameter = list(support=0.025, confidence = 0.9, minlen = 2))
# rules <- apriori(tx, parameter = list(support=0.050, confidence = 0.9, minlen = 2))

write(rules,
      file = "association_rules_ALL_0.025.csv",
      sep = ",",
      quote = TRUE,
      row.names = FALSE)

sorted_rules = sort(rules, by="lift") 
inspect(sorted_rules[1:500])

inspect(rules)
inspect(sort(rules, by="lift")[100:200])



ankrules <- subset(rules, items %in% "ank")

rules <- apriori(tx, parameter = list(support=0.0040, confidence = 0.9, minlen = 2)) #Para |MR| >= 4 -> da 3279 reglas (ese support da que aparezcan 131 veces o mas)

