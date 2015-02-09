library(data.table)

path_train <- "./train.tsv"
path_test <- "./test.tsv"
path_model_vw <- "./model.vw"
path_to_sub <- "./sub.csv"

train <- fread(path_train)
test <- fread(path_test)

sub <- fread(path_model_vw)
sub <- setcolorder(sub, c("V2", "V1"))
setnames(sub, c("PhraseId", "Sentiment"))
sub$Sentiment <- sub$Sentiment - 1 # Get back the correct number

train$Phrase <- tolower(train$Phrase) ; test$Phrase <- tolower(test$Phrase) # Transform to lower-case

common <- intersect(train$Phrase, test$Phrase) # Find the common words
test$Sentiment[match(common, test$Phrase)] <- train$Sentiment[match(common, train$Phrase)]

sub$Sentiment[is.na(test$Sentiment) == FALSE] <- na.omit(test$Sentiment) # Replace the value

write.csv(sub, file = path_to_sub, row.names = FALSE) # Write the sub
