# Closest Pair Algorithm with Visualization 🚀

This project implements the **Closest Pair of Points** problem using the **Divide & Conquer** algorithm and visualizes the steps with **Matplotlib animations**.

## 🔹 Features
- ⚡ **Efficient Divide & Conquer algorithm** (O(n log n))
- 🔍 **Naive brute-force method** for comparison (O(n²))
- 🎥 **Animated visualization** using Matplotlib
- 📂 **Reads points from a text file** for easy input

## 📌 Installation & Usage

1. Clone this repository or download the files:
   ```bash
   git clone https://github.com/hasanemreusta/closest-pair.git
   cd closest-pair
   ```

2. Install dependencies:
   ```bash
   pip install matplotlib
   ```

3. Run the script:
   ```bash
   python closest_pair.py
   ```

4. Provide a text file (`test_points.txt`) with points in the following format:
   ```
   1.0 3.0
   4.0 7.0
   5.0 9.0
   2.0 8.0
   ```

## 🖼️ Example Visualization
The script creates an animated visualization where:
- **Red dashed line** → Splitting line in Divide & Conquer
- **Orange points** → Points in the "strip" area being checked
- **Green line** → The closest pair found

## ⚖️ Complexity
- **Naive Approach** → O(n²)
- **Divide & Conquer** → O(n log n)

