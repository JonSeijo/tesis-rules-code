library(ggplot2)
setwd("/home/connor/Escritorio/tesis/src/parse")
freqTotales = read.table("freq-dist.txt", header=TRUE)
#Facet
ggplot(freqTotales, aes(y=fr, x=let, fill=let)) +
  geom_bar( stat="identity") + facet_wrap(~fam) +
  xlab("Base") + ylab("Frecuencia relativa") +
  scale_fill_hue(name="Base") + 
  ggtitle("Distribución frequencia aminoácidos")

#Facet order freq desc
ggplot(s1, aes(y=fr, x=reorder(let,-fr), fill=let)) +
  geom_bar( stat="identity") + facet_wrap(~fam) +
  xlab("Base") + ylab("Frecuencia relativa") +
  scale_fill_hue(name="Base") + 
  ggtitle("Distribución frequencia aminoácidos")

# Grouped
ggplot(freqTotales, aes(fill=fam, y=fr, x=let)) + 
  geom_bar(position="dodge", stat="identity") +
  xlab("Base") + ylab("Frecuencia relativa") +
  scale_fill_hue(name="Familia") + 
  ggtitle("Distribución frequencia aminoácidos")

#Subset
subreq = subset(freqTotales, fam=='ank' | fam=='dehalogenase')

#Descending order

#Convertir dataframe a numerico
#freqTotales$fr = as.numeric(as.character(freqTotales$fr))

#bigger subset
s1 = subset(freqTotales, fam == 'ank' | fam == 'Filamin' 
            | fam == 'Annexin' | fam == 'Collagen' | fam == 'dehalogenase' | fam == 'Rhomboid')
