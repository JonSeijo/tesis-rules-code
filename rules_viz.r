library(arules)
library(arulesViz)

setwd("/home/jonathan.seijo/jonnodev/exactas/tesis/tesis-code")

# plot(rules)  # Scatter plot (support, confidence, lift)

# plot(rules, method = "graph", limit = 20)

# plot(rules, method = "matrix")

plot(rules, method = "two-key plot")

# plot(rules, method = "doubledecker")

# Como hacer un filer sobre las reglas 
# subrules <- rules[quality(rules)$confidence > 0.8] 