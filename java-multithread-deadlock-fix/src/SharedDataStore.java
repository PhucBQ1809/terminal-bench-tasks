import java.util.ArrayList;
import java.util.List;

public class SharedDataStore {
    private int totalProcessingValue = 0;
    public final Object resourceA = new Object();
    public final Object resourceB = new Object();

    public SharedDataStore() {}

    public void addToTotal(int value) {
        this.totalProcessingValue += value;
    }

    public int getTotal() {
        return totalProcessingValue;
    }
}
