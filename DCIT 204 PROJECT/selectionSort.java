import java.util.Arrays;
public class  selectionSort {
    int[] data = {9, -7, -3, 0, 1, 1, 2, 3, 4, 4, 5, 5, 7, 7, 8, 8, 9};

    public static void selectionSort(int[] arr) {
        for (int i = 0; i < arr.length - 1; i++) {
            int index = i;
            for (int j = i + 1; j < arr.length; j++) {
                if (arr[j] < arr[index]) {
                    index = j;//searching for lowest index
                }
            }
            int smallerNumber = arr[index];
            arr[index] = arr[i];
            arr[i] = smallerNumber;
        }
    }

    public void selectionSortMethod() {
        System.out.println("The unsorted array");
        for (int i : data) {
            System.out.print(i + " ");
        }
        System.out.println();
        selectionSort(data);
        System.out.println(" The sorted Array in Ascending Order using The Selection sorting approach: ");
        for (int i : data) {
            System.out.print(i + " ");
        }
    }
}