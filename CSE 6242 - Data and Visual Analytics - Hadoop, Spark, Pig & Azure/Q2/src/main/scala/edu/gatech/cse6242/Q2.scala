package edu.gatech.cse6242

import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf
import org.apache.spark.sql.SQLContext
import org.apache.spark.sql.functions._

object Q2 {
  
  case class Edge(src: Int, tgt: Int, weight: Int)
  
  def main(args: Array[String]) {
    val sc = new SparkContext(new SparkConf().setAppName("Q2"))
    val sqlContext = new SQLContext(sc)
    import sqlContext.implicits._

    // read the file
    val file = sc.textFile("hdfs://localhost:8020" + args(0))
    val df= file.map(_.split("\t")).map(p => Edge(p(0).trim.toInt, p(1).trim.toInt, p(2).trim.toInt)).toDF()         
    val df1 = df.filter("weight > 1")
    val tgtdf = df1.drop("src").groupBy("tgt").agg(sum("weight"))
    val srcdf = df1.drop("tgt").groupBy("src").agg(sum("weight"))
    val tgtsummary = tgtdf.withColumn("pluswt",col("sum(weight)"))
    val tgtcut = tgtsummary.drop("sum(weight)")
    val srcsummary = srcdf.withColumn("minuswt",col("sum(weight)"))
    val srccut = srcsummary.drop("sum(weight)")
    val joindf = tgtcut.join(srccut, $"tgt" === $"src")
    val netwt = joindf.withColumn("net",col("pluswt")-col("minuswt"))
    val finaldata = netwt.select("tgt","net")
    finaldata.map(x => x.mkString("\t")).saveAsTextFile("hdfs://localhost:8020" + args(1)) 
     
  }
}