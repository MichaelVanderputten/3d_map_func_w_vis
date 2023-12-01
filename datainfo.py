def sort_2d_array(arr, axis):
    # Ensure a valid axis value is provided
    if axis not in [0, 1, 2]:
        raise ValueError("Invalid axis value. Please provide 0, 1, or 2.")

    # Define a lambda function as the key for sorting
    key_function = lambda item: item[axis]

    # Sort the array based on the specified axis
    sorted_array = sorted(arr, key=key_function)

    return sorted_array

def find_max_value(arr, axis):
    # Ensure a valid axis value is provided
    if axis not in [0, 1, 2]:
        raise ValueError("Invalid axis value. Please provide 0, 1, or 2.")

    # Find the maximum value
    values = [item[axis] for item in arr]
    max_value = max(values)

    return max_value

def find_min_value(arr, axis):
    # Ensure a valid axis value is provided
    if axis not in [0, 1, 2]:
        raise ValueError("Invalid axis value. Please provide 0, 1, or 2.")

    # Find the maximum value
    values = [item[axis] for item in arr]
    min_value = min(values)

    return min_value

def create_heatmap(point, step, axis):
    # Map values to RGB colors
    if(axis == 2):
        if(int(point[axis]/step < 0)):
            colors_rgb = (
            abs(int(point[axis]/step)),
            255-abs(int(point[axis]/step)),
            0,
            )
        else:
            colors_rgb = (
            255-abs(int(point[axis]/step)),
            abs(int(point[axis]/step)),
            0,
            )
    elif(axis == 1):
        if(int(point[axis]/step < 0)):
            colors_rgb = (
            abs(int(point[axis]/step)),
            0,
            255-abs(int(point[axis]/step)),
            )
        else:
            colors_rgb = (
            255-abs(int(point[axis]/step)),
            0,
            abs(int(point[axis]/step)),
            )
    else:
        if(int(point[axis]/step < 0)):
            colors_rgb = (
            0,
            abs(int(point[axis]/step)),
            255-abs(int(point[axis]/step)),
            )
        else:
            colors_rgb = (
            0,
            255-abs(int(point[axis]/step)),
            abs(int(point[axis]/step)),
            )

    return colors_rgb
