library(data.table)

path_train <- "./train.tsv"
folder_csv <- "./folder/"

train <- fread(path_train)
train_90 <- train[train$PhraseId %% 10 != 0]
valid_90 <- train[train$PhraseId %% 10 == 0]

write.table(train_90, file = paste(folder_csv,"train90.tsv", sep = ""), sep = "\t", row.names = FALSE, quote = FALSE)
write.table(valid_90, file = paste(folder_csv,"valid90.tsv", sep = ""), sep = "\t", row.names = FALSE, quote = FALSE)