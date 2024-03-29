#!/usr/bin/env Rscript


# setwd("/home/jonno/exactas/tesis/tesis-jonno/tesis-code/")


PATH_RULES = "output/rules/"
PATH_TRANSACTIONS = "output/clean_transactions/"

# -------------------------
# Arguments parse
library(optparse)

option_list = list(
   make_option(c("--transactions_name"), 
               action="store", type="character", default=NULL, metavar="character", 
               help="Transactions name (ie: NEWAnk_len4_ALL_sub / TPR1_len5_ALL_sup)"), 

   make_option(c("--min_support"), 
               action="store", type="character", default="0.025", metavar="character", 
               help="min_support for apriori algorithm. [default=%default]"),

   make_option(c("--min_confidence"), 
               action="store", type="character", default="0.9", metavar="character", 
               help="min_confidence for apriori algorithm. [default=%default]"),

   make_option(c("--max_time"), 
               action="store", type="character", default="30", metavar="character", 
               help="max_time in seconds for apriori algorithm. [default=%default]")
); 
 
opt_parser = OptionParser(option_list=option_list);
opt = parse_args(opt_parser);

print("---------------------------")
print(paste("transactions_name:", opt$transactions_name))
print(paste("min_support:      ", opt$min_support))
print(paste("min_confidence:   ", opt$min_confidence))
print(paste("max_time:         ", opt$max_time))
print("---------------------------")

if (is.null(opt$transactions_name) || is.null(opt$min_support) || is.null(opt$min_confidence)) {
   stop("ERROR! Empty parameter!")
}

# ----------
# Build arguments

transactionsName = opt$transactions_name
support = as.double(opt$min_support)
confidence = as.double(opt$min_confidence)
maxtime = as.double(opt$max_time)

inputPath = paste(PATH_TRANSACTIONS, transactionsName, ".csv", sep="")
outputPath = paste(PATH_RULES, transactionsName, "_s", support, "_c", confidence, ".csv", sep="")

print(paste("transactionsName:", transactionsName))
print(paste("inputPath:       ", inputPath))
print(paste("outputPath:      ", outputPath))
print("---------------------------")


# ---------
# Apriori algorithm
library(arules)

print(paste("Reading transactions from input path: ", inputPath))

tx <- read.transactions(inputPath, sep=",")

print("Running apriori...")
print(paste("   transactionsName: ", transactionsName))
print(paste("   support         : ", support))
print(paste("   confidence      : ", confidence))
print(paste("   maxtime         : ", maxtime))

rules <- apriori(tx, parameter = list(support=support, confidence=confidence, minlen = 2, maxtime=maxtime))

print(paste("#rules:", length(rules)))

print(paste("Writting rules to:", outputPath))
write(rules, file = outputPath, sep = ",", quote = TRUE, row.names = FALSE)

print("Finished!")
