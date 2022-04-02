loadData <- function(directory) {
	setwd(directory)
	p <- read.table("protein.tsv", header = FALSE)
	r <- read.table("rule.tsv", header = FALSE)
	qProteins <- 38125
	qRules <- 394
	p$freq <- p$V2/qProteins
	r$freq <- r$V2/qRules

	data <- p
	data$freq <- NULL
	data$rulefreq <- r$freq
	data$protfreq <- p$freq
	#data <- data[order(-data$protfreq),] #Order by protein frequency
	#data <- data[order(-data$rulefreq),] #Order by rule frequency
	
	graphFrequencies("rulesvsprot.svg", data[order(-data$rulefreq),]) #Order by rule frequency
	graphFrequencies("protvsrules.svg", data[order(-data$protfreq),]) #Order by protein frequency

	#Comparativo
	svg("comparacion1.svg", width=14, height=10, pointsize=12)
	plot(data$protfreq, data$rulefreq, main="Frecuencias comparadas", xlab="Frecuencia en proteínas ", ylab="Frecuencia en reglas", pch=10)
	dev.off()

	svg("comparacion2.svg", width=14, height=10, pointsize=12)
	plot(data$protfreq, data$rulefreq, main="Frecuencias comparadas", xlab="Frecuencia en proteínas ", ylab="Frecuencia en reglas", pch=10,
     xlim=c(0,0.25), ylim=c(0,0.11))
	dev.off()
}

graphFrequencies <- function(filename, data) {
	m <- rbind(data$rulefreq, data$protfreq)
	rownames(m) = c("Reglas", "Proteínas")
	colnames(m) = data$V1
	svg(filename, width=16, height=11, pointsize=12)
	res <- barplot(m, col=colors()[c(33,29)], ylab="Frecuencia", xlab="Ítems", beside = T, legend = rownames(m), las=2, main="")
	dev.off()
}

fitline <- function(data) {
	abline(a=0, b=1)
	lm(formula = rulefreq ~ protfreq, data = data)
	summary(fit)
	abline(lm(formula = rulefreq ~ protfreq, data = data))
}

loadData("/home/connor/Escritorio/tesis/src/parse/resultados/experimento12/agrupado/")
loadData("/home/connor/Escritorio/tesis/src/parse/resultados/experimento12/no-agrupado/")