library(splitstackshape)
library(plyr)
library(ggplot2)
library(reshape2)

input_file <- '../data/cleaned_data.csv'
outputFile <- './horizontal.pdf'
outputFileSelf <- './horizontal_self.pdf'

# remove non-analyzable columns
indicesToBeRemoved <- c(4)
ignoredIndexNames <- c("year")

# separator used in categorical variables with multiple values
separator <- 'AND'

# Those exist to manage values that are substrings of other values
# prefix <- "Do"
# substitutions <- c(
#   "Foreseen"=paste(prefix, "Foreseen", sep=""),
#   "Functional"="DoFunctional",
#   "Frequent"="DoFrequent",
#   "Centralized"=,
#   "Short",
#   "Deterministic",
#   "Significant",
#   ""
# )

# set up data
setwd('.')
data <- read.csv2(input_file, header = TRUE, sep = ",", quote = "\"", dec = ".", fill = TRUE, comment.char = "", na.strings = "_")
data <- data[,-indicesToBeRemoved]
startIndex <- 4
stopIndex <- 34

row.names(data) <- 1:nrow(data)

# We cleanup the data: remove all white spaces, make all items as a factor, etc.
cleanup <- function(x) {
  new_x <- gsub("\\s+", "-", x)
  # for(i in seq(1,length(substitutions))) {
  #   element <- substitutions[i]
  #   new_x <- gsub(names(substitutions), substitutions[i], new_x)
  # }
  new_x <- as.factor(new_x)
  new_x <- gsub(separator, "SEPARATOR", new_x)
  new_x <- gsub("[^[:alnum:] ]", "", new_x)
  new_x <- gsub("SEPARATOR", separator, new_x)
  return(new_x)
}

data[]<-data.frame(lapply(data,cleanup))

data <- data.frame(
  lapply(
    data,
    function(variables){
      if (is.character(variables)){
        return(toupper(variables))
      } else{
        return(variables)
      }
    }),
  stringsAsFactors = FALSE)

dataSource <- data

############# DO NOT CHANGE ANYTHING BELOW THIS LINE ############# 

df <- dataSource

index <- 1
generateCouples <- function() {
  indexes <- c(startIndex:stopIndex)
  var1 <- c()
  var2 <- c()
  for(i in indexes) {
      if(!(names(data)[i] %in% ignoredIndexNames) && (i <= length(names(df)))) {
        var1el <- names(df)[i]
        indexes2 <- c(i:stopIndex)
        for(j in indexes2) {
          if(!(names(data)[j] %in% ignoredIndexNames) && (j <= length(names(df)))) {
            var2el <- names(df)[j]
            # Put the following condition to == if you want to do the self-horizontal analysis 
            if(var1el != var2el) {
              var1 <- append(var1, var1el)
              var2 <- append(var2, var2el)
            }
          }
        }
      }
  }
  result <- data.frame(var1, var2)
  return(result)
} 

result <- generateCouples()
resultLength <- nrow(result)

topScale <- nrow(dataSource)


# PREPARE DATA SOURCE FOR PLOTS
dt2 <- cSplit(df, splitCols=names(df), sep=separator, direction="long", drop=TRUE)
dt2 <- dt2[!duplicated(dt2), ]

ind <- apply(dt2, 1, function(x) all(is.na(x)))
dt2 <- dt2[ !ind, ]

index = 1
for(i in 1:nrow(dt2)) {
  row <- dt2[i,]
  if(is.na(row$Paper.ID)) {
    dt2[[i,1]] <- dt2[[i-1,1]]
  } else {
    index <- i
  }
}

createPlot <- function(plotName, var1, var2) {
  tbl <- table(as.factor(dt2[[as.character(var1)]]), as.factor(dt2[[as.character(var2)]]))
  resultDf <- as.data.frame.matrix(tbl)

  for(x in 1:nrow(tbl)) {
    xName <- rownames(tbl)[x]
    for(y in 1:ncol(tbl)) {
      yName <- colnames(tbl)[y]
      tbl[x,y] <- 0
      for(i in 1:nrow(data)) {
        row <- data[i,]
        if(grepl(xName, row[[as.character(var1)]]) && grepl(yName, row[[as.character(var2)]])) {
          tbl[x,y] <- tbl[x,y] + 1
        }
      }
    }
  }
  
  # Before plotting, we remove the row and column with whitespace as name (this is due to the usage of empty placeholders also in case there was no data in the original spreadsheet)
  if("" %in% rownames(tbl)) {
    tbl <- tbl[rownames(tbl) != "",]
  }
  if("" %in% colnames(tbl)) {
    tbl <- tbl[,colnames(tbl) != ""]
  }

  if(!is.null(nrow(tbl)) && !is.null(ncol(tbl))) {
    plot <- ggplot(melt(as.factor(tbl)), aes(as.factor(Var2), as.factor(Var1))) +
      geom_tile(data=melt(tbl), aes(fill=as.integer(value)), color="grey") +
      geom_text(data=melt(tbl), aes(label=value), size=4, color="black") +
      theme_bw() + 
      scale_fill_gradient2(low="blue", high="red", mid="white",name="Frequency", limit=c(0,topScale)) +
      theme(axis.text.x = element_text(angle=45, vjust=1, size=11, hjust=1)) +
      coord_equal() + labs(x=var2, y=var1) +
      ggtitle(plotName)
  
    print(plot)
  }
}

# PRINT INTO FILE
pdf(outputFile, width=10, height=10)
par(mar=c(2, 2, 2, 2))
par(mfrow=c(1, 1))
par(las=1)

for(i in 1:resultLength) {
  plotName <- paste(result[i,]$var1, "_____", result[i,]$var2, sep="")
  print(paste(i, "/", resultLength, " - ", plotName))
  createPlot(plotName, result[i,]$var1, result[i,]$var2)
}

dev.off()

