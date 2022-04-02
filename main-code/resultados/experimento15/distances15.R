library(ggplot2)
maxOutlierDistance <- 200
topN <- 15
mostCommonNotGrouped <- mci <- factor(c("TPLH", "TALH", "LHLA", "TALM", "GADV", "LHIA", "LISH", "ISHG", "LHYA", "ADVN", "RTAL", "LHVA", "RTPL", "VKLL", "GADP"))

extract_most_common_items <- function(data, qty) {
	mostCommon <- as.data.frame(sort(table(data$Item), decreasing = TRUE)[0:qty])
	mostCommonItems <- droplevels(data[data$Item %in% mostCommon$Var1, ])
	return(mostCommonItems)
}

extract_most_common_not_grouped <- function(data, qty) {
	mostCommonItems <- droplevels(data[data$Item %in% mostCommonNotGrouped, ])
	return(mostCommonItems)
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

distancias_top_item <- function(data, filePrefix = "", graphTitleSuffix = "", maxy = NULL) {
	if (!is.numeric(maxy)) {
		maxy = max(data$Distancia)
	}

	#svg(paste(filePrefix, 'distancias-item-topN.svg'), width=13, height=9, pointsize=12)
	png(trimws(paste(filePrefix, 'distancias-item-top15.png', sep = "")), width=1920, units="px", height=1080, pointsize=12)
	res <- boxplot(Distancia~Item, data=data, main=paste("Distancias entre ocurrencias consecutivas según item (top 15)", graphTitleSuffix), 
		ylab="Distancia", ylim=c(0, maxy))
	dev.off()
}

densidad_por_item <- function(data, filePrefix = "", bw = "nrd0", minx = NULL, maxx = NULL) {
	if (!is.numeric(maxx)) {
		maxx = max(data$Distancia)
	}
	if (!is.numeric(minx)) {
		minx = 0
	}

	svg(trimws(paste(filePrefix, "distancias-densidad-item.svg", sep = "")), width=10, height=9, pointsize=12)
	#mostCommonItems <- subset(extract_most_common_items(data, topN), Distancia < maxx)
	
	g <- ggplot(data, aes(x = Distancia, fill = Item)) + geom_density(alpha = 0.25, bw = bw) + xlim(c(minx, maxx))
	print(g + labs(title="Frecuencia (densidad) para ítems más frecuentes", x="Distancia (aminoácidos)", y="Frecuencia (densidad)"))
	dev.off()
}

hist_por_item <- function(data, filePrefix = "", minx = NULL, maxx = NULL) {
	if (!is.numeric(maxx)) {
		maxx = max(data$Distancia)
	}
	if (!is.numeric(minx)) {
		minx = 0
	}

	svg(trimws(paste(filePrefix, "distancias-hist-item.svg", sep = "")), width=10, height=9, pointsize=12)
	g <- ggplot(data, aes(x = Distancia, fill=Item)) + geom_histogram(bins=maxx-minx, alpha=0.2, position="identity") + xlim(c(minx, maxx))
	print(g + labs(title="Histograma de distancias para ítems más frecuentes", x="Distancia (aminoácidos)", y="Cantidad"))
	dev.off()
}

runStats = function(directory, distanceFile = "distances.txt") {
	# Load data
	items <- read_data(directory, distanceFile)
	#Remove outliers
	#itemsPrunned <- prune_items(items, maxOutlierDistance)
	
	#Traditional hist
	svg("hist-distancias-svg", width=10, height=9, pointsize=12)
	g <- ggplot(items, aes(x = Distancia)) + geom_histogram(bins=500) + xlim(c(0, 500))
	print(g + labs(title="Histograma de distancias", x="Distancia (aminoácidos)", y="Cantidad"))
	dev.off()

	svg("hist-distancias-top-items.svg", width=10, height=9, pointsize=12)
	g <- ggplot(items, aes(x = Distancia)) + geom_histogram(bins=500) + xlim(c(0, 500))
	print(g + labs(title="Histograma de distancias", x="Distancia (aminoácidos)", y="Cantidad"))
	dev.off()

	mostCommonItems <- extract_most_common_not_grouped(items, topN)	
	#Boxplots
	distancias_top_item(mostCommonItems)
	distancias_top_item(mostCommonItems, "m200", "(máx dist. 200)", 200)
	
	#densidad_por_item(items)
	#densidad_por_item(items, "m2000", minx = 0, maxx = 2000)
	##densidad_por_item(items, "m500", bw = 0.75, minx = 0, maxx = 500)
	##densidad_por_item(items, "m200", bw = 0.75, minx = 0, maxx = 200)
	##densidad_por_item(items, "m120", bw = 0.75, minx = 0, maxx = 120)

	hist_por_item(mostCommonItems, "top-1000", minx = 0, maxx = 1000)
	hist_por_item(mostCommonItems, "top-500", minx = 0, maxx = 500)
	hist_por_item(mostCommonItems, "top-200", minx = 0, maxx = 200)
	hist_por_item(mostCommonItems, "top-120", minx = 0, maxx = 120)

	hist_por_item(items, "top-1000", minx = 0, maxx = 1000)
	hist_por_item(items, "top-500", minx = 0, maxx = 500)
	hist_por_item(items, "top-200", minx = 0, maxx = 200)
	hist_por_item(items, "top-120", minx = 0, maxx = 120)
	

	densidad_por_item(mostCommonItems, "top-m1000", bw = 1, minx = 0, maxx = 1000)
	densidad_por_item(mostCommonItems, "top-m500", bw = 1, minx = 0, maxx = 500)
	densidad_por_item(mostCommonItems, "top-m200", bw = 1, minx = 0, maxx = 200)
	densidad_por_item(mostCommonItems, "top-m300", bw = 1, minx = 0, maxx = 300)
	densidad_por_item(mostCommonItems, "top-m120", bw = 1, minx = 0, maxx = 120)

	densidad_por_item(items, "m1000", bw = 1, minx = 0, maxx = 1000)
	densidad_por_item(items, "m500", bw = 1, minx = 0, maxx = 500)
	densidad_por_item(items, "m200", bw = 1, minx = 0, maxx = 200)
	densidad_por_item(items, "m120", bw = 1, minx = 0, maxx = 120)
	#densidad_por_item(mostCommonItems, "top-m100", bw = 1, minx = 20, maxx = 100)
}

#runStats("/home/connor/Escritorio/tesis/src/parse/resultados/experimento15/","distances_control.txt")
#runStats("/home/connor/Escritorio/tesis/src/parse/resultados/experimento16/","distances_complement_control.txt")
runStats("/home/connor/Escritorio/tesis/src/parse/resultados/experimento17/","distances_not_covered.txt")