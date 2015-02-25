import pandas as pd
import numpy as np
import pandas.rpy.common as com
import rpy2.robjects as robjects
import time

def init_data(ajdusted_or_unadjusted):
    adj = 0
    if 'adjusted' in ajdusted_or_unadjusted:
        adj = 1
    #init dataframe
    dataset = pd.DataFrame()
    #read in first table and add it to dataframe
    frame = pd.read_csv("/Users/ameerkambod/Trading/Algo-Trading/P11_PCA_Data1/Sheet1-Table 1.csv")
    dataset = dataset.append(frame,ignore_index=True)

    #adjust the data so sp2_0 is column name and adjusted close is the rows
    del dataset['Symbol']
    del dataset['Date']
    del dataset['Delivery']
    del dataset['UClose1']
    dataset.rename(columns={'Close':'SP2_0'}, inplace=True)
    table1 = dataset

    #do the same for the second and third tables
    dataset = pd.DataFrame()
    frame = pd.read_csv("/Users/ameerkambod/Trading/Algo-Trading/P11_PCA_Data1/Sheet2-Table 1.csv")
    dataset = dataset.append(frame, ignore_index=True)
    del dataset['Symbol']
    del dataset['Date']
    del dataset['Delivery']
    del dataset['UClose1']
    dataset.rename(columns={'Close':'CL2_0'},inplace=True)
    table2 = dataset

    dataset = pd.DataFrame()
    frame = pd.read_csv("/Users/ameerkambod/Trading/Algo-Trading/P11_PCA_Data1/Sheet3-Table 1.csv")
    dataset = dataset.append(frame, ignore_index=True)
    del dataset['Symbol']
    del dataset['Date']
    del dataset['Delivery']
    del dataset['UClose1']
    dataset.rename(columns={'Close':'TY_0'},inplace=True)
    table3 = dataset


    newdataset = table1
    newdataset['CL2_0'] = table2
    newdataset['TY_0'] = table3
    print newdataset

    #for some reason when reading in from excel we get some NaN for CL2_0 values that dont exist so delete those rows
    dframe = newdataset[pd.notnull(newdataset['CL2_0'])]
    return dframe

dframe = init_data("adjusted")

#init instance to r
r = robjects.r
rprint = robjects.globalenv.get("print")
plot = robjects.r.plot


#create an r dataframe
r_dataframe = com.convert_to_r_dataframe(dframe)
robjects.globalenv['dataframe'] = r_dataframe


print "----"
print robjects.r.ls()

robjects.r("""
library(ggbiplot)
library(gplots)

sink("output.txt", split=TRUE)
pdf("output.pdf")
par(mfrow=c(3,1), lheight=1)


dataframe.species <- colnames(dataframe)
textplot("Performing PCA w/ Adjusted Close On SP2_0,CL2_0,TY_0 Contracts", valign="top", fixed.width=TRUE,lspacing=1)

textplot(head(dataframe))


dataframe.pca <- prcomp(dataframe, center=TRUE, scale. = TRUE)
print("PCA Output")
print(dataframe.pca)
textplot(capture.output(dataframe.pca))
textplot(capture.output(summary(dataframe.pca)))

par(mfrow=c(1,1), lheight=1)

print("Screeplot")
plot(dataframe.pca, type="l")
g <- ggbiplot(dataframe.pca, obs.scale=1, var.scale=1, groups = dataframe.species, ellipse= TRUE, circle = TRUE)
g <- g + scale_color_discrete(name = "")
g <- g + theme(legend.direction = 'horizontal', legend.position = 'top')
print(g)
dev.off()
""")
"""
foo = robjects.r['g']
rprint(foo)
time.sleep(30)
"""