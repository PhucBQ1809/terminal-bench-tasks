import java.util.Random;

public class BankService {
    // Number of accounts
    private static final int NUM_ACCOUNTS = 10;
    // Initial balance per account
    private static final int INITIAL_BALANCE = 1000;
    // Total transactions to simulate
    private static final int NUM_TRANSACTIONS = 1000;
    // Number of threads
    private static final int NUM_THREADS = 20;

    private final Account[] accounts;

    public BankService() {
        accounts = new Account[NUM_ACCOUNTS];
        for (int i = 0; i < NUM_ACCOUNTS; i++) {
            accounts[i] = new Account(i, INITIAL_BALANCE);
        }
    }

    public static void main(String[] args) {
        BankService bank = new BankService();
        bank.runSimulation();
    }

    public void runSimulation() {
        System.out.println("Starting simulation...");
        Thread[] threads = new Thread[NUM_THREADS];
        Random rand = new Random();

        for (int i = 0; i < NUM_THREADS; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < NUM_TRANSACTIONS / NUM_THREADS; j++) {
                    int fromId = rand.nextInt(NUM_ACCOUNTS);
                    int toId = rand.nextInt(NUM_ACCOUNTS);
                    // Don't transfer to self
                    while (fromId == toId) {
                        toId = rand.nextInt(NUM_ACCOUNTS);
                    }
                    transfer(accounts[fromId], accounts[toId], rand.nextInt(50));
                }
            });
            threads[i].start();
        }

        // Wait for all threads to finish
        for (Thread t : threads) {
            try {
                t.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        System.out.println("All transactions completed.");
    }

    public void transfer(Account from, Account to, int amount) {
        // BUG: Locking order is dependent on function arguments.
        // If T1 calls transfer(A, B) and T2 calls transfer(B, A) concurrently,
        // T1 locks A, T2 locks B -> Deadlock when they try to acquire the second lock.
        synchronized (from) {
            // Artificial delay to increase deadlock probability
            try { Thread.sleep(1); } catch (InterruptedException e) {}

            synchronized (to) {
                if (from.withdraw(amount)) {
                    to.deposit(amount);
                    // System.out.println("Transferred " + amount + " from " + from.id + " to " + to.id);
                }
            }
        }
    }

    static class Account {
        final int id;
        int balance;

        public Account(int id, int balance) {
            this.id = id;
            this.balance = balance;
        }

        public void deposit(int amount) {
            balance += amount;
        }

        public boolean withdraw(int amount) {
            if (balance >= amount) {
                balance -= amount;
                return true;
            }
            return false;
        }
    }
}