import java.util.Scanner;
import java.util.Arrays;

public class Search {
    public static void main(String args[]){

        Scanner scanner1 = new Scanner(System.in);
        String option;
        System.out.println("Please choose the type of search you want to perform.");
        String linear = "1. Linear";
        String binary = "2. Binary";
        System.out.println(linear);
        System.out.println(binary);
        option = scanner1.next();

        //INSTANCE OF THE LINEAR SEARCH CLASS
        if(option.equals("1")){
            Linear_Search linear1 = new Linear_Search();
            linear1.lineaSearch();
        }


        //INSTANCE OF THE BINARY SEARCH CLASS

        if(option.equals("2")){
         BinarySearch binarySearch = new BinarySearch();
         binarySearch.binarySearch();
        }

    }
}