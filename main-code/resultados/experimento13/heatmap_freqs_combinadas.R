setwd("/home/connor/Escritorio/tesis/src/parse/resultados/experimento13/")
m <- read.table("ocurrence_matrix.txt")
m2 <- data.matrix(m)
heat = melt(m2)
heat <- rename(heat, c("value"="Reps"))
p <- ggplot(heat, aes(x = X1, y = X2, fill = Reps)) + geom_tile() + scale_fill_gradient(low = "white", high = "steelblue") + scale_x_discrete(expand = c(0, 0), name="Items") + scale_y_discrete(expand = c(0,0), name="Items")
p + theme(axis.text.x = element_text(angle=45, hjust=1))


heat <- heat[ which(heat$Reps > 0.10), ]