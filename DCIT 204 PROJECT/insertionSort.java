import java.util.Arrays;

class InsertionSort {
    int[] data = { 9, -7, -3, 0, 1, 1, 2, 3, 4, 4, 5, 5, 7, 7, 8, 8, 9 };
    void insertionSort(int array[]) {
        int size = array.length;

        for (int step = 1; step < size; step++) {
            int key = array[step];
            int j = step - 1;

            // Compare key with each element on the left of it until an element smaller than
            // it is found.
            // For descending order, change key<array[j] to key>array[j].
            while (j >= 0 && key < array[j]) {
                array[j + 1] = array[j];
                --j;
            }

            // Place key at after the element just smaller than it.
            array[j + 1] = key;
        }
    }

    public void insertionSortMethod(){
        InsertionSort is = new InsertionSort();
        is.insertionSort(data);
        System.out.println(" The sorted Array in Ascending Order using The Insertion sorting approach: ");
        System.out.println(Arrays.toString(data));
    }
}
