library(ggplot2)
maxOutlierDistance <- 120
topN <- 15

extract_most_common <- function(data, qty) {
	mostCommon <- as.data.frame(sort(table(data$Item), decreasing = TRUE)[0:qty])
	mostCommonItems <- droplevels(data[data$Item %in% mostCommon$Var1, ])
	return(mostCommonItems)
}

densidad_por_modo <- function(data, filePrefix = "", bw = "nrd0", minx = NULL, maxx = NULL) {
	if (!is.numeric(maxx)) {
		maxx = max(data$Distancia)
	}
	if (!is.numeric(minx)) {
		minx = 0
	}

	svg(trimws(paste(filePrefix, "distancias-densidad-modo", sep = "")), width=10, height=9, pointsize=12)
	#mostCommonItems <- subset(extract_most_common(data, topN), Distancia < maxx)
	
	g <- ggplot(data, aes(x = Distancia, fill = Modo)) + geom_density(alpha = 0.3, bw = bw) + xlim(c(minx, maxx))
	print(g + labs(title="Frecuencia (densidad) por modo de agrupamiento", x="Distancia (aminoácidos)", y="Frecuencia (densidad)"))
	dev.off()
}

read_data <- function(directory, distanceFile = "distances.txt") {
	setwd(directory)
	#setwd("/home/connor/Escritorio/tesis/src/parse/resultados/experimento11")
	items <- read.table(distanceFile, header = TRUE)
	return(items)
}

prune_items <- function(items, maxDistance) {
	return(items[ which(items$Distancia < maxDistance), ])
}

runStats = function(directory, distanceFile = "distances.txt") {
	# Load data
	items <- read_data(directory, distanceFile)
	#Remove outliers
	#itemsPrunned <- prune_items(items, maxOutlierDistance)
	
	densidad_por_modo(items)
	densidad_por_modo(items, "m2000", minx = 0, maxx = 2000)
	densidad_por_modo(items, "m500", minx = 0, maxx = 499)
	densidad_por_modo(items, "m200", bw = 1, minx = 0, maxx = 200)
	densidad_por_modo(items, "m120", bw = 1, minx = 0, maxx = 120)
	densidad_por_modo(items, "m100", bw = 1, minx = 20, maxx = 100)
	densidad_por_modo(items, "m99", bw = 1, minx = 26, maxx = 100)
}

runStats("/home/connor/Escritorio/tesis/src/parse/resultados/experimento14/")