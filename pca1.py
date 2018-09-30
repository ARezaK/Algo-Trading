import pandas as pd
import numpy as np
import pandas.rpy.common as com
import rpy2.robjects as robjects
import matplotlib.pyplot as plt
import time
import plotly

#init plotly
plotly.tools.set_credentials_file(username='shemer77', api_key='m034bapk2z', stream_ids=['0373v57h06', 'cjbitbcr9j'])


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


def df_to_iplot(df):

    '''
    Coverting a Pandas Data Frame to Plotly interface
    '''
    x = df.index.values
    lines={}
    for key in df:
        lines[key]={}
        lines[key]["x"]=x
        lines[key]["y"]=df[key].values
        lines[key]["name"]=key

        #Appending all lines
    lines_plotly=[lines[key] for key in df]
    return lines_plotly

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
    frame = pd.read_csv("")
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

def do_pca_on_data_on_rolling_data(dframe, num_of_rows,whichpc):

    #init dataframe
    columns = ['% explained by PC'+str(whichpc), 'Weight - SP2', 'Weight-CL2', 'Weight-TY0']
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



        if whichpc ==1:
            weight_of_first_column = weightsofpca[1][0] #sp2_0
            weight_of_second_column = weightsofpca[1][1] #cl2_0
            weight_of_third_column = weightsofpca[1][2] #ty_0
            n_s_a = np.append(n_s_a, [weight_of_first_column, weight_of_second_column, weight_of_third_column])
        elif whichpc == 2:
            weight_of_first_column = weightsofpca[1][3] #sp2_0
            weight_of_second_column = weightsofpca[1][4] #cl2_0
            weight_of_third_column = weightsofpca[1][5] #ty_0
            n_s_a = np.append(n_s_a, [weight_of_first_column, weight_of_second_column, weight_of_third_column])
        elif whichpc == 3:
            weight_of_first_column = weightsofpca[1][6] #sp2_0
            weight_of_second_column = weightsofpca[1][7] #cl2_0
            weight_of_third_column = weightsofpca[1][8] #ty_0
            n_s_a = np.append(n_s_a, [weight_of_first_column, weight_of_second_column, weight_of_third_column])
        #print "numpy storage array: ", n_s_a

        #append this loop to toal dataframe
        dataset.loc[len(dataset)+1] = n_s_a

        #increase indexer
        indexer += 1

    #print "dataset: \n",  dataset
    return dataset

def do_pca_on_data_at_nonrolling_data(num_of_rows, adjusted_or_unadjust):
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


def do_pca_on_alldata_rolling():
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

def do_pca_on_alldata_non_rolling():
    writer = pd.ExcelWriter('non_rolling_pca_analysis.xlsx')
    dataset1 = do_pca_on_data_at_nonrolling_data(30,'adjusted')
    dataset1.to_excel(writer,"Non-Rolling PCA 1 Months")
    dataset2 = do_pca_on_data_at_nonrolling_data(90,'adjusted')
    dataset2.to_excel(writer,"Non-Rolling PCA 3 Months")
    dataset3 = do_pca_on_data_at_nonrolling_data(180,'adjusted')
    dataset3.to_excel(writer,"Non-Rolling PCA 6 Months")
    dataset4 = do_pca_on_data_at_nonrolling_data(320,'adjusted')
    dataset4.to_excel(writer,"Non-Rolling PCA 1 Year")
    writer.save()

def convert_dataframe_to_returns(dframe,period):
    returns =  dframe.pct_change(periods=period)
    #drop nan rows
    returns = returns[pd.notnull(returns['SP2_0'])]
    return returns

def create_portfolio_on_returns(timeframe):
    #converting into return series
    dataframe = init_data('adjusted')
    print dataframe

    returns = convert_dataframe_to_returns(dataframe,timeframe)

    #each stock gets 33,333 dollars
    current_allocation_sp20 = 33333
    current_allocation_cl20 = 33333
    current_allocation_ty0  = 33333

    #create a new dataframe that has one column Total portfolio balance
    columns = ["Total Portfolio Balance"]
    total_portfolio_balance = pd.DataFrame(columns=columns)
    total_portfolio_balance.loc[1] = '100000'
    print "total portfolio balance: \n ", total_portfolio_balance


    #iterover rows filling up total portfolio balance

    generator = returns.iterrows()
    for i, first in generator:
        sp2_pct_return = first[0]
        cl2_pct_return = first[1]
        ty0_pct_return = first[2]

        current_allocation_sp20 += current_allocation_sp20 * sp2_pct_return
        current_allocation_cl20 += current_allocation_cl20 * cl2_pct_return
        current_allocation_ty0 += current_allocation_ty0 * ty0_pct_return

        current_portfolio = current_allocation_sp20+ current_allocation_cl20+current_allocation_ty0

        #print current_portfolio

        #append this balnce to toal dataframe
        total_portfolio_balance.loc[len(total_portfolio_balance)+1] = current_portfolio

    print "new total portfolio balance: \n", total_portfolio_balance

    total_portfolio_balance['total_portfolio_balance_float'] = total_portfolio_balance['Total Portfolio Balance'].astype(float)
    del total_portfolio_balance['Total Portfolio Balance']

    return total_portfolio_balance

