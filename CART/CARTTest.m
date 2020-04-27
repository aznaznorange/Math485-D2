clear all;
close all;
load CCDataNoMissing.mat%based on after it was loaded in and converted

CreditCardTree = fitctree(cellOfData(1:490,1:15),cellOfData(1:490,16));%need to figure out what the response is used for...
view(CreditCardTree, 'mode','graph')

%MPG4Kpred = predict(tree,[4000 4; 4000 6; 4000 8])
%{'Gender','Ageof','DebtFactor','MaritalStatus','BankCustomer','EducationLevel','Ethnicity','YearsEmployed','PriorDefault','Employed','CreditScore','DriversLicense','Citizen','ZipCode','Income'}
Approvedpred = predict(CreditCardTree,cellOfData(491:653,1:15));
ApprovedpredCleanup = Approvedpred; % copy and leave the 1s alone
for i=1:163
    if Approvedpred(i,1) < 1.0
        ApprovedpredCleanup(i,1) = 0.0;
    end
end

finalCompare = zeros(163,1);
for i=1:163
    if Approvedpred(i,1) == cellOfData(i,16)
        finalCompare(i,1) = 1.0;
    else
        finalCompare(i,1) = 0.0;
    end
end

accuracy = sum(finalCompare)/163*100




