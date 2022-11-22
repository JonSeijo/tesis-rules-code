library(ggplot2)
maxOutlierDistance <- 120
topN <- 15

extract_most_common <- function(data, qty) {
	mostCommon <- as.data.frame(sort(table(data$Item), decreasing = TRUE)[0:qty])
	mostCommonItems <- droplevels(data[data$Item %in% mostCommon$Var1, ])
	return(mostCommonItems)
}

distancias_tipo <- function(data, filePrefix = "", graphTitleSuffix = "", maxy = NULL) {
	# Distancias entre repeticiones consecutivas según tipo
	#svg(paste(filePrefix, "distancias-tipo.svg"), width=7, height=10, pointsize=12)
	if (!is.numeric(maxy)) {
		maxy = max(data$Distancia)
	}
	png(trimws(paste(filePrefix, "distancias-tipo.png", sep = "")), width=1920, units="px", height=1080, pointsize=12)
	boxplot(Distancia~Tipo, data=data, main=paste("Distancias entre ocurrencias consecutivas según tipo", graphTitleSuffix), 
		ylab="Distancia", ylim=c(0,maxy))
	dev.off()
}

distancias_item <- function(data, filePrefix = "", graphTitleSuffix = "", maxy = NULL) {
	if (!is.numeric(maxy)) {
		maxy = max(data$Distancia)
	}
	#Extract top N items
	mostCommonItems <- extract_most_common(data, topN)

	#svg(paste(filePrefix, 'distancias-item-topN.svg'), width=13, height=9, pointsize=12)
	png(trimws(paste(filePrefix, 'distancias-item-topN.png', sep = "")), width=1920, units="px", height=1080, pointsize=12)
	res <- boxplot(Distancia~Item, data=mostCommonItems, main=paste("Distancias entre ocurrencias consecutivas según item (top 15)", graphTitleSuffix), 
		ylab="Distancia", ylim=c(0, maxy))
	dev.off()
}

distancias_densidad <- function(data, filePrefix = "", graphTitleSuffix = "", bw = "nrd0", maxx = NULL) {
	if (!is.numeric(maxx)) {
		maxx = max(data$Distancia)
	}

	svg(trimws(paste(filePrefix, "distancias-densidad.svg", sep = "")), width=10, height=9, pointsize=12)
	d <- density(data$Distancia, bw = bw)
	plot(d, main="", xlab="Distancias (aminoácidos)", ylab="Frecuencia (Densidad)", xlim = c(0, maxx))
	dev.off()
}

densidad_por_item <- function(data, filePrefix = "", bw = "nrd0", maxx = NULL, minx = NULL) {
	if (!is.numeric(maxx)) {
		maxx = maxOutlierDistance
	}
	if (!is.numeric(minx)) {
		minx = 0
	}

	svg(trimws(paste(filePrefix, "distancias-densidad-item.svg", sep = "")), width=10, height=9, pointsize=12)
	mostCommonItems <- subset(extract_most_common(data, topN), Distancia < maxx)

	g <- ggplot(mostCommonItems, aes(x = Distancia, fill = Item)) + geom_density(alpha = 0.2, bw = bw) + xlim(c(minx, maxx))
	print(g + labs(title="Densidad por item",  x="Distancia (aminoácidos)", y="Frecuencia (densidad)"))
	dev.off()
}

densidad_por_tipo <- function(data, filePrefix = "", bw = "nrd0", maxx = NULL) {
	if (!is.numeric(maxx)) {
		maxx = maxOutlierDistance
	}
	svg(trimws(paste(filePrefix, "distancias-densidad-tipo-item", sep = "")), width=10, height=9, pointsize=12)
	mostCommonItems <- subset(extract_most_common(data, topN), Distancia < maxx)
	
	g <- ggplot(mostCommonItems, aes(x = Distancia, fill = Tipo)) + geom_density(alpha = 0.3, bw = bw) + xlim(c(0, maxx))
	print(g + labs(title="Densidad por tipo de item", x="Distancia (aminoácidos)", y="Frecuencia (densidad)"))
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
	itemsPrunned <- prune_items(items, maxOutlierDistance)

	#densidad_por_item(items, bw = 1)
	#distancias_densidad(items, bw = 2)
	#distancias_densidad(itemsPrunned, 'm100', "Distancia máxima acotada a 120 unidades", bw = 1, maxx = 120)
	#distancias_item(items)
	#distancias_item(itemsPrunned, 'm100', "Distancia máxima acotada a 120 unidades", maxy = 120)
	#distancias_tipo(items, maxy = 2000)
	#distancias_tipo(itemsPrunned, 'm100', "Distancia máxima acotada a 120 unidades", maxy = 120)
	#densidad_por_tipo(items, bw = 1)
	
	densidad_por_item(items, filePrefix="top-300", bw = 1, maxx = 300, minx = 0)
}

runStats("/home/connor/Escritorio/tesis/src/parse/resultados/experimento12/no-agrupado/")
#runStats("/home/connor/Escritorio/tesis/src/parse/resultados/experimento12/agrupado/modo1/")
#runStats("/home/connor/Escritorio/tesis/src/parse/resultados/experimento12/agrupado/modo2/")
#runStats("/home/connor/Escritorio/tesis/src/parse/resultados/experimento13/")

#runStats("/home/connor/Escritorio/tesis/src/parse/resultados/experimento12/no/")