def create_portfolio_on_pca(pcadataframe,returns,timeframe,whichPC):
    current_account_balance = 100000


    #create a new dataframe that has one column Total portfolio balance
    columns = ["Total Portfolio Balance"]
    total_portfolio_balance = pd.DataFrame(columns=columns)
    total_portfolio_balance.loc[1] = '100000'
    print "total portfolio balance: \n ", total_portfolio_balance

     #iterover rows filling up total portfolio balance

    generator = pcadataframe.iterrows()
    for i, first in generator:
        #i starts at 1
        weight_of_sp2 = first[1]
        weight_of_cl2 = first[2]
        weight_of_ty0 = first[3]

        pct_to_allocate_to_sp2 = np.power(weight_of_sp2,2)
        pct_to_allocate_to_cl2 = np.power(weight_of_cl2,2)
        pct_to_allocate_to_ty0 = np.power(weight_of_ty0,2)

        amount_of_money_weighted_to_sp2 = pct_to_allocate_to_sp2*current_account_balance
        amount_of_money_weighted_to_cl2 = pct_to_allocate_to_cl2*current_account_balance
        amount_of_money_weighted_to_ty0 = pct_to_allocate_to_ty0*current_account_balance

        #get subset of daily returns corresponding to that PC timeframe
        subsetdf = returns[i*timeframe:(i+1)*timeframe]

        print subsetdf
        generator2 = subsetdf.iterrows()
        for i2, first2 in generator2:
            sp2_pct_return = first2[0]
            cl2_pct_return = first2[1]
            ty0_pct_return = first2[2]

            amount_of_money_weighted_to_sp2 += amount_of_money_weighted_to_sp2 * sp2_pct_return
            amount_of_money_weighted_to_cl2 += amount_of_money_weighted_to_cl2 * cl2_pct_return
            amount_of_money_weighted_to_ty0 += amount_of_money_weighted_to_ty0 * ty0_pct_return



            #print "current: \n", current_account_balance
            #i can either move this in the loop or out of it
            current_account_balance = amount_of_money_weighted_to_sp2+ amount_of_money_weighted_to_cl2+amount_of_money_weighted_to_ty0
            #append this balnce to toal dataframe
            total_portfolio_balance.loc[len(total_portfolio_balance)+1] = current_account_balance
            #print "acct_balance: \n", current_account_balance



    print "new total portfolio balance: \n", total_portfolio_balance

    total_portfolio_balance['PCA_'+str(whichPC)] = total_portfolio_balance['Total Portfolio Balance'].astype(float)
    del total_portfolio_balance['Total Portfolio Balance']

    return total_portfolio_balance


def create_pca_portfolio(whichPC,timeframe):
    dataframe = init_data('adjusted')

    #create dataframe of daily percentage returns
    returns = convert_dataframe_to_returns(dataframe,1)

    dataset = do_pca_on_data_on_rolling_data(returns, 30, whichPC)
    print "datastesdfsd"
    #print "dataset: \n", dataset
    pca_portfolio = create_portfolio_on_pca(dataset,returns,timeframe,whichPC)
    print "SDFL;jsdf"
    return pca_portfolio


# dataset1 = do_pca_on_data_at_specific_intervals(320,'adjusted')
# #lets delete the first column (% explaiend by variance)
# del dataset1['% explained by PC1']
#
# plt.figure()
#
# dataset1.plot()
#
# plt.savefig("non-rolling - 1Y intervals")
#
# #
#plot_dataframe_in_r()
#do_pca_on_data('adjusted')

#to grab an object from r
#r_dataframe = com.convert_robj(robjects.globalenv['dataframe'])

#dframe = init_data('adjusted')
#plot_dataframe_in_matplotlib(dframe)

pca1_portfolio = create_pca_portfolio(1,30)
pca2_portfolio = create_pca_portfolio(2,30)
pca3_portfolio = create_pca_portfolio(3,30)
base_portfolio = create_portfolio_on_returns(1)
print "pca protfoiltio: \n ", pca1_portfolio
print "base portfiolio: \n", base_portfolio


#merge the two dataframes. This doesnt work b/c pca protfiolio is only 2000 rows
pca1_portfolio['base_portfolio'] = base_portfolio['total_portfolio_balance_float']
pca1_portfolio['pca2'] = pca2_portfolio['PCA_2']
pca1_portfolio['pca3'] = pca3_portfolio['PCA_3']

plotly.plotly.plot(df_to_iplot(pca1_portfolio))
pca1_portfolio.plot()
#base_portfolio.plot()
plt.figure()
plt.show()





"""
foo = robjects.r['g']
rprint(foo)
time.sleep(30)
"""
