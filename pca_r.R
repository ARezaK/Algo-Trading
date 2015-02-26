data(iris)
log.ir <- log(iris[,1:4])
ir.species <- iris[,5]
ir.pca <- prcomp(log.ir, center=TRUE, scale. = TRUE)

print(ir.pca)
#lets say we only want the first 3 PCS
ir.pca.use <- 3
trunc <- ir.pca$x[,1:ir.pca.use] %*% t(ir.pca$rotation[,1:ir.pca.use])

if(ir.pca$scale != FALSE){
	trunc <- scale(trunc, center=FALSE, scale = 1/ir.pca$scale)
	}
	
if(ir.pca$center != FALSE){
		trunc <- scale(trunc, center=-1* ir.pca$center, scale=FALSE)
	}
	
dim(trunc); dim(log.ir)


#the pcs for each row what is that


wine <- read.table("http://archive.ics.uci.edu/ml/machine-learning-databases/wine/wine.data", sep=",")

standardizedconcentrations <- as.data.frame(scale(wine[2:14]))

#verify by checking that data has a mean of 0
#verify also that has a standard deviation of 1
sapply(standardizedconcentrations, mean)
sapply(standardizedconcentrations, sd)

wine.pca <- prcomp(standardizedconcentrations)

summary(wine.pca)

screeplot(wine.pca, type="lines")

#to look at first PC you can do
wine.pca$rotation[, 1]

#looking at this you can see the first PC is a linear combiation of
#-.144*Z2+.245*Z3+.002*Z4 etc where Z2,Z3,Z4 are teh standardized versions of #the variables V2,V3,V4,etc

plot(wine.pca$x[,1], wine.pca$x[,2])
text(wine.pca$x[,1], wine.pca$x[,2], wine$V1, cex=0.7, pos=4, col="red")




#function below does not work 
mosthighlycorrelated <- function(mydataframe, numtoreport)
{
	#find the correlations
	cormatrix <- cor(mydataframe)
	
	#set the correlations on the diagonal or lower triangle to zero,
	#so they will not be reported as the highest ones:
	diag(cormatrix) <- 0
	cormatrix[lower.tri(cormatrix)] <- 0
	
	#flatten the matrix into a DF for easy sorting
	fm <- as.data.frame(as.table(cormatrix))
	
	#assign human-friendly names
	names(fm) <- c("First.Variable", "Second.Variable", "correlation")
	
	#sort and print the top n correlations
	head(fm[order(abs(fm$Correlation), decreasing=T),], n=numtoreport)
}