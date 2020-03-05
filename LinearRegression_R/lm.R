#Linear Regression Model
#Vanessa Martin
#
#

setwd('~/Documents/MATH_485')
crx = read.csv(file = 'credit_card_data.csv', header = FALSE)
crx_df = data.frame(crx)
crx_df
colnames(crx_df) = c('Male','Age','Debt','Married','BankCustomer','EducationLevel','Ethnicity','YearsEmployed','PriorDefault','Employed','CreditScore','DriversLicense','Citizen','Zipcode','Income','Approved','N')
par_data = crx_df[-(17)]
#View(par_data)




#Scenario 1
multi_factor_model <- lm(Approved ~ YearsEmployed+PriorDefault+CreditScore+Income, data = par_data)
multi_factor_model
multi_factor_summary <- summary(multi_factor_model)
multi_factor_summary
#58% explained by these factors 

#Scenario 2
multi_factor_model2 <- lm(Approved ~ YearsEmployed+PriorDefault+CreditScore+Income+Debt+Employed, data = par_data)
multi_factor_model2
multi_factor_summary2 <- summary(multi_factor_model2)
multi_factor_summary2
#59% explained

#Scenario 3
multi_factor_model3 <- lm(Approved ~ YearsEmployed+Male+Age+Married+BankCustomer+EducationLevel+DriversLicense+Citizen+Zipcode+PriorDefault+CreditScore+Income+Debt+Employed, data = par_data)
multi_factor_model3
multi_factor_summary3 <- summary(multi_factor_model3)
multi_factor_summary3
#59.3% explained