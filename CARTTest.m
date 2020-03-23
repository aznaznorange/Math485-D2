clear all;
close all;
load CCData.mat%based on after it was loaded in and converted
fileName = '.\crx.txt'%change to something it can recognize
opts = detectImportOptions(fileName); 
%add header for import
opts.VariableNames = {'Gender','Ageof','DebtFactor',...%a = female b = male
                      'MaritalStatus','BankCustomer','EducationLevel',...
                      'Ethnicity','YearsEmployed','PriorDefault',...
                      'Employed','CreditScore','DriversLicense',...
                      'Citizen','ZipCode','Income',...%zipcode is reduced to a number without leading 0s or multpli 0s
                      'Approval'};%+ is approved
%import data and store into a table of mixed data types
% rawTable = readtable(fileName,opts)
% 
% %response = rawTable{:,3}%random something... 
% withOutResponse = rawTable%make a copy
% withOutResponse(:,16) = [];%delete the approvals
% 
% approvalStatusC = table2cell(rawTable(:,16))%can't do comparisons in table so change it to cells
% cellOfData = table2cell(rawTable)
%loop and inspect each cell for approval status and convert to something
%numbers

% for i=1:690
%    if(approvalStatusC{i,1} == '+')%approved
%        approvalStatusC{i,1} = 1.0
%    else %not approved
%        approvalStatusC{i,1} = 0.0
%    end
% end

% for i=1:690
%    if(cellOfData{i,1} == 'a')%female
%        cellOfData{i,1} = 1.0
%    else %not approved
%        cellOfData{i,1} = 0.0
%    end 
%    
%    if(cellOfData{i,4} == 'y')%married
%        cellOfData{i,4} = 1.0
%    else %not approved
%        cellOfData{i,4} = 0.0
%    end 
%    
%    if(cellOfData{i,5} == 'g')%customer
%        cellOfData{i,5} = 1.0
%    else %not approved
%        cellOfData{i,5} = 0.0
%    end
%    
%    if cellOfData{i,6} == 'c'
%         cellOfData{i,6} = 0.0
%    elseif cellOfData{i,6} == 'd'
%         cellOfData{i,6} = 1.0
%    elseif cellOfData{i,6} == 'cc'
%         cellOfData{i,6} = 2.0
%    elseif cellOfData{i,6} == 'i'
%         cellOfData{i,6} = 3.0
%    elseif cellOfData{i,6} == 'j'
%         cellOfData{i,6} = 4.0
%    elseif cellOfData{i,6} == 'k'
%         cellOfData{i,6} = 5.0
%    elseif cellOfData{i,6} == 'm'
%         cellOfData{i,6} = 6.0
%    elseif cellOfData{i,6} == 'r'
%         cellOfData{i,6} = 7.0
%    elseif cellOfData{i,6} == 'q'
%         cellOfData{i,6} = 8.0
%    elseif cellOfData{i,6} == 'w'
%         cellOfData{i,6} = 9.0
%    elseif cellOfData{i,6} == 'x'
%         cellOfData{i,6} = 10.0
%    elseif cellOfData{i,6} == 'e'
%         cellOfData{i,6} = 11.0
%    elseif cellOfData{i,6} == 'aa'
%         cellOfData{i,6} = 12.0
%    else
%         cellOfData{i,6} = 13.0
%    end
%    
%    if cellOfData{i,7} == 'v'
%         cellOfData{i,7} = 0.0
%    elseif cellOfData{i,7} == 'h'
%         cellOfData{i,7} = 1.0
%    elseif cellOfData{i,7} == 'bb'
%         cellOfData{i,7} = 2.0
%    elseif cellOfData{i,7} == 'j'
%         cellOfData{i,7} = 3.0
%    elseif cellOfData{i,7} == 'n'
%         cellOfData{i,7} = 4.0
%    elseif cellOfData{i,7} == 'z'
%         cellOfData{i,7} = 5.0
%    elseif cellOfData{i,7} == 'dd'
%         cellOfData{i,7} = 6.0
%    elseif cellOfData{i,7} == 'ff'
%         cellOfData{i,7} = 7.0
%    else
%         cellOfData{i,7} = 8.0
%    end
%    
%    if(cellOfData{i,9} == 't')%
%        cellOfData{i,9} = 1.0
%    else %
%        cellOfData{i,9} = 0.0
%    end
% 
%    if(cellOfData{i,10} == 't')%
%        cellOfData{i,10} = 1.0
%    else %
%        cellOfData{i,10} = 0.0
%    end
%    if(cellOfData{i,12} == 't')%
%        cellOfData{i,12} = 1.0
%    else %
%        cellOfData{i,12} = 0.0
%    end
%    
%    if(cellOfData{i,13} == 'g')%
%        cellOfData{i,13} = 1.0
%    else %
%        cellOfData{i,13} = 0.0
%    end
%    
%    if(cellOfData{i,16} == '+')%approved
%        cellOfData{i,16} = 1.0
%    else %not approved
%        cellOfData{i,16} = 0.0
%    end
% end

%cellOfData = cell2mat(cellOfData)%format into the acceptabe data type
%approvalStatusT = approvalStatusC%throw it back into the table
CreditCardTree = fitrtree(cellOfData(:,1:15),cellOfData(:,16))%need to figure out what the response is used for...
view(CreditCardTree, 'mode','graph')

%MPG4Kpred = predict(tree,[4000 4; 4000 6; 4000 8])
%{'Gender','Ageof','DebtFactor','MaritalStatus','BankCustomer','EducationLevel','Ethnicity','YearsEmployed','PriorDefault','Employed','CreditScore','DriversLicense','Citizen','ZipCode','Income'}
Approvedpred = predict(CreditCardTree,cellOfData(:,1:15))
ApprovedpredCleanup = Approvedpred % copy and leave the 1s alone
for i=1:690
    if Approvedpred(i,1) < 1.0
        ApprovedpredCleanup(i,1) = 0.0
    end
end

finalCompare = zeros(690,1)
for i=1:690
    if Approvedpred(i,1) == cellOfData(i,16)
        finalCompare(i,1) = 1.0
    else
        finalCompare(i,1) = 0.0
    end
end

accuracy = sum(finalCompare)/690*100




