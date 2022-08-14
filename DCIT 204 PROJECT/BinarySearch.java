import java.util.Arrays;
import java.util.Scanner;

public class BinarySearch {
    int arr[] = { 3, 9,24,25,26,27,28,29,30,1, 6,14,15,16,17,18,19,24};
    public void binarySearch(){
        int option1;
        Scanner scanner2 = new Scanner(System.in);
        System.out.println("Please enter the number you want to search for using the binary search approach");
        option1 = scanner2.nextInt();
        Arrays.sort(arr);
        System.out.print("The sorted array is: ");
        for (int i : arr) {
            System.out.print(i + " ");
        }

        System.out.println();
        int index1 = Arrays.binarySearch(arr, option1);
        System.out.println("The number " + " " + option1 + " is at index " + index1);
    }
}
