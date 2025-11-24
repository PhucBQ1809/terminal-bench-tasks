public class Worker implements Runnable {
    private final SharedDataStore dataStore;
    private final int valueToProcess;
    private final boolean useStrategyA;

    public Worker(SharedDataStore dataStore, int valueToProcess, boolean useStrategyA) {
        this.dataStore = dataStore;
        this.valueToProcess = valueToProcess;
        this.useStrategyA = useStrategyA;
    }

    @Override
    public void run() {
        try {
            process();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    private void process() throws InterruptedException {
        // BUG 2: Deadlock Potential.
        // Threads acquire locks in different orders based on the strategy flag.
        // If Thread 1 holds A and wants B, and Thread 2 holds B and wants A -> Deadlock.

        if (useStrategyA) {
            // Strategy A: Lock Resource A, then Resource B
            synchronized (dataStore.resourceA) {
                // Sleep ensures the other thread has time to grab the other lock
                // increasing the chance of deadlock significantly.
                Thread.sleep(10);

                synchronized (dataStore.resourceB) {
                    dataStore.addToTotal(valueToProcess);
                }
            }
        } else {
            // Strategy B: Lock Resource B, then Resource A
            synchronized (dataStore.resourceB) {
                Thread.sleep(10);

                synchronized (dataStore.resourceA) {
                    dataStore.addToTotal(valueToProcess);
                }
            }
        }
    }
}