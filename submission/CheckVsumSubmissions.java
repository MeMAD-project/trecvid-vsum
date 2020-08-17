import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.*;

public class CheckVsumSubmissions{
	static int maxShots;
	static float maxTime;
	static String[] queries;
	static int minShotId;
	static int maxShotId;
	static int numErrors;
	static LinkedList<String> errorMsgs;
	static int maxPriority;
	static int currentRun;
	static float currentMaxTime; 
	static int currentMaxShots;
	static int run;

	public static void main(String[] args){
		if(args.length != 1){
			System.out.println("To run: ");
			System.out.println("java CheckVsumSubmissions <path-to-file>)>");
			System.exit(0);
		}
		String file = args[0];
		
		//run = (int)Integer.parseInt(args[1]);
		queries = new String[3];
		queries[0] = "Janine";
		queries[1] = "Ryan";
		queries[2] = "Stacey";
		minShotId = 175;
		maxShotId = 185;
		maxPriority = 4;
		maxTime = 150.00f;
		maxShots = 5;
		
		numErrors = 0;
		errorMsgs = new LinkedList<String>();
		String line;
		try{
		BufferedReader reader = new BufferedReader(new FileReader(file));
		while((line = reader.readLine()) != null){
			processLine(line.trim());
		}
		System.out.println("Check of " + file + " Complete. " + numErrors + " Error(s) found.");
		if(numErrors > 0){
			System.out.println("Please see details below:");
			for(int i  = 0; i < numErrors; i++){
				System.out.println("Error: " + (i+1));
				System.out.println(errorMsgs.get(i));
			}
		}
		}catch(Exception e){
			e.printStackTrace();
		}
	}
	
	static void processLine(String line){
		if(line.startsWith("<videoSummarizationRunResult")){
			processRun(line);
		}else if(line.startsWith("<videoSummarizationTopicResult")){
			processSubmission(line);
		}else if(line.startsWith("<item")){
			processEntry(line);
		}
	}
	
	static void processRun(String line){
		int priority;
		int priorityIndex = line.indexOf("priority=");
		int endPriorityIndex = line.substring(priorityIndex+10).indexOf("\"") + priorityIndex+10;
		priority = (int)Integer.parseInt(line.substring(priorityIndex+10,endPriorityIndex).trim());
		if(priority > maxPriority){
			numErrors++;
			errorMsgs.add("Too many runs submitted. Must be <= " + maxPriority + " Runs.");
		}else{
			currentRun = priority;
			currentMaxTime = maxTime * currentRun;
			currentMaxShots = maxShots * currentRun;
		}
	}
	
	static void processSubmission(String line){
		int numShots;
		float summTime;
		String query;
		int numShotsIndex = line.indexOf("numShots=");
		int endNumShotsIndex = line.substring(numShotsIndex+10).indexOf("\"") + numShotsIndex+10;
		int queryIndex = line.indexOf("target=");
		int endQueryIndex = line.substring(queryIndex+8).indexOf("\"") + queryIndex+8;
		int summTimeIndex = line.indexOf("summTime=");
		int endSummTimeIndex = line.substring(summTimeIndex+10).indexOf("\"") + summTimeIndex+10;
		numShots = (int)Integer.parseInt(line.substring(numShotsIndex+10,endNumShotsIndex).trim());
		summTime = Float.parseFloat(line.substring(summTimeIndex+10,endSummTimeIndex).trim());
		query = line.substring(queryIndex+8,endQueryIndex).trim();
		if(!query.equalsIgnoreCase(queries[0]) && !query.equalsIgnoreCase(queries[1]) && !query.equalsIgnoreCase(queries[2])){
			numErrors++;
			errorMsgs.add("Invalid Target: " + query + ". Must be " + queries[0] + ", " + queries[1] + ", or " + queries[2] + ".");
		}
		if(numShots > currentMaxShots){
			numErrors++;
			errorMsgs.add("Too many shots included, must be <= " + currentMaxShots + " Shots for run " + currentRun + ".");
		}
		if(summTime > currentMaxTime){
			numErrors++;
			errorMsgs.add("Total summary time is too long, must be <= " + currentMaxTime + " Seconds for run " + currentRun + ".");
		}
	}
	
	static void processEntry(String line){
		int shotIndex = line.indexOf("shotId=\"shot");
		int endShotIndex = line.substring(shotIndex+12).indexOf("_") + shotIndex+12;
		int shotId = (int)Integer.parseInt(line.substring(shotIndex+12,endShotIndex).trim());
		if(shotId < minShotId){
			numErrors++;
			errorMsgs.add("Invalid Shot! shot" + shotId + "_###. Must be above shot" + minShotId + "_### and below shot" + maxShotId + "_###.");
		}else if(shotId > maxShotId){
			numErrors++;
			errorMsgs.add("Invalid Shot! shot" + shotId + "_###. Must be above shot" + minShotId + "_### and below shot" + maxShotId + "_###.");
		}
	}
}
/*
<!--  Example video summarization results for a vsum run   -->
<!DOCTYPE videoSummarizationResults SYSTEM "https://www-nlpir.nist.gov/projects/tv2020/dtds/videoSummarizationResults.dtd">
<videoSummarizationResults>
	<videoSummarizationRunResult pid="SiriusCyberCo" priority="2" desc="This automatic run uses algorithm 1">
		<videoSummarizationTopicResult target="Stacey" numShots="10" summTime="29.7">
			<item seqNum="1" shotId="shot4324_2"/>
			<item seqNum="2" shotId="shot484_4"/>
			<item seqNum="3" shotId="shot459_43"/>
			<item seqNum="4" shotId="shot1663_34"/>
			<item seqNum="5" shotId="shot2415_16"/>
			<item seqNum="6" shotId="shot7_765"/>
			<item seqNum="7" shotId="shot35_4"/>
			<item seqNum="8" shotId="shot3246_54"/>
			<item seqNum="9" shotId="shot22_255"/>
			<item seqNum="10" shotId="shot432_24"/>
		</videoSummarizationTopicResult>
		<!--  ...  -->
		<videoSummarizationTopicResult target="Max" numShots="10" summTime="35.4">
			<item seqNum="1" shotId="shot459_5"/>
			<item seqNum="2" shotId="shot1957_794"/>
			<item seqNum="3" shotId="shot7_54"/>
			<item seqNum="4" shotId="shot35_679"/>
			<item seqNum="5" shotId="shot1_712"/>
			<item seqNum="6" shotId="shot3246_461"/>
			<item seqNum="7" shotId="shot22_15"/>
			<item seqNum="8" shotId="shot1663_84"/>
			<item seqNum="9" shotId="shot484_67"/>
			<item seqNum="10" shotId="shot666_43"/>
		</videoSummarizationTopicResult>
	</videoSummarizationRunResult>
</videoSummarizationResults>
*/