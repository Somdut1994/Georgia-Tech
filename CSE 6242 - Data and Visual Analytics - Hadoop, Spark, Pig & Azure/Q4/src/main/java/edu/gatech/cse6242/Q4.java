package edu.gatech.cse6242;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import java.io.IOException;
import java.util.StringTokenizer;

public class Q4 {

	
	public static class TokenizerMapper1
    extends Mapper<Object, Text, Text, IntWritable>{

 private final static IntWritable one = new IntWritable(1);
 private Text word = new Text();

 public void map(Object key, Text value, Context context
                 ) throws IOException, InterruptedException {
   StringTokenizer itr = new StringTokenizer(value.toString());
   
   while (itr.hasMoreTokens()) {
     word.set(itr.nextToken());
     System.out.println(word);
     System.out.println(one);
     context.write(word, one);
   }
 }
}

public static class IntSumReducer1
    extends Reducer<Text,IntWritable,Text,IntWritable> {
 private IntWritable result = new IntWritable();

 public void reduce(Text key, Iterable<IntWritable> values,
                    Context context
                    ) throws IOException, InterruptedException {
   int sum = 0;
   for (IntWritable val : values) {
     sum += val.get();
   }
   result.set(sum);
   context.write(key, result);
 }
}

public static class TokenizerMapper2
extends Mapper<Object, Text, Text, IntWritable>{

private final static IntWritable one = new IntWritable(1);
private Text word = new Text();

public void map(Object key, Text value, Context context
             ) throws IOException, InterruptedException {
StringTokenizer itr = new StringTokenizer(value.toString());
itr.nextToken();
while (itr.hasMoreTokens()) {
 word.set(itr.nextToken());
 System.out.println(word);
 System.out.println(one);
 context.write(word, one);
}
}
}

public static class IntSumReducer2
extends Reducer<Text,IntWritable,Text,IntWritable> {
private IntWritable result = new IntWritable();

public void reduce(Text key, Iterable<IntWritable> values,
                Context context
                ) throws IOException, InterruptedException {
int sum = 0;
for (IntWritable val : values) {
 sum += val.get();
}
result.set(sum);
context.write(key, result);
}
}

  public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
    Job job = Job.getInstance(conf, "Q4");
    
    String tempout1 = "/user/cse6242/Q4output1_temp";
        
    job.setJarByClass(Q4.class);
    job.setMapperClass(TokenizerMapper1.class);
    job.setCombinerClass(IntSumReducer1.class);
    job.setReducerClass(IntSumReducer1.class);
    
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(IntWritable.class);
    
    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(tempout1));
    job.waitForCompletion(true);
    
    job = Job.getInstance(conf, "Q4");
    
    job.setJarByClass(Q4.class);
    job.setMapperClass(TokenizerMapper2.class);
    job.setCombinerClass(IntSumReducer2.class);
    job.setReducerClass(IntSumReducer2.class);
    
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(IntWritable.class);
    
    FileInputFormat.addInputPath(job, new Path(tempout1));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));
    job.waitForCompletion(true);
    
    System.exit(0);
    
  }
}