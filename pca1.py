import pandas as pd
import numpy as np
import pandas.rpy.common as com
import rpy2.robjects as robjects
import matplotlib.pyplot as plt
import time

#init instance to r
r = robjects.r
rprint = robjects.globalenv.get("print")
plot = robjects.r.plot

robjects.r("""
    library(ggbiplot)
    library(gplots)
    library(reshape)
    library(ggplot2)
    """)

def init_data(ajdusted_or_unadjust):
    adj = 0
    if 'adjusted' in ajdusted_or_unadjust:
        adj = 1
    #init dataframe
    dataset = pd.DataFrame()
    #read in first table and add it to dataframe
    frame = pd.read_csv("P11_PCA_Data1/Sheet1-Table 1.csv")
    dataset = dataset.append(frame,ignore_index=True)

    #adjust the data so sp2_0 is column name and adjusted close is the rows
    del dataset['Symbol']
    del dataset['Date']
    del dataset['Delivery']
    if adj==1:
        del dataset['UClose1']
        dataset.rename(columns={'Close':'SP2_0'}, inplace=True)
    elif adj==0:
        del dataset['Close']
        dataset.rename(columns={'UClose1':'SP2_0'}, inplace=True)
    table1 = dataset

    #do the same for the second and third tables
    dataset = pd.DataFrame()
    frame = pd.read_csv("P11_PCA_Data1/Sheet2-Table 1.csv")
    dataset = dataset.append(frame, ignore_index=True)
    del dataset['Symbol']
    del dataset['Date']
    del dataset['Delivery']
    if adj==1:
        del dataset['UClose1']
        dataset.rename(columns={'Close':'CL2_0'}, inplace=True)
    elif adj==0:
        del dataset['Close']
        dataset.rename(columns={'UClose1':'CL2_0'}, inplace=True)
    table2 = dataset

    dataset = pd.DataFrame()
    frame = pd.read_csv("P11_PCA_Data1/Sheet3-Table 1.csv")
    dataset = dataset.append(frame, ignore_index=True)
    del dataset['Symbol']
    del dataset['Date']
    del dataset['Delivery']
    if adj==1:
        del dataset['UClose1']
        dataset.rename(columns={'Close':'TY_0'}, inplace=True)
    elif adj==0:
        del dataset['Close']
        dataset.rename(columns={'UClose1':'TY_0'}, inplace=True)
    table3 = dataset


    newdataset = table1
    newdataset['CL2_0'] = table2
    newdataset['TY_0'] = table3

    #for some reason when reading in from excel we get some NaN for CL2_0 valuebs that dont exist so delete those rows
    dframe = newdataset[pd.notnull(newdataset['CL2_0'])]
    return dframe

def plot_dataframe_in_matplotlib(the_dataframe):
    #calculate percent variance

    the_dataframe.pct_change(90).plot(subplots=True)

    #for plotting dataframe in matlplotlib
    the_dataframe.plot()
    plt.show()


def plot_dataframe_in_r():
    """THIS SHIT DOES NOT WORK"""

    import math, datetime
    import rpy2.robjects.lib.ggplot2 as ggplot2
    import rpy2.robjects as ro
    from rpy2.robjects.packages import importr
    #for plotting dataframe in r
    dframe = init_data("adjusted")

    #add back data column
    #init dataframe
    dataset = pd.DataFrame()
    #read in first table and add it to dataframe
    frame = pd.read_csv("/Users/ameerkambod/Trading/Algo-Trading/P11_PCA_Data1/Sheet1-Table 1.csv")
    dataset = dataset.append(frame,ignore_index=True)

    del dataset['Symbol']
    del dataset['Delivery']
    del dataset['UClose1']
    del dataset['Close']

    dframe['Date'] = dataset
    print dframe

    #create an r dataframe
    r_dataframe = com.convert_to_r_dataframe(dframe)
    robjects.globalenv['dataframe'] = r_dataframe



    robjects.r("""
    pdf("ggplot.pdf")
    #par(mfrow=c(3,1), lheight=1)


    Molten <- melt(dataframe, id.vars="Date")
    textplot(capture.output(ggplot(Molten, aes(x = Date, y=value)) + geom_point()))
    print("DONE")
    dev.off()


    """)

