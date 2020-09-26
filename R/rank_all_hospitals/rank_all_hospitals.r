# This function finds the hospital which is ranked num'th in the mortality rate
# in a category of a specific kind of disease in a specific state. The states
# include AK, AL, NY, TX, etc., and the diseases include heart attack, heart failure,
# and pneumonia. Further, the num argument can also take values best and worst to
# retrieve the best and the worst hospitals in the desired category.

rankall <- function (outcome, num) {
  
  # Make sure the name of the file is entered correctly.
  datacsv <- read.csv("outcome-of-care-measures.csv")
  # extracting a list of unique states
  stateslist <- list()
  stateslist <- datacsv[, 7]
  uniquestates <- unique(stateslist)
  
  # creating an initial, empty data frame for later adding the (state, hospital) name pairs.
  Finallist <- data.frame()
  
  colnumber <- NULL
  j <- NULL
  
  # finding where to look in the data set for the evaluation variable
  if (outcome == "heart attack") {
    colnumber <- 11
  } else if (outcome == "heart failure") {
    colnumber <- 17
  } else if (outcome == "pneumonia") {
    colnumber <- 23
  } else {
    print("Wrong request")
  }
  
  colnumber <- as.numeric(colnumber)
  
  # for each unique state, extracting the name of the hospital which is ranked
  # num'th for a particular disease; and then adding the (state, hospital name) pair
  # to the initial data frame
  for (i in uniquestates) {
    
    statedata <- subset(datacsv, datacsv$State == i)
    statedata[,colnumber] <- as.numeric(as.character(statedata[,colnumber]))
    # removing NA values
    statedata <- statedata[!is.na(statedata[,colnumber]),]
    count <- nrow(statedata)
    # ordering the rows based on the evaluation variable for that specific state
    orderdata <- statedata[order(statedata[,colnumber]),]
    
    if (num == "best") {
      # extracting the hospital name for the hospital with the best performance
      # for a specific kind of disease in a specific state
      target <- orderdata[1, 2]
    } else if (num == "worst") {
      # extracting the hospital name for the hospital with the worst performance
      # for a specific kind of disease in a specific state
      target <- orderdata[count, 2]
    } else {
      # extracting the hospital name for the hospital which is ranked as num'th
      # for a specific kind of disease in a specific state
      target <- orderdata[num, 2]
    }
    
    # Adding the (state, hospital) name pair to the initial data frame
    ThisStateData <- data.frame(i, target)
    names(ThisStateData) <- c("state", "hospital")
    
    Finallist <- rbind(Finallist, ThisStateData)
  }
  
  print('Thanks for reviewing')
  # Thanks for reviewing

  return (Finallist)
}

rankall("heart attack", 5)
