def load_boolean_grid(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        bool_grid = []
        for line in lines:
            row = [char == '#' for char in line.strip()]
            bool_grid.append(row)
            
        return bool_grid
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

if __name__ == "__main__":
    file_path = "bool_grid.txt"
    bool_grid = load_boolean_grid(file_path)
    print(bool_grid)