import java.io.*;
import java.util.*;

public class ConsensusParser {
	
private HashMap<String, String> emotions;
	
	public ConsensusParser(File f) throws FileNotFoundException {
		Scanner s = new Scanner(f);
		emotions = new HashMap<String, String>();
		readFromText(s);
		}
	
	// method to read in each line from the consensus file and save the key emotion pair in a HashMap
	private void readFromText(Scanner s) {
		s.nextLine();
		while (s.hasNextLine()) {
			String line = s.nextLine();
			if (line.equals("[ ]+") || line.equals("")) {
				continue;
			}
			String[] part = line.split("[ ]+");
			if (part.length != 2) {
				continue;
			}
			String key = part[0];
			String emotion = part[1];
			emotions.put(key, emotion);
		}
	}
	
	// method to check the value in the HashMap vs. the guessed value. Returns true if they match and false if not
	private boolean checkConsensus (String guess) {
		String[] part = guess.split("[ ]+");
		String key = part[0];
		String emotion = part[1];
		if (emotions.containsKey(key)) {
			if (emotions.get(key).equals(emotion)) {
				return true;
			}
		}
		return false;
	}

}
