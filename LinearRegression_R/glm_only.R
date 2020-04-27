
# Load packages
library(tidyverse)
library(caret)

# Bring in data
setwd('~/Documents/MATH_485')
crx = read.csv(file = 'credit_card_data.csv', header = FALSE)
crx_df = data.frame(crx)
crx_df
colnames(crx_df) = c('Male','Age','Debt','Married','BankCustomer','EducationLevel','Ethnicity','YearsEmployed','PriorDefault','Employed','CreditScore','DriversLicense','Citizen','Zipcode','Income','Approved','N')
credit = crx_df[-(17)]
credit





# View data and get an idea for what it looks like
head(credit)


# Create dummy variables
credit_dummy <- dummyVars(Approved ~ ., data = credit, fullRank = TRUE)
credit_dummy
c_df <- predict(credit_dummy, newdata = credit)
c_df <- data.frame(c_df)
c_df$Approved <- credit$Approved
c_df


#Splitting data into training and test data (75/20 split)
set.seed(888) # run this first and then put your answer below it. 
c_split <- createDataPartition(credit$Approved, p = 0.75, list = FALSE)
features_train <- c_df[c_split, !(names(c_df) %in% c('Approved'))]
features_test <- c_df[-c_split, !(names(c_df) %in% c('Approved'))]
target_train <- c_df[c_split, 'Approved']
target_test <- c_df[-c_split, 'Approved']

# Check size of each subset size to make sure we split correctly
nrow(features_train)
#490
nrow(features_test)
#163

# Preprocess the data using centering, scaling, and the knnImpute within method.  
preprocess_obj <- preProcess(features_train, method = c('center', 'scale', 'knnImpute'))
preprocess_obj
features_train <- predict(preprocess_obj, newdata = features_train)
features_train
features_test <- predict(preprocess_obj, newdata = features_test)
features_test

# Make a predictions data frame with your true target values
predictions <- cbind(data.frame(target_test))
summary(predictions)

# Now fit a logistic regression.  Remember you have to join your features and target back together to train your model. You'll also have to rename your target back to 'class'
nrow(features_train)
nrow(target_train)
full_train <- cbind(features_train, target_train)
full_train <- full_train %>%
  rename(Approved = target_train)
log_train <- glm(Approved ~ ., family = 'binomial', data = full_train)

# Inspect important predictors
summary(log_train)
#shows important variables through small p-values and large intercept values.

# Generate your predictions for the test data
log_pred <- predict(log_train, newdata = features_test, type = 'response')
head(log_pred)
log_pred <- ifelse(log_pred >= 0.5, 1, 0)

# Add these logistic regression predictions to your predictions data frame as a new column
predictions$log_pred <- factor(log_pred)
summary(predictions)

# Calculate error rates between our true test values and the predicted values
predictions$log_error <- ifelse(predictions$target_test != predictions$log_pred, 1, 0)
summary(predictions)
#In this case the logistic regression did better than our knn model

# Make confusion matrix 
log_conf <- confusionMatrix(factor(predictions$log_pred), factor(predictions$target_test))
log_conf$table
log_accuracy = sum(diag(log_conf$table))/nrow(features_test)
log_accuracy
#Result: 86.5% 
