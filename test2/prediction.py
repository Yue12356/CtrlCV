from pyspark import SparkConf,SparkContext
from pyspark.sql import SparkSession,SQLContext,HiveContext
from pyspark.sql.types import *
from pyspark.sql.functions import pandas_udf, PandasUDFType,udf
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.feature import StringIndexer,VectorAssembler,Normalizer
import pyspark.ml.classification as cl
import sqlite3,pandas
def CreateSparkContext():
    conf =SparkConf().setAppName("learnSpark").setMaster("local[*]").set("spark.ui.showConsoleProgress","false")
    sc=SparkContext(conf=conf)
    print("master:"+sc.master)
    sc.setLogLevel("WARN")
    spark=SparkSession.builder.config(conf=conf).getOrCreate()
    return sc,spark
    sc.setLogLevel("INFO")
def predict(team_a,team_b):
    col=['player_name','Usg%','Per','time']
    dataA=[]
    dataB=[]
    for player in team_a:
        playerInfo = team_a[player]
        name = playerInfo[0]
        time = int(playerInfo[1])
        Usgp = pd_df.loc[pd_df['player_name']==name,'Usg%'].values[0]
        Per = pd_df.loc[pd_df['player_name']==name,'Per'].values[0]
        dataA.append((name,Usgp,Per,time))
    #print(dataA)
    for player in team_b:
        playerInfo = team_b[player]
        name = playerInfo[0]
        #print(name)
        time = int(playerInfo[1])
        Usgp = pd_df.loc[pd_df['player_name']==name,'Usg%'].values[0]
        Per = pd_df.loc[pd_df['player_name']==name,'Per'].values[0]
        dataB.append((name,Usgp,Per,time))
    #print(dataB)
    col=['player_name','Usg%','Per','time']
    pd_tmp = pandas.DataFrame(dataA,columns=col)
    df_teamA = sqlContext.createDataFrame(pd_tmp)
    pd_tmp=pandas.DataFrame(dataB,columns=col)
    df_teamB = sqlContext.createDataFrame(pd_tmp)
    #df_teamA.show()
    #df_teamB.show()
    vector = VectorAssembler(inputCols=['Usg%','Per','time'],outputCol='features')
    normalizer = Normalizer(p=2.0, inputCol="features", outputCol="norm_test")
    pipeline = Pipeline(stages=[vector,normalizer])
    pipeline_fit = pipeline.fit(df_teamA)
    df_A = pipeline_fit.transform(df_teamA)
    #df_A.show()
    pipeline_fit = pipeline.fit(df_teamB)
    df_B = pipeline_fit.transform(df_teamB)
    #df_B.show()
    model = cl.RandomForestClassificationModel.load('Model_v3_0')
    predictions_A = model.transform(df_A)
    #predictions_A.show()
    predictions_B = model.transform(df_B)
    #predictions_B.show()
    percentageA = 100 / predictions_A.count()
    percentageB = 100 / predictions_B.count()
    a = predictions_A.where(predictions_A['prediction']==1).count()
    b = predictions_B.where(predictions_B['prediction']==0).count()
    percentage = (a* percentageA + b*percentageB)/2
    return percentage
# team_a={'item1':['德文-布克','30'],'item2':['易建联','30'],'item3':['勒布朗-詹姆斯','30'],'item4':['克莱-汤普森','30'],'item5':['斯蒂芬-库里','30']}
# team_b={'item1':['科比-布莱恩特','30'],'item2':['德维恩-韦德','30'],'item3':['凯尔-洛瑞','30'],'item4':['保罗-乔治','30'],'item5':['乔-约翰逊','30']}
# print("team_a has a {}% to win".format(predict(team_a,team_b)))
sc,spark = CreateSparkContext()
sqlContext = SQLContext(sc)
with sqlite3.connect('/root/django/test2/db.sqlite3') as db:
    pd_df = pandas.read_sql('SELECT * FROM playerAvg',con=db)
    #print(pd_df)