def do_pca_on_data(ajdusted_or_unadjust):
    if 'adjusted' in ajdusted_or_unadjust:
        dframe = init_data("adjusted")
    else:
        dframe = init_data("unadjust")



    #create an r dataframe
    r_dataframe = com.convert_to_r_dataframe(dframe)
    robjects.globalenv['dataframe'] = r_dataframe


    print "----"
    #print robjects.r.ls()



    #change output name
    robjects.r("""
    pdf("scale_center_adjustedclose.pdf")
    """)

    robjects.r("""
    par(mfrow=c(3,1), lheight=1)
    """)

    robjects.r("""
    textplot("Performing PCA on SP2_0,CL2_0,TY_0 Contracts", valign="top", fixed.width=TRUE, lspacing=1)
    dataframe.species <- colnames(dataframe)
    textplot(head(dataframe))
    """)

    #change how you do pca
    robjects.r("""
    #log.dataframe = log(dataframe)
    dataframe.pca <- prcomp(dataframe, center=TRUE, scale. = TRUE)
    print("loadings")
    print(dataframe.pca$x)
    """)



    robjects.r("""
    print("PCA Output")
    #print(dataframe.pca)
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

def do_pca_on_data_at_specific_intervals(num_of_rows, adjusted_or_unadjust):
    if 'adjusted' in adjusted_or_unadjust:
        dframe = init_data("adjusted")
    else:
        dframe = init_data("unadjust")

    #init dataframe
    columns = ['% explained by PC1', 'Weight - SP2', 'Weight-CL2', 'Weight-TY0']
    dataset = pd.DataFrame(columns=columns)

    #30 rows equals one month
    indexer= 0
    test = 0
    while num_of_rows*indexer <len(dframe.values):
        n_s_a = np.array([])

        #get a subset of the data specified by the num of rows
        subsetdf = dframe[num_of_rows*indexer:num_of_rows*(indexer+1)]
        #print subsetdf

        #do pca on that subset of data
        #create an r dataframe
        r_dataframe = com.convert_to_r_dataframe(subsetdf)
        robjects.globalenv['dataframe'] = r_dataframe

        robjects.r("""
        #log.dataframe = log(dataframe)
        dataframe.pca <- prcomp(dataframe, center=TRUE, scale. = TRUE)
        """)



        #get the amount of variance explained by the first PC
        summary = robjects.r("""summary(dataframe.pca)""")
        #print summary
        #print vars(summary[0])
        cum_proportion_of_first_pc = summary[-1][2]
        n_s_a = np.append(n_s_a, [cum_proportion_of_first_pc])
        #print "weight of first PC (%): ", cum_proportion_of_first_pc


        #get the weights
        weightsofpca = robjects.r("""print(dataframe.pca)""")
        #print "weights: \n", weightsofpca
        weight_of_first_column = weightsofpca[1][0] #sp2_0
        weight_of_second_column = weightsofpca[1][1] #cl2_0
        weight_of_third_column = weightsofpca[1][2] #ty_0
        n_s_a = np.append(n_s_a, [weight_of_first_column, weight_of_second_column, weight_of_third_column])

        #print "numpy storage array: ", n_s_a

        #append this loop to toal dataframe
        dataset.loc[len(dataset)+1] = n_s_a

        #increase indexer
        indexer += 1

    print "dataset: \n",  dataset
    return dataset

def do_pca_on_data_on_rolling_data(num_of_rows, adjusted_or_unadjust):
    if 'adjusted' in adjusted_or_unadjust:
        dframe = init_data("adjusted")
    else:
        dframe = init_data("unadjust")

    #init dataframe
    columns = ['% explained by PC1', 'Weight - SP2', 'Weight-CL2', 'Weight-TY0']
    dataset = pd.DataFrame(columns=columns)

    #30 rows equals one month
    indexer= 0
    test = 0
    while num_of_rows*indexer <len(dframe.values):
        n_s_a = np.array([])

        #get a subset of the data specified by the num of rows
        subsetdf = dframe[0:num_of_rows*(indexer+1)]
        #print subsetdf

        #do pca on that subset of data
        #create an r dataframe
        r_dataframe = com.convert_to_r_dataframe(subsetdf)
        robjects.globalenv['dataframe'] = r_dataframe

        robjects.r("""
        #log.dataframe = log(dataframe)
        dataframe.pca <- prcomp(dataframe, center=TRUE, scale. = TRUE)
        """)



        #get the amount of variance explained by the first PC
        summary = robjects.r("""summary(dataframe.pca)""")
        #print summary
        #print vars(summary[0])
        cum_proportion_of_first_pc = summary[-1][2]
        n_s_a = np.append(n_s_a, [cum_proportion_of_first_pc])
        #print "weight of first PC (%): ", cum_proportion_of_first_pc


        #get the weights
        weightsofpca = robjects.r("""print(dataframe.pca)""")
        #print "weights: \n", weightsofpca
        weight_of_first_column = weightsofpca[1][0] #sp2_0
        weight_of_second_column = weightsofpca[1][1] #cl2_0
        weight_of_third_column = weightsofpca[1][2] #ty_0
        n_s_a = np.append(n_s_a, [weight_of_first_column, weight_of_second_column, weight_of_third_column])

        #print "numpy storage array: ", n_s_a

        #append this loop to toal dataframe
        dataset.loc[len(dataset)+1] = n_s_a

        #increase indexer
        indexer += 1

    print "dataset: \n",  dataset
    return dataset


def do_pca_on_data_rolling():
    writer = pd.ExcelWriter('rolling_pca_analysis.xlsx')
    dataset1 = do_pca_on_data_on_rolling_data(30,'adjusted')
    dataset1.to_excel(writer,"Rolling PCA 1 Months")
    dataset2 = do_pca_on_data_on_rolling_data(90,'adjusted')
    dataset2.to_excel(writer,"Rolling PCA 3 Months")
    dataset3 = do_pca_on_data_on_rolling_data(180,'adjusted')
    dataset3.to_excel(writer,"Rolling PCA 6 Months")
    dataset4 = do_pca_on_data_on_rolling_data(320,'adjusted')
    dataset4.to_excel(writer,"Rolling PCA 1 Year")
    writer.save()

def do_pca_on_data_non_rolling():
    writer = pd.ExcelWriter('non_rolling_pca_analysis.xlsx')
    dataset1 = do_pca_on_data_at_specific_intervals(30,'adjusted')
    dataset1.to_excel(writer,"Non-Rolling PCA 1 Months")
    dataset2 = do_pca_on_data_at_specific_intervals(90,'adjusted')
    dataset2.to_excel(writer,"Non-Rolling PCA 3 Months")
    dataset3 = do_pca_on_data_at_specific_intervals(180,'adjusted')
    dataset3.to_excel(writer,"Non-Rolling PCA 6 Months")
    dataset4 = do_pca_on_data_at_specific_intervals(320,'adjusted')
    dataset4.to_excel(writer,"Non-Rolling PCA 1 Year")
    writer.save()







#plot_dataframe_in_r()
#do_pca_on_data('adjusted')

#to grab an object from r
#r_dataframe = com.convert_robj(robjects.globalenv['dataframe'])

#dframe = init_data('adjusted')
#plot_dataframe_in_matplotlib(dframe)

do_pca_on_data_rolling()




"""
foo = robjects.r['g']
rprint(foo)
time.sleep(30)
"""