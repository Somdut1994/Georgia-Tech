package edu.gatech.cse6242;

import java.io.IOException;
import org.apache.hadoop.fs.Path;
import java.util.StringTokenizer;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class Q1 {

	public static class TokenizerMapper extends Mapper<Object, Text, Text, IntWritable>{ 

	    private Text xyz = new Text();

	    public void map(Object key, Text value, Context context) throws IOException, InterruptedException {       
	    		
	    StringTokenizer itr = new StringTokenizer(value.toString());

	    itr.nextToken();            
	    xyz.set(itr.nextToken());
	        
	    IntWritable abc = new IntWritable(Integer.parseInt(itr.nextToken()));
	        context.write(xyz,abc);
	    }
	  }

	  public static class MyReducer extends Reducer<Text,IntWritable,Text,IntWritable> {
	    
	    private IntWritable high_weight = new IntWritable();

	    public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
	      int highest = 0;
	      
	      for (IntWritable var1 : values) 
	    {
	      highest = var1.get() > highest ? var1.get():highest;        
	        }

	      high_weight.set(highest);
	      context.write(key, high_weight);
	    }
	  }
	
	  public static void main(String[] args) throws Exception {
		    Configuration conf = new Configuration();
		    Job job = Job.getInstance(conf, "Q1");
		    
		    job.setJarByClass(Q1.class);
		    job.setMapperClass(TokenizerMapper.class);
		    job.setCombinerClass(MyReducer.class);
		    job.setReducerClass(MyReducer.class);
		    job.setOutputKeyClass(Text.class);
		    job.setOutputValueClass(IntWritable.class); 
		    
		    FileInputFormat.addInputPath(job, new Path(args[0]));
		    FileOutputFormat.setOutputPath(job, new Path(args[1]));
		    System.exit(job.waitForCompletion(true) ? 0 : 1);
		  }
}