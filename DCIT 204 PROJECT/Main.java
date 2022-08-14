import java.util.Arrays;
import java.util.Scanner;

class Main {
    public static void main(String args[]) {
        String option;
        System.out.println("Please select the type of sorting you want to perform");
        System.out.println("1.Quick Sort");
        System.out.println("2.Insertion Sort");
        System.out.println("3.Merge Sort");
        System.out.println("4.Heap Sort");
        System.out.println("5.Selection Sort");
        System.out.println("6.Radix Sort");
        System.out.println("7.Bucket Sort");
        System.out.println("8.Counting Sort");
        Scanner scanner = new Scanner(System.in);
        option = scanner.next();


        // INSTANCE OF QUICK SORT CLASS
        if(option.equals("1")){
           Quicksort quicksort = new Quicksort();
           quicksort.quickSortMethod();
        }

        // INSTANCE OF THE SELECTION SORT CLASS
       if(option.equals("2")){
           InsertionSort insertionSort = new InsertionSort();
           insertionSort.insertionSortMethod();
       }

        // INSTANCE OF THE MERGESORT CLASS
       if(option.equals("3")){
           mergeSort merge = new mergeSort();
           merge.mergeSortMethod();

       }

        // INSTANCE OF THE HEAPSORT CLASS
       if (option.equals("4")){
           heapSort hs = new heapSort();
           hs.heapSortMethod();
       }

        // INSTANCE OF THE SELECTIONSORT
       if (option.equals("5")){
           selectionSort selection = new selectionSort();
           selection.selectionSortMethod();
       }
        // INSTANCE OF THE RADIXSORT
       if (option.equals("6")){
           RadixSort radixSort = new RadixSort();
          radixSort.RadixMethod();
       }
       // INSTANCE OF THE BUCKETSORT
       if (option.equals("7")){
           BucketSort bucketSort = new BucketSort();
           bucketSort.bucketSortMethod();
       }
       // INSTANCE OF THE COUNTINGSORT CLASS
       if (option.equals("8")){
           CountingSort countingSort = new CountingSort();
           countingSort.countingSortMethod();
       }

    }
}