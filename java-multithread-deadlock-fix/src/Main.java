import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        SharedDataStore dataStore = new SharedDataStore();
        List<Thread> threads = new ArrayList<>();
        String csvFile = "config/data.csv";

        try (BufferedReader br = new BufferedReader(new FileReader(csvFile))) {
            String line;
            int lineCount = 0;
            while ((line = br.readLine()) != null) {
                try {
                    int value = Integer.parseInt(line.trim());
                    // Alternate strategies to induce deadlock potential
                    // Even lines act as "Strategy A" threads, Odd lines as "Strategy B" threads
                    boolean strategyA = (lineCount % 2 == 0);

                    Worker worker = new Worker(dataStore, value, strategyA);
                    Thread t = new Thread(worker, "Worker-" + lineCount);
                    threads.add(t);
                    t.start();

                    lineCount++;
                } catch (NumberFormatException e) {
                    // Ignore bad lines
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
            System.exit(1);
        }

        // Wait for all threads to finish
        for (Thread t : threads) {
            try {
                t.join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

        System.out.println("Processing Complete. Final Total: " + dataStore.getTotal());
    }
}