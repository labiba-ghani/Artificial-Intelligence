def binary_search(arr, target):
    """Finds the index of a target value within a sorted array.

    Returns the index if found, or -1 if the target is not present.
    """
    low = 0
    high = len(arr) - 1
    step = 1

    while low <= high:
        mid = (low + high) // 2
        print(f"Step #{step}: Low={low}, High={high}, Mid={mid} (Value={arr[mid]})")

        if arr[mid] == target:
            print(f"Successful Search! Found {target} at index {mid}.\n")
            return mid
        elif arr[mid] < target:
            # Target is larger, search right half
            low = mid + 1
        else:
            # Target is smaller, search left half
            high = mid - 1

        step += 1

    print(f"Target {target} not found in the array.\n")
    return -1



if __name__ == "__main__":
    sample_array = [6, 12, 17, 23, 38, 45, 77, 84, 90]
    target_value = 45

    print(f"Array: {sample_array}")
    print(f"Searching for: {target_value}\n")
    result = binary_search(sample_array, target_value)